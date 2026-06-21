from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R12_DIR = BASE / "1013L_R12_existing_page_hydrated_viewmodel_visual_smoke"


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
    result = read_json(R12_DIR / "1013L_R12_result.json")
    smoke = read_json(R12_DIR / "hydrated_viewmodel_visual_smoke_1013L_R12.json")

    if result.get("final_status") != "PASS_1013L_R12_EXISTING_PAGE_HYDRATED_VIEWMODEL_VISUAL_SMOKE":
        fail("unexpected R12 final status")
    for key in [
        "visual_smoke_pass",
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
    if result.get("screenshot_count") != 4:
        fail("unexpected R12 screenshot count")

    if smoke.get("visual_smoke_pass") is not True:
        fail("R12 visual smoke did not pass")
    cases = smoke.get("cases", [])
    if len(cases) != 4:
        fail("R12 visual smoke case count mismatch")
    for case in cases:
        if case.get("pass") is not True:
            fail(f"visual smoke case failed: {case.get('case_id')}")
        screenshot = ROOT / case.get("path", "")
        if not screenshot.exists():
            fail(f"missing screenshot: {screenshot}")
        if screenshot.stat().st_size != case.get("bytes"):
            fail(f"screenshot byte size mismatch: {screenshot}")
        if case.get("bytes", 0) < 10000:
            fail(f"screenshot too small: {screenshot}")
        if case.get("actual_width") != case.get("width") or case.get("actual_height") != case.get("height"):
            fail(f"screenshot dimensions mismatch: {screenshot}")

    boundary = smoke.get("boundary", {})
    assert_true(boundary, "visual_smoke_only")
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

    print("PASS: 1013L R12 existing page hydrated viewmodel visual smoke")


if __name__ == "__main__":
    main()
