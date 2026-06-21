from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R10_READONLY_ROUTE_REGISTRATION_REVIEW_GATE"
INHERITS_FROM = "1013K_R9_BIG_UNIT_READONLY_ENDPOINT_DRY_RUN_WITHOUT_ROUTE_REGISTRATION"
NEXT_STAGE = "1013K_R11_READONLY_ROUTE_REGISTRATION_STATIC_APPLY_GATED"
PROPOSED_PUBLIC_PATH = "/api/prep-room/big-unit-preview-viewmodel/{viewmodel_id}"
PROPOSED_FLASK_PATH = "/api/prep-room/big-unit-preview-viewmodel/<viewmodel_id>"


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
        "r9_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R9_big_unit_readonly_endpoint_dry_run_without_route_registration/"
            "1013K_R9_result.json",
        ),
        "r9_request_fixture": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R9_big_unit_readonly_endpoint_dry_run_without_route_registration/"
            "big_unit_readonly_endpoint_request_fixture_1013K_R9.json",
        ),
        "routes_py": root / "backend" / "xiaobei_ai" / "routes.py",
    }
    missing = [str(path) for path in sources.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing route-registration gate sources: {missing}")
    return {key: _read_json(path) if path.suffix == ".json" else path.read_text(encoding="utf-8") for key, path in sources.items()}


def boundary_flags() -> dict[str, bool]:
    return {
        "route_registration_review_gate_only": True,
        "route_registration_allowed_after_gate": True,
        "route_registered": False,
        "routes_py_modified": False,
        "route_module_created": False,
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


def _route_files(root: Path) -> list[Path]:
    route_dir = root / "backend" / "xiaobei_ai"
    return sorted(route_dir.glob("*routes*.py")) + [route_dir / "routes.py"]


def build_route_collision_review(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    route_files = []
    matched_existing_routes = []
    for path in _route_files(root):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        route_files.append(str(path.relative_to(root)))
        if "big-unit-preview-viewmodel" in text or "big_unit_preview_viewmodel" in text:
            matched_existing_routes.append(
                {
                    "path": str(path.relative_to(root)),
                    "matched_terms": [
                        term
                        for term in ["big-unit-preview-viewmodel", "big_unit_preview_viewmodel"]
                        if term in text
                    ],
                }
            )
    return {
        "collision_review_id": "readonly_route_collision_review_1013K_R10",
        "stage": STAGE_ID,
        "reviewed_route_files": route_files,
        "reviewed_route_file_count": len(route_files),
        "proposed_public_path": PROPOSED_PUBLIC_PATH,
        "proposed_flask_path": PROPOSED_FLASK_PATH,
        "matched_existing_routes": matched_existing_routes,
        "route_collision_detected": bool(matched_existing_routes),
        "collision_review_pass": not matched_existing_routes,
        **boundary_flags(),
        **profile(),
    }


def build_route_mount_plan(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    _load_sources(root)
    return {
        "mount_plan_id": "readonly_route_mount_plan_1013K_R10",
        "stage": STAGE_ID,
        "future_route_module": "backend/xiaobei_ai/prep_room_big_unit_readonly_routes_1013K_R11.py",
        "future_import_line": "from . import prep_room_big_unit_readonly_routes_1013K_R11",
        "future_register_line": "prep_room_big_unit_readonly_routes_1013K_R11.register_routes(bp, _cors_preflight)",
        "future_handler_import": (
            "from .prep_room_big_unit_readonly_endpoint_dry_run_1013K_R9 "
            "import handle_readonly_viewmodel_request"
        ),
        "endpoint_function": "get_big_unit_preview_viewmodel_route",
        "proposed_public_path": PROPOSED_PUBLIC_PATH,
        "proposed_flask_path": PROPOSED_FLASK_PATH,
        "proposed_methods": ["GET", "OPTIONS"],
        "cors_preflight_required": True,
        "cors_preflight_function": "_cors_preflight",
        "readonly_handler_source": "prep_room_big_unit_readonly_endpoint_dry_run_1013K_R9.handle_readonly_viewmodel_request",
        "response_source_stage": "1013K_R9_BIG_UNIT_READONLY_ENDPOINT_DRY_RUN_WITHOUT_ROUTE_REGISTRATION",
        "route_registration_allowed_next": True,
        "route_registration_performed": False,
        "routes_py_patch_allowed_next": True,
        "routes_py_patch_performed": False,
        **boundary_flags(),
        **profile(),
    }


def build_route_registration_gate(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    collision = build_route_collision_review(root)
    mount_plan = build_route_mount_plan(root)
    r9_pass = (
        sources["r9_result"].get("final_status")
        == "PASS_1013K_R9_BIG_UNIT_READONLY_ENDPOINT_DRY_RUN_WITHOUT_ROUTE_REGISTRATION"
        and sources["r9_result"].get("validator_pass") is True
    )
    request_count = sources["r9_request_fixture"].get("request_count")
    gate_pass = (
        r9_pass
        and request_count == 3
        and collision["collision_review_pass"] is True
        and "GET" in mount_plan["proposed_methods"]
        and "OPTIONS" in mount_plan["proposed_methods"]
        and mount_plan["cors_preflight_required"] is True
    )
    return {
        "route_registration_gate_id": "readonly_route_registration_gate_1013K_R10",
        "stage": STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "r9_pass": r9_pass,
        "r9_request_fixture_loaded": True,
        "r9_request_count": request_count,
        "existing_routes_reviewed": True,
        "route_collision_detected": collision["route_collision_detected"],
        "collision_review_pass": collision["collision_review_pass"],
        "route_module_plan_created": True,
        "cors_preflight_plan_created": True,
        "proposed_public_path": PROPOSED_PUBLIC_PATH,
        "proposed_flask_path": PROPOSED_FLASK_PATH,
        "proposed_methods": mount_plan["proposed_methods"],
        "route_registration_gate_pass": gate_pass,
        "route_registration_allowed_next": gate_pass,
        "routes_py_patch_allowed_next": gate_pass,
        "route_registration_performed": False,
        "routes_py_patch_performed": False,
        **boundary_flags(),
        **profile(),
    }


def build_route_registration_trace(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    collision = build_route_collision_review(root)
    mount_plan = build_route_mount_plan(root)
    gate = build_route_registration_gate(root)
    events = [
        {
            "event_id": "r10_event_01_r9_sources_loaded",
            "event_type": "load_r9_endpoint_dry_run_sources",
            "r9_pass": gate["r9_pass"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r10_event_02_existing_routes_reviewed",
            "event_type": "review_existing_xiaobei_ai_route_files_for_collision",
            "reviewed_route_file_count": collision["reviewed_route_file_count"],
            "route_collision_detected": collision["route_collision_detected"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r10_event_03_future_mount_plan_created",
            "event_type": "create_future_route_module_import_and_register_plan",
            "future_route_module": mount_plan["future_route_module"],
            "route_registration_performed": False,
            "side_effects_performed": False,
        },
        {
            "event_id": "r10_event_04_gate_decision_recorded",
            "event_type": "record_route_registration_review_gate_decision_without_applying",
            "route_registration_gate_pass": gate["route_registration_gate_pass"],
            "next_stage": NEXT_STAGE,
            "side_effects_performed": False,
        },
    ]
    return {
        "trace_id": "readonly_route_registration_trace_1013K_R10",
        "stage": STAGE_ID,
        "event_count": len(events),
        "events": events,
        "side_effects_performed": False,
        **boundary_flags(),
        **profile(),
    }


def build_readonly_route_registration_review_gate(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "route_registration_gate": build_route_registration_gate(root),
        "route_mount_plan": build_route_mount_plan(root),
        "route_collision_review": build_route_collision_review(root),
        "route_registration_trace": build_route_registration_trace(root),
        "boundary": boundary_flags(),
    }
