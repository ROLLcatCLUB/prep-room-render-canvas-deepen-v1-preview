from __future__ import annotations

from typing import Any

from .output_parser import OutputParserError, parse_patch_output


STAGE_ID = "1013E_MODEL_PROMPT_TO_REASONING_FIELD_PATCH_POC"

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

BOUNDARY_FLAGS = {
    "teacher_review_required": True,
    "formal_apply_performed": False,
    "database_written": False,
    "memory_written": False,
    "feishu_written": False,
    "formal_export_created": False,
    "official_archive_created": False,
}

ALLOWED_IDS = {
    "section_id": [
        "basis",
        "analysis",
        "goals",
        "keypoints",
        "preparation",
        "teaching_process",
        "assessment",
        "reflection",
    ],
    "step_id": ["intro", "sense", "explore", "make", "share"],
    "affected_object": [
        "big_screen",
        "handout",
        "rubric",
        "resource_reference",
        "evidence_note",
        "teacher_action",
        "student_activity",
    ],
    "quality_gate_level": ["basic_usable", "ready_to_teach", "refined", "open_class_ready"],
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
    "boundary_flags": dict(BOUNDARY_FLAGS),
}

HARD_RULES = [
    "只输出 JSON，不要 markdown，不要解释，不要代码块。",
    "不要生成整篇教案；只输出设计判断、字段补丁、影响范围、质量门和页面绑定提示。",
    "field_patch_candidates 必须映射到具体 section_id 或 step_id。",
    "teacher_review_required 必须为 true。",
    "formal_apply_performed、database_written、memory_written、feishu_written、formal_export_created、official_archive_created 必须为 false。",
    "教师可见内容要说人话，不要出现 schema、provider、database、memory、Feishu、formal_apply 等界面词。",
    "不要伪造真实学生档案；没有真实记录时标明为教学预设或小备推测。",
]


def parse_lesson_reasoning_output(
    raw_text: str,
    provider_meta: dict[str, Any] | None = None,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    try:
        payload, parser_meta = parse_patch_output(raw_text, provider_meta)
    except OutputParserError as exc:
        return None, {
            "parser_mode": "json_parse_error",
            "parse_subcode": exc.parse_subcode,
            "parse_error_code": exc.code,
            "parse_error_message": exc.message,
            "diagnostics": exc.diagnostics,
            "extraction_required": False,
        }
    if not isinstance(payload, dict):
        return None, {
            "parser_mode": "strict_json_parser",
            "parse_subcode": "non_object_json",
            "parse_error_code": "json_contract_error",
            "parse_error_message": "Provider output JSON must be an object.",
            "diagnostics": {},
            "extraction_required": False,
        }
    meta = dict(parser_meta or {})
    meta["extraction_required"] = bool(meta.get("provider_output_sanitized"))
    return payload, meta


def validate_lesson_reasoning_payload(parsed: dict[str, Any] | None) -> list[str]:
    if not isinstance(parsed, dict):
        return ["parsed_result_not_object"]
    errors: list[str] = []
    required_keys = [
        "lesson_design_mode",
        "intent_summary",
        "intent_classification",
        "lesson_design_brief",
        "patch_target_resolution",
        "teaching_step_reasoning_updates",
        "field_patch_candidates",
        "impact_scope",
        "quality_gate_update",
        "teacher_questions",
        "ui_binding_hint",
        "boundary_flags",
    ]
    for key in required_keys:
        if key not in parsed:
            errors.append(f"missing_{key}")

    brief = parsed.get("lesson_design_brief")
    if not isinstance(brief, dict):
        errors.append("lesson_design_brief_not_object")
    else:
        for key in ["core_learning_problem", "student_baseline", "target_shift", "teaching_route", "evidence_plan"]:
            if not brief.get(key):
                errors.append(f"lesson_design_brief_missing_{key}")

    patches = parsed.get("field_patch_candidates")
    if not _is_non_empty_list(patches):
        errors.append("missing_field_patch_candidates")
    else:
        for index, patch in enumerate(patches):
            if not isinstance(patch, dict):
                errors.append(f"patch_{index}_not_object")
                continue
            if not patch.get("target_section") and not patch.get("target_step_id"):
                errors.append(f"patch_{index}_missing_target")
            if not patch.get("target_field"):
                errors.append(f"patch_{index}_missing_target_field")
            if patch.get("teacher_review_required") is not True:
                errors.append(f"patch_{index}_teacher_review_required_not_true")
            if patch.get("formal_apply_performed") is not False:
                errors.append(f"patch_{index}_formal_apply_not_false")

    step_updates = parsed.get("teaching_step_reasoning_updates")
    if not isinstance(step_updates, list):
        errors.append("teaching_step_reasoning_updates_not_list")
    elif step_updates:
        needed = [
            "student_state_before",
            "student_state_after",
            "teacher_action",
            "student_action",
            "big_screen_state",
            "learning_sheet_state",
            "assessment_evidence",
        ]
        for key in needed:
            if not any(isinstance(item, dict) and item.get(key) for item in step_updates):
                errors.append(f"step_updates_missing_{key}")

    impact = parsed.get("impact_scope")
    if not _is_non_empty_list(impact):
        errors.append("missing_impact_scope")

    gate = parsed.get("quality_gate_update")
    if not isinstance(gate, dict):
        errors.append("quality_gate_update_not_object")
    elif gate.get("level") not in {"basic_usable", "ready_to_teach", "refined", "open_class_ready"}:
        errors.append("quality_gate_level_invalid")

    boundary = parsed.get("boundary_flags") if isinstance(parsed.get("boundary_flags"), dict) else {}
    if boundary.get("teacher_review_required") is not True:
        errors.append("boundary_teacher_review_required_not_true")
    for key in [
        "formal_apply_performed",
        "database_written",
        "memory_written",
        "feishu_written",
        "formal_export_created",
        "official_archive_created",
    ]:
        if boundary.get(key) is not False:
            errors.append(f"boundary_{key}_not_false")
    return errors


def build_lesson_reasoning_request(case: dict[str, Any], source_context: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "task": "把教师自然语言意图转成课时设计推理字段补丁，验证模型是否稳定输出结构化 JSON。",
        "fixed_lesson_context": LESSON_CONTEXT,
        "lesson_design_mode": case["lesson_design_mode"],
        "teacher_input": case["teacher_input"],
        "case_expectation": case["expectation"],
        "source_context": source_context,
        "required_output_shape": REQUIRED_OUTPUT_SHAPE,
        "allowed_ids": ALLOWED_IDS,
        "hard_rules": HARD_RULES,
    }


def _is_non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)
