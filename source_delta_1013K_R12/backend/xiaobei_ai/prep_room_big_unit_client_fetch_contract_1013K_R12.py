from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R12_READONLY_ROUTE_RESPONSE_CONTRACT_AND_CLIENT_FETCH_FIXTURE"
INHERITS_FROM = "1013K_R11_READONLY_ROUTE_REGISTRATION_STATIC_APPLY_GATED"
NEXT_STAGE = "1013K_R13_RENDERER_READONLY_FETCH_ADAPTER_FIXTURE"
ROUTE_PUBLIC_TEMPLATE = "/api/prep-room/big-unit-preview-viewmodel/{viewmodel_id}"


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
        "r11_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R11_readonly_route_registration_static_apply_gated/1013K_R11_result.json",
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
        raise FileNotFoundError(f"Missing R12 client fetch contract sources: {missing}")
    return {key: _read_json(path) for key, path in sources.items()}


def boundary_flags() -> dict[str, bool]:
    return {
        "client_fetch_contract_only": True,
        "frontend_page_modified": False,
        "runtime_connected": False,
        "http_server_started": False,
        "preview_only": True,
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


def build_response_contract(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    viewmodel = sources["r8_response"]["viewmodel"]
    first_chunk_id = sources["r8_response"]["render_queue"][0]
    return {
        "response_contract_id": "readonly_route_response_contract_1013K_R12",
        "stage": STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "r11_pass": sources["r11_result"].get("validator_pass") is True,
        "route_public_template": ROUTE_PUBLIC_TEMPLATE,
        "viewmodel_id": viewmodel["viewmodel_id"],
        "first_chunk_id": first_chunk_id,
        "supported_fetch_modes": [
            {
                "mode": "full_viewmodel",
                "method": "GET",
                "path": ROUTE_PUBLIC_TEMPLATE,
                "required_response_fields": ["ok", "status", "viewmodel", "render_queue", "chunk_count"],
            },
            {
                "mode": "single_chunk",
                "method": "GET",
                "path": f"{ROUTE_PUBLIC_TEMPLATE}?chunk_id={{chunk_id}}",
                "required_response_fields": ["ok", "status", "chunk", "chunked", "can_update_independently"],
            },
            {
                "mode": "readonly_error",
                "method": "GET",
                "path": f"{ROUTE_PUBLIC_TEMPLATE}?chunk_id={{missing_chunk_id}}",
                "required_response_fields": ["ok", "status", "error_code", "teacher_visible_message"],
            },
        ],
        "chunked_rendering_supported": True,
        "whole_document_blob_required": False,
        "renderer_can_request_single_chunk": True,
        **boundary_flags(),
    }


def build_client_fetch_fixture_js(root: Path | None = None) -> str:
    contract = build_response_contract(root)
    viewmodel_id = contract["viewmodel_id"]
    first_chunk_id = contract["first_chunk_id"]
    return f"""// 1013K_R12 readonly client fetch fixture.
// Fixture only: not mounted into the main frontend and not connected to runtime.
export async function fetchBigUnitPreviewViewModel({{ viewmodelId, chunkId, fetchImpl = fetch }}) {{
  const encodedId = encodeURIComponent(viewmodelId);
  const url = new URL(`/api/prep-room/big-unit-preview-viewmodel/${{encodedId}}`, window.location.origin);
  if (chunkId) {{
    url.searchParams.set('chunk_id', chunkId);
  }}
  const response = await fetchImpl(url.toString(), {{ method: 'GET' }});
  const payload = await response.json();
  return {{
    ok: response.ok && payload.ok === true,
    status: response.status,
    mode: payload.response_mode || 'readonly_error',
    viewmodel: payload.viewmodel || null,
    chunk: payload.chunk || null,
    renderQueue: payload.render_queue || [],
    teacherVisibleMessage: payload.teacher_visible_message || '',
    previewOnly: payload.boundary?.preview_only === true,
    formalApplyPerformed: payload.formal_apply_performed === true,
  }};
}}

export const bigUnitPreviewFetchExamples1013K_R12 = {{
  full: {{ viewmodelId: '{viewmodel_id}' }},
  singleChunk: {{ viewmodelId: '{viewmodel_id}', chunkId: '{first_chunk_id}' }},
  missingChunk: {{ viewmodelId: '{viewmodel_id}', chunkId: 'missing_chunk_for_error_fixture' }},
}};
"""


def build_fetch_trace(root: Path | None = None) -> dict[str, Any]:
    contract = build_response_contract(root)
    events = [
        {
            "event_id": "r12_event_01_r11_route_contract_loaded",
            "event_type": "load_r11_static_route_result",
            "r11_pass": contract["r11_pass"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r12_event_02_response_modes_defined",
            "event_type": "define_full_single_chunk_and_error_fetch_modes",
            "mode_count": len(contract["supported_fetch_modes"]),
            "side_effects_performed": False,
        },
        {
            "event_id": "r12_event_03_client_fetch_fixture_created",
            "event_type": "create_standalone_client_fetch_fixture_js",
            "frontend_page_modified": False,
            "side_effects_performed": False,
        },
    ]
    return {
        "trace_id": "readonly_client_fetch_contract_trace_1013K_R12",
        "stage": STAGE_ID,
        "event_count": len(events),
        "events": events,
        "side_effects_performed": False,
        **boundary_flags(),
    }


def build_readonly_route_response_contract_and_client_fetch_fixture(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "response_contract": build_response_contract(root),
        "client_fetch_fixture_js": build_client_fetch_fixture_js(root),
        "fetch_trace": build_fetch_trace(root),
        "boundary": boundary_flags(),
    }
