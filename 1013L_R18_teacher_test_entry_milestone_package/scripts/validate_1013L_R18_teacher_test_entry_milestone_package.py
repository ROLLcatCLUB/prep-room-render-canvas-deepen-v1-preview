from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R18_DIR = BASE / "1013L_R18_teacher_test_entry_milestone_package"


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
    result = read_json(R18_DIR / "1013L_R18_result.json")
    if result.get("final_status") != "PASS_1013L_R18_TEACHER_TEST_ENTRY_MILESTONE_PACKAGE":
        fail("unexpected R18 final status")
    if result.get("failed_checks") != []:
        fail(f"R18 has failed checks: {result.get('failed_checks')}")

    for key in [
        "review_package_created",
        "teacher_test_entry_ready",
        "desktop_smoke_pass",
        "mobile_smoke_pass",
        "r5_guard_closure_included",
        "milestone_package_only",
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
        "formal_frontend_binding_allowed",
    ]:
        assert_false(result, key)

    required_paths = [
        "REVIEW_PACKAGE_MANIFEST_1013L_R18.md",
        "GPT_REVIEW_PROMPT_1013L_R18.md",
        "1013L_R18_report.md",
        "1013L_R16_existing_page_mobile_layout_polish_and_teacher_test_entry/1013L_R16_result.json",
        "1013L_R16A_r5_guard_closure_note_for_current_line/1013L_R16A_result.json",
        "1013L_R17_existing_page_teacher_test_desktop_smoke_package/1013L_R17_result.json",
        "1013L_R17_existing_page_teacher_test_desktop_smoke_package/prep_room_render_canvas_deepen_v1_1013L_R17_teacher_test_desktop.html",
        "1013L_R17_existing_page_teacher_test_desktop_smoke_package/ui_smoke_1013L_R17_desktop_big_unit.png",
        "1013L_R17_existing_page_teacher_test_desktop_smoke_package/ui_smoke_1013L_R17_desktop_courseware_edit.png",
        "1013L_R17_existing_page_teacher_test_desktop_smoke_package/ui_smoke_1013L_R17_desktop_display_preview.png",
    ]
    for rel_path in required_paths:
        if not (R18_DIR / rel_path).exists():
            fail(f"missing required R18 package file: {rel_path}")

    html = (R18_DIR / "1013L_R17_existing_page_teacher_test_desktop_smoke_package" / "prep_room_render_canvas_deepen_v1_1013L_R17_teacher_test_desktop.html").read_text(encoding="utf-8-sig")
    for forbidden in ["小备草稿", "大单元编辑后续接弹窗", "当前只做只读渲染"]:
        if forbidden in html:
            fail(f"forbidden phrase remains in packaged html: {forbidden}")
    for required in ["小教草稿", "第一单元《多变的色彩》", "进入大屏预览", "退出预览"]:
        if required not in html:
            fail(f"required phrase missing in packaged html: {required}")

    if result.get("copied_artifact_count", 0) < 18:
        fail("R18 copied artifact count too low")

    print("PASS: 1013L R18 teacher test entry milestone package")


if __name__ == "__main__":
    main()
