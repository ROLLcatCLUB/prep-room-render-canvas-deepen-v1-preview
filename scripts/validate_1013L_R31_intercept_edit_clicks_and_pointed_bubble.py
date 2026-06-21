from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R31_DIR = BASE / "1013L_R31_intercept_edit_clicks_and_pointed_bubble"
HTML = R31_DIR / "prep_room_render_canvas_deepen_v1_1013L_R31_pointed_edit_bubble.html"
RESULT = R31_DIR / "1013L_R31_result.json"
SMOKE = R31_DIR / "pointed_edit_bubble_smoke_1013L_R31.json"
REPORT = R31_DIR / "1013L_R31_report.md"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> None:
    failures: list[str] = []
    for path in [HTML, RESULT, SMOKE, REPORT]:
        if not path.exists():
            failures.append(f"missing:{path.name}")

    if failures:
        raise SystemExit("FAIL: " + ", ".join(failures))

    html = HTML.read_text(encoding="utf-8-sig")
    result = read_json(RESULT)
    smoke = read_json(SMOKE)

    expected_status = "PASS_1013L_R31_INTERCEPT_EDIT_CLICKS_AND_POINTED_BUBBLE"
    checks = {
        "final_status_pass": result.get("final_status") == expected_status,
        "failed_checks_empty": result.get("failed_checks") == [],
        "old_edit_event_intercepted": result.get("old_edit_event_intercepted") is True,
        "left_top_old_panel_prevented": result.get("left_top_old_panel_prevented") is True,
        "arrow_points_to_clicked_row": result.get("edit_bubble_arrow_points_to_clicked_row") is True,
        "no_rerender_flash": result.get("lesson_edit_bubble_created_without_rerender_flash") is True,
        "big_unit_same_pattern": result.get("big_unit_edit_bubble_uses_same_pattern") is True,
        "center_hints_removed": result.get("center_courseware_hints_removed") is True,
        "inherits_existing_page_lineage": result.get("inherits_existing_page_lineage") is True,
        "new_disconnected_page_not_created": result.get("new_disconnected_page_created") is False,
        "inherits_r30": "script-1013L-R30-center-hints-edit-bubble-fix" in html,
        "r31_script_present": "script-1013L-R31-pointed-edit-bubble" in html,
        "r31_style_present": "style-1013L-R31-pointed-edit-bubble" in html,
        "old_bubbles_hidden": ".nb-readable-step .nb-edit-bubble:not(.r31-pointed-edit-bubble)" in html,
        "stop_immediate_present": "event.stopImmediatePropagation()" in html,
        "arrow_top_present": "--r31-arrow-top" in html,
        "pointed_attr_present": "pointed_to_clicked_row" in html,
        "big_unit_intercept_present": "[data-r6p-edit], [data-r6p-view]" in html,
        "smoke_r31_script": smoke.get("r31_script_injected") is True,
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
    }
    failures.extend(name for name, ok in checks.items() if not ok)

    if failures:
        raise SystemExit("FAIL: " + ", ".join(failures))
    print("PASS: 1013L R31 intercept edit clicks and pointed bubble")


if __name__ == "__main__":
    main()
