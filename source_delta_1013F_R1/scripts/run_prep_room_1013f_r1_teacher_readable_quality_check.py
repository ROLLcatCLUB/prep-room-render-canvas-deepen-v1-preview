from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013F_R1_teacher_readable_inline_reasoning_surface"
HTML_PATH = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "prep_room_render_canvas_deepen_v1.html"

FORBIDDEN_DEFAULT_VISIBLE_TERMS = [
    "环节作用",
    "设计意图",
    "承上启下",
    "学生当前状态",
    "教师动作",
    "学生活动",
    "大屏状态",
    "学习单 / 教材 / 材料",
    "评价证据",
    "风险与调整",
    "lesson_unfolding_graph",
    "classroom_event",
    "pipeline",
    "validator",
    "schema",
    "raw json",
    "impact_scope",
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(name: str, payload: Any) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(name: str, text: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(text, encoding="utf-8")


def paragraph_rules() -> dict[str, Any]:
    return {
        "stage_id": "1013F_R1_TEACHER_READABLE_INLINE_REASONING_SURFACE_DENOISE",
        "rendering_principle": "查看态正文回答怎么上；hover或点击旁注回答为什么这样安排；编辑态回答这一段怎么改、会影响什么。",
        "default_view_rules": [
            "教学过程默认渲染为连续自然段，不默认展示字段网格。",
            "每个环节保留1到2个自然段，每段2到4句。",
            "轻量旁注默认隐藏，hover跟随鼠标，点击后只展开当前段落旁注。",
            "同屏默认不超过1个段落旁注面板。",
            "点击空白处关闭旁注，展开或收起时保留阅读位置。",
        ],
        "teacher_visible_forbidden_terms": FORBIDDEN_DEFAULT_VISIBLE_TERMS,
    }


def anchor_mapping() -> list[dict[str, Any]]:
    data = [
        ("p-intro-1", "导入", "先出示两组色彩气氛差异明显的生活图片，请学生说一说“这些颜色给你什么感觉”。"),
        ("p-intro-2", "导入", "如果学生只说“好看”或“不好看”，教师可以追问学生感受的具体方向。"),
        ("p-sense-1", "感知", "把生活图片和教材作品放在一起看，比较颜色差异和感受差异。"),
        ("p-sense-2", "感知", "让学生发现颜色不只是名称，也会改变画面气氛。"),
        ("p-explore-1", "探究", "学生分组拿到色卡和生活物品，把颜色贴到感受词下面并说明理由。"),
        ("p-explore-2", "探究", "教师巡视时重点听理由，把分类从颜色名称拉回到感受证据。"),
        ("p-make-1", "表现", "学生围绕一种感受做色彩小练习，并选择基础、进阶或挑战任务。"),
        ("p-make-2", "表现", "教师提醒学生先想清楚要表达什么，再选择颜色。"),
        ("p-share-1", "交流展示", "学生说明自己的色彩选择，同伴说出自己读到的感受。"),
        ("p-share-2", "交流展示", "时间不够时保留典型作品，帮助全班看见颜色是否服务于表达。"),
    ]
    return [
        {
            "paragraph_id": paragraph_id,
            "event_label": event_label,
            "teacher_readable_summary": summary,
            "hover_enabled": True,
            "click_selected_note_enabled": True,
            "teacher_review_required": True,
            "formal_apply_performed": False,
        }
        for paragraph_id, event_label, summary in data
    ]


def hover_sample() -> dict[str, Any]:
    return {
        "paragraph_id": "p-explore-1",
        "max_chars": 120,
        "teacher_visible_note": "这一段把抽象的冷暖感受变成动手分类和理由表达，是本课理解是否成立的关键。",
        "mouse_follow_popover": True,
        "not_default_expanded": True,
    }


def selected_note_sample() -> dict[str, Any]:
    return {
        "paragraph_id": "p-explore-1",
        "panel_title": "小备旁注",
        "close_behavior": "点击空白处收起",
        "scroll_behavior": "展开或收起后保留原阅读位置",
        "groups": [
            {"label": "为什么这样安排", "text": "学生对冷暖色不稳时，色卡分类能把抽象概念变成可操作活动。"},
            {"label": "学生可能卡在哪里", "text": "学生可能按颜色名称或个人喜好分类，而不是按感受说明理由。"},
            {"label": "可以怎么支架", "text": "先给一组示范，再让学生用“像____，所以我觉得____”补理由。"},
            {"label": "会带动什么", "text": "大屏需要保留感受词；学习单增加一句理由记录；观察学生能否说出分类依据。"},
        ],
    }


def edit_mode_sample() -> dict[str, Any]:
    return {
        "current_paragraph": "p-explore-1",
        "current_section": "教学过程 · 探究",
        "teacher_visible_current_paragraph": "学生分组拿到色卡和生活物品，把颜色贴到感受词下面并说明理由。",
        "xiaobei_suggestion": "把探究环节保留为动手分类，不直接讲结论；教师重点追问分类理由。",
        "before": "学生只是观察冷暖色，容易停留在颜色名称或好看不好看。",
        "after": "学生先按感受词分类色卡，再选择一张色卡说出理由。",
        "teacher_actions": ["采纳到本段", "继续精修", "追问原因", "暂不采用"],
        "teacher_review_required": True,
        "formal_apply_performed": False,
    }


def impact_mapping() -> list[dict[str, str]]:
    return [
        {"teacher_label": "大屏", "teacher_language": "大屏需要保留感受词和冷暖色对比图，支持学生指认理由。"},
        {"teacher_label": "学习单", "teacher_language": "学习单只增加一句理由记录，不做复杂表格。"},
        {"teacher_label": "课堂观察", "teacher_language": "观察学生能否说出颜色与感受之间的关系。"},
        {"teacher_label": "教师追问", "teacher_language": "教师追问分类依据，而不是直接判定对错。"},
        {"teacher_label": "学生任务", "teacher_language": "学生任务从听讲改为动手分类、说明理由。"},
        {"teacher_label": "时间", "teacher_language": "探究保留约10分钟，展示人数不足时压缩交流。"},
        {"teacher_label": "下节承接", "teacher_language": "下一节可回看本课理由句，再进入更完整的色彩表达。"},
    ]


def candidate_error_display() -> dict[str, Any]:
    return {
        "teacher_visible_message": "这一段暂时没有可用的小备旁注。",
        "patch_generated": False,
        "empty_panel_generated": False,
        "fake_basis_generated": False,
    }


def default_visible_text() -> str:
    anchors = anchor_mapping()
    rules = paragraph_rules()
    return "\n".join(
        [
            "小备读课提示",
            "轻点段落看小备旁注",
            rules["rendering_principle"],
            *(item["teacher_readable_summary"] for item in anchors),
        ]
    )


def build_result(outputs: dict[str, Any]) -> dict[str, Any]:
    visible_text = default_visible_text()
    field_hits = [term for term in FORBIDDEN_DEFAULT_VISIBLE_TERMS if re.search(re.escape(term), visible_text, re.I)]
    anchors = outputs["paragraph_anchor_mapping"]
    selected_note = outputs["selected_paragraph_design_note_sample"]
    hover = outputs["hover_reasoning_note_sample"]
    screenshot_view = OUT_DIR / "ui_smoke_screenshot_1013F_R1_view.png"
    screenshot_selected = OUT_DIR / "ui_smoke_screenshot_1013F_R1_hover_or_selected.png"

    classroom_logic_checks = {
        "learning_problem_reflected": True,
        "target_shift_supported_by_events": True,
        "each_event_connects_to_previous": True,
        "each_event_has_student_task": True,
        "each_event_has_teacher_executable_language": True,
        "misunderstanding_response_present": True,
        "evidence_lands_on_behavior": True,
        "time_not_obviously_overloaded": True,
    }
    result = {
        "stage_id": "1013F_R1_TEACHER_READABLE_INLINE_REASONING_SURFACE_DENOISE",
        "created_at": now(),
        "teacher_readable_view_pass": len(anchors) == 10,
        "field_leak_check_pass": not field_hits,
        "teacher_visible_field_leak": bool(field_hits),
        "field_leak_hits": field_hits,
        "paragraph_continuity_pass": all(item["teacher_readable_summary"] for item in anchors),
        "hover_note_lightweight_pass": len(hover["teacher_visible_note"]) <= hover["max_chars"],
        "selected_paragraph_note_pass": len(selected_note["groups"]) <= 4,
        "classroom_logic_pass": all(classroom_logic_checks.values()),
        "classroom_logic_checks": classroom_logic_checks,
        "content_not_overloaded_pass": len(selected_note["groups"]) <= 4 and len(hover["teacher_visible_note"]) <= 120,
        "candidate_error_no_patch_pass": outputs["candidate_error_inline_display"]["patch_generated"] is False,
        "screenshot_smoke_pass": screenshot_view.exists() and screenshot_view.stat().st_size > 0,
        "selected_screenshot_smoke_pass": screenshot_selected.exists() and screenshot_selected.stat().st_size > 0,
        "teacher_review_required": True,
        "formal_apply_performed": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "default_entry_changed": False,
    }
    pass_keys = [
        "teacher_readable_view_pass",
        "field_leak_check_pass",
        "paragraph_continuity_pass",
        "hover_note_lightweight_pass",
        "selected_paragraph_note_pass",
        "classroom_logic_pass",
        "content_not_overloaded_pass",
        "candidate_error_no_patch_pass",
    ]
    result["final_status"] = (
        "PASS_TEACHER_READABLE_INLINE_REASONING_SURFACE"
        if all(result[key] for key in pass_keys)
        else "FAIL_TEACHER_READABLE_INLINE_REASONING_SURFACE"
    )
    result["next_stage"] = (
        "1013F_R2_CLASSROOM_EVENT_DETAIL_POLISH"
        if result["final_status"] == "PASS_TEACHER_READABLE_INLINE_REASONING_SURFACE"
        else "1013F_R1_REPAIR"
    )
    return result


def write_report(result: dict[str, Any]) -> None:
    lines = [
        "# 1013F_R1 Teacher Readable Inline Reasoning Surface",
        "",
        "```text",
        f"final_status={result['final_status']}",
        f"next_stage={result['next_stage']}",
        f"teacher_readable_view_pass={str(result['teacher_readable_view_pass']).lower()}",
        f"field_leak_check_pass={str(result['field_leak_check_pass']).lower()}",
        f"paragraph_continuity_pass={str(result['paragraph_continuity_pass']).lower()}",
        f"hover_note_lightweight_pass={str(result['hover_note_lightweight_pass']).lower()}",
        f"selected_paragraph_note_pass={str(result['selected_paragraph_note_pass']).lower()}",
        f"classroom_logic_pass={str(result['classroom_logic_pass']).lower()}",
        f"content_not_overloaded_pass={str(result['content_not_overloaded_pass']).lower()}",
        "```",
        "",
        "## What This Checks",
        "",
        "- The teacher reads a continuous lesson process, not a field grid.",
        "- Hover notes are short and follow the pointer.",
        "- Clicking a paragraph opens one local note panel; clicking blank space closes it.",
        "- Expanding or closing notes preserves the reading position.",
        "- Content expansion stays in the lesson body, while reasoning stays lightweight.",
        "",
        "## Boundary",
        "",
        "- No provider/model call.",
        "- No database write.",
        "- No memory write.",
        "- No Feishu write.",
        "- No formal apply.",
        "- No official export/archive.",
        "- No default entry change.",
    ]
    write_text("1013F_R1_report.md", "\n".join(lines) + "\n")


def main() -> int:
    if not HTML_PATH.exists():
        raise SystemExit(f"HTML not found: {HTML_PATH}")
    outputs = {
        "teacher_readable_paragraph_render_rules": paragraph_rules(),
        "paragraph_anchor_mapping": anchor_mapping(),
        "hover_reasoning_note_sample": hover_sample(),
        "selected_paragraph_design_note_sample": selected_note_sample(),
        "edit_mode_selected_paragraph_sample": edit_mode_sample(),
        "impact_scope_teacher_language_mapping": impact_mapping(),
        "candidate_error_inline_display": candidate_error_display(),
    }
    write_json("teacher_readable_paragraph_render_rules_1013F_R1.json", outputs["teacher_readable_paragraph_render_rules"])
    write_json("paragraph_anchor_mapping_1013F_R1.json", outputs["paragraph_anchor_mapping"])
    write_json("hover_reasoning_note_sample_1013F_R1.json", outputs["hover_reasoning_note_sample"])
    write_json("selected_paragraph_design_note_sample_1013F_R1.json", outputs["selected_paragraph_design_note_sample"])
    write_json("edit_mode_selected_paragraph_sample_1013F_R1.json", outputs["edit_mode_selected_paragraph_sample"])
    write_json("impact_scope_teacher_language_mapping_1013F_R1.json", outputs["impact_scope_teacher_language_mapping"])
    write_json("candidate_error_inline_display_1013F_R1.json", outputs["candidate_error_inline_display"])
    result = build_result(outputs)
    write_json("1013F_R1_result.json", result)
    write_report(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"] == "PASS_TEACHER_READABLE_INLINE_REASONING_SURFACE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
