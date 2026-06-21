from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R15_ISOLATED_STATIC_FRONTEND_READONLY_BINDING_FIXTURE"
INHERITS_FROM = "1013K_R14_FRONTEND_READONLY_RENDER_BINDING_REVIEW_GATE"
NEXT_STAGE = "1013K_R16_ISOLATED_STATIC_BINDING_VISUAL_SMOKE"


def _repo_root_from_module() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


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
        "r14_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R14_frontend_readonly_render_binding_review_gate/1013K_R14_result.json",
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
        raise FileNotFoundError(f"Missing R15 isolated static binding sources: {missing}")
    return {key: _read_json(path) for key, path in sources.items()}


def boundary_flags() -> dict[str, bool]:
    return {
        "isolated_static_binding_fixture_only": True,
        "formal_frontend_page_modified": False,
        "runtime_connected": False,
        "http_server_started": False,
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


def build_renderer_chunk_mount_map(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    viewmodel = sources["r8_response"]["viewmodel"]
    chunks = viewmodel.get("section_chunks", [])
    return {
        "chunk_mount_map_id": "renderer_chunk_mount_map_1013K_R15",
        "stage": STAGE_ID,
        "source_viewmodel_id": viewmodel["viewmodel_id"],
        "chunk_count": len(chunks),
        "chunks": [
            {
                "chunk_id": chunk["chunk_id"],
                "mount_id": f"chunk-{chunk['chunk_id']}",
                "teacher_label": chunk["teacher_label"],
                "order": chunk["order"],
                "can_update_independently": True,
            }
            for chunk in chunks
        ],
        "progressive_rendering_supported": True,
        "single_chunk_update_supported": True,
        "whole_document_blob_required": False,
        **boundary_flags(),
    }


def _section_html(chunk: dict[str, Any]) -> str:
    paragraphs = "\n".join(f"<p>{html.escape(text)}</p>" for text in chunk.get("paragraphs", []))
    badges = "".join(f"<span>{html.escape(badge)}</span>" for badge in chunk.get("status_badges", []))
    return f"""
      <section class="unit-section" id="chunk-{html.escape(chunk['chunk_id'])}" data-chunk-id="{html.escape(chunk['chunk_id'])}">
        <div class="section-head">
          <span class="number">{html.escape(str(chunk.get('title_number', '')))}</span>
          <h2>{html.escape(chunk.get('teacher_label', ''))}</h2>
          <button>查看说明</button>
        </div>
        <div class="section-body">{paragraphs}</div>
        <div class="badges">{badges}</div>
      </section>
"""


def build_isolated_static_html(root: Path | None = None) -> str:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    viewmodel = sources["r8_response"]["viewmodel"]
    header = viewmodel["header"]
    material_prompt = viewmodel["material_prompt"]
    chunks = viewmodel.get("section_chunks", [])
    status_lights = "".join(
        f"<span class=\"light {html.escape(light['tone'])}\">{html.escape(light['label'])}</span>"
        for light in header.get("status_lights", [])
    )
    material_actions = "".join(f"<button>{html.escape(action)}</button>" for action in material_prompt.get("actions", []))
    nav_items = "".join(
        f"<a href=\"#chunk-{html.escape(chunk['chunk_id'])}\">{html.escape(chunk['title_number'])} {html.escape(chunk['teacher_label'])}</a>"
        for chunk in chunks
    )
    sections = "\n".join(_section_html(chunk) for chunk in chunks)
    fixture_json = html.escape(json.dumps({"viewmodel_id": viewmodel["viewmodel_id"], "chunk_count": len(chunks)}, ensure_ascii=False))
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(header['title'])} · 只读绑定样张</title>
  <style>
    body {{ margin: 0; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #12312d; background: #edf5ed; }}
    .shell {{ max-width: 1120px; margin: 32px auto; padding: 28px 34px 44px; background: #f8fbf3; border: 1px solid rgba(28, 104, 91, .18); border-radius: 18px; }}
    header {{ border-bottom: 1px dashed rgba(28, 104, 91, .22); padding-bottom: 18px; }}
    .eyebrow {{ color: #24796b; font-weight: 700; font-size: 13px; }}
    h1 {{ margin: 8px 0 12px; font-size: 30px; line-height: 1.2; }}
    .status {{ display: flex; gap: 8px; flex-wrap: wrap; }}
    .light {{ display: inline-flex; align-items: center; border: 1px solid rgba(28, 104, 91, .22); border-radius: 999px; padding: 3px 9px; font-size: 12px; background: rgba(255,255,255,.7); }}
    .yellow::before {{ content: ""; width: 7px; height: 7px; border-radius: 50%; background: #d89b2a; margin-right: 5px; }}
    .green::before {{ content: ""; width: 7px; height: 7px; border-radius: 50%; background: #24796b; margin-right: 5px; }}
    .red::before {{ content: ""; width: 7px; height: 7px; border-radius: 50%; background: #b65a52; margin-right: 5px; }}
    .prompt {{ margin: 20px 0 18px; padding: 12px 14px; border: 1px solid #e1b464; border-left: 4px solid #cf8b1f; border-radius: 12px; background: #fff9ea; display: flex; gap: 16px; align-items: center; justify-content: space-between; }}
    .prompt p {{ margin: 0; font-size: 13px; line-height: 1.55; }}
    button {{ border: 1px solid rgba(28, 104, 91, .28); background: #ffffffb8; color: #176557; border-radius: 999px; padding: 6px 10px; font-weight: 700; }}
    .layout {{ display: grid; grid-template-columns: 210px minmax(0, 1fr); gap: 26px; align-items: start; }}
    nav {{ position: sticky; top: 18px; display: flex; flex-direction: column; gap: 6px; font-size: 13px; }}
    nav a {{ color: #176557; text-decoration: none; padding: 7px 9px; border-radius: 10px; }}
    nav a:hover {{ background: rgba(35, 124, 105, .1); }}
    .unit-section {{ border-top: 1px solid rgba(28, 104, 91, .13); padding: 18px 0; }}
    .section-head {{ display: flex; align-items: center; gap: 10px; }}
    .number {{ color: #24796b; font-weight: 800; }}
    h2 {{ margin: 0; font-size: 18px; flex: 1; }}
    .section-body p {{ margin: 9px 0; line-height: 1.8; font-size: 15px; }}
    .badges {{ display: flex; gap: 8px; margin-top: 10px; }}
    .badges span {{ font-size: 12px; color: #55706a; border: 1px solid rgba(28,104,91,.15); border-radius: 999px; padding: 3px 8px; }}
    .fixture-data {{ display: none; }}
  </style>
</head>
<body>
  <main class="shell" data-stage="{STAGE_ID}" data-binding-mode="isolated_static_fixture">
    <header>
      <div class="eyebrow">{html.escape(header['eyebrow'])}</div>
      <h1>{html.escape(header['title'])}</h1>
      <div class="status">{status_lights}</div>
    </header>
    <div class="prompt">
      <p>{html.escape(material_prompt['text'])}</p>
      <div>{material_actions}</div>
    </div>
    <div class="layout">
      <nav aria-label="大单元段落目录">{nav_items}</nav>
      <article>{sections}</article>
    </div>
    <script type="application/json" class="fixture-data">{fixture_json}</script>
  </main>
</body>
</html>
"""


def build_binding_smoke(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    viewmodel = sources["r8_response"]["viewmodel"]
    chunks = viewmodel.get("section_chunks", [])
    html_text = build_isolated_static_html(root)
    return {
        "smoke_id": "isolated_static_frontend_binding_smoke_1013K_R15",
        "stage": STAGE_ID,
        "r14_pass": sources["r14_result"].get("validator_pass") is True,
        "html_created": True,
        "chunk_count": len(chunks),
        "all_chunks_mounted": all(f"chunk-{chunk['chunk_id']}" in html_text for chunk in chunks),
        "teacher_title_visible": viewmodel["header"]["title"] in html_text,
        "material_prompt_visible": viewmodel["material_prompt"]["text"] in html_text,
        "formal_frontend_page_modified": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        **boundary_flags(),
    }


def build_binding_trace(root: Path | None = None) -> dict[str, Any]:
    smoke = build_binding_smoke(root)
    events = [
        {
            "event_id": "r15_event_01_r14_gate_loaded",
            "event_type": "load_r14_frontend_binding_gate",
            "r14_pass": smoke["r14_pass"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r15_event_02_isolated_html_fixture_created",
            "event_type": "render_viewmodel_chunks_to_isolated_static_html",
            "chunk_count": smoke["chunk_count"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r15_event_03_mount_map_created",
            "event_type": "map_chunk_ids_to_static_mount_ids",
            "all_chunks_mounted": smoke["all_chunks_mounted"],
            "side_effects_performed": False,
        },
    ]
    return {
        "trace_id": "isolated_static_frontend_binding_trace_1013K_R15",
        "stage": STAGE_ID,
        "event_count": len(events),
        "events": events,
        "side_effects_performed": False,
        **boundary_flags(),
    }


def build_isolated_static_frontend_readonly_binding_fixture(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "isolated_static_html": build_isolated_static_html(root),
        "renderer_chunk_mount_map": build_renderer_chunk_mount_map(root),
        "binding_smoke": build_binding_smoke(root),
        "binding_trace": build_binding_trace(root),
        "boundary": boundary_flags(),
    }
