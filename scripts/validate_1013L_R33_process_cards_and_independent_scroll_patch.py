from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R33_DIR = BASE / "1013L_R33_process_courseware_cards_and_independent_scroll"
HTML = R33_DIR / "prep_room_render_canvas_deepen_v1_1013L_R33_process_cards_scroll.html"
RESULT = R33_DIR / "1013L_R33_result.json"
SMOKE = R33_DIR / "process_cards_scroll_smoke_1013L_R33.json"
REPORT = R33_DIR / "1013L_R33_report.md"


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

    expected_status = "PASS_1013L_R33_PROCESS_COURSEWARE_CARDS_AND_INDEPENDENT_SCROLL_PATCH"
    checks = {
        "final_status_pass": result.get("final_status") == expected_status,
        "failed_checks_empty": result.get("failed_checks") == [],
        "inherits_r32": "script-1013L-R32-right-rail-courseware-cards" in html,
        "r33_script_present": "script-1013L-R33-process-cards-scroll" in html,
        "r33_style_present": "style-1013L-R33-process-cards-scroll" in html,
        "r32_extra_block_hidden": ".r32-courseware-right-draft" in html and "display: none !important" in html,
        "process_cards_marker_present": "data-1013l-r33-process-card" in html,
        "process_display_override_present": ".nb-workspace .r33-process-courseware-card" in html and "display: flex !important" in html,
        "non_process_not_restored": result.get("non_process_section_courseware_cards_restored") is False,
        "original_right_draft_kept": result.get("original_right_rail_courseware_draft_kept") is True,
        "right_draft_local_selection": result.get("right_draft_click_selects_card_only") is True and "data-1013l-r33-selected-right-draft" in html,
        "independent_scroll_enabled": result.get("prep_column_independent_scroll") is True and "data-1013l-r33-independent-scroll" in html,
        "left_independent_scroll": result.get("left_catalog_independent_scroll") is True,
        "right_independent_scroll": result.get("right_rail_independent_scroll") is True,
        "no_disconnected_page": result.get("new_disconnected_page_created") is False,
        "smoke_process_cards": smoke.get("process_cards_restored") is True,
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
    print("PASS: 1013L R33 process cards and independent scroll patch")


if __name__ == "__main__":
    main()
