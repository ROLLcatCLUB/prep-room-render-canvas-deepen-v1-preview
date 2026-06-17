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
    build_lesson_reasoning_request,
    parse_lesson_reasoning_output,
    validate_lesson_reasoning_payload,
)


STAGE_ID = "1013E_MODEL_PROMPT_TO_REASONING_FIELD_PATCH_POC"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "live_poc_1013E"
SOURCE_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"

TEST_CASES = [
    {
        "case_id": "test_1_quick_daily",
        "filename": "test_1_quick_daily_result.json",
        "lesson_design_mode": "quick_daily",
        "teacher_input": "今天时间不多，先帮我快速整理一版能上课的基本设计。",
        "expectation": [
            "不过度追问",
            "基础 lesson_design_brief",
            "简洁教学流程",
            "基础评价证据",
            "quality_gate 至少 basic_usable",
            "不生成公开课式长设计",
        ],
    },
    {
        "case_id": "test_2_standard_daily",
        "filename": "test_2_standard_daily_result.json",
        "lesson_design_mode": "standard_daily",
        "teacher_input": "学生对冷暖色不太理解，要设计得更直观一点。",
        "expectation": [
            "判断为补学情 / 改探究环节 / 强化直观体验",
            "定位到学情分析、探究环节、大屏、学习单、评价证据",
            "输出 1-2 个 field_patch_candidate",
            "不重写整篇教案",
        ],
    },
    {
        "case_id": "test_3_open_class",
        "filename": "test_3_open_class_result.json",
        "lesson_design_mode": "open_class",
        "teacher_input": "这节课我要拿来展示，问题串、学生表达和评价证据要更清楚。",
        "expectation": [
            "强化问题串",
            "强化学生表达",
            "强化课堂展示",
            "强化评价证据",
            "quality_gate 接近 open_class_ready 但可标缺口",
        ],
    },
    {
        "case_id": "test_4_research_lesson",
        "filename": "test_4_research_lesson_result.json",
        "lesson_design_mode": "research_lesson",
        "teacher_input": "我想研究学生怎么从说颜色好看，过渡到能说明颜色带来的感受。",
        "expectation": [
            "明确 core_learning_problem",
            "明确教学假设",
            "明确 evidence_plan",
            "说明从感知到表达的学习路径",
            "不变成论文",
        ],
    },
]

LESSON_CONTEXT = {
    "semester": "2026春学期",
    "subject": "美术",
    "grade": "三年级",
    "unit": "色彩单元",
    "lesson_code": "1-2",
    "lesson_title": "色彩的感觉",
    "duration_minutes": 40,
    "initial_teaching_judgment": [
        "学生知道很多颜色，也会说喜欢或不喜欢。",
        "但他们未必能把颜色、情绪、生活场景和作品表达联系起来。",
        "本课目标不是只认识冷暖色，而是让学生能说出颜色带来的感受，并尝试用色彩表达心情或场景。",
    ],
    "available_resource_candidates": [
        "色彩单元课标摘要",
        "教材图例",
        "冷暖色图片素材",
        "优秀课例《色彩的感觉》",
        "美术评价量规维度：色彩、创意、过程性评价",
    ],
}

REQUIRED_OUTPUT_SHAPE = {
    "lesson_design_mode": "",
    "intent_summary": "",
    "intent_classification": {
        "intent_type": "",
        "confidence": "high | medium | low",
        "reason": "",
    },
    "lesson_design_brief": {
        "core_learning_problem": "",
        "student_baseline": "",
        "target_shift": "",
        "unit_position": "",
        "curriculum_basis": [],
        "textbook_basis": [],
        "prior_learning_basis": [],
        "teacher_intent": "",
        "classroom_constraints": [],
        "resource_budget": "low | medium | high",
        "teaching_route": [],
        "evidence_plan": [],
        "risk_points": [],
        "next_best_questions": [],
    },
    "patch_target_resolution": [
        {
            "section_id": "",
            "step_id": "",
            "target_field": "",
            "reason": "",
        }
    ],
    "teaching_step_reasoning_updates": [
        {
            "step_id": "",
            "step_name": "",
            "duration": "",
            "step_role": "",
            "design_intent": "",
            "student_state_before": "",
            "student_state_after": "",
            "teacher_action": "",
            "student_action": "",
            "big_screen_state": "",
            "textbook_or_material_state": "",
            "learning_sheet_state": "",
            "assessment_evidence": "",
            "transition_from_previous": "",
            "transition_to_next": "",
            "risk_and_adjustment": "",
        }
    ],
    "field_patch_candidates": [
        {
            "field_patch_id": "",
            "target_section": "",
            "target_step_id": "",
            "target_field": "",
            "patch_type": "fill_missing | revise | restructure | add_example | simplify | enrich",
            "before_summary": "",
            "after_candidate": "",
            "reasoning_basis": [],
            "impact_scope": [],
            "teacher_review_required": True,
            "formal_apply_performed": False,
        }
    ],
    "impact_scope": [
        {
            "affected_object": "big_screen | handout | rubric | resource_reference | evidence_note | teacher_action | student_activity",
            "impact_summary": "",
            "requires_teacher_confirmation": True,
        }
    ],
    "quality_gate_update": {
        "level": "basic_usable | ready_to_teach | refined | open_class_ready",
        "passed_items": [],
        "missing_items": [],
        "risk_items": [],
        "next_best_action": "",
    },
    "teacher_questions": [
        {
            "question": "",
            "why_needed": "",
            "options": [],
        }
    ],
    "ui_binding_hint": {
        "should_enter_edit_mode": True,
        "edit_target": "",
        "candidate_display_position": "",
        "right_tray_updates": [],
        "view_mode_summary": "",
    },
    "boundary_flags": {
        "teacher_review_required": True,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_export_created": False,
        "official_archive_created": False,
    },
}

SECRET_PATTERNS = [
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]{12,}", re.I),
    re.compile(r"sk-[A-Za-z0-9_\-]{12,}", re.I),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{12,}", re.I),
    re.compile(r"(?i)(api[_-]?key|authorization|secret|tenant_access_token)\s*[:=]\s*['\"][^'\"]{8,}"),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(name: str) -> str:
    return (SOURCE_DIR / name).read_text(encoding="utf-8")


def read_json(name: str) -> Any:
    return json.loads(read_text(name))


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


def is_non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


def compact_source_context() -> dict[str, Any]:
    return {
        "lesson_design_model": read_json("lesson_design_reasoning_model_1013D.json"),
        "brief_sample": read_json("lesson_design_brief_sample_1013D.json"),
        "step_reasoning_sample": read_json("teaching_step_reasoning_sample_1013D.json"),
        "quality_gate_sample": read_json("lesson_design_quality_gate_1013D.json"),
        "question_strategy": read_json("xiaobei_question_strategy_1013D.json"),
        "trace_module": read_json("lesson_reasoning_trace_module_1013E.json"),
        "view_edit_plan_excerpt": read_text("prep_notebook_1013C_view_edit_teaching_process_design_plan.md")[:6000],
    }


def build_prompt(case: dict[str, Any], source_context: dict[str, Any]) -> dict[str, str]:
    request_payload = build_lesson_reasoning_request(case, source_context)
    system_prompt = (
        "你是师维备课室的小备，负责小学美术备课协作。"
        "你不是直接写完整教案，而是先做教学判断，再输出可由教师确认的字段补丁。"
        "你必须严格输出一个 JSON 对象。"
    )
    user_prompt = json.dumps(request_payload, ensure_ascii=False)
    return {"system_prompt": system_prompt, "user_prompt": user_prompt}


def call_provider(case: dict[str, Any], source_context: dict[str, Any]) -> dict[str, Any]:
    prompt = build_prompt(case, source_context)
    started = time.perf_counter()
    provider_result = providers.generate_json_patch(
        {"mode": STAGE_ID, "case_id": case["case_id"]},
        prompt,
        {
            "provider": "openai_compatible",
            "temperature": 0.1,
            "max_tokens": 5200,
            "timeout_ms": 90000,
            "use_response_format": True,
        },
    )
    latency_ms = round((time.perf_counter() - started) * 1000)
    raw_text = provider_result.get("raw_text") or ""
    meta = provider_result.get("provider_meta") or {}
    parsed, parser_meta = parse_lesson_reasoning_output(raw_text, meta)
    parser_mode = parser_meta.get("parser_mode") or "unknown"
    extraction_required = bool(parser_meta.get("extraction_required"))
    validation_errors = validate_lesson_reasoning_payload(parsed)
    if parser_meta.get("parse_error_code"):
        validation_errors = [parser_meta["parse_error_code"], *validation_errors]
    secret_hits = secret_scan_text(raw_text)
    success = not validation_errors and not secret_hits and parser_mode == "strict_json"
    return {
        "case_id": case["case_id"],
        "lesson_design_mode": case["lesson_design_mode"],
        "teacher_input": case["teacher_input"],
        "strict_json_success": bool(success),
        "success": bool(success),
        "parser_mode": parser_mode,
        "extraction_required": bool(extraction_required),
        "parser_meta": parser_meta,
        "validation_errors": validation_errors,
        "secret_scan_hits": secret_hits,
        "provider_called": True,
        "model_called": True,
        "latency_ms": meta.get("latency_ms") or latency_ms,
        "provider_meta": {
            "provider": meta.get("provider"),
            "model": meta.get("model"),
            "base_url_host": str(meta.get("base_url") or "").split("/")[2] if "://" in str(meta.get("base_url") or "") else "",
            "credential_source": meta.get("credential_source"),
            "reasoning_split": bool(meta.get("reasoning_split")),
        },
        "parsed_json": parsed,
        "raw_response_redacted": redact_text(raw_text),
        "redacted_request": redact_text(json.dumps(prompt, ensure_ascii=False)),
    }


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


def blocked_outputs(provider_status: dict[str, Any]) -> int:
    empty_results = []
    for case in TEST_CASES:
        payload = {
            "case_id": case["case_id"],
            "lesson_design_mode": case["lesson_design_mode"],
            "teacher_input": case["teacher_input"],
            "strict_json_success": False,
            "success": False,
            "provider_called": False,
            "model_called": False,
            "final_status": "BLOCKED_MISSING_PROVIDER_ENV",
            "validation_errors": ["missing_provider_env"],
            "parsed_json": None,
        }
        write_json(case["filename"], payload)
        empty_results.append(payload)
    result = {
        "stage_id": STAGE_ID,
        "created_at": now(),
        "final_status": "BLOCKED_MISSING_PROVIDER_ENV",
        "provider_called": False,
        "model_called": False,
        "strict_json_success_count": 0,
        "successful_case_count": 0,
        "provider_status": provider_status,
        "boundary_flags": {
            "teacher_review_required": True,
            "formal_apply_performed": False,
            "database_written": False,
            "memory_written": False,
            "feishu_written": False,
            "formal_export_created": False,
            "official_archive_created": False,
        },
        "next_stage": "1013E_R1_PROVIDER_ENV_RECHECK",
    }
    write_json("1013E_result.json", result)
    write_json("provider_metrics_1013E.json", {"provider_called": False, "model_called": False, "provider_status": provider_status})
    write_json("redacted_provider_trace_1013E.json", [])
    write_text("prompt_used_1013E.md", build_prompt(TEST_CASES[0], compact_source_context())["system_prompt"] + "\n\n" + build_prompt(TEST_CASES[0], compact_source_context())["user_prompt"])
    write_text(
        "1013E_report.md",
        "# 1013E Model Prompt To Reasoning Field Patch POC\n\n"
        "```text\n"
        "final_status=BLOCKED_MISSING_PROVIDER_ENV\n"
        "provider_called=false\n"
        "model_called=false\n"
        "next_stage=1013E_R1_PROVIDER_ENV_RECHECK\n"
        "```\n",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2


def final_status_for(results: list[dict[str, Any]]) -> tuple[str, str]:
    strict_count = sum(1 for item in results if item.get("strict_json_success"))
    safe_extracted_count = sum(
        1
        for item in results
        if item.get("parser_mode") == "extracted_json" and not item.get("validation_errors") and not item.get("secret_scan_hits")
    )
    success_count = strict_count + safe_extracted_count
    if strict_count == 4:
        return "PASS_STRICT_JSON_ALL", "1013F_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING"
    if strict_count == 3 and success_count >= 3:
        return "PASS_STRICT_JSON_WITH_ONE_FAILURE", "1013F_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING"
    if success_count >= 3:
        return "PASS_WITH_EXTRACTION_CAVEAT", "1013F_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING"
    return "FAIL_MODEL_OUTPUT_NOT_STABLE", "1013E_R1_PROMPT_REPAIR"


def aggregate_pass_criteria(results: list[dict[str, Any]]) -> dict[str, Any]:
    parsed_success = [item.get("parsed_json") for item in results if item.get("parsed_json") and not item.get("validation_errors")]
    strict_success_count = sum(1 for item in results if item.get("strict_json_success"))
    cases_with_brief = sum(1 for parsed in parsed_success if isinstance(parsed.get("lesson_design_brief"), dict))
    cases_with_patch = sum(1 for parsed in parsed_success if is_non_empty_list(parsed.get("field_patch_candidates")))
    cases_with_step_updates = sum(1 for parsed in parsed_success if is_non_empty_list(parsed.get("teaching_step_reasoning_updates")))
    targetable_patches = sum(
        1
        for parsed in parsed_success
        for patch in parsed.get("field_patch_candidates", [])
        if isinstance(patch, dict) and (patch.get("target_section") or patch.get("target_step_id"))
    )
    impact_objects = sorted(
        {
            impact.get("affected_object")
            for parsed in parsed_success
            for impact in parsed.get("impact_scope", [])
            if isinstance(impact, dict) and impact.get("affected_object")
        }
    )
    gate_levels = sorted(
        {
            parsed.get("quality_gate_update", {}).get("level")
            for parsed in parsed_success
            if isinstance(parsed.get("quality_gate_update"), dict)
        }
    )
    boundary_ok = all(
        (parsed.get("boundary_flags") or {}).get("teacher_review_required") is True
        and (parsed.get("boundary_flags") or {}).get("formal_apply_performed") is False
        and (parsed.get("boundary_flags") or {}).get("database_written") is False
        and (parsed.get("boundary_flags") or {}).get("memory_written") is False
        and (parsed.get("boundary_flags") or {}).get("feishu_written") is False
        for parsed in parsed_success
    )
    return {
        "strict_json_success_count": strict_success_count,
        "safe_success_count": len(parsed_success),
        "cases_with_lesson_design_brief": cases_with_brief,
        "cases_with_field_patch_candidates": cases_with_patch,
        "cases_with_teaching_step_reasoning_updates": cases_with_step_updates,
        "targetable_patch_count": targetable_patches,
        "impact_objects": impact_objects,
        "quality_gate_levels": gate_levels,
        "boundary_ok": boundary_ok,
        "secret_scan_ok": not any(item.get("secret_scan_hits") for item in results),
    }


def write_report(final_status: str, next_stage: str, results: list[dict[str, Any]], criteria: dict[str, Any]) -> None:
    lines = [
        "# 1013E Model Prompt To Reasoning Field Patch POC",
        "",
        "```text",
        f"final_status={final_status}",
        f"next_stage={next_stage}",
        f"strict_json_success_count={criteria['strict_json_success_count']}",
        f"safe_success_count={criteria['safe_success_count']}",
        f"cases_with_lesson_design_brief={criteria['cases_with_lesson_design_brief']}",
        f"cases_with_field_patch_candidates={criteria['cases_with_field_patch_candidates']}",
        f"cases_with_teaching_step_reasoning_updates={criteria['cases_with_teaching_step_reasoning_updates']}",
        f"targetable_patch_count={criteria['targetable_patch_count']}",
        f"boundary_ok={str(criteria['boundary_ok']).lower()}",
        f"secret_scan_ok={str(criteria['secret_scan_ok']).lower()}",
        "```",
        "",
        "## Boundary",
        "",
        "- No database write.",
        "- No memory write.",
        "- No Feishu write.",
        "- No formal apply.",
        "- No official export.",
        "- No official archive.",
        "- Provider requests and responses are redacted.",
        "",
        "## Test Cases",
        "",
    ]
    for item in results:
        lines.append(
            f"- `{item['case_id']}` `{item['lesson_design_mode']}`: "
            f"{'PASS' if item.get('strict_json_success') else 'FAIL'}; "
            f"parser={item.get('parser_mode')}; errors={len(item.get('validation_errors') or [])}"
        )
    lines.extend(
        [
            "",
            "## Impact Objects",
            "",
            ", ".join(criteria.get("impact_objects") or []) or "none",
            "",
            "## Quality Gate Levels",
            "",
            ", ".join(criteria.get("quality_gate_levels") or []) or "none",
        ]
    )
    write_text("1013E_report.md", "\n".join(lines) + "\n")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    source_context = compact_source_context()
    provider_status = provider_public_status()
    if not provider_status.get("credential_available"):
        return blocked_outputs(provider_status)

    write_text(
        "prompt_used_1013E.md",
        "# 1013E Prompt Template\n\n"
        "## System Prompt\n\n"
        + build_prompt(TEST_CASES[0], source_context)["system_prompt"]
        + "\n\n## Sample User Prompt\n\n"
        + build_prompt(TEST_CASES[0], source_context)["user_prompt"]
        + "\n",
    )

    results: list[dict[str, Any]] = []
    traces: list[dict[str, Any]] = []
    for case in TEST_CASES:
        try:
            result = call_provider(case, source_context)
        except providers.ProviderError as exc:
            result = {
                "case_id": case["case_id"],
                "lesson_design_mode": case["lesson_design_mode"],
                "teacher_input": case["teacher_input"],
                "strict_json_success": False,
                "success": False,
                "provider_called": True,
                "model_called": True,
                "parser_mode": "provider_error",
                "validation_errors": [exc.code],
                "error_message_redacted": redact_text(exc.message)[:500],
                "secret_scan_hits": [],
                "parsed_json": None,
            }
        write_json(case["filename"], result)
        results.append(result)
        traces.append(
            {
                "case_id": result["case_id"],
                "lesson_design_mode": result["lesson_design_mode"],
                "teacher_input": result["teacher_input"],
                "provider_called": result.get("provider_called", False),
                "model_called": result.get("model_called", False),
                "strict_json_success": result.get("strict_json_success", False),
                "parser_mode": result.get("parser_mode"),
                "extraction_required": result.get("extraction_required", False),
                "validation_errors": result.get("validation_errors", []),
                "secret_scan_hits": result.get("secret_scan_hits", []),
                "latency_ms": result.get("latency_ms"),
                "provider_meta": result.get("provider_meta", {}),
                "redacted_request": result.get("redacted_request", ""),
                "raw_response_redacted": result.get("raw_response_redacted", ""),
            }
        )

    final_status, next_stage = final_status_for(results)
    criteria = aggregate_pass_criteria(results)
    if not criteria.get("secret_scan_ok"):
        final_status = "FAIL_SECRET_SCAN_HIT"
        next_stage = "1013E_R1_SECRET_REVIEW"
    result_payload = {
        "stage_id": STAGE_ID,
        "created_at": now(),
        "final_status": final_status,
        "provider_called": any(item.get("provider_called") for item in results),
        "model_called": any(item.get("model_called") for item in results),
        "provider_status": provider_status,
        "pass_criteria": criteria,
        "case_files": [case["filename"] for case in TEST_CASES],
        "boundary_flags": {
            "teacher_review_required": True,
            "formal_apply_performed": False,
            "database_written": False,
            "memory_written": False,
            "feishu_written": False,
            "formal_export_created": False,
            "official_archive_created": False,
        },
        "next_stage": next_stage,
    }
    latencies = [item.get("latency_ms") for item in results if isinstance(item.get("latency_ms"), int)]
    metrics = {
        "provider_called": result_payload["provider_called"],
        "model_called": result_payload["model_called"],
        "case_count": len(results),
        "strict_json_success_count": criteria["strict_json_success_count"],
        "safe_success_count": criteria["safe_success_count"],
        "latency_summary": {
            "count": len(latencies),
            "min_ms": min(latencies) if latencies else None,
            "max_ms": max(latencies) if latencies else None,
            "avg_ms": round(sum(latencies) / len(latencies)) if latencies else None,
        },
        "provider_status": provider_status,
    }
    write_json("1013E_result.json", result_payload)
    write_json("provider_metrics_1013E.json", metrics)
    write_json("redacted_provider_trace_1013E.json", traces)
    write_report(final_status, next_stage, results, criteria)
    print(json.dumps(result_payload, ensure_ascii=False, indent=2))
    return 0 if final_status.startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
