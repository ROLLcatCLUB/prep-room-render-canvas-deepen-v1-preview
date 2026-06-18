from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6A_BIG_UNIT_CONTEXT_REQUIRED_GATE"
NEXT_STAGE = "1013I_R6B_OFFICIAL_BIG_UNIT_MATERIAL_READONLY_EXTRACTION_FIXTURE"
R6_PASS_STATUS = "PASS_1013I_R6_TEACHER_SELF_PREP_RENDER_SURFACE_ALPHA"
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]
GATE_STATUS_ENUM = [
    "missing",
    "candidate_extracted",
    "teacher_confirmed",
    "degraded_single_lesson_mode",
]
GATE_DECISION_ENUM = [
    "block_single_lesson_prep",
    "allow_after_teacher_confirm",
    "allow_degraded_single_lesson_draft",
]
SOURCE_QUALITY_ENUM = [
    "none",
    "teacher_input_only",
    "official_material",
    "official_material_plus_teacher_confirm",
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
REQUIRED_EXTRACTION_FIELDS = [
    "source_doc_id",
    "source_title",
    "source_type",
    "source_authority_level",
    "unit_title_candidates",
    "lesson_sequence_candidates",
    "big_idea_candidates",
    "essential_question_candidates",
    "task_chain_candidates",
    "assessment_focus_candidates",
    "evidence_collection_candidates",
    "quote_anchor_refs",
    "extraction_confidence",
    "teacher_confirmation_required",
]
SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)app[_-]?secret\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)tenant[_-]?access[_-]?token\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)cookie\s*[:=]\s*['\"][^'\"]{20,}"),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_output_root(root: Path) -> Path:
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    if (
        (root / "README.md").exists()
        or (root / "1013I_R6_teacher_self_prep_render_surface_alpha").exists()
        or (root / "scripts" / Path(__file__).name).exists()
    ):
        return root
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def profile() -> dict[str, Any]:
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


def boundary() -> dict[str, Any]:
    return {
        "contract_only": True,
        "fixture_only": True,
        "preview_only": True,
        "actual_material_parsing_performed": False,
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
    }


def build_big_unit_context() -> dict[str, Any]:
    return {
        "unit_title": "第一单元 多变的色彩",
        "grade": "三年级",
        "semester": "2025学年第二学期",
        "lesson_title": "色彩的感觉",
        "lesson_position_in_unit": "missing_pending_official_material_extraction",
        "unit_big_idea": "pending_official_material_readonly_extraction",
        "unit_essential_question": "颜色如何表达感受，并在作品与交流中形成可观察的学习证据？",
        "unit_learning_goals": [],
        "unit_task_chain": [],
        "prior_lesson_connection": "pending_lesson_sequence_extraction",
        "next_lesson_connection": "pending_lesson_sequence_extraction",
        "current_lesson_role": "unknown_pending_teacher_confirm",
        "core_competency_focus": ["审美感知", "艺术表现", "创意实践", "文化理解"],
        "evidence_to_collect": [],
        "assessment_focus": [],
        "teacher_attention_points": [
            "单课候选生成前必须先判断本课在大单元学习进程中的位置。",
            "缺少大单元上下文时只能进入临时单课草案，不进入完整备课链。",
        ],
        "source_material_refs": [],
    }


def build_gate_contract() -> dict[str, Any]:
    return {
        "contract_id": "big_unit_context_gate_contract_1013I_R6A",
        "stage": STAGE_ID,
        "required_before_single_lesson_prep": True,
        "gate_status_enum": GATE_STATUS_ENUM,
        "gate_decision_enum": GATE_DECISION_ENUM,
        "teacher_confirmation_required": True,
        "source_quality_enum": SOURCE_QUALITY_ENUM,
        "missing_context_message": "缺少大单元上下文，不能直接进入完整单课备课候选。",
        "degraded_mode_warning": "缺少大单元上下文，本次仅为临时单课草案，不进入完整备课链。",
        "next_required_action": "先读取或补充官方大单元资料，抽取单元结构，并由教师确认本课位置。",
        "revised_chain": [
            "teacher_input",
            "big_unit_context_gate",
            "lesson_position_judgement",
            "teacher_confirm_unit_position",
            "self_prep_review_cards",
            "preview_only",
        ],
        "big_unit_context_required_fields": REQUIRED_BIG_UNIT_FIELDS,
        "current_lesson_role_enum": CURRENT_LESSON_ROLE_ENUM,
        "r7_visual_review_paused": True,
        "r6_product_semantics_changed": False,
        **boundary(),
        **profile(),
    }


def build_gate_fixture() -> dict[str, Any]:
    return {
        "fixture_id": "big_unit_context_gate_fixture_1013I_R6A",
        "stage": STAGE_ID,
        "big_unit_context_gate": {
            "required_before_single_lesson_prep": True,
            "status": "missing",
            "decision": "block_single_lesson_prep",
            "teacher_confirmation_required": True,
            "reason": "单课备课必须先判断本课在大单元中的位置。",
            "source_quality": "none",
            "missing_context_message": "缺少大单元上下文，不能直接进入完整单课备课候选。",
            "degraded_mode_warning": "缺少大单元上下文，本次仅为临时单课草案，不进入完整备课链。",
            "next_required_action": "进入官方大单元资料只读抽取 fixture。",
        },
        "lesson_position_judgement": {
            "registered": True,
            "status": "pending_big_unit_context",
            "teacher_confirm_unit_position_required": True,
        },
        "degraded_single_lesson_mode": {
            "defined": True,
            "allowed_only_after_teacher_choice": True,
            "warning": "缺少大单元上下文，本次仅为临时单课草案。",
        },
        "big_unit_context": build_big_unit_context(),
        **boundary(),
        **profile(),
    }


def build_extraction_hook() -> dict[str, Any]:
    return {
        "hook_id": "big_unit_context_official_material_extraction_hook_1013I_R6A",
        "stage": STAGE_ID,
        "purpose": "Define the future read-only extraction shape for official big-unit materials.",
        "readonly_only": True,
        "actual_material_parsing_performed": False,
        "fields_to_extract": REQUIRED_EXTRACTION_FIELDS,
        "sample_extraction_record": {
            "source_doc_id": None,
            "source_title": None,
            "source_type": "official_big_unit_material",
            "source_authority_level": "official",
            "unit_title_candidates": [],
            "lesson_sequence_candidates": [],
            "big_idea_candidates": [],
            "essential_question_candidates": [],
            "task_chain_candidates": [],
            "assessment_focus_candidates": [],
            "evidence_collection_candidates": [],
            "quote_anchor_refs": [],
            "extraction_confidence": "not_run",
            "teacher_confirmation_required": True,
        },
        **boundary(),
        **profile(),
    }


def scan_deprecated(*payloads: Any) -> list[str]:
    text = json.dumps(payloads, ensure_ascii=False)
    return [name for name in DEPRECATED_VISIBLE_NAMES if name in text]


def scan_secrets(*payloads: Any) -> list[str]:
    text = json.dumps(payloads, ensure_ascii=False)
    return [pattern.pattern for pattern in SECRET_PATTERNS if pattern.search(text)]


def build_result(
    r6_result: dict[str, Any],
    contract: dict[str, Any],
    fixture: dict[str, Any],
    hook: dict[str, Any],
) -> dict[str, Any]:
    context = fixture["big_unit_context"]
    gate = fixture["big_unit_context_gate"]
    required_fields_present = all(field in context for field in REQUIRED_BIG_UNIT_FIELDS)
    hook_fields_present = all(field in hook["sample_extraction_record"] for field in REQUIRED_EXTRACTION_FIELDS)
    false_keys = [
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
    deprecated_hits = scan_deprecated(contract, fixture, hook)
    secret_hits = scan_secrets(contract, fixture, hook)
    profile_ok = all(
        payload["agent_role"] == "unified_teacher_agent"
        and payload["assistant_profile"]["display_name"] == "小教"
        and payload["active_space"] == "prep_room"
        and payload["active_capability"] == "lesson_prep"
        for payload in [contract, fixture, hook]
    )
    final_pass = (
        r6_result.get("final_status") == R6_PASS_STATUS
        and contract["required_before_single_lesson_prep"]
        and contract["gate_status_enum"] == GATE_STATUS_ENUM
        and contract["gate_decision_enum"] == GATE_DECISION_ENUM
        and contract["source_quality_enum"] == SOURCE_QUALITY_ENUM
        and contract["teacher_confirmation_required"]
        and bool(contract["missing_context_message"])
        and bool(contract["degraded_mode_warning"])
        and gate["required_before_single_lesson_prep"]
        and fixture["lesson_position_judgement"]["registered"]
        and fixture["lesson_position_judgement"]["teacher_confirm_unit_position_required"]
        and fixture["degraded_single_lesson_mode"]["defined"]
        and required_fields_present
        and contract["current_lesson_role_enum"] == CURRENT_LESSON_ROLE_ENUM
        and hook_fields_present
        and hook["readonly_only"]
        and contract["r7_visual_review_paused"]
        and not contract["r6_product_semantics_changed"]
        and profile_ok
        and not deprecated_hits
        and not secret_hits
        and not any(payload[key] for payload in [contract, fixture, hook] for key in false_keys)
    )
    return {
        "stage": STAGE_ID,
        "generated_at": now(),
        "inherits_from": "1013I_R6_TEACHER_SELF_PREP_RENDER_SURFACE_ALPHA",
        "final_status": f"PASS_{STAGE_ID}" if final_pass else f"FAIL_{STAGE_ID}",
        "next_stage": NEXT_STAGE,
        "r6_result_present": True,
        "r6_final_status": r6_result.get("final_status"),
        "r6_product_semantics_changed": False,
        "r7_visual_review_paused": True,
        "big_unit_context_gate_created": True,
        "required_before_single_lesson_prep": True,
        "lesson_position_judgement_registered": True,
        "teacher_confirm_unit_position_registered": True,
        "degraded_single_lesson_mode_defined": True,
        "official_material_extraction_hook_created": True,
        "gate_status_enum_complete": contract["gate_status_enum"] == GATE_STATUS_ENUM,
        "gate_decision_enum_complete": contract["gate_decision_enum"] == GATE_DECISION_ENUM,
        "source_quality_enum_complete": contract["source_quality_enum"] == SOURCE_QUALITY_ENUM,
        "big_unit_context_required_fields_present": required_fields_present,
        "current_lesson_role_enum_complete": contract["current_lesson_role_enum"] == CURRENT_LESSON_ROLE_ENUM,
        "official_material_extraction_hook_fields_present": hook_fields_present,
        "teacher_visible_deprecated_agent_hits": deprecated_hits,
        "secret_scan_hits": secret_hits,
        "agent_role": "unified_teacher_agent",
        "assistant_profile_present": True,
        "assistant_profile_display_name": "小教",
        "active_space": "prep_room",
        "active_capability": "lesson_prep",
        "formal_apply_allowed": False,
        "provider_model_call_allowed": False,
        **boundary(),
    }


def build_report(result: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# 1013I R6A Big Unit Context Required Gate",
            "",
            f"- FINAL_STATUS: `{result['final_status']}`",
            f"- NEXT_STAGE: `{result['next_stage']}`",
            "- Scope: contract-only / fixture-only required gate; no real material parsing.",
            "",
            "## Decision",
            "",
            "Single-lesson prep is paused as a normal path until the system has a big-unit context gate and lesson-position judgement.",
            "",
            "Revised chain:",
            "",
            "```text",
            "teacher_input -> big_unit_context_gate -> lesson_position_judgement -> teacher_confirm_unit_position -> self_prep_review_cards -> preview_only",
            "```",
            "",
            "## Gate Behavior",
            "",
            "- Missing big-unit context blocks normal single-lesson prep.",
            "- A degraded single-lesson draft is allowed only as a clearly labeled temporary mode.",
            "- Official big-unit materials enter later through read-only extraction, then teacher confirmation.",
            "",
            "## Boundary",
            "",
            f"- r7_visual_review_paused={str(result['r7_visual_review_paused']).lower()}",
            f"- r6_product_semantics_changed={str(result['r6_product_semantics_changed']).lower()}",
            f"- actual_material_parsing_performed={str(result['actual_material_parsing_performed']).lower()}",
            f"- provider_called={str(result['provider_called']).lower()}",
            f"- model_called={str(result['model_called']).lower()}",
            f"- formal_apply_performed={str(result['formal_apply_performed']).lower()}",
            f"- lesson_body_modified={str(result['lesson_body_modified']).lower()}",
            f"- html_body_modified={str(result['html_body_modified']).lower()}",
            f"- database_written={str(result['database_written']).lower()}",
            f"- memory_written={str(result['memory_written']).lower()}",
            f"- feishu_written={str(result['feishu_written']).lower()}",
            "",
        ]
    )


def copy_source_delta(root: Path, output_root: Path) -> None:
    source_delta_dir = output_root / "source_delta_1013I_R6A" / "scripts"
    source_delta_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "scripts" / Path(__file__).name, source_delta_dir / Path(__file__).name)


def run(root: Path) -> int:
    output_root = resolve_output_root(root)
    r6_result = read_json(output_root / "1013I_R6_teacher_self_prep_render_surface_alpha" / "1013I_R6_result.json")
    out_dir = output_root / "1013I_R6A_big_unit_context_required_gate"
    contract = build_gate_contract()
    fixture = build_gate_fixture()
    hook = build_extraction_hook()
    result = build_result(r6_result, contract, fixture, hook)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "big_unit_context_gate_contract_1013I_R6A.json", contract)
    write_json(out_dir / "big_unit_context_gate_fixture_1013I_R6A.json", fixture)
    write_json(out_dir / "big_unit_context_official_material_extraction_hook_1013I_R6A.json", hook)
    write_json(out_dir / "1013I_R6A_result.json", result)
    write_text(out_dir / "1013I_R6A_report.md", build_report(result))
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
