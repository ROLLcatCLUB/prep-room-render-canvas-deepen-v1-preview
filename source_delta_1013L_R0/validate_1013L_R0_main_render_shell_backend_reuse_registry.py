from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAGE_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013L_R0_main_render_shell_backend_reuse_registry"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def read_json(path: Path):
    if not path.exists():
        fail(f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> None:
    result = read_json(STAGE_DIR / "1013L_R0_result.json")
    registry = read_json(STAGE_DIR / "render_stage_registry_1013L_R0.json")
    reuse = read_json(STAGE_DIR / "backend_reuse_matrix_1013L_R0.json")
    policy = read_json(STAGE_DIR / "agent_profile_route_normalization_policy_1013L_R0.json")

    if result.get("final_status") != "PASS_1013L_R0_MAIN_RENDER_SHELL_BACKEND_REUSE_REGISTRY":
        fail("unexpected final_status")
    if result.get("backup_verified") is not True:
        fail("backup was not verified")
    if result.get("new_disconnected_page_created") is not False:
        fail("new disconnected page was created")
    if result.get("formal_frontend_binding_allowed") is not False:
        fail("formal frontend binding was allowed")

    expected_states = {
        "home_scene",
        "prep_notebook",
        "big_unit_design",
        "single_lesson_design",
        "courseware_workspace",
        "classroom_display_preview",
        "material_intake",
        "week_calendar",
    }
    state_ids = {item.get("state_id") for item in registry.get("states", [])}
    missing_states = expected_states - state_ids
    if missing_states:
        fail(f"missing render states: {sorted(missing_states)}")
    shell_shape = registry.get("shell_shape", {})
    for key in ["top_shell_persistent", "render_stage_dynamic", "bottom_agent_bar_persistent"]:
        if shell_shape.get(key) is not True:
            fail(f"shell shape missing true flag: {key}")

    if policy.get("canonical_agent_role") != "unified_renameable_agent":
        fail("canonical agent role is not unified_renameable_agent")
    if policy.get("routing_depends_on_display_name") is not False:
        fail("routing still depends on display name")
    if "小教" not in policy.get("legacy_visible_names", []):
        fail("legacy visible name 小教 was not recorded for migration")
    if "小备" not in policy.get("legacy_visible_names", []):
        fail("legacy/default visible name 小备 was not recorded")

    groups = {item.get("group_id") for item in reuse.get("reuse_groups", [])}
    for group_id in [
        "workbench_shell_viewmodel",
        "big_unit_readonly_chunks",
        "curriculum_and_big_unit_derivation",
        "courseware_viewmodel",
        "knowledge_and_official_unit_sources",
    ]:
        if group_id not in groups:
            fail(f"missing backend reuse group: {group_id}")

    routes_py = ROOT / "backend" / "xiaobei_ai" / "routes.py"
    routes_text = routes_py.read_text(encoding="utf-8-sig")
    if "prep_room_render_shell_registry_1013L_R0" not in routes_text:
        fail("render shell registry module not registered in routes.py")

    print("PASS: 1013L R0 main render shell backend reuse registry")


if __name__ == "__main__":
    main()
