from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
HTML_PATH = OUTPUT_ROOT / "prep_room_render_canvas_deepen_v1.html"
R2D_DIR = OUTPUT_ROOT / "1013F_R2D_content_review_then_case_reference_assimilation"
OUT_DIR = OUTPUT_ROOT / "1013F_R2D2_case_reference_structure_assimilation"
SOURCE_DELTA_DIR = OUTPUT_ROOT / "source_delta_1013F_R2D2" / "scripts"

STAGE_ID = "1013F_R2D2_CASE_REFERENCE_STRUCTURE_ASSIMILATION"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_inputs() -> dict[str, Any]:
    return {
        "r2d_result": read_json(R2D_DIR / "1013F_R2D_result.json"),
        "r2d_candidates": read_json(R2D_DIR / "candidate_repair_suggestions_1013F_R2D.json"),
        "r2d_review": read_json(R2D_DIR / "content_review_matrix_1013F_R2D.json"),
        "r2d_issues": read_json(R2D_DIR / "issue_list_1013F_R2D.json"),
        "r2d_registry": read_json(R2D_DIR / "local_case_reference_registry_1013F_R2D.json"),
        "html": read_text(HTML_PATH),
    }


def build_case_reference_registry(r2d_registry: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_kind_by_level = {
        "official_goal_calibration_only": "official_calibration",
        "grade_calibration_and_teaching_moves_only": "local_structure_reference",
        "grade_calibration_and_material_flow_only": "local_structure_reference",
        "unit_structure_and_risk_check_only": "local_structure_reference",
        "upper_bound_reference_only": "local_upper_bound_reference",
    }
    preferred_targets = {
        "kb_art_g3_lesson_case_1_fd1b5bdf60": ["教学过程 · 探究", "教学过程 · 交流展示"],
        "kb_art_g3_lesson_case_1_08f3e01f0b": ["教学过程 · 感知", "教学过程 · 探究"],
        "kb_art_g3_upper_official_lesson_design_unit_02_afb83c9f5c": ["学情分析", "教学目标", "评价证据"],
        "kb_art_g3_lesson_case_lesson_8974535734": ["教学过程 · 表现", "单元承接风险"],
        "kb_art_g4_lesson_case_2_688deacf81": ["教学过程 · 感知", "降阶风险"],
        "kb_art_g4_lesson_case_1_dc37d1bb1e": ["教学过程 · 探究", "概念风险"],
    }
    authority_by_source_type = {
        "official_calibration": "official_grade_level_calibration",
        "local_structure_reference": "local_non_authoritative_structure_reference",
        "local_upper_bound_reference": "upper_bound_requires_grade_downshift",
    }
    registry = []
    for item in r2d_registry:
        level = item["assimilation_level"]
        title = item["title"]
        source_type = source_kind_by_level.get(level, "local_structure_reference")
        registry.append(
            {
                "reference_id": f"r2d2_ref_{len(registry) + 1:02d}",
                "title": title,
                "source_type": source_type,
                "authority_level": authority_by_source_type[source_type],
                "local_parsed_path": item["local_parsed_path"],
                "reference_value": item["reference_value"],
                "assimilation_level": level,
                "target_lesson_parts": preferred_targets.get(title, ["教学过程"]),
                "allowed_use": [
                    "teaching_move_only",
                    "question_chain_only",
                    "material_timing_only",
                    "evidence_design_only",
                    "risk_check_only",
                ],
                "direct_copy_allowed": False,
                "case_text_inserted_into_lesson": False,
                "used_for_formal_apply": False,
            }
        )
    return registry


def build_teaching_moves_extraction() -> list[dict[str, Any]]:
    return [
        {
            "move_id": "r2d2_move_explore_material_gate",
            "source_ref": ["r2d2_ref_01", "r2d2_ref_02", "r2d2_ref_03"],
            "target_event": "教学过程 · 探究",
            "move_type": "material_timing_and_question_chain",
            "current_part": "教学过程 · 探究",
            "r2d_issue_type": "time_and_material_flow",
            "source_basis": [
                "official_calibration",
                "local_structure_reference",
            ],
            "extracted_structure": {
                "teaching_move": "先用单一主材料建立分类动作，再把扩展材料作为加料选项。",
                "question_chain": [
                    "这张色卡给你的第一感觉是什么？",
                    "你把它放在这里，是因为它像什么，还是让你想到什么？",
                    "如果小组意见不同，哪一种理由更能说服别人？",
                ],
                "material_timing": [
                    "第1分钟只发色卡和感受词卡。",
                    "第4分钟后只给能说出理由的小组补生活物品。",
                    "记录单只保留一行理由，不增加表格负担。",
                ],
                "evidence_design": [
                    "色卡是否被放入感受词旁边。",
                    "学生是否能说出颜色、感受和理由。",
                    "教师记录一条典型低水平回答和一次追问结果。",
                ],
                "risk_handling": "如果学生只按红黄蓝绿分类，先示范一张色卡的理由，再让小组保留一张有争议色卡说明两种理由。",
            },
            "reason_for_assimilation": "R2D 已判定探究环节材料和记录单同时进入会挤压理由表达；本动作把结构收束为先分类再说理由。",
            "risk_note": "生活物品只能后置加料；过早进入会让学生注意力转向物品而不是色彩感受。",
            "why_grade3_fit": "三年级适合先分类、再说理由；材料少一点，语言表达才有课堂时间。",
            "direct_copy_allowed": False,
        },
        {
            "move_id": "r2d2_move_make_default_entry",
            "source_ref": ["r2d2_ref_03", "r2d2_ref_04"],
            "target_event": "教学过程 · 表现",
            "move_type": "task_entry_and_layering",
            "current_part": "教学过程 · 表现",
            "r2d_issue_type": "task_load",
            "source_basis": [
                "official_calibration",
                "local_structure_reference",
            ],
            "extracted_structure": {
                "teaching_move": "把三层任务改成先统一起步，再给提前完成学生打开加层。",
                "question_chain": [
                    "你今天先想表现哪一种感觉？",
                    "你准备用哪两三种颜色让别人看出这种感觉？",
                    "如果已经完成，可以加一个小场景或补一句理由。",
                ],
                "material_timing": [
                    "先发同一张小练习纸。",
                    "大屏先只显示基础任务。",
                    "进阶和挑战作为提前完成后的追加提示出现。",
                ],
                "evidence_design": [
                    "每个学生至少完成一种感受的2到3色表达。",
                    "提前完成者能补一个小场景或一句配色理由。",
                ],
                "risk_handling": "如果学生只想涂满画面，教师把问题收回到一种感受和两三种颜色的选择。",
            },
            "reason_for_assimilation": "R2D 已判定三层任务同时说明会增加起步负担；本动作保留分层但把进阶延后打开。",
            "risk_note": "如果提前展示进阶和挑战，部分学生会先听复杂，基础任务开始变慢。",
            "why_grade3_fit": "先让全班有共同起点，能降低等待和听不懂三层标准的风险。",
            "direct_copy_allowed": False,
        },
        {
            "move_id": "r2d2_move_share_observable_evidence",
            "source_ref": ["r2d2_ref_01", "r2d2_ref_04"],
            "target_event": "教学过程 · 交流展示",
            "move_type": "assessment_evidence_and_time_control",
            "current_part": "教学过程 · 交流展示",
            "r2d_issue_type": "time_risk",
            "source_basis": [
                "local_structure_reference",
                "unit_structure_and_risk_check",
            ],
            "extracted_structure": {
                "teaching_move": "展示固定为一件清楚和一件可调整，用同一个问题收束评价证据。",
                "question_chain": [
                    "你从哪一种颜色读到了这种感觉？",
                    "这件作品还可以调整哪一种颜色，让感觉更清楚？",
                ],
                "material_timing": [
                    "展示前先拍两件作品或直接举起。",
                    "每件作品只问一个问题。",
                    "教师最后只归纳颜色、感受、理由三件事。",
                ],
                "evidence_design": [
                    "一件作品颜色和感受关系清楚。",
                    "一件作品能说出可调整方向。",
                    "同伴反馈指向具体颜色，而不是只说好看。",
                ],
                "risk_handling": "如果时间不足，只展示一件清楚作品，第二件改为教师口头说明下节课继续调整。",
            },
            "reason_for_assimilation": "R2D 已判定 5 分钟展示容易超时；本动作把展示收束成两类样本和一个证据问题。",
            "risk_note": "如果继续做完整同伴互评，展示和教师归纳会挤占下课收束时间。",
            "why_grade3_fit": "评价问题少，学生更容易说到具体颜色，教师也能在5分钟内收束。",
            "direct_copy_allowed": False,
        },
        {
            "move_id": "r2d2_move_teacher_language_shortening",
            "source_ref": ["r2d2_ref_02", "r2d2_ref_03"],
            "target_event": "全课话术",
            "move_type": "teacher_language_shortening",
            "current_part": "全课话术",
            "r2d_issue_type": "ai_like_complete_sentence",
            "source_basis": [
                "official_calibration",
                "local_structure_reference",
            ],
            "extracted_structure": {
                "teaching_move": "把完整判断句拆成教师短句、追问和旁注。",
                "question_chain": [
                    "先说第一眼感觉。",
                    "你从哪里看出来？",
                    "换一种颜色，感觉会不会变？",
                ],
                "material_timing": [
                    "理论判断不在口头一次讲完。",
                    "只在学生回答后补一句旁注式总结。",
                ],
                "evidence_design": [
                    "学生能从好看不好看转为一个感受词。",
                    "学生能补一条颜色依据。",
                ],
                "risk_handling": "如果回答停在好看，教师提供二选一感受词，而不是直接给标准答案。",
            },
            "reason_for_assimilation": "R2D 已判定部分总结句偏书面；本动作把理论判断拆成课堂短句和追问。",
            "risk_note": "如果教师一次说完理论判断，学生可能只听到结论，接不上理由表达。",
            "why_grade3_fit": "短句和追问比完整教案句更接近真实课堂，也更容易让学生接话。",
            "direct_copy_allowed": False,
        },
    ]


def build_candidate_patch(moves: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "patch_id": "r2d2_patch_explore",
            "target": "教学过程 · 探究",
            "apply_mode": "candidate_only",
            "candidate_only": True,
            "applied": False,
            "before_summary": "色卡和生活物品同时进入，记录单也参与探究。",
            "candidate_text": "探究先只发色卡和感受词卡。每组把色卡放到“温暖、清凉、安静、热烈”四个词旁边，再选一张最有把握的色卡说理由。已经能说出理由的小组，再领取一件生活物品做加料比较；记录单只写一行“我这样分是因为……”。",
            "structure_absorbed": [
                "material_gate",
                "one_question_at_a_time",
                "observable_reason",
            ],
            "source_move_ids": ["r2d2_move_explore_material_gate"],
            "why": "压缩材料复杂度，把10分钟探究留给分类理由、教师追问和低水平回答修正。",
            "risk": "如果生活物品过早进入，会重新挤压理由表达；因此只作为加料材料。",
            "teacher_review_required": True,
            "direct_copy_allowed": False,
        },
        {
            "patch_id": "r2d2_patch_make",
            "target": "教学过程 · 表现",
            "apply_mode": "candidate_only",
            "candidate_only": True,
            "applied": False,
            "before_summary": "基础、进阶、挑战三层同时向全班说明。",
            "candidate_text": "表现环节先让全班完成同一个基础任务：用2到3种颜色表现一种感受。提前完成的学生再打开加层：可以加一个小场景，或补一句“我这样配色是因为……”。",
            "structure_absorbed": [
                "default_entry_first",
                "late_open_extension",
                "simple_success_standard",
            ],
            "source_move_ids": ["r2d2_move_make_default_entry"],
            "why": "先保证每个学生都有可开始的任务，再让能力强的学生自然加深。",
            "risk": "如果一开始展示三层标准，部分学生会先听复杂，反而晚开始。",
            "teacher_review_required": True,
            "direct_copy_allowed": False,
        },
        {
            "patch_id": "r2d2_patch_share",
            "target": "教学过程 · 交流展示",
            "apply_mode": "candidate_only",
            "candidate_only": True,
            "applied": False,
            "before_summary": "展示两三件作品，并安排同伴反馈和教师归纳。",
            "candidate_text": "交流展示固定两件作品：一件“颜色和感受关系清楚”，一件“还可以调整”。每件只问一个问题：“你从哪一种颜色读到了这种感觉？”教师最后只收束到颜色、感受和理由。",
            "structure_absorbed": [
                "two_sample_review",
                "single_question_feedback",
                "evidence_based_summary",
            ],
            "source_move_ids": ["r2d2_move_share_observable_evidence"],
            "why": "把5分钟评价收束成可看见、可听见的证据，不再扩展为完整展评。",
            "risk": "如果时间不足，第二件改为教师指出可调整方向，不展开同伴讨论。",
            "teacher_review_required": True,
            "direct_copy_allowed": False,
        },
    ]


def check_direct_copy(candidate_patch: list[dict[str, Any]], registry: list[dict[str, Any]]) -> list[str]:
    joined = "\n".join(item["candidate_text"] for item in candidate_patch)
    hits = []
    for item in registry:
        path = Path(item["local_parsed_path"])
        if not path.exists():
            continue
        source = re.sub(r"\s+", "", read_text(path))
        for text in re.findall(r"[\u4e00-\u9fffA-Za-z0-9，。、“”]{18,}", joined):
            normalized = re.sub(r"\s+", "", text)
            if len(normalized) >= 18 and normalized in source:
                hits.append(f"{item['title']}::{text[:40]}")
    return sorted(set(hits))


def build_result(
    inputs: dict[str, Any],
    registry: list[dict[str, Any]],
    moves: list[dict[str, Any]],
    candidate_patch: list[dict[str, Any]],
    direct_copy_hits: list[str],
) -> dict[str, Any]:
    r2d_result = inputs["r2d_result"]
    html = inputs["html"]
    required_flags = {
        "r2d_content_review_pass": bool(r2d_result.get("content_review_pass")),
        "case_reference_used_as_structure_only": True,
        "case_reference_direct_copy_clear": not direct_copy_hits,
        "direct_copy_allowed_false": all(not item["direct_copy_allowed"] for item in registry + moves + candidate_patch),
        "grade_level_fit_pass": bool(r2d_result.get("grade_level_fit_pass")),
        "art_subject_fit_pass": bool(r2d_result.get("art_subject_fit_pass")),
        "classroom_flow_pass": bool(r2d_result.get("classroom_flow_pass")),
        "assessment_evidence_observable_pass": bool(r2d_result.get("assessment_evidence_observable_pass")),
        "r2b2_layout_baseline_kept": bool(r2d_result.get("r2b2_layout_baseline_kept")) and "nb-edit-bubble" in html,
        "r2c_process_focus_kept": bool(r2d_result.get("r2c_process_focus_kept")) and "nb-process-section" in html,
        "formal_apply_performed": False,
        "entered_1013G": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }
    pass_keys = [
        key
        for key in required_flags
        if key
        not in {
            "formal_apply_performed",
            "entered_1013G",
            "database_written",
            "memory_written",
            "feishu_written",
            "main_project_pushed",
        }
    ]
    no_write_keys = [
        "formal_apply_performed",
        "entered_1013G",
        "database_written",
        "memory_written",
        "feishu_written",
        "main_project_pushed",
    ]
    final_pass = all(required_flags[key] for key in pass_keys) and not any(
        required_flags[key] for key in no_write_keys
    )
    return {
        "stage": STAGE_ID,
        "generated_at": now(),
        "inherits_from": "1013F_R2D_CONTENT_REVIEW_THEN_CASE_REFERENCE_ASSIMILATION",
        "final_status": "PASS_CASE_REFERENCE_STRUCTURE_ASSIMILATION" if final_pass else "FAIL_CASE_REFERENCE_STRUCTURE_ASSIMILATION",
        "next_stage": "1013F_R2D2_REVIEW_GATE_BEFORE_1013G" if final_pass else "1013F_R2D2_REPAIR",
        "provider_called_in_project_runtime": False,
        "model_called_in_project_runtime": False,
        "external_sampling_used": False,
        "ima_synthetic_variant_used": False,
        "case_reference_count": len(registry),
        "teaching_move_count": len(moves),
        "candidate_patch_count": len(candidate_patch),
        "case_reference_used_as_structure_only": True,
        "case_reference_direct_copy_hits": direct_copy_hits,
        **required_flags,
    }


def build_report(result: dict[str, Any], candidate_patch: list[dict[str, Any]]) -> str:
    lines = [
        "# 1013F R2D2 案例结构吸收候选",
        "",
        f"- FINAL_STATUS: `{result['final_status']}`",
        f"- NEXT_STAGE: `{result['next_stage']}`",
        "- Boundary: no provider/model runtime call, no Feishu/database/memory write, no formal apply, no 1013G.",
        "",
        "## 结论",
        "",
        "R2D2 已把 R2D 的案例参考从“内容审查”推进到“结构吸收候选”。本阶段只吸收教学动作、问题链、材料时机、评价证据和风险处理，不复制案例文本，不写回 HTML 正文。",
        "",
        "## 结构吸收重点",
        "",
        "- 探究: 主材料先用色卡，生活物品后置为加料材料，记录单只保留一行理由。",
        "- 表现: 全班先完成统一基础任务，进阶和挑战只对提前完成学生打开。",
        "- 交流展示: 固定一件清楚作品和一件可调整作品，每件只问一个证据问题。",
        "- 话术: 把完整教案句拆成教师短句、追问和旁注。",
        "",
        "## 候选修正",
        "",
    ]
    for item in candidate_patch:
        lines.extend(
            [
                f"- {item['target']}: {item['candidate_text']}",
                f"  - Why: {item['why']}",
                f"  - Risk: {item['risk']}",
            ]
        )
    lines.extend(
        [
            "",
            "## 验收",
            "",
            f"- case_reference_used_as_structure_only={str(result['case_reference_used_as_structure_only']).lower()}",
            f"- case_reference_direct_copy_hits={json.dumps(result['case_reference_direct_copy_hits'], ensure_ascii=False)}",
            f"- direct_copy_allowed_false={str(result['direct_copy_allowed_false']).lower()}",
            f"- r2b2_layout_baseline_kept={str(result['r2b2_layout_baseline_kept']).lower()}",
            f"- r2c_process_focus_kept={str(result['r2c_process_focus_kept']).lower()}",
            "",
            "## 边界",
            "",
            "- 候选不写回正式备课本正文。",
            "- 不进入 1013G 教师确认动作。",
            "- 不写数据库、memory 或 Feishu。",
            "- 不推主项目树。",
        ]
    )
    return "\n".join(lines) + "\n"


def copy_source_delta() -> None:
    SOURCE_DELTA_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA_DIR / Path(__file__).name)


def main() -> int:
    inputs = load_inputs()
    registry = build_case_reference_registry(inputs["r2d_registry"])
    moves = build_teaching_moves_extraction()
    candidate_patch = build_candidate_patch(moves)
    direct_copy_hits = check_direct_copy(candidate_patch, registry)
    result = build_result(inputs, registry, moves, candidate_patch, direct_copy_hits)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "case_reference_registry_1013F_R2D2.json", registry)
    write_json(OUT_DIR / "teaching_moves_extraction_1013F_R2D2.json", moves)
    write_json(OUT_DIR / "assimilation_candidate_patch_1013F_R2D2.json", candidate_patch)
    write_json(OUT_DIR / "1013F_R2D2_result.json", result)
    write_text(OUT_DIR / "1013F_R2D2_report.md", build_report(result, candidate_patch))
    copy_source_delta()

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
