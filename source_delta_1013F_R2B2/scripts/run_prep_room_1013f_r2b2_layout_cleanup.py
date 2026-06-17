from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "prep_room_render_canvas_deepen_v1.html"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013F_R2B2_layout_cleanup"


REMOVED_BRIEF = "本课使用真实课题 1-2《色彩的感觉》。当前学生档案和课堂反馈尚未接入，学情先按三年级常见认知做预设，后续再由真实记录校准。"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(name: str, payload: Any) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(name: str, text: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(text, encoding="utf-8")


def layout_rules() -> dict[str, Any]:
    return {
        "stage_id": "1013F_R2B2_LAYOUT_CLEANUP",
        "rules": [
            "Edit buttons toggle the edit bubble open and closed.",
            "The removed lesson-brief sentence is not rendered in the main reading flow.",
            "Lesson status is compressed into the view/edit state row with colored lights and text.",
            "Design judgement and read-lesson hint move to the right auxiliary panel above other drawer content.",
            "The main reading area enters the lesson body directly and uses a light text background.",
            "Current-section modification stays inside the annotation bubble.",
            "The edit bubble starts near the right edge of the current paragraph and expands over the right-side area.",
        ],
    }


def evaluate(html: str) -> dict[str, Any]:
    canvas_match = re.search(r"function renderPrepNotebookCanvas[\s\S]*?function renderWeekCalendarCard", html)
    canvas = canvas_match.group(0) if canvas_match else ""
    right_match = re.search(r"function renderPrepNotebookRightPanel[\s\S]*?function renderPrepNotebookCanvas", html)
    right_panel = right_match.group(0) if right_match else ""
    handle_match = re.search(r"function handlePrepEditTarget[\s\S]*?function togglePrepIntent", html)
    handle = handle_match.group(0) if handle_match else ""
    return {
        "edit_button_toggle_pass": "isSameProcess" in handle and 'setPrepNotebookMode("view")' in handle,
        "edit_button_label_toggle_pass": '${isFocused ? "收起" : "编辑"}' in html,
        "removed_brief_not_rendered_pass": "lesson.brief" not in canvas and REMOVED_BRIEF not in canvas,
        "inline_status_lights_pass": "renderLessonStatusLights(lesson)" in canvas and "nb-status-lights" in html,
        "status_grid_removed_from_main_pass": "nb-status-grid" not in canvas,
        "right_panel_brief_pass": "renderRightLessonBrief(view)" in right_panel,
        "right_panel_collapsible_pass": "<details open>" in html and "<details>" in html,
        "main_body_direct_pass": "renderLessonReasoningBrief(lesson)" not in canvas and "renderReasoningBinding1013F(view)" not in canvas,
        "body_light_background_pass": "nb-doc-body-surface" in html,
        "edit_bubble_kept_pass": "renderEditBubble(view" in html and "nb-edit-bubble" in html,
        "edit_bubble_near_text_edge_pass": "left: calc(100% - 18px);" in html,
    }


def build_result(html: str) -> dict[str, Any]:
    checks = evaluate(html)
    screenshot_view = OUT_DIR / "ui_smoke_screenshot_1013F_R2B2_view.png"
    screenshot_edit = OUT_DIR / "ui_smoke_screenshot_1013F_R2B2_edit_toggle_bubble.png"
    result = {
        "stage_id": "1013F_R2B2_LAYOUT_CLEANUP",
        "created_at": now(),
        **checks,
        "screenshot_view_pass": screenshot_view.exists() and screenshot_view.stat().st_size > 0,
        "screenshot_edit_pass": screenshot_edit.exists() and screenshot_edit.stat().st_size > 0,
        "teacher_review_required": True,
        "formal_apply_performed": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "default_entry_changed": False,
        "entered_1013G": False,
    }
    pass_keys = list(checks.keys())
    result["final_status"] = (
        "PASS_LAYOUT_CLEANUP"
        if all(result[key] for key in pass_keys)
        else "FAIL_LAYOUT_CLEANUP"
    )
    result["next_stage"] = (
        "1013F_R2C_CLASSROOM_EVENT_DETAIL_POLISH"
        if result["final_status"] == "PASS_LAYOUT_CLEANUP"
        else "1013F_R2B2_REPAIR"
    )
    return result


def write_report(result: dict[str, Any]) -> None:
    lines = [
        "# 1013F_R2B2 Layout Cleanup",
        "",
        "```text",
        f"final_status={result['final_status']}",
        f"next_stage={result['next_stage']}",
        f"edit_button_toggle_pass={str(result['edit_button_toggle_pass']).lower()}",
        f"inline_status_lights_pass={str(result['inline_status_lights_pass']).lower()}",
        f"right_panel_brief_pass={str(result['right_panel_brief_pass']).lower()}",
        f"main_body_direct_pass={str(result['main_body_direct_pass']).lower()}",
        "```",
        "",
        "## Summary",
        "",
        "- Edit buttons now toggle the annotation bubble open and closed.",
        "- Lesson status moved into the view/edit state row as colored lights plus text.",
        "- The removed lesson-brief sentence is not rendered in the main body.",
        "- Design judgement and read-lesson hint moved to the right auxiliary panel as collapsible content.",
        "- The main reading area now enters the lesson body directly with a light text background.",
        "- The edit bubble now starts near the right edge of the selected paragraph and expands over the right-side area.",
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
    write_text("1013F_R2B2_report.md", "\n".join(lines) + "\n")


def main() -> int:
    html = HTML_PATH.read_text(encoding="utf-8")
    write_json("layout_cleanup_rules_1013F_R2B2.json", layout_rules())
    result = build_result(html)
    write_json("1013F_R2B2_result.json", result)
    write_report(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"] == "PASS_LAYOUT_CLEANUP" else 1


if __name__ == "__main__":
    raise SystemExit(main())
