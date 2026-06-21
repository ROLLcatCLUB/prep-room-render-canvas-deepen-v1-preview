from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R8_DIR = BASE / "1013L_R8_original_page_static_readonly_fetch_hook"


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


def extract_hook_payload(html: str) -> dict:
    match = re.search(
        r'<script id="main-shell-static-readonly-fetch-hook-1013L-R8" type="application/json">\s*(.*?)\s*</script>',
        html,
        re.S,
    )
    if not match:
        fail("missing embedded R8 hook JSON payload")
    return json.loads(match.group(1))


def main() -> None:
    result = read_json(R8_DIR / "1013L_R8_result.json")
    contract = read_json(R8_DIR / "static_readonly_fetch_hook_contract_1013L_R8.json")
    resolution = read_json(R8_DIR / "static_hook_state_resolution_fixture_1013L_R8.json")
    html_path = R8_DIR / "prep_room_render_canvas_deepen_v1_1013L_R8_static_readonly_fetch_hook.html"
    if not html_path.exists():
        fail("missing R8 static hook html")
    html = html_path.read_text(encoding="utf-8-sig")
    embedded = extract_hook_payload(html)

    if result.get("final_status") != "PASS_1013L_R8_ORIGINAL_PAGE_STATIC_READONLY_FETCH_HOOK":
        fail("unexpected R8 final status")
    for key in [
        "static_hook_created",
        "original_horizontal_tool_strip_preserved",
        "original_view_switching_preserved",
        "do_not_replace_visible_shell",
    ]:
        assert_true(result, key)
    for key in [
        "new_shell_standard_created",
        "visible_dom_changed",
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
        "ai-tool-strip",
        "toolRail",
        "viewTabs",
        "data-view",
        "coursewareExpanded",
        "chatInput",
        "main-shell-fetch-adapter-1013L-R5",
        "main-shell-original-ui-smoke-1013L-R6",
        "main-shell-static-readonly-fetch-hook-1013L-R8",
        "__SHIWEI_MAIN_SHELL_READONLY_FETCH_HOOK__",
    ]:
        if marker not in html:
            fail(f"R8 html missing marker: {marker}")

    for marker in [
        "stateList",
        "stageBody",
        "agent-bar",
        "师维 · 主壳基线",
    ]:
        if marker in html:
            fail(f"R8 html still contains simplified-shell marker: {marker}")

    if embedded.get("hook_id") != contract.get("hook_id"):
        fail("embedded hook payload does not match contract")
    if contract.get("adapter_map", {}).get("state_count") != 7:
        fail("unexpected adapter map state count")
    if contract.get("state_map", {}).get("mapping_count") != 7:
        fail("unexpected state map mapping count")
    if contract.get("view_to_state", {}).get("weekCalendar") != "week_calendar":
        fail("missing weekCalendar state resolution")
    if contract.get("view_to_state", {}).get("prepNotebook") != "single_lesson_design":
        fail("missing prepNotebook state resolution")
    if contract.get("route_overrides", {}).get("preview_display_query") != "classroom_display_preview":
        fail("missing display preview route override")
    if contract.get("route_overrides", {}).get("coursewareExpanded_hash") != "courseware_workspace":
        fail("missing courseware expanded route override")

    routing = contract.get("agent_routing", {})
    if routing.get("routing_depends_on_display_name") is not False:
        fail("agent routing still depends on display name")
    if routing.get("routing_key_field") != "active_capability":
        fail("agent routing key is not active_capability")

    expected_states = {
        "week_calendar",
        "single_lesson_design",
        "courseware_workspace",
        "classroom_display_preview",
    }
    actual_states = {item.get("expected_state_id") for item in resolution.get("expected_resolutions", [])}
    missing = expected_states - actual_states
    if missing:
        fail(f"resolution fixture missing expected states: {sorted(missing)}")

    for payload in [
        contract.get("boundary", {}),
        resolution.get("boundary", {}),
    ]:
        assert_true(payload, "static_hook_only")
        for key in [
            "visible_dom_changed",
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
            assert_false(payload, key)

    print("PASS: 1013L R8 original page static readonly fetch hook")


if __name__ == "__main__":
    main()
