from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
PREVIEW_STATE_PATH = OUTPUT_ROOT / "1013H_sandbox_apply_to_preview_only" / "sandbox_preview_state_1013H.json"
OUT_DIR = OUTPUT_ROOT / "1013I_teacher_self_prep_input_minimal_flow"
SOURCE_DELTA_DIR = OUTPUT_ROOT / "source_delta_1013I" / "scripts"

STAGE_ID = "1013I_TEACHER_SELF_PREP_INPUT_MINIMAL_FLOW"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_input_schema() -> dict[str, Any]:
    return {
        "schema_id": "teacher_self_prep_input_schema_1013I",
        "stage": STAGE_ID,
        "purpose": "Capture the minimum teacher input needed to start a lesson-prep preview request without calling a provider or writing formal lesson content.",
        "required_fields": [
            "grade_level",
            "subject",
            "lesson_title",
            "lesson_count",
            "unit_or_textbook_context",
        ],
        "optional_fields": [
            "textbook_version",
            "class_profile_hint",
            "existing_materials",
            "teacher_ideas",
            "classroom_constraints",
            "preferred_depth",
            "resource_preferences",
        ],
        "field_definitions": {
            "grade_level": {"type": "string", "example": "三年级", "teacher_label": "年级"},
            "subject": {"type": "string", "example": "美术", "teacher_label": "学科"},
            "lesson_title": {"type": "string", "example": "色彩的感觉", "teacher_label": "课题"},
            "lesson_count": {"type": "integer", "example": 1, "teacher_label": "课时数"},
            "unit_or_textbook_context": {"type": "string", "example": "第一单元 多变的色彩", "teacher_label": "单元/教材位置"},
            "textbook_version": {"type": "string", "example": "校本/人美版等", "teacher_label": "教材版本"},
            "class_profile_hint": {"type": "string", "example": "学生能说颜色名称，但说理由弱", "teacher_label": "班级情况"},
            "existing_materials": {"type": "array", "items": "string", "teacher_label": "已有材料"},
            "teacher_ideas": {"type": "string", "teacher_label": "老师已有想法"},
            "classroom_constraints": {"type": "array", "items": "string", "teacher_label": "课堂限制"},
            "preferred_depth": {"type": "enum", "values": ["quick_daily", "standard_daily", "polish", "open_class"], "teacher_label": "备课深度"},
            "resource_preferences": {"type": "array", "items": "string", "teacher_label": "资源偏好"},
        },
        "forbidden_behavior": [
            "provider_call",
            "model_call",
            "formal_apply",
            "lesson_body_write",
            "database_write",
            "memory_write",
            "feishu_write",
        ],
    }


def build_teacher_input_fixture() -> dict[str, Any]:
    return {
        "input_fixture_id": "teacher_self_prep_input_fixture_1013I",
        "teacher_id": "local_preview_teacher",
        "space": "备课室",
        "agent": "小备",
        "grade_level": "三年级",
        "subject": "美术",
        "lesson_title": "色彩的感觉",
        "lesson_count": 1,
        "unit_or_textbook_context": "第一单元 多变的色彩",
        "textbook_version": "本地 2025 第二学期三年级美术计划",
        "class_profile_hint": "学生能说出常见颜色和喜欢不喜欢，但把颜色感受说成理由还不稳定。",
        "existing_materials": ["色卡", "生活图片", "课堂学习单草稿"],
        "teacher_ideas": "希望探究别太复杂，让学生能说出颜色带来的感受。",
        "classroom_constraints": ["40分钟常态课", "不做公开课式复杂材料", "展示评价控制在5分钟内"],
        "preferred_depth": "standard_daily",
        "resource_preferences": ["轻学习单", "大屏提示词", "可撤回预览"],
    }


def build_sufficiency_assessment(input_fixture: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    missing_required = [field for field in schema["required_fields"] if not input_fixture.get(field)]
    available_optional = [field for field in schema["optional_fields"] if input_fixture.get(field)]
    can_start_preview = not missing_required
    return {
        "assessment_id": "input_sufficiency_assessment_1013I",
        "required_fields_present": len(missing_required) == 0,
        "missing_required_fields": missing_required,
        "available_optional_fields": available_optional,
        "can_generate_request_envelope": can_start_preview,
        "can_generate_preview_fixture": can_start_preview,
        "needs_follow_up_question": False,
        "follow_up_questions": [],
        "safe_to_call_provider": False,
        "reason": "Required lesson-start fields are present, so a preview fixture can be built without model/provider calls.",
    }


def build_request_envelope(input_fixture: dict[str, Any], assessment: dict[str, Any]) -> dict[str, Any]:
    return {
        "request_id": "teacher_self_prep_request_1013I",
        "stage": STAGE_ID,
        "request_type": "teacher_self_prep_preview_request",
        "teacher_input": input_fixture,
        "input_sufficiency": {
            "required_fields_present": assessment["required_fields_present"],
            "can_generate_preview_fixture": assessment["can_generate_preview_fixture"],
            "needs_follow_up_question": assessment["needs_follow_up_question"],
        },
        "requested_outputs": [
            "self_prep_preview_fixture",
            "candidate_card_seed",
            "preview_chain_bridge",
        ],
        "provider_policy": {
            "provider_call_allowed": False,
            "model_call_allowed": False,
            "reason": "1013I validates the teacher input envelope and preview fixture only.",
        },
        "write_policy": {
            "formal_apply_allowed": False,
            "lesson_body_write_allowed": False,
            "database_write_allowed": False,
            "memory_write_allowed": False,
            "feishu_write_allowed": False,
        },
    }


def build_preview_fixture(request: dict[str, Any], preview_state_1013h: dict[str, Any]) -> dict[str, Any]:
    teacher_input = request["teacher_input"]
    return {
        "fixture_id": "self_prep_preview_fixture_1013I",
        "source_request_id": request["request_id"],
        "preview_mode": "fixture_only_no_provider",
        "lesson_header": {
            "grade_level": teacher_input["grade_level"],
            "subject": teacher_input["subject"],
            "lesson_title": teacher_input["lesson_title"],
            "lesson_count": teacher_input["lesson_count"],
            "unit_or_textbook_context": teacher_input["unit_or_textbook_context"],
            "preferred_depth": teacher_input["preferred_depth"],
        },
        "teacher_visible_summary": "小备已根据年级、课题、单元和老师已有想法整理出一份预览起点，后续仍需教师审阅。",
        "preview_sections": [
            {
                "section_id": "learning_problem",
                "title": "本课先解决什么",
                "preview_text": "学生不只说颜色名称和喜欢不喜欢，而是能把颜色和温暖、清凉、安静、热烈等感受连起来，并说出一个理由。",
                "source": "teacher_input_fixture",
            },
            {
                "section_id": "material_plan",
                "title": "材料先轻后加",
                "preview_text": "先用色卡和感受词卡建立分类，再把生活物品作为已经能说出理由的小组加料材料。",
                "source": "reuse_1013H_preview_pattern",
            },
            {
                "section_id": "review_chain_ready",
                "title": "后续可进入候选审阅",
                "preview_text": "这份预览可继续生成候选卡，再进入教师审阅准备和 sandbox preview。",
                "source": "preview_chain_bridge",
            },
        ],
        "reuse_from_1013H": {
            "preview_state_id": preview_state_1013h["preview_state_id"],
            "accepted_preview_items_count": len(preview_state_1013h.get("accepted_preview_items", [])),
            "preview_only_policy_kept": bool(preview_state_1013h.get("preview_only")),
        },
        "boundary_flags": {
            "fixture_only": True,
            "provider_called": False,
            "model_called": False,
            "formal_apply_performed": False,
            "lesson_body_modified": False,
            "html_body_modified": False,
            "database_written": False,
            "memory_written": False,
            "feishu_written": False,
        },
    }


def build_preview_chain_bridge(request: dict[str, Any], preview_fixture: dict[str, Any]) -> dict[str, Any]:
    return {
        "bridge_id": "preview_chain_bridge_1013I",
        "source_request_id": request["request_id"],
        "source_fixture_id": preview_fixture["fixture_id"],
        "next_chain_candidates": [
            "candidate_card_seed",
            "teacher_review_prep_surface",
            "sandbox_preview_state",
        ],
        "can_enter_candidate_review_later": True,
        "must_pass_teacher_review_before_preview_apply": True,
        "formal_apply_allowed": False,
        "notes": [
            "1013I creates the teacher-start envelope and a fixture preview only.",
            "A later stage may generate candidates from this envelope, but must keep provider/model and write boundaries explicit.",
        ],
    }


def build_result(
    schema: dict[str, Any],
    request: dict[str, Any],
    assessment: dict[str, Any],
    preview_fixture: dict[str, Any],
    bridge: dict[str, Any],
) -> dict[str, Any]:
    boundary = {
        "teacher_input_schema_created": bool(schema),
        "teacher_input_fixture_created": True,
        "request_envelope_created": bool(request),
        "input_sufficiency_assessment_created": bool(assessment),
        "self_prep_preview_fixture_created": bool(preview_fixture),
        "preview_chain_bridge_created": bool(bridge),
        "required_fields_present": assessment["required_fields_present"],
        "can_generate_preview_fixture": assessment["can_generate_preview_fixture"],
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }
    final_pass = (
        boundary["teacher_input_schema_created"]
        and boundary["request_envelope_created"]
        and boundary["input_sufficiency_assessment_created"]
        and boundary["self_prep_preview_fixture_created"]
        and boundary["preview_chain_bridge_created"]
        and boundary["required_fields_present"]
        and boundary["can_generate_preview_fixture"]
        and not any(
            boundary[key]
            for key in [
                "provider_called",
                "model_called",
                "formal_apply_performed",
                "lesson_body_modified",
                "html_body_modified",
                "database_written",
                "memory_written",
                "feishu_written",
                "main_project_pushed",
            ]
        )
    )
    return {
        "stage": STAGE_ID,
        "generated_at": now(),
        "inherits_from": "1013H_SANDBOX_APPLY_TO_PREVIEW_ONLY",
        "final_status": "PASS_1013I_TEACHER_SELF_PREP_INPUT_MINIMAL_FLOW" if final_pass else "FAIL_1013I_TEACHER_SELF_PREP_INPUT_MINIMAL_FLOW",
        "next_stage": "1013I_R1_CANDIDATE_CARD_SEED_FROM_SELF_PREP_REQUEST",
        **boundary,
    }


def build_report(result: dict[str, Any], request: dict[str, Any], assessment: dict[str, Any]) -> str:
    teacher_input = request["teacher_input"]
    lines = [
        "# 1013I Teacher Self Prep Input Minimal Flow",
        "",
        f"- FINAL_STATUS: `{result['final_status']}`",
        f"- NEXT_STAGE: `{result['next_stage']}`",
        "- Boundary: input envelope and fixture preview only; no provider/model call, no formal apply, no lesson body write, no database/memory/Feishu write.",
        "",
        "## Teacher Input",
        "",
        f"- 年级: {teacher_input['grade_level']}",
        f"- 学科: {teacher_input['subject']}",
        f"- 课题: {teacher_input['lesson_title']}",
        f"- 单元: {teacher_input['unit_or_textbook_context']}",
        f"- 备课深度: {teacher_input['preferred_depth']}",
        "",
        "## Sufficiency",
        "",
        f"- required_fields_present={str(assessment['required_fields_present']).lower()}",
        f"- can_generate_request_envelope={str(assessment['can_generate_request_envelope']).lower()}",
        f"- can_generate_preview_fixture={str(assessment['can_generate_preview_fixture']).lower()}",
        f"- needs_follow_up_question={str(assessment['needs_follow_up_question']).lower()}",
        "",
        "## Required Checks",
        "",
        f"- teacher_input_schema_created={str(result['teacher_input_schema_created']).lower()}",
        f"- request_envelope_created={str(result['request_envelope_created']).lower()}",
        f"- input_sufficiency_assessment_created={str(result['input_sufficiency_assessment_created']).lower()}",
        f"- self_prep_preview_fixture_created={str(result['self_prep_preview_fixture_created']).lower()}",
        f"- preview_chain_bridge_created={str(result['preview_chain_bridge_created']).lower()}",
        f"- provider_called={str(result['provider_called']).lower()}",
        f"- model_called={str(result['model_called']).lower()}",
        f"- formal_apply_performed={str(result['formal_apply_performed']).lower()}",
        f"- lesson_body_modified={str(result['lesson_body_modified']).lower()}",
        f"- html_body_modified={str(result['html_body_modified']).lower()}",
        f"- database_written={str(result['database_written']).lower()}",
        f"- memory_written={str(result['memory_written']).lower()}",
        f"- feishu_written={str(result['feishu_written']).lower()}",
    ]
    return "\n".join(lines) + "\n"


def copy_source_delta() -> None:
    SOURCE_DELTA_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA_DIR / Path(__file__).name)


def main() -> int:
    preview_state = read_json(PREVIEW_STATE_PATH)
    schema = build_input_schema()
    input_fixture = build_teacher_input_fixture()
    assessment = build_sufficiency_assessment(input_fixture, schema)
    request = build_request_envelope(input_fixture, assessment)
    preview_fixture = build_preview_fixture(request, preview_state)
    bridge = build_preview_chain_bridge(request, preview_fixture)
    result = build_result(schema, request, assessment, preview_fixture, bridge)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "teacher_self_prep_input_schema_1013I.json", schema)
    write_json(OUT_DIR / "teacher_self_prep_input_fixture_1013I.json", input_fixture)
    write_json(OUT_DIR / "input_sufficiency_assessment_1013I.json", assessment)
    write_json(OUT_DIR / "teacher_self_prep_request_1013I.json", request)
    write_json(OUT_DIR / "self_prep_preview_fixture_1013I.json", preview_fixture)
    write_json(OUT_DIR / "preview_chain_bridge_1013I.json", bridge)
    write_json(OUT_DIR / "1013I_result.json", result)
    write_text(OUT_DIR / "1013I_report.md", build_report(result, request, assessment))
    copy_source_delta()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
