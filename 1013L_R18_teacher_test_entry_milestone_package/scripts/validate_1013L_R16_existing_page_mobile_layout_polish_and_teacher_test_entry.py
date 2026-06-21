from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R16_DIR = BASE / "1013L_R16_existing_page_mobile_layout_polish_and_teacher_test_entry"


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
    result = read_json(R16_DIR / "1013L_R16_result.json")
    smoke = read_json(R16_DIR / "mobile_layout_polish_smoke_1013L_R16.json")
    html_path = R16_DIR / "prep_room_render_canvas_deepen_v1_1013L_R16_mobile_polish_teacher_test_entry.html"
    entry_path = R16_DIR / "teacher_test_entry_1013L_R16.md"
    if not html_path.exists():
        fail("missing R16 html")
    if not entry_path.exists():
        fail("missing R16 teacher entry")
    html = html_path.read_text(encoding="utf-8-sig")
    entry = entry_path.read_text(encoding="utf-8-sig")

    if result.get("final_status") != "PASS_1013L_R16_EXISTING_PAGE_MOBILE_LAYOUT_POLISH_AND_TEACHER_TEST_ENTRY":
        fail("unexpected R16 final status")
    for key in [
        "mobile_layout_polished",
        "mobile_big_unit_body_visible_smoke_pass",
        "teacher_test_entry_created",
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

    for marker in [
        "main-shell-mobile-polish-style-1013L-R16",
        "main-shell-mobile-polish-1013L-R16",
        "data-1013l-r13-big-unit-surface",
        "main-shell-big-unit-visible-hydration-1013L-R13",
        "main-shell-visible-hydration-1013L-R11",
    ]:
        if marker not in html:
            fail(f"R16 html missing marker: {marker}")
    for marker in [
        "?r13=bigUnit",
        "?mode=edit#coursewareExpanded",
        "?preview=display&screen=03#coursewareExpanded",
    ]:
        if marker not in entry:
            fail(f"R16 teacher entry missing marker: {marker}")

    if smoke.get("smoke_pass") is not True:
        fail("R16 smoke failed")
    cases = smoke.get("cases", [])
    if len(cases) != 2:
        fail("R16 smoke case count mismatch")
    for case in cases:
        if case.get("pass") is not True:
            fail(f"R16 smoke case failed: {case.get('case_id')} missing {case.get('missing_markers')}")
        screenshot = ROOT / case.get("path", "")
        if not screenshot.exists():
            fail(f"missing screenshot: {screenshot}")
        if screenshot.stat().st_size != case.get("bytes"):
            fail(f"screenshot byte size mismatch: {screenshot}")
        if case.get("bytes", 0) < 10000:
            fail(f"screenshot too small: {screenshot}")

    boundary = smoke.get("boundary", {})
    assert_true(boundary, "mobile_static_polish_only")
    assert_true(boundary, "existing_page_reused")
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
        "formal_frontend_binding_allowed",
    ]:
        assert_false(boundary, key)

    print("PASS: 1013L R16 existing page mobile layout polish and teacher test entry")


if __name__ == "__main__":
    main()
