from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.xiaobei_ai import providers  # noqa: E402
from backend.xiaobei_ai.prep_room_lesson_reasoning_contract_1013E import (  # noqa: E402
    BOUNDARY_FLAGS,
    parse_lesson_reasoning_output,
    validate_compact_lesson_reasoning_payload,
)


STAGE_ID = "1013E_R2_STANDARD_DAILY_PROMPT_REPAIR_AND_UI_BINDING_READY_CHECK"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "live_poc_1013E_R2"

CASE = {
    "case_id": "test_standard_daily_repair",
    "lesson_design_mode": "standard_daily",
    "teacher_input": "学生对冷暖色不太理解，要设计得更直观一点。",
}

SECRET_PATTERNS = [
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]{12,}", re.I),
    re.compile(r"sk-[A-Za-z0-9_\-]{12,}", re.I),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{12,}", re.I),
    re.compile(r"(?i)(api[_-]?key|authorization|secret|tenant_access_token)\s*[:=]\s*['\"][^'\"]{8,}"),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(name: str, payload: Any) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_text(name: str, text: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    path.write_text(text, encoding="utf-8")
    return path


def provider_public_status() -> dict[str, Any]:
    status = providers.provider_status()
    generation = status.get("generation") or {}
    return {
        "provider_name": status.get("provider_name"),
        "credential_available": bool(generation.get("credential_available")),
        "credential_source": generation.get("credential_source"),
        "model": generation.get("model"),
        "base_url": generation.get("base_url"),
    }


def build_prompt() -> dict[str, str]:
    request = {
        "stage_id": STAGE_ID,
        "lesson": "三年级美术 色彩单元 1-2《色彩的感觉》 40分钟",
        "teacher_input": CASE["teacher_input"],
        "output_keys": [
            "lesson_design_mode",
            "intent_summary",
            "lesson_design_brief_compact",
            "target_resolution",
            "step_reasoning_updates",
            "field_patch_candidates",
            "impact_scope",
            "quality_gate_update",
            "teacher_questions",
            "ui_binding_hint",
            "boundary_flags",
        ],
        "field_types": {
            "lesson_design_brief_compact": "object，必须含 core_learning_problem student_baseline target_shift teaching_route evidence_plan risk_points basis_summary",
            "target_resolution": "array，至少 analysis 和 teaching_process/explore 两项",
            "step_reasoning_updates": "array，只写一个 object，step_id 必须是 explore",
            "field_patch_candidates": "array，恰好两个 object",
            "impact_scope": "array，恰好 big_screen handout evidence_note 三个 object",
            "quality_gate_update": "object，level 用 ready_to_teach",
            "teacher_questions": "array，可空",
            "ui_binding_hint": "object",
            "boundary_flags": "object",
        },
        "must_cover": {
            "step_reasoning_updates": "只写 explore 探究环节，含 teacher_action student_action big_screen_state learning_sheet_state assessment_evidence。",
            "field_patch_candidates": "两条：analysis/student_baseline 与 teaching_process/explore/student_activity。",
            "impact_scope": ["big_screen", "handout", "evidence_note"],
            "quality_gate_level": "ready_to_teach",
            "flags": BOUNDARY_FLAGS,
        },
        "content_hint": "学生能说颜色和喜好，但冷暖色理解停在表层。用大屏冷暖生活图、色卡分组、学习单感受记录格，评价学生能否说出分类理由。",
        "json_rules": [
            "只输出 JSON 对象，不要 markdown，不要代码块，不要解释。",
            "不要写填空句，不要写下划线空格。",
            "字符串里不要写英文双引号。",
            "不要写 teacher_input content_hint field_path current_value patch_value 这些词。",
        ],
    }
    return {
        "system_prompt": (
            "你是师维备课室的小备，只输出一个 JSON 对象。"
            "不要 markdown，不要代码块，不要解释文字。"
            "只输出只读候选，不正式应用。"
        ),
        "user_prompt": json.dumps(request, ensure_ascii=False, separators=(",", ":")),
    }


def call_provider(prompt: dict[str, str]) -> dict[str, Any]:
    started = time.perf_counter()
    provider_result = providers.generate_json_patch(
        {"mode": STAGE_ID, "case_id": CASE["case_id"]},
        prompt,
        {
            "provider": "openai_compatible",
            "model": "MiniMax-M2.7-highspeed",
            "temperature": 0.1,
            "max_tokens": 2400,
            "timeout_ms": 100000,
            "use_response_format": True,
            "use_reasoning_split": False,
        },
    )
    latency_ms = round((time.perf_counter() - started) * 1000)
    raw_text = str(provider_result.get("raw_text") or "")
    provider_meta = provider_result.get("provider_meta") if isinstance(provider_result.get("provider_meta"), dict) else {}
    parsed, parser_meta = parse_lesson_reasoning_output(raw_text, provider_meta)
    validation_errors = validate_compact_lesson_reasoning_payload(parsed)
    validation_errors.extend(_standard_daily_coverage_errors(parsed))
    if parser_meta.get("parse_error_code"):
        validation_errors = [parser_meta["parse_error_code"], *validation_errors]
    secret_hits = secret_scan_text(raw_text)
    if secret_hits:
        validation_errors.append("secret_scan_hit")
    strict_success = not validation_errors and parser_meta.get("parser_mode") == "strict_json_parser"
    return {
        "stage_id": STAGE_ID,
        "case_id": CASE["case_id"],
        "lesson_design_mode": CASE["lesson_design_mode"],
        "teacher_input": CASE["teacher_input"],
        "strict_json_success": bool(strict_success),
        "success": bool(strict_success),
        "parser_mode": parser_meta.get("parser_mode") or "unknown",
        "parser_meta": _public_parser_meta(parser_meta),
        "validation_errors": validation_errors,
        "secret_scan_hits": secret_hits,
        "provider_called": True,
        "model_called": True,
        "latency_ms": provider_meta.get("latency_ms") or latency_ms,
        "provider_meta": _public_provider_meta(provider_meta),
        "parsed_json": parsed,
        "raw_response_redacted": redact_text(raw_text),
        "redacted_request": redact_text(json.dumps(prompt, ensure_ascii=False)),
        "boundary_flags": dict(BOUNDARY_FLAGS),
    }


def _standard_daily_coverage_errors(parsed: dict[str, Any] | None) -> list[str]:
    if not isinstance(parsed, dict):
        return []
    errors: list[str] = []
    steps = parsed.get("step_reasoning_updates") if isinstance(parsed.get("step_reasoning_updates"), list) else []
    if not any(isinstance(item, dict) and item.get("step_id") == "explore" for item in steps):
        errors.append("missing_explore_step_update")
    impacts = parsed.get("impact_scope") if isinstance(parsed.get("impact_scope"), list) else []
    impact_ids = {item.get("affected_object") for item in impacts if isinstance(item, dict)}
    for required in ["big_screen", "handout", "evidence_note"]:
        if required not in impact_ids:
            errors.append(f"missing_impact_{required}")
    patches = parsed.get("field_patch_candidates") if isinstance(parsed.get("field_patch_candidates"), list) else []
    if not any(isinstance(item, dict) and item.get("target_section") == "analysis" for item in patches):
        errors.append("missing_analysis_patch")
    if not any(
        isinstance(item, dict)
        and item.get("target_section") == "teaching_process"
        and item.get("target_step_id") == "explore"
        for item in patches
    ):
        errors.append("missing_explore_patch")
    return errors


def final_payload(case_result: dict[str, Any], provider_status: dict[str, Any]) -> dict[str, Any]:
    passed = bool(case_result.get("strict_json_success"))
    return {
        "stage_id": STAGE_ID,
        "created_at": now(),
        "final_status": "STANDARD_DAILY_REPAIR_STRICT_JSON_PASS" if passed else "STANDARD_DAILY_REPAIR_FAILED",
        "next_stage": "1013F_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING"
        if passed
        else "1013E_R3_PROMPT_REPAIR_OR_MODEL_STRATEGY_ADJUSTMENT",
        "provider_called": bool(case_result.get("provider_called")),
        "model_called": bool(case_result.get("model_called")),
        "provider_status": provider_status,
        "strict_json_success": passed,
        "validation_errors": case_result.get("validation_errors") or [],
        "boundary_flags": dict(BOUNDARY_FLAGS),
        "case_file": "test_standard_daily_repair_result.json",
    }


def write_report(result: dict[str, Any], case_result: dict[str, Any]) -> None:
    lines = [
        "# 1013E_R2 Standard Daily Prompt Repair",
        "",
        "```text",
        f"final_status={result.get('final_status')}",
        f"next_stage={result.get('next_stage')}",
        f"strict_json_success={str(result.get('strict_json_success')).lower()}",
        f"validation_error_count={len(case_result.get('validation_errors') or [])}",
        "secret_scan_ok=true" if not case_result.get("secret_scan_hits") else "secret_scan_ok=false",
        "```",
        "",
        "## Case",
        "",
        "- mode: `standard_daily`",
        "- input: 学生对冷暖色不太理解，要设计得更直观一点。",
        "",
        "## Boundary",
        "",
        "- Provider called once for this repair run.",
        "- No database write.",
        "- No memory write.",
        "- No Feishu write.",
        "- No formal apply.",
        "- No formal export or archive.",
        "- Request and response are redacted.",
    ]
    if case_result.get("validation_errors"):
        lines.extend(["", "## Validation Errors", ""])
        lines.extend(f"- `{item}`" for item in case_result.get("validation_errors") or [])
    write_text("1013E_R2_report.md", "\n".join(lines) + "\n")


def blocked_outputs(provider_status: dict[str, Any]) -> int:
    case_result = {
        "stage_id": STAGE_ID,
        "case_id": CASE["case_id"],
        "lesson_design_mode": CASE["lesson_design_mode"],
        "teacher_input": CASE["teacher_input"],
        "strict_json_success": False,
        "success": False,
        "provider_called": False,
        "model_called": False,
        "validation_errors": ["missing_provider_env"],
        "parsed_json": None,
        "boundary_flags": dict(BOUNDARY_FLAGS),
    }
    result = final_payload(case_result, provider_status)
    result["final_status"] = "BLOCKED_MISSING_PROVIDER_ENV"
    result["next_stage"] = "1013E_R2_PROVIDER_ENV_RECHECK"
    write_json("test_standard_daily_repair_result.json", case_result)
    write_json("1013E_R2_result.json", result)
    write_json("provider_metrics_1013E_R2.json", {"provider_called": False, "model_called": False, "provider_status": provider_status})
    write_json("redacted_provider_trace_1013E_R2.json", [])
    write_text("prompt_repair_standard_daily_1013E_R2.md", _prompt_markdown(build_prompt()))
    write_report(result, case_result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt()
    write_text("prompt_repair_standard_daily_1013E_R2.md", _prompt_markdown(prompt))
    provider_status = provider_public_status()
    if not provider_status.get("credential_available"):
        return blocked_outputs(provider_status)
    try:
        case_result = call_provider(prompt)
    except providers.ProviderError as exc:
        case_result = {
            "stage_id": STAGE_ID,
            "case_id": CASE["case_id"],
            "lesson_design_mode": CASE["lesson_design_mode"],
            "teacher_input": CASE["teacher_input"],
            "strict_json_success": False,
            "success": False,
            "provider_called": True,
            "model_called": True,
            "parser_mode": "provider_error",
            "validation_errors": [exc.code],
            "error_message_redacted": redact_text(exc.message)[:500],
            "secret_scan_hits": [],
            "parsed_json": None,
            "boundary_flags": dict(BOUNDARY_FLAGS),
        }
    result = final_payload(case_result, provider_status)
    write_json("test_standard_daily_repair_result.json", _public_case_result(case_result))
    write_json("1013E_R2_result.json", result)
    write_json(
        "provider_metrics_1013E_R2.json",
        {
            "provider_called": result["provider_called"],
            "model_called": result["model_called"],
            "strict_json_success": result["strict_json_success"],
            "latency_ms": case_result.get("latency_ms"),
            "provider_status": provider_status,
        },
    )
    write_json(
        "redacted_provider_trace_1013E_R2.json",
        [
            {
                "case_id": CASE["case_id"],
                "lesson_design_mode": CASE["lesson_design_mode"],
                "strict_json_success": case_result.get("strict_json_success"),
                "parser_mode": case_result.get("parser_mode"),
                "validation_errors": case_result.get("validation_errors") or [],
                "secret_scan_hits": case_result.get("secret_scan_hits") or [],
                "latency_ms": case_result.get("latency_ms"),
                "provider_meta": case_result.get("provider_meta") or {},
                "redacted_request": case_result.get("redacted_request") or "",
                "raw_response_redacted": case_result.get("raw_response_redacted") or "",
            }
        ],
    )
    write_report(result, case_result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"] == "STANDARD_DAILY_REPAIR_STRICT_JSON_PASS" else 1


def _public_case_result(case_result: dict[str, Any]) -> dict[str, Any]:
    payload = dict(case_result)
    payload.pop("raw_response_redacted", None)
    payload.pop("redacted_request", None)
    return payload


def _prompt_markdown(prompt: dict[str, str]) -> str:
    return (
        "# 1013E_R2 Standard Daily Prompt Repair\n\n"
        "## System Prompt\n\n"
        f"{prompt['system_prompt']}\n\n"
        "## User Prompt\n\n"
        f"{prompt['user_prompt']}\n"
    )


def redact_text(text: str) -> str:
    value = str(text or "")
    replacements = [
        (r"Bearer\s+[A-Za-z0-9._\-]+", "Bearer <REDACTED>"),
        (r"sk-[A-Za-z0-9._\-]{8,}", "sk-<REDACTED>"),
        (r"gh[pousr]_[A-Za-z0-9_]+", "gh-<REDACTED>"),
        (r"(api[_-]?key[\"'\s:=]+)[A-Za-z0-9._\-]+", r"\1<REDACTED>"),
        (r"(secret[\"'\s:=]+)[A-Za-z0-9._\-]+", r"\1<REDACTED>"),
        (r"C:\\Users\\Administrator", r"<USER_HOME_REDACTED>"),
    ]
    for pattern, replacement in replacements:
        value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)
    return value


def secret_scan_text(text: str) -> list[str]:
    return [pattern.pattern for pattern in SECRET_PATTERNS if pattern.search(text or "")]


def _public_provider_meta(meta: dict[str, Any]) -> dict[str, Any]:
    base_url = str(meta.get("base_url") or "")
    host = base_url.split("/")[2] if "://" in base_url else ""
    return {
        "provider": meta.get("provider"),
        "model": meta.get("model"),
        "base_url_host": host,
        "credential_source": meta.get("credential_source"),
        "reasoning_split": bool(meta.get("reasoning_split")),
        "latency_ms": meta.get("latency_ms"),
    }


def _public_parser_meta(meta: dict[str, Any]) -> dict[str, Any]:
    return {
        "parser_mode": meta.get("parser_mode"),
        "parse_subcode": meta.get("parse_subcode"),
        "parse_error_code": meta.get("parse_error_code"),
        "raw_prefix_type": meta.get("raw_prefix_type") or meta.get("raw_response_prefix_type"),
        "provider_output_sanitized": bool(meta.get("provider_output_sanitized")),
        "extraction_required": bool(meta.get("extraction_required")),
    }


if __name__ == "__main__":
    raise SystemExit(main())
