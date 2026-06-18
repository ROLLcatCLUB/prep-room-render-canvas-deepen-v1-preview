from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6D_TEXTBOOK_ANCHOR_AND_BIG_UNIT_DESIGN_CHAIN_CONTRACT"
FINAL_STATUS = "PASS_1013I_R6D_TEXTBOOK_ANCHOR_AND_BIG_UNIT_DESIGN_CHAIN_CONTRACT"
INHERITS_FROM = "1013I_R6C_CURRICULUM_STANDARD_CONTROL_LAYER_CONTRACT"
R6C_PASS_STATUS = "PASS_1013I_R6C_CURRICULUM_STANDARD_CONTROL_LAYER_CONTRACT"
NEXT_STAGE = "1013I_R6E_OFFICIAL_UNIT_MATERIAL_READONLY_EXTRACTION_FIXTURE"
STAGE_DIR_NAME = "1013I_R6D_textbook_anchor_and_big_unit_design_chain_contract"
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
        "actual_textbook_parsing_performed": False,
        "actual_big_unit_material_parsing_performed": False,
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


def contract() -> dict[str, Any]:
    return {
        "contract_id": "textbook_anchor_and_big_unit_design_chain_contract_1013I_R6D",
        "stage": STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "textbook_anchor_object": "lesson_textbook_map",
        "big_unit_chain_object": "unit_package",
        "lesson_position_object": "lesson_position_judgement",
        "role": "connect_curriculum_standard_control_to_textbook_unit_and_lesson_position_before_candidate_generation",
        "textbook_anchor_required": True,
        "big_unit_design_chain_defined": True,
        "lesson_position_judgement_required": True,
        "teacher_confirm_unit_position_required": True,
        "single_lesson_generation_blocked_without_textbook_anchor": True,
        "single_lesson_generation_blocked_without_lesson_position": True,
        "degraded_draft_mode_allowed_after_teacher_choice": True,
        "degraded_draft_mode_must_be_visible": True,
        "textbook_anchor_required_fields": [
            "lesson_textbook_map_id",
            "textbook_version",
            "subject",
            "grade",
            "semester",
            "unit_id",
            "unit_title",
            "lesson_id",
            "lesson_code",
            "lesson_title",
            "lesson_count",
            "textbook_catalog_ref",
            "textbook_page_or_activity_ref",
            "material_or_image_anchor",
            "textbook_activity_hint",
            "source_material_refs",
            "anchor_status",
            "teacher_confirmation_status",
        ],
        "big_unit_design_chain_required_fields": [
            "unit_package_id",
            "unit_title",
            "unit_big_idea",
            "unit_essential_question",
            "unit_learning_goals",
            "unit_performance_task",
            "unit_task_chain",
            "unit_assessment_focus",
            "unit_learning_evidence_chain",
            "lesson_sequence",
            "source_material_refs",
            "chain_status",
            "teacher_confirmation_status",
        ],
        "lesson_position_required_fields": [
            "lesson_id",
            "lesson_title",
            "lesson_position_in_unit",
            "current_lesson_role",
            "prior_lesson_connection",
            "next_lesson_connection",
            "current_lesson_unit_task",
            "current_lesson_evidence",
            "allowed_candidate_scope",
            "blocked_candidate_scope",
            "teacher_confirmation_status",
        ],
        "anchor_status_enum": [
            "missing_textbook_anchor",
            "candidate_anchor_from_teacher_input",
            "candidate_anchor_from_official_material",
            "teacher_confirmed_textbook_anchor",
        ],
        "chain_status_enum": [
            "missing_big_unit_chain",
            "candidate_chain_from_official_material",
            "candidate_chain_from_teacher_input",
            "teacher_confirmed_big_unit_chain",
        ],
        "lesson_position_status_enum": [
            "missing_lesson_position",
            "candidate_position_pending_teacher_review",
            "teacher_confirmed_lesson_position",
            "degraded_single_lesson_draft_only",
        ],
        "current_lesson_role_enum": [
            "unit_entry",
            "concept_building",
            "method_learning",
            "skill_practice",
            "creative_production",
            "critique_and_revision",
            "exhibition_or_reflection",
            "transfer_extension",
            "unknown_pending_teacher_confirm",
        ],
        "normal_generation_gate": {
            "requires_curriculum_standard_control_layer": True,
            "requires_textbook_anchor": True,
            "requires_big_unit_design_chain": True,
            "requires_lesson_position_judgement": True,
            "requires_teacher_confirm_unit_position": True,
            "allows_candidate_cards_after_all_required_gates": True,
            "allows_formal_apply": False,
        },
        "relation_to_curriculum_standard_control_layer": {
            "curriculum_standard_sets_direction": True,
            "textbook_anchor_sets_content_landing": True,
            "big_unit_chain_sets_sequence_and_task_role": True,
            "lesson_position_sets_current_lesson_job": True,
        },
        "relation_to_official_case_reference": {
            "official_cases_reference_only": True,
            "official_cases_may_inform_field_shape": True,
            "official_cases_may_not_replace_textbook_anchor": True,
            "official_cases_may_not_replace_big_unit_chain": True,
            "official_cases_may_not_replace_teacher_confirmation": True,
        },
        "revised_chain": [
            "teacher_input",
            "curriculum_standard_control_layer",
            "textbook_anchor_check",
            "big_unit_design_chain_check",
            "lesson_position_judgement",
            "teacher_confirm_unit_position",
            "self_prep_review_cards",
            "preview_only",
        ],
        "r7_visual_review_paused": True,
        **profile(),
        **boundary(),
    }


def textbook_anchor_fixture() -> dict[str, Any]:
    return {
        "fixture_id": "textbook_anchor_fixture_1013I_R6D",
        "stage": STAGE_ID,
        "lesson_textbook_map": {
            "lesson_textbook_map_id": "lesson_textbook_map_1013I_R6D_color_feeling_pending",
            "subject": "美术",
            "grade": "三年级",
            "semester": "上册",
            "unit_id": "unit_color_pending",
            "unit_title": "多变的色彩",
            "lesson_id": "lesson_color_feeling_pending",
            "lesson_code": "1-2",
            "lesson_title": "色彩的感觉",
            "lesson_count": 1,
            "textbook_version": None,
            "textbook_catalog_ref": "pending_textbook_catalog_ref",
            "textbook_page_or_activity_ref": None,
            "material_or_image_anchor": None,
            "textbook_activity_hint": "pending_teacher_or_official_material_confirm",
            "source_material_refs": [],
            "anchor_status": "missing_textbook_anchor",
            "teacher_confirmation_status": "pending_teacher_confirm",
        },
        "normal_single_lesson_generation_allowed": False,
        "degraded_single_lesson_draft_allowed_after_teacher_choice": True,
        "teacher_visible_message": "缺少教材锚点，不能直接进入完整单课备课候选。请先确认教材版本、单元、课题和教材活动落点。",
        **profile(),
        **boundary(),
    }


def big_unit_chain_fixture() -> dict[str, Any]:
    return {
        "fixture_id": "big_unit_design_chain_fixture_1013I_R6D",
        "stage": STAGE_ID,
        "unit_package": {
            "unit_package_id": "unit_package_1013I_R6D_color_pending",
            "unit_title": "多变的色彩",
            "unit_big_idea": None,
            "unit_essential_question": None,
            "unit_learning_goals": [],
            "unit_performance_task": None,
            "unit_task_chain": [],
            "unit_assessment_focus": [],
            "unit_learning_evidence_chain": [],
            "lesson_sequence": [
                {"lesson_code": "1-1", "lesson_title": "渐变的魅力", "role": "unknown_pending_teacher_confirm"},
                {"lesson_code": "1-2", "lesson_title": "色彩的感觉", "role": "unknown_pending_teacher_confirm"},
                {"lesson_code": "1-3", "lesson_title": "渐变的节奏", "role": "unknown_pending_teacher_confirm"},
            ],
            "source_material_refs": [],
            "chain_status": "missing_big_unit_chain",
            "teacher_confirmation_status": "pending_teacher_confirm",
        },
        "big_unit_design_chain_defined": True,
        "big_unit_generation_performed": False,
        "teacher_visible_message": "当前只定义大单元链对象和缺失状态，不生成大单元设计正文。后续需要读取官方单元资料或教师输入后再形成候选链。",
        **profile(),
        **boundary(),
    }


def lesson_position_fixture() -> dict[str, Any]:
    return {
        "fixture_id": "lesson_position_judgement_fixture_1013I_R6D",
        "stage": STAGE_ID,
        "lesson_position_judgement": {
            "lesson_id": "lesson_color_feeling_pending",
            "lesson_title": "色彩的感觉",
            "lesson_position_in_unit": "pending_teacher_confirm",
            "current_lesson_role": "unknown_pending_teacher_confirm",
            "prior_lesson_connection": "pending_big_unit_chain",
            "next_lesson_connection": "pending_big_unit_chain",
            "current_lesson_unit_task": None,
            "current_lesson_evidence": [],
            "allowed_candidate_scope": [
                "ask_for_textbook_anchor",
                "ask_for_big_unit_position",
                "build_preview_only_question_cards",
            ],
            "blocked_candidate_scope": [
                "generate_full_lesson_plan",
                "generate_big_unit_design_body",
                "formal_apply_to_lesson_body",
                "treat_official_case_as_textbook_anchor",
            ],
            "position_status": "missing_lesson_position",
            "teacher_confirmation_status": "pending_teacher_confirm",
        },
        "teacher_confirm_unit_position_required": True,
        "candidate_cards_blocked_until_confirmation": True,
        "single_lesson_generation_performed": False,
        **profile(),
        **boundary(),
    }


def contract_markdown(data: dict[str, Any]) -> str:
    chain = "\n".join(f"-> {item}" if index else item for index, item in enumerate(data["revised_chain"]))
    anchor_fields = "\n".join(f"- `{item}`" for item in data["textbook_anchor_required_fields"])
    unit_fields = "\n".join(f"- `{item}`" for item in data["big_unit_design_chain_required_fields"])
    position_fields = "\n".join(f"- `{item}`" for item in data["lesson_position_required_fields"])
    return f"""# 1013I_R6D Textbook Anchor And Big Unit Design Chain Contract

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

R6D defines the contract relationship between `lesson_textbook_map`, `unit_package`, and `lesson_position_judgement`.

It connects R6C's curriculum-standard control layer to the concrete textbook anchor, the larger unit design chain, and the current lesson's role in that chain. It is contract-only and fixture-only: no big-unit body is generated and no single-lesson plan is generated.

## Required Textbook Anchor Fields

{anchor_fields}

## Required Big Unit Chain Fields

{unit_fields}

## Required Lesson Position Fields

{position_fields}

## Generation Gate

```text
textbook_anchor_required=true
big_unit_design_chain_defined=true
lesson_position_judgement_required=true
teacher_confirm_unit_position_required=true
single_lesson_generation_blocked_without_textbook_anchor=true
single_lesson_generation_blocked_without_lesson_position=true
```

## Chain

```text
{chain}
```

## Non-Negotiable Rules

- `lesson_textbook_map` is the textbook semantic anchor, not an image path list.
- `unit_package` is the big-unit middle object, not the generated unit-design body.
- The current lesson must have a lesson-position judgement before normal candidate-card generation.
- Teacher confirmation is required before this lesson position can feed candidate cards.
- Missing textbook anchor or missing lesson position can only enter visible degraded draft mode.
- Official cases remain reference-only and cannot replace textbook anchors, unit chains, or teacher confirmation.
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
    stage_dir = output_root / STAGE_DIR_NAME
    r6c_path = output_root / "1013I_R6C_curriculum_standard_control_layer_contract" / "1013I_R6C_result.json"
    latest_path = output_root / "LATEST_REVIEW_ENTRY.md"
    manifest_path = output_root / "REVIEW_PACKAGE_MANIFEST.md"
    r6c = read_json(r6c_path)
    latest_text = latest_path.read_text(encoding="utf-8")
    manifest_text = manifest_path.read_text(encoding="utf-8")
    contract_data = read_json(stage_dir / "textbook_anchor_and_big_unit_design_chain_contract_1013I_R6D.json")
    textbook_fixture = read_json(stage_dir / "textbook_anchor_fixture_1013I_R6D.json")
    unit_fixture = read_json(stage_dir / "big_unit_design_chain_fixture_1013I_R6D.json")
    position_fixture = read_json(stage_dir / "lesson_position_judgement_fixture_1013I_R6D.json")

    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "r6c_result_present": r6c_path.exists(),
        "r6c_final_status": r6c.get("final_status"),
        "r6c_pass": r6c.get("final_status") == R6C_PASS_STATUS,
        "latest_entry_points_to_r6d": f"REVIEW_STAGE={STAGE_ID}" in latest_text and f"FINAL_STATUS={FINAL_STATUS}" in latest_text,
        "latest_entry_next_stage_is_r6e": f"NEXT_RECOMMENDED_STAGE={NEXT_STAGE}" in latest_text,
        "manifest_includes_r6d": STAGE_ID in manifest_text and f"{STAGE_DIR_NAME}/" in manifest_text,
        "manifest_next_stage_is_r6e": NEXT_STAGE in manifest_text,
        "contract_created": (stage_dir / "textbook_anchor_and_big_unit_design_chain_contract_1013I_R6D.json").exists(),
        "textbook_anchor_fixture_created": (stage_dir / "textbook_anchor_fixture_1013I_R6D.json").exists(),
        "big_unit_design_chain_fixture_created": (stage_dir / "big_unit_design_chain_fixture_1013I_R6D.json").exists(),
        "lesson_position_judgement_fixture_created": (stage_dir / "lesson_position_judgement_fixture_1013I_R6D.json").exists(),
        "textbook_anchor_required": contract_data.get("textbook_anchor_required") is True,
        "lesson_textbook_map_object_kept": contract_data.get("textbook_anchor_object") == "lesson_textbook_map",
        "unit_package_object_kept": contract_data.get("big_unit_chain_object") == "unit_package",
        "big_unit_design_chain_defined": contract_data.get("big_unit_design_chain_defined") is True,
        "lesson_position_judgement_required": contract_data.get("lesson_position_judgement_required") is True,
        "teacher_confirm_unit_position_required": contract_data.get("teacher_confirm_unit_position_required") is True,
        "single_lesson_generation_blocked_without_textbook_anchor": contract_data.get("single_lesson_generation_blocked_without_textbook_anchor") is True,
        "single_lesson_generation_blocked_without_lesson_position": contract_data.get("single_lesson_generation_blocked_without_lesson_position") is True,
        "degraded_mode_labeled": contract_data.get("degraded_draft_mode_must_be_visible") is True,
        "official_cases_remain_reference_only": contract_data["relation_to_official_case_reference"]["official_cases_reference_only"] is True,
        "textbook_fixture_marks_missing_anchor": textbook_fixture["lesson_textbook_map"]["anchor_status"] == "missing_textbook_anchor",
        "normal_generation_blocked_in_textbook_fixture": textbook_fixture.get("normal_single_lesson_generation_allowed") is False,
        "unit_fixture_does_not_generate_big_unit_body": unit_fixture.get("big_unit_generation_performed") is False,
        "position_fixture_blocks_candidate_cards": position_fixture.get("candidate_cards_blocked_until_confirmation") is True,
        "r7_visual_review_paused": contract_data.get("r7_visual_review_paused") is True,
        "provider_model_call_allowed": False,
        "formal_apply_allowed": False,
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(stage_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **profile(),
        **boundary(),
    }
    required_true = [
        "r6c_result_present",
        "r6c_pass",
        "latest_entry_points_to_r6d",
        "latest_entry_next_stage_is_r6e",
        "manifest_includes_r6d",
        "manifest_next_stage_is_r6e",
        "contract_created",
        "textbook_anchor_fixture_created",
        "big_unit_design_chain_fixture_created",
        "lesson_position_judgement_fixture_created",
        "textbook_anchor_required",
        "lesson_textbook_map_object_kept",
        "unit_package_object_kept",
        "big_unit_design_chain_defined",
        "lesson_position_judgement_required",
        "teacher_confirm_unit_position_required",
        "single_lesson_generation_blocked_without_textbook_anchor",
        "single_lesson_generation_blocked_without_lesson_position",
        "degraded_mode_labeled",
        "official_cases_remain_reference_only",
        "textbook_fixture_marks_missing_anchor",
        "normal_generation_blocked_in_textbook_fixture",
        "unit_fixture_does_not_generate_big_unit_body",
        "position_fixture_blocks_candidate_cards",
        "r7_visual_review_paused",
    ]
    required_false = [
        "provider_model_call_allowed",
        "formal_apply_allowed",
        "actual_textbook_parsing_performed",
        "actual_big_unit_material_parsing_performed",
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
        result["final_status"] = "FAIL_1013I_R6D_TEXTBOOK_ANCHOR_AND_BIG_UNIT_DESIGN_CHAIN_CONTRACT"
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013I_R6D Textbook Anchor And Big Unit Design Chain Report

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
textbook_anchor_required={str(result["textbook_anchor_required"]).lower()}
lesson_textbook_map_object_kept={str(result["lesson_textbook_map_object_kept"]).lower()}
unit_package_object_kept={str(result["unit_package_object_kept"]).lower()}
big_unit_design_chain_defined={str(result["big_unit_design_chain_defined"]).lower()}
lesson_position_judgement_required={str(result["lesson_position_judgement_required"]).lower()}
teacher_confirm_unit_position_required={str(result["teacher_confirm_unit_position_required"]).lower()}
single_lesson_generation_blocked_without_textbook_anchor={str(result["single_lesson_generation_blocked_without_textbook_anchor"]).lower()}
single_lesson_generation_blocked_without_lesson_position={str(result["single_lesson_generation_blocked_without_lesson_position"]).lower()}
official_cases_remain_reference_only={str(result["official_cases_remain_reference_only"]).lower()}
r7_visual_review_paused={str(result["r7_visual_review_paused"]).lower()}
```

## Chain

```text
teacher_input
-> curriculum_standard_control_layer
-> textbook_anchor_check
-> big_unit_design_chain_check
-> lesson_position_judgement
-> teacher_confirm_unit_position
-> self_prep_review_cards
-> preview_only
```

## Boundary

R6D is contract-only and fixture-only. It does not parse real textbook materials, does not parse real big-unit materials, does not generate a big-unit body, does not generate a single-lesson plan, and does not write lesson body, HTML, database, memory, Feishu, export, or archive.
"""


def copy_source_delta(repo_root: Path) -> None:
    source = repo_root / "scripts" / Path(__file__).name
    target = (
        repo_root
        / "outputs"
        / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
        / "source_delta_1013I_R6D"
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

    contract_data = contract()
    write_json(stage_dir / "textbook_anchor_and_big_unit_design_chain_contract_1013I_R6D.json", contract_data)
    write_text(stage_dir / "textbook_anchor_and_big_unit_design_chain_contract_1013I_R6D.md", contract_markdown(contract_data))
    write_json(stage_dir / "textbook_anchor_fixture_1013I_R6D.json", textbook_anchor_fixture())
    write_json(stage_dir / "big_unit_design_chain_fixture_1013I_R6D.json", big_unit_chain_fixture())
    write_json(stage_dir / "lesson_position_judgement_fixture_1013I_R6D.json", lesson_position_fixture())

    result_path = stage_dir / "1013I_R6D_result.json"
    report_path = stage_dir / "1013I_R6D_report.md"
    stage_files = [
        stage_dir / "textbook_anchor_and_big_unit_design_chain_contract_1013I_R6D.md",
        stage_dir / "textbook_anchor_and_big_unit_design_chain_contract_1013I_R6D.json",
        stage_dir / "textbook_anchor_fixture_1013I_R6D.json",
        stage_dir / "big_unit_design_chain_fixture_1013I_R6D.json",
        stage_dir / "lesson_position_judgement_fixture_1013I_R6D.json",
        result_path,
        report_path,
    ]
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
