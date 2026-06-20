from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R0_CURRICULUM_STANDARD_DERIVATION_BACKEND_CONTRACT"


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
        "r6c_control_contract": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013I_R6C_curriculum_standard_control_layer_contract/"
            "curriculum_standard_control_layer_contract_1013I_R6C.json",
        ),
        "r6c_control_fixture": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013I_R6C_curriculum_standard_control_layer_contract/"
            "curriculum_standard_control_fixture_1013I_R6C.json",
        ),
        "r6c_priority_matrix": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013I_R6C_curriculum_standard_control_layer_contract/"
            "curriculum_standard_priority_matrix_1013I_R6C.json",
        ),
        "r6d_textbook_chain_contract": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013I_R6D_textbook_anchor_and_big_unit_design_chain_contract/"
            "textbook_anchor_and_big_unit_design_chain_contract_1013I_R6D.json",
        ),
        "r6e_textbook_anchor_candidates": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013I_R6E_official_unit_material_readonly_extraction_fixture/"
            "textbook_anchor_candidates_1013I_R6E.json",
        ),
        "r6e_big_unit_chain_candidates": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013I_R6E_official_unit_material_readonly_extraction_fixture/"
            "big_unit_chain_candidates_1013I_R6E.json",
        ),
        "official_unit_field_dictionary_v1": _source_path(
            root,
            "docs/contracts/official_unit_field_dictionary_v1.json",
        ),
    }
    missing = [str(path) for path in sources.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing curriculum derivation sources: {missing}")
    return {key: _read_json(path) for key, path in sources.items()}


def boundary_flags() -> dict[str, bool]:
    return {
        "backend_contract_only": True,
        "backend_adapter_fixture_only": True,
        "preview_only": True,
        "runtime_schema_applied": False,
        "real_curriculum_standard_full_text_parsed": False,
        "full_standard_text_stored": False,
        "full_standard_text_dumped_to_prompt": False,
        "official_curriculum_claim_created": False,
        "textbook_anchor_verified": False,
        "unit_package_written": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "product_runtime_called": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "official_export_created": False,
        "official_archive_created": False,
        "main_project_pushed": False,
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


def build_curriculum_standard_slice_schema(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    control_contract = sources["r6c_control_contract"]
    return {
        "schema_id": "curriculum_standard_slice_schema_1013K_R0",
        "stage": STAGE_ID,
        "inherits_from": "1013I_R6C_CURRICULUM_STANDARD_CONTROL_LAYER_CONTRACT",
        "schema_role": "store_small_structured_standard_slices_for_derivation_control",
        "source_policy": {
            "full_standard_text_stored": False,
            "full_standard_text_dumped_to_prompt": False,
            "structured_refs_required": True,
            "teacher_supplied_ref_allowed": True,
            "official_claim_created": False,
        },
        "required_fields": [
            "slice_id",
            "standard_version_label",
            "subject",
            "school_stage",
            "grade_band",
            "learning_domain",
            "core_literacy_tags",
            "learning_task_direction",
            "assessment_evidence_direction",
            "content_scope_boundary",
            "prohibited_overreach",
            "source_ref_ids",
            "source_quote_policy",
            "confidence",
            "status",
        ],
        "status_enum": [
            "missing_structured_ref",
            "candidate_from_known_control_profile",
            "teacher_confirmed_ref_mapping",
            "needs_manual_standard_review",
        ],
        "slice_examples": [
            {
                "slice_id": "art_g3_4_color_expression_direction_candidate",
                "standard_version_label": "义务教育艺术课程标准方向候选",
                "subject": "美术",
                "school_stage": "小学",
                "grade_band": "3-4",
                "learning_domain": "造型表现 / 欣赏评述 / 综合探索",
                "core_literacy_tags": ["审美感知", "艺术表现", "创意实践", "文化理解"],
                "learning_task_direction": ["观察", "比较", "表现", "交流", "修订"],
                "assessment_evidence_direction": [
                    "能说出色彩带来的感受",
                    "能说明选色理由",
                    "作品呈现较明确视觉意味",
                    "能根据反馈调整一处颜色",
                ],
                "content_scope_boundary": "三年级色彩感受与表达，避免越级进入复杂色彩理论。",
                "prohibited_overreach": [
                    "不得要求三年级学生掌握成人化色彩理论术语",
                    "不得把官方案例样本文字当成课标原文",
                    "不得在缺教材锚点时生成正式单课正文",
                ],
                "source_ref_ids": ["curriculum_standard_control_layer_1013I_R6C"],
                "source_quote_policy": "no_full_text_quote",
                "confidence": "candidate_pending_teacher_or_standard_ref",
                "status": "candidate_from_known_control_profile",
            }
        ],
        "linked_r6c_required_control_fields": [
            field["field"] for field in control_contract.get("required_control_fields", [])
        ],
        **boundary_flags(),
        **profile(),
    }


def build_curriculum_control_profile_schema(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    return {
        "schema_id": "curriculum_control_profile_schema_1013K_R0",
        "stage": STAGE_ID,
        "schema_role": "compose_standard_slices_into_a_generation_control_profile",
        "profile_object": "curriculum_control_profile",
        "required_inputs": [
            "teacher_self_prep_request",
            "curriculum_standard_slices",
            "textbook_anchor_candidate_or_confirmed_anchor",
            "big_unit_chain_candidate_or_confirmed_chain",
        ],
        "required_output_fields": [
            "profile_id",
            "subject",
            "grade_band",
            "core_literacy_focus",
            "learning_task_direction",
            "assessment_evidence_direction",
            "allowed_generation_scope",
            "blocked_generation_scope",
            "teacher_confirmation_required_items",
            "degraded_preview_policy",
            "source_refs",
        ],
        "priority_rule": [
            "curriculum_standard_control_layer",
            "textbook_anchor",
            "big_unit_design_chain",
            "official_case_reference",
            "teacher_input",
            "model_candidate",
        ],
        "normal_generation_gate": {
            "requires_curriculum_standard_control_profile": True,
            "requires_textbook_anchor": True,
            "requires_big_unit_chain": True,
            "requires_teacher_confirmation": True,
            "allows_candidate_generation_after_gates": True,
            "allows_formal_apply": False,
        },
        "conflict_resolution": {
            "official_case_vs_curriculum_standard": "use_curriculum_standard_control_profile_and_keep_case_reference_only",
            "teacher_input_vs_standard_boundary": "ask_teacher_to_revise_or_enter_labeled_degraded_preview",
            "model_candidate_vs_textbook_anchor": "reject_or_mark_for_teacher_review",
        },
        "source_contract_refs": {
            "r6c_control_contract": sources["r6c_control_contract"]["contract_id"],
            "r6d_textbook_chain_contract": sources["r6d_textbook_chain_contract"]["contract_id"],
        },
        **boundary_flags(),
        **profile(),
    }


def build_curriculum_to_big_unit_derivation_contract(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    return {
        "contract_id": "curriculum_to_big_unit_derivation_contract_1013K_R0",
        "stage": STAGE_ID,
        "contract_role": "derive_big_unit_design_candidates_from_curriculum_control_without_generating_final_lesson_body",
        "upstream_chain": [
            "teacher_input",
            "curriculum_standard_slice_selection",
            "curriculum_control_profile",
            "textbook_anchor_check",
            "big_unit_chain_check",
            "lesson_position_judgement",
            "teacher_confirmation",
            "candidate_generation_preview_only",
        ],
        "derivation_targets": [
            "curriculum_basis",
            "core_literacy_goals",
            "student_starting_point",
            "unit_questions",
            "knowledge_and_skills",
            "performance_task",
            "learning_progression",
            "lesson_task_chain",
            "assessment_evidence",
            "materials_and_scaffolds",
        ],
        "blocked_targets_before_confirmation": [
            "formal_unit_package",
            "formal_single_lesson_body",
            "database_record",
            "memory_record",
            "feishu_writeback",
            "official_export",
        ],
        "required_gates": {
            "curriculum_standard_as_control_layer": True,
            "textbook_anchor_required": sources["r6d_textbook_chain_contract"].get("textbook_anchor_required") is True,
            "big_unit_design_chain_required": sources["r6d_textbook_chain_contract"].get("big_unit_design_chain_defined")
            is True,
            "teacher_confirmation_required": True,
            "official_case_reference_only": sources["r6c_control_contract"]
            .get("relation_to_official_case_reference", {})
            .get("official_cases_are_reference_only")
            is True,
        },
        "generation_policy": {
            "candidate_only": True,
            "teacher_review_required": True,
            "preview_only": True,
            "normal_candidate_generation_blocked_without_textbook_anchor": True,
            "normal_candidate_generation_blocked_without_big_unit_chain": True,
            "normal_candidate_generation_blocked_without_curriculum_profile": True,
        },
        **boundary_flags(),
        **profile(),
    }


def build_curriculum_derivation_trace_fixture(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    slice_schema = build_curriculum_standard_slice_schema(root)
    control_profile_schema = build_curriculum_control_profile_schema(root)
    textbook_candidates = sources["r6e_textbook_anchor_candidates"].get("candidates", [])
    chain_candidate = sources["r6e_big_unit_chain_candidates"].get("unit_package_candidate", {})
    return {
        "trace_id": "curriculum_derivation_trace_fixture_1013K_R0_color_feeling",
        "stage": STAGE_ID,
        "trace_role": "show_how_backend_should_reason_from_standard_control_to_big_unit_candidates",
        "teacher_request": {
            "subject": "美术",
            "grade": "三年级",
            "semester": "第二学期",
            "unit_title": "多变的色彩",
            "lesson_title": "色彩的感觉",
            "request_type": "big_unit_then_single_lesson_prep",
        },
        "trace_steps": [
            {
                "step_id": "01_select_curriculum_standard_slices",
                "input_refs": ["curriculum_standard_control_layer_1013I_R6C"],
                "output_object": "curriculum_standard_slices",
                "status": "candidate_pending_teacher_or_standard_ref",
                "notes": [
                    "Only structured direction slices are selected.",
                    "Full curriculum-standard text is not stored or dumped to prompts.",
                ],
            },
            {
                "step_id": "02_build_curriculum_control_profile",
                "input_refs": ["curriculum_standard_slices", "teacher_self_prep_request"],
                "output_object": "curriculum_control_profile",
                "status": "profile_candidate_created",
                "core_literacy_focus": slice_schema["slice_examples"][0]["core_literacy_tags"],
                "learning_task_direction": slice_schema["slice_examples"][0]["learning_task_direction"],
                "assessment_evidence_direction": slice_schema["slice_examples"][0][
                    "assessment_evidence_direction"
                ],
            },
            {
                "step_id": "03_check_textbook_anchor",
                "input_refs": ["textbook_anchor_candidates_1013I_R6E"],
                "output_object": "textbook_anchor_gate",
                "candidate_count": len(textbook_candidates),
                "status": "pending_teacher_confirm",
                "normal_generation_allowed": False,
            },
            {
                "step_id": "04_check_big_unit_chain",
                "input_refs": ["big_unit_chain_candidates_1013I_R6E"],
                "output_object": "big_unit_chain_gate",
                "candidate_chain_status": chain_candidate.get("chain_status"),
                "status": "pending_teacher_confirm",
                "normal_generation_allowed": False,
            },
            {
                "step_id": "05_prepare_big_unit_derivation_targets",
                "input_refs": ["curriculum_control_profile", "textbook_anchor_gate", "big_unit_chain_gate"],
                "output_object": "big_unit_derivation_target_map",
                "target_fields": build_curriculum_to_big_unit_derivation_contract(root)["derivation_targets"],
                "status": "candidate_targets_ready_for_teacher_review",
                "writes_unit_package": False,
                "writes_lesson_body": False,
            },
        ],
        "control_profile_candidate": {
            "profile_id": "curriculum_control_profile_color_feeling_1013K_R0",
            "subject": "美术",
            "grade_band": "3-4",
            "core_literacy_focus": ["审美感知", "艺术表现", "创意实践", "文化理解"],
            "learning_task_direction": ["观察", "比较", "表现", "交流", "修订"],
            "allowed_generation_scope": [
                "大单元设计候选",
                "课时任务链候选",
                "单课继承提示候选",
                "教师审阅卡候选",
            ],
            "blocked_generation_scope": [
                "正式大单元正文写入",
                "正式单课正文写入",
                "数据库保存",
                "记忆写入",
                "飞书写回",
            ],
            "source_refs": [
                "curriculum_standard_control_layer_1013I_R6C",
                "textbook_anchor_candidates_1013I_R6E",
                "big_unit_chain_candidates_1013I_R6E",
            ],
            "teacher_confirmation_required": True,
            "degraded_preview_policy": "allowed_only_with_visible_degraded_label",
        },
        "schemas_used": [
            slice_schema["schema_id"],
            control_profile_schema["schema_id"],
            "curriculum_to_big_unit_derivation_contract_1013K_R0",
        ],
        **boundary_flags(),
        **profile(),
    }


def build_curriculum_standard_derivation_backend_contract(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "curriculum_standard_slice_schema": build_curriculum_standard_slice_schema(root),
        "curriculum_control_profile_schema": build_curriculum_control_profile_schema(root),
        "curriculum_to_big_unit_derivation_contract": build_curriculum_to_big_unit_derivation_contract(root),
        "curriculum_derivation_trace_fixture": build_curriculum_derivation_trace_fixture(root),
        "boundary": boundary_flags(),
    }
