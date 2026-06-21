from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R6_DIR = BASE / "1013L_R6_main_shell_original_ui_readonly_fetch_visible_smoke"
R7_DIR = BASE / "1013L_R7_original_page_fetch_adapter_interaction_binding_plan"
SOURCE_DELTA = BASE / "source_delta_1013L_R7"
R6_HTML = R6_DIR / "prep_room_render_canvas_deepen_v1_1013L_R6_original_ui_fetch_visible_smoke.html"


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def html_text() -> str:
    return R6_HTML.read_text(encoding="utf-8-sig")


def inventory(html: str) -> dict:
    data_views = sorted(set(re.findall(r'data-view="([^"]+)"', html)))
    data_tools = sorted(set(re.findall(r'data-tool="([^"]+)"', html)))
    return {
        "inventory_id": "original_page_interaction_inventory_1013L_R7",
        "stage": "1013L_R7_MAIN_SHELL_READONLY_FETCH_ADAPTER_TO_ORIGINAL_PAGE_INTERACTION_BINDING_PLAN",
        "source_html": rel(R6_HTML),
        "markers": {
            "viewTabs": "viewTabs" in html,
            "toolRail": "toolRail" in html,
            "ai_tool_strip": "ai-tool-strip" in html,
            "selectView_function": "function selectView(viewId)" in html,
            "bindEvents_function": "function bindEvents()" in html,
            "chatInput": "chatInput" in html,
            "coursewareExpanded_hash": "coursewareExpanded" in html,
            "display_preview_route": "?preview=display" in html,
            "main_shell_fetch_adapter_metadata": "main-shell-fetch-adapter-1013L-R5" in html,
            "r6_original_ui_smoke_metadata": "main-shell-original-ui-smoke-1013L-R6" in html,
        },
        "data_view_ids": data_views,
        "data_tool_ids": data_tools,
        "data_view_count": len(data_views),
        "data_tool_count": len(data_tools),
        "boundary": boundary(),
    }


def boundary() -> dict[str, bool]:
    return {
        "binding_plan_only": True,
        "visible_dom_changed": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
    }


def state_map() -> dict:
    mappings = [
        {
            "original_trigger": "initial model.active_view=weekCalendar",
            "original_hook": "model.active_view",
            "render_state_id": "week_calendar",
            "readonly_fetch": "/api/prep-room/main-shell/viewmodel/state/week_calendar",
            "binding_action": "hydrate schedule context into existing weekCalendar view without replacing UI",
            "visible_ui_change_allowed": False,
        },
        {
            "original_trigger": "data-view=prepNotebook",
            "original_hook": "selectView('prepNotebook')",
            "render_state_id": "single_lesson_design",
            "readonly_fetch": "/api/prep-room/main-shell/viewmodel/state/single_lesson_design",
            "binding_action": "hydrate current lesson notebook context into existing prepNotebook view",
            "visible_ui_change_allowed": False,
        },
        {
            "original_trigger": "prepNotebook active_big_unit_id or big-unit entry",
            "original_hook": "existing big-unit entry inside prep notebook tree",
            "render_state_id": "big_unit_design",
            "readonly_fetch": "/api/prep-room/main-shell/viewmodel/state/big_unit_design",
            "binding_action": "hydrate big-unit chunks into existing big-unit reading surface",
            "visible_ui_change_allowed": False,
        },
        {
            "original_trigger": "data-courseware-expanded or #coursewareExpanded",
            "original_hook": "courseware_workspace_expanded=true",
            "render_state_id": "courseware_workspace",
            "readonly_fetch": "/api/prep-room/main-shell/viewmodel/state/courseware_workspace",
            "binding_action": "hydrate courseware screen outline into existing expanded courseware workspace",
            "visible_ui_change_allowed": False,
        },
        {
            "original_trigger": "?preview=display",
            "original_hook": "renderDisplayPreview1013JR1M()",
            "render_state_id": "classroom_display_preview",
            "readonly_fetch": "/api/prep-room/main-shell/viewmodel/state/classroom_display_preview",
            "binding_action": "hydrate selected screen data into existing fullscreen display preview",
            "visible_ui_change_allowed": False,
        },
        {
            "original_trigger": "chatUploadBtn / material chips / material status",
            "original_hook": "chatUploadBtn and existing material placeholders",
            "render_state_id": "material_intake",
            "readonly_fetch": "/api/prep-room/main-shell/viewmodel/state/material_intake",
            "binding_action": "show readonly material intake state until real upload gate is opened",
            "visible_ui_change_allowed": False,
        },
        {
            "original_trigger": "bottom Agent composer",
            "original_hook": "chatInput",
            "render_state_id": "home_scene",
            "readonly_fetch": "/api/prep-room/main-shell/viewmodel/state/home_scene",
            "binding_action": "keep resident Agent input as shell-level context entry, not a route key",
            "visible_ui_change_allowed": False,
        },
    ]
    return {
        "map_id": "original_ui_to_render_state_map_1013L_R7",
        "stage": "1013L_R7_MAIN_SHELL_READONLY_FETCH_ADAPTER_TO_ORIGINAL_PAGE_INTERACTION_BINDING_PLAN",
        "mapping_count": len(mappings),
        "mappings": mappings,
        "agent_routing": {
            "canonical_agent_role": "unified_renameable_agent",
            "routing_depends_on_display_name": False,
            "routing_key_field": "active_capability",
        },
        "boundary": boundary(),
    }


def binding_plan(inv: dict, mapping: dict) -> dict:
    return {
        "plan_id": "main_shell_fetch_adapter_to_original_page_interaction_binding_plan_1013L_R7",
        "stage": "1013L_R7_MAIN_SHELL_READONLY_FETCH_ADAPTER_TO_ORIGINAL_PAGE_INTERACTION_BINDING_PLAN",
        "purpose": "Plan how existing original prep-room page interactions will hydrate readonly fetch adapter viewmodels without changing the visible shell.",
        "source_stage": "1013L_R6_MAIN_SHELL_ORIGINAL_UI_READONLY_FETCH_VISIBLE_SMOKE",
        "do_not_replace_visible_shell": True,
        "reuse_original_view_switching": True,
        "reuse_original_horizontal_tool_strip": True,
        "interaction_inventory": inv,
        "state_mapping": mapping,
        "next_allowed_stage": "1013L_R8_ORIGINAL_PAGE_STATIC_READONLY_FETCH_HOOK",
        "boundary": boundary(),
    }


def copy_source_delta() -> None:
    (SOURCE_DELTA / "scripts").mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        ROOT / "scripts" / "build_1013L_R7_original_page_interaction_binding_plan.py",
        SOURCE_DELTA / "scripts" / "build_1013L_R7_original_page_interaction_binding_plan.py",
    )
    shutil.copy2(
        ROOT / "scripts" / "validate_1013L_R7_original_page_interaction_binding_plan.py",
        SOURCE_DELTA / "scripts" / "validate_1013L_R7_original_page_interaction_binding_plan.py",
    )


def main() -> None:
    html = html_text()
    inv = inventory(html)
    mapping = state_map()
    plan = binding_plan(inv, mapping)
    write_json(R7_DIR / "original_page_interaction_inventory_1013L_R7.json", inv)
    write_json(R7_DIR / "original_ui_to_render_state_map_1013L_R7.json", mapping)
    write_json(R7_DIR / "main_shell_fetch_adapter_to_original_page_binding_plan_1013L_R7.json", plan)
    result = {
        "stage": "1013L_R7_MAIN_SHELL_READONLY_FETCH_ADAPTER_TO_ORIGINAL_PAGE_INTERACTION_BINDING_PLAN",
        "final_status": "PASS_1013L_R7_MAIN_SHELL_READONLY_FETCH_ADAPTER_TO_ORIGINAL_PAGE_INTERACTION_BINDING_PLAN",
        "source_html": rel(R6_HTML),
        "interaction_inventory_created": True,
        "state_mapping_created": True,
        "binding_plan_created": True,
        "mapping_count": mapping["mapping_count"],
        "original_horizontal_tool_strip_preserved": True,
        "original_view_switching_preserved": True,
        "do_not_replace_visible_shell": True,
        "new_shell_standard_created": False,
        "visible_dom_changed": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
        "github_uploaded": False,
        "next_stage": "1013L_R8_ORIGINAL_PAGE_STATIC_READONLY_FETCH_HOOK",
    }
    write_json(R7_DIR / "1013L_R7_result.json", result)
    report = """# 1013L R7 Original Page Interaction Binding Plan

R7 maps existing original prep-room interactions to readonly fetch adapter states. It does not change the visible page.

Key decision: keep the prior polished page as the visible shell. Fetch adapter data may hydrate existing views, but must not introduce a new shell standard.

Next: `1013L_R8_ORIGINAL_PAGE_STATIC_READONLY_FETCH_HOOK`.
"""
    write_text(R7_DIR / "1013L_R7_report.md", report)
    copy_source_delta()
    print(R7_DIR)


if __name__ == "__main__":
    main()
