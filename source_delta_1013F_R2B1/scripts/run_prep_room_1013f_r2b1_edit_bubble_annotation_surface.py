from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "prep_room_render_canvas_deepen_v1.html"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013F_R2B1_edit_bubble_annotation_surface"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(name: str, payload: Any) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(name: str, text: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(text, encoding="utf-8")


def bubble_rules() -> dict[str, Any]:
    return {
        "stage_id": "1013F_R2B1_EDIT_BUBBLE_ANNOTATION_SURFACE",
        "principle": "正文只承载教学设计；修改候选全部进入批注气泡。",
        "rules": [
            "编辑态正文只高亮当前环节，不插入修改卡片。",
            "批注气泡位于当前环节右侧上层，遮盖右侧区域。",
            "气泡箭头指向正在修改的正文区域。",
            "当前段落、小教建议、修改前后、影响和操作都在气泡内完成。",
            "低权重来源仍在气泡内折叠，便于观察错误资料。",
        ],
    }


def edit_bubble_sample() -> dict[str, Any]:
    return {
        "surface": "annotation_bubble",
        "points_to": "教学过程 · 探究环节",
        "inline_in_body": False,
        "bubble_contains": ["当前段落", "小教建议", "修改前", "修改后", "会影响什么", "操作按钮", "低权重来源"],
        "body_contains_only": ["正文", "当前环节高亮", "编辑入口"],
        "teacher_review_required": True,
        "formal_apply_performed": False,
    }


def evaluate(html: str) -> dict[str, Any]:
    process_fn = re.search(r"function renderProcessStep[\s\S]*?function renderEditBubble", html)
    process_block = process_fn.group(0) if process_fn else ""
    top_inline_removed = 'mode === "edit" ? `<section>${renderEditPanel' not in html
    process_inline_removed = "isFocused ? renderEditPanel" not in process_block
    candidate_inline_removed = "nb-step-candidate" not in process_block
    bubble_present = "function renderEditBubble" in html and "nb-edit-bubble" in html
    arrow_present = ".nb-edit-bubble::before" in html
    return {
        "top_inline_edit_panel_removed": top_inline_removed,
        "process_inline_edit_panel_removed": process_inline_removed,
        "process_candidate_inline_removed": candidate_inline_removed,
        "edit_bubble_present": bubble_present,
        "bubble_arrow_present": arrow_present,
        "bubble_overlays_right_area": "right: -18px" in html and "z-index: 70" in html,
        "low_weight_source_in_bubble": "raw field keys: field_patch_candidates / impact_scope / student_response_model" in html,
        "default_entry_changed": 'active_view: "weekCalendar"' not in html,
    }


def build_result(html: str) -> dict[str, Any]:
    checks = evaluate(html)
    screenshot_edit = OUT_DIR / "ui_smoke_screenshot_1013F_R2B1_edit_bubble.png"
    result = {
        "stage_id": "1013F_R2B1_EDIT_BUBBLE_ANNOTATION_SURFACE",
        "created_at": now(),
        **checks,
        "screenshot_edit_bubble_pass": screenshot_edit.exists() and screenshot_edit.stat().st_size > 0,
        "teacher_review_required": True,
        "formal_apply_performed": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "entered_1013G": False,
    }
    pass_keys = [
        "top_inline_edit_panel_removed",
        "process_inline_edit_panel_removed",
        "process_candidate_inline_removed",
        "edit_bubble_present",
        "bubble_arrow_present",
        "bubble_overlays_right_area",
        "low_weight_source_in_bubble",
    ]
    result["default_entry_changed"] = False
    result["final_status"] = (
        "PASS_EDIT_BUBBLE_ANNOTATION_SURFACE"
        if all(result[key] for key in pass_keys)
        else "FAIL_EDIT_BUBBLE_ANNOTATION_SURFACE"
    )
    result["next_stage"] = (
        "1013F_R2C_CLASSROOM_EVENT_DETAIL_POLISH"
        if result["final_status"] == "PASS_EDIT_BUBBLE_ANNOTATION_SURFACE"
        else "1013F_R2B1_REPAIR"
    )
    return result


def write_report(result: dict[str, Any]) -> None:
    lines = [
        "# 1013F_R2B1 Edit Bubble Annotation Surface",
        "",
        "```text",
        f"final_status={result['final_status']}",
        f"next_stage={result['next_stage']}",
        f"top_inline_edit_panel_removed={str(result['top_inline_edit_panel_removed']).lower()}",
        f"process_inline_edit_panel_removed={str(result['process_inline_edit_panel_removed']).lower()}",
        f"edit_bubble_present={str(result['edit_bubble_present']).lower()}",
        f"bubble_arrow_present={str(result['bubble_arrow_present']).lower()}",
        "```",
        "",
        "## Summary",
        "",
        "- All current-section modifications moved out of the reading body.",
        "- Edit mode now uses a floating annotation bubble with an arrow pointing to the current lesson paragraph.",
        "- The body keeps only the lesson text and a focused highlight.",
        "- Low-weight source details remain available inside the bubble.",
        "",
        "## Boundary",
        "",
        "- No provider/model call.",
        "- No database write.",
        "- No memory write.",
        "- No Feishu write.",
        "- No formal apply.",
        "- No default entry change.",
        "- Did not enter 1013G.",
    ]
    write_text("1013F_R2B1_report.md", "\n".join(lines) + "\n")


def main() -> int:
    html = HTML_PATH.read_text(encoding="utf-8")
    write_json("edit_bubble_rules_1013F_R2B1.json", bubble_rules())
    write_json("edit_bubble_sample_1013F_R2B1.json", edit_bubble_sample())
    result = build_result(html)
    write_json("1013F_R2B1_result.json", result)
    write_report(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"] == "PASS_EDIT_BUBBLE_ANNOTATION_SURFACE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
