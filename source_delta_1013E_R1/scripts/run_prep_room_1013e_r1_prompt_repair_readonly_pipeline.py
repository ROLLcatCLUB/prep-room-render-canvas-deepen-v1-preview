from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.xiaobei_ai import providers  # noqa: E402
from backend.xiaobei_ai.prep_room_lesson_reasoning_contract_1013E import BOUNDARY_FLAGS, R1_STAGE_ID  # noqa: E402
from backend.xiaobei_ai.prep_room_lesson_reasoning_pipeline_1013E_R1 import (  # noqa: E402
    build_prompt,
    run_prep_room_lesson_reasoning_pipeline,
)


OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "live_poc_1013E_R1"
SOURCE_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"

TEST_CASES = [
    {
        "case_id": "test_quick_daily",
        "filename": "test_quick_daily_result.json",
        "lesson_design_mode": "quick_daily",
        "teacher_input": "今天时间不多，先帮我快速整理一版能上课的基本设计。",
        "expectation": ["够上课", "少追问", "基础评价证据", "不写公开课长设计"],
    },
    {
        "case_id": "test_standard_daily",
        "filename": "test_standard_daily_result.json",
        "lesson_design_mode": "standard_daily",
        "teacher_input": "学生对冷暖色不太理解，要设计得更直观一点。",
        "expectation": ["定位学情分析", "修改探究环节", "补大屏和学习单", "补评价证据"],
    },
    {
        "case_id": "test_open_class",
        "filename": "test_open_class_result.json",
        "lesson_design_mode": "open_class",
        "teacher_input": "这节课我要拿来展示，问题串、学生表达和评价证据要更清楚。",
        "expectation": ["强化问题串", "强化学生表达", "强化展示", "标记待确认问题"],
    },
    {
        "case_id": "test_research_lesson",
        "filename": "test_research_lesson_result.json",
        "lesson_design_mode": "research_lesson",
        "teacher_input": "我想研究学生怎么从说颜色好看，过渡到能说明颜色带来的感受。",
        "expectation": ["明确学习问题", "明确教学假设", "明确证据计划", "不写论文"],
    },
]

SECRET_PATTERNS = [
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]{12,}", re.I),
    re.compile(r"sk-[A-Za-z0-9_\-]{12,}", re.I),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{12,}", re.I),
    re.compile(r"(?i)(api[_-]?key|authorization|secret|tenant_access_token)\s*[:=]\s*['\"][^'\"]{8,}"),
]

FORBIDDEN_TRACE_TERMS = [
    "schema",
    "provider",
    "field_patch",
    "database",
    "memory",
    "formal_apply",
    "Feishu",
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


def compact_source_context() -> dict[str, Any]:
    return {
        "lesson_focus": "三年级美术 1-2《色彩的感觉》，40分钟。",
        "core_learning_problem": "学生知道颜色，也会说喜欢或不喜欢，但还不能稳定说明颜色带来的感受和理由。",
        "target_shift": "从看到颜色，到说出感受，再到用色彩表达心情或场景。",
        "default_route": ["生活图片唤起感受", "作品和生活图比较", "色卡和生活物品分组", "分层色彩表达练习", "作品说明和同伴反馈"],
        "default_evidence": ["颜色+感受+原因的一句话", "学习单或口头记录", "作品色彩选择理由", "同伴能否读到相近感受"],
        "step_ids": ["intro", "sense", "explore", "make", "share"],
        "section_ids": ["basis", "analysis", "goals", "keypoints", "preparation", "teaching_process", "assessment", "reflection"],
        "quality_gate_levels": ["basic_usable", "ready_to_teach", "refined", "open_class_ready"],
        "source_basis_policy": "没有真实学生档案时，只能写教学预设、小备推测、教材、课标或资料候选。",
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


def blocked_outputs(provider_status: dict[str, Any], source_context: dict[str, Any]) -> int:
    empty_results = []
    for case in TEST_CASES:
        payload = {
            "case_id": case["case_id"],
            "lesson_design_mode": case["lesson_design_mode"],
            "teacher_input": case["teacher_input"],
            "strict_json_success": False,
            "safe_success": False,
            "provider_called": False,
            "model_called": False,
            "final_status": "BLOCKED_MISSING_PROVIDER_ENV",
            "validation_errors": ["missing_provider_env"],
            "readonly_result": None,
            "visible_trace": None,
        }
        write_json(case["filename"], payload)
        empty_results.append(payload)
    result = {
        "stage_id": R1_STAGE_ID,
        "created_at": now(),
        "final_status": "BLOCKED_MISSING_PROVIDER_ENV",
        "next_stage": "1013E_R1_PROVIDER_ENV_RECHECK",
        "provider_called": False,
        "model_called": False,
        "provider_status": provider_status,
        "pass_criteria": aggregate_pass_criteria(empty_results),
        "boundary_flags": dict(BOUNDARY_FLAGS),
    }
    write_json("1013E_R1_result.json", result)
    write_json("provider_metrics_1013E_R1.json", {"provider_called": False, "model_called": False, "provider_status": provider_status})
    write_json("redacted_provider_trace_1013E_R1.json", [])
    write_json("visible_reasoning_trace_samples_1013E_R1.json", [])
    write_text("prompt_repair_1013E_R1.md", _prompt_markdown(source_context))
    write_report(result, empty_results)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2


def sanitize_case_result(result: dict[str, Any]) -> dict[str, Any]:
    payload = dict(result)
    payload.pop("prompt", None)
    payload.pop("raw_text", None)
    return payload


def trace_entry(result: dict[str, Any]) -> dict[str, Any]:
    prompt = result.get("prompt") if isinstance(result.get("prompt"), dict) else {}
    return {
        "case_id": result.get("case_id"),
        "lesson_design_mode": result.get("lesson_design_mode"),
        "provider_called": result.get("provider_called"),
        "model_called": result.get("model_called"),
        "strict_json_success": result.get("strict_json_success"),
        "safe_success": result.get("safe_success"),
        "parser_mode": result.get("parser_mode"),
        "validation_errors": result.get("validation_errors", []),
        "secret_scan_hits": result.get("secret_scan_hits", []),
        "latency_ms": result.get("latency_ms"),
        "provider_meta": result.get("provider_meta", {}),
        "redacted_request": redact_text(json.dumps(prompt, ensure_ascii=False)),
        "raw_response_redacted": redact_text(str(result.get("raw_text") or "")),
    }


def aggregate_pass_criteria(results: list[dict[str, Any]]) -> dict[str, Any]:
    successes = [item for item in results if item.get("safe_success") and not item.get("validation_errors")]
    strict_count = sum(1 for item in results if item.get("strict_json_success"))
    with_candidates = 0
    with_steps = 0
    impact_objects = set()
    gate_levels = set()
    visible_trace_safe = True
    for item in successes:
        compact = (((item.get("readonly_result") or {}).get("parsed_compact")) or {})
        if compact.get("field_patch_candidates"):
            with_candidates += 1
        if compact.get("step_reasoning_updates"):
            with_steps += 1
        for impact in compact.get("impact_scope") or []:
            if isinstance(impact, dict) and impact.get("affected_object"):
                impact_objects.add(impact["affected_object"])
        gate = compact.get("quality_gate_update") if isinstance(compact.get("quality_gate_update"), dict) else {}
        if gate.get("level"):
            gate_levels.add(gate["level"])
        trace_text = json.dumps(item.get("visible_trace") or {}, ensure_ascii=False)
        if any(term in trace_text for term in FORBIDDEN_TRACE_TERMS):
            visible_trace_safe = False
    boundary_ok = all(
        ((item.get("readonly_result") or {}).get("boundary_flags") or {}).get("teacher_review_required") is True
        and ((item.get("readonly_result") or {}).get("boundary_flags") or {}).get("formal_apply_performed") is False
        and ((item.get("readonly_result") or {}).get("boundary_flags") or {}).get("database_written") is False
        and ((item.get("readonly_result") or {}).get("boundary_flags") or {}).get("memory_written") is False
        and ((item.get("readonly_result") or {}).get("boundary_flags") or {}).get("feishu_written") is False
        for item in successes
    )
    return {
        "strict_json_success_count": strict_count,
        "safe_success_count": len(successes),
        "cases_with_field_patch_candidates": with_candidates,
        "cases_with_step_reasoning_updates": with_steps,
        "impact_objects": sorted(impact_objects),
        "quality_gate_levels": sorted(gate_levels),
        "visible_trace_safe": visible_trace_safe,
        "boundary_ok": boundary_ok,
        "secret_scan_ok": not any(item.get("secret_scan_hits") for item in results),
    }


def final_status_for(results: list[dict[str, Any]], criteria: dict[str, Any]) -> tuple[str, str]:
    if not criteria.get("secret_scan_ok"):
        return "FAIL_SECRET_SCAN_HIT", "1013E_R1_SECRET_REVIEW"
    strict = criteria["strict_json_success_count"]
    safe = criteria["safe_success_count"]
    if strict == 4:
        return "PASS_STRICT_JSON_ALL", "1013F_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING"
    if strict >= 3:
        return "PASS_STRICT_JSON_WITH_ONE_FAILURE", "1013F_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING"
    if safe >= 3:
        return "PASS_WITH_EXTRACTION_CAVEAT", "1013F_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING"
    return "FAIL_MODEL_OUTPUT_NOT_STABLE", "1013E_R1_PROMPT_REPAIR"


def write_report(result_payload: dict[str, Any], results: list[dict[str, Any]]) -> None:
    criteria = result_payload.get("pass_criteria") or {}
    lines = [
        "# 1013E_R1 Prompt Repair And Readonly Reasoning Pipeline",
        "",
        "```text",
        f"final_status={result_payload.get('final_status')}",
        f"next_stage={result_payload.get('next_stage')}",
        f"strict_json_success_count={criteria.get('strict_json_success_count')}",
        f"safe_success_count={criteria.get('safe_success_count')}",
        f"cases_with_field_patch_candidates={criteria.get('cases_with_field_patch_candidates')}",
        f"cases_with_step_reasoning_updates={criteria.get('cases_with_step_reasoning_updates')}",
        f"visible_trace_safe={str(criteria.get('visible_trace_safe')).lower()}",
        f"boundary_ok={str(criteria.get('boundary_ok')).lower()}",
        f"secret_scan_ok={str(criteria.get('secret_scan_ok')).lower()}",
        "```",
        "",
        "## Boundary",
        "",
        "- Provider may be called once per mode.",
        "- No database write.",
        "- No memory write.",
        "- No Feishu write.",
        "- No formal apply.",
        "- No official export or archive.",
        "- Requests and responses are redacted.",
        "",
        "## Test Cases",
        "",
    ]
    for item in results:
        lines.append(
            f"- `{item.get('case_id')}` `{item.get('lesson_design_mode')}`: "
            f"{'PASS' if item.get('strict_json_success') else 'FAIL'}; "
            f"safe={str(bool(item.get('safe_success'))).lower()}; "
            f"parser={item.get('parser_mode')}; errors={len(item.get('validation_errors') or [])}"
        )
    lines.extend([
        "",
        "## Impact Objects",
        "",
        ", ".join(criteria.get("impact_objects") or []) or "none",
        "",
        "## Quality Gate Levels",
        "",
        ", ".join(criteria.get("quality_gate_levels") or []) or "none",
    ])
    write_text("1013E_R1_report.md", "\n".join(lines) + "\n")


def _prompt_markdown(source_context: dict[str, Any]) -> str:
    sample = build_prompt(TEST_CASES[0], source_context)
    return (
        "# 1013E_R1 Prompt Repair Template\n\n"
        "## System Prompt\n\n"
        f"{sample['system_prompt']}\n\n"
        "## Sample User Prompt\n\n"
        f"{sample['user_prompt']}\n"
    )


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    source_context = compact_source_context()
    provider_status = provider_public_status()
    write_text("prompt_repair_1013E_R1.md", _prompt_markdown(source_context))
    if not provider_status.get("credential_available"):
        return blocked_outputs(provider_status, source_context)

    results: list[dict[str, Any]] = []
    traces: list[dict[str, Any]] = []
    visible_samples: list[dict[str, Any]] = []
    for case in TEST_CASES:
        try:
            result = run_prep_room_lesson_reasoning_pipeline(case, source_context=source_context)
        except providers.ProviderError as exc:
            result = {
                "stage_id": R1_STAGE_ID,
                "case_id": case["case_id"],
                "lesson_design_mode": case["lesson_design_mode"],
                "teacher_input": case["teacher_input"],
                "provider_called": True,
                "model_called": True,
                "strict_json_success": False,
                "safe_success": False,
                "parser_mode": "provider_error",
                "validation_errors": [exc.code],
                "error_message_redacted": redact_text(exc.message)[:500],
                "secret_scan_hits": [],
                "readonly_result": None,
                "visible_trace": None,
                "prompt": build_prompt(case, source_context),
                "raw_text": "",
            }
        result["secret_scan_hits"] = sorted(set((result.get("secret_scan_hits") or []) + secret_scan_text(json.dumps(sanitize_case_result(result), ensure_ascii=False))))
        write_json(case["filename"], sanitize_case_result(result))
        results.append(result)
        traces.append(trace_entry(result))
        if result.get("visible_trace"):
            visible_samples.append({"case_id": result["case_id"], "trace": result["visible_trace"]})

    criteria = aggregate_pass_criteria(results)
    final_status, next_stage = final_status_for(results, criteria)
    result_payload = {
        "stage_id": R1_STAGE_ID,
        "created_at": now(),
        "final_status": final_status,
        "next_stage": next_stage,
        "provider_called": any(item.get("provider_called") for item in results),
        "model_called": any(item.get("model_called") for item in results),
        "provider_status": provider_status,
        "pass_criteria": criteria,
        "case_files": [case["filename"] for case in TEST_CASES],
        "boundary_flags": dict(BOUNDARY_FLAGS),
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
    write_json("1013E_R1_result.json", result_payload)
    write_json("provider_metrics_1013E_R1.json", metrics)
    write_json("redacted_provider_trace_1013E_R1.json", traces)
    write_json("visible_reasoning_trace_samples_1013E_R1.json", visible_samples)
    write_report(result_payload, results)
    print(json.dumps(result_payload, ensure_ascii=False, indent=2))
    return 0 if final_status.startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
