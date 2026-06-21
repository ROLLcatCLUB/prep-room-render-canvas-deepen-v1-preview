from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R29_DIR = BASE / "1013L_R29_lesson_courseware_marker_and_inline_edit_scope_patch"
HTML = R29_DIR / "prep_room_render_canvas_deepen_v1_1013L_R29_marker_edit_scope_patch.html"
RESULT = R29_DIR / "1013L_R29_result.json"
PATCH = R29_DIR / "lesson_courseware_marker_and_inline_edit_scope_patch_1013L_R29.json"
SMOKE = R29_DIR / "lesson_courseware_marker_and_inline_edit_scope_smoke_1013L_R29.json"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> None:
    failures: list[str] = []
    for path in [HTML, RESULT, PATCH, SMOKE]:
        if not path.exists():
            failures.append(f"missing:{path.name}")

    if failures:
        raise SystemExit("FAIL: " + ", ".join(failures))

    html = HTML.read_text(encoding="utf-8-sig")
    result = read_json(RESULT)
    patch = read_json(PATCH)
    smoke = read_json(SMOKE)

    expected_status = "PASS_1013L_R29_LESSON_COURSEWARE_MARKER_AND_INLINE_EDIT_SCOPE_PATCH"
    checks = {
        "final_status_pass": result.get("final_status") == expected_status,
        "failed_checks_empty": result.get("failed_checks") == [],
        "marker_scope_corrected": result.get("marker_scope_corrected") is True,
        "markers_only_in_process_steps": result.get("courseware_markers_only_in_teaching_process_steps") is True,
        "process_overview_cards_removed": result.get("process_overview_courseware_cards_removed") is True,
        "marker_click_right_draft": result.get("marker_click_opens_right_draft_focus_not_switch_popover") is True,
        "single_lesson_inline_edit": result.get("single_lesson_inline_edit_aligned_to_clicked_line") is True,
        "big_unit_inline_edit": result.get("big_unit_inline_edit_aligned_to_clicked_section") is True,
        "inherits_existing_page_lineage": result.get("inherits_existing_page_lineage") is True,
        "new_disconnected_page_not_created": result.get("new_disconnected_page_created") is False,
        "native_replacements_2": len(patch.get("native_renderer_replacements", [])) == 2,
        "r29_script_present": "script-1013L-R29-marker-edit-scope-patch" in html,
        "r29_style_present": "style-1013L-R29-marker-edit-scope-patch" in html,
        "native_section_markers_noop": "function renderCoursewareSectionMarkers(title) {\n      return \"\";" in html,
        "native_process_overview_noop": "function renderCoursewareProcessOverviewMarkers() {\n      return \"\";" in html,
        "right_draft_present": "r29-courseware-draft" in html,
        "inline_popover_present": "r29-inline-edit-popover" in html,
        "right_draft_focus_present": "focusDraft(currentScreenIndexFromMarker(marker))" in html,
        "bad_markers_removed_runtime": "process_steps_only" in html,
        "runtime_not_connected": result.get("runtime_connected") is False,
        "provider_not_called": result.get("provider_called") is False,
        "model_not_called": result.get("model_called") is False,
        "database_not_written": result.get("database_written") is False,
        "memory_not_written": result.get("memory_written") is False,
        "feishu_not_written": result.get("feishu_written") is False,
        "upload_not_implemented": result.get("upload_implemented") is False,
        "search_not_implemented": result.get("search_implemented") is False,
        "whiteboard_library_not_connected": result.get("whiteboard_library_connected") is False,
        "formal_apply_not_performed": result.get("formal_apply_performed") is False,
        "main_project_not_pushed": result.get("main_project_pushed") is False,
        "github_not_uploaded": result.get("github_uploaded") is False,
        "smoke_script_injected": smoke.get("r29_script_injected") is True,
    }
    failures.extend(name for name, ok in checks.items() if not ok)

    if failures:
        raise SystemExit("FAIL: " + ", ".join(failures))
    print("PASS: 1013L R29 lesson courseware marker and inline edit scope patch")


if __name__ == "__main__":
    main()
