from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R7_DIR = BASE / "1013L_R7_original_page_fetch_adapter_interaction_binding_plan"


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
    result = read_json(R7_DIR / "1013L_R7_result.json")
    inventory = read_json(R7_DIR / "original_page_interaction_inventory_1013L_R7.json")
    state_map = read_json(R7_DIR / "original_ui_to_render_state_map_1013L_R7.json")
    binding_plan = read_json(R7_DIR / "main_shell_fetch_adapter_to_original_page_binding_plan_1013L_R7.json")

    if result.get("final_status") != "PASS_1013L_R7_MAIN_SHELL_READONLY_FETCH_ADAPTER_TO_ORIGINAL_PAGE_INTERACTION_BINDING_PLAN":
        fail("unexpected R7 final status")
    if result.get("mapping_count") != 7:
        fail("unexpected R7 mapping count")

    for key in [
        "interaction_inventory_created",
        "state_mapping_created",
        "binding_plan_created",
        "original_horizontal_tool_strip_preserved",
        "original_view_switching_preserved",
        "do_not_replace_visible_shell",
    ]:
        assert_true(result, key)

    for key in [
        "new_shell_standard_created",
        "visible_dom_changed",
        "runtime_connected",
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

    markers = inventory.get("markers", {})
    for marker in [
        "viewTabs",
        "toolRail",
        "ai_tool_strip",
        "selectView_function",
        "bindEvents_function",
        "chatInput",
        "coursewareExpanded_hash",
        "display_preview_route",
        "main_shell_fetch_adapter_metadata",
        "r6_original_ui_smoke_metadata",
    ]:
        assert_true(markers, marker)

    expected_states = {
        "week_calendar",
        "single_lesson_design",
        "big_unit_design",
        "courseware_workspace",
        "classroom_display_preview",
        "material_intake",
        "home_scene",
    }
    mappings = state_map.get("mappings", [])
    if len(mappings) != 7:
        fail("state map does not contain 7 mappings")
    actual_states = {item.get("render_state_id") for item in mappings}
    missing = expected_states - actual_states
    if missing:
        fail(f"missing mapped render states: {sorted(missing)}")

    for item in mappings:
        if item.get("visible_ui_change_allowed") is not False:
            fail(f"mapping allows visible UI change: {item.get('render_state_id')}")
        fetch = item.get("readonly_fetch", "")
        if not fetch.startswith("/api/prep-room/main-shell/viewmodel/state/"):
            fail(f"mapping uses unexpected readonly fetch path: {fetch}")

    routing = state_map.get("agent_routing", {})
    if routing.get("canonical_agent_role") != "unified_renameable_agent":
        fail("unexpected canonical agent role")
    if routing.get("routing_depends_on_display_name") is not False:
        fail("agent routing still depends on display name")
    if routing.get("routing_key_field") != "active_capability":
        fail("agent routing key is not active_capability")

    if binding_plan.get("do_not_replace_visible_shell") is not True:
        fail("binding plan does not protect visible shell")
    if binding_plan.get("reuse_original_view_switching") is not True:
        fail("binding plan does not reuse original view switching")
    if binding_plan.get("reuse_original_horizontal_tool_strip") is not True:
        fail("binding plan does not reuse original horizontal tool strip")
    if binding_plan.get("next_allowed_stage") != "1013L_R8_ORIGINAL_PAGE_STATIC_READONLY_FETCH_HOOK":
        fail("unexpected next allowed stage")

    for payload in [
        inventory.get("boundary", {}),
        state_map.get("boundary", {}),
        binding_plan.get("boundary", {}),
    ]:
        assert_true(payload, "binding_plan_only")
        for key in [
            "visible_dom_changed",
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

    print("PASS: 1013L R7 original page interaction binding plan")


if __name__ == "__main__":
    main()
