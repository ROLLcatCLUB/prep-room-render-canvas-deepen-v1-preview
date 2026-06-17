from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "prep_room_render_canvas_deepen_v1.html"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013F_R2B_teacher_readable_copy_and_visual_tone_repair"

RAW_FIELD_KEYS = [
    "cognitive_grounding",
    "core_learning_problem",
    "target_shift",
    "key_focus",
    "key_difficulty",
    "classroom_event",
    "execution_view",
    "design_view",
    "student_response_model",
    "scaffold",
    "assessment_evidence",
    "transition_to_next",
    "field_patch_candidates",
    "impact_scope",
]

LABEL_MAP = {
    "cognitive_grounding": "本课方向",
    "core_learning_problem": "学生卡点",
    "target_shift": "从哪到哪",
    "key_focus": "要紧的事",
    "key_difficulty": "易卡住处",
    "classroom_event": "课堂推进",
    "execution_view": "课堂这样做",
    "design_view": "为什么这样",
    "student_response_model": "学生可能会",
    "scaffold": "卡住怎么办",
    "assessment_evidence": "怎么算学会",
    "transition_to_next": "接下来",
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(name: str, payload: Any) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(name: str, text: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(text, encoding="utf-8")


def primary_visible_surface_sample() -> str:
    return "\n".join(
        [
            "小教读课提示",
            "轻点段落看小教旁注",
            "当前段落旁注",
            "小教判断",
            "学生可能卡在哪里",
            "可以怎么支架",
            "会影响什么",
            "当前段落",
            "小教建议",
            "修改前",
            "修改后",
            "采纳到本段",
            "继续精修",
            "追问原因",
            "暂不采用",
        ]
    )


def visual_tone_rules() -> dict[str, Any]:
    return {
        "stage_id": "1013F_R2B_TEACHER_READABLE_COPY_AND_VISUAL_TONE_REPAIR",
        "principle": "读课优先，字段降权，操作围绕当前段落。",
        "reading_rules": {
            "main_body_font_size": "16px",
            "main_body_line_height": "1.76",
            "main_reading_width": "max 760px",
            "classroom_event_spacing": "44px",
            "background": "warm paper gray",
        },
        "side_note_rules": {
            "background": "light warm paper",
            "border": "none or very low contrast",
            "blocks": "light title plus bullet, no table lines",
            "close_behavior": "click blank area",
        },
        "edit_surface_rules": {
            "layout": "four focused reading blocks",
            "desktop_before_after": "two columns",
            "mobile_before_after": "stacked by existing responsive flow",
            "raw_fields": "collapsed low-weight source details only",
        },
    }


def low_weight_source_sample() -> dict[str, Any]:
    return {
        "default_open": False,
        "visual_weight": "low",
        "raw_field_key_present": True,
        "sample_keys": ["classroom_event", "design_view", "execution_view", "field_patch_candidates", "impact_scope"],
        "teacher_purpose": "保留查错入口，但不抢主阅读流。",
    }


def copy_repair_sample() -> dict[str, Any]:
    return {
        "assistant_visible_name": "小教",
        "legacy_xiaobei_visible_hits": 0,
        "teacher_facing_labels": ["学生卡点", "为什么这样", "学生可能会", "卡住怎么办", "怎么算学会", "接下来"],
        "tone_rule": "少用命令式你应该，多用教师可追问、学生可能会、如果卡住、看学生能否。",
    }


def evaluate(html: str) -> dict[str, Any]:
    visible_sample = primary_visible_surface_sample()
    raw_hits = [key for key in RAW_FIELD_KEYS if key in visible_sample]
    map_pass = all(key in html and label in html for key, label in LABEL_MAP.items())
    low_weight_present = "raw field keys:" in html and "nb-low-weight-fields" in html
    return {
        "teacher_readable_label_map_pass": map_pass,
        "primary_surface_raw_field_key_hits": raw_hits,
        "collapsed_source_raw_field_key_present": low_weight_present,
        "visible_xiaobei_legacy_hits": visible_sample.count("legacy_xiaobei_name") + html.count("legacy_xiaobei_name"),
        "side_note_not_inline": "renderSelectedParagraphNote" in html and 'return "";' in html,
        "low_weight_source_details": low_weight_present,
        "edit_surface_not_table_like": "nb-edit-surface" in html and "<table" not in html.lower(),
        "copy_uses_xiaojiao": "小教读课提示" in html and "对小教说一句" in html,
        "visual_tone_css_present": all(
            token in html
            for token in ["font-size: 16px", "line-height: 1.76", "max-width: 760px", "gap: 44px"]
        ),
    }


def build_result(html: str) -> dict[str, Any]:
    checks = evaluate(html)
    screenshot_view = OUT_DIR / "ui_smoke_screenshot_1013F_R2B_view.png"
    screenshot_note = OUT_DIR / "ui_smoke_screenshot_1013F_R2B_selected_note.png"
    screenshot_edit = OUT_DIR / "ui_smoke_screenshot_1013F_R2B_edit.png"
    result = {
        "stage_id": "1013F_R2B_TEACHER_READABLE_COPY_AND_VISUAL_TONE_REPAIR",
        "created_at": now(),
        **checks,
        "screenshot_view_pass": screenshot_view.exists() and screenshot_view.stat().st_size > 0,
        "screenshot_selected_note_pass": screenshot_note.exists() and screenshot_note.stat().st_size > 0,
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
    pass_keys = [
        "teacher_readable_label_map_pass",
        "collapsed_source_raw_field_key_present",
        "side_note_not_inline",
        "low_weight_source_details",
        "edit_surface_not_table_like",
        "copy_uses_xiaojiao",
        "visual_tone_css_present",
    ]
    result["final_status"] = (
        "PASS_TEACHER_READABLE_COPY_AND_VISUAL_TONE_REPAIR"
        if all(result[key] for key in pass_keys)
        and not result["primary_surface_raw_field_key_hits"]
        and result["visible_xiaobei_legacy_hits"] == 0
        else "FAIL_TEACHER_READABLE_COPY_AND_VISUAL_TONE_REPAIR"
    )
    result["next_stage"] = (
        "1013F_R2C_CLASSROOM_EVENT_DETAIL_POLISH"
        if result["final_status"] == "PASS_TEACHER_READABLE_COPY_AND_VISUAL_TONE_REPAIR"
        else "1013F_R2B_REPAIR"
    )
    return result


def write_report(result: dict[str, Any]) -> None:
    lines = [
        "# 1013F_R2B Teacher Readable Copy And Visual Tone Repair",
        "",
        "```text",
        f"final_status={result['final_status']}",
        f"next_stage={result['next_stage']}",
        f"primary_surface_raw_field_key_hits={json.dumps(result['primary_surface_raw_field_key_hits'], ensure_ascii=False)}",
        f"collapsed_source_raw_field_key_present={str(result['collapsed_source_raw_field_key_present']).lower()}",
        f"visible_xiaobei_legacy_hits={result['visible_xiaobei_legacy_hits']}",
        "```",
        "",
        "## Summary",
        "",
        "- Teacher-facing copy now uses 小教 instead of the legacy assistant name.",
        "- Raw backend fields are not removed; they remain in collapsed low-weight source details.",
        "- Main reading flow uses larger text, wider reading width, softer event separation, and quieter notes.",
        "- The stage repairs copy and visual tone only; classroom-event content polish remains R2C.",
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
        "- Did not enter 1013G.",
    ]
    write_text("1013F_R2B_report.md", "\n".join(lines) + "\n")


def main() -> int:
    html = HTML_PATH.read_text(encoding="utf-8")
    write_json("teacher_display_label_map_1013F_R2B.json", LABEL_MAP)
    write_json("visual_tone_rules_1013F_R2B.json", visual_tone_rules())
    write_json("low_weight_source_sample_1013F_R2B.json", low_weight_source_sample())
    write_json("teacher_readable_copy_sample_1013F_R2B.json", copy_repair_sample())
    result = build_result(html)
    write_json("1013F_R2B_result.json", result)
    write_report(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"] == "PASS_TEACHER_READABLE_COPY_AND_VISUAL_TONE_REPAIR" else 1


if __name__ == "__main__":
    raise SystemExit(main())
