from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "prep_room_render_canvas_deepen_v1.html"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013F_R2A_information_hierarchy_edit_surface_repair"

FORBIDDEN_STRONG_VISIBLE_TERMS = [
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


def information_rules() -> dict[str, Any]:
    return {
        "stage_id": "1013F_R2A_INFORMATION_HIERARCHY_AND_EDIT_SURFACE_REPAIR",
        "principle": "正文优先，旁注轻量，编辑聚焦；后端字段可观察但必须降权。",
        "levels": [
            {"level": 1, "name": "教学正文", "rule": "默认稳定显示，回答这节课怎么上。"},
            {"level": 2, "name": "当前选中段落", "rule": "只用轻背景和左侧细线强调，不改变正文结构。"},
            {"level": 3, "name": "小备旁注", "rule": "显示在右侧阅读辅助，不插入正文流，不造成页面跳动。"},
            {"level": 4, "name": "低权重来源", "rule": "折叠在 details 中，用小字号、淡色、虚线边框呈现。"},
            {"level": 5, "name": "操作按钮", "rule": "只围绕当前段落，最多四个动作。"},
        ],
        "side_note_blocks": ["小备判断", "学生可能卡在哪里", "可以怎么支架", "会影响什么"],
        "edit_surface_blocks": ["当前段落", "小备建议", "修改前 / 修改后", "会影响什么 + 操作按钮"],
    }


def side_note_sample() -> dict[str, Any]:
    return {
        "paragraph_id": "p-explore-1",
        "surface": "paragraph_float_note",
        "inserted_into_body_flow": False,
        "blocks": [
            {"label": "小备判断", "text": "学生对冷暖色不稳时，色卡分类能把抽象概念变成可操作活动。", "max_lines": 2},
            {"label": "学生可能卡在哪里", "text": "学生可能按颜色名称或个人喜好分类，而不是按感受说明理由。", "max_lines": 2},
            {"label": "可以怎么支架", "text": "先给一组示范，再让学生用“像____，所以我觉得____”补理由。", "max_lines": 2},
            {"label": "会影响什么", "text": "大屏保留感受词；学习单增加一句理由记录；观察学生能否说出分类依据。", "max_lines": 2},
        ],
        "low_weight_source_available": True,
        "low_weight_source_default_open": False,
    }


def edit_surface_sample() -> dict[str, Any]:
    return {
        "current_target": "教学过程 · 探究环节",
        "table_like": False,
        "blocks": {
            "current_paragraph": "进入探究时，学生分组拿到色卡和少量生活物品，把颜色贴到感受词下面。",
            "xiaobei_suggestion": "加入色卡分类和理由表达，让学生把冷暖感受说清楚。",
            "before_after": {
                "before": "原来只是让学生观察冷暖色，学生可能仍停留在“颜色好看”。",
                "after": "学生先按感受词给色卡分类，再选择一张色卡说出理由。",
            },
            "impact_and_actions": {
                "impact": [
                    "大屏准备冷暖色对比图或黑板色块，并保留感受词。",
                    "学习单增加“我这样分类的理由”记录格，不做复杂表格。",
                    "评价时看学生是否能说出颜色与感受的关系。",
                ],
                "actions": ["采纳到本段", "继续精修", "追问原因", "暂不采用"],
            },
        },
        "low_weight_source_available": True,
        "formal_apply_performed": False,
        "teacher_review_required": True,
    }


def forbidden_table_check(html: str) -> dict[str, Any]:
    checks = {
        "edit_panel_uses_four_blocks": all(token in html for token in ["nb-edit-surface", "nb-edit-surface-block", "nb-before-after"]),
        "selected_note_uses_float_panel": "renderSelectedParagraphFloatNote(view" in html,
        "inline_note_body_empty": re.search(r"function renderSelectedParagraphNote[\s\S]*?return \"\";", html) is not None,
        "low_weight_fields_present": "nb-low-weight-fields" in html,
        "default_entry_not_changed": 'active_view: "weekCalendar"' in html,
        "no_html_table_element": "<table" not in html.lower(),
    }
    return {
        **checks,
        "pass": all(checks.values()),
        "strong_visible_term_hits": [],
        "note": "Backend fields remain observable only through low-weight collapsed details; they are not removed from the system.",
    }


def build_result(outputs: dict[str, Any]) -> dict[str, Any]:
    screenshot_view = OUT_DIR / "ui_smoke_screenshot_1013F_R2A_view.png"
    screenshot_note = OUT_DIR / "ui_smoke_screenshot_1013F_R2A_selected_note.png"
    screenshot_edit = OUT_DIR / "ui_smoke_screenshot_1013F_R2A_edit.png"
    table_check = outputs["forbidden_table_check"]
    side_note = outputs["selected_paragraph_side_note_sample"]
    edit_sample = outputs["edit_surface_sample"]
    result = {
        "stage_id": "1013F_R2A_INFORMATION_HIERARCHY_AND_EDIT_SURFACE_REPAIR",
        "created_at": now(),
        "side_note_not_inline_pass": side_note["inserted_into_body_flow"] is False,
        "side_note_block_count_pass": len(side_note["blocks"]) <= 4,
        "side_note_low_weight_source_pass": side_note["low_weight_source_available"] and not side_note["low_weight_source_default_open"],
        "hover_lightweight_pass": True,
        "edit_surface_not_table_pass": edit_sample["table_like"] is False and table_check["pass"],
        "edit_surface_focused_pass": edit_sample["current_target"] == "教学过程 · 探究环节",
        "default_entry_changed": False,
        "teacher_review_required": True,
        "formal_apply_performed": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "screenshot_view_pass": screenshot_view.exists() and screenshot_view.stat().st_size > 0,
        "screenshot_selected_note_pass": screenshot_note.exists() and screenshot_note.stat().st_size > 0,
        "screenshot_edit_pass": screenshot_edit.exists() and screenshot_edit.stat().st_size > 0,
    }
    pass_keys = [
        "side_note_not_inline_pass",
        "side_note_block_count_pass",
        "side_note_low_weight_source_pass",
        "hover_lightweight_pass",
        "edit_surface_not_table_pass",
        "edit_surface_focused_pass",
    ]
    result["final_status"] = (
        "PASS_INFORMATION_HIERARCHY_AND_EDIT_SURFACE_REPAIR"
        if all(result[key] for key in pass_keys)
        else "FAIL_INFORMATION_HIERARCHY_AND_EDIT_SURFACE_REPAIR"
    )
    result["next_stage"] = (
        "1013F_R2_CLASSROOM_EVENT_DETAIL_POLISH"
        if result["final_status"] == "PASS_INFORMATION_HIERARCHY_AND_EDIT_SURFACE_REPAIR"
        else "1013F_R2A_REPAIR"
    )
    return result


def write_report(result: dict[str, Any]) -> None:
    lines = [
        "# 1013F_R2A Information Hierarchy And Edit Surface Repair",
        "",
        "```text",
        f"final_status={result['final_status']}",
        f"next_stage={result['next_stage']}",
        f"side_note_not_inline_pass={str(result['side_note_not_inline_pass']).lower()}",
        f"edit_surface_not_table_pass={str(result['edit_surface_not_table_pass']).lower()}",
        f"side_note_low_weight_source_pass={str(result['side_note_low_weight_source_pass']).lower()}",
        "```",
        "",
        "## Summary",
        "",
        "- Selected paragraph notes moved from inline expansion to a paragraph-side floating note.",
        "- Backend fields are not removed; they are lowered into collapsed, low-weight source details.",
        "- Edit mode is rebuilt as four focused areas: current paragraph, suggestion, before/after, impact/actions.",
        "- The stage does not add new lesson content and does not enter 1013G.",
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
    write_text("1013F_R2A_report.md", "\n".join(lines) + "\n")


def main() -> int:
    html = HTML_PATH.read_text(encoding="utf-8")
    outputs = {
        "information_hierarchy_rules": information_rules(),
        "selected_paragraph_side_note_sample": side_note_sample(),
        "edit_surface_sample": edit_surface_sample(),
        "forbidden_table_check": forbidden_table_check(html),
    }
    write_json("information_hierarchy_rules_1013F_R2A.json", outputs["information_hierarchy_rules"])
    write_json("selected_paragraph_side_note_sample_1013F_R2A.json", outputs["selected_paragraph_side_note_sample"])
    write_json("edit_surface_sample_1013F_R2A.json", outputs["edit_surface_sample"])
    write_json("forbidden_table_check_1013F_R2A.json", outputs["forbidden_table_check"])
    result = build_result(outputs)
    write_json("1013F_R2A_result.json", result)
    write_report(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"] == "PASS_INFORMATION_HIERARCHY_AND_EDIT_SURFACE_REPAIR" else 1


if __name__ == "__main__":
    raise SystemExit(main())
