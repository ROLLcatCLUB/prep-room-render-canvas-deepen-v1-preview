from __future__ import annotations

import time
from typing import Any

from . import providers
from .prep_room_lesson_reasoning_contract_1013E import (
    BOUNDARY_FLAGS,
    R1_STAGE_ID,
    build_compact_lesson_reasoning_request,
    normalize_compact_lesson_reasoning_payload,
    parse_lesson_reasoning_output,
    validate_compact_lesson_reasoning_payload,
)


TRACE_STAGE_ID = "1013E_R1_PREP_ROOM_LESSON_REASONING_VISIBLE_TRACE"
FORBIDDEN_VISIBLE_TERMS = [
    "schema",
    "provider",
    "field_patch",
    "database",
    "memory",
    "formal_apply",
    "Feishu",
]


def run_prep_room_lesson_reasoning_pipeline(
    input_payload: dict[str, Any],
    *,
    source_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = input_payload if isinstance(input_payload, dict) else {}
    case = {
        "case_id": payload.get("case_id") or f"r1_{payload.get('lesson_design_mode') or 'unknown'}",
        "lesson_design_mode": payload.get("lesson_design_mode") or "standard_daily",
        "teacher_input": payload.get("teacher_input") or "",
        "expectation": payload.get("expectation") if isinstance(payload.get("expectation"), list) else [],
    }
    prompt = build_prompt(case, source_context or {})
    visible_trace = build_visible_trace(case, status="running", validation_errors=[])
    started = time.perf_counter()
    provider_result = providers.generate_json_patch(
        {"mode": R1_STAGE_ID, "case_id": case["case_id"]},
        prompt,
        {
            "provider": payload.get("provider") or "openai_compatible",
            "temperature": 0.1,
            "max_tokens": _max_tokens_for_mode(case["lesson_design_mode"]),
            "timeout_ms": int(payload.get("timeout_ms") or 100000),
            "use_response_format": True,
        },
    )
    latency_ms = round((time.perf_counter() - started) * 1000)
    raw_text = str(provider_result.get("raw_text") or "")
    provider_meta = provider_result.get("provider_meta") if isinstance(provider_result.get("provider_meta"), dict) else {}
    parsed, parser_meta = parse_lesson_reasoning_output(raw_text, provider_meta)
    validation_errors = validate_compact_lesson_reasoning_payload(parsed)
    if parser_meta.get("parse_error_code"):
        validation_errors = [parser_meta["parse_error_code"], *validation_errors]
    normalized = normalize_compact_lesson_reasoning_payload(parsed) if not validation_errors else None
    secret_hits = _secret_scan(raw_text)
    if secret_hits:
        validation_errors = [*validation_errors, "secret_scan_hit"]
    success = not validation_errors and parser_meta.get("parser_mode") == "strict_json_parser"
    safe_success = not validation_errors and bool(parsed)
    final_status = "done" if safe_success else "blocked"
    visible_trace = build_visible_trace(case, status=final_status, validation_errors=validation_errors)

    return {
        "stage_id": R1_STAGE_ID,
        "case_id": case["case_id"],
        "lesson_design_mode": case["lesson_design_mode"],
        "teacher_input": case["teacher_input"],
        "provider_called": True,
        "model_called": True,
        "strict_json_success": bool(success),
        "safe_success": bool(safe_success),
        "parser_mode": parser_meta.get("parser_mode") or "unknown",
        "extraction_required": bool(parser_meta.get("extraction_required")),
        "parser_meta": _public_parser_meta(parser_meta),
        "validation_errors": validation_errors,
        "secret_scan_hits": secret_hits,
        "latency_ms": provider_meta.get("latency_ms") or latency_ms,
        "provider_meta": _public_provider_meta(provider_meta),
        "readonly_result": {
            "readonly": True,
            "candidate_only": True,
            "formal_apply_performed": False,
            "parsed_compact": parsed,
            "normalized_legacy_shape": normalized,
            "boundary_flags": dict(BOUNDARY_FLAGS),
        },
        "visible_trace": visible_trace,
        "prompt": prompt,
        "raw_text": raw_text,
    }


def build_prompt(case: dict[str, Any], source_context: dict[str, Any]) -> dict[str, str]:
    request_payload = build_compact_lesson_reasoning_request(case, source_context)
    mode = str(case.get("lesson_design_mode") or "standard_daily")
    mode_instruction = _mode_instruction(mode)
    system_prompt = (
        "你是师维备课室的小备，负责小学美术课时设计协作。"
        "你只做教学判断和只读候选，不写整篇教案。"
        "你必须输出严格 JSON 对象。"
    )
    request_payload["mode_instruction"] = mode_instruction
    request_payload["output_limits"] = {
        "lesson_design_brief_compact_max_items": 4,
        "step_reasoning_updates_max_items": 2 if mode in {"quick_daily", "standard_daily"} else 3,
        "field_patch_candidates_max_items": 2,
        "impact_scope_max_items": 4,
        "teacher_questions_max_items": 1 if mode == "quick_daily" else 3,
        "text_style": "短句，教师能直接看懂，不要长篇论述。",
    }
    request_payload["minimum_required_counts"] = {
        "target_resolution": 1,
        "step_reasoning_updates": 1,
        "field_patch_candidates": 1,
        "impact_scope": 1,
    }
    request_payload["json_safety"] = [
        "字符串内部不要写英文双引号，例如不要写 \"好看\"，改写为 好看 或 中文引号“好看”。",
        "不要输出尾随逗号。",
        "不要输出空数组来代替必填候选。",
    ]
    return {
        "system_prompt": system_prompt,
        "user_prompt": _json_dumps(request_payload),
    }


def build_visible_trace(case: dict[str, Any], *, status: str, validation_errors: list[str]) -> dict[str, Any]:
    mode_label = _mode_label(str(case.get("lesson_design_mode") or "standard_daily"))
    blocked = bool(validation_errors)
    steps = [
        ("mode", "判断这节课准备到什么程度", f"按{mode_label}来处理，先控制生成深度。"),
        ("student_blocker", "查看学生可能卡在哪里", "重点看学生能否把颜色、感受和理由连起来。"),
        ("target", "定位要修改的段落或环节", _target_text(str(case.get("teacher_input") or ""))),
        ("impact", "检查会影响大屏、学习单和评价证据", "同步检查材料呈现、学习记录和课堂观察证据。"),
        ("candidate", "整理成候选，等待老师确认", "整理为可并入的候选，不直接变成正式结果。"),
    ]
    trace_steps = []
    for index, (step_id, label, text) in enumerate(steps):
        if status == "running":
            step_status = "running" if index == 0 else "pending"
        elif blocked:
            step_status = "blocked" if index >= 3 else "done"
        else:
            step_status = "done"
        trace_steps.append(
            {
                "id": step_id,
                "label": _safe_visible(label),
                "status": step_status,
                "teacher_visible_text": _safe_visible(text),
            }
        )
    return {
        "stage_id": TRACE_STAGE_ID,
        "teacher_visible": True,
        "raw_model_reasoning_visible": False,
        "status": "blocked" if blocked else status,
        "headline": "小备正在整理这次修改" if status == "running" else _headline(blocked),
        "steps": trace_steps,
        "teacher_note": "所有内容都先作为候选，等待老师确认。",
    }


def _mode_instruction(mode: str) -> str:
    instructions = {
        "quick_daily": "快速日常课：够上课，少追问，候选短，不展开公开课式设计。",
        "standard_daily": "标准日常课：目标、流程、学生任务、评价证据要完整，重点修探究环节和直观材料。",
        "open_class": "公开课：强化问题串、学生表达、展示节奏和评价证据，但仍标记待确认问题。",
        "research_lesson": "研究课：明确学习问题、教学假设、证据计划和学生状态变化，不写论文。",
    }
    return instructions.get(mode, instructions["standard_daily"])


def _max_tokens_for_mode(mode: str) -> int:
    if mode == "quick_daily":
        return 1800
    if mode == "standard_daily":
        return 2200
    return 2600


def _mode_label(mode: str) -> str:
    labels = {
        "quick_daily": "快速日常课",
        "standard_daily": "标准日常课",
        "open_class": "公开课",
        "research_lesson": "研究课",
    }
    return labels.get(mode, "标准日常课")


def _target_text(teacher_input: str) -> str:
    text = teacher_input or ""
    if "冷暖色" in text or "直观" in text:
        return "优先定位到学情分析和教学过程的探究环节。"
    if "展示" in text or "问题串" in text:
        return "优先定位到问题串、学生表达和交流展示环节。"
    if "研究" in text or "过渡" in text:
        return "优先定位到学习问题、学生状态变化和证据设计。"
    return "先定位到本课设计简报和教学过程关键环节。"


def _headline(blocked: bool) -> str:
    return "这次输出还需要修正" if blocked else "已整理为只读候选，等待老师确认"


def _safe_visible(text: str) -> str:
    value = str(text or "")
    for term in FORBIDDEN_VISIBLE_TERMS:
        value = value.replace(term, "内部词")
    return value


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


def _secret_scan(text: str) -> list[str]:
    value = str(text or "")
    hits = []
    for marker in ["Bearer ", "sk-", "ghp_", "gho_", "tenant_access_token"]:
        if marker in value:
            hits.append(marker.strip())
    return hits


def _json_dumps(payload: Any) -> str:
    import json

    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
