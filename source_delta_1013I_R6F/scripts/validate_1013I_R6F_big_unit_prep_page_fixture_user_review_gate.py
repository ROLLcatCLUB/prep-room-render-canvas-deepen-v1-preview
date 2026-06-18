from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6F_BIG_UNIT_PREP_PAGE_FIXTURE_USER_REVIEW_GATE"
FINAL_STATUS = "PASS_1013I_R6F_BIG_UNIT_PREP_PAGE_FIXTURE_USER_REVIEW_GATE"
INHERITS_FROM = "1013I_R6E_OFFICIAL_UNIT_MATERIAL_READONLY_EXTRACTION_FIXTURE"
R6E_PASS_STATUS = "PASS_1013I_R6E_OFFICIAL_UNIT_MATERIAL_READONLY_EXTRACTION_FIXTURE"
NEXT_STAGE = "1013I_R6G_BIG_UNIT_PREP_PAGE_FIXTURE_AFTER_USER_APPROVAL"
STAGE_DIR_NAME = "1013I_R6F_big_unit_prep_page_fixture_user_review_gate"
VALIDATOR_NAME = "validate_1013I_R6F_big_unit_prep_page_fixture_user_review_gate.py"
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]
SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)app[_-]?secret\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)tenant[_-]?access[_-]?token\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)cookie\s*[:=]\s*['\"][^'\"]{20,}"),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_output_root(root: Path) -> Path:
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    if (root / "REVIEW_PACKAGE_MANIFEST.md").exists() and (root / "LATEST_REVIEW_ENTRY.md").exists():
        return root
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def profile() -> dict[str, Any]:
    return {
        "agent_role": "unified_teacher_agent",
        "assistant_profile": {
            "display_name": "小教",
            "display_name_customizable": True,
            "wake_name": "小教",
            "voice_profile_id": None,
            "tts_enabled": False,
        },
        "active_space": "prep_room",
        "active_capability": "lesson_prep",
        "capability_keys": ["lesson_prep", "big_unit_context", "curriculum_control"],
    }


def boundary() -> dict[str, bool]:
    return {
        "structure_proposal_only": True,
        "user_review_gate_only": True,
        "page_work_started": False,
        "page_fixture_created": False,
        "ui_implementation_started": False,
        "html_body_modified": False,
        "lesson_body_modified": False,
        "normal_candidate_card_generation_allowed": False,
        "big_unit_generation_performed": False,
        "single_lesson_generation_performed": False,
        "r7_visual_review_entered": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "official_export_created": False,
        "official_archive_created": False,
        "main_project_pushed": False,
    }


def r6e_dir(output_root: Path) -> Path:
    return output_root / "1013I_R6E_official_unit_material_readonly_extraction_fixture"


def load_r6e(output_root: Path) -> dict[str, Any]:
    stage_dir = r6e_dir(output_root)
    return {
        "result": read_json(stage_dir / "1013I_R6E_result.json"),
        "extraction_fixture": read_json(stage_dir / "official_unit_material_extraction_fixture_1013I_R6E.json"),
        "textbook_anchor_candidates": read_json(stage_dir / "textbook_anchor_candidates_1013I_R6E.json"),
        "big_unit_chain_candidates": read_json(stage_dir / "big_unit_chain_candidates_1013I_R6E.json"),
        "teacher_confirmation_required_items": read_json(
            stage_dir / "teacher_confirmation_required_items_1013I_R6E.json"
        ),
    }


def build_page_structure_proposal(r6e: dict[str, Any]) -> dict[str, Any]:
    lesson_position = r6e["extraction_fixture"]["lesson_position_candidate"]
    return {
        "stage": STAGE_ID,
        "proposal_id": "big_unit_prep_page_structure_proposal_1013I_R6F",
        "inherits_from": INHERITS_FROM,
        "proposal_status": "pending_user_review",
        "page_work_started": False,
        "page_fixture_created": False,
        "ui_implementation_started": False,
        "user_review_required_before_page_fixture": True,
        **profile(),
        "page_intent": "help_teacher_review_textbook_anchor_big_unit_chain_lesson_position_before_single_lesson_prep",
        "teacher_visible_title": "大单元位置确认",
        "first_screen_priority": [
            "current_lesson_context",
            "blocking_confirmation_items",
            "textbook_anchor_candidates",
            "lesson_position_candidate",
        ],
        "proposed_information_architecture": [
            {
                "zone_id": "top_context_strip",
                "purpose": "show current lesson and why normal prep is blocked",
                "visible_by_default": True,
                "source": "R6E extraction fixture",
            },
            {
                "zone_id": "left_unit_chain",
                "purpose": "show unit progression candidates without turning them into final unit design",
                "visible_by_default": True,
                "source": "R6E big unit chain candidates",
            },
            {
                "zone_id": "center_review_board",
                "purpose": "review textbook anchor, unit position, and teacher confirmations",
                "visible_by_default": True,
                "source": "R6E textbook and confirmation candidates",
            },
            {
                "zone_id": "right_reference_rail",
                "purpose": "show official-field reference notes and common risks as readonly hints",
                "visible_by_default": False,
                "source": "R6E source index and field refs",
            },
        ],
        "lesson_position_candidate": lesson_position,
        "blocked_until": [
            "teacher_confirms_textbook_version",
            "teacher_confirms_unit_title",
            "teacher_confirms_lesson_code_and_activity_ref",
            "teacher_confirms_unit_task_chain",
            "teacher_confirms_lesson_position",
        ],
        "allowed_next_after_user_approval": NEXT_STAGE,
        **boundary(),
    }


def build_page_sections(r6e: dict[str, Any]) -> dict[str, Any]:
    textbook_candidate_count = len(r6e["textbook_anchor_candidates"].get("candidates", []))
    unit_chain = r6e["big_unit_chain_candidates"]["unit_package_candidate"]["unit_task_chain_candidates"]
    confirmation_items = r6e["teacher_confirmation_required_items"]["items"]
    return {
        "stage": STAGE_ID,
        "sections_id": "big_unit_prep_page_sections_1013I_R6F",
        "user_review_required_before_page_fixture": True,
        "page_work_started": False,
        "ui_implementation_started": False,
        **profile(),
        "sections": [
            {
                "section_id": "current_lesson_context",
                "teacher_label": "当前课题位置",
                "default_state": "expanded",
                "source_data": ["R6E.lesson_position_candidate", "R6E.textbook_anchor_candidates"],
                "must_show": ["subject_grade", "lesson_title", "unit_title_candidates", "blocked_status"],
                "must_not_show": ["engineering_ids_as_primary_copy", "official_claim_badge"],
            },
            {
                "section_id": "textbook_anchor_candidates",
                "teacher_label": "教材锚点候选",
                "default_state": "expanded",
                "candidate_count": textbook_candidate_count,
                "source_data": ["textbook_anchor_candidates_1013I_R6E.json"],
                "teacher_actions": ["confirm_anchor", "mark_wrong", "ask_for_more_material"],
                "writes_formal_anchor": False,
            },
            {
                "section_id": "big_unit_chain_candidates",
                "teacher_label": "大单元推进链",
                "default_state": "expanded",
                "stage_count": len(unit_chain),
                "source_data": ["big_unit_chain_candidates_1013I_R6E.json"],
                "teacher_actions": ["confirm_chain_shape", "revise_stage_order", "mark_field_too_heavy"],
                "writes_unit_package": False,
            },
            {
                "section_id": "lesson_position_candidate",
                "teacher_label": "本课承担什么任务",
                "default_state": "expanded",
                "source_data": ["official_unit_material_extraction_fixture_1013I_R6E.json"],
                "teacher_actions": ["choose_lesson_role", "leave_unknown", "ask_for_unit_material"],
                "writes_lesson_body": False,
            },
            {
                "section_id": "teacher_confirmation_items",
                "teacher_label": "进入单课备课前还要确认",
                "default_state": "expanded",
                "item_count": len(confirmation_items),
                "source_data": ["teacher_confirmation_required_items_1013I_R6E.json"],
                "teacher_actions": ["confirm_item", "defer_item", "request_material"],
                "blocks_normal_candidate_generation": True,
            },
            {
                "section_id": "readonly_reference_notes",
                "teacher_label": "只读依据和风险提醒",
                "default_state": "collapsed",
                "source_data": ["official_unit_material_source_index_1013I_R6E.json"],
                "teacher_actions": ["view_reference", "hide_reference"],
                "official_claim_created": False,
            },
        ],
        **boundary(),
    }


def build_checklist() -> str:
    return f"""# 1013I_R6F Teacher User Review Checklist

```text
STAGE={STAGE_ID}
STATUS=pending_user_review
PAGE_WORK_STARTED=false
UI_IMPLEMENTATION_STARTED=false
NEXT_STAGE_AFTER_APPROVAL={NEXT_STAGE}
```

## 请先看这些问题

1. 第一屏是否应该先让老师看到“为什么不能直接生成单课”？
2. 教材锚点候选、单元链候选、本课位置候选，三者的优先顺序是否合理？
3. 大单元推进链是否应该放左侧，还是放在主区域上方？
4. 教师确认项是否太多，是否需要分成“必须确认 / 可以稍后补”？
5. 只读官方字段依据是否默认折叠，避免压过教师自己的判断？
6. 是否允许老师选择“先临时按单课草稿继续”，并明确标记为降级模式？

## 当前不做

- 不写 HTML 页面。
- 不做视觉实现。
- 不生成大单元正文。
- 不生成单课教案。
- 不调用 provider/model。
- 不写 database/memory/Feishu。
"""


def build_risk_notes() -> str:
    return """# 1013I_R6F Page Risk Notes

## Main Risks

- If the page looks like a final unit design editor, teachers may assume the extracted candidates are confirmed official content.
- If the blocking state is hidden, the system may appear broken because it refuses normal candidate-card generation.
- If all official fields are expanded by default, the page will feel like a form wall instead of a teacher decision surface.
- If lesson-position choice is too abstract, teachers may not know how it changes the following single-lesson prep.

## Guardrails

- Keep candidates visually separate from confirmed fields.
- Keep the normal generation block visible until teacher confirmation is complete.
- Default official reference notes to collapsed.
- Label every candidate as pending teacher review.
- Do not start page fixture or UI implementation until the user approves the structure.
"""


def scan_deprecated_visible_names(paths: list[Path]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name in DEPRECATED_VISIBLE_NAMES:
            if name in text:
                hits.append({"path": str(path), "name": name})
    return hits


def scan_secrets(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append(str(path))
                break
    return hits


def build_result(output_root: Path, stage_files: list[Path]) -> dict[str, Any]:
    stage_dir = output_root / STAGE_DIR_NAME
    r6e = load_r6e(output_root)
    latest_text = (output_root / "LATEST_REVIEW_ENTRY.md").read_text(encoding="utf-8")
    manifest_text = (output_root / "REVIEW_PACKAGE_MANIFEST.md").read_text(encoding="utf-8")
    proposal = read_json(stage_dir / "big_unit_prep_page_structure_proposal_1013I_R6F.json")
    sections = read_json(stage_dir / "big_unit_prep_page_sections_1013I_R6F.json")

    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "r6e_result_present": True,
        "r6e_final_status": r6e["result"].get("final_status"),
        "r6e_pass": r6e["result"].get("final_status") == R6E_PASS_STATUS,
        "latest_entry_points_to_r6f": f"REVIEW_STAGE={STAGE_ID}" in latest_text
        and f"FINAL_STATUS={FINAL_STATUS}" in latest_text,
        "latest_entry_next_stage_is_r6g_after_approval": f"NEXT_RECOMMENDED_STAGE={NEXT_STAGE}" in latest_text,
        "manifest_includes_r6f": STAGE_ID in manifest_text and f"{STAGE_DIR_NAME}/" in manifest_text,
        "manifest_next_stage_is_r6g_after_approval": NEXT_STAGE in manifest_text,
        "page_structure_proposal_created": (
            stage_dir / "big_unit_prep_page_structure_proposal_1013I_R6F.json"
        ).exists(),
        "page_sections_created": (stage_dir / "big_unit_prep_page_sections_1013I_R6F.json").exists(),
        "teacher_user_review_checklist_created": (
            stage_dir / "teacher_user_review_checklist_1013I_R6F.md"
        ).exists(),
        "page_risk_notes_created": (stage_dir / "page_risk_notes_1013I_R6F.md").exists(),
        "user_review_required_before_page_fixture": proposal.get("user_review_required_before_page_fixture") is True,
        "section_count": len(sections.get("sections", [])),
        "textbook_anchor_candidates_visible": any(
            section.get("section_id") == "textbook_anchor_candidates" for section in sections["sections"]
        ),
        "big_unit_chain_candidates_visible": any(
            section.get("section_id") == "big_unit_chain_candidates" for section in sections["sections"]
        ),
        "lesson_position_candidate_visible": any(
            section.get("section_id") == "lesson_position_candidate" for section in sections["sections"]
        ),
        "teacher_confirmation_items_visible": any(
            section.get("section_id") == "teacher_confirmation_items" for section in sections["sections"]
        ),
        "readonly_reference_notes_collapsed": any(
            section.get("section_id") == "readonly_reference_notes" and section.get("default_state") == "collapsed"
            for section in sections["sections"]
        ),
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(stage_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **profile(),
        **boundary(),
    }
    required_true = [
        "r6e_result_present",
        "r6e_pass",
        "latest_entry_points_to_r6f",
        "latest_entry_next_stage_is_r6g_after_approval",
        "manifest_includes_r6f",
        "manifest_next_stage_is_r6g_after_approval",
        "page_structure_proposal_created",
        "page_sections_created",
        "teacher_user_review_checklist_created",
        "page_risk_notes_created",
        "user_review_required_before_page_fixture",
        "textbook_anchor_candidates_visible",
        "big_unit_chain_candidates_visible",
        "lesson_position_candidate_visible",
        "teacher_confirmation_items_visible",
        "readonly_reference_notes_collapsed",
        "structure_proposal_only",
        "user_review_gate_only",
    ]
    required_false = [
        "page_work_started",
        "page_fixture_created",
        "ui_implementation_started",
        "html_body_modified",
        "lesson_body_modified",
        "normal_candidate_card_generation_allowed",
        "big_unit_generation_performed",
        "single_lesson_generation_performed",
        "r7_visual_review_entered",
        "provider_called",
        "model_called",
        "formal_apply_performed",
        "database_written",
        "memory_written",
        "feishu_written",
        "official_export_created",
        "official_archive_created",
        "main_project_pushed",
    ]
    failures = [key for key in required_true if result.get(key) is not True]
    failures.extend([key for key in required_false if result.get(key) is not False])
    if result.get("section_count", 0) < 6:
        failures.append("section_count")
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    if failures:
        result["final_status"] = "FAIL_1013I_R6F_BIG_UNIT_PREP_PAGE_FIXTURE_USER_REVIEW_GATE"
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013I_R6F Big Unit Prep Page Fixture User Review Gate Report

```text
STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}
PAGE_WORK_STARTED=false
UI_IMPLEMENTATION_STARTED=false
USER_REVIEW_REQUIRED_BEFORE_PAGE_FIXTURE=true
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Result

```text
page_structure_proposal_created={str(result["page_structure_proposal_created"]).lower()}
page_sections_created={str(result["page_sections_created"]).lower()}
teacher_user_review_checklist_created={str(result["teacher_user_review_checklist_created"]).lower()}
page_risk_notes_created={str(result["page_risk_notes_created"]).lower()}
section_count={result["section_count"]}
textbook_anchor_candidates_visible={str(result["textbook_anchor_candidates_visible"]).lower()}
big_unit_chain_candidates_visible={str(result["big_unit_chain_candidates_visible"]).lower()}
lesson_position_candidate_visible={str(result["lesson_position_candidate_visible"]).lower()}
teacher_confirmation_items_visible={str(result["teacher_confirmation_items_visible"]).lower()}
readonly_reference_notes_collapsed={str(result["readonly_reference_notes_collapsed"]).lower()}
page_work_started={str(result["page_work_started"]).lower()}
ui_implementation_started={str(result["ui_implementation_started"]).lower()}
```

## Boundary

R6F is a user-review gate for page structure only. It does not create a page fixture, does not write HTML, does not start UI implementation, does not generate a big-unit body, does not generate a single-lesson plan, and does not write database, memory, Feishu, export, or archive.
"""


def copy_source_delta(root: Path, output_root: Path) -> None:
    source = root / "scripts" / VALIDATOR_NAME
    target = output_root / "source_delta_1013I_R6F" / "scripts" / VALIDATOR_NAME
    if source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    root = args.root.resolve()
    output_root = resolve_output_root(root)
    r6e = load_r6e(output_root)
    stage_dir = output_root / STAGE_DIR_NAME
    write_json(
        stage_dir / "big_unit_prep_page_structure_proposal_1013I_R6F.json",
        build_page_structure_proposal(r6e),
    )
    write_json(stage_dir / "big_unit_prep_page_sections_1013I_R6F.json", build_page_sections(r6e))
    write_text(stage_dir / "teacher_user_review_checklist_1013I_R6F.md", build_checklist())
    write_text(stage_dir / "page_risk_notes_1013I_R6F.md", build_risk_notes())
    result_path = stage_dir / "1013I_R6F_result.json"
    report_path = stage_dir / "1013I_R6F_report.md"
    stage_files = [
        stage_dir / "big_unit_prep_page_structure_proposal_1013I_R6F.json",
        stage_dir / "big_unit_prep_page_sections_1013I_R6F.json",
        stage_dir / "teacher_user_review_checklist_1013I_R6F.md",
        stage_dir / "page_risk_notes_1013I_R6F.md",
        result_path,
        report_path,
    ]
    result = build_result(output_root, stage_files)
    write_json(result_path, result)
    write_text(report_path, build_report(result))
    copy_source_delta(root, output_root)
    if result["final_status"] != FINAL_STATUS:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    print(f"{FINAL_STATUS}: {result_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
