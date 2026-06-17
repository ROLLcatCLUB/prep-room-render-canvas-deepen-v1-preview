from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.xiaobei_ai import prep_room_feishu_schedule_1013A, providers  # noqa: E402


STAGE_ID = "1013A_LIVE_PREP_NOTEBOOK_FIELD_PATCH_POC_WITH_FEISHU_SCHEDULE"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "live_poc"
ALLOWED_LAYERS = {"l1_basic", "l2_lesson_execution", "l3_resource_collab", "l4_reflection"}
TEST_CASES = [
    {
        "case_id": "test_1",
        "label": "学情驱动修改",
        "teacher_input": "学生对冷暖色不太理解，要设计得更直观一点。",
    },
    {
        "case_id": "test_2",
        "label": "快速成稿",
        "teacher_input": "先帮我快速生成一版能上课的基本课时设计。",
    },
    {
        "case_id": "test_3",
        "label": "深度打磨",
        "teacher_input": "这节课我想做得更适合公开课展示，问题串和评价证据要更清楚。",
    },
]

INITIAL_CONTEXT = {
    "lesson_ref": {
        "semester": "2026春学期",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "lesson_code": "1-2",
        "lesson_title": "色彩的感觉",
        "duration_minutes": 40,
    },
    "prep_package": {
        "l1_basic": {
            "teacher_goal": "让学生感受冷暖色带来的不同情绪",
            "core_activity": "观察生活中的色彩并尝试表达",
            "assessment_focus": "色彩感受、表达意图、过程参与",
        },
        "l2_lesson_execution": {
            "learning_objectives": [],
            "classroom_flow": [],
            "teacher_questions": [],
            "student_activities": [],
        },
        "l3_resource_collab": {
            "handout": "candidate_exists",
            "rubric": "missing",
            "resource_reference": "candidate_only",
        },
        "l4_reflection": {
            "evidence_note": "not_started",
        },
    },
    "available_resource_candidates": [
        "色彩单元课标摘要",
        "冷暖色图片素材",
        "优秀课例《色彩的感觉》",
        "美术评价量规维度：色彩、创意、过程性评价",
    ],
}

REQUIRED_SCHEMA = {
    "intent_summary": "",
    "target_lesson": {
        "lesson_code": "1-2",
        "lesson_title": "色彩的感觉",
    },
    "field_patch_candidates": [
        {
            "field_patch_id": "patch_001",
            "target_layer": "l1_basic | l2_lesson_execution | l3_resource_collab | l4_reflection",
            "target_block": "",
            "target_field": "",
            "patch_type": "fill_missing | revise | restructure | add_example | simplify | enrich",
            "before_summary": "",
            "after_candidate": "",
            "source_basis": ["教师意图", "课表上下文", "课标摘要候选", "教材/课例候选", "美术学科模板"],
            "teacher_review_required": True,
            "formal_apply_performed": False,
        }
    ],
    "missing_slots": [{"slot": "", "question": "", "options": []}],
    "quality_gate": {
        "level": "基础可用 | 可上课 | 可公开展示",
        "passed_items": [],
        "missing_items": [],
        "next_best_action": "",
    },
    "right_tray_updates": {
        "suggestion": "",
        "pending_review_items": [],
        "resource_candidates_used": [],
        "archive_candidates": [],
    },
    "boundary_flags": {
        "teacher_review_required": True,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_export_created": False,
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


def secret_scan_text(text: str) -> list[str]:
    hits = []
    for pattern in SECRET_PATTERNS:
        if pattern.search(text or ""):
            hits.append(pattern.pattern)
    return hits


def extract_json(raw_text: str) -> tuple[dict[str, Any] | None, bool, str]:
    text = str(raw_text or "").strip()
    if not text:
        return None, False, "empty_response"
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else None, False, "strict_json"
    except json.JSONDecodeError:
        pass
    fenced = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", text)
    candidates = []
    if fenced:
        candidates.append(fenced.group(1))
    first = text.find("{")
    last = text.rfind("}")
    if first >= 0 and last > first:
        candidates.append(text[first : last + 1])
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
            return parsed if isinstance(parsed, dict) else None, True, "extracted_json"
        except json.JSONDecodeError:
            continue
    return None, True, "json_parse_failed"


def validate_result(parsed: dict[str, Any] | None) -> list[str]:
    if not isinstance(parsed, dict):
        return ["parsed_result_not_object"]
    errors: list[str] = []
    patches = parsed.get("field_patch_candidates")
    if not isinstance(patches, list) or not patches:
        errors.append("missing_field_patch_candidates")
    else:
        for index, patch in enumerate(patches):
            if not isinstance(patch, dict):
                errors.append(f"patch_{index}_not_object")
                continue
            if patch.get("target_layer") not in ALLOWED_LAYERS:
                errors.append(f"patch_{index}_target_layer_invalid")
            if patch.get("teacher_review_required") is not True:
                errors.append(f"patch_{index}_teacher_review_required_not_true")
            if patch.get("formal_apply_performed") is not False:
                errors.append(f"patch_{index}_formal_apply_not_false")
    boundary = parsed.get("boundary_flags") if isinstance(parsed.get("boundary_flags"), dict) else {}
    for key in ["formal_apply_performed", "database_written", "memory_written", "feishu_written", "formal_export_created"]:
        if boundary.get(key) is not False:
            errors.append(f"boundary_{key}_not_false")
    if boundary.get("teacher_review_required") is not True:
        errors.append("boundary_teacher_review_required_not_true")
    gate = parsed.get("quality_gate") if isinstance(parsed.get("quality_gate"), dict) else {}
    if gate.get("level") not in {"基础可用", "可上课", "可公开展示"}:
        errors.append("quality_gate_level_invalid")
    return errors


def build_prompt(case: dict[str, str], schedule_result: dict[str, Any]) -> dict[str, str]:
    schedule_context = {
        "source_kind": schedule_result.get("source_kind"),
        "teacher_profile": schedule_result.get("teacher_profile"),
        "schedule_slots": [
            {
                "weekday": slot.get("weekday"),
                "period": slot.get("period"),
                "class_name": slot.get("class_name"),
                "room": slot.get("room"),
                "source_record_id": slot.get("source_record_id"),
            }
            for slot in (schedule_result.get("schedule_slots") or [])[:12]
        ],
        "boundary_flags": schedule_result.get("boundary_flags"),
    }
    user_payload = {
        "task": "把教师一句话转成备课本主备课画布的结构化字段候选补丁。",
        "teacher_input": case["teacher_input"],
        "initial_context": INITIAL_CONTEXT,
        "formal_schedule_context": schedule_context,
        "required_json_schema": REQUIRED_SCHEMA,
        "hard_rules": [
            "只输出 JSON，不要 Markdown，不要代码块，不要解释。",
            "不要生成整篇教案，只生成字段候选补丁。",
            "每个候选都必须等待教师确认。",
            "不得写数据库、memory、飞书，不得正式导出，不得正式归档。",
            "输出文字短而可放进备课本字段。",
        ],
    }
    return {
        "system_prompt": (
            "你是师维备课室主助理小备，服务小学美术教师。"
            "你只把教师意图转成备课字段候选补丁，不直接定稿。"
            "严格只输出一个 JSON 对象。"
        ),
        "user_prompt": json.dumps(user_payload, ensure_ascii=False),
    }


def call_provider(case: dict[str, str], schedule_result: dict[str, Any]) -> dict[str, Any]:
    prompt = build_prompt(case, schedule_result)
    started = time.perf_counter()
    provider_result = providers.generate_json_patch(
        {"mode": "prep_notebook_field_patch_poc", "case_id": case["case_id"]},
        prompt,
        {
            "provider": "openai_compatible",
            "temperature": 0.1,
            "max_tokens": 2400,
            "timeout_ms": 70000,
            "use_response_format": True,
        },
    )
    latency_ms = round((time.perf_counter() - started) * 1000)
    raw_text = provider_result.get("raw_text") or ""
    parsed, extraction_required, parser_mode = extract_json(raw_text)
    errors = validate_result(parsed)
    meta = provider_result.get("provider_meta") or {}
    return {
        "case_id": case["case_id"],
        "label": case["label"],
        "teacher_input": case["teacher_input"],
        "success": not errors,
        "parser_mode": parser_mode,
        "extraction_required": bool(extraction_required),
        "validation_errors": errors,
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
        "raw_response_stored": False,
        "raw_response_preview_redacted": raw_text[:180].replace("\n", " "),
        "parsed_json": parsed,
        "secret_scan_hits": secret_scan_text(raw_text),
    }


def blocked_missing_provider(schedule_result: dict[str, Any]) -> dict[str, Any]:
    status = providers.provider_status()
    public_status = {
        "provider_name": status.get("provider_name"),
        "credential_available": bool((status.get("generation") or {}).get("credential_available")),
        "credential_source": (status.get("generation") or {}).get("credential_source"),
        "model": (status.get("generation") or {}).get("model"),
    }
    return {
        "stage_id": STAGE_ID,
        "final_status": "BLOCKED_MISSING_PROVIDER_ENV",
        "provider_called": False,
        "model_called": False,
        "schedule_source_kind": schedule_result.get("source_kind"),
        "provider_status": public_status,
        "next_stage": "1013A_R1_PROVIDER_ENV_RECHECK",
    }


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    schedule_result, schedule_status = prep_room_feishu_schedule_1013A.get_schedule({"source": "auto"})
    write_json("feishu_schedule_binding_1013A.json", schedule_result)

    status = providers.provider_status()
    generation = status.get("generation") or {}
    if not generation.get("credential_available"):
        result = blocked_missing_provider(schedule_result)
        write_json("1013A_live_poc_result.json", result)
        write_json("provider_metrics_1013A.json", {"provider_called": False, "model_called": False, "reason": "missing_provider_env"})
        write_json("redacted_provider_trace_1013A.json", [])
        write_text(
            "1013A_live_poc_report.md",
            "# 1013A Live POC\n\n```text\nfinal_status=BLOCKED_MISSING_PROVIDER_ENV\nprovider_called=false\nmodel_called=false\n```\n",
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    traces = []
    test_results = []
    for case in TEST_CASES:
        try:
            result = call_provider(case, schedule_result)
        except providers.ProviderError as exc:
            result = {
                "case_id": case["case_id"],
                "label": case["label"],
                "teacher_input": case["teacher_input"],
                "success": False,
                "provider_called": True,
                "model_called": True,
                "error_code": exc.code,
                "error_message_redacted": str(exc.message)[:200],
                "parsed_json": None,
                "validation_errors": [exc.code],
                "secret_scan_hits": [],
            }
        test_results.append(result)
        write_json(f"{case['case_id']}_field_patch_result.json", result)
        traces.append(
            {
                "case_id": result["case_id"],
                "provider_called": result.get("provider_called", False),
                "model_called": result.get("model_called", False),
                "success": result.get("success", False),
                "parser_mode": result.get("parser_mode"),
                "extraction_required": result.get("extraction_required", False),
                "latency_ms": result.get("latency_ms"),
                "provider_meta": result.get("provider_meta", {}),
                "raw_response_stored": False,
                "secret_scan_hits": result.get("secret_scan_hits", []),
            }
        )

    success_count = sum(1 for item in test_results if item.get("success"))
    extraction_count = sum(1 for item in test_results if item.get("extraction_required"))
    failed_count = len(test_results) - success_count
    strict_count = sum(1 for item in test_results if item.get("success") and not item.get("extraction_required"))
    any_secret_hits = any(item.get("secret_scan_hits") for item in test_results)
    if success_count == 0:
        final_status = "FAIL_MODEL_OUTPUT_NOT_USABLE"
        next_stage = "1013A_R1_PROMPT_REPAIR"
    elif extraction_count:
        final_status = "PASS_WITH_EXTRACTION_CAVEAT" if success_count >= 2 else "FAIL_MODEL_OUTPUT_NOT_USABLE"
        next_stage = "1013B_PREP_NOTEBOOK_LIVE_FIELD_PATCH_TO_UI_BINDING" if success_count >= 2 else "1013A_R1_PROMPT_REPAIR"
    else:
        final_status = "PASS_STRICT_JSON" if success_count >= 2 else "FAIL_MODEL_OUTPUT_NOT_USABLE"
        next_stage = "1013B_PREP_NOTEBOOK_LIVE_FIELD_PATCH_TO_UI_BINDING" if success_count >= 2 else "1013A_R1_PROMPT_REPAIR"
    if any_secret_hits:
        final_status = "FAIL_SECRET_SCAN_HIT"
        next_stage = "1013A_R1_SECRET_REVIEW"

    latencies = [item.get("latency_ms") for item in test_results if isinstance(item.get("latency_ms"), int)]
    result = {
        "stage_id": STAGE_ID,
        "created_at": now(),
        "final_status": final_status,
        "provider_called": any(item.get("provider_called") for item in test_results),
        "model_called": any(item.get("model_called") for item in test_results),
        "strict_json_success_count": strict_count,
        "extraction_required_count": extraction_count,
        "failed_count": failed_count,
        "successful_case_count": success_count,
        "field_patch_candidate_generated": any((item.get("parsed_json") or {}).get("field_patch_candidates") for item in test_results),
        "schedule_status_code": schedule_status,
        "schedule_source_kind": schedule_result.get("source_kind"),
        "schedule_slot_count": len(schedule_result.get("schedule_slots") or []),
        "boundary_flags": {
            "teacher_review_required": True,
            "formal_apply_performed": False,
            "database_written": False,
            "memory_written": False,
            "feishu_written": False,
            "formal_export_created": False,
            "feishu_schedule_written": False,
            "frontend_secret_exposed": False,
        },
        "latency_summary": {
            "count": len(latencies),
            "min_ms": min(latencies) if latencies else None,
            "max_ms": max(latencies) if latencies else None,
            "avg_ms": round(sum(latencies) / len(latencies)) if latencies else None,
        },
        "next_stage": next_stage,
    }
    metrics = {
        "provider_called": result["provider_called"],
        "model_called": result["model_called"],
        "case_count": len(test_results),
        "strict_json_success_count": strict_count,
        "extraction_required_count": extraction_count,
        "failed_count": failed_count,
        "latency_summary": result["latency_summary"],
        "provider_status": {
            "credential_source": generation.get("credential_source"),
            "model": generation.get("model"),
            "base_url": generation.get("base_url"),
        },
    }
    report = f"""# 1013A Live Prep Notebook Field Patch POC

```text
final_status={final_status}
provider_called={str(result["provider_called"]).lower()}
model_called={str(result["model_called"]).lower()}
schedule_source_kind={result["schedule_source_kind"]}
schedule_slot_count={result["schedule_slot_count"]}
strict_json_success_count={strict_count}
extraction_required_count={extraction_count}
failed_count={failed_count}
next_stage={next_stage}
```

## Boundary

- Feishu schedule was read only; Feishu write stayed false.
- Provider output was saved only as parsed field-patch JSON and redacted trace.
- No API key, Authorization header, tenant token, database write, memory write, formal export, or formal apply was produced.

## Cases

""" + "\n".join(
        f"- {item['case_id']} {item['label']}: {'PASS' if item.get('success') else 'FAIL'}; parser={item.get('parser_mode') or item.get('error_code')}"
        for item in test_results
    ) + "\n"

    write_json("1013A_live_poc_result.json", result)
    write_json("provider_metrics_1013A.json", metrics)
    write_json("redacted_provider_trace_1013A.json", traces)
    write_text("1013A_live_poc_report.md", report)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if final_status.startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
