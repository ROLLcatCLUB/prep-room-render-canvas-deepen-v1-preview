from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R7_BIG_UNIT_PREVIEW_SURFACE_TO_RENDER_VIEWMODEL_CONTRACT"


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
        "r6_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R6_big_unit_review_action_state_to_preview_surface_fixture/1013K_R6_result.json",
        ),
        "r6_surface": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R6_big_unit_review_action_state_to_preview_surface_fixture/"
            "big_unit_preview_surface_fixture_1013K_R6.json",
        ),
        "r6_navigation": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R6_big_unit_review_action_state_to_preview_surface_fixture/"
            "big_unit_preview_surface_navigation_1013K_R6.json",
        ),
        "r6_status": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R6_big_unit_review_action_state_to_preview_surface_fixture/"
            "big_unit_preview_surface_status_1013K_R6.json",
        ),
    }
    missing = [str(path) for path in sources.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing render viewmodel sources: {missing}")
    return {key: _read_json(path) for key, path in sources.items()}


def boundary_flags() -> dict[str, bool]:
    return {
        "render_viewmodel_contract_only": True,
        "render_viewmodel_fixture_only": True,
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


def build_render_viewmodel_contract(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    surface = sources["r6_surface"]
    return {
        "contract_id": "big_unit_render_viewmodel_contract_1013K_R7",
        "stage": STAGE_ID,
        "source_preview_surface_id": surface["preview_surface_id"],
        "contract_role": "define_frontend_render_shape_for_big_unit_preview_surface",
        "viewmodel_kind": "prep_room_big_unit_design_preview",
        "version": "1013K_R7",
        "top_level_shape": {
            "viewmodel_id": "string",
            "viewmodel_kind": "prep_room_big_unit_design_preview",
            "header": "object",
            "status_strip": "object",
            "material_prompt": "object|null",
            "section_chunks": "array<object>",
            "side_reference": "object",
            "action_bar": "object",
            "progressive_render": "object",
            "boundary": "object",
        },
        "section_chunk_shape": {
            "chunk_id": "string",
            "source_preview_section_id": "string",
            "order": "number",
            "teacher_label": "string",
            "render_as": "reading_section",
            "title_number": "string",
            "paragraphs": "array<string>",
            "summary": "string",
            "status_badges": "array<string>",
            "side_note_ref": "string",
            "actions": "array<object>",
            "render_state": "pending|visible|updating|hidden",
        },
        "progressive_render_contract": {
            "section_chunks_renderable_independently": True,
            "whole_document_blob_required": False,
            "initial_chunk_ids": ["header", "status_strip", "material_prompt"],
            "can_stream_section_by_section": True,
            "can_reorder_without_rewriting_text": True,
            "can_update_single_section_preview": True,
            "stable_chunk_identity_required": True,
        },
        "teacher_surface_rules": {
            "hide_engineering_field_names": True,
            "show_teacher_labels": True,
            "keep_side_notes_collapsed_by_default": True,
            "show_preview_only_status_lightly": True,
            "do_not_show_contract_words_to_teacher": True,
        },
        **boundary_flags(),
        **profile(),
    }


def _chunk_from_section(section: dict[str, Any]) -> dict[str, Any]:
    return {
        "chunk_id": section["preview_section_id"].replace("preview_surface_section", "render_chunk"),
        "source_preview_section_id": section["preview_section_id"],
        "source_review_section_id": section["source_review_section_id"],
        "order": section["order"],
        "teacher_label": section["teacher_label"],
        "render_as": "reading_section",
        "title_number": f"{section['order']:02d}",
        "summary": section["main_reading_content"].get("summary", ""),
        "paragraphs": section["main_reading_content"].get("paragraphs", []),
        "status_badges": section.get("status_badges", []),
        "side_note_ref": section["preview_section_id"].replace("preview_surface_section", "side_note"),
        "actions": [
            {
                "action": action["action"],
                "teacher_label": action["teacher_label"],
                "allowed_now": action.get("allowed_now") is True,
                "preview_only": True,
                "formal_apply_performed": False,
            }
            for action in section.get("available_actions", [])
        ],
        "render_state": "visible",
        "accepted_to_preview": section.get("accepted_to_preview") is True,
        "writes_unit_package": False,
        "writes_lesson_body": False,
        "formal_apply_performed": False,
    }


def build_render_viewmodel_fixture(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    surface = sources["r6_surface"]
    status = sources["r6_status"]
    chunks = [_chunk_from_section(section) for section in surface.get("sections", [])]
    return {
        "viewmodel_id": "big_unit_render_viewmodel_fixture_1013K_R7",
        "stage": STAGE_ID,
        "source_preview_surface_id": surface["preview_surface_id"],
        "viewmodel_kind": "prep_room_big_unit_design_preview",
        "unit_title": surface["unit_title"],
        "header": {
            "title": surface["unit_title"],
            "eyebrow": "大单元设计",
            "status_lights": [
                {"label": "预览", "tone": "green"},
                {"label": "资料待补", "tone": "yellow"},
                {"label": "教师确认前不生效", "tone": "red"},
            ],
            "teacher_visible": True,
        },
        "status_strip": {
            "current_visible_path": status["current_visible_path"],
            "preview_visible": status["preview_visible"],
            "formal_apply_allowed": False,
            "normal_candidate_generation_allowed": False,
            "display_weight": "light",
        },
        "material_prompt": {
            "prompt_id": "big_unit_material_prompt_1013K_R7",
            "display_position": "below_header",
            "tone": "warning_light",
            "text": "缺教材目录、单元页或课时安排时，小教只能先给临时预览；补齐后才能生成更稳定的大单元设计。",
            "actions": ["上传教材目录", "上传单元页", "补充课时安排", "先按临时预览"],
        },
        "section_chunks": chunks,
        "side_reference": {
            "default_collapsed": True,
            "items": [
                {
                    "side_note_id": section["preview_section_id"].replace("preview_surface_section", "side_note"),
                    "source_preview_section_id": section["preview_section_id"],
                    "teacher_label": section["teacher_label"],
                    "risk_note": section.get("side_note", {}).get("risk_note"),
                    "source_context": section.get("side_note", {}).get("source_context", {}),
                }
                for section in surface.get("sections", [])
            ],
        },
        "action_bar": {
            "actions": [
                {"action": "review_all", "teacher_label": "查看全部预览", "preview_only": True},
                {"action": "revise_selected", "teacher_label": "修改当前段", "preview_only": True},
                {"action": "revert_selected", "teacher_label": "撤回当前段预览", "preview_only": True},
            ],
            "formal_apply_action_present": False,
        },
        "progressive_render": {
            "section_chunks_renderable_independently": True,
            "whole_document_blob_required": False,
            "chunk_count": len(chunks),
            "initial_visible_chunk_ids": ["header", "status_strip", "material_prompt"],
            "render_queue": [chunk["chunk_id"] for chunk in chunks],
            "can_update_single_section_preview": True,
            "can_stream_section_by_section": True,
        },
        "boundary": boundary_flags(),
        **boundary_flags(),
        **profile(),
    }


def build_section_render_mapping(root: Path | None = None) -> dict[str, Any]:
    viewmodel = build_render_viewmodel_fixture(root)
    return {
        "mapping_id": "big_unit_section_to_render_chunk_mapping_1013K_R7",
        "stage": STAGE_ID,
        "source_preview_surface_id": viewmodel["source_preview_surface_id"],
        "mappings": [
            {
                "source_preview_section_id": chunk["source_preview_section_id"],
                "chunk_id": chunk["chunk_id"],
                "order": chunk["order"],
                "teacher_label": chunk["teacher_label"],
                "render_state": chunk["render_state"],
                "can_update_independently": True,
            }
            for chunk in viewmodel["section_chunks"]
        ],
        "mapping_count": len(viewmodel["section_chunks"]),
        "all_chunks_stable": True,
        "whole_document_blob_required": False,
        **boundary_flags(),
        **profile(),
    }


def build_render_viewmodel_trace(root: Path | None = None) -> dict[str, Any]:
    viewmodel = build_render_viewmodel_fixture(root)
    mapping = build_section_render_mapping(root)
    events = [
        {
            "event_id": "r7_event_01_preview_surface_loaded",
            "event_type": "load_r6_preview_surface",
            "side_effects_performed": False,
        },
        {
            "event_id": "r7_event_02_viewmodel_contract_created",
            "event_type": "create_render_viewmodel_contract",
            "side_effects_performed": False,
        },
        {
            "event_id": "r7_event_03_viewmodel_fixture_created",
            "event_type": "create_render_viewmodel_fixture",
            "chunk_count": viewmodel["progressive_render"]["chunk_count"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r7_event_04_section_mapping_created",
            "event_type": "create_section_to_render_chunk_mapping",
            "mapping_count": mapping["mapping_count"],
            "side_effects_performed": False,
        },
    ]
    return {
        "trace_id": "big_unit_render_viewmodel_trace_1013K_R7",
        "stage": STAGE_ID,
        "event_count": len(events),
        "events": events,
        "side_effects_performed": False,
        **boundary_flags(),
        **profile(),
    }


def build_big_unit_preview_surface_to_render_viewmodel_contract(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "render_viewmodel_contract": build_render_viewmodel_contract(root),
        "render_viewmodel_fixture": build_render_viewmodel_fixture(root),
        "section_render_mapping": build_section_render_mapping(root),
        "render_viewmodel_trace": build_render_viewmodel_trace(root),
        "boundary": boundary_flags(),
    }
