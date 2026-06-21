from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R8_DIR = BASE / "1013L_R8_original_page_static_readonly_fetch_hook"
R11_DIR = BASE / "1013L_R11_existing_page_readonly_viewmodel_static_hydration_apply"
SOURCE_DELTA = BASE / "source_delta_1013L_R11"
R8_HTML = R8_DIR / "prep_room_render_canvas_deepen_v1_1013L_R8_static_readonly_fetch_hook.html"
COURSEWARE_VIEWMODEL = BASE / "1013K_R29A_courseware_viewmodel_normalization_before_visible_render" / "normalized_courseware_render_viewmodel_1013K_R29A.json"
BIG_UNIT_VIEWMODEL = BASE / "1013K_R8_big_unit_render_viewmodel_readonly_endpoint_contract" / "big_unit_render_viewmodel_readonly_response_fixture_1013K_R8.json"


STAGE = "1013L_R11_EXISTING_PAGE_READONLY_VIEWMODEL_STATIC_HYDRATION_APPLY"
FINAL_STATUS = "PASS_1013L_R11_EXISTING_PAGE_READONLY_VIEWMODEL_STATIC_HYDRATION_APPLY"
NEXT_STAGE = "1013L_R12_EXISTING_PAGE_HYDRATED_VIEWMODEL_VISUAL_SMOKE"


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


def find_browser() -> Path:
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No Edge/Chrome browser found for R11 hydration smoke.")


def boundary() -> dict[str, bool]:
    return {
        "static_hydration_apply_only": True,
        "existing_page_reused": True,
        "new_visible_page_created": False,
        "new_shell_standard_created": False,
        "runtime_connected": False,
        "real_fetch_performed": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
        "formal_frontend_binding_allowed": False,
    }


def status_for_screen(screen: dict) -> str:
    screen_type = screen.get("screen_type", "")
    statuses = [slot.get("status", "") for slot in screen.get("display_body", {}).get("material_slots", [])]
    if "student_work" in screen_type:
        return "待学生作品"
    if "whiteboard" in screen_type or any(status == "placeholder_ready" for status in statuses):
        return "可白板"
    if any(status == "pending_material" for status in statuses):
        return "待补图"
    if any(status == "ready_as_text" for status in statuses) or not statuses:
        return "已有文字"
    return "待教师确认"


def placeholder_for_screen(screen: dict) -> str:
    slots = screen.get("display_body", {}).get("material_slots", [])
    labels = [slot.get("slot_label", "") for slot in slots if slot.get("slot_label")]
    if labels:
        return " / ".join(labels)
    return screen.get("screen_type", "课堂画面")


def compact_courseware_screens(viewmodel: dict) -> list[dict]:
    screens = []
    for screen in viewmodel.get("render_screens", []):
        order = int(screen.get("screen_order") or len(screens) + 1)
        bridge = screen.get("lesson_bridge") or {}
        display = screen.get("display_body") or {}
        screens.append(
            {
                "id": screen.get("screen_id"),
                "index": f"{order:02d}",
                "title": screen.get("title") or f"第 {order} 屏",
                "screen_title": display.get("prompt") or screen.get("title") or "",
                "classroom_text": screen.get("teacher_note") or screen.get("teaching_intent") or "",
                "lesson_link": bridge.get("lesson_section_ref") or "课堂环节",
                "placeholder": placeholder_for_screen(screen),
                "status": status_for_screen(screen),
                "tool": screen.get("screen_type") or "screen",
                "source_screen_id": screen.get("screen_id"),
                "source_chunk_ref": screen.get("source_chunk_ref") or screen.get("source_chunk_refs") or [],
                "preview_only": screen.get("preview_only") is True,
                "display_body": display,
                "teacher_note": screen.get("teacher_note") or "",
                "teaching_intent": screen.get("teaching_intent") or "",
            }
        )
    return screens


def hydration_payload() -> dict:
    courseware = read_json(COURSEWARE_VIEWMODEL)
    big_unit = read_json(BIG_UNIT_VIEWMODEL)
    compact = compact_courseware_screens(courseware)
    pending_screens = [screen for screen in compact if "待补" in screen.get("status", "")]
    whiteboard_screens = [screen for screen in compact if "白板" in screen.get("status", "") or "whiteboard" in screen.get("tool", "")]
    return {
        "hydration_id": "existing_page_readonly_viewmodel_static_hydration_1013L_R11",
        "stage": STAGE,
        "source_html": rel(R8_HTML),
        "courseware_source": rel(COURSEWARE_VIEWMODEL),
        "big_unit_source": rel(BIG_UNIT_VIEWMODEL),
        "courseware": courseware,
        "big_unit": big_unit,
        "compact_courseware_screens": compact,
        "summary": {
            "screen_count": len(compact),
            "pending_material_screen_count": len(pending_screens),
            "whiteboard_screen_count": len(whiteboard_screens),
            "selected_screen_index": "03",
        },
        "hydration_policy": {
            "reuse_existing_page_functions": True,
            "replace_courseware_screen_array_only": True,
            "display_preview_uses_same_viewmodel": True,
            "big_unit_viewmodel_embedded_for_later_route": True,
            "no_new_shell": True,
        },
        "boundary": boundary(),
    }


def hydration_script(payload: dict) -> str:
    json_payload = json.dumps(payload, ensure_ascii=False, indent=2)
    js_payload = json.dumps(payload, ensure_ascii=False)
    return f"""
<style id="main-shell-visible-hydration-style-1013L-R11">
  [data-1013l-r11-display="true"] .r1m-title {{
    font-size: clamp(22px, 2.2vw, 40px);
    line-height: 1.15;
    max-width: 980px;
  }}
  [data-1013l-r11-display="true"] .r1m-question {{
    font-size: clamp(13px, 1.15vw, 20px);
    line-height: 1.4;
  }}
  [data-1013l-r11-display="true"] .r1m-kicker {{
    font-size: clamp(13px, 1vw, 18px);
  }}
  [data-1013l-r11-display="true"] .r1m-images {{
    align-items: stretch;
  }}
  [data-1013l-r11-display="true"] .r1m-image {{
    font-size: clamp(20px, 2.4vw, 42px);
    line-height: 1.18;
  }}
  [data-1013l-r11-display="true"] .r1m-image .r1m-question {{
    display: inline-block;
    margin-top: 22px;
    font-size: clamp(12px, .95vw, 17px);
  }}
</style>
<script id="main-shell-visible-hydration-payload-1013L-R11" type="application/json">
{json_payload}
</script>
<script id="main-shell-visible-hydration-1013L-R11">
(function () {{
  var payload = {js_payload};
  var screens = payload.compact_courseware_screens || [];

  function escapeHtml(value) {{
    if (typeof window.html === "function") return window.html(value == null ? "" : String(value));
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }}

  function selectedScreen() {{
    var query = new URLSearchParams(window.location.search || "");
    var selected = query.get("screen") || payload.summary.selected_screen_index || "03";
    return screens.find(function (screen) {{ return screen.index === selected; }}) || screens[2] || screens[0] || {{}};
  }}

  function materialSlots(screen) {{
    var slots = ((screen.display_body || {{}}).material_slots || []);
    if (!slots.length && screen.placeholder) {{
      slots = [{{ slot_label: screen.placeholder, status: screen.status || "placeholder" }}];
    }}
    return slots;
  }}

  function renderMaterialBlocks(screen) {{
    var slots = materialSlots(screen).slice(0, 4);
    if (!slots.length) {{
      return '<div class="r1m-image">画面占位</div>';
    }}
    return slots.map(function (slot) {{
      return '<div class="r1m-image" data-r11-material-slot="' + escapeHtml(slot.slot_id || slot.slot_label || "slot") + '">' +
        escapeHtml(slot.slot_label || "素材占位") +
        '<br><span class="r1m-question">' + escapeHtml(slot.status || screen.status || "待补") + '</span>' +
      '</div>';
    }}).join("");
  }}

  function renderHydratedDisplayPreview() {{
    var query = new URLSearchParams(window.location.search || "");
    var ratio = query.get("ratio") === "4_3" ? "4_3" : "16_9";
    var isFourThree = ratio === "4_3";
    var screen = selectedScreen();
    return '<div class="r1m-preview-shell" data-1013j-r1m-display-preview="true" data-1013l-r11-display="true" aria-label="大屏预览">' +
      '<main class="r1m-screen-wrap">' +
        '<div class="r1m-screen ' + (isFourThree ? "ratio-4-3" : "ratio-16-9") + '" data-ratio="' + (isFourThree ? "4:3" : "16:9") + '" data-r11-screen-id="' + escapeHtml(screen.source_screen_id || screen.id || "") + '">' +
          '<div><div class="r1m-kicker">' + escapeHtml(screen.index || "03") + ' · 小备草稿</div>' +
          '<div class="r1m-title">' + escapeHtml(screen.screen_title || screen.title || "") + '</div>' +
          '<div class="r1m-question">' + escapeHtml(screen.classroom_text || "") + '</div></div>' +
          '<div class="r1m-images">' + renderMaterialBlocks(screen) + '</div>' +
          '<div class="r1m-bottom"><span class="r1m-chip">' + escapeHtml(screen.title || "") + '</span><span class="r1m-chip">' + (isFourThree ? "4:3" : "16:9") + '</span></div>' +
        '</div>' +
      '</main>' +
      '<nav class="r1m-controls" aria-label="大屏预览控制">' +
        '<a class="r1m-control" href="?preview=display&screen=03#coursewareExpanded">上一屏</a>' +
        '<span class="r1m-chip">当前屏 ' + escapeHtml(screen.index || "03") + ' / 小备草稿</span>' +
        '<a class="r1m-control" href="?preview=display&screen=06#coursewareExpanded">下一屏</a>' +
        '<span class="r1m-ratio">' +
          '<a class="' + (!isFourThree ? "active" : "") + '" href="?preview=display&screen=' + escapeHtml(screen.index || "03") + '&ratio=16_9#coursewareExpanded">16:9</a>' +
          '<a class="' + (isFourThree ? "active" : "") + '" href="?preview=display&screen=' + escapeHtml(screen.index || "03") + '&ratio=4_3#coursewareExpanded">4:3</a>' +
        '</span>' +
        '<a class="r1m-control primary" href="?mode=edit#coursewareExpanded">退出预览</a>' +
      '</nav>' +
    '</div>';
  }}

  function applyCoursewareHydration() {{
    if (!screens.length) return false;
    window.coursewareScreens1013JR1 = screens;
    if (typeof coursewareScreens1013JR1 !== "undefined") {{
      coursewareScreens1013JR1 = screens;
    }}
    window.__SHIWEI_R11_HYDRATED_VIEWMODEL__ = payload;
    document.documentElement.setAttribute("data-1013l-r11-hydrated", "true");
    document.documentElement.setAttribute("data-1013l-r11-courseware-screens", String(screens.length));

    if (typeof renderDisplayPreview1013JR1M === "function") {{
      renderDisplayPreview1013JR1M = renderHydratedDisplayPreview;
    }}

    var query = new URLSearchParams(window.location.search || "");
    if (query.get("preview") === "display") {{
      document.body.innerHTML = renderHydratedDisplayPreview();
      document.documentElement.setAttribute("data-1013l-r11-state", "classroom_display_preview");
      return true;
    }}

    if (typeof renderPrepRoomCanvas === "function") {{
      renderPrepRoomCanvas({{ animate: false }});
      document.documentElement.setAttribute("data-1013l-r11-state", "existing_page_visible_hydration");
      return true;
    }}
    return true;
  }}

  if (document.readyState === "loading") {{
    document.addEventListener("DOMContentLoaded", function () {{ window.setTimeout(applyCoursewareHydration, 0); }});
  }} else {{
    window.setTimeout(applyCoursewareHydration, 0);
  }}
}}());
</script>
"""


def inject_hydration(html_text: str, payload: dict) -> str:
    marker = "main-shell-visible-hydration-1013L-R11"
    if marker in html_text:
        return html_text
    if "</body>" not in html_text:
        raise RuntimeError("source html has no closing body tag")
    return html_text.replace("</body>", hydration_script(payload) + "\n</body>")


def dump_dom(browser: Path, url: str) -> str:
    with tempfile.TemporaryDirectory(prefix="shiwei-r11-browser-") as temp_dir:
        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--disable-background-networking",
            "--allow-file-access-from-files",
            "--virtual-time-budget=5000",
            f"--user-data-dir={temp_dir}",
            "--dump-dom",
            url,
        ]
        completed = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60,
        )
        return completed.stdout


def run_smoke(browser: Path, html_path: Path) -> dict:
    base_url = html_path.resolve().as_uri()
    cases = [
        {
            "case_id": "normal_prep_page_courseware_rail",
            "suffix": "?r11test=normal",
            "required_markers": [
                'data-1013l-r11-hydrated="true"',
                "courseware_screen_seed_03_color_comparison_1013K_R25",
                "哪一组颜色更安静",
            ],
        },
        {
            "case_id": "courseware_expanded_workspace",
            "suffix": "?r11test=courseware#coursewareExpanded",
            "required_markers": [
                'data-1013l-r11-hydrated="true"',
                "courseware_screen_seed_03_color_comparison_1013K_R25",
                "比较两组颜色",
            ],
        },
        {
            "case_id": "display_preview_overlay",
            "suffix": "?preview=display&screen=03#coursewareExpanded",
            "required_markers": [
                'data-1013l-r11-display="true"',
                "courseware_screen_seed_03_color_comparison_1013K_R25",
                "哪一组颜色更安静",
            ],
        },
    ]
    results = []
    for case in cases:
        dom = dump_dom(browser, base_url + case["suffix"])
        missing = [marker for marker in case["required_markers"] if marker not in dom]
        results.append(
            {
                "case_id": case["case_id"],
                "expected_markers": case["required_markers"],
                "missing_markers": missing,
                "pass": missing == [],
            }
        )
    return {
        "smoke_id": "visible_hydration_browser_smoke_1013L_R11",
        "stage": STAGE,
        "case_count": len(results),
        "cases": results,
        "visible_hydration_smoke_pass": all(case["pass"] for case in results),
        "boundary": boundary(),
    }


def copy_source_delta() -> None:
    (SOURCE_DELTA / "scripts").mkdir(parents=True, exist_ok=True)
    for name in [
        "build_1013L_R11_existing_page_readonly_viewmodel_static_hydration_apply.py",
        "validate_1013L_R11_existing_page_readonly_viewmodel_static_hydration_apply.py",
    ]:
        shutil.copy2(ROOT / "scripts" / name, SOURCE_DELTA / "scripts" / name)


def main() -> None:
    payload = hydration_payload()
    source_html = R8_HTML.read_text(encoding="utf-8-sig")
    html_path = R11_DIR / "prep_room_render_canvas_deepen_v1_1013L_R11_static_hydration_apply.html"
    write_text(html_path, inject_hydration(source_html, payload))
    write_json(R11_DIR / "readonly_viewmodel_static_hydration_payload_1013L_R11.json", payload)
    browser = find_browser()
    smoke = run_smoke(browser, html_path)
    write_json(R11_DIR / "visible_hydration_browser_smoke_1013L_R11.json", smoke)
    result = {
        "stage": STAGE,
        "final_status": FINAL_STATUS if smoke["visible_hydration_smoke_pass"] else f"FAIL_{STAGE}",
        "source_stage": "1013L_R10_EXISTING_PAGE_READONLY_VIEWMODEL_BINDING_MILESTONE_PACKAGE",
        "source_html": rel(R8_HTML),
        "hydrated_html": rel(html_path),
        "courseware_source": rel(COURSEWARE_VIEWMODEL),
        "big_unit_source": rel(BIG_UNIT_VIEWMODEL),
        "courseware_viewmodel_embedded": True,
        "big_unit_viewmodel_embedded": True,
        "courseware_screen_array_hydrated": True,
        "courseware_screen_count": payload["summary"]["screen_count"],
        "display_preview_uses_same_viewmodel": True,
        "visible_hydration_smoke_pass": smoke["visible_hydration_smoke_pass"],
        "smoke_case_count": smoke["case_count"],
        "existing_page_reused": True,
        "new_visible_page_created": False,
        "new_shell_standard_created": False,
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
        "next_stage": NEXT_STAGE,
        "boundary": boundary(),
    }
    write_json(R11_DIR / "1013L_R11_result.json", result)
    report = """# 1013L R11 Existing Page Readonly ViewModel Static Hydration Apply

R11 keeps the existing 1013J/R8 page shell and hydrates it with readonly viewmodel data.

It converts the existing courseware viewmodel into the prior `coursewareScreens1013JR1` page shape, so the old right rail, courseware workspace, and display preview continue using existing page functions instead of a new page.

The big-unit viewmodel is embedded for the next visible route step but does not force a new reading page in R11.

Boundary remains static-only: no runtime fetch, no provider/model, no database/memory/Feishu write, no formal apply, and no main project push.
"""
    write_text(R11_DIR / "1013L_R11_report.md", report)
    copy_source_delta()
    print(R11_DIR)


if __name__ == "__main__":
    main()
