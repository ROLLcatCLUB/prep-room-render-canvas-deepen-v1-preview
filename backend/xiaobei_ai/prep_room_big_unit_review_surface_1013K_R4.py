from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R4_STATIC_SECTION_PREVIEW_TO_REVIEW_SURFACE_FIXTURE"


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
        "r3_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R3_big_unit_candidate_envelope_to_static_section_preview/1013K_R3_result.json",
        ),
        "r3_preview_bundle": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R3_big_unit_candidate_envelope_to_static_section_preview/"
            "big_unit_static_section_preview_bundle_1013K_R3.json",
        ),
        "r3_review_actions": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R3_big_unit_candidate_envelope_to_static_section_preview/"
            "big_unit_static_preview_review_actions_1013K_R3.json",
        ),
        "r1_gate_decision": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R1_curriculum_derivation_profile_runtime_dry_run/"
            "curriculum_derivation_gate_decision_1013K_R1.json",
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
        raise FileNotFoundError(f"Missing review surface sources: {missing}")
    return {key: _read_json(path) for key, path in sources.items()}


def boundary_flags() -> dict[str, bool]:
    return {
        "review_surface_fixture_only": True,
        "preview_only": True,
        "teacher_review_required": True,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "unit_package_written": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "runtime_schema_applied": False,
        "official_curriculum_claim_created": False,
        "main_project_pushed": False,
        "github_upload_deferred_until_milestone": True,
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


def _actions_by_section(actions_payload: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {
        item["section_preview_id"]: item.get("actions", [])
        for item in actions_payload.get("actions", [])
    }


def build_review_surface_fixture(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    preview_bundle = sources["r3_preview_bundle"]
    actions_by_section = _actions_by_section(sources["r3_review_actions"])
    gate_decision = sources["r1_gate_decision"]
    review_sections = []
    for section in preview_bundle.get("sections", []):
        review_sections.append(
            {
                "review_section_id": section["section_preview_id"].replace("static_section_preview", "review_section"),
                "source_section_preview_id": section["section_preview_id"],
                "order": section["order"],
                "teacher_label": section["teacher_label"],
                "status_badges": ["临时预览", "待教师确认"],
                "main_reading_content": {
                    "summary": section["summary"],
                    "paragraphs": section["body_paragraphs"],
                },
                "side_note": {
                    "risk_note": section["risk_note"],
                    "source_context": section["source_context"],
                    "default_collapsed": True,
                },
                "teacher_actions": actions_by_section.get(section["section_preview_id"], []),
                "review_state": "pending_teacher_review",
                "accepted_to_preview": False,
                "formal_apply_performed": False,
                "writes_unit_package": False,
                "writes_lesson_body": False,
            }
        )
    return {
        "review_surface_id": "big_unit_static_section_review_surface_1013K_R4",
        "stage": STAGE_ID,
        "source_preview_bundle_id": preview_bundle["bundle_id"],
        "surface_role": "teacher_reviews_static_big_unit_preview_sections_before_any_apply",
        "unit_title": "第一单元《多变的色彩》",
        "surface_status": "preview_review_only",
        "section_count": len(review_sections),
        "sections": review_sections,
        "top_notice": {
            "text": "这些内容是大单元预览，教师确认前不写入正式备课本。",
            "display_weight": "light",
        },
        "blocking_gate_summary": {
            "normal_candidate_generation_allowed": gate_decision["normal_candidate_generation_allowed"],
            "blocked_by": [
                gate["gate_id"]
                for gate in gate_decision.get("gates", [])
                if gate.get("blocks_normal_generation") and not gate.get("pass")
            ],
            "degraded_preview_allowed": gate_decision["degraded_preview_allowed"],
        },
        **boundary_flags(),
        **profile(),
    }


def build_review_state(root: Path | None = None) -> dict[str, Any]:
    surface = build_review_surface_fixture(root)
    return {
        "review_state_id": "big_unit_static_section_review_state_1013K_R4",
        "stage": STAGE_ID,
        "source_review_surface_id": surface["review_surface_id"],
        "section_states": [
            {
                "review_section_id": section["review_section_id"],
                "state": "pending_teacher_review",
                "can_accept_to_preview": True,
                "can_revise": True,
                "can_reject": True,
                "can_formal_apply": False,
                "accepted_to_preview": False,
                "formal_apply_performed": False,
            }
            for section in surface["sections"]
        ],
        "all_sections_pending_teacher_review": True,
        "any_formal_apply_allowed": False,
        **boundary_flags(),
        **profile(),
    }


def build_teacher_review_checklist(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    confirmation_items = sources["r6e_teacher_confirmation_items"].get("items", [])
    return {
        "checklist_id": "big_unit_static_section_teacher_review_checklist_1013K_R4",
        "stage": STAGE_ID,
        "teacher_confirmation_required": True,
        "items": [
            {
                "item_id": item.get("item_id"),
                "teacher_label": item.get("label"),
                "why_it_matters": item.get("why_required"),
                "blocks_normal_generation": item.get("blocks_normal_generation") is True,
                "status": "pending_teacher_confirm",
            }
            for item in confirmation_items
        ],
        "review_before_next_generation": [
            "课标依据是否贴合本单元",
            "核心素养是否转成学生可观察行为",
            "课时任务链是否符合真实教材安排",
            "评价证据是否能在课堂中看见",
            "材料与支架是否符合学校条件",
        ],
        **boundary_flags(),
        **profile(),
    }


def build_review_surface_trace(root: Path | None = None) -> dict[str, Any]:
    surface = build_review_surface_fixture(root)
    state = build_review_state(root)
    checklist = build_teacher_review_checklist(root)
    return {
        "trace_id": "big_unit_static_section_review_surface_trace_1013K_R4",
        "stage": STAGE_ID,
        "events": [
            {
                "event_id": "r4_event_01_static_sections_loaded",
                "event_type": "load_r3_static_sections",
                "section_count": surface["section_count"],
                "side_effects_performed": False,
            },
            {
                "event_id": "r4_event_02_review_surface_created",
                "event_type": "create_teacher_review_surface_fixture",
                "review_surface_id": surface["review_surface_id"],
                "side_effects_performed": False,
            },
            {
                "event_id": "r4_event_03_review_state_initialized",
                "event_type": "initialize_preview_only_review_state",
                "review_state_id": state["review_state_id"],
                "formal_apply_allowed": state["any_formal_apply_allowed"],
                "side_effects_performed": False,
            },
            {
                "event_id": "r4_event_04_teacher_checklist_created",
                "event_type": "create_teacher_confirmation_checklist",
                "checklist_id": checklist["checklist_id"],
                "item_count": len(checklist["items"]),
                "side_effects_performed": False,
            },
        ],
        "side_effects_performed": False,
        **boundary_flags(),
        **profile(),
    }


def build_static_section_preview_to_review_surface_fixture(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "review_surface_fixture": build_review_surface_fixture(root),
        "review_state": build_review_state(root),
        "teacher_review_checklist": build_teacher_review_checklist(root),
        "review_surface_trace": build_review_surface_trace(root),
        "boundary": boundary_flags(),
    }
