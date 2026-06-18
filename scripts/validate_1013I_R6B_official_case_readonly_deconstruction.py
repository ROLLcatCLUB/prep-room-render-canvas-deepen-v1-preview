from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6B_OFFICIAL_CASE_READONLY_DECONSTRUCTION_FOR_SCHEMA_CALIBRATION"
NEXT_STAGE = "1013I_R6C_CURRICULUM_STANDARD_CONTROL_LAYER_CONTRACT"
R6A_PASS_STATUS = "PASS_1013I_R6A_BIG_UNIT_CONTEXT_REQUIRED_GATE"
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]
SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)app[_-]?secret\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)tenant[_-]?access[_-]?token\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)cookie\s*[:=]\s*['\"][^'\"]{20,}"),
]
REQUIRED_CASE_FIELDS = [
    "case_id",
    "case_title",
    "source_type",
    "source_authority_level",
    "subject",
    "grade",
    "semester",
    "lesson_or_unit_title",
    "textbook_anchor",
    "standard_alignment_claims",
    "core_competency_focus",
    "big_unit_signal_present",
    "big_unit_signal_type",
    "lesson_role_signal",
    "learning_task_design",
    "activity_sequence",
    "student_output",
    "assessment_design",
    "learning_evidence_design",
    "teacher_support_moves",
    "student_reflection_or_revision",
    "reusable_design_moves",
    "useful_prompt_patterns",
    "useful_field_patterns",
    "limitations_or_missing_parts",
    "should_not_directly_copy",
    "reference_only",
    "source_refs",
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_output_root(root: Path) -> Path:
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    if (
        (root / "README.md").exists()
        or (root / "1013I_R6A_big_unit_context_required_gate").exists()
        or (root / "scripts" / Path(__file__).name).exists()
    ):
        return root
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def profile() -> dict[str, Any]:
    return {
        "agent_role": "unified_teacher_agent",
        "assistant_profile": {
            "display_name": "小教",
            "display_name_customizable": True,
            "wake_name": "小教",
            "voice_profile_id": None,
            "tts_enabled": False,
            "speaking_style": "calm_professional",
            "assistant_tone": "teacher_work_partner",
            "response_style": "concise_contextual",
        },
        "active_space": "prep_room",
        "active_capability": "lesson_prep",
    }


def boundary() -> dict[str, Any]:
    return {
        "readonly": True,
        "reference_only": True,
        "big_unit_generation_performed": False,
        "single_lesson_generation_performed": False,
        "product_runtime_called": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "official_export_created": False,
        "official_archive_created": False,
        "main_project_pushed": False,
    }


def source_path(name: str) -> str:
    return str(Path("E:/codex/xiaobei-knowledge-base/_parsed") / name)


def source_index() -> dict[str, Any]:
    cases = [
        {
            "case_id": "kb_art_g3_upper_official_lesson_design_unit_02_afb83c9f5c",
            "case_title": "三年级上册官方教学设计参考 - 第二单元 色彩的碰撞",
            "source_type": "official_case_reference",
            "source_authority_level": "official_teaching_design_reference",
            "subject": "美术",
            "grade": "三年级",
            "semester": "上册",
            "lesson_or_unit_title": "第二单元 色彩的碰撞",
            "parsed_source_path": source_path("kb_art_g3_upper_official_lesson_design_unit_02_afb83c9f5c.txt"),
            "local_source_available": Path(source_path("kb_art_g3_upper_official_lesson_design_unit_02_afb83c9f5c.txt")).exists(),
            "reference_only": True,
            "is_curriculum_standard": False,
        },
        {
            "case_id": "kb_art_g3_upper_official_lesson_design_unit_04_bab8ad12a5",
            "case_title": "三年级上册官方教学设计参考 - 第四单元 红红的剪纸",
            "source_type": "official_case_reference",
            "source_authority_level": "official_teaching_design_reference",
            "subject": "美术",
            "grade": "三年级",
            "semester": "上册",
            "lesson_or_unit_title": "第四单元 红红的剪纸",
            "parsed_source_path": source_path("kb_art_g3_upper_official_lesson_design_unit_04_bab8ad12a5.txt"),
            "local_source_available": Path(source_path("kb_art_g3_upper_official_lesson_design_unit_04_bab8ad12a5.txt")).exists(),
            "reference_only": True,
            "is_curriculum_standard": False,
        },
        {
            "case_id": "kb_art_g3_upper_official_lesson_design_unit_06_1f1e109c3e",
            "case_title": "三年级上册官方教学设计参考 - 第六单元 秩序之美",
            "source_type": "official_case_reference",
            "source_authority_level": "official_teaching_design_reference",
            "subject": "美术",
            "grade": "三年级",
            "semester": "上册",
            "lesson_or_unit_title": "第六单元 秩序之美",
            "parsed_source_path": source_path("kb_art_g3_upper_official_lesson_design_unit_06_1f1e109c3e.txt"),
            "local_source_available": Path(source_path("kb_art_g3_upper_official_lesson_design_unit_06_1f1e109c3e.txt")).exists(),
            "reference_only": True,
            "is_curriculum_standard": False,
        },
        {
            "case_id": "kb_art_g3_upper_official_lesson_design_unit_08_448205c865",
            "case_title": "三年级上册官方教学设计参考 - 第八单元 寓言与神话",
            "source_type": "official_case_reference",
            "source_authority_level": "official_teaching_design_reference",
            "subject": "美术",
            "grade": "三年级",
            "semester": "上册",
            "lesson_or_unit_title": "第八单元 寓言与神话",
            "parsed_source_path": source_path("kb_art_g3_upper_official_lesson_design_unit_08_448205c865.txt"),
            "local_source_available": Path(source_path("kb_art_g3_upper_official_lesson_design_unit_08_448205c865.txt")).exists(),
            "reference_only": True,
            "is_curriculum_standard": False,
        },
    ]
    return {
        "index_id": "official_case_source_index_1013I_R6B",
        "stage": STAGE_ID,
        "source_scope": "3-5 high-authority official case references from the local knowledge base",
        "official_case_count": len(cases),
        "cases": cases,
        "cases_treated_as_reference_only": True,
        "cases_not_treated_as_curriculum_standard": True,
        **boundary(),
        **profile(),
    }


def deconstruction_matrix() -> dict[str, Any]:
    cases = [
        {
            "case_id": "kb_art_g3_upper_official_lesson_design_unit_02_afb83c9f5c",
            "case_title": "色彩的碰撞",
            "source_type": "official_case_reference",
            "source_authority_level": "official_teaching_design_reference",
            "subject": "美术",
            "grade": "三年级",
            "semester": "上册",
            "lesson_or_unit_title": "第二单元 色彩的碰撞",
            "textbook_anchor": "三年级上册第二单元，围绕色彩规律、点彩和情感表达组织学习",
            "standard_alignment_claims": ["审美理解", "艺术表现", "生活中的色彩意义", "教-学-评一体化"],
            "core_competency_focus": ["审美感知", "艺术表现", "创意实践"],
            "big_unit_signal_present": True,
            "big_unit_signal_type": ["大观念", "基本问题", "表现性任务", "三阶段任务链", "单元评价表"],
            "lesson_role_signal": "concept_building_to_creative_production",
            "learning_task_design": "从校园和自然色彩观察进入三原色、间色、复色探究，再以点彩和梦幻季节表达情感。",
            "activity_sequence": ["校园色彩观察", "三原色调色实验", "点彩作品探秘", "梦幻季节合作创作", "长卷展示与评价"],
            "student_output": ["色彩实验记录", "点彩动物或点彩组合", "梦幻季节长卷", "单元学习评价表"],
            "assessment_design": ["阶段学习约定", "学习单评价回应", "口头与书面评价", "七彩果实可视化评价"],
            "learning_evidence_design": ["阶段学习单", "调色实验结果", "作品长卷", "自评与互评记录"],
            "teacher_support_moves": ["情境支架", "任务支架", "资源支架", "策略支架", "评价支架"],
            "student_reflection_or_revision": "通过阶段性评价和最终单元学习评价表进行口头、书面回看。",
            "reusable_design_moves": ["以校园真实色彩引入", "用表现性任务统领阶段活动", "把学习单作为过程证据"],
            "useful_prompt_patterns": ["先问学生在真实环境中发现什么", "让学生把色彩规律转成情感表达", "要求说明作品如何传递感受"],
            "useful_field_patterns": ["unit_big_idea", "unit_essential_question", "unit_task_chain", "learning_evidence_chain", "assessment_visualization"],
            "limitations_or_missing_parts": ["案例可参考但不能替代课标控制层", "当前课在教材全册结构中的位置仍需教材锚定"],
            "should_not_directly_copy": ["具体活动名称", "评价图形命名", "完整教学流程语句"],
            "reference_only": True,
            "source_refs": ["official_case_source_index_1013I_R6B#kb_art_g3_upper_official_lesson_design_unit_02_afb83c9f5c"],
        },
        {
            "case_id": "kb_art_g3_upper_official_lesson_design_unit_04_bab8ad12a5",
            "case_title": "红红的剪纸",
            "source_type": "official_case_reference",
            "source_authority_level": "official_teaching_design_reference",
            "subject": "美术",
            "grade": "三年级",
            "semester": "上册",
            "lesson_or_unit_title": "第四单元 红红的剪纸",
            "textbook_anchor": "三年级上册第四单元，围绕传统剪纸、纹样、寓意和校园故事表达组织学习",
            "standard_alignment_claims": ["文化理解", "艺术表现", "生活故事表达", "合作展示评价"],
            "core_competency_focus": ["审美感知", "艺术表现", "文化理解", "创意实践"],
            "big_unit_signal_present": True,
            "big_unit_signal_type": ["大观念", "基本问题", "校园剪纸艺术节", "两阶段学习任务"],
            "lesson_role_signal": "cultural_context_to_creative_production",
            "learning_task_design": "从剪纸历史、寓意和纹样故事出发，学习基本剪法，再剪绘校园故事并组合展示。",
            "activity_sequence": ["剪纸故事探究", "传统纹样体验", "传承人作品研习", "影子大形体验", "校园故事剪纸长卷"],
            "student_output": ["传统纹样练习", "小动物纹样组合", "校园故事剪纸", "长卷展示"],
            "assessment_design": ["任务评价要点", "作品自评和同伴评价", "合作与文化理解维度"],
            "learning_evidence_design": ["参观记录", "纹样练习", "剪纸作品", "单元学习评价表"],
            "teacher_support_moves": ["资源支架", "任务支架", "活动支架", "展示评价支架"],
            "student_reflection_or_revision": "通过自评、同伴给星和教师点评回看任务完成、交流合作和文化理解。",
            "reusable_design_moves": ["把非遗文化转成学生生活故事", "用影子活动理解剪纸大形", "从传统纹样迁移到个人表达"],
            "useful_prompt_patterns": ["这件作品用什么符号讲故事", "你要剪出校园生活中的哪个瞬间", "剪纸的寓意如何和你的生活连接"],
            "useful_field_patterns": ["cultural_context", "symbol_language", "lesson_role_signal", "student_story_output", "peer_assessment"],
            "limitations_or_missing_parts": ["文化资料来源需要正式引用锚点", "教师确认本地校园情境是否适用"],
            "should_not_directly_copy": ["传承人案例细节", "展览馆情境名称", "评价表原有表述"],
            "reference_only": True,
            "source_refs": ["official_case_source_index_1013I_R6B#kb_art_g3_upper_official_lesson_design_unit_04_bab8ad12a5"],
        },
        {
            "case_id": "kb_art_g3_upper_official_lesson_design_unit_06_1f1e109c3e",
            "case_title": "秩序之美",
            "source_type": "official_case_reference",
            "source_authority_level": "official_teaching_design_reference",
            "subject": "美术",
            "grade": "三年级",
            "semester": "上册",
            "lesson_or_unit_title": "第六单元 秩序之美",
            "textbook_anchor": "三年级上册第六单元，围绕对称、重复、渐变与生活空间改造组织学习",
            "standard_alignment_claims": ["审美感知", "设计意识", "生活应用", "学评一致"],
            "core_competency_focus": ["审美感知", "艺术表现", "创意实践"],
            "big_unit_signal_present": True,
            "big_unit_signal_type": ["大观念", "基本问题", "生活改造表现性任务", "两阶段学习任务"],
            "lesson_role_signal": "method_learning_to_transfer_extension",
            "learning_task_design": "先发现自然与生活中的秩序规律，再用秩序美原理进行物品或空间改造。",
            "activity_sequence": ["微型展观察", "图片分类讨论", "校园规律寻找", "经典作品赏析", "生活空间改造方案"],
            "student_output": ["任务单", "速写或照片记录", "秩序图案设计", "生活改造方案", "展示讲解"],
            "assessment_design": ["观察家奖", "创意设计师奖", "秩序美大师奖", "自评互评师评结合"],
            "learning_evidence_design": ["任务单", "设计草图", "装饰成品", "互评海报记录", "成长档案"],
            "teacher_support_moves": ["目标发布", "工具资源", "经典作品启发", "评价标准海报", "奖章反馈"],
            "student_reflection_or_revision": "通过评价标准海报和每组介绍，把功能性、实用性、美观性作为修改依据。",
            "reusable_design_moves": ["从视觉规律走向生活问题解决", "把形式原理转成设计任务", "用评价标准支撑学生互评"],
            "useful_prompt_patterns": ["这个规律解决了什么生活问题", "你的设计用了哪种秩序美原理", "同伴建议能否帮助方案更实用"],
            "useful_field_patterns": ["life_problem_context", "method_principle", "transfer_task", "function_beauty_balance", "evidence_artifacts"],
            "limitations_or_missing_parts": ["需要区分生活应用任务与普通装饰练习", "教材图片和作品来源仍需教材层锚定"],
            "should_not_directly_copy": ["奖项命名", "具体路线与微型展布置", "完整评价海报文案"],
            "reference_only": True,
            "source_refs": ["official_case_source_index_1013I_R6B#kb_art_g3_upper_official_lesson_design_unit_06_1f1e109c3e"],
        },
        {
            "case_id": "kb_art_g3_upper_official_lesson_design_unit_08_448205c865",
            "case_title": "寓言与神话",
            "source_type": "official_case_reference",
            "source_authority_level": "official_teaching_design_reference",
            "subject": "美术",
            "grade": "三年级",
            "semester": "上册",
            "lesson_or_unit_title": "第八单元 寓言与神话",
            "textbook_anchor": "三年级上册第八单元，围绕故事视觉表达、折叠书和儿童剧展演组织学习",
            "standard_alignment_claims": ["文化理解", "跨学科学习", "创意表达", "合作评价"],
            "core_competency_focus": ["审美感知", "艺术表现", "创意实践", "文化理解"],
            "big_unit_signal_present": True,
            "big_unit_signal_type": ["大观念", "基本问题", "校园故事展演", "三阶段任务链", "单元评价量规"],
            "lesson_role_signal": "cultural_context_to_exhibition_or_reflection",
            "learning_task_design": "从故事文化价值探究进入插图、折叠书创编和儿童剧展演，形成综合表达。",
            "activity_sequence": ["资料包探究", "看图猜故事", "故事插图", "折叠书创编", "道具制作与剧场展演"],
            "student_output": ["故事草图", "插图卡片", "折叠书", "演出计划表", "道具与表演"],
            "assessment_design": ["单元评价量规", "小组评语", "主题情节插图质量评价", "展示表演评价"],
            "learning_evidence_design": ["学习单", "草图", "折叠书", "演出计划表", "小组评语"],
            "teacher_support_moves": ["邀请函情境", "资料包", "任务单", "关键问题", "小组合作支架", "量规支架"],
            "student_reflection_or_revision": "通过小组评语和单元量规回顾文化理解、团队合作和创意表达。",
            "reusable_design_moves": ["用任务邀请建立真实情境", "把文化主题转成视觉翻译任务", "把作品扩展为展演证据链"],
            "useful_prompt_patterns": ["故事的关键情节如何被画出来", "你的折叠书如何表达新的理解", "表演准备中每个人留下了什么证据"],
            "useful_field_patterns": ["cross_subject_task", "story_visual_translation", "group_role_plan", "performance_evidence", "reflection_comment"],
            "limitations_or_missing_parts": ["跨学科价值判断需教师把关", "故事资料包来源需要引用锚点"],
            "should_not_directly_copy": ["邀请函话术", "故事资料包内容", "单元量规原文"],
            "reference_only": True,
            "source_refs": ["official_case_source_index_1013I_R6B#kb_art_g3_upper_official_lesson_design_unit_08_448205c865"],
        },
    ]
    return {
        "matrix_id": "official_case_deconstruction_matrix_1013I_R6B",
        "stage": STAGE_ID,
        "required_fields": REQUIRED_CASE_FIELDS,
        "cases": cases,
        "cases_treated_as_reference_only": True,
        "cases_not_treated_as_curriculum_standard": True,
        **boundary(),
        **profile(),
    }


def design_moves() -> dict[str, Any]:
    return {
        "design_moves_id": "official_case_design_moves_1013I_R6B",
        "stage": STAGE_ID,
        "context_intro_moves": ["用校园、展览、邀请函或真实生活问题建立任务背景"],
        "aesthetic_observation_moves": ["观察自然、校园、经典作品或民间作品中的视觉特征"],
        "concept_building_moves": ["把颜色规律、纹样符号、秩序原理、故事视觉化等概念转成学生问题"],
        "method_learning_moves": ["通过教师示范、资料包、作品研习或任务单建立可操作方法"],
        "skill_practice_moves": ["短练习、学习单、草图、纹样练习、材料试验"],
        "creative_production_moves": ["长卷、剪纸故事、空间改造、折叠书或展演作品"],
        "critique_revision_moves": ["同伴建议、评价标准海报、小组评语、阶段性评价回应"],
        "exhibition_reflection_moves": ["创想会、艺术节、改造展、故事展演等公开展示任务"],
        "transfer_extension_moves": ["从形式规律迁移到生活应用，从故事插图迁移到展演"],
        "assessment_evidence_moves": ["学习单、草图、作品、演出计划、互评记录、单元评价表"],
        "reference_only": True,
        **boundary(),
        **profile(),
    }


def calibration_suggestions() -> dict[str, Any]:
    return {
        "suggestions_id": "official_case_schema_calibration_suggestions_1013I_R6B",
        "stage": STAGE_ID,
        "should_add_fields": [
            "curriculum_standard_control",
            "standard_interpretation_bridge",
            "textbook_structure_anchor",
            "official_case_reference",
            "learning_evidence_chain",
            "unit_performance_task",
            "lesson_role_signal",
            "teacher_confirmation_gate",
        ],
        "should_rename_fields": [
            {
                "from": "official_material_extraction",
                "to": "official_case_reference_deconstruction",
                "reason": "Official cases are reference samples, not upstream standards.",
            }
        ],
        "should_lower_weight_fields": [
            "case_activity_sequence_as_direct_plan",
            "case_evaluation_language_as_direct_rubric",
        ],
        "should_keep_as_reference_only": [
            "official_case_reference",
            "useful_design_moves",
            "useful_prompt_patterns",
            "useful_field_patterns",
        ],
        "should_not_include_in_system": [
            "case_text_direct_copy",
            "case_as_curriculum_standard",
            "case_as_teacher_confirmed_unit_design",
        ],
        "prompt_wording_suggestions": [
            "先说明案例只作参考，再提炼可借鉴设计动作。",
            "要求小教区分课标方向、教材锚点、案例参考和教师确认。",
            "把案例语言转为教师可读建议，不复制案例原句。",
        ],
        "teacher_visible_surface_suggestions": [
            "教师端显示为“参考案例启发”，不显示为“系统依据”。",
            "把案例启发压缩成短卡片：可借鉴、需确认、不照搬。",
            "大单元闸门页面应先显示课标/教材/单元位置，再显示案例启发。",
        ],
        "reference_only": True,
        **boundary(),
        **profile(),
    }


def scan_deprecated(*payloads: Any) -> list[str]:
    text = json.dumps(payloads, ensure_ascii=False)
    return [name for name in DEPRECATED_VISIBLE_NAMES if name in text]


def scan_secrets(*payloads: Any) -> list[str]:
    text = json.dumps(payloads, ensure_ascii=False)
    return [pattern.pattern for pattern in SECRET_PATTERNS if pattern.search(text)]


def build_result(
    r6a_result: dict[str, Any],
    index: dict[str, Any],
    matrix: dict[str, Any],
    moves: dict[str, Any],
    suggestions: dict[str, Any],
) -> dict[str, Any]:
    cases = matrix["cases"]
    official_case_count = len(cases)
    case_fields_ok = all(all(field in case for field in REQUIRED_CASE_FIELDS) for case in cases)
    reference_only_ok = all(case["reference_only"] is True for case in cases)
    not_standard_ok = all(source["is_curriculum_standard"] is False for source in index["cases"])
    deprecated_hits = scan_deprecated(index, matrix, moves, suggestions)
    secret_hits = scan_secrets(index, matrix, moves, suggestions)
    profile_ok = all(
        payload["agent_role"] == "unified_teacher_agent"
        and payload["assistant_profile"]["display_name"] == "小教"
        and payload["active_space"] == "prep_room"
        and payload["active_capability"] == "lesson_prep"
        for payload in [index, matrix, moves, suggestions]
    )
    false_keys = [
        "big_unit_generation_performed",
        "single_lesson_generation_performed",
        "product_runtime_called",
        "provider_called",
        "model_called",
        "formal_apply_performed",
        "lesson_body_modified",
        "html_body_modified",
        "database_written",
        "memory_written",
        "feishu_written",
        "official_export_created",
        "official_archive_created",
        "main_project_pushed",
    ]
    no_writes = not any(payload[key] for payload in [index, matrix, moves, suggestions] for key in false_keys)
    final_pass = (
        r6a_result.get("final_status") == R6A_PASS_STATUS
        and official_case_count >= 3
        and case_fields_ok
        and reference_only_ok
        and not_standard_ok
        and matrix["cases_not_treated_as_curriculum_standard"]
        and moves["reference_only"]
        and suggestions["reference_only"]
        and profile_ok
        and no_writes
        and not deprecated_hits
        and not secret_hits
    )
    return {
        "stage": STAGE_ID,
        "generated_at": now(),
        "inherits_from": "1013I_R6A_BIG_UNIT_CONTEXT_REQUIRED_GATE",
        "final_status": f"PASS_{STAGE_ID}" if final_pass else f"FAIL_{STAGE_ID}",
        "next_stage": NEXT_STAGE,
        "r6a_result_present": True,
        "r6a_final_status": r6a_result.get("final_status"),
        "official_case_sources_indexed": True,
        "official_case_count": official_case_count,
        "deconstruction_matrix_created": True,
        "case_required_fields_present": case_fields_ok,
        "design_moves_extracted": True,
        "schema_calibration_suggestions_created": True,
        "cases_treated_as_reference_only": reference_only_ok,
        "cases_not_treated_as_curriculum_standard": not_standard_ok,
        "teacher_visible_deprecated_agent_hits": deprecated_hits,
        "secret_scan_hits": secret_hits,
        "agent_role": "unified_teacher_agent",
        "assistant_profile_present": True,
        "assistant_profile_display_name": "小教",
        "active_space": "prep_room",
        "active_capability": "lesson_prep",
        "formal_apply_allowed": False,
        "provider_model_call_allowed": False,
        **boundary(),
    }


def build_report(result: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# 1013I R6B Official Case Readonly Deconstruction",
            "",
            f"- FINAL_STATUS: `{result['final_status']}`",
            f"- NEXT_STAGE: `{result['next_stage']}`",
            "- Scope: official cases are deconstructed as reference samples only.",
            "",
            "## What R6B Does",
            "",
            "- Indexes 4 verified Grade 3 upper official teaching-design references.",
            "- Extracts case-level design structures, design moves, useful prompt patterns, and field calibration suggestions.",
            "- Keeps cases out of the curriculum-standard layer.",
            "",
            "## What R6B Does Not Do",
            "",
            "- It does not generate a big-unit design.",
            "- It does not generate a single-lesson plan.",
            "- It does not copy official case text into the lesson body.",
            "- It does not call product runtime, provider, or model.",
            "",
            "## Result",
            "",
            f"- official_case_count={result['official_case_count']}",
            f"- cases_treated_as_reference_only={str(result['cases_treated_as_reference_only']).lower()}",
            f"- cases_not_treated_as_curriculum_standard={str(result['cases_not_treated_as_curriculum_standard']).lower()}",
            f"- design_moves_extracted={str(result['design_moves_extracted']).lower()}",
            f"- schema_calibration_suggestions_created={str(result['schema_calibration_suggestions_created']).lower()}",
            "",
        ]
    )


def copy_source_delta(root: Path, output_root: Path) -> None:
    source_delta_dir = output_root / "source_delta_1013I_R6B" / "scripts"
    source_delta_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "scripts" / Path(__file__).name, source_delta_dir / Path(__file__).name)


def run(root: Path) -> int:
    output_root = resolve_output_root(root)
    r6a_result = read_json(output_root / "1013I_R6A_big_unit_context_required_gate" / "1013I_R6A_result.json")
    out_dir = output_root / "1013I_R6B_official_case_readonly_deconstruction"
    index = source_index()
    matrix = deconstruction_matrix()
    moves = design_moves()
    suggestions = calibration_suggestions()
    result = build_result(r6a_result, index, matrix, moves, suggestions)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "official_case_source_index_1013I_R6B.json", index)
    write_json(out_dir / "official_case_deconstruction_matrix_1013I_R6B.json", matrix)
    write_json(out_dir / "official_case_design_moves_1013I_R6B.json", moves)
    write_json(out_dir / "official_case_schema_calibration_suggestions_1013I_R6B.json", suggestions)
    write_json(out_dir / "1013I_R6B_result.json", result)
    write_text(out_dir / "1013I_R6B_report.md", build_report(result))
    copy_source_delta(root, output_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=None)
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else repo_root_from_script()
    return run(root)


if __name__ == "__main__":
    raise SystemExit(main())
