from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R11_DIR = BASE / "1013L_R11_existing_page_readonly_viewmodel_static_hydration_apply"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def read_json(path: Path):
    if not path.exists():
        fail(f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def assert_true(payload: dict, key: str) -> None:
    if payload.get(key) is not True:
        fail(f"expected true flag: {key}")


def assert_false(payload: dict, key: str) -> None:
    if payload.get(key) is not False:
        fail(f"expected false flag: {key}")


def main() -> None:
    result = read_json(R11_DIR / "1013L_R11_result.json")
    payload = read_json(R11_DIR / "readonly_viewmodel_static_hydration_payload_1013L_R11.json")
    smoke = read_json(R11_DIR / "visible_hydration_browser_smoke_1013L_R11.json")
    html_path = R11_DIR / "prep_room_render_canvas_deepen_v1_1013L_R11_static_hydration_apply.html"
    if not html_path.exists():
        fail("missing R11 hydrated html")
    html = html_path.read_text(encoding="utf-8-sig")

    if result.get("final_status") != "PASS_1013L_R11_EXISTING_PAGE_READONLY_VIEWMODEL_STATIC_HYDRATION_APPLY":
        fail("unexpected R11 final status")
    for key in [
        "courseware_viewmodel_embedded",
        "big_unit_viewmodel_embedded",
        "courseware_screen_array_hydrated",
        "display_preview_uses_same_viewmodel",
        "visible_hydration_smoke_pass",
        "existing_page_reused",
    ]:
        assert_true(result, key)
    for key in [
        "new_visible_page_created",
        "new_shell_standard_created",
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

    if result.get("courseware_screen_count") != 8:
        fail("unexpected hydrated courseware screen count")
    if result.get("smoke_case_count") != 3:
        fail("unexpected R11 smoke case count")

    for marker in [
        "ai-tool-strip",
        "toolRail",
        "viewTabs",
        "data-view",
        "coursewareExpanded",
        "chatInput",
        "main-shell-static-readonly-fetch-hook-1013L-R8",
        "main-shell-visible-hydration-style-1013L-R11",
        "main-shell-visible-hydration-payload-1013L-R11",
        "main-shell-visible-hydration-1013L-R11",
        "__SHIWEI_MAIN_SHELL_READONLY_FETCH_HOOK__",
    ]:
        if marker not in html:
            fail(f"R11 html missing marker: {marker}")

    for marker in [
        "stateList",
        "stageBody",
        "agent-bar",
        "师维 · 主壳基线",
    ]:
        if marker in html:
            fail(f"R11 html still contains simplified-shell marker: {marker}")

    compact = payload.get("compact_courseware_screens", [])
    if len(compact) != 8:
        fail("payload compact courseware screen count is not 8")
    if compact[2].get("source_screen_id") != "courseware_screen_seed_03_color_comparison_1013K_R25":
        fail("third hydrated screen does not come from R29A comparison seed")
    if payload.get("summary", {}).get("screen_count") != 8:
        fail("payload summary screen count mismatch")
    if payload.get("hydration_policy", {}).get("reuse_existing_page_functions") is not True:
        fail("R11 does not reuse existing page functions")
    if payload.get("hydration_policy", {}).get("replace_courseware_screen_array_only") is not True:
        fail("R11 does not use courseware screen array hydration")
    if payload.get("hydration_policy", {}).get("no_new_shell") is not True:
        fail("R11 allows new shell")

    if smoke.get("visible_hydration_smoke_pass") is not True:
        fail("R11 browser hydration smoke failed")
    if smoke.get("case_count") != 3:
        fail("R11 browser smoke case count mismatch")
    for case in smoke.get("cases", []):
        if case.get("pass") is not True:
            fail(f"R11 smoke case failed: {case.get('case_id')} missing {case.get('missing_markers')}")

    for payload_item in [
        result.get("boundary", {}),
        payload.get("boundary", {}),
        smoke.get("boundary", {}),
    ]:
        if "static_hydration_apply_only" in payload_item:
            assert_true(payload_item, "static_hydration_apply_only")
        for key in [
            "existing_page_reused",
        ]:
            if key in payload_item:
                assert_true(payload_item, key)
        for key in [
            "new_visible_page_created",
            "new_shell_standard_created",
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
            if key in payload_item:
                assert_false(payload_item, key)

    print("PASS: 1013L R11 existing page readonly viewmodel static hydration apply")


if __name__ == "__main__":
    main()
