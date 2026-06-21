from __future__ import annotations

from copy import deepcopy
from typing import Any

from flask import jsonify, request

from .prep_room_big_unit_readonly_endpoint_dry_run_1013K_R9 import handle_readonly_viewmodel_request


STAGE_ID = "1013K_R11_READONLY_ROUTE_REGISTRATION_STATIC_APPLY_GATED"
ROUTE_PATH = "/api/prep-room/big-unit-preview-viewmodel/<viewmodel_id>"


def _route_boundary() -> dict[str, bool]:
    return {
        "readonly_route_registered": True,
        "route_registered": True,
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
    }


def _route_request(viewmodel_id: str) -> dict[str, Any]:
    return {
        "request_id": "r11_route_request_big_unit_preview_viewmodel",
        "method": request.method,
        "viewmodel_id": viewmodel_id,
        "query": request.args.to_dict(flat=True),
        "expected_response_mode": "readonly_route_registered_preview",
    }


def _annotate_route_response(response: dict[str, Any]) -> dict[str, Any]:
    annotated = deepcopy(response)
    annotated["route_stage"] = STAGE_ID
    annotated["route_path"] = ROUTE_PATH
    annotated["route_registered"] = True
    annotated["readonly_route_registered"] = True
    annotated["runtime_connected"] = False
    annotated["provider_called"] = False
    annotated["model_called"] = False
    annotated["database_written"] = False
    annotated["memory_written"] = False
    annotated["feishu_written"] = False
    annotated["formal_apply_performed"] = False
    boundary = annotated.get("boundary")
    if isinstance(boundary, dict):
        boundary = deepcopy(boundary)
        boundary.update(_route_boundary())
        annotated["boundary"] = boundary
    else:
        annotated["boundary"] = _route_boundary()
    return annotated


def register_routes(bp, cors_preflight):
    @bp.route(ROUTE_PATH, methods=["GET", "OPTIONS"])
    def get_big_unit_preview_viewmodel_route_1013K_R11(viewmodel_id):
        if request.method == "OPTIONS":
            return cors_preflight()
        response = handle_readonly_viewmodel_request(_route_request(viewmodel_id))
        annotated = _annotate_route_response(response)
        return jsonify(annotated), int(annotated.get("status") or 200)
