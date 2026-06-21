from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R35_DIR = BASE / "1013L_R35_paragraph_level_courseware_cards"
HTML = R35_DIR / "prep_room_render_canvas_deepen_v1_1013L_R35_paragraph_courseware_cards.html"
RESULT = R35_DIR / "1013L_R35_result.json"
SMOKE = R35_DIR / "paragraph_courseware_cards_smoke_1013L_R35.json"
REPORT = R35_DIR / "1013L_R35_report.md"


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

    expected_status = "PASS_1013L_R35_PARAGRAPH_LEVEL_COURSEWARE_CARDS_PATCH"
    checks = {
        "final_status_pass": result.get("final_status") == expected_status,
        "failed_checks_empty": result.get("failed_checks") == [],
        "inherits_r34": "script-1013L-R34-process-courseware-cards-visible" in html,
        "r35_script_present": "script-1013L-R35-paragraph-courseware-cards" in html,
        "r35_style_present": "style-1013L-R35-paragraph-courseware-cards" in html,
        "paragraph_cards_present": "r35-inline-screen-card" in html and "paragraphMap" in html,
        "add_screen_entry_present": "r35-add-screen-card" in html,
        "single_screen_05_present": "screen_05_task" in html and "大屏 05" in html,
        "single_screen_06_present": "screen_06_whiteboard" in html and "大屏 06" in html,
        "no_combined_cards": result.get("combined_screen_cards_removed") is True,
        "each_card_single_screen": result.get("each_visible_card_targets_single_screen") is True,
        "right_selection_capture": result.get("right_draft_click_no_longer_selects_all_rows") is True and "stopImmediatePropagation" in html,
        "right_selection_attr": "data-1013l-r35-selected-screen" in html,
        "aggregate_hidden": ".r34-process-display-card" in html and "display: none !important" in html,
        "no_disconnected_page": result.get("new_disconnected_page_created") is False,
        "smoke_paragraph_level": smoke.get("paragraph_level_cards_created") is True,
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
    print("PASS: 1013L R35 paragraph level courseware cards patch")


if __name__ == "__main__":
    main()
