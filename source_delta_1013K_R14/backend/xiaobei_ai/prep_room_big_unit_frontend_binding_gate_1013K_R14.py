from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R14_FRONTEND_READONLY_RENDER_BINDING_REVIEW_GATE"
INHERITS_FROM = "1013K_M3_READONLY_ROUTE_CLIENT_RENDERER_MILESTONE_PACKAGE"
NEXT_STAGE = "1013K_R15_ISOLATED_STATIC_FRONTEND_READONLY_BINDING_FIXTURE"


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
        "m3_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_M3_readonly_route_client_renderer_milestone_package/1013K_M3_result.json",
        ),
        "r12_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R12_readonly_route_response_contract_and_client_fetch_fixture/1013K_R12_result.json",
        ),
        "r13_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R13_renderer_readonly_fetch_adapter_fixture/1013K_R13_result.json",
        ),
    }
    missing = [str(path) for path in sources.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing R14 frontend binding gate sources: {missing}")
    return {key: _read_json(path) for key, path in sources.items()}


def boundary_flags() -> dict[str, bool]:
    return {
        "frontend_binding_review_gate_only": True,
        "frontend_page_modified": False,
        "main_frontend_mount_allowed": False,
        "isolated_static_binding_allowed_next": True,
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


def build_frontend_surface_inventory(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    frontend_dir = root / "frontend"
    output_root = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    formal_candidates = []
    for name in ["xiaojiao-preview.html", "xiaobei_workbench.html", "home.html"]:
        path = frontend_dir / name
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="ignore")
            formal_candidates.append(
                {
                    "path": str(path.relative_to(root)),
                    "exists": True,
                    "mentions_big_unit": "大单元" in text or "big unit" in text.lower(),
                    "mentions_prep_room": "备课" in text or "prep" in text.lower(),
                    "recommended_for_direct_mount": False,
                }
            )
    static_fixture_candidates = []
    for path in sorted(output_root.glob("**/*.html")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "大单元" in text or "色彩的感觉" in text or "备课室" in text:
            static_fixture_candidates.append(
                {
                    "path": str(path.relative_to(root)),
                    "recommended_for_isolated_binding_fixture": True,
                    "is_output_fixture": True,
                }
            )
        if len(static_fixture_candidates) >= 8:
            break
    return {
        "frontend_surface_inventory_id": "frontend_readonly_render_binding_surface_inventory_1013K_R14",
        "stage": STAGE_ID,
        "formal_frontend_candidates": formal_candidates,
        "formal_frontend_candidate_count": len(formal_candidates),
        "static_fixture_candidates": static_fixture_candidates,
        "static_fixture_candidate_count": len(static_fixture_candidates),
        "formal_frontend_direct_mount_recommended": False,
        "isolated_static_fixture_recommended": True,
        **boundary_flags(),
    }


def build_binding_plan(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    inventory = build_frontend_surface_inventory(root)
    m3_pass = sources["m3_result"].get("validator_pass") is True
    return {
        "binding_plan_id": "frontend_readonly_render_binding_plan_1013K_R14",
        "stage": STAGE_ID,
        "m3_pass": m3_pass,
        "recommended_binding_mode": "isolated_static_fixture_first",
        "main_frontend_mount_allowed": False,
        "isolated_static_binding_allowed_next": m3_pass and inventory["isolated_static_fixture_recommended"],
        "target_route": "/api/prep-room/big-unit-preview-viewmodel/{viewmodel_id}",
        "client_fetch_fixture_source": (
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R12_readonly_route_response_contract_and_client_fetch_fixture/client_fetch_fixture_1013K_R12.js"
        ),
        "renderer_adapter_fixture_source": (
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R13_renderer_readonly_fetch_adapter_fixture/renderer_readonly_fetch_adapter_fixture_1013K_R13.js"
        ),
        "required_next_stage_outputs": [
            "isolated_static_frontend_binding_fixture_html",
            "readonly_fetch_binding_smoke_result",
            "renderer_chunk_mount_map",
            "no_main_frontend_patch_confirmation",
        ],
        "forbidden_next_stage": [
            "modify_frontend_xiaojiao_preview_html",
            "modify_frontend_home_html",
            "connect_provider_or_model",
            "write_database_or_memory_or_feishu",
            "formal_apply",
        ],
        **boundary_flags(),
    }


def build_binding_risk_review(root: Path | None = None) -> dict[str, Any]:
    inventory = build_frontend_surface_inventory(root)
    risks = [
        {
            "risk_id": "r14_risk_formal_frontend_surface_not_yet_selected",
            "severity": "medium",
            "mitigation": "Use isolated static binding fixture before touching formal frontend pages.",
        },
        {
            "risk_id": "r14_risk_static_preview_line_has_many_html_versions",
            "severity": "medium",
            "mitigation": "Bind to a copied fixture and record exact source file instead of patching all HTML variants.",
        },
        {
            "risk_id": "r14_risk_backend_route_registered_but_runtime_not_started",
            "severity": "low",
            "mitigation": "Use Flask test-client or mocked fetch fixture until explicit runtime smoke gate.",
        },
    ]
    return {
        "binding_risk_review_id": "frontend_readonly_render_binding_risk_review_1013K_R14",
        "stage": STAGE_ID,
        "risk_count": len(risks),
        "risks": risks,
        "formal_frontend_candidate_count": inventory["formal_frontend_candidate_count"],
        "static_fixture_candidate_count": inventory["static_fixture_candidate_count"],
        "risk_review_pass": True,
        **boundary_flags(),
    }


def build_frontend_binding_gate(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    plan = build_binding_plan(root)
    inventory = build_frontend_surface_inventory(root)
    risk = build_binding_risk_review(root)
    gate_pass = (
        sources["m3_result"].get("validator_pass") is True
        and sources["r12_result"].get("validator_pass") is True
        and sources["r13_result"].get("validator_pass") is True
        and plan["isolated_static_binding_allowed_next"] is True
        and plan["main_frontend_mount_allowed"] is False
        and risk["risk_review_pass"] is True
    )
    return {
        "frontend_binding_gate_id": "frontend_readonly_render_binding_gate_1013K_R14",
        "stage": STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "m3_pass": sources["m3_result"].get("validator_pass") is True,
        "r12_fetch_contract_pass": sources["r12_result"].get("validator_pass") is True,
        "r13_renderer_adapter_pass": sources["r13_result"].get("validator_pass") is True,
        "frontend_surface_inventory_created": True,
        "binding_plan_created": True,
        "binding_risk_review_created": True,
        "formal_frontend_candidate_count": inventory["formal_frontend_candidate_count"],
        "static_fixture_candidate_count": inventory["static_fixture_candidate_count"],
        "main_frontend_mount_allowed": False,
        "isolated_static_binding_allowed_next": plan["isolated_static_binding_allowed_next"],
        "frontend_binding_gate_pass": gate_pass,
        **boundary_flags(),
    }


def build_binding_trace(root: Path | None = None) -> dict[str, Any]:
    gate = build_frontend_binding_gate(root)
    events = [
        {
            "event_id": "r14_event_01_m3_sources_loaded",
            "event_type": "load_m3_route_client_renderer_milestone",
            "m3_pass": gate["m3_pass"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r14_event_02_frontend_surfaces_inventoried",
            "event_type": "inventory_formal_frontend_and_static_fixture_candidates",
            "formal_frontend_candidate_count": gate["formal_frontend_candidate_count"],
            "static_fixture_candidate_count": gate["static_fixture_candidate_count"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r14_event_03_binding_plan_recorded",
            "event_type": "record_isolated_static_binding_before_formal_frontend_mount",
            "main_frontend_mount_allowed": False,
            "isolated_static_binding_allowed_next": gate["isolated_static_binding_allowed_next"],
            "side_effects_performed": False,
        },
    ]
    return {
        "trace_id": "frontend_readonly_render_binding_gate_trace_1013K_R14",
        "stage": STAGE_ID,
        "event_count": len(events),
        "events": events,
        "side_effects_performed": False,
        **boundary_flags(),
    }


def build_frontend_readonly_render_binding_review_gate(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "frontend_binding_gate": build_frontend_binding_gate(root),
        "frontend_surface_inventory": build_frontend_surface_inventory(root),
        "binding_plan": build_binding_plan(root),
        "binding_risk_review": build_binding_risk_review(root),
        "binding_trace": build_binding_trace(root),
        "boundary": boundary_flags(),
    }
