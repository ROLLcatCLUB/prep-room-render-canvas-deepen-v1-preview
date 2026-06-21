from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R15_DIR = BASE / "1013L_R15_existing_page_hydration_milestone_package"


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
    result = read_json(R15_DIR / "1013L_R15_result.json")
    file_index = read_json(R15_DIR / "milestone_file_index_1013L_R15.json")
    latest = (BASE / "LATEST_REVIEW_ENTRY.md").read_text(encoding="utf-8-sig")
    manifest = (BASE / "REVIEW_PACKAGE_MANIFEST.md").read_text(encoding="utf-8-sig")
    prompt = (BASE / "GPT_REVIEW_PROMPT_1013L_R15.md").read_text(encoding="utf-8-sig")

    if result.get("final_status") != "PASS_1013L_R15_EXISTING_PAGE_HYDRATION_MILESTONE_PACKAGE":
        fail("unexpected R15 final status")
    for key in [
        "r11_pass",
        "r12_pass",
        "r13_pass",
        "r14_pass",
        "existing_page_reused",
        "original_horizontal_tool_strip_preserved",
        "original_view_switching_preserved",
        "resident_agent_input_preserved",
        "courseware_viewmodel_visible_hydrated",
        "display_preview_uses_hydrated_courseware_viewmodel",
        "big_unit_viewmodel_visible_hydrated",
        "desktop_big_unit_visual_smoke_pass",
        "desktop_normal_visual_smoke_pass",
        "mobile_big_unit_smoke_dom_pass",
        "mobile_layout_polish_required",
        "github_uploaded",
        "github_review_package_uploaded",
    ]:
        assert_true(result, key)
    for key in [
        "formal_frontend_binding_allowed",
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
        assert_false(result, key)
    if result.get("big_unit_chunk_count") != 10:
        fail("unexpected big-unit chunk count")
    if result.get("failed_checks") != []:
        fail(f"R15 failed checks are not empty: {result.get('failed_checks')}")
    if len(result.get("r14_visual_cases", [])) != 3:
        fail("R15 did not record R14 visual cases")

    boundary = result.get("boundary", {})
    assert_true(boundary, "milestone_package_only")
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

    if file_index.get("missing_files") != []:
        fail("R15 file index has missing files")
    if file_index.get("file_count", 0) < 30:
        fail("R15 file index is unexpectedly small")
    for item in file_index.get("files", []):
        path = ROOT / item.get("path", "")
        if not path.exists():
            fail(f"indexed file missing: {path}")
        if path.stat().st_size != item.get("bytes"):
            fail(f"indexed byte size mismatch: {path}")

    for text, label in [
        (latest, "LATEST_REVIEW_ENTRY.md"),
        (manifest, "REVIEW_PACKAGE_MANIFEST.md"),
        (prompt, "GPT_REVIEW_PROMPT_1013L_R15.md"),
    ]:
        for marker in [
            "1013L_R15_EXISTING_PAGE_HYDRATION_MILESTONE_PACKAGE",
            "mobile_layout_polish_required=true",
            "formal_frontend_binding_allowed=false",
            "runtime_connected=false",
            "provider_called=false",
            "model_called=false",
            "formal_apply_performed=false",
        ]:
            if marker not in text:
                fail(f"{label} missing marker: {marker}")

    print("PASS: 1013L R15 existing page hydration milestone package")


if __name__ == "__main__":
    main()
