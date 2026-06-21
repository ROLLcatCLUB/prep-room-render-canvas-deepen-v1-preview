from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R5_BIG_UNIT_REVIEW_ACTION_STATE_DRY_RUN"


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
        "r4_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R4_static_section_preview_to_review_surface_fixture/1013K_R4_result.json",
        ),
        "r4_surface": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R4_static_section_preview_to_review_surface_fixture/"
            "big_unit_review_surface_fixture_1013K_R4.json",
        ),
        "r4_state": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R4_static_section_preview_to_review_surface_fixture/"
            "big_unit_review_state_1013K_R4.json",
        ),
        "r4_checklist": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R4_static_section_preview_to_review_surface_fixture/"
            "big_unit_teacher_review_checklist_1013K_R4.json",
        ),
    }
    missing = [str(path) for path in sources.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing review action state sources: {missing}")
    return {key: _read_json(path) for key, path in sources.items()}


def boundary_flags() -> dict[str, bool]:
    return {
        "action_state_dry_run_only": True,
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
        "github_upload_deferred_until_next_milestone": True,
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


def _section_base(section: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_review_section_id": section["review_section_id"],
        "source_section_preview_id": section["source_section_preview_id"],
        "order": section["order"],
        "teacher_label": section["teacher_label"],
        "main_reading_content": section["main_reading_content"],
        "side_note": section["side_note"],
    }


def build_accepted_preview_items(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    surface = _load_sources(root)["r4_surface"]
    items = []
    for section in surface.get("sections", []):
        items.append(
            {
                **_section_base(section),
                "preview_item_id": section["review_section_id"].replace("review_section", "accepted_preview_item"),
                "action": "accept_to_preview",
                "state": "accepted_to_preview_only",
                "status_badges": ["已进入预览", "教师确认前不生效"],
                "can_revert": True,
                "can_revise": True,
                "can_formal_apply": False,
                "accepted_to_preview": True,
                "writes_unit_package": False,
                "writes_lesson_body": False,
                "formal_apply_performed": False,
            }
        )
    return {
        "accepted_preview_items_id": "big_unit_section_accepted_preview_items_1013K_R5",
        "stage": STAGE_ID,
        "source_review_surface_id": surface["review_surface_id"],
        "item_count": len(items),
        "items": items,
        **boundary_flags(),
        **profile(),
    }


def build_revision_queue(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    surface = _load_sources(root)["r4_surface"]
    items = []
    for section in surface.get("sections", []):
        items.append(
            {
                **_section_base(section),
                "revision_item_id": section["review_section_id"].replace("review_section", "revision_item"),
                "action": "revise",
                "state": "revision_requested_preview_only",
                "teacher_prompt": f"请告诉小教，{section['teacher_label']}这一段想改得更具体、简短，还是更贴近你的教材。",
                "can_return_to_preview": True,
                "can_formal_apply": False,
                "writes_unit_package": False,
                "writes_lesson_body": False,
                "formal_apply_performed": False,
            }
        )
    return {
        "revision_queue_id": "big_unit_section_revision_queue_1013K_R5",
        "stage": STAGE_ID,
        "source_review_surface_id": surface["review_surface_id"],
        "item_count": len(items),
        "items": items,
        **boundary_flags(),
        **profile(),
    }


def build_rejected_items(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    surface = _load_sources(root)["r4_surface"]
    items = []
    for section in surface.get("sections", []):
        items.append(
            {
                **_section_base(section),
                "rejected_item_id": section["review_section_id"].replace("review_section", "rejected_item"),
                "action": "reject",
                "state": "rejected_for_current_preview_path",
                "teacher_label_for_state": "暂不采用",
                "can_restore": True,
                "can_formal_apply": False,
                "writes_unit_package": False,
                "writes_lesson_body": False,
                "formal_apply_performed": False,
            }
        )
    return {
        "rejected_items_id": "big_unit_section_rejected_items_1013K_R5",
        "stage": STAGE_ID,
        "source_review_surface_id": surface["review_surface_id"],
        "item_count": len(items),
        "items": items,
        **boundary_flags(),
        **profile(),
    }


def build_review_action_state(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    r4_surface = sources["r4_surface"]
    accepted = build_accepted_preview_items(root)
    revision = build_revision_queue(root)
    rejected = build_rejected_items(root)
    return {
        "review_action_state_id": "big_unit_section_review_action_state_1013K_R5",
        "stage": STAGE_ID,
        "source_review_surface_id": r4_surface["review_surface_id"],
        "current_default_path": "accepted_to_preview_only",
        "path_semantics": {
            "accepted_preview_items": "current simulated preview path for all sections",
            "revision_queue": "alternate path simulation for revise action",
            "rejected_items": "alternate path simulation for reject action",
            "not_simultaneous_teacher_final_state": True,
        },
        "accepted_preview_items_count": accepted["item_count"],
        "revision_queue_count": revision["item_count"],
        "rejected_items_count": rejected["item_count"],
        "revert_available": True,
        "normal_candidate_generation_allowed": False,
        "can_formal_apply": False,
        "teacher_confirmation_required": True,
        **boundary_flags(),
        **profile(),
    }


def build_action_trace(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    surface = _load_sources(root)["r4_surface"]
    events = []
    for section in surface.get("sections", []):
        for action in ["accept_to_preview", "revise", "reject"]:
            events.append(
                {
                    "event_id": f"r5_event_{section['order']:02d}_{action}",
                    "review_section_id": section["review_section_id"],
                    "teacher_label": section["teacher_label"],
                    "action": action,
                    "result_state": {
                        "accept_to_preview": "accepted_to_preview_only",
                        "revise": "revision_requested_preview_only",
                        "reject": "rejected_for_current_preview_path",
                    }[action],
                    "side_effects_performed": False,
                    "provider_called": False,
                    "model_called": False,
                    "formal_apply_performed": False,
                    "writes_unit_package": False,
                    "writes_lesson_body": False,
                }
            )
    return {
        "action_trace_id": "big_unit_section_review_action_trace_1013K_R5",
        "stage": STAGE_ID,
        "source_review_surface_id": surface["review_surface_id"],
        "event_count": len(events),
        "events": events,
        "side_effects_performed": False,
        **boundary_flags(),
        **profile(),
    }


def build_big_unit_review_action_state_dry_run(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "review_action_state": build_review_action_state(root),
        "accepted_preview_items": build_accepted_preview_items(root),
        "revision_queue": build_revision_queue(root),
        "rejected_items": build_rejected_items(root),
        "action_trace": build_action_trace(root),
        "boundary": boundary_flags(),
    }
