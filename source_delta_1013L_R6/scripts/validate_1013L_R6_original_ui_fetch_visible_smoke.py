from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R6_DIR = BASE / "1013L_R6_main_shell_original_ui_readonly_fetch_visible_smoke"


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
    result = read_json(R6_DIR / "1013L_R6_result.json")
    html_path = R6_DIR / "prep_room_render_canvas_deepen_v1_1013L_R6_original_ui_fetch_visible_smoke.html"
    if not html_path.exists():
        fail("missing R6 visible smoke html")
    html = html_path.read_text(encoding="utf-8-sig")

    for marker in [
        "ai-tool-strip",
        "toolRail",
        "viewTabs",
        "data-view",
        "coursewareExpanded",
        "chatInput",
        "main-shell-fetch-adapter-1013L-R5",
        "main-shell-original-ui-smoke-1013L-R6",
    ]:
        if marker not in html:
            fail(f"R6 html missing original-shell marker: {marker}")

    for marker in [
        "stateList",
        "stageBody",
        "agent-bar",
        "师维 · 主壳基线",
    ]:
        if marker in html:
            fail(f"R6 html still contains simplified-shell marker: {marker}")

    if result.get("final_status") != "PASS_1013L_R6_MAIN_SHELL_ORIGINAL_UI_READONLY_FETCH_VISIBLE_SMOKE":
        fail("unexpected R6 final status")
    for key in [
        "original_horizontal_tool_strip_preserved",
        "original_view_tabs_preserved",
        "original_data_view_switching_preserved",
        "courseware_expanded_route_preserved",
        "bottom_agent_input_preserved",
        "fetch_adapter_metadata_present",
        "screenshot_smoke_pass",
    ]:
        if result.get(key) is not True:
            fail(f"expected true result flag: {key}")
    for key in [
        "new_shell_standard_created",
        "simplified_shell_used_as_visible_shell",
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
        assert_false(result, key)

    for screenshot in result.get("visual_smoke_screenshots", []):
        screenshot_path = R6_DIR / screenshot
        if not screenshot_path.exists():
            fail(f"missing screenshot: {screenshot}")
        if screenshot_path.stat().st_size < 1024:
            fail(f"screenshot too small: {screenshot}")

    print("PASS: 1013L R6 original UI fetch visible smoke")


if __name__ == "__main__":
    main()
