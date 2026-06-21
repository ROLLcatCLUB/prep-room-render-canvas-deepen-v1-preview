from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE_DIR = BASE / "1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter"


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


def main() -> None:
    result = read_json(STAGE_DIR / "1013L_R5_result.json")
    contract = read_json(STAGE_DIR / "main_shell_backend_viewmodel_fetch_contract_1013L_R5.json")
    adapter_map = read_json(STAGE_DIR / "main_shell_state_fetch_adapter_map_1013L_R5.json")
    response = read_json(STAGE_DIR / "main_shell_viewmodel_readonly_response_fixture_1013L_R5.json")
    courseware_state = read_json(STAGE_DIR / "main_shell_state_viewmodel_courseware_workspace_1013L_R5.json")
    big_unit_state = read_json(STAGE_DIR / "main_shell_state_viewmodel_big_unit_design_1013L_R5.json")

    html_path = STAGE_DIR / "shiwei_main_render_shell_1013L_R5_fetch_adapter_static.html"
    if not html_path.exists():
        fail("missing R5 static shell html")
    html = html_path.read_text(encoding="utf-8-sig")
    for marker in [
        "main-shell-fetch-adapter-1013L-R5",
        "ai-tool-strip",
        "toolRail",
        "viewTabs",
        "data-view",
        "coursewareExpanded",
        "chatInput",
    ]:
        if marker not in html:
            fail(f"R5 html missing marker: {marker}")

    if result.get("final_status") != "PASS_1013L_R5_MAIN_SHELL_BACKEND_VIEWMODEL_READONLY_FETCH_ADAPTER":
        fail("unexpected R5 final status")
    if result.get("state_fetch_adapter_count") != 7:
        fail("unexpected R5 state adapter count")
    if result.get("teacher_visible_shell_reused") is not True:
        fail("R5 did not reuse the teacher-visible original shell")
    if result.get("original_horizontal_tool_strip_preserved") is not True:
        fail("original horizontal tool strip was not preserved")
    if result.get("original_view_switching_preserved") is not True:
        fail("original view switching was not preserved")
    if result.get("simplified_shell_used_as_visible_shell") is not False:
        fail("simplified shell was still used as visible shell")
    if result.get("screenshot_smoke_pass") is not True:
        fail("screenshot smoke did not pass")
    for screenshot in result.get("visual_smoke_screenshots", []):
        screenshot_path = STAGE_DIR / screenshot
        if not screenshot_path.exists():
            fail(f"missing screenshot smoke artifact: {screenshot}")
        if screenshot_path.stat().st_size < 1024:
            fail(f"screenshot smoke artifact is too small: {screenshot}")
    if response.get("viewmodel_type") != "prep_room_main_render_shell":
        fail("unexpected main shell viewmodel type")
    if response.get("fetch_adapter_map", {}).get("state_count") != 7:
        fail("response adapter map state count mismatch")

    expected_states = {
        "home_scene",
        "big_unit_design",
        "single_lesson_design",
        "courseware_workspace",
        "classroom_display_preview",
        "material_intake",
        "week_calendar",
    }
    actual_states = {item.get("state_id") for item in adapter_map.get("states", [])}
    missing = expected_states - actual_states
    if missing:
        fail(f"missing state adapters: {sorted(missing)}")

    routing = adapter_map.get("agent_profile", {}).get("routing", {})
    if routing.get("routing_depends_on_display_name") is not False:
        fail("agent routing still depends on display name")
    if routing.get("routing_key_field") != "active_capability":
        fail("agent routing key is not active_capability")

    if courseware_state.get("fetch_adapter", {}).get("source_fixture", "").find("1013K_R29A") < 0:
        fail("courseware state does not reuse 1013K_R29A viewmodel")
    if big_unit_state.get("fetch_adapter", {}).get("source_endpoint") != "/api/prep-room/big-unit-preview-viewmodel/big_unit_render_viewmodel_fixture_1013K_R7":
        fail("big-unit state does not point to existing readonly route")

    for payload in [result, contract.get("boundary", {}), adapter_map.get("boundary", {}), response.get("boundary", {})]:
        for key in [
            "formal_frontend_binding_allowed",
            "runtime_connected",
            "provider_called",
            "model_called",
            "database_written",
            "memory_written",
            "feishu_written",
            "formal_apply_performed",
            "main_project_pushed",
        ]:
            assert_false(payload, key)

    routes_text = (ROOT / "backend" / "xiaobei_ai" / "routes.py").read_text(encoding="utf-8-sig")
    if "prep_room_main_shell_fetch_adapter_1013L_R5" not in routes_text:
        fail("R5 adapter module is not registered in routes.py")

    print("PASS: 1013L R5 main shell fetch adapter")


if __name__ == "__main__":
    main()
