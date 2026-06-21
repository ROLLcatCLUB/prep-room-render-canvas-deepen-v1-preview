from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R17_DIR = BASE / "1013L_R17_existing_page_teacher_test_desktop_smoke_package"


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
    result = read_json(R17_DIR / "1013L_R17_result.json")
    smoke = read_json(R17_DIR / "teacher_test_desktop_smoke_1013L_R17.json")
    html_path = R17_DIR / "prep_room_render_canvas_deepen_v1_1013L_R17_teacher_test_desktop.html"
    entry_path = R17_DIR / "teacher_test_entry_1013L_R17.md"
    report_path = R17_DIR / "1013L_R17_report.md"
    for path in [html_path, entry_path, report_path]:
        if not path.exists():
            fail(f"missing R17 artifact: {path}")

    if result.get("final_status") != "PASS_1013L_R17_EXISTING_PAGE_TEACHER_TEST_DESKTOP_SMOKE_PACKAGE":
        fail("unexpected R17 final status")
    if result.get("failed_checks") != []:
        fail(f"R17 has failed checks: {result.get('failed_checks')}")
    if smoke.get("smoke_pass") is not True:
        fail("R17 smoke did not pass")

    for key in [
        "desktop_teacher_test_package_created",
        "teacher_test_entry_created",
        "desktop_big_unit_smoke_pass",
        "desktop_courseware_edit_smoke_pass",
        "desktop_display_preview_smoke_pass",
        "teacher_test_desktop_smoke_only",
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
        "formal_frontend_binding_allowed",
    ]:
        assert_false(result, key)

    cases = smoke.get("cases", [])
    if len(cases) != 3:
        fail("R17 smoke case count mismatch")
    for case in cases:
        if case.get("pass") is not True:
            fail(f"R17 smoke case failed: {case.get('case_id')} missing {case.get('missing_markers')}")
        screenshot = ROOT / case.get("path", "")
        if not screenshot.exists():
            fail(f"missing screenshot: {screenshot}")
        if screenshot.stat().st_size != case.get("bytes"):
            fail(f"screenshot byte size mismatch: {screenshot}")
        if case.get("bytes", 0) < 10000:
            fail(f"screenshot too small: {screenshot}")
        size = case.get("png_size") or {}
        if size.get("width") != 1920 or size.get("height") != 1080:
            fail(f"unexpected screenshot size: {case.get('case_id')} {size}")

    html = html_path.read_text(encoding="utf-8-sig")
    for forbidden in ["小备草稿", "大单元编辑后续接弹窗", "当前只做只读渲染"]:
        if forbidden in html:
            fail(f"forbidden visible phrase remains in R17 html: {forbidden}")
    for required in ["小教草稿", "编辑会在弹窗里处理，教师确认前不写入正式备课本。"]:
        if required not in html:
            fail(f"required current phrase missing in R17 html: {required}")

    print("PASS: 1013L R17 existing page teacher test desktop smoke package")


if __name__ == "__main__":
    main()
