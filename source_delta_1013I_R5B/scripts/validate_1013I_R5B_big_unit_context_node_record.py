from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R5B_BIG_UNIT_CONTEXT_NODE_RECORD"
NEXT_STAGE = "1013I_R6_TEACHER_SELF_PREP_RENDER_SURFACE_ALPHA_WITH_BIG_UNIT_PLACEHOLDER"
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]
REQUIRED_BIG_UNIT_FIELDS = [
    "unit_title",
    "grade",
    "semester",
    "lesson_title",
    "lesson_position_in_unit",
    "unit_big_idea",
    "unit_essential_question",
    "unit_learning_goals",
    "unit_task_chain",
    "prior_lesson_connection",
    "next_lesson_connection",
    "current_lesson_role",
    "core_competency_focus",
    "evidence_to_collect",
    "assessment_focus",
    "teacher_attention_points",
    "source_material_refs",
]
CURRENT_LESSON_ROLE_ENUM = [
    "unit_entry",
    "concept_building",
    "method_learning",
    "skill_practice",
    "creative_production",
    "critique_and_revision",
    "exhibition_or_reflection",
    "transfer_extension",
    "unknown_pending_teacher_confirm",
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_output_root(root: Path) -> Path:
    nested_output_root = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested_output_root.exists():
        return nested_output_root
    if (
        (root / "1013I_R4_minimal_self_prep_page_fixture").exists()
        or (root / "README.md").exists()
        or (root / "scripts" / Path(__file__).name).exists()
    ):
        return root
    raise FileNotFoundError(
        "Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs. "
        "Run from xiaobei-core root or from the GitHub review repo root."
    )


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_profile() -> dict[str, Any]:
    return {
        "agent_role": "unified_teacher_agent",
        "assistant_profile": {
            "display_name": "小教",
            "display_name_customizable": True,
            "wake_name": "小教",
            "voice_profile_id": None,
            "tts_enabled": False,
            "speaking_style": "calm_professional",
            "assistant_tone": "teacher_work_partner",
            "response_style": "concise_contextual",
        },
        "active_space": "prep_room",
        "active_capability": "lesson_prep",
    }


def build_contract() -> dict[str, Any]:
    profile = build_profile()
    return {
        "contract_id": "big_unit_context_contract_1013I_R5B",
        "stage": STAGE_ID,
        "purpose": "Record the upstream big-unit context node for teacher self-prep before candidate card generation.",
        "big_unit_context_required_fields": REQUIRED_BIG_UNIT_FIELDS,
        "current_lesson_role_enum": CURRENT_LESSON_ROLE_ENUM,
        "node_position": {
            "original_chain": ["teacher_input", "review_cards", "preview_only"],
            "revised_chain": [
                "teacher_input",
                "big_unit_context_check",
                "lesson_position_judgement",
                "review_cards",
                "preview_only",
            ],
            "big_unit_context_check_is_upstream_node": True,
        },
        "fallback_policy": {
            "if_big_unit_material_missing": "可先按单课备课，但建议补充大单元资料。",
            "if_official_big_unit_material_exists": "Use read-only extraction later to build big_unit_context_fixture.",
            "r6_requirement": "R6 render surface must reserve a big-unit position placeholder instead of pretending the node does not exist.",
        },
        "future_official_unit_material_extraction_hook": True,
        "actual_material_parsing_performed": False,
        "contract_only": True,
        "fixture_only": True,
        "preview_only": True,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "official_export_created": False,
        "official_archive_created": False,
        "main_project_pushed": False,
        **profile,
    }


def build_fixture() -> dict[str, Any]:
    profile = build_profile()
    return {
        "fixture_id": "big_unit_context_fixture_1013I_R5B",
        "stage": STAGE_ID,
        "fixture_status": "placeholder_pending_official_material_extraction",
        "big_unit_context": {
            "unit_title": "第一单元 多变的色彩",
            "grade": "三年级",
            "semester": "2025学年第二学期",
            "lesson_title": "色彩的感觉",
            "lesson_position_in_unit": "pending_official_big_unit_material_review",
            "unit_big_idea": "pending_official_big_unit_material_review",
            "unit_essential_question": "颜色如何表达感受并支持创作表达？",
            "unit_learning_goals": [
                "从颜色识别推进到颜色感受表达",
                "在观察、表达、创作和展示中形成连续学习证据",
            ],
            "unit_task_chain": [
                "感知颜色带来的心理和生活经验",
                "用材料和图例支持表达理由",
                "在作品中尝试表达一种感受",
                "通过展示评价回看表达是否清楚",
            ],
            "prior_lesson_connection": "pending_official_sequence_review",
            "next_lesson_connection": "pending_official_sequence_review",
            "current_lesson_role": "unknown_pending_teacher_confirm",
            "core_competency_focus": ["审美感知", "艺术表现", "创意实践"],
            "evidence_to_collect": [
                "学生能否说出颜色感受",
                "学生能否给出与生活或画面相关的理由",
                "学生作品是否能表达一种明确感受",
            ],
            "assessment_focus": [
                "表达是否从喜欢不喜欢推进到感受和理由",
                "作品中的色彩选择是否服务于感受表达",
            ],
            "teacher_attention_points": [
                "不要把单课直接处理成孤立教案",
                "先判断本课在大单元中的角色，再生成候选卡",
                "缺少官方大单元资料时保留待确认状态",
            ],
            "source_material_refs": [
                {
                    "ref_id": "official_big_unit_materials_pending_readonly_extraction",
                    "ref_type": "future_hook",
                    "actual_material_parsing_performed": False,
                    "note": "User reported official big-unit materials exist in the local knowledge base; R5B only records the hook.",
                }
            ],
        },
        "big_unit_context_check": {
            "required_before_candidate_card_generation": True,
            "if_missing": "可先按单课备课，但建议补充大单元资料。",
            "if_available": "Extract unit title, lesson sequence, task chain, assessment focus, and evidence clues before candidate cards.",
        },
        "future_official_unit_material_extraction_hook": True,
        "actual_material_parsing_performed": False,
        "contract_only": True,
        "fixture_only": True,
        "preview_only": True,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "official_export_created": False,
        "official_archive_created": False,
        "main_project_pushed": False,
        **profile,
    }


def scan_deprecated(payload: Any) -> list[str]:
    text = json.dumps(payload, ensure_ascii=False)
    return [name for name in DEPRECATED_VISIBLE_NAMES if name in text]


def build_result(contract: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    context = fixture["big_unit_context"]
    required_fields_present = all(field in context for field in REQUIRED_BIG_UNIT_FIELDS)
    role_enum_present = contract["current_lesson_role_enum"] == CURRENT_LESSON_ROLE_ENUM
    revised_chain = contract["node_position"]["revised_chain"]
    chain_revision_present = "big_unit_context_check" in revised_chain and "lesson_position_judgement" in revised_chain
    deprecated_hits = sorted(set(scan_deprecated(contract) + scan_deprecated(fixture)))
    boundary_false_keys = [
        "actual_material_parsing_performed",
        "provider_called",
        "model_called",
        "formal_apply_performed",
        "lesson_body_modified",
        "html_body_modified",
        "database_written",
        "memory_written",
        "feishu_written",
        "official_export_created",
        "official_archive_created",
        "main_project_pushed",
    ]
    profile_ok = (
        contract["agent_role"] == "unified_teacher_agent"
        and fixture["agent_role"] == "unified_teacher_agent"
        and contract["assistant_profile"]["display_name"] == "小教"
        and fixture["assistant_profile"]["display_name"] == "小教"
        and contract["active_space"] == "prep_room"
        and fixture["active_space"] == "prep_room"
        and contract["active_capability"] == "lesson_prep"
        and fixture["active_capability"] == "lesson_prep"
    )
    final_pass = (
        required_fields_present
        and role_enum_present
        and chain_revision_present
        and contract["future_official_unit_material_extraction_hook"]
        and fixture["future_official_unit_material_extraction_hook"]
        and profile_ok
        and not deprecated_hits
        and not any(contract[key] or fixture[key] for key in boundary_false_keys)
    )
    return {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": f"PASS_{STAGE_ID}" if final_pass else f"FAIL_{STAGE_ID}",
        "next_stage": NEXT_STAGE,
        "big_unit_context_contract_created": True,
        "big_unit_context_fixture_created": True,
        "required_fields_present": required_fields_present,
        "required_fields": REQUIRED_BIG_UNIT_FIELDS,
        "current_lesson_role_enum_present": role_enum_present,
        "chain_revision_present": chain_revision_present,
        "big_unit_context_check_is_upstream_node": contract["node_position"]["big_unit_context_check_is_upstream_node"],
        "future_official_unit_material_extraction_hook": True,
        "actual_material_parsing_performed": False,
        "r6_requires_big_unit_placeholder": True,
        "contract_only": True,
        "fixture_only": True,
        "preview_only": True,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "official_export_created": False,
        "official_archive_created": False,
        "main_project_pushed": False,
        "agent_role": "unified_teacher_agent",
        "assistant_profile_present": True,
        "assistant_profile_display_name": "小教",
        "active_space": "prep_room",
        "active_capability": "lesson_prep",
        "teacher_visible_deprecated_agent_hits": deprecated_hits,
        "formal_apply_allowed": False,
        "provider_model_call_allowed": False,
    }


def build_report(result: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# 1013I R5B Big Unit Context Node Record",
            "",
            f"- FINAL_STATUS: `{result['final_status']}`",
            f"- NEXT_STAGE: `{result['next_stage']}`",
            "- Scope: contract-only / fixture-only record of the big-unit context node.",
            "",
            "## Why This Node Exists",
            "",
            "The teacher self-prep chain cannot treat a lesson as isolated. Before candidate cards are generated, the system must reserve a check for the lesson's position inside the larger unit.",
            "",
            "Original chain:",
            "",
            "```text",
            "teacher_input -> review_cards -> preview_only",
            "```",
            "",
            "Revised chain:",
            "",
            "```text",
            "teacher_input -> big_unit_context_check -> lesson_position_judgement -> review_cards -> preview_only",
            "```",
            "",
            "## Future Hook",
            "",
            "- Official big-unit materials may be read later through a read-only extraction chain.",
            "- R5B does not parse real official materials.",
            "- If big-unit materials are missing, the UI may continue single-lesson prep with a visible recommendation to supplement unit context.",
            "- R6 must reserve a big-unit position placeholder if render surface work continues.",
            "",
            "## Boundary",
            "",
            f"- actual_material_parsing_performed={str(result['actual_material_parsing_performed']).lower()}",
            f"- provider_called={str(result['provider_called']).lower()}",
            f"- model_called={str(result['model_called']).lower()}",
            f"- formal_apply_performed={str(result['formal_apply_performed']).lower()}",
            f"- lesson_body_modified={str(result['lesson_body_modified']).lower()}",
            f"- html_body_modified={str(result['html_body_modified']).lower()}",
            f"- database_written={str(result['database_written']).lower()}",
            f"- memory_written={str(result['memory_written']).lower()}",
            f"- feishu_written={str(result['feishu_written']).lower()}",
            f"- official_export_created={str(result['official_export_created']).lower()}",
            f"- official_archive_created={str(result['official_archive_created']).lower()}",
            "",
        ]
    )


def copy_source_delta(root: Path, output_root: Path) -> None:
    source_delta_dir = output_root / "source_delta_1013I_R5B" / "scripts"
    source_delta_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "scripts" / Path(__file__).name, source_delta_dir / Path(__file__).name)


def run(root: Path) -> int:
    output_root = resolve_output_root(root)
    out_dir = output_root / "1013I_R5B_big_unit_context_node_record"
    contract = build_contract()
    fixture = build_fixture()
    result = build_result(contract, fixture)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "big_unit_context_contract_1013I_R5B.json", contract)
    write_json(out_dir / "big_unit_context_fixture_1013I_R5B.json", fixture)
    write_json(out_dir / "1013I_R5B_result.json", result)
    write_text(out_dir / "big_unit_context_node_report_1013I_R5B.md", build_report(result))
    copy_source_delta(root, output_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=None)
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else repo_root_from_script()
    return run(root)


if __name__ == "__main__":
    raise SystemExit(main())
