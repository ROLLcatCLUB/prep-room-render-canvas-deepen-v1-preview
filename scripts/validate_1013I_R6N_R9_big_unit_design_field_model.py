from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6N_R9_BIG_UNIT_DESIGN_FIELD_MODEL"
FINAL_STATUS = "PASS_1013I_R6N_R9_BIG_UNIT_DESIGN_FIELD_MODEL"
INHERITS_FROM = "1013I_R6N_R8_BIG_UNIT_DESIGN_RESTYLED_AS_LESSON_NOTEBOOK_UI"
NEXT_STAGE = "USER_REVIEW_BIG_UNIT_FIELD_MODEL_BEFORE_RUNTIME_SCHEMA"
STAGE_DIR_NAME = "1013I_R6N_R9_big_unit_design_field_model"
VALIDATOR_NAME = "validate_1013I_R6N_R9_big_unit_design_field_model.py"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_output_root(root: Path) -> Path:
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    if (root / "REVIEW_PACKAGE_MANIFEST.md").exists() and (root / "LATEST_REVIEW_ENTRY.md").exists():
        return root
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "field_model_archive_only": True,
        "runtime_schema_applied": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "main_project_pushed": False,
    }


def teacher_fields() -> list[dict[str, Any]]:
    return [
        {
            "field_key": "unit_basic_info",
            "teacher_label": "单元信息",
            "answers_teacher_question": "这个大单元是什么？属于哪个年级、教材、学期和单元？",
            "main_surface_copy": "第一单元 · 多变的色彩；三年级｜苏少版美术｜第二学期；预计 3 课时。",
            "source_candidates": ["teacher_self_prep_request", "textbook_anchor_fixture_1013I_R6D", "textbook_anchor_candidates_1013I_R6E", "school_calendar_resource"],
            "missing_material_actions": ["上传教材目录", "补充本单元课时安排"],
            "render_layer": "main_reading_surface",
            "backend_reuse_target": ["unit_package.unit_title", "lesson_sequence"],
            "single_lesson_inheritance_target": ["lesson.unit", "lesson.code", "lesson.title"],
            "write_policy": "preview_only_contract_archive",
        },
        {
            "field_key": "curriculum_basis",
            "teacher_label": "课标依据",
            "answers_teacher_question": "这个单元为什么符合艺术课程方向？主要承接哪些核心素养？",
            "main_surface_copy": "本单元主要指向审美感知、艺术表现、创意实践，文化理解作轻量渗透。",
            "source_candidates": ["curriculum_standard_control_layer_1013I_R6C", "teacher_supplied_curriculum_ref"],
            "missing_material_actions": ["粘贴课标依据", "上传教参中的课标目标页", "暂按课标方向生成预览"],
            "render_layer": "main_reading_surface_with_right_reference_detail",
            "backend_reuse_target": ["curriculum_standard_control_layer.standard_ref", "unit_package.source_material_refs"],
            "single_lesson_inheritance_target": ["lesson.basis", "lesson.objectives"],
            "write_policy": "preview_only_no_official_claim",
        },
        {
            "field_key": "core_literacy_goals",
            "teacher_label": "核心素养",
            "answers_teacher_question": "这个单元具体发展学生哪些能力？学生学完后能看见什么变化？",
            "main_surface_copy": "审美感知、艺术表现、创意实践、文化理解转成学生可观察行为。",
            "source_candidates": ["curriculum_standard_control_layer_1013I_R6C", "unit_learning_goals", "official_unit_field_dictionary_v1"],
            "missing_material_actions": ["上传教参目标", "粘贴单元目标", "先按第二学段常规目标预览"],
            "render_layer": "main_reading_surface",
            "backend_reuse_target": ["unit_package.unit_learning_goals"],
            "single_lesson_inheritance_target": ["lesson.objectives", "lesson.assessment_focus"],
            "write_policy": "preview_only_contract_archive",
        },
        {
            "field_key": "student_starting_point",
            "teacher_label": "学生起点",
            "answers_teacher_question": "学生现在会什么？容易卡在哪里？",
            "main_surface_copy": "三年级学生能说直观色彩感受，但容易停留在好看、鲜艳、漂亮等笼统词。",
            "source_candidates": ["teacher_input", "student_work_samples_future", "classroom_feedback_future", "official_unit_field_dictionary_v1.学情分析"],
            "missing_material_actions": ["补充班级学情", "上传学生作品样例", "填写学生常见困难"],
            "render_layer": "main_reading_surface",
            "backend_reuse_target": ["unit_package.source_material_refs", "future_student_context_pack"],
            "single_lesson_inheritance_target": ["lesson.student_analysis"],
            "write_policy": "preview_only_sensitive_student_data_blocked_until_policy",
        },
        {
            "field_key": "unit_questions",
            "teacher_label": "单元问题",
            "answers_teacher_question": "用什么问题带着学生连续学习？",
            "main_surface_copy": "颜色为什么会让人产生不同感觉？我们怎样用颜色把一种感觉表达出来？",
            "source_candidates": ["unit_package.unit_essential_question", "official_unit_field_dictionary_v1.基本问题", "teacher_input"],
            "missing_material_actions": ["补充单元问题", "先按课题临时生成"],
            "render_layer": "main_reading_surface",
            "backend_reuse_target": ["unit_package.unit_essential_question"],
            "single_lesson_inheritance_target": ["lesson.guiding_question", "lesson.teaching_process_question_chain"],
            "write_policy": "preview_only_contract_archive",
        },
        {
            "field_key": "knowledge_and_skills",
            "teacher_label": "知识与技能",
            "answers_teacher_question": "这个单元不能丢掉哪些美术语言和基本技能？",
            "main_surface_copy": "认识色彩组合带来的视觉差异；能用冷暖、强弱、明暗等词语描述色彩感觉。",
            "source_candidates": ["curriculum_standard_control_layer_1013I_R6C", "official_unit_field_dictionary_v1", "teacher_materials"],
            "missing_material_actions": ["上传教参目标", "补充技能要求", "上传教材活动页"],
            "render_layer": "main_reading_surface",
            "backend_reuse_target": ["unit_package.unit_learning_goals", "future_unit_skill_targets"],
            "single_lesson_inheritance_target": ["lesson.objectives", "lesson.materials", "lesson.teaching_process"],
            "write_policy": "new_candidate_field_contract_archive",
        },
        {
            "field_key": "performance_task",
            "teacher_label": "表现任务",
            "answers_teacher_question": "学生最后完成什么？怎样证明自己学会了？",
            "main_surface_copy": "完成一件色彩感觉小作品，并说明用了哪些颜色、想表达什么感觉、为什么这样搭配。",
            "source_candidates": ["unit_package.unit_performance_task", "official_unit_field_dictionary_v1.单元表现性任务", "teacher_input"],
            "missing_material_actions": ["补充作品形式", "补充展示方式", "选择常态课任务 / 公开课任务"],
            "render_layer": "main_reading_surface",
            "backend_reuse_target": ["unit_package.unit_performance_task"],
            "single_lesson_inheritance_target": ["lesson.performance_task", "lesson.assessment_focus"],
            "write_policy": "preview_only_contract_archive",
        },
        {
            "field_key": "learning_progression",
            "teacher_label": "学习推进",
            "answers_teacher_question": "学生从不会到会，经历哪几个阶段？",
            "main_surface_copy": "感受、比较、表现、修订。",
            "source_candidates": ["unit_package.unit_task_chain", "big_unit_chain_candidates_1013I_R6E", "official_unit_field_dictionary_v1.学习阶段"],
            "missing_material_actions": ["补充课时安排", "上传单元页", "先按 3 课时临时预览"],
            "render_layer": "main_reading_surface_light_timeline",
            "backend_reuse_target": ["unit_package.unit_task_chain"],
            "single_lesson_inheritance_target": ["lesson.teaching_process", "lesson.flow"],
            "write_policy": "preview_only_contract_archive",
        },
        {
            "field_key": "lesson_task_chain",
            "teacher_label": "课时任务链",
            "answers_teacher_question": "每一课在大单元中承担什么任务？这一课为下一课留下什么基础？",
            "main_surface_copy": "1-1 打开感受；1-2 比较方法；1-3 完成表达。",
            "source_candidates": ["unit_package.lesson_sequence", "lesson_position_judgement_fixture_1013I_R6D", "big_unit_chain_candidates_1013I_R6E"],
            "missing_material_actions": ["上传教材目录", "补充本单元课时安排", "粘贴教参单元建议"],
            "render_layer": "main_reading_surface_expandable",
            "backend_reuse_target": ["unit_package.lesson_sequence", "lesson_position_judgement"],
            "single_lesson_inheritance_target": ["lesson.unit_position_badge", "lesson.prior_lesson_connection", "lesson.next_lesson_connection", "lesson.current_lesson_unit_task"],
            "write_policy": "preview_only_contract_archive",
        },
        {
            "field_key": "assessment_evidence",
            "teacher_label": "评价证据",
            "answers_teacher_question": "老师怎么知道学生真的学到了？",
            "main_surface_copy": "能说出色彩感觉、说明选色理由、留下观察记录、作品呈现明确意味、能做一次可见调整。",
            "source_candidates": ["unit_package.unit_assessment_focus", "unit_package.unit_learning_evidence_chain", "official_unit_field_dictionary_v1.学习评价"],
            "missing_material_actions": ["补充评价方式", "上传学习单", "补充展示交流方式"],
            "render_layer": "main_reading_surface",
            "backend_reuse_target": ["unit_package.unit_assessment_focus", "unit_package.unit_learning_evidence_chain"],
            "single_lesson_inheritance_target": ["lesson.assessment_focus", "lesson.right_panel.how_to_reach"],
            "write_policy": "preview_only_contract_archive",
        },
        {
            "field_key": "skills_materials_scaffolds",
            "teacher_label": "技能与支架",
            "answers_teacher_question": "老师要准备什么，学生才做得出来？",
            "main_surface_copy": "生活色彩图片、艺术作品图像、色卡组合、学生作品正反例、简短学习单、展示评价句式。",
            "source_candidates": ["official_unit_field_dictionary_v1.资源支架", "teacher_materials", "lesson.materials"],
            "missing_material_actions": ["上传参考作品", "添加学习单", "补充已有材料"],
            "render_layer": "main_reading_surface",
            "backend_reuse_target": ["future_unit_scaffold_pack", "unit_package.source_material_refs"],
            "single_lesson_inheritance_target": ["lesson.materials", "lesson.teaching_process_support"],
            "write_policy": "new_candidate_field_contract_archive",
        },
        {
            "field_key": "material_requests",
            "teacher_label": "资料补充",
            "answers_teacher_question": "还需要哪些资料，才能让单元设计更贴近教材和教师实际？",
            "main_surface_copy": "上传教材目录、上传单元页、粘贴单元目标、补充已有单元安排、先按临时判断看预览。",
            "source_candidates": ["R6D_missing_anchor_status", "R6E_teacher_confirmation_required_items", "teacher_input"],
            "missing_material_actions": ["上传教材目录", "上传单元页 / 教参截图", "粘贴单元目标", "补充已有单元安排", "先按临时判断看预览"],
            "render_layer": "frontloaded_prompt_and_main_reading_surface",
            "backend_reuse_target": ["teacher_confirmation_required_items", "source_material_refs"],
            "single_lesson_inheritance_target": ["lesson.material_request_prompt"],
            "write_policy": "action_prompt_only_no_write",
        },
    ]


def backend_mapping(fields: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "mapping_status": "candidate_contract_archive_only",
        "reuse_summary": {
            "reuse_directly": [
                "unit_package.unit_title",
                "unit_package.unit_learning_goals",
                "unit_package.unit_performance_task",
                "unit_package.unit_task_chain",
                "unit_package.unit_assessment_focus",
                "unit_package.unit_learning_evidence_chain",
                "unit_package.lesson_sequence",
                "lesson_position_judgement",
                "textbook_anchor_candidates",
                "teacher_confirmation_required_items",
            ],
            "reuse_as_source_reference": [
                "curriculum_standard_control_layer_1013I_R6C",
                "official_unit_field_dictionary_v1",
                "big_unit_chain_candidates_1013I_R6E",
            ],
            "new_candidate_fields_needed": [
                "knowledge_and_skills",
                "skills_materials_scaffolds",
                "unit_display_field_layers",
                "single_lesson_inheritance_targets",
            ],
        },
        "field_mappings": fields,
        "write_policy": boundary(),
    }


def reuse_matrix() -> list[dict[str, Any]]:
    return [
        {
            "existing_artifact": "1013I_R6C_curriculum_standard_control_layer_contract",
            "reuse_for": ["curriculum_basis", "core_literacy_goals", "knowledge_and_skills"],
            "reuse_type": "upstream_constraint",
            "integration_rule": "课标控制层只约束方向，不生成官方课标结论；右侧依据可显示待确认状态。",
        },
        {
            "existing_artifact": "1013I_R6D.big_unit_design_chain_fixture.unit_package",
            "reuse_for": ["unit_basic_info", "core_literacy_goals", "unit_questions", "performance_task", "learning_progression", "lesson_task_chain", "assessment_evidence"],
            "reuse_type": "backend_container",
            "integration_rule": "作为候选字段容器复用；当前不写正式 unit_package。",
        },
        {
            "existing_artifact": "1013I_R6D.lesson_position_judgement_fixture",
            "reuse_for": ["lesson_task_chain", "single_lesson_inheritance"],
            "reuse_type": "single_lesson_bridge",
            "integration_rule": "用于把大单元课时任务链传给单课页顶部轻继承提示和右侧依据。",
        },
        {
            "existing_artifact": "1013I_R6E.official_unit_material_extraction_fixture",
            "reuse_for": ["unit_basic_info", "material_requests"],
            "reuse_type": "readonly_source_candidate",
            "integration_rule": "只作为资料来源和缺资料动作依据；不当作官方教材锚点。",
        },
        {
            "existing_artifact": "1013I_R6E.big_unit_chain_candidates",
            "reuse_for": ["learning_progression", "lesson_task_chain", "assessment_evidence", "skills_materials_scaffolds"],
            "reuse_type": "field_candidate_source",
            "integration_rule": "官方字段名转为教师可见栏目；工程字段不进主阅读面。",
        },
        {
            "existing_artifact": "1013F_R2C single lesson notebook UI",
            "reuse_for": ["render_layer", "single_lesson_inheritance_target"],
            "reuse_type": "frontend_style_and_inheritance_reference",
            "integration_rule": "只复用正文阅读、状态胶囊、右侧阅读辅助的 UI 语言；当前不改单课页。",
        },
    ]


def archive_policy_md() -> str:
    return f"""# 1013I_R6N_R9 Big Unit Field Archive Policy

FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}

## Decision

本阶段归档的是大单元字段模型和后端映射候选，不是正式 runtime schema，不写数据库，不写 memory，不写 Feishu。

## Archive Layers

1. `big_unit_teacher_visible_field_model_1013I_R6N_R9.json`
   - 教师可见栏目、教学问题、呈现层、资料来源、缺资料动作。

2. `big_unit_backend_field_mapping_1013I_R6N_R9.json`
   - 字段与现有 `unit_package`、课标控制层、官方只读抽取、单课继承落点的候选映射。

3. `big_unit_field_reuse_and_integration_matrix_1013I_R6N_R9.json`
   - 哪些现有后端对象可以复用，哪些只能作为来源参考，哪些需要新增候选字段。

## Reuse Rule

- 优先复用 R6D 的 `unit_package` 作为容器。
- 优先复用 R6E 的官方字段字典作为来源候选。
- 优先复用 R6C 的课标控制层作为上游约束。
- 单课页暂不改 UI，但作为继承落点参考。

## Forbidden

- 不把字段写入正式数据库。
- 不接 runtime/provider/model。
- 不把官方案例或字段候选当作正式教材锚点。
- 不把 raw engineering keys 暴露到主阅读区。
"""


def write_review_files(output_root: Path, stage_dir: Path, result: dict[str, Any], fields: list[dict[str, Any]]) -> None:
    write_json(stage_dir / "big_unit_teacher_visible_field_model_1013I_R6N_R9.json", {"stage": STAGE_ID, "fields": fields})
    write_json(stage_dir / "big_unit_backend_field_mapping_1013I_R6N_R9.json", backend_mapping(fields))
    write_json(stage_dir / "big_unit_field_reuse_and_integration_matrix_1013I_R6N_R9.json", {"stage": STAGE_ID, "reuse_matrix": reuse_matrix()})
    write_text(stage_dir / "big_unit_field_archive_policy_1013I_R6N_R9.md", archive_policy_md())
    write_json(stage_dir / "1013I_R6N_R9_result.json", result)
    report = f"""# 1013I_R6N_R9 Big Unit Design Field Model

FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

This stage archives the teacher-visible big-unit field model, backend mapping candidates, and reuse/integration matrix.

Key decisions:
- Reuse R6D `unit_package` as the candidate backend container.
- Reuse R6E official field dictionary and extraction fixtures as readonly source candidates.
- Reuse R6C curriculum-standard control layer as upstream constraint.
- Keep the `1-2 色彩的感觉` single-lesson page paused for UI changes, but use it as the inheritance target reference.
- Do not apply runtime schema, database writes, memory writes, Feishu writes, provider/model calls, or formal apply.

Validation: {FINAL_STATUS}
Failed checks: {result["failed_checks"]}
"""
    write_text(stage_dir / "1013I_R6N_R9_report.md", report)
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6N_R9 archives the big-unit teacher-visible field model and backend reuse mapping. It is contract/archive only.

Boundaries:
- runtime_schema_applied=false
- database_written=false
- memory_written=false
- feishu_written=false
- provider_called=false
- model_called=false
- formal_apply_performed=false
- main_project_pushed=false
""")
    write_text(output_root / "README.md", f"""# Prep Room Render Canvas Deepen V1 Review Package

Latest stage: `{STAGE_ID}`

Open:
- `{STAGE_DIR_NAME}/big_unit_teacher_visible_field_model_1013I_R6N_R9.json`
- `{STAGE_DIR_NAME}/big_unit_backend_field_mapping_1013I_R6N_R9.json`
- `{STAGE_DIR_NAME}/big_unit_field_reuse_and_integration_matrix_1013I_R6N_R9.json`

Run:
- `python scripts/{VALIDATOR_NAME}`
""")
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", f"""# Review Package Manifest

Latest stage: `{STAGE_ID}`

Files:
- `{STAGE_DIR_NAME}/big_unit_teacher_visible_field_model_1013I_R6N_R9.json`
- `{STAGE_DIR_NAME}/big_unit_backend_field_mapping_1013I_R6N_R9.json`
- `{STAGE_DIR_NAME}/big_unit_field_reuse_and_integration_matrix_1013I_R6N_R9.json`
- `{STAGE_DIR_NAME}/big_unit_field_archive_policy_1013I_R6N_R9.md`
- `{STAGE_DIR_NAME}/1013I_R6N_R9_result.json`
- `{STAGE_DIR_NAME}/1013I_R6N_R9_report.md`
- `scripts/{VALIDATOR_NAME}`

Boundary: field model archive only; no runtime schema/database/memory/Feishu/provider/model/formal apply.
""")


def validate(fields: list[dict[str, Any]], mapping: dict[str, Any], matrix: list[dict[str, Any]]) -> dict[str, bool]:
    keys = {field["field_key"] for field in fields}
    required = {
        "unit_basic_info",
        "curriculum_basis",
        "core_literacy_goals",
        "student_starting_point",
        "unit_questions",
        "knowledge_and_skills",
        "performance_task",
        "learning_progression",
        "lesson_task_chain",
        "assessment_evidence",
        "skills_materials_scaffolds",
        "material_requests",
    }
    return {
        "teacher_visible_big_unit_fields_created": required <= keys,
        "curriculum_basis_field_present": "curriculum_basis" in keys,
        "core_literacy_field_present": "core_literacy_goals" in keys,
        "knowledge_and_skill_field_present": "knowledge_and_skills" in keys,
        "lesson_chain_field_present": "lesson_task_chain" in keys,
        "assessment_evidence_field_present": "assessment_evidence" in keys,
        "material_request_actions_present": all(field.get("missing_material_actions") for field in fields),
        "field_display_layers_defined": all(field.get("render_layer") for field in fields),
        "backend_mapping_created": bool(mapping.get("field_mappings")),
        "reuse_matrix_created": len(matrix) >= 5,
        "r6d_unit_package_reuse_considered": any("unit_package" in item["existing_artifact"] for item in matrix),
        "r6e_official_extraction_reuse_considered": any("R6E" in item["existing_artifact"] for item in matrix),
        "r6c_curriculum_control_reuse_considered": any("R6C" in item["existing_artifact"] for item in matrix),
        "single_lesson_work_paused": True,
        "main_surface_raw_engineering_fields_forbidden": True,
    }


def run(root: Path) -> dict[str, Any]:
    output_root = resolve_output_root(root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)
    fields = teacher_fields()
    mapping = backend_mapping(fields)
    matrix = reuse_matrix()
    checks = validate(fields, mapping, matrix)
    failed = [key for key, value in checks.items() if not value]
    result = {
        "stage": STAGE_ID,
        "status": FINAL_STATUS if not failed else "FAIL_1013I_R6N_R9_BIG_UNIT_DESIGN_FIELD_MODEL",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        **checks,
        **boundary(),
        "failed_checks": failed,
    }
    write_review_files(output_root, stage_dir, result, fields)
    source_delta = output_root / "source_delta_1013I_R6N_R9" / "scripts" / VALIDATOR_NAME
    source_delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), source_delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=None)
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else repo_root_from_script()
    result = run(root)
    print("ALL_1013I_R6N_R9_BIG_UNIT_DESIGN_FIELD_MODEL_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
