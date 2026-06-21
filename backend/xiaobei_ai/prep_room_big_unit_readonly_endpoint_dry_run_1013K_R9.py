from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R9_BIG_UNIT_READONLY_ENDPOINT_DRY_RUN_WITHOUT_ROUTE_REGISTRATION"


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
        "r8_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R8_big_unit_render_viewmodel_readonly_endpoint_contract/1013K_R8_result.json",
        ),
        "r8_contract": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R8_big_unit_render_viewmodel_readonly_endpoint_contract/"
            "big_unit_render_viewmodel_readonly_endpoint_contract_1013K_R8.json",
        ),
        "r8_response": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R8_big_unit_render_viewmodel_readonly_endpoint_contract/"
            "big_unit_render_viewmodel_readonly_response_fixture_1013K_R8.json",
        ),
    }
    missing = [str(path) for path in sources.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing readonly endpoint dry-run sources: {missing}")
    return {key: _read_json(path) for key, path in sources.items()}


def boundary_flags() -> dict[str, bool]:
    return {
        "readonly_endpoint_dry_run_only": True,
        "route_registered": False,
        "http_server_started": False,
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


def build_request_fixtures(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    response = _load_sources(root)["r8_response"]
    viewmodel_id = response["viewmodel"]["viewmodel_id"]
    first_chunk_id = response["render_queue"][0]
    return {
        "request_fixture_id": "big_unit_readonly_endpoint_request_fixture_1013K_R9",
        "stage": STAGE_ID,
        "requests": [
            {
                "request_id": "r9_request_full_viewmodel",
                "method": "GET",
                "viewmodel_id": viewmodel_id,
                "query": {"mode": "preview"},
                "expected_response_mode": "full_viewmodel_fixture",
            },
            {
                "request_id": "r9_request_single_chunk",
                "method": "GET",
                "viewmodel_id": viewmodel_id,
                "query": {"mode": "preview", "chunk_id": first_chunk_id},
                "expected_response_mode": "single_chunk_fixture",
            },
            {
                "request_id": "r9_request_missing_chunk",
                "method": "GET",
                "viewmodel_id": viewmodel_id,
                "query": {"mode": "preview", "chunk_id": "missing_chunk_for_error_fixture"},
                "expected_response_mode": "readonly_error_fixture",
            },
        ],
        "request_count": 3,
        **boundary_flags(),
        **profile(),
    }


def _find_chunk(viewmodel: dict[str, Any], chunk_id: str) -> dict[str, Any] | None:
    for chunk in viewmodel.get("section_chunks", []):
        if chunk.get("chunk_id") == chunk_id:
            return chunk
    return None


def handle_readonly_viewmodel_request(request: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    response_fixture = sources["r8_response"]
    viewmodel = response_fixture["viewmodel"]
    expected_viewmodel_id = viewmodel["viewmodel_id"]
    request_viewmodel_id = request.get("viewmodel_id")
    query = request.get("query", {})
    chunk_id = query.get("chunk_id")

    base = {
        "stage": STAGE_ID,
        "request_id": request.get("request_id"),
        "method": request.get("method"),
        "viewmodel_id": request_viewmodel_id,
        "route_registered": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        **profile(),
    }
    if request.get("method") != "GET":
        return {
            **base,
            "ok": False,
            "status": 405,
            "error_code": "METHOD_NOT_ALLOWED",
            "teacher_visible_message": "当前只支持只读查看。",
            "boundary": boundary_flags(),
        }
    if request_viewmodel_id != expected_viewmodel_id:
        return {
            **base,
            "ok": False,
            "status": 404,
            "error_code": "VIEWMODEL_NOT_FOUND",
            "teacher_visible_message": "没有找到这份大单元预览。",
            "boundary": boundary_flags(),
        }
    if chunk_id:
        chunk = _find_chunk(viewmodel, chunk_id)
        if chunk is None:
            return {
                **base,
                "ok": False,
                "status": 404,
                "error_code": "CHUNK_NOT_FOUND",
                "missing_chunk_id": chunk_id,
                "teacher_visible_message": "没有找到这一段预览内容，可以返回完整预览重新选择。",
                "chunked": True,
                "whole_document_blob_required": False,
                "boundary": boundary_flags(),
            }
        return {
            **base,
            "ok": True,
            "status": 200,
            "response_mode": "single_chunk_fixture",
            "chunked": True,
            "chunk": chunk,
            "whole_document_blob_required": False,
            "can_update_independently": True,
            "boundary": boundary_flags(),
        }
    return {
        **base,
        "ok": True,
        "status": 200,
        "response_mode": "full_viewmodel_fixture",
        "chunked": True,
        "viewmodel": viewmodel,
        "chunk_count": response_fixture["chunk_count"],
        "render_queue": response_fixture["render_queue"],
        "whole_document_blob_required": False,
        "boundary": boundary_flags(),
    }


def build_dry_run_responses(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    requests = build_request_fixtures(root)["requests"]
    responses = [handle_readonly_viewmodel_request(request, root) for request in requests]
    return {
        "dry_run_responses_id": "big_unit_readonly_endpoint_dry_run_responses_1013K_R9",
        "stage": STAGE_ID,
        "responses": responses,
        "response_count": len(responses),
        "full_response": responses[0],
        "single_chunk_response": responses[1],
        "error_response": responses[2],
        **boundary_flags(),
        **profile(),
    }


def build_endpoint_dry_run_trace(root: Path | None = None) -> dict[str, Any]:
    request_fixtures = build_request_fixtures(root)
    dry_run_responses = build_dry_run_responses(root)
    events = [
        {
            "event_id": "r9_event_01_r8_contract_loaded",
            "event_type": "load_r8_endpoint_contract_and_response_fixture",
            "side_effects_performed": False,
        },
        {
            "event_id": "r9_event_02_request_fixtures_created",
            "event_type": "create_full_single_chunk_and_error_requests",
            "request_count": request_fixtures["request_count"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r9_event_03_dry_run_responses_created",
            "event_type": "handle_requests_in_function_without_route_registration",
            "response_count": dry_run_responses["response_count"],
            "side_effects_performed": False,
        },
    ]
    return {
        "trace_id": "big_unit_readonly_endpoint_dry_run_trace_1013K_R9",
        "stage": STAGE_ID,
        "event_count": len(events),
        "events": events,
        "side_effects_performed": False,
        **boundary_flags(),
        **profile(),
    }


def build_big_unit_readonly_endpoint_dry_run_without_route_registration(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    responses = build_dry_run_responses(root)
    return {
        "stage": STAGE_ID,
        "request_fixtures": build_request_fixtures(root),
        "full_response": responses["full_response"],
        "single_chunk_response": responses["single_chunk_response"],
        "error_response": responses["error_response"],
        "dry_run_responses": responses,
        "endpoint_trace": build_endpoint_dry_run_trace(root),
        "boundary": boundary_flags(),
    }
