from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R13_DIR = BASE / "1013L_R13_existing_page_big_unit_viewmodel_visible_hydration"


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


def assert_boundary_clean(payload: dict) -> None:
    for key in [
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
        if key in payload:
            assert_false(payload, key)


def main() -> None:
    result = read_json(R13_DIR / "1013L_R13_result.json")
    payload = read_json(R13_DIR / "big_unit_visible_hydration_payload_1013L_R13.json")
    smoke = read_json(R13_DIR / "big_unit_visible_hydration_browser_smoke_1013L_R13.json")
    html_path = R13_DIR / "prep_room_render_canvas_deepen_v1_1013L_R13_big_unit_visible_hydration.html"
    if not html_path.exists():
        fail("missing R13 hydrated html")
    html = html_path.read_text(encoding="utf-8-sig")

    if result.get("final_status") != "PASS_1013L_R13_EXISTING_PAGE_BIG_UNIT_VIEWMODEL_VISIBLE_HYDRATION":
        fail("unexpected R13 final status")

    for key in [
        "existing_page_reused",
        "left_tree_big_unit_entry_preserved",
        "big_unit_viewmodel_visible_hydrated",
        "render_big_unit_surface_overridden_from_viewmodel",
        "right_resource_rail_preserved",
        "browser_smoke_pass",
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

    if result.get("big_unit_chunk_count") != 10:
        fail("expected 10 big-unit chunks")
    if payload.get("summary", {}).get("chunk_count") != 10:
        fail("payload chunk_count mismatch")
    if payload.get("summary", {}).get("side_note_count", 0) < 8:
        fail("expected side notes for big-unit chunks")
    if payload.get("hydration_policy", {}).get("reuse_existing_page_functions") is not True:
        fail("R13 does not reuse existing page functions")
    if payload.get("hydration_policy", {}).get("no_new_shell") is not True:
        fail("R13 allows a new shell")

    for marker in [
        "ai-tool-strip",
        "toolRail",
        "viewTabs",
        "data-view",
        "coursewareExpanded",
        "chatInput",
        "main-shell-visible-hydration-1013L-R11",
        "main-shell-big-unit-visible-hydration-payload-1013L-R13",
        "main-shell-big-unit-visible-hydration-1013L-R13",
        "renderBigUnitFromViewModel",
        "data-1013l-r13-big-unit-surface",
    ]:
        if marker not in html:
            fail(f"R13 html missing marker: {marker}")

    for marker in [
        "stateList",
        "stageBody",
        "agent-bar",
        "师维 · 主壳基线",
    ]:
        if marker in html:
            fail(f"R13 html still contains simplified-shell marker: {marker}")

    smoke_cases = smoke.get("cases", [])
    if smoke.get("big_unit_visible_hydration_smoke_pass") is not True:
        fail("R13 browser hydration smoke failed")
    if smoke.get("case_count") != 3 or len(smoke_cases) != 3:
        fail("R13 browser smoke case count mismatch")
    for case in smoke_cases:
        if case.get("pass") is not True:
            fail(f"R13 smoke case failed: {case.get('case_id')} missing {case.get('missing_markers')}")

    for payload_item in [
        result.get("boundary", {}),
        payload.get("boundary", {}),
        smoke.get("boundary", {}),
    ]:
        if "existing_page_reused" in payload_item:
            assert_true(payload_item, "existing_page_reused")
        for key in [
            "new_visible_page_created",
            "new_shell_standard_created",
        ]:
            if key in payload_item:
                assert_false(payload_item, key)
        assert_boundary_clean(payload_item)

    print("PASS: 1013L R13 existing page big-unit viewmodel visible hydration")


if __name__ == "__main__":
    main()
