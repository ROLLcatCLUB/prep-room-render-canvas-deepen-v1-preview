from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R32_DIR = BASE / "1013L_R32_restore_right_rail_courseware_cards_only"
HTML = R32_DIR / "prep_room_render_canvas_deepen_v1_1013L_R32_right_rail_courseware_cards.html"
RESULT = R32_DIR / "1013L_R32_result.json"
SMOKE = R32_DIR / "right_rail_courseware_cards_smoke_1013L_R32.json"
REPORT = R32_DIR / "1013L_R32_report.md"


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

    expected_status = "PASS_1013L_R32_RESTORE_RIGHT_RAIL_COURSEWARE_CARDS_ONLY"
    checks = {
        "final_status_pass": result.get("final_status") == expected_status,
        "failed_checks_empty": result.get("failed_checks") == [],
        "inherits_r31": "script-1013L-R31-pointed-edit-bubble" in html,
        "r32_script_present": "script-1013L-R32-right-rail-courseware-cards" in html,
        "r32_style_present": "style-1013L-R32-right-rail-courseware-cards" in html,
        "right_rail_block_present": "r32-courseware-right-draft" in html,
        "right_rail_card_grid_present": "r32-courseware-card-grid" in html,
        "right_rail_detail_present": "data-r32-courseware-detail" in html,
        "reads_existing_viewmodel": "1013k-courseware-screen-viewmodel" in html,
        "fallback_eight_screens_present": "fallbackScreens" in html and "总结回看" in html,
        "center_cleanup_kept": "data-1013l-r32-center-courseware-hints" in html,
        "center_hints_not_restored": result.get("center_courseware_hints_restored") is False,
        "target_area_right_only": result.get("screen_cards_target_area") == "right_rail_courseware_draft_only",
        "no_disconnected_page": result.get("new_disconnected_page_created") is False,
        "r29_top_extra_block_not_restored": result.get("r29_top_extra_block_restored") is False and ".r29-courseware-draft" in html,
        "smoke_right_restored": smoke.get("right_rail_cards_restored") is True,
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
    print("PASS: 1013L R32 right rail courseware cards restored only")


if __name__ == "__main__":
    main()
