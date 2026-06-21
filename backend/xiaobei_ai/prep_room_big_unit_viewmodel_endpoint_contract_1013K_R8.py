from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R8_BIG_UNIT_RENDER_VIEWMODEL_READONLY_ENDPOINT_CONTRACT"


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
        "r7_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R7_big_unit_preview_surface_to_render_viewmodel_contract/1013K_R7_result.json",
        ),
        "r7_contract": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R7_big_unit_preview_surface_to_render_viewmodel_contract/"
            "big_unit_render_viewmodel_contract_1013K_R7.json",
        ),
        "r7_viewmodel": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R7_big_unit_preview_surface_to_render_viewmodel_contract/"
            "big_unit_render_viewmodel_fixture_1013K_R7.json",
        ),
        "r7_mapping": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R7_big_unit_preview_surface_to_render_viewmodel_contract/"
            "big_unit_section_to_render_chunk_mapping_1013K_R7.json",
        ),
    }
    missing = [str(path) for path in sources.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing readonly endpoint contract sources: {missing}")
    return {key: _read_json(path) for key, path in sources.items()}


def boundary_flags() -> dict[str, bool]:
    return {
        "readonly_endpoint_contract_only": True,
        "route_registered": False,
        "runtime_connected": False,
        "preview_only": True,
        "teacher_review_required": True,
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


def build_readonly_endpoint_contract(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    viewmodel = sources["r7_viewmodel"]
    return {
        "endpoint_contract_id": "big_unit_render_viewmodel_readonly_endpoint_contract_1013K_R8",
        "stage": STAGE_ID,
        "source_viewmodel_id": viewmodel["viewmodel_id"],
        "contract_role": "define_future_readonly_endpoint_for_chunked_big_unit_render_viewmodel",
        "route_registered": False,
        "method": "GET",
        "path_template": "/api/prep-room/big-unit-preview-viewmodel/{viewmodel_id}",
        "query_params": {
            "include": ["header", "status_strip", "material_prompt", "section_chunks", "side_reference", "action_bar"],
            "chunk_id": "optional stable render chunk id for incremental fetch",
            "mode": "preview",
        },
        "response_shape": {
            "ok": "boolean",
            "stage": STAGE_ID,
            "viewmodel": "object",
            "chunked": "boolean",
            "whole_document_blob_required": "boolean",
            "boundary": "object",
        },
        "allowed_response_modes": ["full_viewmodel_fixture", "single_chunk_fixture"],
        "forbidden_runtime_behavior": [
            "provider_call",
            "model_call",
            "database_write",
            "memory_write",
            "feishu_write",
            "formal_apply",
            "unit_package_write",
            "lesson_body_write",
        ],
        "section_chunks_renderable_independently": True,
        "whole_document_blob_required": False,
        **boundary_flags(),
        **profile(),
    }


def build_response_fixture(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    viewmodel = sources["r7_viewmodel"]
    mapping = sources["r7_mapping"]
    return {
        "response_fixture_id": "big_unit_render_viewmodel_readonly_response_fixture_1013K_R8",
        "stage": STAGE_ID,
        "ok": True,
        "route_registered": False,
        "method": "GET",
        "path": f"/api/prep-room/big-unit-preview-viewmodel/{viewmodel['viewmodel_id']}",
        "viewmodel": viewmodel,
        "chunked": True,
        "chunk_count": viewmodel.get("progressive_render", {}).get("chunk_count"),
        "render_queue": viewmodel.get("progressive_render", {}).get("render_queue", []),
        "single_chunk_example": {
            "chunk_id": mapping["mappings"][0]["chunk_id"],
            "fetch_path": f"/api/prep-room/big-unit-preview-viewmodel/{viewmodel['viewmodel_id']}?chunk_id={mapping['mappings'][0]['chunk_id']}",
            "can_update_independently": True,
        },
        "whole_document_blob_required": False,
        "side_reference_default_collapsed": viewmodel.get("side_reference", {}).get("default_collapsed"),
        "formal_apply_action_present": viewmodel.get("action_bar", {}).get("formal_apply_action_present"),
        "boundary": boundary_flags(),
        **boundary_flags(),
        **profile(),
    }


def build_endpoint_trace(root: Path | None = None) -> dict[str, Any]:
    contract = build_readonly_endpoint_contract(root)
    response = build_response_fixture(root)
    events = [
        {
            "event_id": "r8_event_01_r7_viewmodel_loaded",
            "event_type": "load_r7_render_viewmodel_fixture",
            "side_effects_performed": False,
        },
        {
            "event_id": "r8_event_02_endpoint_contract_created",
            "event_type": "create_readonly_endpoint_contract_without_route_registration",
            "route_registered": contract["route_registered"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r8_event_03_response_fixture_created",
            "event_type": "create_readonly_response_fixture",
            "chunk_count": response["chunk_count"],
            "side_effects_performed": False,
        },
    ]
    return {
        "trace_id": "big_unit_render_viewmodel_readonly_endpoint_trace_1013K_R8",
        "stage": STAGE_ID,
        "event_count": len(events),
        "events": events,
        "side_effects_performed": False,
        **boundary_flags(),
        **profile(),
    }


def build_big_unit_render_viewmodel_readonly_endpoint_contract(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "readonly_endpoint_contract": build_readonly_endpoint_contract(root),
        "readonly_response_fixture": build_response_fixture(root),
        "endpoint_trace": build_endpoint_trace(root),
        "boundary": boundary_flags(),
    }
