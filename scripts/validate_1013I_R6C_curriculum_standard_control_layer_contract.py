from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6C_CURRICULUM_STANDARD_CONTROL_LAYER_CONTRACT"
FINAL_STATUS = "PASS_1013I_R6C_CURRICULUM_STANDARD_CONTROL_LAYER_CONTRACT"
NEXT_STAGE = "1013I_R6D_TEXTBOOK_ANCHOR_AND_BIG_UNIT_DESIGN_CHAIN_CONTRACT"
INHERITS_FROM = "1013I_R6B_R1_REVIEW_MANIFEST_ALIGNMENT"
R6B_R1_PASS_STATUS = "PASS_1013I_R6B_R1_REVIEW_MANIFEST_ALIGNMENT"
R6B_PASS_STATUS = "PASS_1013I_R6B_OFFICIAL_CASE_READONLY_DECONSTRUCTION_FOR_SCHEMA_CALIBRATION"

STAGE_DIR_NAME = "1013I_R6C_curriculum_standard_control_layer_contract"
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]
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
    if (root / "REVIEW_PACKAGE_MANIFEST.md").exists() and (root / "LATEST_REVIEW_ENTRY.md").exists():
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
        "real_curriculum_standard_full_text_parsed": False,
        "official_curriculum_claim_created": False,
        "big_unit_generation_performed": False,
        "single_lesson_generation_performed": False,
        "product_runtime_called": False,
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


def control_contract() -> dict[str, Any]:
    return {
        "contract_id": "curriculum_standard_control_layer_contract_1013I_R6C",
        "stage": STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "layer_key": "curriculum_standard_control_layer",
        "layer_role": "upstream_constraint_layer",
        "object_name": "lesson_standard_map",
        "object_policy": "Store structured mapping cards and missing markers. Do not store or invent full curriculum-standard text.",
        "authority_rule": {
            "curriculum_standard_outranks_official_case_reference": True,
            "official_case_reference_may_override_curriculum_standard": False,
            "official_case_reference_may_override_textbook_anchor": False,
            "teacher_confirmation_required": True,
            "teacher_confirmation_cannot_remove_required_standard_check": True,
            "textbook_anchor_required_before_lesson_generation": True,
        },
        "required_control_fields": [
            {"field": "standard_version_label", "required": True, "mode": "structured_ref_or_missing"},
            {"field": "subject", "required": True, "mode": "teacher_input_or_textbook_context"},
            {"field": "school_stage", "required": True, "mode": "teacher_input_or_structured_ref"},
            {"field": "grade_band", "required": True, "mode": "teacher_input_or_structured_ref"},
            {"field": "art_domain_or_learning_domain", "required": True, "mode": "structured_ref_or_teacher_confirm"},
            {"field": "core_literacy_tags", "required": True, "mode": "structured_ref_or_candidate_with_teacher_confirm"},
            {"field": "learning_task_direction", "required": True, "mode": "structured_ref_or_missing"},
            {"field": "assessment_requirement", "required": True, "mode": "structured_ref_or_missing"},
            {"field": "academic_quality_or_performance_evidence", "required": True, "mode": "structured_ref_or_missing"},
            {"field": "content_scope_boundary", "required": True, "mode": "structured_ref_or_missing"},
            {"field": "prohibited_overreach", "required": True, "mode": "structured_ref_or_missing"},
            {"field": "standard_ref_ids", "required": True, "mode": "source_ref_or_missing"},
            {"field": "interpretation_status", "required": True, "mode": "enum"},
            {"field": "teacher_confirmation_status", "required": True, "mode": "enum"},
        ],
        "interpretation_status_enum": [
            "missing_structured_standard_ref",
            "candidate_interpretation_pending_teacher_review",
            "structured_standard_ref_available",
            "teacher_confirmed_standard_mapping",
        ],
        "teacher_confirmation_status_enum": [
            "not_requested",
            "pending_teacher_confirm",
            "teacher_confirmed",
            "teacher_rejected_or_needs_revision",
        ],
        "relation_to_big_unit_context_gate": {
            "required_before_big_unit_candidate_generation": True,
            "required_before_lesson_position_judgement": True,
            "feeds_fields": [
                "unit_learning_goals",
                "core_competency_focus",
                "evidence_to_collect",
                "assessment_focus",
                "teacher_attention_points",
            ],
            "missing_standard_action": "hold_normal_self_prep_and_request_standard_or_allow_labeled_degraded_draft",
        },
        "relation_to_textbook_anchor": {
            "textbook_anchor_required": True,
            "curriculum_standard_sets_direction": True,
            "textbook_anchor_sets_lesson_content_landing": True,
            "missing_textbook_anchor_action": "hold_lesson_generation_or_ask_teacher_to_confirm_textbook_position",
        },
        "relation_to_official_case_reference": {
            "official_cases_are_reference_only": True,
            "can_borrow_schema_or_prompt_patterns": True,
            "can_copy_case_text_directly": False,
            "can_be_treated_as_curriculum_standard": False,
            "case_conflict_action": "prefer_curriculum_standard_and_textbook_anchor_then_request_teacher_review",
        },
        "relation_to_teacher_confirmation": {
            "teacher_confirmation_required_before_candidate_cards": True,
            "teacher_can_select_degraded_single_lesson_draft": True,
            "degraded_mode_must_be_visible": True,
            "teacher_confirmation_is_final_classroom_judgement_within_standard_bounds": True,
        },
        "revised_chain": [
            "teacher_input",
            "curriculum_standard_control_layer",
            "textbook_anchor_check",
            "big_unit_context_gate",
            "lesson_position_judgement",
            "teacher_confirm_unit_position",
            "self_prep_review_cards",
            "preview_only",
        ],
        "r7_visual_review_paused": True,
        "next_stage": NEXT_STAGE,
        **boundary(),
        **profile(),
    }


def control_fixture() -> dict[str, Any]:
    return {
        "fixture_id": "curriculum_standard_control_fixture_1013I_R6C",
        "stage": STAGE_ID,
        "lesson_context": {
            "subject": "美术",
            "grade": "三年级",
            "semester": "上册",
            "lesson_title": "色彩的感觉",
            "active_space": "prep_room",
            "active_capability": "lesson_prep",
        },
        "curriculum_standard_control_layer": {
            "status": "missing_structured_standard_ref",
            "normal_self_prep_allowed": False,
            "candidate_questioning_allowed": True,
            "degraded_single_lesson_draft_allowed_after_teacher_choice": True,
            "standard_version_label": None,
            "standard_ref_ids": [],
            "core_literacy_tags": {
                "status": "candidate_tags_pending_structured_ref",
                "candidate_tags": ["审美感知", "艺术表现", "创意实践", "文化理解"],
                "official_quote": False,
            },
            "learning_task_direction": None,
            "assessment_requirement": None,
            "academic_quality_or_performance_evidence": None,
            "content_scope_boundary": None,
            "prohibited_overreach": None,
            "teacher_visible_message": "缺少结构化课标依据，不能直接进入完整单课备课。可以先补课标依据，或由教师选择临时单课草案模式。",
        },
        "textbook_anchor_check": {
            "required": True,
            "status": "pending_textbook_anchor",
            "teacher_visible_message": "请确认本课在教材和单元中的位置，再进入候选卡生成。",
        },
        "big_unit_context_gate": {
            "required": True,
            "status": "pending_big_unit_context",
            "inherits_required_fields_from": "big_unit_context_gate_contract_1013I_R6A",
        },
        "official_case_reference_policy": {
            "cases_are_reference_only": True,
            "may_show_as": "参考案例启发",
            "may_override_standard": False,
            "may_override_textbook_anchor": False,
            "direct_copy_allowed": False,
        },
        "teacher_action_options": [
            {
                "action": "补充课标依据",
                "effect": "continue_to_standard_mapping",
                "formal_apply_performed": False,
            },
            {
                "action": "确认教材与单元位置",
                "effect": "continue_to_textbook_anchor_check",
                "formal_apply_performed": False,
            },
            {
                "action": "临时单课草案",
                "effect": "degraded_single_lesson_draft_only",
                "formal_apply_performed": False,
            },
        ],
        **boundary(),
        **profile(),
    }


def priority_matrix() -> dict[str, Any]:
    rows = [
        {
            "rank": 1,
            "layer": "curriculum_standard_control_layer",
            "authority": "upstream_constraint",
            "may_override_lower_layers": True,
            "may_be_overridden_by_official_case": False,
            "role": "Sets learning direction, competency focus, assessment evidence, and scope boundaries.",
        },
        {
            "rank": 2,
            "layer": "textbook_anchor",
            "authority": "required_content_landing",
            "may_override_lower_layers": True,
            "may_override_curriculum_standard": False,
            "role": "Locates the specific lesson content, unit sequence, materials, and textbook position.",
        },
        {
            "rank": 3,
            "layer": "big_unit_context_gate_and_lesson_position",
            "authority": "unit_structure_control",
            "may_override_official_case_reference": True,
            "may_override_curriculum_standard": False,
            "role": "Judges what this lesson is supposed to do inside the larger unit.",
        },
        {
            "rank": 4,
            "layer": "teacher_confirmation_gate",
            "authority": "classroom_judgement_inside_required_bounds",
            "may_request_revision": True,
            "may_remove_required_standard_check": False,
            "role": "Confirms or revises mappings and chooses whether to continue, revise, or use degraded draft mode.",
        },
        {
            "rank": 5,
            "layer": "official_case_reference",
            "authority": "reference_only",
            "may_override_curriculum_standard": False,
            "may_override_textbook_anchor": False,
            "role": "Offers reusable design moves, field patterns, and wording inspiration only.",
        },
        {
            "rank": 6,
            "layer": "provider_or_model_candidate",
            "authority": "candidate_only_when_enabled_later",
            "may_override_any_control_layer": False,
            "role": "Later model output must become reviewable candidates, not direct lesson body.",
        },
    ]
    return {
        "matrix_id": "curriculum_standard_priority_matrix_1013I_R6C",
        "stage": STAGE_ID,
        "priority_rows": rows,
        "conflict_rules": [
            {
                "conflict": "official_case_reference_vs_curriculum_standard",
                "resolution": "use_curriculum_standard_control_layer_and_mark_case_as_reference_only",
            },
            {
                "conflict": "teacher_input_missing_standard_ref",
                "resolution": "ask_for_standard_ref_or_enter_visible_degraded_draft_mode",
            },
            {
                "conflict": "textbook_anchor_missing",
                "resolution": "hold_normal_lesson_generation_until_textbook_anchor_is_confirmed",
            },
            {
                "conflict": "candidate_activity_exceeds_grade_or_scope",
                "resolution": "reject_or_revise_candidate_before_teacher_review_cards",
            },
        ],
        "curriculum_standard_outranks_official_case_reference": True,
        "textbook_anchor_required_before_lesson_generation": True,
        "teacher_confirmation_required": True,
        "official_cases_reference_only": True,
        "r7_visual_review_paused": True,
        **boundary(),
        **profile(),
    }


def contract_markdown(contract: dict[str, Any], matrix: dict[str, Any]) -> str:
    fields = "\n".join(
        f"- `{item['field']}`: required={str(item['required']).lower()}, mode={item['mode']}"
        for item in contract["required_control_fields"]
    )
    rows = "\n".join(
        f"{row['rank']}. `{row['layer']}` - {row['authority']}: {row['role']}"
        for row in matrix["priority_rows"]
    )
    return f"""# 1013I_R6C Curriculum Standard Control Layer Contract

```text
STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Purpose

R6C defines `curriculum_standard_control_layer` as the upstream constraint layer for teacher self-prep, big-unit context judgement, lesson-position judgement, candidate-card generation, and later render surfaces.

This stage is contract-only. It does not parse real curriculum-standard full text, does not create official curriculum claims, does not generate a big-unit design, and does not generate a single-lesson plan.

## Control Fields

{fields}

## Priority

{rows}

## Chain

```text
teacher_input
-> curriculum_standard_control_layer
-> textbook_anchor_check
-> big_unit_context_gate
-> lesson_position_judgement
-> teacher_confirm_unit_position
-> self_prep_review_cards
-> preview_only
```

## Non-Negotiable Rules

- Curriculum standard is the upstream constraint layer.
- Textbook anchor is required before normal lesson generation.
- Official cases are reference-only and cannot override curriculum standards, textbook anchors, or teacher confirmation.
- Teacher confirmation remains required before candidate cards, but it cannot remove the required standard check.
- R7 visual review remains paused until the standard control, interpretation, textbook anchor, and big-unit design chain are filled.
"""


def scan_deprecated_visible_names(paths: list[Path]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name in DEPRECATED_VISIBLE_NAMES:
            if name in text:
                hits.append({"path": str(path), "name": name})
    return hits


def scan_secrets(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append(str(path))
                break
    return hits


def build_result(output_root: Path, stage_files: list[Path]) -> dict[str, Any]:
    latest_path = output_root / "LATEST_REVIEW_ENTRY.md"
    manifest_path = output_root / "REVIEW_PACKAGE_MANIFEST.md"
    r6b_r1_path = output_root / "1013I_R6B_R1_review_manifest_alignment" / "1013I_R6B_R1_result.json"
    r6b_path = output_root / "1013I_R6B_official_case_readonly_deconstruction" / "1013I_R6B_result.json"
    contract_path = output_root / STAGE_DIR_NAME / "curriculum_standard_control_layer_contract_1013I_R6C.json"
    fixture_path = output_root / STAGE_DIR_NAME / "curriculum_standard_control_fixture_1013I_R6C.json"
    matrix_path = output_root / STAGE_DIR_NAME / "curriculum_standard_priority_matrix_1013I_R6C.json"

    r6b_r1 = read_json(r6b_r1_path)
    r6b = read_json(r6b_path)
    contract = read_json(contract_path)
    fixture = read_json(fixture_path)
    matrix = read_json(matrix_path)
    latest_text = latest_path.read_text(encoding="utf-8")
    manifest_text = manifest_path.read_text(encoding="utf-8")

    required_fields = {item["field"] for item in contract.get("required_control_fields", [])}
    expected_fields = {
        "standard_version_label",
        "school_stage",
        "core_literacy_tags",
        "learning_task_direction",
        "assessment_requirement",
        "academic_quality_or_performance_evidence",
        "content_scope_boundary",
        "prohibited_overreach",
        "standard_ref_ids",
        "interpretation_status",
        "teacher_confirmation_status",
    }
    priority_layers = [row.get("layer") for row in matrix.get("priority_rows", [])]

    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "r6b_r1_result_present": r6b_r1_path.exists(),
        "r6b_r1_final_status": r6b_r1.get("final_status"),
        "r6b_r1_pass": r6b_r1.get("final_status") == R6B_R1_PASS_STATUS,
        "r6b_result_present": r6b_path.exists(),
        "r6b_final_status": r6b.get("final_status"),
        "r6b_pass": r6b.get("final_status") == R6B_PASS_STATUS,
        "latest_entry_points_to_r6c": f"REVIEW_STAGE={STAGE_ID}" in latest_text
        and f"FINAL_STATUS={FINAL_STATUS}" in latest_text,
        "latest_entry_next_stage_is_r6d": f"NEXT_RECOMMENDED_STAGE={NEXT_STAGE}" in latest_text,
        "manifest_includes_r6c": "1013I_R6C_CURRICULUM_STANDARD_CONTROL_LAYER_CONTRACT" in manifest_text
        and f"{STAGE_DIR_NAME}/" in manifest_text,
        "manifest_next_stage_is_r6d": NEXT_STAGE in manifest_text,
        "contract_created": contract_path.exists(),
        "fixture_created": fixture_path.exists(),
        "priority_matrix_created": matrix_path.exists(),
        "curriculum_standard_control_layer_defined": contract.get("layer_key") == "curriculum_standard_control_layer",
        "lesson_standard_map_object_kept": contract.get("object_name") == "lesson_standard_map",
        "full_text_not_stored_or_invented": "Do not store or invent full curriculum-standard text" in contract.get("object_policy", ""),
        "required_control_fields_present": expected_fields.issubset(required_fields),
        "curriculum_standard_outranks_official_case_reference": matrix.get("curriculum_standard_outranks_official_case_reference") is True,
        "textbook_anchor_required_before_lesson_generation": matrix.get("textbook_anchor_required_before_lesson_generation") is True,
        "teacher_confirmation_required": matrix.get("teacher_confirmation_required") is True,
        "official_cases_reference_only": matrix.get("official_cases_reference_only") is True,
        "official_cases_remain_reference_only": r6b.get("cases_treated_as_reference_only") is True,
        "cases_not_treated_as_curriculum_standard": r6b.get("cases_not_treated_as_curriculum_standard") is True,
        "r7_visual_review_paused": contract.get("r7_visual_review_paused") is True and matrix.get("r7_visual_review_paused") is True,
        "priority_order_complete": priority_layers[:6]
        == [
            "curriculum_standard_control_layer",
            "textbook_anchor",
            "big_unit_context_gate_and_lesson_position",
            "teacher_confirmation_gate",
            "official_case_reference",
            "provider_or_model_candidate",
        ],
        "fixture_marks_missing_structured_standard_ref": fixture["curriculum_standard_control_layer"]["status"]
        == "missing_structured_standard_ref",
        "normal_self_prep_blocked_without_standard_ref": fixture["curriculum_standard_control_layer"][
            "normal_self_prep_allowed"
        ]
        is False,
        "degraded_mode_labeled": fixture["curriculum_standard_control_layer"][
            "degraded_single_lesson_draft_allowed_after_teacher_choice"
        ]
        is True,
        "provider_model_call_allowed": False,
        "formal_apply_allowed": False,
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(stage_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **profile(),
        **boundary(),
    }

    required_true = [
        "r6b_r1_result_present",
        "r6b_r1_pass",
        "r6b_result_present",
        "r6b_pass",
        "latest_entry_points_to_r6c",
        "latest_entry_next_stage_is_r6d",
        "manifest_includes_r6c",
        "manifest_next_stage_is_r6d",
        "contract_created",
        "fixture_created",
        "priority_matrix_created",
        "curriculum_standard_control_layer_defined",
        "lesson_standard_map_object_kept",
        "full_text_not_stored_or_invented",
        "required_control_fields_present",
        "curriculum_standard_outranks_official_case_reference",
        "textbook_anchor_required_before_lesson_generation",
        "teacher_confirmation_required",
        "official_cases_reference_only",
        "official_cases_remain_reference_only",
        "cases_not_treated_as_curriculum_standard",
        "r7_visual_review_paused",
        "priority_order_complete",
        "fixture_marks_missing_structured_standard_ref",
        "normal_self_prep_blocked_without_standard_ref",
        "degraded_mode_labeled",
    ]
    required_false = [
        "provider_model_call_allowed",
        "formal_apply_allowed",
        "real_curriculum_standard_full_text_parsed",
        "official_curriculum_claim_created",
        "big_unit_generation_performed",
        "single_lesson_generation_performed",
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
    failures = [key for key in required_true if result.get(key) is not True]
    failures.extend([key for key in required_false if result.get(key) is not False])
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    if failures:
        result["final_status"] = "FAIL_1013I_R6C_CURRICULUM_STANDARD_CONTROL_LAYER_CONTRACT"
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013I_R6C Curriculum Standard Control Layer Report

```text
STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Result

```text
curriculum_standard_control_layer_defined={str(result["curriculum_standard_control_layer_defined"]).lower()}
lesson_standard_map_object_kept={str(result["lesson_standard_map_object_kept"]).lower()}
required_control_fields_present={str(result["required_control_fields_present"]).lower()}
curriculum_standard_outranks_official_case_reference={str(result["curriculum_standard_outranks_official_case_reference"]).lower()}
textbook_anchor_required_before_lesson_generation={str(result["textbook_anchor_required_before_lesson_generation"]).lower()}
teacher_confirmation_required={str(result["teacher_confirmation_required"]).lower()}
official_cases_reference_only={str(result["official_cases_reference_only"]).lower()}
r7_visual_review_paused={str(result["r7_visual_review_paused"]).lower()}
real_curriculum_standard_full_text_parsed=false
official_curriculum_claim_created=false
```

## Chain

```text
teacher_input
-> curriculum_standard_control_layer
-> textbook_anchor_check
-> big_unit_context_gate
-> lesson_position_judgement
-> teacher_confirm_unit_position
-> self_prep_review_cards
-> preview_only
```

## Boundary

R6C is contract-only and fixture-only. It does not parse real curriculum-standard full text, does not generate official curriculum claims, does not generate a big-unit design, does not generate a single-lesson plan, and does not write lesson body, HTML, database, memory, Feishu, export, or archive.
"""


def copy_source_delta(repo_root: Path) -> None:
    source = repo_root / "scripts" / Path(__file__).name
    target = (
        repo_root
        / "outputs"
        / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
        / "source_delta_1013I_R6C"
        / "scripts"
        / Path(__file__).name
    )
    if source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()

    root = args.root.resolve()
    output_root = resolve_output_root(root)
    stage_dir = output_root / STAGE_DIR_NAME

    contract = control_contract()
    fixture = control_fixture()
    matrix = priority_matrix()
    contract_md_path = stage_dir / "curriculum_standard_control_layer_contract_1013I_R6C.md"
    contract_json_path = stage_dir / "curriculum_standard_control_layer_contract_1013I_R6C.json"
    fixture_path = stage_dir / "curriculum_standard_control_fixture_1013I_R6C.json"
    matrix_path = stage_dir / "curriculum_standard_priority_matrix_1013I_R6C.json"
    result_path = stage_dir / "1013I_R6C_result.json"
    report_path = stage_dir / "1013I_R6C_report.md"

    write_json(contract_json_path, contract)
    write_json(fixture_path, fixture)
    write_json(matrix_path, matrix)
    write_text(contract_md_path, contract_markdown(contract, matrix))

    stage_files = [contract_md_path, contract_json_path, fixture_path, matrix_path, result_path, report_path]
    result = build_result(output_root, stage_files)
    write_json(result_path, result)
    write_text(report_path, build_report(result))

    local_repo_root = repo_root_from_script()
    if (local_repo_root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1").exists():
        copy_source_delta(local_repo_root)

    if result["final_status"] != FINAL_STATUS:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    print(f"{FINAL_STATUS}: {result_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
