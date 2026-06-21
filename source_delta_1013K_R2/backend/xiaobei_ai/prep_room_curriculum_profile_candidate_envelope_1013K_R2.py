from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R2_CURRICULUM_PROFILE_TO_BIG_UNIT_CANDIDATE_ENVELOPE"


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
        "r1_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R1_curriculum_derivation_profile_runtime_dry_run/1013K_R1_result.json",
        ),
        "r1_runtime_state": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R1_curriculum_derivation_profile_runtime_dry_run/"
            "curriculum_derivation_runtime_state_1013K_R1.json",
        ),
        "r1_gate_decision": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R1_curriculum_derivation_profile_runtime_dry_run/"
            "curriculum_derivation_gate_decision_1013K_R1.json",
        ),
        "r1_target_map": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R1_curriculum_derivation_profile_runtime_dry_run/"
            "curriculum_derivation_target_map_1013K_R1.json",
        ),
        "r6e_teacher_confirmation_items": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013I_R6E_official_unit_material_readonly_extraction_fixture/"
            "teacher_confirmation_required_items_1013I_R6E.json",
        ),
    }
    missing = [str(path) for path in sources.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing curriculum candidate envelope sources: {missing}")
    return {key: _read_json(path) for key, path in sources.items()}


def boundary_flags() -> dict[str, bool]:
    return {
        "candidate_envelope_only": True,
        "prompt_envelope_only": True,
        "degraded_preview_only": True,
        "preview_only": True,
        "normal_candidate_generation_allowed": False,
        "provider_called": False,
        "model_called": False,
        "candidate_text_generated": False,
        "unit_package_written": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "runtime_schema_applied": False,
        "full_standard_text_dumped_to_prompt": False,
        "official_curriculum_claim_created": False,
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


TARGET_LABELS = {
    "curriculum_basis": "课标依据",
    "core_literacy_goals": "核心素养",
    "student_starting_point": "学生起点",
    "unit_questions": "单元问题",
    "knowledge_and_skills": "知识与技能",
    "performance_task": "表现任务",
    "learning_progression": "学习推进",
    "lesson_task_chain": "课时任务链",
    "assessment_evidence": "评价证据",
    "materials_and_scaffolds": "材料与支架",
}


TARGET_INTENTS = {
    "curriculum_basis": "把课标方向转成教师可读的单元依据，不引用或伪造课标全文。",
    "core_literacy_goals": "把审美感知、艺术表现、创意实践、文化理解转成学生可观察行为。",
    "student_starting_point": "说明三年级学生在色彩表达上的已有经验和可能困难。",
    "unit_questions": "形成能带动观察、比较、表现和修订的单元问题。",
    "knowledge_and_skills": "保留本单元不能丢的美术语言和基本技能。",
    "performance_task": "明确学生最后完成什么作品或表达，并能留下评价证据。",
    "learning_progression": "按感受、比较、表现、修订组织学习推进。",
    "lesson_task_chain": "说明 1-1、1-2、1-3 各课承担的单元任务和证据。",
    "assessment_evidence": "列出过程、作品、表达和修订中的可观察证据。",
    "materials_and_scaffolds": "列出图片、色卡、学习单、示例和评价句式等支架。",
}


def build_candidate_generation_policy(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    decision = sources["r1_gate_decision"]
    return {
        "policy_id": "curriculum_profile_candidate_generation_policy_1013K_R2",
        "stage": STAGE_ID,
        "source_decision_id": decision["decision_id"],
        "normal_candidate_generation_allowed": decision["normal_candidate_generation_allowed"],
        "degraded_preview_allowed": decision["degraded_preview_allowed"],
        "degraded_preview_label_required": decision["degraded_preview_label_required"],
        "generation_mode": "degraded_preview_candidate_envelope",
        "provider_model_call_allowed": False,
        "must_not_generate_final_text": True,
        "must_not_write_unit_package": True,
        "must_not_write_lesson_body": True,
        "prompt_guard": {
            "full_standard_text_dumped_to_prompt": False,
            "official_curriculum_claim_allowed": False,
            "case_text_direct_copy_allowed": False,
            "teacher_confirmation_required_before_normal_generation": True,
            "use_teacher_readable_language": True,
            "avoid_engineering_terms_in_teacher_surface": True,
        },
        "blocked_by_gates": [
            gate["gate_id"]
            for gate in decision.get("gates", [])
            if gate.get("blocks_normal_generation") is True and gate.get("pass") is not True
        ],
        **boundary_flags(),
        **profile(),
    }


def build_candidate_envelope_bundle(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    state = sources["r1_runtime_state"]
    target_map = sources["r1_target_map"]
    policy = build_candidate_generation_policy(root)
    profile_obj = state["curriculum_control_profile"]
    envelopes = []
    for index, target in enumerate(target_map.get("targets", []), start=1):
        target_key = target["target_key"]
        envelopes.append(
            {
                "envelope_id": f"big_unit_candidate_envelope_{target_key}_1013K_R2",
                "order": index,
                "target_key": target_key,
                "teacher_label": TARGET_LABELS.get(target_key, target_key),
                "candidate_role": "big_unit_section_preview_candidate_request",
                "generation_mode": policy["generation_mode"],
                "normal_generation_allowed_now": False,
                "candidate_text_generated": False,
                "teacher_review_required": True,
                "degraded_preview_label_required": True,
                "source_control_profile_id": profile_obj["profile_id"],
                "source_intent": TARGET_INTENTS.get(target_key, "生成大单元候选段落的预览请求。"),
                "control_inputs": {
                    "core_literacy_focus": profile_obj["core_literacy_focus"],
                    "learning_task_direction": profile_obj["learning_task_direction"],
                    "assessment_evidence_direction": profile_obj["assessment_evidence_direction"],
                    "content_scope_boundary": state["selected_curriculum_standard_slice"]["content_scope_boundary"],
                    "prohibited_overreach": state["selected_curriculum_standard_slice"]["prohibited_overreach"],
                },
                "source_refs": [
                    "curriculum_derivation_runtime_state_1013K_R1.json",
                    "curriculum_derivation_gate_decision_1013K_R1.json",
                    "curriculum_derivation_target_map_1013K_R1.json",
                ],
                "blocked_write_targets": [
                    "unit_package",
                    "lesson_body",
                    "database",
                    "memory",
                    "feishu",
                    "formal_apply",
                ],
                "allowed_output_shape": {
                    "candidate_summary": "string_future",
                    "candidate_body_preview": "string_future",
                    "risk_note": "string_future",
                    "teacher_action_options": [
                        "采纳到预览",
                        "再改一版",
                        "暂不采用",
                    ],
                },
                "writes_unit_package": False,
                "writes_lesson_body": False,
            }
        )
    return {
        "bundle_id": "curriculum_profile_to_big_unit_candidate_envelope_bundle_1013K_R2",
        "stage": STAGE_ID,
        "source_state_id": state["state_id"],
        "source_target_map_id": target_map["target_map_id"],
        "envelope_count": len(envelopes),
        "envelopes": envelopes,
        "normal_candidate_generation_allowed": False,
        "degraded_preview_allowed": policy["degraded_preview_allowed"],
        "policy_ref": policy["policy_id"],
        **boundary_flags(),
        **profile(),
    }


def build_prompt_context_pack(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    state = sources["r1_runtime_state"]
    confirmation_items = sources["r6e_teacher_confirmation_items"]
    selected = state["selected_curriculum_standard_slice"]
    return {
        "context_pack_id": "curriculum_profile_prompt_context_pack_1013K_R2",
        "stage": STAGE_ID,
        "context_pack_role": "safe_context_for_future_candidate_generation_without_calling_model",
        "teacher_visible_context": {
            "subject": "美术",
            "grade_band": selected["grade_band"],
            "unit_theme": "多变的色彩",
            "lesson_title": "色彩的感觉",
            "core_literacy_focus": selected["core_literacy_tags"],
            "learning_task_direction": selected["learning_task_direction"],
            "assessment_evidence_direction": selected["assessment_evidence_direction"],
        },
        "hidden_control_context": {
            "content_scope_boundary": selected["content_scope_boundary"],
            "prohibited_overreach": selected["prohibited_overreach"],
            "source_quote_policy": selected["source_quote_policy"],
            "pending_confirmation_items": [
                item.get("label") for item in confirmation_items.get("items", [])
            ],
        },
        "prompt_must_not_include": [
            "full_curriculum_standard_text",
            "official_case_original_text_copy",
            "database_write_instruction",
            "formal_apply_instruction",
            "memory_write_instruction",
            "feishu_write_instruction",
        ],
        "future_model_call_allowed": False,
        **boundary_flags(),
        **profile(),
    }


def build_candidate_envelope_trace(root: Path | None = None) -> dict[str, Any]:
    policy = build_candidate_generation_policy(root)
    bundle = build_candidate_envelope_bundle(root)
    context = build_prompt_context_pack(root)
    return {
        "trace_id": "curriculum_profile_to_big_unit_candidate_envelope_trace_1013K_R2",
        "stage": STAGE_ID,
        "events": [
            {
                "event_id": "r2_event_01_policy_loaded",
                "event_type": "policy_from_r1_gate_decision",
                "output_ref": policy["policy_id"],
                "normal_candidate_generation_allowed": policy["normal_candidate_generation_allowed"],
                "side_effects_performed": False,
            },
            {
                "event_id": "r2_event_02_context_pack_built",
                "event_type": "safe_prompt_context_pack",
                "output_ref": context["context_pack_id"],
                "future_model_call_allowed": context["future_model_call_allowed"],
                "side_effects_performed": False,
            },
            {
                "event_id": "r2_event_03_envelopes_created",
                "event_type": "candidate_envelope_bundle",
                "output_ref": bundle["bundle_id"],
                "envelope_count": bundle["envelope_count"],
                "candidate_text_generated": False,
                "side_effects_performed": False,
            },
        ],
        "side_effects_performed": False,
        "candidate_text_generated": False,
        "provider_called": False,
        "model_called": False,
        **boundary_flags(),
        **profile(),
    }


def build_curriculum_profile_to_big_unit_candidate_envelope(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "candidate_generation_policy": build_candidate_generation_policy(root),
        "prompt_context_pack": build_prompt_context_pack(root),
        "candidate_envelope_bundle": build_candidate_envelope_bundle(root),
        "candidate_envelope_trace": build_candidate_envelope_trace(root),
        "boundary": boundary_flags(),
    }
