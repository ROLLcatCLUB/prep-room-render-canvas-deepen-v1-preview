from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R6_BIG_UNIT_REVIEW_ACTION_STATE_TO_PREVIEW_SURFACE_FIXTURE"


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
        "r5_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R5_big_unit_review_action_state_dry_run/1013K_R5_result.json",
        ),
        "r5_action_state": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R5_big_unit_review_action_state_dry_run/"
            "big_unit_section_preview_action_state_1013K_R5.json",
        ),
        "r5_accepted_items": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R5_big_unit_review_action_state_dry_run/"
            "big_unit_section_accepted_preview_items_1013K_R5.json",
        ),
        "r5_revision_queue": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R5_big_unit_review_action_state_dry_run/"
            "big_unit_section_revision_queue_1013K_R5.json",
        ),
        "r5_rejected_items": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R5_big_unit_review_action_state_dry_run/"
            "big_unit_section_rejected_items_1013K_R5.json",
        ),
    }
    missing = [str(path) for path in sources.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing preview surface sources: {missing}")
    return {key: _read_json(path) for key, path in sources.items()}


def boundary_flags() -> dict[str, bool]:
    return {
        "preview_surface_fixture_only": True,
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


def _preview_section(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "preview_section_id": item["preview_item_id"].replace("accepted_preview_item", "preview_surface_section"),
        "source_preview_item_id": item["preview_item_id"],
        "source_review_section_id": item["source_review_section_id"],
        "order": item["order"],
        "teacher_label": item["teacher_label"],
        "display_state": "preview_visible",
        "status_badges": item["status_badges"],
        "main_reading_content": item["main_reading_content"],
        "side_note": item["side_note"],
        "available_actions": [
            {
                "action": "revert",
                "teacher_label": "撤回预览",
                "allowed_now": True,
                "formal_apply_performed": False,
            },
            {
                "action": "revise",
                "teacher_label": "再改一版",
                "allowed_now": True,
                "formal_apply_performed": False,
            },
            {
                "action": "reject",
                "teacher_label": "暂不采用",
                "allowed_now": True,
                "formal_apply_performed": False,
            },
        ],
        "accepted_to_preview": True,
        "writes_unit_package": False,
        "writes_lesson_body": False,
        "formal_apply_performed": False,
    }


def build_preview_surface_fixture(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    accepted_items = sources["r5_accepted_items"].get("items", [])
    sections = [_preview_section(item) for item in accepted_items]
    return {
        "preview_surface_id": "big_unit_preview_surface_fixture_1013K_R6",
        "stage": STAGE_ID,
        "source_action_state_id": sources["r5_action_state"]["review_action_state_id"],
        "unit_title": "第一单元《多变的色彩》",
        "surface_role": "renderable_preview_surface_after_teacher_accept_to_preview_simulation",
        "display_mode": "big_unit_design_preview",
        "section_count": len(sections),
        "sections": sections,
        "top_notice": {
            "text": "当前为大单元预览，教师确认前不写入正式备课本。",
            "display_weight": "light",
        },
        "preview_surface_ready_for_static_render": True,
        "normal_candidate_generation_allowed": False,
        "can_formal_apply": False,
        **boundary_flags(),
        **profile(),
    }


def build_preview_navigation(root: Path | None = None) -> dict[str, Any]:
    surface = build_preview_surface_fixture(root)
    return {
        "navigation_id": "big_unit_preview_surface_navigation_1013K_R6",
        "stage": STAGE_ID,
        "source_preview_surface_id": surface["preview_surface_id"],
        "items": [
            {
                "preview_section_id": section["preview_section_id"],
                "order": section["order"],
                "teacher_label": section["teacher_label"],
                "display_state": section["display_state"],
            }
            for section in surface["sections"]
        ],
        "item_count": surface["section_count"],
        **boundary_flags(),
        **profile(),
    }


def build_preview_status(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    return {
        "preview_status_id": "big_unit_preview_surface_status_1013K_R6",
        "stage": STAGE_ID,
        "current_visible_path": "accepted_to_preview_only",
        "accepted_preview_items_count": sources["r5_action_state"].get("accepted_preview_items_count"),
        "revision_queue_count": sources["r5_action_state"].get("revision_queue_count"),
        "rejected_items_count": sources["r5_action_state"].get("rejected_items_count"),
        "revision_and_reject_are_alternate_paths": True,
        "revert_available": True,
        "preview_visible": True,
        "formal_apply_allowed": False,
        "normal_candidate_generation_allowed": False,
        **boundary_flags(),
        **profile(),
    }


def build_preview_surface_trace(root: Path | None = None) -> dict[str, Any]:
    surface = build_preview_surface_fixture(root)
    navigation = build_preview_navigation(root)
    status = build_preview_status(root)
    events = [
        {
            "event_id": "r6_event_01_action_state_loaded",
            "event_type": "load_r5_action_state",
            "side_effects_performed": False,
        },
        {
            "event_id": "r6_event_02_preview_surface_created",
            "event_type": "create_renderable_preview_surface_fixture",
            "preview_surface_id": surface["preview_surface_id"],
            "section_count": surface["section_count"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r6_event_03_navigation_created",
            "event_type": "create_preview_navigation",
            "navigation_id": navigation["navigation_id"],
            "item_count": navigation["item_count"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r6_event_04_status_created",
            "event_type": "create_preview_status",
            "preview_status_id": status["preview_status_id"],
            "side_effects_performed": False,
        },
    ]
    return {
        "preview_surface_trace_id": "big_unit_preview_surface_trace_1013K_R6",
        "stage": STAGE_ID,
        "event_count": len(events),
        "events": events,
        "side_effects_performed": False,
        **boundary_flags(),
        **profile(),
    }


def build_big_unit_review_action_state_to_preview_surface_fixture(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "preview_surface_fixture": build_preview_surface_fixture(root),
        "preview_navigation": build_preview_navigation(root),
        "preview_status": build_preview_status(root),
        "preview_surface_trace": build_preview_surface_trace(root),
        "boundary": boundary_flags(),
    }
