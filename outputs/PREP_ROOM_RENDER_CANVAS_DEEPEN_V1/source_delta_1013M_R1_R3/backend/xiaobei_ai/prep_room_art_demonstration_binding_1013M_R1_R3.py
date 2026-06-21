from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013M_R1_R3_ART_DEMONSTRATION_BACKEND_BINDING_PACKAGE"
R0_STAGE_DIR = (
    "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
    "1013M_R0_art_demonstration_and_visual_scaffold_contract"
)


def boundary_flags() -> dict[str, bool]:
    return {
        "backend_binding_package_only": True,
        "request_envelope_only": True,
        "prompt_binding_only": True,
        "normalization_fixture_only": True,
        "courseware_seed_fixture_only": True,
        "preview_only": True,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "main_project_pushed": False,
    }


def _repo_root_from_module() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _r0_dir(root: Path) -> Path:
    return root / R0_STAGE_DIR


def load_r0_contract_assets(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    stage_dir = _r0_dir(root)
    schema = _read_json(stage_dir / "art_demonstration_visual_scaffold_schema_1013M_R0.json")
    sample = _read_json(stage_dir / "sample_fixture_color_contrast_harmony_1013M_R0.json")
    mapping = _read_json(stage_dir / "courseware_mapping_for_demonstration_1013M_R0.json")
    return {
        "schema": schema,
        "sample_fixture": sample,
        "courseware_mapping": mapping,
        "source_files": {
            "schema": str(stage_dir / "art_demonstration_visual_scaffold_schema_1013M_R0.json"),
            "sample_fixture": str(stage_dir / "sample_fixture_color_contrast_harmony_1013M_R0.json"),
            "courseware_mapping": str(stage_dir / "courseware_mapping_for_demonstration_1013M_R0.json"),
        },
    }


def detect_art_demonstration_need(case: dict[str, Any]) -> dict[str, Any]:
    text = " ".join(
        str(case.get(key) or "")
        for key in ["subject", "lesson_title", "teacher_input", "unit", "performance_task"]
    )
    keywords = ["美术", "绘画", "画", "创作", "表现", "设计", "制作", "手工", "色彩", "构图", "技法", "材料"]
    hits = [keyword for keyword in keywords if keyword in text]
    required = bool(hits)
    return {
        "art_demonstration_required": required,
        "matched_keywords": hits,
        "reason": "本课包含美术创作或视觉表现任务，需要在学生动手前生成示范与支架。"
        if required
        else "未识别到明确的美术创作任务，可不强制生成示范与支架。",
    }


def default_lesson_case() -> dict[str, Any]:
    return {
        "case_id": "color_feeling_art_demo_binding_1013M_R1_R3",
        "grade": "三年级",
        "subject": "美术",
        "unit": "第一单元 · 多变的色彩",
        "lesson_title": "1-2《色彩的感觉》",
        "lesson_design_mode": "standard_daily",
        "teacher_input": "学生需要在创作前知道怎么用颜色表达感觉，不要照抄老师范画。",
        "performance_task": "用一组颜色表达一种明确感觉，并能说出选色理由。",
        "duration_minutes": 40,
        "resource_constraints": ["可使用图片、色卡、黑板、学习单", "不接真实资料库"],
    }


def build_art_demonstration_request_envelope(
    case: dict[str, Any] | None = None,
    *,
    root: Path | None = None,
) -> dict[str, Any]:
    case = case or default_lesson_case()
    assets = load_r0_contract_assets(root)
    schema_block = assets["schema"]["demonstration_block"]
    need = detect_art_demonstration_need(case)
    required_fields = [
        {
            "field_key": key,
            "teacher_label": value.get("teacher_label"),
            "required": value.get("required") is True,
            "description": value.get("description") or "",
        }
        for key, value in schema_block.items()
    ]
    return {
        "stage": STAGE_ID,
        "envelope_id": "art_demonstration_request_envelope_1013M_R1",
        "case": case,
        "art_demonstration_and_visual_scaffold_required": need["art_demonstration_required"],
        "requirement_reason": need["reason"],
        "matched_keywords": need["matched_keywords"],
        "insert_position_policy": {
            "insert_after_step_id": "explore",
            "insert_before_step_id": "make",
            "insert_step_id": "demo",
            "insert_step_name": "示范与支架",
            "fallback_if_no_explore_step": "insert_before_student_creation",
        },
        "required_fields": required_fields,
        "allowed_step_id_extension": {
            "base_step_ids": ["intro", "sense", "explore", "make", "share"],
            "new_candidate_step_id": "demo",
            "runtime_contract_patch_applied": False,
            "reason": "本阶段只生成 request envelope，不直接修改 1013E runtime ALLOWED_IDS。",
        },
        "source_contract": assets["source_files"]["schema"],
        **boundary_flags(),
    }


def build_art_demonstration_prompt_binding(envelope: dict[str, Any]) -> dict[str, Any]:
    case = envelope.get("case") if isinstance(envelope.get("case"), dict) else default_lesson_case()
    required_labels = [item["teacher_label"] for item in envelope.get("required_fields", []) if item.get("required")]
    return {
        "stage": STAGE_ID,
        "prompt_binding_id": "art_demonstration_prompt_binding_1013M_R2",
        "source_envelope_id": envelope["envelope_id"],
        "system_prompt_patch": (
            "你是师维备课室的小教，负责小学美术课时设计协作。"
            "当课程包含绘画、设计、制作或视觉表现任务时，必须生成“示范与支架”环节。"
            "示范不是让学生照抄范画，而是帮助学生看清方法、步骤、工具技法和视觉标准。"
        ),
        "user_prompt_patch": {
            "lesson_title": case.get("lesson_title"),
            "teacher_task": "请为本课生成 art_demonstration_and_visual_scaffold 候选。",
            "must_include_teacher_visible_parts": required_labels,
            "must_not_write": [
                "不要只写“教师示范”。",
                "不要让学生照抄老师范画。",
                "不要把工程字段名放进教师主阅读区。",
                "不要生成正式教案正文。",
            ],
            "style": [
                "短句，教师能直接放进教学过程。",
                "包含可记忆的三步口令。",
                "明确错例和修正方法。",
                "同龄作品用于打开思路，不用于临摹。",
            ],
        },
        "expected_output_shape": {
            "process_step": "demo",
            "field_patch_candidate": "teaching_process/demo",
            "courseware_screen_seeds": [
                "teacher_demo_screen",
                "step_mantra_screen",
                "mistake_comparison_screen",
                "peer_example_screen",
                "pre_creation_check_screen",
            ],
            "assessment_link": "original_expression_and_method_use",
        },
        **boundary_flags(),
    }


def static_generation_candidate_from_r0_sample(root: Path | None = None) -> dict[str, Any]:
    assets = load_r0_contract_assets(root)
    demo = assets["sample_fixture"]["art_demonstration_and_visual_scaffold"]
    return {
        "candidate_id": "art_demo_static_candidate_1013M_R3",
        "source": "sample_fixture_color_contrast_harmony_1013M_R0.json",
        "candidate_only": True,
        "process_step": {
            "step_id": "demo",
            "step_name": "示范与支架",
            "duration": "8分钟",
            "step_role": demo["demo_purpose"],
            "design_intent": "把学生动手前最容易卡住的工具、技法、步骤和视觉标准讲清楚。",
            "student_state_before": "学生知道颜色可以表达感觉，但还不知道从哪里开始，也容易照着老师画。",
            "student_state_after": "学生能说出自己的主色、伙伴色、点亮位置和不照抄的创作打算。",
            "teacher_action": "用色卡或小稿演示：先定主色，再找伙伴，最后一点亮；再展示错例和同龄作品。",
            "student_action": "跟读三步口令，选择自己的主色和伙伴色，说出动手前检查。",
            "big_screen_state": "大屏显示示范步骤、三步口令、错例对比、同龄作品和动手前检查。",
            "learning_sheet_state": "学习单增加主色、伙伴色、点亮位置和我想表达的感觉。",
            "assessment_evidence": "学生能说明选色理由，作品有自己的表达而不是照抄范画。",
            "transition_from_previous": "承接探究中的色彩感受分类和理由表达。",
            "transition_to_next": "进入个人色彩小练习或作品表现。",
            "risk_and_adjustment": "若学生照抄范画，提醒只借鉴方法；困难学生可借鉴局部，但需改成自己的画面。",
        },
        "demonstration_block": demo,
        **boundary_flags(),
    }


def normalize_art_demonstration_output(candidate: dict[str, Any]) -> dict[str, Any]:
    step = candidate["process_step"]
    demo = candidate["demonstration_block"]
    return {
        "stage": STAGE_ID,
        "normalization_id": "art_demonstration_normalized_output_1013M_R3",
        "source_candidate_id": candidate["candidate_id"],
        "process_step_insert": {
            "id": "demo",
            "name": "示范与支架",
            "time": step["duration"],
            "summary": "教师用三步口令、技法示范、错例辨析和同龄作品支架，帮助学生在创作前知道怎样用颜色表达感觉。",
            "tags": ["技法示范", "三步口令", "同龄作品"],
            "intent": {
                "role": step["step_role"],
                "design": step["design_intent"],
                "transition": f"{step['transition_from_previous']} {step['transition_to_next']}",
                "student": step["student_state_before"],
                "teacher": step["teacher_action"],
                "activity": step["student_action"],
                "screen": step["big_screen_state"],
                "material": "色卡、示范小稿、错例、同龄作品、学习单。",
                "evidence": step["assessment_evidence"],
                "risk": step["risk_and_adjustment"],
            },
        },
        "field_patch_candidate": {
            "field_patch_id": "field_patch_art_demo_step_1013M_R3",
            "target_section": "teaching_process",
            "target_step_id": "demo",
            "target_field": "process_steps",
            "patch_type": "insert_step",
            "before_summary": "教学过程从探究直接进入表现，学生动手前缺少示范、技法和视觉标准支架。",
            "after_candidate": "在探究与表现之间加入“示范与支架”。",
            "reasoning_basis": [
                "小学美术创作前需要教师示范工具和技法。",
                "三步口令能帮助学生记住绘画过程。",
                "同龄作品能打开思路，但必须避免照抄。",
            ],
            "impact_scope": ["big_screen", "handout", "rubric", "student_activity"],
            "teacher_review_required": True,
            "formal_apply_performed": False,
        },
        "assessment_link": {
            "assessment_focus": "方法迁移与原创表达",
            "observable_evidence": demo["assessment_link"],
            "copy_boundary": demo["anti_copy_guidance"],
        },
        **boundary_flags(),
    }


def build_art_demonstration_courseware_seeds(normalized: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "seed_bundle_id": "art_demonstration_courseware_screen_seeds_1013M_R3",
        "source_normalization_id": normalized["normalization_id"],
        "screen_seed_count": 5,
        "screen_seeds": [
            _screen_seed(1, "teacher_demo", "老师示范", "怎样让颜色有主要感觉", "teacher_demo_screen", ["示范小稿", "色卡"], "先看老师怎样选主色。"),
            _screen_seed(2, "step_mantra", "三步口令", "先定主色，再找伙伴，最后一点亮", "step_mantra_screen", [], "跟着口令说一遍。"),
            _screen_seed(3, "mistake_compare", "哪里容易乱", "颜色太多时，画面会失去重点", "mistake_comparison_screen", ["错例小稿"], "如果只留一个点亮位置，会不会更清楚？"),
            _screen_seed(4, "peer_examples", "同龄作品", "学方法，不照抄", "peer_example_screen", ["同龄作品 2-3 张"], "你想学习哪一种配色方法？"),
            _screen_seed(5, "pre_creation_check", "动手前看一眼", "我的主色是什么？我想表达什么感觉？", "pre_creation_check_screen", [], "开始前先确认自己的选择。"),
        ],
        "lesson_to_courseware_binding": {
            "target_step_id": "demo",
            "target_step_name": "示范与支架",
            "binding_policy": "paragraph_level_courseware_cards",
            "right_rail_target": "大屏草稿",
        },
        **boundary_flags(),
    }


def _screen_seed(
    order: int,
    key: str,
    title: str,
    prompt: str,
    screen_type: str,
    material_labels: list[str],
    interaction_hint: str,
) -> dict[str, Any]:
    return {
        "screen_id": f"art_demo_screen_seed_{order:02d}_{key}_1013M_R3",
        "screen_order": order,
        "screen_title": title,
        "screen_type": screen_type,
        "source_lesson_section_refs": ["teaching_process", "demo"],
        "teacher_visible_purpose": prompt,
        "visual_priority": "image_or_demo_primary_text_light",
        "material_slots": [
            {
                "slot_id": f"slot_{key}_{index + 1}",
                "slot_label": label,
                "expected_count": 1,
                "status": "pending_material",
            }
            for index, label in enumerate(material_labels)
        ],
        "classroom_prompt": prompt,
        "interaction_hint": interaction_hint,
        "status": "pending_material" if material_labels else "ready_as_text_screen",
        "preview_only": True,
    }


def build_art_demonstration_backend_binding_package(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    envelope = build_art_demonstration_request_envelope(root=root)
    prompt_binding = build_art_demonstration_prompt_binding(envelope)
    candidate = static_generation_candidate_from_r0_sample(root)
    normalized = normalize_art_demonstration_output(candidate)
    courseware = build_art_demonstration_courseware_seeds(normalized)
    return {
        "stage": STAGE_ID,
        "package_id": "1013M_R1_R3_ART_DEMONSTRATION_BACKEND_BINDING_PACKAGE",
        "request_envelope": envelope,
        "prompt_binding": prompt_binding,
        "static_generation_candidate": candidate,
        "normalized_output": normalized,
        "courseware_screen_seed_bundle": courseware,
        "reuse_policy": {
            "reuse_1013E_lesson_reasoning_contract": True,
            "reuse_1013E_staged_derivation_pipeline": True,
            "reuse_1013K_courseware_screen_seed_shape": True,
            "runtime_contract_patch_applied": False,
            "new_disconnected_page_created": False,
        },
        **boundary_flags(),
    }


def validate_art_demonstration_backend_binding_package(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    envelope = package.get("request_envelope") if isinstance(package.get("request_envelope"), dict) else {}
    prompt = package.get("prompt_binding") if isinstance(package.get("prompt_binding"), dict) else {}
    normalized = package.get("normalized_output") if isinstance(package.get("normalized_output"), dict) else {}
    courseware = package.get("courseware_screen_seed_bundle") if isinstance(package.get("courseware_screen_seed_bundle"), dict) else {}

    if envelope.get("art_demonstration_and_visual_scaffold_required") is not True:
        errors.append("art_demonstration_required_not_true")
    if len(envelope.get("required_fields") or []) < 10:
        errors.append("required_fields_less_than_10")
    if "不要只写“教师示范”" not in json.dumps(prompt, ensure_ascii=False):
        errors.append("prompt_missing_teacher_demo_guard")
    if ((normalized.get("process_step_insert") or {}).get("id")) != "demo":
        errors.append("normalized_process_step_demo_missing")
    if ((normalized.get("field_patch_candidate") or {}).get("formal_apply_performed")) is not False:
        errors.append("field_patch_formal_apply_not_false")
    if courseware.get("screen_seed_count") != 5:
        errors.append("courseware_seed_count_not_5")
    for seed in courseware.get("screen_seeds") or []:
        if seed.get("preview_only") is not True:
            errors.append(f"screen_seed_not_preview_only:{seed.get('screen_id')}")

    for key, expected in boundary_flags().items():
        if package.get(key) != expected:
            errors.append(f"boundary_flag_mismatch:{key}")
    return errors
