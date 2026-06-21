from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R30_DIR = BASE / "1013L_R30_remove_center_courseware_hints_and_restore_edit_bubble"
HTML = R30_DIR / "prep_room_render_canvas_deepen_v1_1013L_R30_center_hints_edit_bubble_fix.html"
RESULT = R30_DIR / "1013L_R30_result.json"
PATCH = R30_DIR / "center_hints_edit_bubble_patch_1013L_R30.json"
SMOKE = R30_DIR / "center_hints_edit_bubble_smoke_1013L_R30.json"


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
    smoke = read_json(SMOKE)

    expected_status = "PASS_1013L_R30_REMOVE_CENTER_COURSEWARE_HINTS_AND_RESTORE_EDIT_BUBBLE"
    checks = {
        "final_status_pass": result.get("final_status") == expected_status,
        "failed_checks_empty": result.get("failed_checks") == [],
        "center_courseware_hints_removed": result.get("center_courseware_hints_removed") is True,
        "r29_extra_right_draft_removed": result.get("r29_extra_right_draft_removed") is True,
        "r29_left_top_popover_removed": result.get("r29_left_top_popover_removed") is True,
        "right_rail_existing_draft_reused": result.get("right_rail_existing_draft_reused") is True,
        "edit_bubble_style_restored": result.get("edit_bubble_style_restored") is True,
        "edit_bubble_aligned": result.get("edit_bubble_aligned_to_clicked_row") is True,
        "big_unit_same_bubble": result.get("big_unit_edit_uses_same_bubble_pattern") is True,
        "inherits_existing_page_lineage": result.get("inherits_existing_page_lineage") is True,
        "new_disconnected_page_not_created": result.get("new_disconnected_page_created") is False,
        "inherits_r29": "script-1013L-R29-marker-edit-scope-patch" in html,
        "r30_script_present": "script-1013L-R30-center-hints-edit-bubble-fix" in html,
        "r30_style_present": "style-1013L-R30-center-hints-edit-bubble-fix" in html,
        "central_hints_hide_css_present": ".nb-readable-process .courseware-section-rail" in html,
        "r29_draft_hide_css_present": ".r29-courseware-draft" in html,
        "r29_popover_hide_css_present": ".r29-inline-edit-popover" in html,
        "nb_edit_bubble_reused": "nb-edit-bubble r30-follow-edit-bubble" in html,
        "right_draft_note_present": "data-1013l-r30-right-draft-in-place" in html,
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
        "smoke_r30_script": smoke.get("r30_script_injected") is True,
    }
    failures.extend(name for name, ok in checks.items() if not ok)

    if failures:
        raise SystemExit("FAIL: " + ", ".join(failures))
    print("PASS: 1013L R30 remove center courseware hints and restore edit bubble")


if __name__ == "__main__":
    main()
