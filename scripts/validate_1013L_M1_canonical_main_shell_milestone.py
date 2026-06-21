from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
MILESTONE = BASE / "1013L_M1_canonical_main_shell_milestone"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def read_json(path: Path):
    if not path.exists():
        fail(f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> None:
    html_path = MILESTONE / "shiwei_main_render_shell_1013L_M1.html"
    if not html_path.exists():
        fail("missing canonical shell html")
    html = html_path.read_text(encoding="utf-8-sig")
    for required in [
        "render-stage-registry",
        "stateList",
        "stageBody",
        "agent-bar",
        "displayOverlay",
        "小备",
        "RenderStage",
    ]:
        if required not in html:
            fail(f"html missing required marker: {required}")

    result = read_json(MILESTONE / "1013L_M1_result.json")
    registry = read_json(MILESTONE / "canonical_shell_render_stage_registry_1013L_M1.json")
    mount_map = read_json(MILESTONE / "existing_surface_render_stage_mount_map_1013L_M1.json")

    if result.get("final_status") != "PASS_1013L_M1_CANONICAL_MAIN_SHELL_MILESTONE":
        fail("unexpected final status")
    if result.get("screenshot_smoke_pass") is not True:
        fail("screenshot smoke did not pass")
    for screenshot in result.get("visual_smoke_screenshots", []):
        screenshot_path = MILESTONE / screenshot
        if not screenshot_path.exists():
            fail(f"missing screenshot smoke artifact: {screenshot}")
        if screenshot_path.stat().st_size < 1024:
            fail(f"screenshot smoke artifact is too small: {screenshot}")
    for key in [
        "top_shell_persistent",
        "render_stage_dynamic",
        "bottom_agent_bar_persistent",
    ]:
        if result.get(key) is not True:
            fail(f"missing true result flag: {key}")
        if registry.get(key) is not True:
            fail(f"missing true registry flag: {key}")

    expected_states = {
        "home_scene",
        "big_unit_design",
        "single_lesson_design",
        "courseware_workspace",
        "classroom_display_preview",
        "material_intake",
        "week_calendar",
    }
    actual_states = {item.get("state_id") for item in registry.get("states", [])}
    missing = expected_states - actual_states
    if missing:
        fail(f"missing render states: {sorted(missing)}")

    if registry.get("agent_profile", {}).get("canonical_agent_role") != "unified_renameable_agent":
        fail("agent role is not unified renameable")
    if registry.get("agent_profile", {}).get("routing_depends_on_display_name") is not False:
        fail("routing still depends on display name")

    if mount_map.get("new_disconnected_page_created") is not False:
        fail("mount map says a disconnected page was created")
    for item in mount_map.get("mounts", []):
        source_file = item.get("source_file")
        if source_file and not source_file.startswith("/api/") and "existing " not in source_file:
            candidate = ROOT / source_file
            if not candidate.exists():
                fail(f"mount source missing: {source_file}")

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
        "github_uploaded",
    ]:
        if result.get(key) is not False:
            fail(f"boundary flag is not false: {key}")

    print("PASS: 1013L M1 canonical main shell milestone")


if __name__ == "__main__":
    main()
