from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R34_DIR = BASE / "1013L_R34_process_courseware_cards_visible_fix"
HTML = R34_DIR / "prep_room_render_canvas_deepen_v1_1013L_R34_process_cards_visible.html"
RESULT = R34_DIR / "1013L_R34_result.json"
SMOKE = R34_DIR / "process_cards_visible_smoke_1013L_R34.json"
REPORT = R34_DIR / "1013L_R34_report.md"


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

    expected_status = "PASS_1013L_R34_PROCESS_COURSEWARE_CARDS_VISIBLE_FIX"
    checks = {
        "final_status_pass": result.get("final_status") == expected_status,
        "failed_checks_empty": result.get("failed_checks") == [],
        "inherits_r33": "script-1013L-R33-process-cards-scroll" in html,
        "r34_script_present": "script-1013L-R34-process-courseware-cards-visible" in html,
        "r34_style_present": "style-1013L-R34-process-courseware-cards-visible" in html,
        "new_card_class_present": "r34-process-display-card" in html,
        "new_chip_class_present": "r34-screen-chip" in html,
        "new_note_class_present": "r34-screen-note" in html,
        "does_not_depend_on_old_marker_class": result.get("old_courseware_section_rail_not_required_for_process_cards") is True,
        "cleanup_resistant": result.get("r31_r32_cleanup_resistant") is True and "MutationObserver" in html,
        "r32_duplicate_removed_runtime": result.get("right_rail_extra_r32_block_removed") is True and "removeDuplicateR32RightBlock" in html,
        "right_original_kept": result.get("original_right_rail_courseware_draft_kept") is True,
        "non_process_not_restored": result.get("non_process_section_courseware_cards_restored") is False,
        "no_disconnected_page": result.get("new_disconnected_page_created") is False,
        "smoke_r34_script": smoke.get("r34_script_injected") is True,
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
    print("PASS: 1013L R34 process courseware cards visible fix")


if __name__ == "__main__":
    main()
