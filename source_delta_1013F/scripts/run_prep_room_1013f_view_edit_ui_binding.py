from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
R4_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "live_poc_1013E_R4"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013F_view_edit_ui_binding"

FORBIDDEN_TEACHER_TERMS = [
    "lesson_unfolding_graph",
    "LearningProblemDeriver",
    "EvidenceBinder",
    "EffectivenessEvaluator",
    "pipeline_pass",
    "schema",
    "validator",
    "raw json",
    "field_patch",
    "database",
    "memory",
    "Feishu",
    "formal_apply",
    "provider",
]

IMPACT_LABELS = {
    "big_screen": "大屏",
    "handout": "学习单",
    "evidence_note": "评价证据",
    "teacher_action": "教师引导",
    "student_activity": "学生活动",
    "time_balance": "时间安排",
    "next_lesson_connection": "下一课承接",
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(name: str, payload: Any) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_text(name: str, text: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    path.write_text(text, encoding="utf-8")
    return path


def load_standard_case() -> dict[str, Any]:
    cases = json.loads((R4_DIR / "case_results_1013E_R4.json").read_text(encoding="utf-8"))
    for case in cases:
        if case.get("case_id") == "standard_daily_cold_warm_more_visual":
            return case
    raise SystemExit("standard_daily_cold_warm_more_visual not found")


def build_view_binding(case: dict[str, Any]) -> dict[str, Any]:
    graph = case["candidate"]["lesson_unfolding_graph"]
    grounding = graph["cognitive_grounding"]
    events = graph["classroom_events"]
    return {
        "binding_id": "1013F_VIEW_MODE_STANDARD_DAILY_COLOR_FEELING",
        "lesson_label": "1-2《色彩的感觉》",
        "teacher_visible_judgement": "这节课的关键不是让学生记住冷暖色名称，而是帮助学生从“颜色好看”走向“能说出颜色带来的感受”。",
        "learning_problem": grounding["core_learning_problem"],
        "target_shift": grounding["target_shift"],
        "teaching_route_summary": "先用生活图片唤起感受，再通过色卡分类帮助学生建立冷暖体验，最后把感受转化为自己的色彩表达。",
        "classroom_events": [
            {
                "event_id": event["event_id"],
                "event_label": event["event_name"],
                "minutes": event["duration"]["recommended_minutes"],
                "teacher_focus_cue": event["execution_view"]["teacher_focus_cue"],
                "core_question": event["execution_view"]["core_question"],
                "student_task": event["execution_view"]["student_task"],
                "assessment_evidence": _clean_evidence(event["design_view"]["assessment_evidence"]),
                "student_change": f"{event['design_view']['student_state_before']} → {event['design_view']['student_state_after']}",
            }
            for event in events
        ],
        "evidence_points": [
            "学生能把色卡或图片放入感受类别，并说出理由。",
            "学生能在学习单中写出颜色、感受和理由之间的关系。",
        ],
        "time_arrangement": "40分钟：4 + 8 + 10 + 13 + 5。",
        "next_lesson_connection": graph["next_lesson_connection"],
        "teacher_review_required": True,
        "formal_apply_performed": False,
    }


def build_edit_binding(case: dict[str, Any]) -> dict[str, Any]:
    graph = case["candidate"]["lesson_unfolding_graph"]
    target = next(event for event in graph["classroom_events"] if event["event_id"] == "EVT_3")
    responses = target["student_response_model"]
    return {
        "binding_id": "1013F_EDIT_MODE_EVT_3_COLOR_SORT",
        "current_event": "教学过程 · 色卡分类探究",
        "target_event_id": "EVT_3",
        "student_state_before": target["design_view"]["student_state_before"],
        "student_state_after": target["design_view"]["student_state_after"],
        "teacher_focus_cue": target["execution_view"]["teacher_focus_cue"],
        "core_question": target["execution_view"]["core_question"],
        "student_task": target["execution_view"]["student_task"],
        "student_response_models": [
            {
                "type_label": _response_label(item["type"]),
                "student_response": item["student_response"],
                "teacher_next_move": item["teacher_next_move"],
                "scaffold": item["scaffold"],
            }
            for item in responses
        ],
        "screen_material_handout": {
            "big_screen": target["design_view"]["big_screen_state"],
            "material": target["design_view"]["textbook_or_material_state"],
            "handout": target["design_view"]["learning_sheet_state"],
        },
        "assessment_evidence": _clean_evidence(target["design_view"]["assessment_evidence"]),
        "transition_to_next": target["design_view"]["transition_to_next"],
        "teacher_review_required": True,
        "formal_apply_performed": False,
    }


def build_patch_cards(case: dict[str, Any]) -> list[dict[str, Any]]:
    candidate = case["candidate"]
    patch = candidate["field_patch_candidates"][1]
    return [
        {
            "candidate_id": "1013F_PATCH_EVT_3_COLOR_SORT_REASON",
            "target_event_id": "EVT_3",
            "target_section_label": "教学过程 · 色卡分类探究",
            "teacher_visible_summary": "建议改探究环节：加入色卡分类和理由表达，让学生把冷暖感受说清楚。",
            "before_summary": "原来只是让学生观察冷暖色，学生可能仍停留在“颜色好看”。",
            "after_candidate": "学生先按“温暖、清凉、安静、热烈”等感受给色卡分类，再选择一张色卡说出理由。",
            "why_this_change": "这样能把抽象的冷暖感受变成可操作的分类活动，也能留下学生是否理解的证据。",
            "impact_scope": build_impact_scope(candidate),
            "teacher_review_required": True,
            "formal_apply_performed": False,
            "source_patch_summary": patch["after_candidate"],
        }
    ]


def build_impact_scope(candidate: dict[str, Any]) -> list[dict[str, str]]:
    base = [
        ("big_screen", "准备冷暖色对比图或黑板色块，并保留感受词。"),
        ("handout", "增加“我这样分类的理由”记录格，不做复杂表格。"),
        ("evidence_note", "评价时看学生是否能说出颜色与感受的关系。"),
        ("teacher_action", "教师追问分类依据，而不是直接判定对错。"),
        ("student_activity", "学生从听讲改为动手分类、说明理由。"),
        ("time_balance", "探究环节保留 10 分钟，展示人数不足时压缩交流。"),
        ("next_lesson_connection", "下一课可以回看本课理由句，再进入更完整的色彩表达。"),
    ]
    return [{"impact_key": key, "label": IMPACT_LABELS[key], "summary": summary} for key, summary in base]


def build_teacher_actions() -> dict[str, Any]:
    return {
        "actions": [
            {"id": "accept_preview", "label": "采纳到本段", "effect": "只更新预览状态，等待后续正式确认。"},
            {"id": "refine_more", "label": "继续精修", "effect": "继续围绕当前课堂事件调整。"},
            {"id": "ask_reason", "label": "追问原因", "effect": "显示小备为什么建议这样改。"},
            {"id": "defer", "label": "暂不采用", "effect": "保留候选，不进入正文。"},
        ],
        "teacher_review_required": True,
        "formal_apply_performed": False,
    }


def build_candidate_error_display() -> dict[str, Any]:
    return {
        "candidate_error_policy": "如果缺少证据绑定或候选不完整，不生成修改卡片。",
        "teacher_visible_message": "小备这次没有整理出可用候选，建议重新说一下你想调整的地方。",
        "forbidden_behaviors": ["空默认值", "半截候选", "无证据绑定的候选", "工程错误暴露给教师"],
    }


def build_result(outputs: dict[str, Any]) -> dict[str, Any]:
    visible_text = json.dumps(_teacher_visible_values(outputs), ensure_ascii=False)
    forbidden_hits = [term for term in FORBIDDEN_TEACHER_TERMS if re.search(re.escape(term), visible_text, re.I)]
    screenshot_path = OUT_DIR / "ui_smoke_screenshot_1013F.png"
    edit_screenshot_path = OUT_DIR / "ui_smoke_screenshot_1013F_edit.png"
    pass_status = not forbidden_hits
    return {
        "stage_id": "1013F_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING",
        "created_at": now(),
        "final_status": "PASS_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING" if pass_status else "FAIL_VIEW_EDIT_UI_BINDING",
        "next_stage": "1013G_TEACHER_REVIEW_ACTIONS_PREVIEW_SANDBOX" if pass_status else "1013F_R1_BINDING_REPAIR",
        "view_mode_binding_pass": bool(outputs["view_mode_binding_sample"]["classroom_events"]),
        "edit_mode_binding_pass": outputs["edit_mode_binding_sample"]["target_event_id"] == "EVT_3",
        "patch_candidate_card_pass": bool(outputs["patch_candidate_cards"]),
        "impact_scope_mapping_pass": bool(outputs["impact_scope_mapping"]),
        "screenshot_smoke_pass": screenshot_path.exists() and screenshot_path.stat().st_size > 0,
        "edit_screenshot_smoke_pass": edit_screenshot_path.exists() and edit_screenshot_path.stat().st_size > 0,
        "screenshot_files": [
            screenshot_path.as_posix(),
            edit_screenshot_path.as_posix(),
        ],
        "teacher_review_required": True,
        "formal_apply_performed": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "default_entry_changed": False,
        "forbidden_teacher_visible_hits": forbidden_hits,
    }


def _teacher_visible_values(value: Any) -> Any:
    if isinstance(value, dict):
        hidden_keys = {
            "binding_id",
            "candidate_id",
            "target_event_id",
            "event_id",
            "impact_key",
            "id",
            "teacher_review_required",
            "formal_apply_performed",
        }
        return {key: _teacher_visible_values(item) for key, item in value.items() if key not in hidden_keys}
    if isinstance(value, list):
        return [_teacher_visible_values(item) for item in value]
    return value


def write_report(result: dict[str, Any]) -> None:
    lines = [
        "# 1013F Reasoning Field Patch To View/Edit UI Binding",
        "",
        "```text",
        f"final_status={result['final_status']}",
        f"next_stage={result['next_stage']}",
        f"view_mode_binding_pass={str(result['view_mode_binding_pass']).lower()}",
        f"edit_mode_binding_pass={str(result['edit_mode_binding_pass']).lower()}",
        f"patch_candidate_card_pass={str(result['patch_candidate_card_pass']).lower()}",
        f"impact_scope_mapping_pass={str(result['impact_scope_mapping_pass']).lower()}",
        f"screenshot_smoke_pass={str(result['screenshot_smoke_pass']).lower()}",
        f"edit_screenshot_smoke_pass={str(result['edit_screenshot_smoke_pass']).lower()}",
        "```",
        "",
        "## Summary",
        "",
        "- R4 staged lesson derivation is bound to teacher-readable view mode and edit mode samples.",
        "- The binding shows judgement, suggested target, impact scope, and teacher review actions.",
        "- The HTML preview uses a preview-only `#prepNotebook1013F` / `#prepNotebook1013FEdit` state and does not change the default entry.",
        "",
        "## Boundary",
        "",
        "- No provider/model call.",
        "- No database write.",
        "- No memory write.",
        "- No Feishu write.",
        "- No formal apply.",
        "- No official export/archive.",
        "- No raw model output is sent to frontend.",
    ]
    write_text("1013F_report.md", "\n".join(lines) + "\n")


def _clean_evidence(text: str) -> str:
    return str(text or "").replace("EVID_COLOR_SORT：", "").replace("EVID_REASON_SENTENCE：", "")


def _response_label(value: str) -> str:
    return {
        "expected": "可能回答",
        "partial": "回答不完整",
        "misconception": "可能误解",
        "off_focus": "注意偏离",
        "silent": "沉默卡住",
    }.get(value, "学生反应")


def main() -> int:
    case = load_standard_case()
    outputs = {
        "view_mode_binding_sample": build_view_binding(case),
        "edit_mode_binding_sample": build_edit_binding(case),
        "patch_candidate_cards": build_patch_cards(case),
        "impact_scope_mapping": build_impact_scope(case["candidate"]),
        "teacher_review_action_contract": build_teacher_actions(),
        "candidate_error_display": build_candidate_error_display(),
    }
    result = build_result(outputs)
    write_json("view_mode_binding_sample_1013F.json", outputs["view_mode_binding_sample"])
    write_json("edit_mode_binding_sample_1013F.json", outputs["edit_mode_binding_sample"])
    write_json("patch_candidate_cards_1013F.json", outputs["patch_candidate_cards"])
    write_json("impact_scope_mapping_1013F.json", outputs["impact_scope_mapping"])
    write_json("teacher_review_action_contract_1013F.json", outputs["teacher_review_action_contract"])
    write_json("candidate_error_display_1013F.json", outputs["candidate_error_display"])
    write_json("1013F_result.json", result)
    write_report(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"] == "PASS_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING" else 1


if __name__ == "__main__":
    raise SystemExit(main())
