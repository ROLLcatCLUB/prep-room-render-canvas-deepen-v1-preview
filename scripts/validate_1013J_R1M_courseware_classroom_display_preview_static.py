from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STAGE_ID = "1013J_R1M_COURSEWARE_CLASSROOM_DISPLAY_PREVIEW_STATIC"
FINAL_STATUS = "PASS_1013J_R1M_COURSEWARE_CLASSROOM_DISPLAY_PREVIEW_STATIC"
INHERITS_FROM = "1013J_R1L_COURSEWARE_MATERIAL_PLACEHOLDER_STATE_FLOW_STATIC"
BASE_DIR_NAME = "1013J_R1L_courseware_material_placeholder_state_flow_static"
BASE_HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1L_material_placeholder_state_flow.html"
STAGE_DIR_NAME = "1013J_R1M_courseware_classroom_display_preview_static"
HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1M_classroom_display_preview.html"
VALIDATOR_NAME = "validate_1013J_R1M_courseware_classroom_display_preview_static.py"

BOUNDARY = {
    "runtime_connected": False,
    "provider_called": False,
    "model_called": False,
    "formal_apply_performed": False,
    "database_written": False,
    "memory_written": False,
    "feishu_written": False,
    "upload_implemented": False,
    "search_implemented": False,
    "material_library_connected": False,
    "whiteboard_library_connected": False,
    "student_client_connected": False,
    "display_websocket_connected": False,
    "ppt_export_implemented": False,
    "drag_edit_implemented": False,
    "main_project_pushed": False,
}

CHROME = [Path("C:/Program Files/Google/Chrome/Application/chrome.exe"), Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe")]


def locate(root: Path) -> Path:
    out = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    return out if out.exists() else root


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def browser() -> Path | None:
    return next((p for p in CHROME if p.exists()), None)


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def css() -> str:
    return """
    .r1m-entry-note{border:1px solid rgba(43,124,106,.18);border-radius:14px;background:rgba(255,255,250,.76);padding:12px;display:grid;gap:8px;font-size:12px;line-height:1.45}
    .r1m-preview-shell{position:fixed;inset:0;z-index:100;background:radial-gradient(circle at 50% 0%,rgba(235,249,243,.95),#f8fbf7 46%,#e7f3ee 100%);display:grid;grid-template-rows:1fr auto;align-items:center;justify-items:center;padding:24px;color:var(--ink)}
    .r1m-screen-wrap{width:min(92vw,1420px);display:grid;gap:12px;justify-items:center}
    .r1m-screen{width:100%;aspect-ratio:16/9;border:1px solid rgba(43,124,106,.22);border-radius:22px;background:linear-gradient(145deg,#fffef8,#f4fbf5);box-shadow:0 26px 70px rgba(16,61,53,.18);padding:42px;display:grid;grid-template-rows:auto 1fr auto;gap:24px}
    .r1m-screen.ratio-4-3{width:min(76vw,1080px);aspect-ratio:4/3}
    .r1m-kicker{font-size:18px;color:var(--green);font-weight:900}
    .r1m-title{font-size:42px;line-height:1.12;font-weight:950;color:var(--ink);letter-spacing:0}
    .r1m-question{font-size:20px;color:var(--muted);font-weight:760}
    .r1m-images{display:grid;grid-template-columns:1fr 1fr;gap:26px;min-height:0}
    .r1m-image{border:1px dashed rgba(43,124,106,.30);border-radius:20px;background:linear-gradient(135deg,rgba(255,244,226,.82),rgba(232,246,240,.88));display:grid;place-items:center;text-align:center;color:rgba(43,124,106,.82);font-size:28px;font-weight:900}
    .r1m-board{border:1px dashed rgba(43,124,106,.32);border-radius:20px;background:rgba(235,248,243,.9);display:grid;place-items:center;min-height:0;color:rgba(43,124,106,.86);font-size:30px;font-weight:950}
    .r1m-bottom{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
    .r1m-chip{border:1px solid rgba(43,124,106,.18);border-radius:999px;background:rgba(255,255,250,.78);padding:6px 12px;color:var(--green);font-size:13px;font-weight:850}
    .r1m-controls{width:min(92vw,1420px);display:flex;justify-content:center;align-items:center;gap:10px;border:1px solid rgba(43,124,106,.18);border-radius:999px;background:rgba(255,255,250,.76);box-shadow:0 14px 36px rgba(16,61,53,.10);padding:10px 14px}
    .r1m-control{border:1px solid rgba(43,124,106,.2);background:rgba(240,250,246,.8);color:var(--green);border-radius:999px;padding:8px 14px;font-size:13px;font-weight:900;text-decoration:none}
    .r1m-control.primary{background:var(--green);color:white;border-color:var(--green)}
    .r1m-ratio{display:inline-flex;border:1px solid rgba(43,124,106,.20);border-radius:999px;overflow:hidden;background:white}
    .r1m-ratio span{padding:8px 12px;font-size:13px;font-weight:900;color:var(--green)}
    .r1m-ratio .active{background:var(--green);color:white}
    @media(max-width:900px){.r1m-title{font-size:30px}.r1m-question{font-size:16px}.r1m-screen{padding:24px}.r1m-image,.r1m-board{font-size:20px}.r1m-controls{border-radius:24px;flex-wrap:wrap}}
    """


def js() -> str:
    return """
    function renderDisplayPreview1013JR1M() {
      const params = new URLSearchParams(window.location.search || "");
      const selected = params.get("screen") === "06" ? "06" : "03";
      const ratio = params.get("ratio") === "4_3" ? "4_3" : "16_9";
      const isFourThree = ratio === "4_3";
      const screen03 = `
        <div class="r1m-screen ${isFourThree ? "ratio-4-3" : "ratio-16-9"}" data-ratio="${isFourThree ? "4:3" : "16:9"}">
          <div><div class="r1m-kicker">03 · 样例草稿</div><div class="r1m-title">哪一组颜色更安静？</div><div class="r1m-question">你从哪些颜色看出来？</div></div>
          <div class="r1m-images"><div class="r1m-image">热闹的色彩组合</div><div class="r1m-image">安静的色彩组合</div></div>
          <div class="r1m-bottom"><span class="r1m-chip">两图对比</span><span class="r1m-chip">${isFourThree ? "4:3" : "16:9"}</span></div>
        </div>`;
      const screen06 = `
        <div class="r1m-screen ${isFourThree ? "ratio-4-3" : "ratio-16-9"}" data-ratio="${isFourThree ? "4:3" : "16:9"}">
          <div><div class="r1m-kicker">06 · 样例草稿</div><div class="r1m-title">试一组颜色</div><div class="r1m-question">拖一拖色卡，看看画面感觉有什么变化。</div></div>
          <div class="r1m-board">课堂互动区<br><span class="r1m-question">可用于圈画和试色</span></div>
          <div class="r1m-bottom"><span class="r1m-chip">白板试色</span><span class="r1m-chip">${isFourThree ? "4:3" : "16:9"}</span></div>
        </div>`;
      return `<div class="r1m-preview-shell" data-1013j-r1m-display-preview="true" aria-label="大屏预览">
        <main class="r1m-screen-wrap">${selected === "06" ? screen06 : screen03}</main>
        <nav class="r1m-controls" aria-label="大屏预览控制">
          <a class="r1m-control" href="?preview=display&screen=03#coursewareExpanded">上一屏</a>
          <span class="r1m-chip">当前屏 ${selected} / 样例草稿</span>
          <a class="r1m-control" href="?preview=display&screen=06#coursewareExpanded">下一屏</a>
          <span class="r1m-ratio"><span class="${!isFourThree ? "active" : ""}">16:9</span><span class="${isFourThree ? "active" : ""}">4:3</span></span>
          <a class="r1m-control" href="?preview=display&screen=${selected}&ratio=16_9#coursewareExpanded">16:9</a>
          <a class="r1m-control" href="?preview=display&screen=${selected}&ratio=4_3#coursewareExpanded">4:3</a>
          <a class="r1m-control primary" href="?mode=edit#coursewareExpanded">退出预览</a>
        </nav>
      </div>`;
    }
    function renderCoursewareExpandedWorkspace1013JR1(view) {
      const params = new URLSearchParams(window.location.search || "");
      if (params.get("preview") === "display") return renderDisplayPreview1013JR1M();
      return `
      <div class="r1j-merge-shell" data-1013j-r1m-entry="true" data-1013j-r1g-responsive-full="true" aria-label="课件制作区">
        <div class="r1j-workspace">
          <aside class="r1j-panel" aria-label="课件草稿">
            <div class="r1j-panel-title">大屏草稿</div>
            <button class="node-action primary" type="button">＋ 添加页面</button>
            <div class="r1j-screen-list">
              <button class="r1j-screen-item active" type="button"><span>03</span><strong>哪一组颜色更安静？</strong><div class="r1j-ops"><span class="r1j-chip">待补图</span></div></button>
              <button class="r1j-screen-item" type="button"><span>06</span><strong>白板试色</strong><div class="r1j-ops"><span class="r1j-chip">可白板</span></div></button>
            </div>
          </aside>
          <main class="r1j-main" aria-label="制作区入口">
            <section class="r1l-stage">
              <div class="r1m-entry-note"><strong>大屏预览</strong><p>课件制作区用于编辑；大屏预览用于课堂投屏前查看。</p><a class="node-action primary" href="?preview=display&screen=03#coursewareExpanded">进入大屏预览</a></div>
            </section>
          </main>
          <aside class="r1j-panel" aria-label="预览说明">
            <div class="r1j-panel-title">预览控制</div>
            <div class="r1m-entry-note"><p>预览态只显示课堂大屏画面，并保留上一屏、下一屏、退出预览和比例切换。</p></div>
          </aside>
        </div>
      </div>`;
    }
    """


def patch_html(out: Path) -> str:
    html = (out / BASE_DIR_NAME / BASE_HTML_NAME).read_text(encoding="utf-8")
    html = html.replace("1013J_R1L 素材占位状态流转", "1013J_R1M 大屏预览静态样张")
    html = html.replace("</style>", css() + "\n</style>", 1)
    html = html.replace("    initPrepRoomRenderCanvas();", js() + "\n    initPrepRoomRenderCanvas();", 1)
    return html


def js_check(stage: Path, html: str) -> dict[str, Any]:
    node = shutil.which("node")
    if not node:
        return {"javascript_syntax_check_pass": False, "javascript_syntax_error": "node_not_found"}
    files = []
    for i, text in enumerate(re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, flags=re.S | re.I)):
        p = stage / f"javascript_syntax_1013J_R1M_{i:02d}.js"
        write(p, text)
        files.append(p.name)
        proc = subprocess.run([node, "--check", str(p)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode:
            return {"javascript_syntax_check_pass": False, "javascript_syntax_error": proc.stderr or proc.stdout, "javascript_syntax_files": files}
    return {"javascript_syntax_check_pass": True, "javascript_syntax_files": files}


def screenshot(stage: Path, html_path: Path) -> dict[str, Any]:
    b = browser()
    shots = []
    if not b:
        return {"screenshot_smoke_pass": False, "screenshots": shots}
    cases = [
        ("preview_screen_03", "?preview=display&screen=03#coursewareExpanded"),
        ("preview_screen_06", "?preview=display&screen=06#coursewareExpanded"),
        ("preview_ratio_16_9", "?preview=display&screen=03&ratio=16_9#coursewareExpanded"),
        ("preview_ratio_4_3", "?preview=display&screen=03&ratio=4_3#coursewareExpanded"),
    ]
    for name, suffix in cases:
        out = stage / f"ui_smoke_screenshot_1013J_R1M_{name}.png"
        subprocess.run([str(b), "--headless=new", "--disable-gpu", "--window-size=1440,1100", f"--screenshot={out}", "file:///" + html_path.as_posix() + suffix], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        w, h = png_size(out)
        shots.append({"case": name, "path": out.name, "width": w, "height": h, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": True, "screenshots": shots}


def validate(html: str) -> dict[str, Any]:
    preview_start = html.find("function renderDisplayPreview1013JR1M")
    preview_end = html.find("function renderCoursewareExpandedWorkspace1013JR1", preview_start)
    preview_source = html[preview_start:preview_end] if preview_start >= 0 and preview_end > preview_start else html
    start = html.rfind('data-1013j-r1m-display-preview="true"')
    entry_start = html.rfind('data-1013j-r1m-entry="true"')
    text = html[start : start + 9000] if start >= 0 else html
    entry_text = html[entry_start : entry_start + 3000] if entry_start >= 0 else html
    visible = re.sub(r"<!--.*?-->", "", preview_source + entry_text, flags=re.S)
    banned = ["schema", "payload", "provider", "model", "database", "runtime", "validator", "mapping_json", "field key", "formal apply", "writeback", "mock", "websocket", "backend"]
    return {
        "classroom_display_preview_created": "data-1013j-r1m-display-preview" in html,
        "display_preview_entry_present": "进入大屏预览" in entry_text,
        "editing_panels_hidden_in_preview": "r1j-panel" not in preview_source and "模板选择器" not in preview_source and "小教推荐" not in preview_source,
        "main_display_screen_visible": "r1m-screen" in text and "大屏预览" in text,
        "screen_03_preview_created": "03 · 样例草稿" in preview_source and "哪一组颜色更安静？" in preview_source and "热闹的色彩组合" in preview_source,
        "screen_06_preview_created": "06 · 样例草稿" in preview_source and "试一组颜色" in preview_source and "课堂互动区" in preview_source,
        "previous_next_controls_present": "上一屏" in text and "下一屏" in text,
        "exit_preview_action_present": "退出预览" in text,
        "exit_preview_clears_preview_query": "?mode=edit#coursewareExpanded" in preview_source,
        "screen_ratio_16_9_present": "16:9" in text,
        "screen_ratio_4_3_present": "4:3" in text,
        "screen_ratio_visual_difference_present": "ratio-4-3" in preview_source and "aspect-ratio:4/3" in html and "aspect-ratio:16/9" in html,
        "teacher_visible_engineering_terms_absent": all(x not in visible for x in banned),
        **BOUNDARY,
    }


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    root = Path(ap.parse_args().root).resolve()
    out = locate(root)
    stage = out / STAGE_DIR_NAME
    stage.mkdir(parents=True, exist_ok=True)
    html = patch_html(out)
    html_path = stage / HTML_NAME
    write(html_path, html)
    write_json(stage / "classroom_display_preview_state_1013J_R1M.json", {"stage": STAGE_ID, "preview_screen": "03", "ratio": "16:9", **BOUNDARY})
    write_json(stage / "display_preview_navigation_fixture_1013J_R1M.json", {"stage": STAGE_ID, "controls": ["上一屏", "下一屏", "退出预览"], **BOUNDARY})
    write_json(stage / "display_preview_screen_ratio_fixture_1013J_R1M.json", {"stage": STAGE_ID, "ratios": ["16:9", "4:3"], "visual_difference_present": True, **BOUNDARY})
    write_json(stage / "display_preview_exit_fixture_1013J_R1M.json", {"stage": STAGE_ID, "exit_target": "课件制作区", "exit_href": "?mode=edit#coursewareExpanded", "clears_preview_query": True, **BOUNDARY})
    checks = validate(html)
    checks.update(js_check(stage, html))
    shot = screenshot(stage, html_path)
    checks["screenshot_smoke_pass"] = shot["screenshot_smoke_pass"]
    failed = [k for k, v in checks.items() if k not in BOUNDARY and k not in {"javascript_syntax_files"} and v is not True] + [k for k in BOUNDARY if checks.get(k) is not False]
    result = {"stage": STAGE_ID, "final_status": FINAL_STATUS if not failed else "FAIL_" + STAGE_ID, "inherits_from": INHERITS_FROM, "next_stage": "USER_REVIEW_COURSEWARE_VISIBLE_WORKFLOW", "auto_continue_allowed": False, "needs_user_review": True, "next_recommended": "USER_REVIEW_COURSEWARE_VISIBLE_WORKFLOW", "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), **checks, "screenshots": shot.get("screenshots", []), "failed_checks": failed}
    write_json(stage / "1013J_R1M_result.json", result)
    write(stage / "1013J_R1M_report.md", f"# 1013J_R1M\n\nFINAL_STATUS={result['final_status']}\n\nStatic classroom display preview mode. This is the visible workflow queue endpoint and must stop for user review. No runtime, display websocket, student client, whiteboard, upload, search, material library, export, provider/model, or storage integration.\n\nFailed checks: {failed}\n")
    write(out / "LATEST_REVIEW_ENTRY.md", f"# Latest Review Entry\n\nSTAGE={STAGE_ID}\nFINAL_STATUS={result['final_status']}\nNEXT_STAGE={result['next_stage']}\nAUTO_CONTINUE_ALLOWED=false\nNEEDS_USER_REVIEW=true\n\nR1M creates a static classroom display preview mode and closes the current visible workflow queue for user review.\n")
    write(out / "README.md", f"# Prep Room Review Package\n\nLatest stage: `{STAGE_ID}`\n\nProduction/editing surface: `{STAGE_DIR_NAME}/{HTML_NAME}#coursewareExpanded`.\n\nDisplay preview: `{STAGE_DIR_NAME}/{HTML_NAME}?preview=display&screen=03#coursewareExpanded`.\n")
    write(out / "REVIEW_PACKAGE_MANIFEST.md", f"# Review Package Manifest\n\nLatest stage: `{STAGE_ID}`\n\nIncludes `{STAGE_DIR_NAME}` and `scripts/{VALIDATOR_NAME}`.\n\nQueue endpoint: auto-continue is false; user review required. Boundaries: static fixture only; no classroom runtime/student client/display websocket/whiteboard/upload/search/material-library/PPT export/provider/model/database/memory/Feishu integration; main project not pushed.\n")
    delta = out / "source_delta_1013J_R1M" / "scripts" / VALIDATOR_NAME
    delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))
    print("ALL_1013J_R1M_COURSEWARE_CLASSROOM_DISPLAY_PREVIEW_STATIC_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["final_status"], "failed_checks": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
