from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R10_DIR = BASE / "1013L_R10_existing_page_readonly_viewmodel_binding_milestone_package"


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
    result = read_json(R10_DIR / "1013L_R10_result.json")
    file_index = read_json(R10_DIR / "milestone_file_index_1013L_R10.json")
    latest = (BASE / "LATEST_REVIEW_ENTRY.md").read_text(encoding="utf-8-sig")
    manifest = (BASE / "REVIEW_PACKAGE_MANIFEST.md").read_text(encoding="utf-8-sig")
    prompt = (BASE / "GPT_REVIEW_PROMPT_1013L_R10.md").read_text(encoding="utf-8-sig")

    if result.get("final_status") != "PASS_1013L_R10_EXISTING_PAGE_READONLY_VIEWMODEL_BINDING_MILESTONE_PACKAGE":
        fail("unexpected R10 final status")
    for key in [
        "r7_pass",
        "r8_pass",
        "r9_pass",
        "existing_original_page_reused",
        "original_horizontal_tool_strip_preserved",
        "original_view_switching_preserved",
        "resident_agent_input_preserved",
        "hidden_readonly_fetch_hook_created",
        "hook_resolution_smoke_pass",
        "github_uploaded",
        "github_review_package_uploaded",
    ]:
        assert_true(result, key)
    for key in [
        "new_visible_page_created",
        "new_shell_standard_created",
        "formal_frontend_binding_allowed",
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
    if result.get("smoke_case_count") != 5:
        fail("unexpected R10 smoke case count")
    if result.get("failed_checks") != []:
        fail(f"R10 failed checks are not empty: {result.get('failed_checks')}")

    boundary = result.get("boundary", {})
    assert_true(boundary, "milestone_package_only")
    for key in [
        "new_visible_page_created",
        "new_shell_standard_created",
        "visible_dom_changed_in_r10",
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
        fail("R10 file index has missing files")
    if file_index.get("file_count", 0) < 20:
        fail("R10 file index is unexpectedly small")

    for text, label in [
        (latest, "LATEST_REVIEW_ENTRY.md"),
        (manifest, "REVIEW_PACKAGE_MANIFEST.md"),
        (prompt, "GPT_REVIEW_PROMPT_1013L_R10.md"),
    ]:
        for marker in [
            "1013L_R10_EXISTING_PAGE_READONLY_VIEWMODEL_BINDING_MILESTONE_PACKAGE",
            "runtime_connected=false",
            "provider_called=false",
            "model_called=false",
            "formal_apply_performed=false",
        ]:
            if marker not in text:
                fail(f"{label} missing marker: {marker}")

    print("PASS: 1013L R10 existing page readonly viewmodel binding milestone package")


if __name__ == "__main__":
    main()
