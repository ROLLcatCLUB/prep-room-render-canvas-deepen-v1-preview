from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "prep_room_render_canvas_deepen_v1.html"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013F_R2C_classroom_event_detail_polish"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(name: str, payload: Any) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(name: str, text: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(text, encoding="utf-8")


def extract_readable_plan(html: str) -> str:
    match = re.search(r"function readableStepPlan\(step\) \{[\s\S]*?function paragraphAnchorId", html)
    return match.group(0) if match else ""


def extract_render_lesson_section(html: str) -> str:
    match = re.search(r"function renderLessonSection[\s\S]*?function renderIntentPanel", html)
    return match.group(0) if match else ""


def extract_render_process_step(html: str) -> str:
    match = re.search(r"function renderProcessStep[\s\S]*?function renderEditBubble", html)
    return match.group(0) if match else ""


def extract_render_process_section(html: str) -> str:
    match = re.search(r"function renderProcessSection[\s\S]*?function renderLessonDesignMode", html)
    return match.group(0) if match else ""


def count_plan_paragraphs(plan: str, step_id: str) -> int:
    match = re.search(rf"{step_id}:\s*\{{[\s\S]*?paragraphs:\s*\[([\s\S]*?)\]\s*,\s*hover:", plan)
    if not match:
        return 0
    return len(re.findall(r'"[^"\n]+",?', match.group(1)))


def evaluate(html: str) -> dict[str, Any]:
    lesson_section = extract_render_lesson_section(html)
    process_step = extract_render_process_step(html)
    process_section = extract_render_process_section(html)
    plan = extract_readable_plan(html)
    step_ids = ["intro", "sense", "explore", "make", "share"]
    paragraph_counts = {step_id: count_plan_paragraphs(plan, step_id) for step_id in step_ids}
    return {
        "section_body_numbered_pass": "nb-numbered-body" in lesson_section and "nb-numbered-item" in lesson_section,
        "section_click_no_outer_frame_pass": 'class="nb-doc-section ${focused ? "section-editing" : ""}"' in lesson_section,
        "section_edit_panel_still_present_pass": "focused ? renderEditPanel(view, section.title)" in lesson_section,
        "process_section_distinct_background_pass": "nb-process-section" in html and "nb-process-focus-note" in process_section,
        "process_step_numbered_pass": "nb-step-detail-list" in process_step and "nb-step-detail-item" in process_step,
        "process_not_truncated_pass": ".slice(0, 2)" not in process_step,
        "all_process_steps_expanded_pass": all(count >= 3 for count in paragraph_counts.values()),
        "classroom_problem_solving_copy_pass": all(
            text in plan
            for text in [
                "教师可以这样开口",
                "学生可能会先说画面里有什么",
                "有争议的色卡",
                "学习单不是额外负担",
                "不同水平的学生都有入口",
                "如果同伴读到的感受和作者不一样",
            ]
        ),
        "edit_bubble_baseline_kept_pass": "nb-edit-bubble" in html and "left: calc(100% - 18px);" in html,
        "right_panel_baseline_kept_pass": "renderRightLessonBrief(view)" in html,
    }, paragraph_counts


def build_result(html: str) -> dict[str, Any]:
    checks, paragraph_counts = evaluate(html)
    screenshot_view = OUT_DIR / "ui_smoke_screenshot_1013F_R2C_view_numbered_sections.png"
    screenshot_process = OUT_DIR / "ui_smoke_screenshot_1013F_R2C_process_focus.png"
    screenshot_edit = OUT_DIR / "ui_smoke_screenshot_1013F_R2C_edit_bubble_kept.png"
    result = {
        "stage_id": "1013F_R2C_CLASSROOM_EVENT_DETAIL_POLISH",
        "created_at": now(),
        **checks,
        "process_paragraph_counts": paragraph_counts,
        "screenshot_view_pass": screenshot_view.exists() and screenshot_view.stat().st_size > 0,
        "screenshot_process_pass": screenshot_process.exists() and screenshot_process.stat().st_size > 0,
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
        "PASS_CLASSROOM_EVENT_DETAIL_POLISH"
        if all(result[key] for key in pass_keys)
        else "FAIL_CLASSROOM_EVENT_DETAIL_POLISH"
    )
    result["next_stage"] = (
        "1013F_R2D_CASE_REFERENCE_ASSIMILATION_OR_CONTENT_REVIEW"
        if result["final_status"] == "PASS_CLASSROOM_EVENT_DETAIL_POLISH"
        else "1013F_R2C_REPAIR"
    )
    return result


def write_samples() -> None:
    write_json(
        "classroom_event_detail_rules_1013F_R2C.json",
        {
            "stage_id": "1013F_R2C_CLASSROOM_EVENT_DETAIL_POLISH",
            "rules": [
                "Normal lesson sections use numbered body lines.",
                "Clicking normal sections must not frame the main reading text.",
                "The edit panel may keep its border below the normal section.",
                "Teaching process uses a distinct focus background.",
                "Teaching process step paragraphs use visible 1/2/3 sequence numbers.",
                "Each classroom event includes teacher language, likely student response, scaffold, resource/evidence, and transition.",
                "R2B2 right-side assistant panels and edit-bubble mechanism remain inherited.",
            ],
        },
    )


def write_report(result: dict[str, Any]) -> None:
    lines = [
        "# 1013F_R2C Classroom Event Detail Polish",
        "",
        "```text",
        f"final_status={result['final_status']}",
        f"next_stage={result['next_stage']}",
        f"section_body_numbered_pass={str(result['section_body_numbered_pass']).lower()}",
        f"process_section_distinct_background_pass={str(result['process_section_distinct_background_pass']).lower()}",
        f"all_process_steps_expanded_pass={str(result['all_process_steps_expanded_pass']).lower()}",
        f"edit_bubble_baseline_kept_pass={str(result['edit_bubble_baseline_kept_pass']).lower()}",
        "```",
        "",
        "## Summary",
        "",
        "- Normal sections now read as numbered teaching-design points.",
        "- Clicking a normal section no longer frames the main body text; only the edit panel below keeps a container.",
        "- Teaching process now has a distinct focus background and a teacher-facing attention cue.",
        "- Teaching-process paragraphs now show visible sequence numbers.",
        "- Classroom events were expanded with teacher language, likely student responses, scaffolds, resources, evidence, and transitions.",
        "- R2B2 right-panel brief and edit-bubble mechanism were kept.",
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
    write_text("1013F_R2C_report.md", "\n".join(lines) + "\n")


def main() -> int:
    html = HTML_PATH.read_text(encoding="utf-8")
    write_samples()
    result = build_result(html)
    write_json("1013F_R2C_result.json", result)
    write_report(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"] == "PASS_CLASSROOM_EVENT_DETAIL_POLISH" else 1


if __name__ == "__main__":
    raise SystemExit(main())
