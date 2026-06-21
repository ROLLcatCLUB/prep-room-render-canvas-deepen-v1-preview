from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R9_DIR = BASE / "1013L_R9_original_page_viewmodel_hydration_static_smoke"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def read_json(path: Path):
    if not path.exists():
        fail(f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def assert_false(payload: dict, key: str) -> None:
    if payload.get(key) is not False:
        fail(f"expected false flag: {key}")


def assert_true(payload: dict, key: str) -> None:
    if payload.get(key) is not True:
        fail(f"expected true flag: {key}")


def main() -> None:
    result = read_json(R9_DIR / "1013L_R9_result.json")
    smoke = read_json(R9_DIR / "hook_resolution_browser_smoke_1013L_R9.json")
    html_path = R9_DIR / "prep_room_render_canvas_deepen_v1_1013L_R9_hook_smoke.html"
    if not html_path.exists():
        fail("missing R9 hook smoke html")
    html = html_path.read_text(encoding="utf-8-sig")

    if result.get("final_status") != "PASS_1013L_R9_ORIGINAL_PAGE_VIEWMODEL_HYDRATION_STATIC_SMOKE":
        fail("unexpected R9 final status")
    for key in [
        "hook_resolution_smoke_pass",
        "expected_states_passed",
        "original_page_shell_preserved",
    ]:
        assert_true(result, key)
    for key in [
        "new_visible_page_created",
        "visible_dom_changed",
        "runtime_connected",
        "real_fetch_performed",
        "provider_called",
        "model_called",
        "database_written",
        "memory_written",
        "feishu_written",
        "formal_apply_performed",
        "main_project_pushed",
        "github_uploaded",
    ]:
        assert_false(result, key)

    for marker in [
        "ai-tool-strip",
        "toolRail",
        "viewTabs",
        "data-view",
        "coursewareExpanded",
        "chatInput",
        "main-shell-static-readonly-fetch-hook-1013L-R8",
        "__SHIWEI_MAIN_SHELL_READONLY_FETCH_HOOK__",
        "main-shell-hook-smoke-runner-1013L-R9",
    ]:
        if marker not in html:
            fail(f"R9 html missing marker: {marker}")

    expected = {
        "default_single_lesson": "single_lesson_design",
        "week_calendar": "week_calendar",
        "prep_notebook": "single_lesson_design",
        "courseware_expanded": "courseware_workspace",
        "display_preview": "classroom_display_preview",
    }
    cases = smoke.get("cases", [])
    if len(cases) != 5:
        fail("unexpected R9 smoke case count")
    for case in cases:
        case_id = case.get("case_id")
        if case_id not in expected:
            fail(f"unexpected R9 smoke case: {case_id}")
        if case.get("actual_state_id") != expected[case_id]:
            fail(f"case {case_id} resolved to {case.get('actual_state_id')}, expected {expected[case_id]}")
        if case.get("readonly_endpoint") != f"/api/prep-room/main-shell/viewmodel/state/{expected[case_id]}":
            fail(f"case {case_id} has unexpected readonly endpoint")
        if case.get("real_fetch_performed") is not False:
            fail(f"case {case_id} performed real fetch")
        if case.get("pass") is not True:
            fail(f"case {case_id} did not pass")

    assert_true(smoke, "hook_resolution_smoke_pass")
    boundary = smoke.get("boundary", {})
    assert_true(boundary, "static_browser_smoke_only")
    for key in [
        "visible_dom_changed",
        "runtime_connected",
        "real_fetch_performed",
        "provider_called",
        "model_called",
        "database_written",
        "memory_written",
        "feishu_written",
        "formal_apply_performed",
        "main_project_pushed",
    ]:
        assert_false(boundary, key)

    print("PASS: 1013L R9 original page viewmodel hydration static smoke")


if __name__ == "__main__":
    main()
