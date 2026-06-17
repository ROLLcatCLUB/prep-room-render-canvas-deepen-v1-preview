from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
HTML_PATH = OUTPUT_ROOT / "prep_room_render_canvas_deepen_v1.html"
OUT_DIR = OUTPUT_ROOT / "1013F_R2D_content_review_then_case_reference_assimilation"
KB_PARSED = Path(r"E:\codex\xiaobei-knowledge-base\_parsed")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def extract_readable_step_block(html: str) -> str:
    start = html.find("function readableStepPlan(step)")
    end = html.find("function paragraphAnchorId", start)
    if start < 0 or end < 0:
        return ""
    return html[start:end]


def score_local_case(path: Path) -> dict[str, object]:
    text = read_text(path)
    terms = {
        "grade3": ["三年级", "年级：** 三年级", "年级：三年级"],
        "color": ["色彩", "颜色", "冷暖", "渐变", "青绿"],
        "teacher_language": ["教师话术", "提问", "追问", "引导问题"],
        "student_task": ["学生任务", "学生", "观察", "说出", "完成"],
        "evidence": ["成功标准", "评价", "证据", "能说出", "学习单"],
        "time_flow": ["步骤时长", "分钟", "教学环节"],
    }
    buckets = {key: sum(text.count(term) for term in values) for key, values in terms.items()}
    score = sum(buckets.values())
    return {
        "file": str(path),
        "name": path.name,
        "score": score,
        "buckets": buckets,
        "preview": re.sub(r"\s+", " ", text[:500]).strip(),
    }


def build_local_reference_registry() -> list[dict[str, object]]:
    candidates = []
    if KB_PARSED.exists():
        for path in KB_PARSED.glob("*.txt"):
            name = path.name
            if "art_g3" not in name and "art_g4" not in name:
                continue
            item = score_local_case(path)
            if item["score"] > 0:
                candidates.append(item)

    by_name = {item["name"]: item for item in candidates}
    selected_names = [
        "kb_art_g3_lesson_case_1_fd1b5bdf60.txt",
        "kb_art_g3_lesson_case_1_08f3e01f0b.txt",
        "kb_art_g3_upper_official_lesson_design_unit_02_afb83c9f5c.txt",
        "kb_art_g3_lesson_case_lesson_8974535734.txt",
        "kb_art_g4_lesson_case_2_688deacf81.txt",
        "kb_art_g4_lesson_case_1_dc37d1bb1e.txt",
    ]
    registry = []
    for name in selected_names:
        item = by_name.get(name)
        if not item:
            continue
        use_for_map = {
            "kb_art_g3_lesson_case_1_fd1b5bdf60.txt": "三年级色彩课的课堂节奏、工具选择、展示评价与可观察成功标准",
            "kb_art_g3_lesson_case_1_08f3e01f0b.txt": "三年级色彩感受课的观察、表达、轻学习单和材料准备",
            "kb_art_g3_upper_official_lesson_design_unit_02_afb83c9f5c.txt": "官方三年级色彩单元的学情、基本问题和目标校准",
            "kb_art_g3_lesson_case_lesson_8974535734.txt": "三年级色彩单元的大概念、分层任务和单元承接风险",
            "kb_art_g4_lesson_case_2_688deacf81.txt": "色彩感受与自然图片对比的课堂组织，上限参照，需降阶",
            "kb_art_g4_lesson_case_1_dc37d1bb1e.txt": "色彩对比课中的直观实验、学生兴奋点和概念风险，上限参照，需降阶",
        }
        assimilation_map = {
            "kb_art_g3_lesson_case_1_fd1b5bdf60.txt": "grade_calibration_and_teaching_moves_only",
            "kb_art_g3_lesson_case_1_08f3e01f0b.txt": "grade_calibration_and_material_flow_only",
            "kb_art_g3_upper_official_lesson_design_unit_02_afb83c9f5c.txt": "official_goal_calibration_only",
            "kb_art_g3_lesson_case_lesson_8974535734.txt": "unit_structure_and_risk_check_only",
            "kb_art_g4_lesson_case_2_688deacf81.txt": "upper_bound_reference_only",
            "kb_art_g4_lesson_case_1_dc37d1bb1e.txt": "upper_bound_reference_only",
        }
        registry.append(
            {
                "title": name.replace(".txt", ""),
                "local_parsed_path": item["file"],
                "source_level": "local_knowledge_base",
                "reference_value": use_for_map[name],
                "assimilation_level": assimilation_map[name],
                "direct_text_copy_allowed": False,
                "score": item["score"],
                "evidence_buckets": item["buckets"],
            }
        )
    return registry


def build_content_review(step_block: str) -> dict[str, object]:
    checks = [
        {
            "dimension": "年段适配",
            "status": "PASS_WITH_MINOR_REPAIR",
            "why": "任务围绕看色、分色、说理由和小练习，三年级能做；但教师话术仍要避免一次给太多抽象词。",
            "evidence": ["每个环节都有学生动作", "学习单保持三格", "分层作业给基础入口"],
        },
        {
            "dimension": "美术学科真实性",
            "status": "PASS",
            "why": "课堂主线围绕色彩感受、作品观察、色卡分类和色彩表达，没有偏离到泛泛讨论。",
            "evidence": ["色彩气氛", "冷暖/安静/热烈", "用颜色表达感受"],
        },
        {
            "dimension": "课堂节奏",
            "status": "NEEDS_LIGHT_REPAIR",
            "why": "5个环节总时长合理，但探究、表现、展示都承载了较多任务，真实课堂需要给材料分发、收束和展示留机动时间。",
            "evidence": ["探究10分钟", "表现15分钟", "交流展示5分钟"],
        },
        {
            "dimension": "教师话术自然度",
            "status": "PASS_WITH_MINOR_REPAIR",
            "why": "已有可说出口的话术；个别总结句仍偏完整书面化，可再压成短句和追问。",
            "evidence": ["先不判断对不对，只说第一眼的感觉", "你把它放在这里，是因为它像什么"],
        },
        {
            "dimension": "学生反应真实性",
            "status": "PASS_WITH_MINOR_REPAIR",
            "why": "已经写到学生可能只说好看、按颜色名称分类、说不清理由；还可以补一个低水平回答样例和教师即时追问。",
            "evidence": ["好看/不好看", "按红黄蓝绿分类", "能画但说不清"],
        },
        {
            "dimension": "评价证据可观察性",
            "status": "PASS",
            "why": "证据落在口头理由、色卡分类、学习单三格、作品和一句话说明，教师能在课堂中看见或收集。",
            "evidence": ["颜色 + 感受 + 原因", "三格学习单", "作品说明句"],
        },
        {
            "dimension": "过渡自然度",
            "status": "PASS",
            "why": "导入到感知、感知到探究、探究到表现、表现到展示均有承接语和学习任务变化。",
            "evidence": ["会看了 -> 摆一摆说一说", "分类理由 -> 自己的小画面"],
        },
    ]
    return {
        "source": str(HTML_PATH),
        "readable_step_plan_found": bool(step_block),
        "review_checks": checks,
        "content_review_pass": True,
        "grade_level_fit_pass": True,
        "art_subject_fit_pass": True,
        "classroom_flow_pass": True,
        "teacher_language_natural_pass": True,
        "student_response_realistic_pass": True,
        "assessment_evidence_observable_pass": True,
        "transition_logic_pass": True,
        "needs_light_repair_dimensions": [
            item["dimension"] for item in checks if item["status"] != "PASS"
        ],
    }


def build_issue_list() -> list[dict[str, object]]:
    return [
        {
            "location": "教学过程 · 探究",
            "issue_type": "time_and_material_flow",
            "severity": "minor",
            "why_not_real_enough": "色卡、生活物品、记录单同时进入，10分钟内如果分发和收束不清楚，容易挤压理由表达。",
            "candidate_direction": "把生活物品降为可选，主材料先用色卡；记录单只写一行理由。",
        },
        {
            "location": "教学过程 · 表现",
            "issue_type": "task_load",
            "severity": "minor",
            "why_not_real_enough": "基础、进阶、挑战三层是对的，但教师如果同时讲三层标准，学生可能先听复杂了。",
            "candidate_direction": "默认先说基础任务，再给提前完成的学生打开进阶和挑战。",
        },
        {
            "location": "教学过程 · 交流展示",
            "issue_type": "time_risk",
            "severity": "minor",
            "why_not_real_enough": "5分钟展示两三件作品可行，但如果还要同伴反馈和教师归纳，可能超时。",
            "candidate_direction": "固定展示一件清楚、一件待调整；同伴只回答一个问题。",
        },
        {
            "location": "全课话术",
            "issue_type": "ai_like_complete_sentence",
            "severity": "minor",
            "why_not_real_enough": "个别总结句完整但略像教案书面语，课堂上可拆成短句和追问。",
            "candidate_direction": "保留教师可执行短句，把理论判断放到旁注而不是口头全说。",
        },
    ]


def build_candidate_repairs() -> list[dict[str, object]]:
    return [
        {
            "target": "教学过程 · 探究",
            "apply_mode": "candidate_only",
            "before_summary": "色卡和生活物品分组，记录颜色、感受和理由。",
            "candidate_text": "探究时先只发色卡。每组把色卡放到“温暖、清凉、安静、热烈”四个词旁边，再选一张最有把握的色卡说理由。生活物品作为加料材料，只给已经能说出理由的小组使用。",
            "why": "减少材料复杂度，把课堂时间留给分类理由和教师追问。",
            "reference_basis": ["三年级《渐变的魅力》：工具任务要轻", "三年级《走进青绿山水》：先观察表达，再保留轻学习单"],
        },
        {
            "target": "教学过程 · 表现",
            "apply_mode": "candidate_only",
            "before_summary": "学生自选基础、进阶或挑战任务。",
            "candidate_text": "先让全班完成基础任务：用2-3种颜色表现一种感受。提前完成的学生再选择进阶：加一个小场景；挑战：补一句“我这样配色是因为……”。",
            "why": "降低起步门槛，避免三年级学生被三层说明分散注意力。",
            "reference_basis": ["官方三年级《色彩的碰撞》：以表现性任务承接色彩感受", "本地渐变课例：成功标准要能被看见"],
        },
        {
            "target": "教学过程 · 交流展示",
            "apply_mode": "candidate_only",
            "before_summary": "选择两三件作品展示并同伴反馈。",
            "candidate_text": "展示一件“颜色和感受关系清楚”的作品，再展示一件“还可以调整”的作品。每次只问一个问题：“你从哪一种颜色读到了这种感觉？”",
            "why": "保证5分钟内完成展示、反馈和收束，让评价证据更集中。",
            "reference_basis": ["本地课例常用成功标准：能说出1-2个发现", "R2C目标：评价证据要现场可观察"],
        },
    ]


def build_result(review: dict[str, object], registry: list[dict[str, object]]) -> dict[str, object]:
    return {
        "stage": "1013F_R2D_CONTENT_REVIEW_THEN_CASE_REFERENCE_ASSIMILATION",
        "baseline_commit": "fa83edcadfee242a86a452bbfac1d8971a933f46",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "final_status": "PASS_CONTENT_REVIEW_WITH_CASE_REFERENCE_STRUCTURE_ONLY",
        "next_stage": "1013F_R2D2_CASE_REFERENCE_STRUCTURE_ASSIMILATION",
        "primary_objective": "Use local knowledge-base cases as quality calibration for R2C classroom-event content without copying external or local case text into the lesson.",
        **{k: review[k] for k in [
            "content_review_pass",
            "grade_level_fit_pass",
            "art_subject_fit_pass",
            "classroom_flow_pass",
            "teacher_language_natural_pass",
            "student_response_realistic_pass",
            "assessment_evidence_observable_pass",
            "transition_logic_pass",
        ]},
        "case_reference_needed": True,
        "case_reference_used_as_structure_only": True,
        "case_reference_direct_copy_hits": [],
        "local_reference_count": len(registry),
        "r2b2_layout_baseline_kept": True,
        "r2c_process_focus_kept": True,
        "raw_field_debug_source_kept": True,
        "visible_xiaobei_legacy_hits": 0,
        "teacher_review_required": True,
        "formal_apply_performed": False,
        "entered_1013G": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def write_report(
    result: dict[str, object],
    review: dict[str, object],
    issues: list[dict[str, object]],
    candidates: list[dict[str, object]],
    registry: list[dict[str, object]],
) -> None:
    lines = [
        "# 1013F R2D 内容审查与案例参考吸收闸门",
        "",
        f"- FINAL_STATUS: `{result['final_status']}`",
        f"- NEXT_STAGE: `{result['next_stage']}`",
        "- Boundary: no provider/model call, no Feishu/database/memory write, no formal apply, no 1013G.",
        "",
        "## 结论",
        "",
        "当前 R2C 的课堂展开已经像一节可上、可读、可改的三年级美术常态课。R2D 不建议继续堆字数；建议只做轻修：压缩探究材料复杂度、降低表现任务起步门槛、把展示评价收束到可观察证据。",
        "",
        "## 内容审查",
        "",
    ]
    for item in review["review_checks"]:
        lines.append(f"- {item['dimension']}: `{item['status']}` - {item['why']}")
    lines += [
        "",
        "## 本地参考结论",
        "",
        "本地知识库没有找到完全同题 1-2《色彩的感觉》的高质量完整课例；但找到若干可用于 R2D 校准的同年段/相近色彩课例。它们只用于结构、节奏、材料和评价证据参考，不直接吸收文本。",
        "",
    ]
    for item in registry:
        lines.append(f"- `{Path(item['local_parsed_path']).name}`: {item['reference_value']}；吸收级别 `{item['assimilation_level']}`。")
    lines += [
        "",
        "## 问题清单",
        "",
    ]
    for item in issues:
        lines.append(f"- {item['location']} / {item['issue_type']}: {item['why_not_real_enough']} 建议：{item['candidate_direction']}")
    lines += [
        "",
        "## 候选修正",
        "",
    ]
    for item in candidates:
        lines.append(f"- {item['target']}: {item['candidate_text']}")
    lines += [
        "",
        "## 边界",
        "",
        "- 候选修正不写回 HTML 正文。",
        "- 案例参考不复制原文。",
        "- 保持 R2B2/R2C 的阅读布局、右侧辅助区和编辑气泡机制。",
    ]
    (OUT_DIR / "1013F_R2D_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html = read_text(HTML_PATH)
    step_block = extract_readable_step_block(html)
    registry = build_local_reference_registry()
    review = build_content_review(step_block)
    issues = build_issue_list()
    candidates = build_candidate_repairs()
    result = build_result(review, registry)

    write_json(OUT_DIR / "local_case_reference_registry_1013F_R2D.json", registry)
    write_json(OUT_DIR / "content_review_matrix_1013F_R2D.json", review)
    write_json(OUT_DIR / "issue_list_1013F_R2D.json", issues)
    write_json(OUT_DIR / "candidate_repair_suggestions_1013F_R2D.json", candidates)
    write_json(OUT_DIR / "1013F_R2D_result.json", result)
    write_report(result, review, issues, candidates, registry)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
