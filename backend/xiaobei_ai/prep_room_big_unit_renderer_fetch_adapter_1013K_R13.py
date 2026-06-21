from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R13_RENDERER_READONLY_FETCH_ADAPTER_FIXTURE"
INHERITS_FROM = "1013K_R12_READONLY_ROUTE_RESPONSE_CONTRACT_AND_CLIENT_FETCH_FIXTURE"
NEXT_STAGE = "1013K_M3_READONLY_ROUTE_CLIENT_RENDERER_MILESTONE_PACKAGE"


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
        "r12_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R12_readonly_route_response_contract_and_client_fetch_fixture/1013K_R12_result.json",
        ),
        "r12_contract": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R12_readonly_route_response_contract_and_client_fetch_fixture/"
            "readonly_route_response_contract_1013K_R12.json",
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
        raise FileNotFoundError(f"Missing R13 renderer adapter sources: {missing}")
    return {key: _read_json(path) for key, path in sources.items()}


def boundary_flags() -> dict[str, bool]:
    return {
        "renderer_fetch_adapter_fixture_only": True,
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


def build_renderer_adapter_contract(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    response = sources["r8_response"]
    viewmodel = response["viewmodel"]
    chunks = viewmodel.get("section_chunks", [])
    return {
        "renderer_adapter_contract_id": "renderer_readonly_fetch_adapter_contract_1013K_R13",
        "stage": STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "r12_pass": sources["r12_result"].get("validator_pass") is True,
        "source_route_public_template": sources["r12_contract"]["route_public_template"],
        "viewmodel_id": viewmodel["viewmodel_id"],
        "render_queue": response["render_queue"],
        "render_chunk_count": len(chunks),
        "renderer_input_modes": ["full_viewmodel_response", "single_chunk_response"],
        "renderer_output_shape": {
            "document_header": "teacher_reading_header",
            "render_queue": "ordered_chunk_ids",
            "section_chunks": "independent_renderable_sections",
            "chunk_patch_target": "chunk_id",
            "preview_status": "preview_only_boundary",
        },
        "progressive_rendering_supported": True,
        "single_chunk_update_supported": True,
        "whole_document_blob_required": False,
        **boundary_flags(),
    }


def build_renderer_adapter_fixture_js(root: Path | None = None) -> str:
    contract = build_renderer_adapter_contract(root)
    return f"""// 1013K_R13 renderer readonly fetch adapter fixture.
// Fixture only: not mounted into the main frontend and not connected to runtime.
export function adaptBigUnitViewModelResponseToRenderState(payload) {{
  if (!payload || payload.ok !== true) {{
    return {{
      ok: false,
      mode: 'readonly_error',
      teacherVisibleMessage: payload?.teacher_visible_message || '暂时无法读取这份大单元预览。',
      previewOnly: true,
      chunks: [],
      renderQueue: [],
    }};
  }}
  if (payload.chunk) {{
    return {{
      ok: true,
      mode: 'single_chunk',
      previewOnly: payload.boundary?.preview_only !== false,
      chunks: [payload.chunk],
      renderQueue: [payload.chunk.chunk_id],
      replaceChunkId: payload.chunk.chunk_id,
    }};
  }}
  const viewmodel = payload.viewmodel || {{}};
  return {{
    ok: true,
    mode: 'full_viewmodel',
    previewOnly: payload.boundary?.preview_only !== false,
    documentHeader: viewmodel.document_header || null,
    chunks: viewmodel.section_chunks || [],
    renderQueue: payload.render_queue || viewmodel.render_queue || [],
    chunkCount: payload.chunk_count || (viewmodel.section_chunks || []).length,
  }};
}}

export const bigUnitRendererAdapterContract1013K_R13 = {{
  viewmodelId: '{contract["viewmodel_id"]}',
  progressiveRenderingSupported: true,
  singleChunkUpdateSupported: true,
  wholeDocumentBlobRequired: false,
}};
"""


def build_renderer_adapter_trace(root: Path | None = None) -> dict[str, Any]:
    contract = build_renderer_adapter_contract(root)
    events = [
        {
            "event_id": "r13_event_01_r12_fetch_contract_loaded",
            "event_type": "load_r12_fetch_contract",
            "r12_pass": contract["r12_pass"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r13_event_02_renderer_output_shape_defined",
            "event_type": "define_renderer_render_state_output_shape",
            "progressive_rendering_supported": contract["progressive_rendering_supported"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r13_event_03_adapter_fixture_created",
            "event_type": "create_standalone_renderer_adapter_fixture_js",
            "frontend_page_modified": False,
            "side_effects_performed": False,
        },
    ]
    return {
        "trace_id": "renderer_readonly_fetch_adapter_trace_1013K_R13",
        "stage": STAGE_ID,
        "event_count": len(events),
        "events": events,
        "side_effects_performed": False,
        **boundary_flags(),
    }


def build_renderer_readonly_fetch_adapter_fixture(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "renderer_adapter_contract": build_renderer_adapter_contract(root),
        "renderer_adapter_fixture_js": build_renderer_adapter_fixture_js(root),
        "renderer_adapter_trace": build_renderer_adapter_trace(root),
        "boundary": boundary_flags(),
    }
