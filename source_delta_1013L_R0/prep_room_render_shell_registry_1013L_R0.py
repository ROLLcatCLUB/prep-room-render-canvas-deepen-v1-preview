from __future__ import annotations

from copy import deepcopy
from typing import Any

from flask import jsonify, request


STAGE_ID = "1013L_R0_MAIN_RENDER_SHELL_BASELINE_AND_BACKEND_REUSE_REGISTRY"
REGISTRY_ROUTE = "/api/prep-room/render-shell/registry"
STATE_ROUTE = "/api/prep-room/render-shell/state/<state_id>"


def boundary_flags() -> dict[str, bool]:
    return {
        "shell_registry_only": True,
        "render_stage_registry_created": True,
        "backend_reuse_registry_created": True,
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


def agent_profile_policy() -> dict[str, Any]:
    return {
        "policy_id": "unified_renameable_agent_policy_1013L_R0",
        "stage": STAGE_ID,
        "canonical_agent_role": "unified_renameable_agent",
        "default_display_name": "小备",
        "display_name_customizable": True,
        "wake_name_customizable": True,
        "legacy_visible_names": ["小备", "小教"],
        "legacy_backend_roles": ["unified_teacher_agent"],
        "routing_depends_on_display_name": False,
        "routing_key_field": "active_capability",
        "profile_shape": {
            "agent_role": "unified_renameable_agent",
            "assistant_profile": {
                "display_name": "小备",
                "display_name_customizable": True,
                "wake_name": "小备",
                "voice_profile_id": None,
                "tts_enabled": False,
            },
        },
        "migration_rule": (
            "Existing backend payloads that still expose unified_teacher_agent or legacy visible names "
            "must be normalized at the render-shell boundary. Do not use display names as route keys."
        ),
    }


def render_stage_registry() -> dict[str, Any]:
    states = [
        {
            "state_id": "home_scene",
            "teacher_label": "首页场景",
            "render_stage_role": "scene_level_entry",
            "backend_source": "workbench_preview_viewmodel_builder_071B",
            "route_or_adapter": "/api/xiaobei/workbench/preview_viewmodel/dry_run",
            "reuse_action": "reuse_as_shell_scene_viewmodel_safety_base",
            "status": "available_for_shell_mapping",
        },
        {
            "state_id": "prep_notebook",
            "teacher_label": "备课本",
            "render_stage_role": "lesson_notebook_reading_and_preview",
            "backend_source": "prep_room_lesson_reasoning_contract_1013E",
            "route_or_adapter": "existing 1013F/1013E static and reasoning fixtures",
            "reuse_action": "reuse_existing_single_lesson_surface_and_lesson_reasoning_contracts",
            "status": "available_for_static_shell_mapping",
        },
        {
            "state_id": "big_unit_design",
            "teacher_label": "大单元设计",
            "render_stage_role": "big_unit_reading_chunks_and_preview_actions",
            "backend_source": "prep_room_big_unit_render_viewmodel_1013K_R7",
            "route_or_adapter": "/api/prep-room/big-unit-preview-viewmodel/{viewmodel_id}",
            "reuse_action": "reuse_existing_readonly_viewmodel_endpoint_and_chunk_rendering",
            "status": "available_for_shell_mapping",
        },
        {
            "state_id": "single_lesson_design",
            "teacher_label": "单课备课",
            "render_stage_role": "single_lesson_inherits_big_unit_context",
            "backend_source": "prep_room_staged_derivation_pipeline_1013E_R4",
            "route_or_adapter": "local staged derivation pipeline fixture",
            "reuse_action": "reuse_for_lesson_derivation_after_shell_state_packet",
            "status": "needs_thin_shell_adapter",
        },
        {
            "state_id": "courseware_workspace",
            "teacher_label": "课件制作",
            "render_stage_role": "courseware_screen_outline_and_workspace",
            "backend_source": "1013K_R25_to_R29A courseware viewmodel assets",
            "route_or_adapter": "hidden normalized courseware render viewmodel in existing 1013J_R1M page",
            "reuse_action": "reuse_current_viewmodel_normalization_before_visible_render",
            "status": "available_for_shell_mapping_after_R30",
        },
        {
            "state_id": "classroom_display_preview",
            "teacher_label": "大屏预览",
            "render_stage_role": "fullscreen_classroom_display_overlay",
            "backend_source": "1013J_R1M classroom display preview static assets",
            "route_or_adapter": "existing static overlay state",
            "reuse_action": "reuse_overlay_and_screen_ratio_controls",
            "status": "available_for_static_shell_mapping",
        },
        {
            "state_id": "material_intake",
            "teacher_label": "资料补充",
            "render_stage_role": "material_upload_and_text_intake_placeholder",
            "backend_source": "kb_evidence_service and official_unit_field_dictionary_v1",
            "route_or_adapter": "/api/xiaobei/kb/* readonly routes",
            "reuse_action": "reuse_kb_search_and_lesson_resource_routes_later_without_write",
            "status": "needs_upload_gate_before_real_file_intake",
        },
        {
            "state_id": "week_calendar",
            "teacher_label": "周课表",
            "render_stage_role": "schedule_context_for_prep_room",
            "backend_source": "prep_room_feishu_schedule_1013A",
            "route_or_adapter": "/api/xiaobei/prep-room/schedule",
            "reuse_action": "reuse_readonly_schedule_adapter",
            "status": "available_readonly",
        },
    ]
    return {
        "registry_id": "render_stage_registry_1013L_R0",
        "stage": STAGE_ID,
        "shell_shape": {
            "top_shell_persistent": True,
            "render_stage_dynamic": True,
            "bottom_agent_bar_persistent": True,
            "content_pages_are_render_stage_states": True,
            "standalone_static_pages_are_rollback_or_review_artifacts_only": True,
        },
        "state_count": len(states),
        "states": states,
        **boundary_flags(),
    }


def backend_reuse_matrix() -> dict[str, Any]:
    return {
        "matrix_id": "backend_reuse_matrix_1013L_R0",
        "stage": STAGE_ID,
        "reuse_groups": [
            {
                "group_id": "workbench_shell_viewmodel",
                "reuse_now": True,
                "files": [
                    "backend/xiaobei_ai/workbench_preview_viewmodel_builder_071B.py",
                    "backend/xiaobei_ai/workbench_preview_viewmodel_routes_071C.py",
                ],
                "route": "/api/xiaobei/workbench/preview_viewmodel/dry_run",
                "notes": "Use as a safe ViewModel normalizer and gate policy reference for the persistent shell.",
            },
            {
                "group_id": "big_unit_readonly_chunks",
                "reuse_now": True,
                "files": [
                    "backend/xiaobei_ai/prep_room_big_unit_render_viewmodel_1013K_R7.py",
                    "backend/xiaobei_ai/prep_room_big_unit_viewmodel_endpoint_contract_1013K_R8.py",
                    "backend/xiaobei_ai/prep_room_big_unit_readonly_endpoint_dry_run_1013K_R9.py",
                    "backend/xiaobei_ai/prep_room_big_unit_readonly_routes_1013K_R11.py",
                    "backend/xiaobei_ai/prep_room_big_unit_client_fetch_contract_1013K_R12.py",
                    "backend/xiaobei_ai/prep_room_big_unit_renderer_fetch_adapter_1013K_R13.py",
                ],
                "route": "/api/prep-room/big-unit-preview-viewmodel/{viewmodel_id}",
                "notes": "Already supports full viewmodel and single chunk fetch. Reuse for staged rendering.",
            },
            {
                "group_id": "curriculum_and_big_unit_derivation",
                "reuse_now": True,
                "files": [
                    "backend/xiaobei_ai/prep_room_curriculum_standard_derivation_1013K_R0.py",
                    "backend/xiaobei_ai/prep_room_curriculum_derivation_runtime_dry_run_1013K_R1.py",
                    "backend/xiaobei_ai/prep_room_curriculum_profile_candidate_envelope_1013K_R2.py",
                    "backend/xiaobei_ai/prep_room_big_unit_static_section_preview_1013K_R3.py",
                    "backend/xiaobei_ai/prep_room_big_unit_review_surface_1013K_R4.py",
                    "backend/xiaobei_ai/prep_room_big_unit_review_action_state_1013K_R5.py",
                    "backend/xiaobei_ai/prep_room_big_unit_preview_surface_1013K_R6.py",
                ],
                "route": "fixture builders only",
                "notes": "Reuse before adding any new big-unit fields. Do not rewrite this chain.",
            },
            {
                "group_id": "courseware_viewmodel",
                "reuse_now": True,
                "files": [
                    "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/1013K_R25_curriculum_chunk_to_courseware_screen_seed_contract/",
                    "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/1013K_R26_courseware_screen_seed_to_viewmodel_fixture/",
                    "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/1013K_R27_courseware_viewmodel_to_existing_page_hidden_data_injection/",
                    "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/1013K_R29A_courseware_viewmodel_normalization_before_visible_render/",
                ],
                "route": "existing 1013J_R1M hidden viewmodel data",
                "notes": "Promote into shell state after registry. Do not create a new courseware page.",
            },
            {
                "group_id": "knowledge_and_official_unit_sources",
                "reuse_now": True,
                "files": [
                    "docs/contracts/official_unit_field_dictionary_v1.json",
                    "docs/contracts/official_unit_field_prompt_standard_v1.json",
                    "docs/contracts/official_unit_field_question_flow_v1.json",
                    "subject_packs/art/",
                    "business_packs/education/",
                    "knowledge-base/",
                ],
                "route": "/api/xiaobei/kb/* readonly routes where applicable",
                "notes": "Use existing official field and subject-pack assets before defining new big-unit fields.",
            },
        ],
        **boundary_flags(),
    }


def build_shell_baseline_contract() -> dict[str, Any]:
    return {
        "contract_id": "main_render_shell_baseline_contract_1013L_R0",
        "stage": STAGE_ID,
        "purpose": "Lock the prep-room work into one persistent shell with dynamic RenderStage states and reusable backend viewmodels.",
        "source_backup": {
            "snapshot": "Z:/SmartEdu_Backups/xiaobei-core/full_snapshot_20260621_125633",
            "note": "Z:/SmartEdu_Backups/xiaobei-core/SNAPSHOT_20260621_125633_BEFORE_1013L.md",
        },
        "persistent_shell": {
            "top_menu": "persistent",
            "render_stage": "dynamic_state_container",
            "bottom_agent_input": "persistent",
            "resident_agent": agent_profile_policy(),
        },
        "page_rule": {
            "canonical_main_page_required_before_more_feature_lines": True,
            "new_static_pages_allowed_only_as_backup_or_review_copy": True,
            "future_features_must_target_render_stage_state": True,
            "do_not_rewrite_existing_backend_chains": True,
        },
        "render_stage_registry": render_stage_registry(),
        "backend_reuse_matrix": backend_reuse_matrix(),
        **boundary_flags(),
    }


def build_render_shell_state_registry_response() -> dict[str, Any]:
    return {
        "ok": True,
        "stage": STAGE_ID,
        "contract": build_shell_baseline_contract(),
        "registry": render_stage_registry(),
        "backend_reuse_matrix": backend_reuse_matrix(),
        "agent_profile_policy": agent_profile_policy(),
        "boundary": boundary_flags(),
    }


def get_render_stage_state(state_id: str) -> dict[str, Any]:
    registry = render_stage_registry()
    for state in registry["states"]:
        if state["state_id"] == state_id:
            return {
                "ok": True,
                "stage": STAGE_ID,
                "state": deepcopy(state),
                "agent_profile_policy": agent_profile_policy(),
                "boundary": boundary_flags(),
            }
    return {
        "ok": False,
        "stage": STAGE_ID,
        "status": 404,
        "error_code": "RENDER_STAGE_STATE_NOT_FOUND",
        "teacher_visible_message": "没有找到这个工作状态，可以回到备课室首页重新选择。",
        "boundary": boundary_flags(),
    }


def register_routes(bp, cors_preflight):
    @bp.route(REGISTRY_ROUTE, methods=["GET", "OPTIONS"])
    def prep_room_render_shell_registry_route_1013L_R0():
        if request.method == "OPTIONS":
            return cors_preflight()
        return jsonify(build_render_shell_state_registry_response()), 200

    @bp.route(STATE_ROUTE, methods=["GET", "OPTIONS"])
    def prep_room_render_shell_state_route_1013L_R0(state_id):
        if request.method == "OPTIONS":
            return cors_preflight()
        response = get_render_stage_state(state_id)
        return jsonify(response), int(response.get("status") or 200)
