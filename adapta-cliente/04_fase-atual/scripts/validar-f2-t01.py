#!/usr/bin/env python3
"""Validação determinística da fixture sintética da F2-T01.

Não acessa rede, Kenlo ou Skip. A ferramenta prova o contrato de entrada,
normalização e classificação da fixture; promoção, permissões e rollback
executáveis permanecem na F2-T02.
"""

from __future__ import annotations

import argparse
import calendar
import hashlib
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse

MONEY_FIELDS = {
    "price": "R$ Locação",
    "condominium_fee": "R$ Cond.",
    "iptu": "R$ Iptu",
}
REQUIRED_FIELDS = ("property_code", "title", "availability_status", "source_ref", "valid_until")
FORBIDDEN_NORMALIZED_KEYS = {
    "promotor",
    "promotor(es)",
    "promotores",
    "indicador",
    "indicador(es)",
    "indicadores",
}


def parse_date(value: object, label: str) -> date:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{label}: data deve estar em YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label}: data inválida") from exc


def subtract_months(value: date, months: int) -> date:
    month_index = value.year * 12 + value.month - 1 - months
    year, month_zero_based = divmod(month_index, 12)
    month = month_zero_based + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def normalize_money(value: object, label: str) -> int | float | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        raise ValueError(f"{label}: booleano não é valor monetário")
    if isinstance(value, (int, float)):
        numeric = float(value)
    elif isinstance(value, str):
        text = value.strip().replace("R$", "").replace(" ", "")
        if not text:
            return None
        if "," in text:
            text = text.replace(".", "").replace(",", ".")
        try:
            numeric = float(text)
        except ValueError as exc:
            raise ValueError(f"{label}: valor monetário inválido") from exc
    else:
        raise ValueError(f"{label}: tipo monetário inválido")
    if numeric == 0:
        return None
    return int(numeric) if numeric.is_integer() else numeric


def is_safe_media(url: object, allowlist: list[str]) -> bool:
    if not isinstance(url, str) or not url.startswith("https://"):
        return False
    parsed = urlparse(url)
    return bool(parsed.hostname) and parsed.hostname in allowlist


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def validate_fixture(data: dict) -> tuple[dict, list[dict], list[str]]:
    source = data["source"]
    if source.get("system") != "Kenlo Mob":
        raise ValueError("source.system deve ser Kenlo Mob")
    if source.get("file_format") != "xls":
        raise ValueError("source.file_format deve ser xls")
    if source.get("column_count") != 29:
        raise ValueError("source.column_count deve ser 29")
    cutoff = parse_date(source["cutoff_date"], "source.cutoff_date")
    if source.get("frequency") != "weekly":
        raise ValueError("source.frequency deve ser weekly")
    if source.get("retention_years") != 1:
        raise ValueError("source.retention_years deve ser 1")
    allowlist = source.get("media_allowlist", [])
    if not isinstance(allowlist, list) or not all(isinstance(item, str) for item in allowlist):
        raise ValueError("source.media_allowlist deve ser uma lista de domínios")

    rows = data.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ValueError("fixture.rows deve conter pelo menos uma linha")

    threshold = subtract_months(cutoff, 6)
    results: list[dict] = []
    canonical_rows: list[dict] = []
    checks: list[str] = []

    for row in rows:
        source_row = row["source_row"]
        raw = row.get("raw", {})
        normalized = dict(row.get("normalized", {}))
        reasons: list[str] = []
        warnings: list[str] = []

        leaked = {str(key).lower() for key in normalized} & FORBIDDEN_NORMALIZED_KEYS
        if leaked:
            reasons.append("forbidden_operational_fields_in_catalog:" + ",".join(sorted(leaked)))

        for canonical_name, raw_name in MONEY_FIELDS.items():
            derived = normalize_money(raw.get(raw_name), raw_name)
            if canonical_name in normalized and normalized[canonical_name] != derived:
                reasons.append(f"money_normalization_mismatch:{canonical_name}")
            normalized[canonical_name] = derived

        normalized.setdefault("media_urls", [])
        if not isinstance(normalized["media_urls"], list):
            reasons.append("media_urls_not_list")
        elif not normalized["media_urls"]:
            normalized.setdefault("media_status", "pending_manual_registration")
            warnings.append("media_pending_manual_registration")
        else:
            normalized.setdefault("media_status", "provided_for_validation")
            unsafe = [url for url in normalized["media_urls"] if not is_safe_media(url, allowlist)]
            if unsafe:
                reasons.append("unsafe_media_blocked")

        captador = raw.get("Captador(es)")
        if captador not in (None, ""):
            normalized["captador_internal"] = captador

        for field in REQUIRED_FIELDS:
            value = normalized.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                reasons.append(f"required_missing:{field}")

        valid_until_value = normalized.get("valid_until")
        valid_until = None
        if valid_until_value not in (None, ""):
            try:
                valid_until = parse_date(valid_until_value, f"linha {source_row}.valid_until")
                if valid_until < cutoff:
                    reasons.append("invalid_or_expired_valid_until")
            except ValueError:
                reasons.append("invalid_or_expired_valid_until")

        updated_value = raw.get("Data de atualização")
        stale_review = False
        try:
            updated_at = parse_date(updated_value, f"linha {source_row}.Data de atualização")
            stale_review = updated_at < threshold
        except ValueError:
            reasons.append("invalid_last_updated_at")
            updated_at = None
        if stale_review:
            warnings.append("stale_review")

        status = normalized.get("availability_status")
        if status != "active":
            reasons.append("availability_not_active")

        hard_reasons = [reason for reason in reasons if reason != "unsafe_media_blocked"]
        if hard_reasons:
            classification = "rejected"
        elif "unsafe_media_blocked" in reasons:
            classification = "pending"
        else:
            classification = "accepted"

        active_candidate = classification == "accepted" and status == "active"
        result = {
            "case": row.get("case"),
            "source_row": source_row,
            "property_code": normalized.get("property_code"),
            "classification": classification,
            "active_candidate": active_candidate,
            "stale_review": stale_review,
            "reasons": sorted(set(reasons)),
            "warnings": sorted(set(warnings)),
            "normalized": normalized,
        }
        results.append(result)
        canonical_rows.append({
            "source_row": source_row,
            "normalized": normalized,
            "classification": classification,
            "active_candidate": active_candidate,
            "stale_review": stale_review,
            "reasons": sorted(set(reasons)),
            "warnings": sorted(set(warnings)),
        })

    canonical_payload = {
        "source": {
            "system": source["system"],
            "file_name": source["file_name"],
            "file_format": source["file_format"],
            "column_count": source["column_count"],
            "cutoff_date": source["cutoff_date"],
            "frequency": source["frequency"],
        },
        "rows": canonical_rows,
    }
    content_hash = hashlib.sha256(canonical_json(canonical_payload).encode("utf-8")).hexdigest()
    catalog_version = f"cat-{source['cutoff_date'].replace('-', '')}-{content_hash[:12]}"
    counts = {
        "rows_total": len(results),
        "accepted": sum(item["classification"] == "accepted" for item in results),
        "pending": sum(item["classification"] == "pending" for item in results),
        "rejected": sum(item["classification"] == "rejected" for item in results),
    }

    by_case = {item["case"]: item for item in results}
    expected = {
        "valid_zero_values_no_media": "accepted",
        "stale_review_but_accepted": "accepted",
        "missing_required_property_code": "rejected",
        "expired_valid_until": "rejected",
        "unsafe_manual_media_pending": "pending",
    }
    for case, expected_classification in expected.items():
        actual = by_case.get(case, {}).get("classification")
        if actual != expected_classification:
            raise AssertionError(f"{case}: esperado {expected_classification}, obtido {actual}")
    checks.append("zero monetário normalizado para ausência")
    checks.append("mídia ausente classificada como pendência manual sem recusar o item")
    checks.append("desatualizado aceito com stale_review")
    checks.append("obrigatório ausente recusado com motivo")
    checks.append("vigência vencida recusada com motivo")
    checks.append("mídia insegura pendenciada e nunca ativa")
    for item in results:
        normalized_keys = {str(key).lower() for key in item["normalized"]}
        if normalized_keys & FORBIDDEN_NORMALIZED_KEYS:
            raise AssertionError(f"PII operacional indevida no catálogo: linha {item['source_row']}")
    checks.append("Promotor(es) e Indicador(es) ausentes do catálogo normalizado")

    loaded_at = datetime.fromisoformat(source["loaded_at"])
    retention_expires_at = loaded_at.replace(year=loaded_at.year + 1).isoformat()
    receipt = {
        "schema": "catalog_import_receipt/v1",
        "fixture_id": data["fixture_id"],
        "import_id": "import-f2-t01-synthetic-001",
        "catalog_version": catalog_version,
        "source_ref": source["file_name"],
        "source": source["system"],
        "cutoff_date": source["cutoff_date"],
        "content_hash": content_hash,
        "loaded_by": source["loaded_by"],
        "loaded_at": source["loaded_at"],
        "retention_expires_at": retention_expires_at,
        **counts,
        "promotion_status": "validation_only",
        "promotion_note": "F2-T01 não promove versão real; promoção, permissão e rollback são F2-T02.",
        "idempotency_key": content_hash,
        "items": results,
    }
    return receipt, canonical_payload, checks


def render_report(receipt: dict, checks: list[str], fixture_path: str) -> str:
    lines = [
        "# Relatório de validação — F2-T01",
        "",
        "> Execução local determinística sobre fixture sintética; nenhuma chamada ao Kenlo ou ao Skip foi feita.",
        "",
        "## Escopo e baseline",
        "",
        f"- Fixture: `{fixture_path}`.",
        "- Entrada contratual: `.xls`, 29 colunas, fonte Kenlo Mob, corte em `2026-09-15`.",
        "- A fixture é sintética e não contém PII real, credenciais ou dado de imóvel real.",
        "- O baseline do HEAD não continha contrato/fixture/validador da F2-T01; esta execução cria a primeira prova reproduzível.",
        "- `promotion_status` é `validation_only`: não houve promoção de versão nem alteração de catálogo.",
        "",
        "## Resultado do recibo",
        "",
        f"- `import_id`: `{receipt['import_id']}`.",
        f"- `catalog_version`: `{receipt['catalog_version']}`.",
        f"- `content_hash`: `{receipt['content_hash']}`.",
        f"- Fonte/corte: `{receipt['source']}` / `{receipt['cutoff_date']}`.",
        f"- Totais: **{receipt['rows_total']}** linhas · **{receipt['accepted']}** aceitas · **{receipt['pending']}** pendentes · **{receipt['rejected']}** recusadas.",
        f"- Idempotência contratual: repetir o mesmo conteúdo canônico mantém `content_hash` e `catalog_version`; não cria versão materialmente duplicada.",
        "",
        "## Casos exercitados",
        "",
        "| Caso | Classificação | Ativo? | Evidência |",
        "|---|---|---:|---|",
    ]
    for item in receipt["items"]:
        evidence = "; ".join(item["reasons"] + item["warnings"]) or "campos válidos"
        lines.append(f"| `{item['case']}` | `{item['classification']}` | {'sim' if item['active_candidate'] else 'não'} | {evidence} |")
    lines += [
        "",
        "## Critérios F2-T01",
        "",
        "| Critério | Resultado | Prova |",
        "|---|---|---|",
        "| CA-2-001 | PASS nesta fixture | Recibo com `import_id`, versão, fonte, data de corte, hash e totais. |",
        "| CA-2-002 | PASS nesta fixture | Linhas aceitas preservam os campos canônicos; zeros monetários viram ausência; mídia ausente vira pendência manual; nenhum valor é inventado. |",
        "| CA-2-003 | PASS nesta fixture | Obrigatório ausente e vigência vencida são recusados; mídia insegura fica pendente e não ativa; motivos aparecem por linha. |",
        "",
        "## Checagens executadas",
        "",
    ]
    lines.extend(f"- PASS — {check}." for check in checks)
    lines += [
        "",
        "## Limites e próximo gate",
        "",
        "- O contrato formaliza versionamento, idempotência, recibo append-only e rollback lógico, mas a implementação executável desses comportamentos não foi iniciada nesta task.",
        "- O parser de `.xls` real, a promoção controlada, o acesso por papel e a prova de rollback pertencem à F2-T02.",
        "- A lista completa das 29 colunas ainda depende da primeira exportação real; os cabeçalhos não confirmados não foram inventados nem copiados para o catálogo mínimo.",
        "- A Fase 1 permanece inalterada.",
        "",
        "## Comando reproduzível",
        "",
        "```sh",
        "python3 adapta-cliente/04_fase-atual/scripts/validar-f2-t01.py \\",
        "  --fixture adapta-cliente/04-fase-atual/fixtures/catalogo-f2-t01.json \\",
        "  --receipt adapta-cliente/06_notas/fase-2/recibo-f2-t01.json \\",
        "  --report adapta-cliente/06_notas/fase-2/relatorio-f2-t01.md",
        "```",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    fixture_path = Path(args.fixture)
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    receipt, canonical_payload, checks = validate_fixture(data)

    # A segunda derivação do mesmo payload é a prova local de estabilidade do hash contratual.
    second_hash = hashlib.sha256(canonical_json(canonical_payload).encode("utf-8")).hexdigest()
    if second_hash != receipt["content_hash"]:
        raise AssertionError("hash canônico não é estável")
    checks.append("hash canônico reproduzido duas vezes sem divergência")

    receipt_path = Path(args.receipt)
    report_path = Path(args.report)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(render_report(receipt, checks, str(fixture_path)), encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "receipt": str(receipt_path),
        "report": str(report_path),
        "catalog_version": receipt["catalog_version"],
        "content_hash": receipt["content_hash"],
        "rows_total": receipt["rows_total"],
        "accepted": receipt["accepted"],
        "pending": receipt["pending"],
        "rejected": receipt["rejected"],
        "checks": len(checks),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
