from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R2D2_DIR = OUTPUT_ROOT / "1013F_R2D2_case_reference_structure_assimilation"
OUT_DIR = OUTPUT_ROOT / "1013F_R2D2_review_gate_before_1013G"
SOURCE_DELTA_DIR = OUTPUT_ROOT / "source_delta_1013F_R2D2_REVIEW_GATE" / "scripts"
HTML_PATH = OUTPUT_ROOT / "prep_room_render_canvas_deepen_v1.html"

STAGE_ID = "1013F_R2D2_REVIEW_GATE_BEFORE_1013G"


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
        "registry": read_json(R2D2_DIR / "case_reference_registry_1013F_R2D2.json"),
        "moves": read_json(R2D2_DIR / "teaching_moves_extraction_1013F_R2D2.json"),
        "patches": read_json(R2D2_DIR / "assimilation_candidate_patch_1013F_R2D2.json"),
        "r2d2_result": read_json(R2D2_DIR / "1013F_R2D2_result.json"),
        "html": read_text(HTML_PATH),
    }


def has_required_registry_fields(registry: list[dict[str, Any]]) -> bool:
    required = {"source_type", "authority_level", "assimilation_level", "direct_copy_allowed"}
    return all(required.issubset(item.keys()) and item["direct_copy_allowed"] is False for item in registry)


def has_required_move_fields(moves: list[dict[str, Any]]) -> bool:
    required = {"source_ref", "target_event", "move_type", "reason_for_assimilation", "risk_note"}
    return all(required.issubset(item.keys()) and item["direct_copy_allowed"] is False for item in moves)


def has_required_patch_fields(patches: list[dict[str, Any]]) -> bool:
    return all(
        item.get("applied") is False
        and item.get("candidate_only") is True
        and item.get("teacher_review_required") is True
        and item.get("apply_mode") == "candidate_only"
        for item in patches
    )


def score_patch_for_gate(patch: dict[str, Any], move_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    text = patch["candidate_text"]
    source_moves = [move_by_id[move_id] for move_id in patch.get("source_move_ids", []) if move_id in move_by_id]
    heavy_markers = ["公开课", "跨学科", "大型", "完整展评", "复杂表格", "长篇", "多媒体联动"]
    adult_tone_markers = ["审美素养", "艺术表现力", "大观念", "综合评估", "理论体系"]
    pass_reasons = []
    risks = []

    if any(marker in text for marker in heavy_markers):
        risks.append("candidate_may_be_too_heavy_for_daily_lesson")
    if any(marker in text for marker in adult_tone_markers):
        risks.append("candidate_has_adult_or_public_lesson_tone")
    if len(text) > 180:
        risks.append("candidate_text_too_long_for_teacher_review_card")
    if not source_moves:
        risks.append("missing_source_move_trace")

    if "探究" in patch["target"] and all(term in text for term in ["色卡", "理由"]):
        pass_reasons.append("keeps_explore_material_light_and_reason_visible")
    if "表现" in patch["target"] and all(term in text for term in ["基础任务", "提前完成"]):
        pass_reasons.append("keeps_default_entry_before_extension")
    if "交流展示" in patch["target"] and all(term in text for term in ["每件只问一个问题", "颜色"]):
        pass_reasons.append("keeps_assessment_observable_and_time_bounded")

    decision = "approved_for_1013G_prep_candidate" if not risks and pass_reasons else "rejected_or_needs_repair"
    return {
        "patch_id": patch["patch_id"],
        "target": patch["target"],
        "decision": decision,
        "candidate_text": text,
        "source_move_ids": patch.get("source_move_ids", []),
        "pass_reasons": pass_reasons,
        "risk_notes": risks,
        "teacher_review_required": True,
        "formal_apply_allowed": False,
        "enter_1013G_now": False,
    }


def build_gate_lists(inputs: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    move_by_id = {item["move_id"]: item for item in inputs["moves"]}
    decisions = [score_patch_for_gate(item, move_by_id) for item in inputs["patches"]]
    approved = [item for item in decisions if item["decision"] == "approved_for_1013G_prep_candidate"]
    rejected = [item for item in decisions if item["decision"] != "approved_for_1013G_prep_candidate"]
    return approved, rejected


def build_result(inputs: dict[str, Any], approved: list[dict[str, Any]], rejected: list[dict[str, Any]]) -> dict[str, Any]:
    r2d2_result = inputs["r2d2_result"]
    schema_pass = {
        "patch_candidate_only_schema_pass": has_required_patch_fields(inputs["patches"]),
        "registry_schema_pass": has_required_registry_fields(inputs["registry"]),
        "teaching_moves_trace_schema_pass": has_required_move_fields(inputs["moves"]),
    }
    boundary_pass = {
        "case_reference_direct_copy_hits_clear": r2d2_result.get("case_reference_direct_copy_hits") == [],
        "html_body_modified": False,
        "r2b2_layout_baseline_kept": bool(r2d2_result.get("r2b2_layout_baseline_kept")),
        "r2c_process_focus_kept": bool(r2d2_result.get("r2c_process_focus_kept")),
        "formal_apply_performed": False,
        "entered_1013G": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }
    quality_pass = {
        "approved_candidate_count": len(approved),
        "rejected_candidate_count": len(rejected),
        "all_approved_candidates_still_require_teacher_review": all(
            item["teacher_review_required"] and not item["formal_apply_allowed"] and not item["enter_1013G_now"]
            for item in approved
        ),
    }
    positive_keys = list(schema_pass) + [
        "case_reference_direct_copy_hits_clear",
        "r2b2_layout_baseline_kept",
        "r2c_process_focus_kept",
        "all_approved_candidates_still_require_teacher_review",
    ]
    no_write_keys = [
        "html_body_modified",
        "formal_apply_performed",
        "entered_1013G",
        "database_written",
        "memory_written",
        "feishu_written",
        "main_project_pushed",
    ]
    merged = {**schema_pass, **boundary_pass, **quality_pass}
    final_pass = all(bool(merged[key]) for key in positive_keys) and not any(bool(merged[key]) for key in no_write_keys)
    return {
        "stage": STAGE_ID,
        "generated_at": now(),
        "inherits_from": "1013F_R2D2_CASE_REFERENCE_STRUCTURE_ASSIMILATION",
        "final_status": "PASS_R2D2_REVIEW_GATE_BEFORE_1013G" if final_pass else "FAIL_R2D2_REVIEW_GATE_BEFORE_1013G",
        "next_stage": "1013G_PREP_CANDIDATE_REVIEW_SANDBOX" if final_pass else "1013F_R2D2_REPAIR",
        "allow_enter_1013G_now": False,
        "allow_formal_apply": False,
        "approved_candidate_ids": [item["patch_id"] for item in approved],
        "rejected_candidate_ids": [item["patch_id"] for item in rejected],
        **merged,
    }


def build_report(result: dict[str, Any], approved: list[dict[str, Any]], rejected: list[dict[str, Any]]) -> str:
    lines = [
        "# 1013F R2D2 Review Gate Before 1013G",
        "",
        f"- FINAL_STATUS: `{result['final_status']}`",
        f"- NEXT_STAGE: `{result['next_stage']}`",
        "- Boundary: review only; no HTML write, no formal apply, no 1013G execution, no database/memory/Feishu write.",
        "",
        "## Gate Decision",
        "",
        "R2D2 candidate outputs are acceptable for a later `1013G_PREP` candidate-review sandbox, but this gate does not enter 1013G and does not apply any lesson text.",
        "",
        "`approved` in this report means approved for sandbox preview only. It is not approval for formal apply, not teacher confirmation, and not permission to merge candidate text into the lesson body.",
        "",
        "## Approved Candidates",
        "",
    ]
    for item in approved:
        lines.extend(
            [
                f"- `{item['patch_id']}` -> {item['target']}",
                f"  - reasons: {', '.join(item['pass_reasons'])}",
            ]
        )
    if rejected:
        lines.extend(["", "## Rejected Candidates", ""])
        for item in rejected:
            lines.extend(
                [
                    f"- `{item['patch_id']}` -> {item['target']}",
                    f"  - risks: {', '.join(item['risk_notes'])}",
                ]
            )
    else:
        lines.extend(["", "## Rejected Candidates", "", "- None."])
    lines.extend(
        [
            "",
            "## Required Checks",
            "",
            f"- patch_candidate_only_schema_pass={str(result['patch_candidate_only_schema_pass']).lower()}",
            f"- registry_schema_pass={str(result['registry_schema_pass']).lower()}",
            f"- teaching_moves_trace_schema_pass={str(result['teaching_moves_trace_schema_pass']).lower()}",
            f"- case_reference_direct_copy_hits_clear={str(result['case_reference_direct_copy_hits_clear']).lower()}",
            f"- html_body_modified={str(result['html_body_modified']).lower()}",
            f"- r2b2_layout_baseline_kept={str(result['r2b2_layout_baseline_kept']).lower()}",
            f"- r2c_process_focus_kept={str(result['r2c_process_focus_kept']).lower()}",
            f"- formal_apply_performed={str(result['formal_apply_performed']).lower()}",
            f"- entered_1013G={str(result['entered_1013G']).lower()}",
            f"- database_written={str(result['database_written']).lower()}",
            f"- memory_written={str(result['memory_written']).lower()}",
            f"- feishu_written={str(result['feishu_written']).lower()}",
            f"- main_project_pushed={str(result['main_project_pushed']).lower()}",
            "",
            "## Boundary",
            "",
            "- Approved here means approved for a later candidate-review sandbox only.",
            "- It does not mean teacher confirmation has happened.",
            "- It does not mean formal apply is allowed.",
        ]
    )
    return "\n".join(lines) + "\n"


def copy_source_delta() -> None:
    SOURCE_DELTA_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA_DIR / Path(__file__).name)


def main() -> int:
    inputs = load_inputs()
    approved, rejected = build_gate_lists(inputs)
    result = build_result(inputs, approved, rejected)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "approved_candidate_moves.json", approved)
    write_json(OUT_DIR / "rejected_candidate_moves.json", rejected)
    write_json(OUT_DIR / "R2D2_review_gate_result.json", result)
    write_text(OUT_DIR / "R2D2_review_gate_report.md", build_report(result, approved, rejected))
    copy_source_delta()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
