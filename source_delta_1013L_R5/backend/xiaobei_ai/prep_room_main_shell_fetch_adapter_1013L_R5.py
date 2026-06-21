from __future__ import annotations

from copy import deepcopy
from typing import Any

from flask import jsonify, request

from . import prep_room_render_shell_registry_1013L_R0


STAGE_ID = "1013L_R5_MAIN_SHELL_BACKEND_VIEWMODEL_READONLY_FETCH_ADAPTER"
VIEWMODEL_ROUTE = "/api/prep-room/main-shell/viewmodel"
STATE_VIEWMODEL_ROUTE = "/api/prep-room/main-shell/viewmodel/state/<state_id>"


def boundary_flags() -> dict[str, bool]:
    return {
        "readonly_fetch_adapter_only": True,
        "formal_frontend_binding_allowed": False,
        "new_disconnected_page_created": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
    }


def normalized_agent_profile() -> dict[str, Any]:
    policy = prep_room_render_shell_registry_1013L_R0.agent_profile_policy()
    return {
        "agent_role": "unified_renameable_agent",
        "assistant_profile": {
            "display_name": policy["default_display_name"],
            "display_name_customizable": True,
            "wake_name": policy["default_display_name"],
            "wake_name_customizable": True,
            "voice_profile_id": None,
            "tts_enabled": False,
        },
        "routing": {
            "routing_depends_on_display_name": False,
            "routing_key_field": "active_capability",
            "legacy_visible_names": policy["legacy_visible_names"],
            "legacy_backend_roles": policy["legacy_backend_roles"],
        },
    }


def state_fetch_adapters() -> list[dict[str, Any]]:
    return [
        {
            "state_id": "home_scene",
            "teacher_label": "开始",
            "active_capability": "prep_room_home",
            "render_slot": "stage_body",
            "readonly_endpoint": "/api/prep-room/main-shell/viewmodel/state/home_scene",
            "source_endpoint": "/api/xiaobei/workbench/preview_viewmodel/dry_run",
            "source_fixture": "embedded_shell_home_scene",
            "fetch_policy": "readonly_or_static_fallback",
            "adapter_status": "ready_for_shell_fetch",
        },
        {
            "state_id": "big_unit_design",
            "teacher_label": "大单元",
            "active_capability": "big_unit_design",
            "render_slot": "stage_body",
            "readonly_endpoint": "/api/prep-room/main-shell/viewmodel/state/big_unit_design",
            "source_endpoint": "/api/prep-room/big-unit-preview-viewmodel/big_unit_render_viewmodel_fixture_1013K_R7",
            "source_fixture": "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/1013K_R8_big_unit_render_viewmodel_readonly_endpoint_contract/big_unit_render_viewmodel_readonly_response_fixture_1013K_R8.json",
            "fetch_policy": "prefer_existing_readonly_endpoint_then_fixture",
            "adapter_status": "ready_for_shell_fetch",
        },
        {
            "state_id": "single_lesson_design",
            "teacher_label": "单课",
            "active_capability": "single_lesson_prep",
            "render_slot": "stage_body",
            "readonly_endpoint": "/api/prep-room/main-shell/viewmodel/state/single_lesson_design",
            "source_endpoint": None,
            "source_fixture": "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/1013F_R2C_RESTORED_single_lesson_teaching_design_surface/prep_room_render_canvas_deepen_v1_RESTORED_1013F_R2C_single_lesson_teaching_design.html",
            "fetch_policy": "static_surface_fallback_until_lesson_viewmodel_route",
            "adapter_status": "static_fallback_ready",
        },
        {
            "state_id": "courseware_workspace",
            "teacher_label": "课件",
            "active_capability": "courseware_workspace",
            "render_slot": "stage_body",
            "readonly_endpoint": "/api/prep-room/main-shell/viewmodel/state/courseware_workspace",
            "source_endpoint": None,
            "source_fixture": "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/1013K_R29A_courseware_viewmodel_normalization_before_visible_render/normalized_courseware_render_viewmodel_1013K_R29A.json",
            "fetch_policy": "fixture_fallback_until_courseware_route",
            "adapter_status": "ready_for_shell_fetch",
        },
        {
            "state_id": "classroom_display_preview",
            "teacher_label": "大屏",
            "active_capability": "classroom_display_preview",
            "render_slot": "stage_overlay",
            "readonly_endpoint": "/api/prep-room/main-shell/viewmodel/state/classroom_display_preview",
            "source_endpoint": None,
            "source_fixture": "1013J_R1M display overlay state embedded in shell",
            "fetch_policy": "reuse_shell_courseware_screen_viewmodel",
            "adapter_status": "ready_for_shell_fetch",
        },
        {
            "state_id": "material_intake",
            "teacher_label": "资料",
            "active_capability": "material_intake",
            "render_slot": "stage_body",
            "readonly_endpoint": "/api/prep-room/main-shell/viewmodel/state/material_intake",
            "source_endpoint": "/api/xiaobei/kb/*",
            "source_fixture": "docs/contracts/official_unit_field_dictionary_v1.json",
            "fetch_policy": "placeholder_until_upload_gate",
            "adapter_status": "placeholder_ready",
        },
        {
            "state_id": "week_calendar",
            "teacher_label": "周课表",
            "active_capability": "schedule_context",
            "render_slot": "stage_body",
            "readonly_endpoint": "/api/prep-room/main-shell/viewmodel/state/week_calendar",
            "source_endpoint": "/api/xiaobei/prep-room/schedule",
            "source_fixture": "backend/xiaobei_ai/prep_room_feishu_schedule_1013A.py",
            "fetch_policy": "reuse_existing_readonly_schedule_route",
            "adapter_status": "ready_for_shell_fetch",
        },
    ]


def adapter_map() -> dict[str, Any]:
    adapters = state_fetch_adapters()
    return {
        "adapter_map_id": "main_shell_state_fetch_adapter_map_1013L_R5",
        "stage": STAGE_ID,
        "state_count": len(adapters),
        "states": adapters,
        "agent_profile": normalized_agent_profile(),
        "boundary": boundary_flags(),
    }


def contract() -> dict[str, Any]:
    return {
        "contract_id": "main_shell_backend_viewmodel_fetch_contract_1013L_R5",
        "stage": STAGE_ID,
        "purpose": "Expose a readonly main-shell ViewModel adapter that lets the persistent shell fetch existing surface sources as RenderStage states.",
        "canonical_shell": "1013L_M1_canonical_main_shell_milestone/shiwei_main_render_shell_1013L_M1.html",
        "routes": {
            "full_shell_viewmodel": VIEWMODEL_ROUTE,
            "state_viewmodel": STATE_VIEWMODEL_ROUTE,
        },
        "reuse_policy": {
            "do_not_rewrite_existing_backend_chains": True,
            "do_not_create_disconnected_page_line": True,
            "prefer_existing_readonly_routes": True,
            "fixture_fallback_allowed": True,
            "formal_frontend_binding_deferred": True,
        },
        "state_fetch_adapter_map": adapter_map(),
        "boundary": boundary_flags(),
    }


def build_main_shell_viewmodel_response() -> dict[str, Any]:
    registry = prep_room_render_shell_registry_1013L_R0.render_stage_registry()
    return {
        "ok": True,
        "stage": STAGE_ID,
        "viewmodel_id": "main_shell_viewmodel_1013L_R5",
        "viewmodel_type": "prep_room_main_render_shell",
        "shell": {
            "top_shell_persistent": True,
            "render_stage_dynamic": True,
            "bottom_agent_bar_persistent": True,
            "content_pages_are_render_stage_states": True,
        },
        "agent_profile": normalized_agent_profile(),
        "render_stage_registry": registry,
        "fetch_adapter_map": adapter_map(),
        "boundary": boundary_flags(),
    }


def get_state_viewmodel(state_id: str) -> dict[str, Any]:
    adapters = {item["state_id"]: item for item in state_fetch_adapters()}
    adapter = adapters.get(state_id)
    if adapter is None:
        return {
            "ok": False,
            "stage": STAGE_ID,
            "status": 404,
            "error_code": "MAIN_SHELL_STATE_VIEWMODEL_NOT_FOUND",
            "teacher_visible_message": "没有找到这个工作状态，可以回到备课室重新选择。",
            "boundary": boundary_flags(),
        }
    state_response = prep_room_render_shell_registry_1013L_R0.get_render_stage_state(state_id)
    return {
        "ok": True,
        "stage": STAGE_ID,
        "viewmodel_id": f"main_shell_state_viewmodel_{state_id}_1013L_R5",
        "state_id": state_id,
        "state": deepcopy(state_response.get("state") or {}),
        "fetch_adapter": deepcopy(adapter),
        "agent_profile": normalized_agent_profile(),
        "boundary": boundary_flags(),
    }


def register_routes(bp, cors_preflight):
    @bp.route(VIEWMODEL_ROUTE, methods=["GET", "OPTIONS"])
    def prep_room_main_shell_viewmodel_route_1013L_R5():
        if request.method == "OPTIONS":
            return cors_preflight()
        return jsonify(build_main_shell_viewmodel_response()), 200

    @bp.route(STATE_VIEWMODEL_ROUTE, methods=["GET", "OPTIONS"])
    def prep_room_main_shell_state_viewmodel_route_1013L_R5(state_id):
        if request.method == "OPTIONS":
            return cors_preflight()
        response = get_state_viewmodel(state_id)
        return jsonify(response), int(response.get("status") or 200)
