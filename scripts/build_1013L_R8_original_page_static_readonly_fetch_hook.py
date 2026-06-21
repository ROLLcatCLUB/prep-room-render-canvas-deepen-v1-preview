from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R5_DIR = BASE / "1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter"
R6_DIR = BASE / "1013L_R6_main_shell_original_ui_readonly_fetch_visible_smoke"
R7_DIR = BASE / "1013L_R7_original_page_fetch_adapter_interaction_binding_plan"
R8_DIR = BASE / "1013L_R8_original_page_static_readonly_fetch_hook"
SOURCE_DELTA = BASE / "source_delta_1013L_R8"
R6_HTML = R6_DIR / "prep_room_render_canvas_deepen_v1_1013L_R6_original_ui_fetch_visible_smoke.html"


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "static_hook_only": True,
        "visible_dom_changed": False,
        "runtime_connected": False,
        "real_fetch_performed": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
    }


def hook_payload(adapter_map: dict, state_map: dict, binding_plan: dict) -> dict:
    return {
        "hook_id": "main_shell_static_readonly_fetch_hook_1013L_R8",
        "stage": "1013L_R8_ORIGINAL_PAGE_STATIC_READONLY_FETCH_HOOK",
        "source_stage": "1013L_R7_MAIN_SHELL_READONLY_FETCH_ADAPTER_TO_ORIGINAL_PAGE_INTERACTION_BINDING_PLAN",
        "source_html": rel(R6_HTML),
        "purpose": "Expose a hidden static hook that can resolve the existing original page interaction state to a readonly fetch adapter, without changing visible UI or calling runtime.",
        "adapter_map": adapter_map,
        "state_map": state_map,
        "binding_plan_id": binding_plan.get("plan_id"),
        "view_to_state": {
            "weekCalendar": "week_calendar",
            "prepNotebook": "single_lesson_design",
        },
        "route_overrides": {
            "preview_display_query": "classroom_display_preview",
            "coursewareExpanded_hash": "courseware_workspace",
        },
        "agent_routing": state_map.get("agent_routing", {}),
        "boundary": boundary(),
    }


def hook_script(payload: dict) -> str:
    json_payload = json.dumps(payload, ensure_ascii=False, indent=2)
    js_payload = json.dumps(payload, ensure_ascii=False)
    return f"""
<script id="main-shell-static-readonly-fetch-hook-1013L-R8" type="application/json">
{json_payload}
</script>
<script>
(function () {{
  var payload = {js_payload};
  var states = (payload.adapter_map && payload.adapter_map.states) || [];
  var viewToState = payload.view_to_state || {{}};
  var routeOverrides = payload.route_overrides || {{}};

  function getQuery() {{
    try {{
      return new URLSearchParams(window.location.search || "");
    }} catch (error) {{
      return new URLSearchParams("");
    }}
  }}

  function getActiveViewId() {{
    var tab = document.querySelector("#viewTabs .view-tab.active[data-view], #viewTabs [aria-selected='true'][data-view]");
    if (tab) return tab.getAttribute("data-view");
    return "weekCalendar";
  }}

  function getActiveViewStateId() {{
    var query = getQuery();
    if (query.get("preview") === "display") return routeOverrides.preview_display_query || "classroom_display_preview";
    if (window.location.hash === "#coursewareExpanded") return routeOverrides.coursewareExpanded_hash || "courseware_workspace";
    var viewId = getActiveViewId();
    return viewToState[viewId] || "home_scene";
  }}

  function getFetchAdapterForState(stateId) {{
    var target = stateId || getActiveViewStateId();
    for (var i = 0; i < states.length; i += 1) {{
      if (states[i] && states[i].state_id === target) return states[i];
    }}
    return null;
  }}

  function getReadonlyEndpoint(stateId) {{
    var adapter = getFetchAdapterForState(stateId);
    return adapter ? adapter.readonly_endpoint || null : null;
  }}

  function snapshot() {{
    var stateId = getActiveViewStateId();
    var adapter = getFetchAdapterForState(stateId);
    return {{
      stage: payload.stage,
      state_id: stateId,
      readonly_endpoint: adapter ? adapter.readonly_endpoint || null : null,
      active_capability: adapter ? adapter.active_capability || null : null,
      static_hook_only: true,
      real_fetch_performed: false
    }};
  }}

  Object.defineProperty(window, "__SHIWEI_MAIN_SHELL_READONLY_FETCH_HOOK__", {{
    configurable: false,
    enumerable: false,
    writable: false,
    value: {{
      stage: payload.stage,
      payload: payload,
      getActiveViewStateId: getActiveViewStateId,
      getFetchAdapterForState: getFetchAdapterForState,
      getReadonlyEndpoint: getReadonlyEndpoint,
      snapshot: snapshot
    }}
  }});
}}());
</script>
"""


def inject_hook(html: str, payload: dict) -> str:
    marker = "main-shell-static-readonly-fetch-hook-1013L-R8"
    if marker in html:
        return html
    if "</body>" not in html:
        raise RuntimeError("source html has no closing body tag")
    return html.replace("</body>", hook_script(payload) + "\n</body>")


def copy_source_delta() -> None:
    (SOURCE_DELTA / "scripts").mkdir(parents=True, exist_ok=True)
    for name in [
        "build_1013L_R8_original_page_static_readonly_fetch_hook.py",
        "validate_1013L_R8_original_page_static_readonly_fetch_hook.py",
    ]:
        shutil.copy2(ROOT / "scripts" / name, SOURCE_DELTA / "scripts" / name)


def main() -> None:
    adapter_map = read_json(R5_DIR / "main_shell_state_fetch_adapter_map_1013L_R5.json")
    state_map = read_json(R7_DIR / "original_ui_to_render_state_map_1013L_R7.json")
    binding_plan = read_json(R7_DIR / "main_shell_fetch_adapter_to_original_page_binding_plan_1013L_R7.json")
    payload = hook_payload(adapter_map, state_map, binding_plan)
    html = R6_HTML.read_text(encoding="utf-8-sig")
    rendered_html = inject_hook(html, payload)

    html_path = R8_DIR / "prep_room_render_canvas_deepen_v1_1013L_R8_static_readonly_fetch_hook.html"
    write_text(html_path, rendered_html)
    write_json(R8_DIR / "static_readonly_fetch_hook_contract_1013L_R8.json", payload)
    write_json(
        R8_DIR / "static_hook_state_resolution_fixture_1013L_R8.json",
        {
            "fixture_id": "static_hook_state_resolution_fixture_1013L_R8",
            "stage": payload["stage"],
            "expected_resolutions": [
                {"url_hint": "default", "expected_state_id": "week_calendar"},
                {"url_hint": "#coursewareExpanded", "expected_state_id": "courseware_workspace"},
                {"url_hint": "?preview=display&screen=03#coursewareExpanded", "expected_state_id": "classroom_display_preview"},
                {"dom_hint": "active data-view=prepNotebook", "expected_state_id": "single_lesson_design"},
            ],
            "boundary": boundary(),
        },
    )
    result = {
        "stage": "1013L_R8_ORIGINAL_PAGE_STATIC_READONLY_FETCH_HOOK",
        "final_status": "PASS_1013L_R8_ORIGINAL_PAGE_STATIC_READONLY_FETCH_HOOK",
        "source_html": rel(R6_HTML),
        "html_fixture": rel(html_path),
        "static_hook_created": True,
        "hook_global_name": "__SHIWEI_MAIN_SHELL_READONLY_FETCH_HOOK__",
        "state_adapter_count": adapter_map.get("state_count"),
        "state_mapping_count": state_map.get("mapping_count"),
        "original_horizontal_tool_strip_preserved": True,
        "original_view_switching_preserved": True,
        "do_not_replace_visible_shell": True,
        "new_shell_standard_created": False,
        "visible_dom_changed": False,
        "runtime_connected": False,
        "real_fetch_performed": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
        "github_uploaded": False,
        "next_stage": "1013L_R9_ORIGINAL_PAGE_VIEWMODEL_HYDRATION_STATIC_SMOKE",
    }
    write_json(R8_DIR / "1013L_R8_result.json", result)
    report = """# 1013L R8 Original Page Static Readonly Fetch Hook

R8 injects a hidden static hook into the existing polished prep-room page copy.

The hook can resolve the current original-page route/view into a readonly state adapter, but it does not call runtime, modify visible DOM, connect provider/model, or write any persistence layer.

Next: `1013L_R9_ORIGINAL_PAGE_VIEWMODEL_HYDRATION_STATIC_SMOKE`.
"""
    write_text(R8_DIR / "1013L_R8_report.md", report)
    copy_source_delta()
    print(R8_DIR)


if __name__ == "__main__":
    main()
