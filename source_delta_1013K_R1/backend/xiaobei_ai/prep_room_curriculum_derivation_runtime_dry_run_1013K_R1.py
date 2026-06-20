from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R1_CURRICULUM_DERIVATION_PROFILE_RUNTIME_DRY_RUN"


def _repo_root_from_module() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _source_path(root: Path, relative_path: str) -> Path:
    direct = root / relative_path
    if direct.exists():
        return direct
    review_prefix = "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
    if relative_path.startswith(review_prefix):
        review_root_path = root / relative_path.removeprefix(review_prefix)
        if review_root_path.exists():
            return review_root_path
    return direct


def _load_sources(root: Path) -> dict[str, Any]:
    sources = {
        "r0_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R0_curriculum_standard_derivation_backend_contract/1013K_R0_result.json",
        ),
        "r0_slice_schema": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R0_curriculum_standard_derivation_backend_contract/"
            "curriculum_standard_slice_schema_1013K_R0.json",
        ),
        "r0_profile_schema": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R0_curriculum_standard_derivation_backend_contract/"
            "curriculum_control_profile_schema_1013K_R0.json",
        ),
        "r0_derivation_contract": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R0_curriculum_standard_derivation_backend_contract/"
            "curriculum_to_big_unit_derivation_contract_1013K_R0.json",
        ),
        "r0_trace_fixture": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R0_curriculum_standard_derivation_backend_contract/"
            "curriculum_derivation_trace_fixture_1013K_R0.json",
        ),
        "r6e_textbook_anchor_candidates": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013I_R6E_official_unit_material_readonly_extraction_fixture/"
            "textbook_anchor_candidates_1013I_R6E.json",
        ),
        "r6e_big_unit_chain_candidates": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013I_R6E_official_unit_material_readonly_extraction_fixture/"
            "big_unit_chain_candidates_1013I_R6E.json",
        ),
        "r6e_teacher_confirmation_items": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013I_R6E_official_unit_material_readonly_extraction_fixture/"
            "teacher_confirmation_required_items_1013I_R6E.json",
        ),
    }
    missing = [str(path) for path in sources.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing curriculum runtime dry-run sources: {missing}")
    return {key: _read_json(path) for key, path in sources.items()}


def boundary_flags() -> dict[str, bool]:
    return {
        "runtime_dry_run_only": True,
        "in_memory_only": True,
        "readonly_sources_only": True,
        "preview_only": True,
        "side_effects_performed": False,
        "runtime_schema_applied": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "unit_package_written": False,
        "textbook_anchor_verified": False,
        "official_curriculum_claim_created": False,
        "full_standard_text_stored": False,
        "full_standard_text_dumped_to_prompt": False,
        "big_unit_body_generated": False,
        "single_lesson_body_generated": False,
        "main_project_pushed": False,
    }


def profile() -> dict[str, Any]:
    return {
        "agent_role": "unified_teacher_agent",
        "assistant_profile": {
            "display_name": "小教",
            "display_name_customizable": True,
            "wake_name": "小教",
            "voice_profile_id": None,
            "tts_enabled": False,
        },
        "active_space": "prep_room",
        "active_capability": "lesson_prep",
    }


def build_dry_run_request(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    teacher_request = sources["r0_trace_fixture"]["teacher_request"]
    return {
        "request_id": "curriculum_derivation_runtime_dry_run_request_1013K_R1",
        "stage": STAGE_ID,
        "source_trace_id": sources["r0_trace_fixture"]["trace_id"],
        "teacher_request": teacher_request,
        "requested_mode": "backend_runtime_dry_run",
        "dry_run_policy": {
            "read_sources": True,
            "compose_in_memory_state": True,
            "evaluate_gates": True,
            "write_database": False,
            "write_memory": False,
            "call_provider_or_model": False,
            "formal_apply": False,
        },
        "source_refs": [
            "1013K_R0_result.json",
            "curriculum_standard_slice_schema_1013K_R0.json",
            "curriculum_control_profile_schema_1013K_R0.json",
            "curriculum_to_big_unit_derivation_contract_1013K_R0.json",
            "curriculum_derivation_trace_fixture_1013K_R0.json",
            "textbook_anchor_candidates_1013I_R6E.json",
            "big_unit_chain_candidates_1013I_R6E.json",
            "teacher_confirmation_required_items_1013I_R6E.json",
        ],
        **boundary_flags(),
        **profile(),
    }


def _selected_slice(sources: dict[str, Any]) -> dict[str, Any]:
    examples = sources["r0_slice_schema"].get("slice_examples", [])
    if not examples:
        raise ValueError("R0 slice schema has no slice_examples.")
    return examples[0]


def build_runtime_state(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    selected = _selected_slice(sources)
    textbook_candidates = sources["r6e_textbook_anchor_candidates"].get("candidates", [])
    big_unit_candidate = sources["r6e_big_unit_chain_candidates"].get("unit_package_candidate", {})
    teacher_confirmation_items = sources["r6e_teacher_confirmation_items"].get("items", [])
    control_profile = {
        "profile_id": "curriculum_control_profile_color_feeling_1013K_R1",
        "source_profile_id": sources["r0_trace_fixture"]["control_profile_candidate"]["profile_id"],
        "subject": selected["subject"],
        "school_stage": selected["school_stage"],
        "grade_band": selected["grade_band"],
        "learning_domain": selected["learning_domain"],
        "core_literacy_focus": selected["core_literacy_tags"],
        "learning_task_direction": selected["learning_task_direction"],
        "assessment_evidence_direction": selected["assessment_evidence_direction"],
        "allowed_generation_scope": sources["r0_trace_fixture"]["control_profile_candidate"][
            "allowed_generation_scope"
        ],
        "blocked_generation_scope": sources["r0_trace_fixture"]["control_profile_candidate"][
            "blocked_generation_scope"
        ],
        "teacher_confirmation_required_items": [
            {
                "item_id": item.get("item_id"),
                "label": item.get("label"),
                "blocks_normal_generation": item.get("blocks_normal_generation") is True,
            }
            for item in teacher_confirmation_items
        ],
        "degraded_preview_policy": "allowed_only_with_visible_degraded_label",
        "source_refs": [
            "curriculum_standard_slice_schema_1013K_R0.slice_examples[0]",
            "textbook_anchor_candidates_1013I_R6E",
            "big_unit_chain_candidates_1013I_R6E",
        ],
        "status": "profile_built_in_memory_dry_run",
    }
    return {
        "state_id": "curriculum_derivation_runtime_state_1013K_R1",
        "stage": STAGE_ID,
        "request_id": "curriculum_derivation_runtime_dry_run_request_1013K_R1",
        "runtime_state_kind": "in_memory_dry_run_state",
        "selected_curriculum_standard_slice": selected,
        "curriculum_control_profile": control_profile,
        "textbook_anchor_gate_input": {
            "candidate_count": len(textbook_candidates),
            "candidate_statuses": [
                candidate.get("candidate_anchor", {}).get("teacher_confirmation_status")
                for candidate in textbook_candidates
            ],
            "verified_textbook_anchor_created": sources["r6e_textbook_anchor_candidates"].get(
                "verified_textbook_anchor_created"
            )
            is True,
        },
        "big_unit_chain_gate_input": {
            "candidate_chain_status": big_unit_candidate.get("chain_status"),
            "teacher_confirmation_status": big_unit_candidate.get("teacher_confirmation_status"),
            "unit_package_created": sources["r6e_big_unit_chain_candidates"].get("unit_package_created") is True,
        },
        "side_effect_assertion": {
            "state_persisted": False,
            "unit_package_written": False,
            "lesson_body_written": False,
            "provider_called": False,
            "model_called": False,
        },
        **boundary_flags(),
        **profile(),
    }


def build_gate_decision(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    state = build_runtime_state(root)
    textbook_ready = (
        state["textbook_anchor_gate_input"]["candidate_count"] > 0
        and state["textbook_anchor_gate_input"]["verified_textbook_anchor_created"] is True
    )
    big_unit_ready = state["big_unit_chain_gate_input"]["unit_package_created"] is True
    teacher_confirmation_ready = all(
        item["blocks_normal_generation"] is False
        for item in state["curriculum_control_profile"]["teacher_confirmation_required_items"]
    )
    curriculum_profile_ready = bool(state["curriculum_control_profile"].get("profile_id"))
    normal_generation_allowed = (
        curriculum_profile_ready and textbook_ready and big_unit_ready and teacher_confirmation_ready
    )
    return {
        "decision_id": "curriculum_derivation_gate_decision_1013K_R1",
        "stage": STAGE_ID,
        "source_state_id": state["state_id"],
        "gates": [
            {
                "gate_id": "curriculum_control_profile_gate",
                "pass": curriculum_profile_ready,
                "reason": "Control profile was built in memory from structured R0 slice and trace.",
                "blocks_normal_generation": False,
            },
            {
                "gate_id": "textbook_anchor_gate",
                "pass": textbook_ready,
                "reason": "Textbook anchor remains candidate-only and not teacher-confirmed.",
                "blocks_normal_generation": True,
            },
            {
                "gate_id": "big_unit_chain_gate",
                "pass": big_unit_ready,
                "reason": "Big-unit chain remains candidate-only and no unit_package is written.",
                "blocks_normal_generation": True,
            },
            {
                "gate_id": "teacher_confirmation_gate",
                "pass": teacher_confirmation_ready,
                "reason": "Teacher confirmation items from R6E are still pending.",
                "blocks_normal_generation": True,
            },
        ],
        "normal_candidate_generation_allowed": normal_generation_allowed,
        "degraded_preview_allowed": True,
        "degraded_preview_label_required": True,
        "next_safe_action": "build_preview_candidate_envelope_after_teacher_review_or_degraded_choice",
        **boundary_flags(),
        **profile(),
    }


def build_derivation_target_map(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    contract = sources["r0_derivation_contract"]
    gate_decision = build_gate_decision(root)
    targets = []
    for target in contract["derivation_targets"]:
        targets.append(
            {
                "target_key": target,
                "target_status": "ready_as_preview_candidate_target",
                "source_control": "curriculum_control_profile_color_feeling_1013K_R1",
                "requires_teacher_review_before_generation": True,
                "normal_generation_allowed_now": gate_decision["normal_candidate_generation_allowed"],
                "writes_unit_package": False,
                "writes_lesson_body": False,
            }
        )
    return {
        "target_map_id": "curriculum_derivation_target_map_1013K_R1",
        "stage": STAGE_ID,
        "source_decision_id": gate_decision["decision_id"],
        "target_count": len(targets),
        "targets": targets,
        "blocked_targets_before_confirmation": contract["blocked_targets_before_confirmation"],
        **boundary_flags(),
        **profile(),
    }


def build_runtime_trace(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    request = build_dry_run_request(root)
    state = build_runtime_state(root)
    decision = build_gate_decision(root)
    target_map = build_derivation_target_map(root)
    events = [
        {
            "event_id": "r1_event_01_request_loaded",
            "event_type": "readonly_request_intake",
            "output_ref": request["request_id"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r1_event_02_state_built",
            "event_type": "in_memory_state_build",
            "output_ref": state["state_id"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r1_event_03_gates_evaluated",
            "event_type": "gate_decision",
            "output_ref": decision["decision_id"],
            "normal_candidate_generation_allowed": decision["normal_candidate_generation_allowed"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r1_event_04_targets_mapped",
            "event_type": "target_map",
            "output_ref": target_map["target_map_id"],
            "target_count": target_map["target_count"],
            "side_effects_performed": False,
        },
    ]
    return {
        "trace_id": "curriculum_derivation_runtime_trace_1013K_R1",
        "stage": STAGE_ID,
        "events": events,
        "side_effects_performed": any(event["side_effects_performed"] for event in events),
        "normal_candidate_generation_allowed": decision["normal_candidate_generation_allowed"],
        "degraded_preview_allowed": decision["degraded_preview_allowed"],
        "runtime_state_written": False,
        **boundary_flags(),
        **profile(),
    }


def build_curriculum_derivation_profile_runtime_dry_run(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "dry_run_request": build_dry_run_request(root),
        "runtime_state": build_runtime_state(root),
        "gate_decision": build_gate_decision(root),
        "derivation_target_map": build_derivation_target_map(root),
        "runtime_trace": build_runtime_trace(root),
        "boundary": boundary_flags(),
    }
