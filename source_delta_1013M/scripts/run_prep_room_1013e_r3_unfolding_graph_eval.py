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
    evaluate_classroom_unfolding_effectiveness,
    evaluate_time_balance,
    normalize_lesson_reasoning_wide_payload,
    parse_lesson_reasoning_output,
    validate_lesson_unfolding_graph_payload,
)


STAGE_ID = "1013E_R3_LESSON_UNFOLDING_GRAPH_SCHEMA_NORMALIZER_AND_EFFECTIVENESS_EVAL"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "live_poc_1013E_R3"

SECRET_PATTERNS = [
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]{12,}", re.I),
    re.compile(r"sk-[A-Za-z0-9_\-]{12,}", re.I),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{12,}", re.I),
    re.compile(r"(?i)(api[_-]?key|authorization|secret|tenant_access_token)\s*[:=]\s*['\"][^'\"]{8,}"),
]

CASES = [
    {
        "case_id": "standard_daily_cold_warm_more_visual",
        "lesson_design_mode": "standard_daily",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "topic": "1-2《色彩的感觉》",
        "duration_minutes": 40,
        "lesson_position": "unit_middle",
        "teacher_input": "学生对冷暖色不太理解，要设计得更直观一点。",
        "student_baseline": "学生知道常见颜色，也会说喜欢，但冷暖色理解停在表层。",
        "expected_focus": ["冷暖色", "直观材料", "探究", "学习单", "评价证据"],
    },
    {
        "case_id": "standard_daily_art_music_dance_rhythm",
        "lesson_design_mode": "standard_daily",
        "grade": "三年级",
        "subject": "美术",
        "unit": "节奏与表现",
        "topic": "节奏与色彩/线条表现",
        "duration_minutes": 40,
        "lesson_position": "unit_middle",
        "teacher_input": "我想放一段美术和音乐结合的舞蹈，让学生感受节奏，再引到线条和色彩表现。帮我设计这一段怎么展开。",
        "student_baseline": "学生知道线条和颜色能表达感受，但容易把节奏理解成热闹或好看。",
        "expected_focus": ["资源目的", "观看焦点", "收集感受", "支架", "过渡语"],
    },
    {
        "case_id": "quick_daily_basic_design",
        "lesson_design_mode": "quick_daily",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "topic": "1-2《色彩的感觉》",
        "duration_minutes": 40,
        "lesson_position": "unit_middle",
        "teacher_input": "今天时间不多，先帮我快速整理一版能上课的基本设计。",
        "student_baseline": "学生能说颜色名称，但表达理由容易停在好看、漂亮。",
        "expected_focus": ["够上课", "少追问", "时间可行", "评价证据"],
    },
    {
        "case_id": "open_class_question_expression_evidence",
        "lesson_design_mode": "open_class",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "topic": "1-2《色彩的感觉》",
        "duration_minutes": 40,
        "lesson_position": "unit_middle",
        "teacher_input": "这节课我要拿来展示，问题串、学生表达和评价证据要更清楚。",
        "student_baseline": "学生愿意说，但常常只说颜色好看，需要问题和表达支架。",
        "expected_focus": ["问题串", "学生表达", "大屏状态", "评价证据"],
    },
    {
        "case_id": "research_lesson_color_feeling_transition",
        "lesson_design_mode": "research_lesson",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "topic": "1-2《色彩的感觉》",
        "duration_minutes": 40,
        "lesson_position": "unit_middle",
        "teacher_input": "我想研究学生怎么从说颜色好看，过渡到能说明颜色带来的感受。",
        "student_baseline": "学生有颜色经验，但表达多停留在喜好判断，缺少理由链。",
        "expected_focus": ["学习问题", "教学假设", "证据链", "学生反应"],
    },
    {
        "case_id": "constrained_low_resource_no_video",
        "lesson_design_mode": "standard_daily",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "topic": "1-2《色彩的感觉》",
        "duration_minutes": 40,
        "lesson_position": "unit_middle",
        "teacher_input": "这节课不能放视频，也没有平板，只有黑板和几张图片，帮我把活动改得还能上。",
        "student_baseline": "学生需要直观材料支持，单靠口头讲解容易理解偏浅。",
        "expected_focus": ["资源替代", "黑板", "图片", "支架", "证据"],
    },
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


def build_prompt(case: dict[str, Any], *, retry: bool = False) -> dict[str, str]:
    max_events = 3 if case["lesson_design_mode"] in {"quick_daily", "standard_daily"} else 4
    request = {
        "task": "把教师意图推演成课时展开图。只返回 JSON，不写完整教案。",
        "case": {
            "case_id": case["case_id"],
            "lesson_design_mode": case["lesson_design_mode"],
            "grade": case["grade"],
            "subject": case["subject"],
            "unit": case["unit"],
            "topic": case["topic"],
            "duration_minutes": case["duration_minutes"],
            "lesson_position": case["lesson_position"],
            "teacher_input": case["teacher_input"],
            "student_baseline": case["student_baseline"],
            "expected_focus": case["expected_focus"],
        },
        "output_shape": {
            "lesson_unfolding_graph": {
                "lesson_design_mode": "string",
                "design_context": {"grade": case["grade"], "subject": case["subject"], "topic": case["topic"]},
                "cognitive_grounding": {
                    "core_learning_problem": "string",
                    "student_baseline": "string",
                    "real_stuck_point": "string",
                    "target_shift": "从...到...",
                    "key_focus": "string",
                    "key_difficulty": "string",
                },
                "constraints": {
                    "total_duration_minutes": case["duration_minutes"],
                    "resource_budget": "low|medium|high",
                    "class_condition": "string",
                    "lesson_position": case["lesson_position"],
                    "material_conditions": ["string"],
                },
                "main_event_sequence": ["E1"],
                "classroom_events": [
                    {
                        "event_id": "E1",
                        "event_name": "string",
                        "duration": {"recommended_minutes": 5, "min_minutes": 3, "max_minutes": 7, "time_risk": "string"},
                        "execution_view": {
                            "teacher_focus_cue": "老师可直接说的一句话",
                            "core_question": "string",
                            "student_task": "string",
                            "teacher_summary_sentence": "string",
                        },
                        "design_view": {
                            "learning_purpose": "string",
                            "design_intent": "string",
                            "student_state_before": "string",
                            "student_state_after": "string",
                            "teacher_action": "string",
                            "student_action": "string",
                            "big_screen_state": "string",
                            "textbook_or_material_state": "string",
                            "learning_sheet_state": "string",
                            "assessment_evidence": "string",
                            "transition_from_previous": "string",
                            "transition_to_next": "string",
                            "risk_and_adjustment": "string",
                        },
                        "student_response_model": [
                            {"type": "expected|partial|misconception|off_focus|silent", "student_response": "string", "teacher_next_move": "string", "scaffold": "string"}
                        ],
                        "resource_use": {"resource_type": "string", "why_needed": "string", "attention_focus": "string", "fallback_if_unavailable": "string"},
                        "teacher_review_required": True,
                        "formal_apply_performed": False,
                    }
                ],
                "structure_rebalance_candidates": [],
                "evidence_plan": ["string"],
                "lesson_position_connection": {
                    "unit_start_entry": "",
                    "unit_middle_next_lesson_connection": "string",
                    "unit_end_closure": "",
                },
                "closure_plan": "string",
                "next_lesson_connection": "string",
                "quality_gate": {},
            },
            "field_patch_candidates": [],
            "impact_scope": [],
            "quality_gate_update": {},
            "boundary_flags": BOUNDARY_FLAGS,
        },
        "rules": [
            f"classroom_events 写 {max_events} 个以内。",
            "每个事件必须有 teacher_focus_cue、student_task、student_state_before、student_state_after、assessment_evidence、transition_to_next。",
            "至少一个事件要预判 expected 和 off_focus 或 silent 反应，并写 teacher_next_move/scaffold。",
            "如果资源不可用，resource_use.fallback_if_unavailable 必须写替代方案。",
            "所有内容都是候选，teacher_review_required=true，formal_apply_performed=false。",
            "不要说已写入、已同步、已归档、已正式应用。",
        ],
    }
    if retry:
        request = {
            "task": "返回纯 JSON 课堂展开候选，字段短，不能写完整教案。",
            "case": {
                "case_id": case["case_id"],
                "lesson_design_mode": case["lesson_design_mode"],
                "topic": case["topic"],
                "duration_minutes": case["duration_minutes"],
                "teacher_input": case["teacher_input"],
                "student_baseline": case["student_baseline"],
            },
            "must_keys": [
                "lesson_unfolding_graph",
                "field_patch_candidates",
                "impact_scope",
                "quality_gate_update",
                "boundary_flags",
            ],
            "lesson_unfolding_graph_minimum": {
                "cognitive_grounding": "core_learning_problem student_baseline real_stuck_point target_shift key_focus key_difficulty",
                "constraints": "total_duration_minutes resource_budget class_condition lesson_position material_conditions",
                "main_event_sequence": ["E1", "E2"],
                "classroom_events": "恰好2个。每个有 duration execution_view design_view student_response_model resource_use teacher_review_required formal_apply_performed",
            },
            "rules": [
                "第一个字符必须是 {，最后一个字符必须是 }。",
                "不要 markdown，不要代码块，不要解释。",
                "每个字符串不超过 32 个汉字。",
                "每个事件必须有学生进入前、完成后、评价证据、过渡语。",
                "至少一个学生反应必须是 off_focus 或 silent，并给支架。",
                "不要正式应用，必须等老师确认。",
            ],
        }
    return {
        "system_prompt": "你是师维备课室的小备。你的任务是推演课堂如何发生，只输出 JSON 候选，不写整篇教案，不做正式应用。",
        "user_prompt": json.dumps(request, ensure_ascii=False, separators=(",", ":")),
    }


def call_provider(case: dict[str, Any]) -> dict[str, Any]:
    prompt = build_prompt(case)
    attempts = []
    try:
        attempt = request_provider(case, prompt, retry=False)
        attempts.append(attempt)
    except providers.ProviderError as exc:
        attempts.append(
            {
                "raw_text": "",
                "parsed": None,
                "parser_mode": "provider_error",
                "parser_meta": {"provider_error_code": exc.code},
                "provider_meta": exc.meta or {},
                "latency_ms": None,
                "error_message_redacted": redact_text(exc.message)[:500],
            }
        )
        retry_prompt = build_prompt(case, retry=True)
        attempt = request_provider(case, retry_prompt, retry=True)
        attempts.append(attempt)
        prompt = retry_prompt
    if not attempt["parsed"]:
        retry_prompt = build_prompt(case, retry=True)
        try:
            retry_attempt = request_provider(case, retry_prompt, retry=True)
        except providers.ProviderError as exc:
            retry_attempt = {
                "raw_text": "",
                "parsed": None,
                "parser_mode": "provider_error",
                "parser_meta": {"provider_error_code": exc.code},
                "provider_meta": exc.meta or {},
                "latency_ms": None,
                "error_message_redacted": redact_text(exc.message)[:500],
            }
        attempts.append(retry_attempt)
        if retry_attempt["parsed"]:
            attempt = retry_attempt
            prompt = retry_prompt
    parsed = attempt["parsed"]
    normalized = normalize_lesson_reasoning_wide_payload(parsed)
    contract_errors = validate_lesson_unfolding_graph_payload(normalized)
    effectiveness = evaluate_classroom_unfolding_effectiveness(normalized)
    graph = normalized.get("lesson_unfolding_graph") if isinstance(normalized, dict) else {}
    time_balance = evaluate_time_balance(graph, ((graph or {}).get("constraints") or {}).get("total_duration_minutes", case["duration_minutes"]) if isinstance(graph, dict) else case["duration_minutes"])
    normalization_success = isinstance(normalized, dict) and isinstance(normalized.get("lesson_unfolding_graph"), dict)
    contract_success = not contract_errors
    boundary_ok = _boundary_ok(normalized)
    secret_hits = secret_scan_text(attempt["raw_text"]) + secret_scan_text(json.dumps(normalized, ensure_ascii=False))
    case_result = {
        "case_id": case["case_id"],
        "lesson_design_mode": case["lesson_design_mode"],
        "teacher_input": case["teacher_input"],
        "strict_json_success": attempt["parser_mode"] == "strict_json_parser",
        "wide_json_parse_success": bool(parsed),
        "normalization_success": normalization_success,
        "contract_validation_success": contract_success,
        "contract_validation_errors": contract_errors,
        "effectiveness_pass": bool(effectiveness.get("pass")),
        "boundary_ok": boundary_ok,
        "secret_scan_hits": sorted(set(secret_hits)),
        "attempt_count": len(attempts),
        "attempts": [_public_attempt(item) for item in attempts],
        "normalized_payload": normalized,
        "classroom_unfolding_effectiveness": effectiveness,
        "time_balance": time_balance,
        "provider_called": True,
        "model_called": True,
        "provider_meta": public_provider_meta(attempt["provider_meta"]),
    }
    return {
        "case_result": case_result,
        "trace": {
            "case_id": case["case_id"],
            "attempt_count": len(attempts),
            "redacted_request": redact_text(json.dumps(prompt, ensure_ascii=False)),
            "raw_response_redacted": redact_text(attempt["raw_text"]),
            "attempts": [_public_attempt(item) for item in attempts],
        },
    }


def request_provider(case: dict[str, Any], prompt: dict[str, str], *, retry: bool) -> dict[str, Any]:
    started = time.perf_counter()
    provider_result = providers.generate_json_patch(
        {"mode": STAGE_ID, "case_id": case["case_id"], "retry": retry},
        prompt,
        {
            "provider": "openai_compatible",
            "model": "MiniMax-M3",
            "temperature": 0.1,
            "max_tokens": 3200 if not retry else 2200,
            "timeout_ms": 120000,
            "use_response_format": True,
            "use_reasoning_split": False,
        },
    )
    latency_ms = round((time.perf_counter() - started) * 1000)
    raw_text = str(provider_result.get("raw_text") or "")
    provider_meta = provider_result.get("provider_meta") if isinstance(provider_result.get("provider_meta"), dict) else {}
    parsed, parser_meta = parse_lesson_reasoning_output(raw_text, provider_meta)
    parser_mode = parser_meta.get("parser_mode") or "unknown"
    if parsed is None:
        parsed, wide_meta = parse_wide_json(raw_text)
        if parsed is not None:
            parser_mode = wide_meta["parser_mode"]
            parser_meta = {**parser_meta, **wide_meta}
    return {
        "raw_text": raw_text,
        "parsed": parsed,
        "parser_mode": parser_mode,
        "parser_meta": parser_meta,
        "provider_meta": provider_meta,
        "latency_ms": provider_meta.get("latency_ms") or latency_ms,
    }


def parse_wide_json(raw_text: str) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    text = str(raw_text or "").strip()
    if not text:
        return None, {"parser_mode": "wide_json_parse_error", "parse_error_code": "empty_output"}
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3 and lines[0].startswith("```") and lines[-1].strip() == "```":
            text = "\n".join(lines[1:-1]).strip()
    try:
        payload = json.loads(text)
        return payload if isinstance(payload, dict) else None, {"parser_mode": "wide_json_parser", "extraction_method": "unfenced_or_direct"}
    except json.JSONDecodeError:
        extracted = extract_balanced_json_object(text)
        if extracted:
            try:
                payload = json.loads(extracted)
                return payload if isinstance(payload, dict) else None, {"parser_mode": "wide_json_parser", "extraction_method": "balanced_object"}
            except json.JSONDecodeError:
                pass
    return None, {"parser_mode": "wide_json_parse_error", "parse_error_code": "invalid_json_output"}


def extract_balanced_json_object(text: str) -> str:
    start = text.find("{")
    if start < 0:
        return ""
    depth = 0
    in_string = False
    escape = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    return ""


def aggregate_results(case_results: list[dict[str, Any]]) -> dict[str, Any]:
    def count(key: str) -> int:
        return sum(1 for item in case_results if item.get(key))

    return {
        "case_count": len(case_results),
        "strict_or_wide_parse_success_count": sum(1 for item in case_results if item.get("strict_json_success") or item.get("wide_json_parse_success")),
        "normalization_success_count": count("normalization_success"),
        "contract_validation_success_count": count("contract_validation_success"),
        "effectiveness_pass_count": count("effectiveness_pass"),
        "boundary_ok_count": count("boundary_ok"),
        "secret_scan_ok": not any(item.get("secret_scan_hits") for item in case_results),
    }


def final_status_for(case_results: list[dict[str, Any]], aggregate: dict[str, Any]) -> tuple[str, str]:
    standard = next((item for item in case_results if item["case_id"] == "standard_daily_cold_warm_more_visual"), {})
    dance = next((item for item in case_results if item["case_id"] == "standard_daily_art_music_dance_rhythm"), {})
    dance_graph = ((dance.get("normalized_payload") or {}).get("lesson_unfolding_graph") or {})
    dance_has_event = bool(dance_graph.get("classroom_events"))
    if not aggregate.get("secret_scan_ok"):
        return "FAIL_SECRET_SCAN_HIT", "1013E_R3_SECRET_REVIEW"
    if not standard.get("contract_validation_success") or not standard.get("effectiveness_pass"):
        return "FAIL_STANDARD_DAILY_REPAIR", "1013E_R4_MODEL_STRATEGY_ADJUSTMENT"
    if not dance_has_event or aggregate.get("effectiveness_pass_count", 0) < 4:
        return "FAIL_CLASSROOM_UNFOLDING_EFFECTIVENESS", "1013E_R4_TEACHING_EVENT_PROMPT_REPAIR"
    if (
        aggregate.get("strict_or_wide_parse_success_count", 0) >= 5
        and aggregate.get("normalization_success_count", 0) >= 5
        and aggregate.get("contract_validation_success_count", 0) >= 5
        and aggregate.get("boundary_ok_count", 0) >= 5
    ):
        return "PASS_LESSON_UNFOLDING_GRAPH_NORMALIZER_AND_EFFECTIVENESS_EVAL", "1013F_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING"
    return "FAIL_CLASSROOM_UNFOLDING_EFFECTIVENESS", "1013E_R4_TEACHING_EVENT_PROMPT_REPAIR"


def write_report(result: dict[str, Any], case_results: list[dict[str, Any]], aggregate: dict[str, Any]) -> None:
    lines = [
        "# 1013E_R3 Lesson Unfolding Graph Normalizer And Effectiveness Eval",
        "",
        "```text",
        f"final_status={result['final_status']}",
        f"next_stage={result['next_stage']}",
        f"strict_or_wide_parse_success_count={aggregate['strict_or_wide_parse_success_count']}/6",
        f"normalization_success_count={aggregate['normalization_success_count']}/6",
        f"contract_validation_success_count={aggregate['contract_validation_success_count']}/6",
        f"effectiveness_pass_count={aggregate['effectiveness_pass_count']}/6",
        f"boundary_ok_count={aggregate['boundary_ok_count']}/6",
        f"secret_scan_ok={str(aggregate['secret_scan_ok']).lower()}",
        "```",
        "",
        "## Case Results",
        "",
        "| case_id | parse | normalized | contract | effectiveness | boundary |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in case_results:
        lines.append(
            f"| `{item['case_id']}` | {str(bool(item.get('strict_json_success') or item.get('wide_json_parse_success'))).lower()} | "
            f"{str(bool(item.get('normalization_success'))).lower()} | {str(bool(item.get('contract_validation_success'))).lower()} | "
            f"{str(bool(item.get('effectiveness_pass'))).lower()} | {str(bool(item.get('boundary_ok'))).lower()} |"
        )
    lines.extend(
        [
            "",
            "## classroom_unfolding_script_result",
            "",
            "- Generated through `lesson_unfolding_graph.classroom_events`.",
            "- Each event separates execution view, design view, response model, resource use, duration, and boundary flags.",
            "",
            "## classroom_unfolding_effectiveness_eval",
            "",
            "- Evaluates resource purpose, attention focus, teacher guidance, student response prediction, scaffold quality, collection/evidence, media/material timing, transition, time feasibility, and age appropriateness.",
            "",
            "## dance_rhythm_case_result",
            "",
            "- The dance/rhythm case is treated only as a teacher-provided classroom event request, not as a default resource inserted into unrelated lessons.",
            "",
            "## Boundary",
            "",
            "- Provider may be called for six cases.",
            "- No database write.",
            "- No memory write.",
            "- No Feishu write.",
            "- No formal apply.",
            "- No official export.",
            "- No official archive.",
            "- No UI binding.",
            "- Requests and responses are redacted in trace outputs.",
        ]
    )
    write_text("1013E_R3_report.md", "\n".join(lines) + "\n")


def blocked_outputs(provider_status: dict[str, Any]) -> int:
    case_results = []
    for case in CASES:
        case_results.append(
            {
                "case_id": case["case_id"],
                "lesson_design_mode": case["lesson_design_mode"],
                "teacher_input": case["teacher_input"],
                "strict_json_success": False,
                "wide_json_parse_success": False,
                "normalization_success": False,
                "contract_validation_success": False,
                "effectiveness_pass": False,
                "boundary_ok": True,
                "provider_called": False,
                "model_called": False,
                "error": "missing_provider_env",
            }
        )
    aggregate = aggregate_results(case_results)
    result = {
        "stage_id": STAGE_ID,
        "created_at": now(),
        "final_status": "BLOCKED_MISSING_PROVIDER_ENV",
        "next_stage": "1013E_R3_PROVIDER_ENV_RECHECK",
        "provider_called": False,
        "model_called": False,
        "provider_status": provider_status,
        "aggregate": aggregate,
        "boundary_flags": dict(BOUNDARY_FLAGS),
    }
    write_all_outputs(result, case_results, [], [], aggregate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2


def write_all_outputs(
    result: dict[str, Any],
    case_results: list[dict[str, Any]],
    traces: list[dict[str, Any]],
    prompts: list[dict[str, Any]],
    aggregate: dict[str, Any],
) -> None:
    standard = next((item for item in case_results if item["case_id"] == "standard_daily_cold_warm_more_visual"), {})
    dance = next((item for item in case_results if item["case_id"] == "standard_daily_art_music_dance_rhythm"), {})
    normalization_trace = [
        {
            "case_id": item["case_id"],
            "normalization_success": item.get("normalization_success"),
            "contract_validation_success": item.get("contract_validation_success"),
            "contract_validation_errors": item.get("contract_validation_errors") or [],
        }
        for item in case_results
    ]
    effectiveness_eval = [
        {
            "case_id": item["case_id"],
            **(item.get("classroom_unfolding_effectiveness") or {}),
        }
        for item in case_results
    ]
    time_trace = [{"case_id": item["case_id"], **(item.get("time_balance") or {})} for item in case_results]
    metrics = {
        "provider_called": result.get("provider_called"),
        "model_called": result.get("model_called"),
        "case_count": len(case_results),
        "aggregate": aggregate,
        "provider_status": result.get("provider_status"),
    }
    write_json("1013E_R3_result.json", result)
    write_json("case_results_1013E_R3.json", case_results)
    write_json("standard_daily_repair_result_1013E_R3.json", standard)
    write_json("dance_rhythm_case_result_1013E_R3.json", dance)
    write_json("wide_to_unfolding_normalization_trace_1013E_R3.json", normalization_trace)
    write_json("classroom_unfolding_effectiveness_eval_1013E_R3.json", effectiveness_eval)
    write_json("time_rebalance_trace_1013E_R3.json", time_trace)
    write_json("provider_metrics_1013E_R3.json", metrics)
    write_json("redacted_provider_trace_1013E_R3.json", traces)
    write_text("prompt_repair_1013E_R3.md", prompt_markdown(prompts))
    write_report(result, case_results, aggregate)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    provider_status = provider_public_status()
    prompts = [{"case_id": case["case_id"], "prompt": build_prompt(case)} for case in CASES]
    if not provider_status.get("credential_available"):
        return blocked_outputs(provider_status)

    case_results = []
    traces = []
    for case in CASES:
        try:
            outcome = call_provider(case)
            case_results.append(public_case_result(outcome["case_result"]))
            traces.append(outcome["trace"])
        except providers.ProviderError as exc:
            case_results.append(
                {
                    "case_id": case["case_id"],
                    "lesson_design_mode": case["lesson_design_mode"],
                    "teacher_input": case["teacher_input"],
                    "strict_json_success": False,
                    "wide_json_parse_success": False,
                    "normalization_success": False,
                    "contract_validation_success": False,
                    "contract_validation_errors": [exc.code],
                    "effectiveness_pass": False,
                    "boundary_ok": True,
                    "provider_called": True,
                    "model_called": True,
                    "error_message_redacted": redact_text(exc.message)[:500],
                    "secret_scan_hits": [],
                }
            )
            traces.append({"case_id": case["case_id"], "provider_error": exc.code, "message_redacted": redact_text(exc.message)[:500]})
    aggregate = aggregate_results(case_results)
    final_status, next_stage = final_status_for(case_results, aggregate)
    result = {
        "stage_id": STAGE_ID,
        "created_at": now(),
        "final_status": final_status,
        "next_stage": next_stage,
        "provider_called": any(item.get("provider_called") for item in case_results),
        "model_called": any(item.get("model_called") for item in case_results),
        "provider_status": provider_status,
        "aggregate": aggregate,
        "boundary_flags": dict(BOUNDARY_FLAGS),
    }
    write_all_outputs(result, case_results, traces, prompts, aggregate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if final_status == "PASS_LESSON_UNFOLDING_GRAPH_NORMALIZER_AND_EFFECTIVENESS_EVAL" else 1


def _boundary_ok(payload: dict[str, Any] | None) -> bool:
    if not isinstance(payload, dict):
        return False
    boundary = payload.get("boundary_flags") if isinstance(payload.get("boundary_flags"), dict) else {}
    if boundary.get("teacher_review_required") is not True or boundary.get("formal_apply_performed") is not False:
        return False
    graph = payload.get("lesson_unfolding_graph") if isinstance(payload.get("lesson_unfolding_graph"), dict) else {}
    events = graph.get("classroom_events") if isinstance(graph.get("classroom_events"), list) else []
    return all(event.get("teacher_review_required") is True and event.get("formal_apply_performed") is False for event in events if isinstance(event, dict))


def public_case_result(case_result: dict[str, Any]) -> dict[str, Any]:
    payload = dict(case_result)
    return payload


def _public_attempt(attempt: dict[str, Any]) -> dict[str, Any]:
    return {
        "parser_mode": attempt.get("parser_mode"),
        "latency_ms": attempt.get("latency_ms"),
        "provider_meta": public_provider_meta(attempt.get("provider_meta") or {}),
        "raw_response_prefix_redacted": redact_text(attempt.get("raw_text") or "")[:800],
    }


def public_provider_meta(meta: dict[str, Any]) -> dict[str, Any]:
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


def prompt_markdown(prompts: list[dict[str, Any]]) -> str:
    lines = ["# 1013E_R3 Prompt Template", ""]
    if prompts:
        sample = prompts[0]["prompt"]
        lines.extend(["## System Prompt", "", sample["system_prompt"], "", "## Sample User Prompt", "", sample["user_prompt"], ""])
    lines.extend(["## Case Prompts", ""])
    for item in prompts:
        lines.append(f"- `{item['case_id']}`")
    return "\n".join(lines) + "\n"


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


if __name__ == "__main__":
    raise SystemExit(main())

