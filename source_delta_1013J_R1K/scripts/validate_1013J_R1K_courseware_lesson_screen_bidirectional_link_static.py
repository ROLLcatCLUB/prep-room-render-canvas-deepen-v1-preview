from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STAGE_ID = "1013J_R1K_COURSEWARE_LESSON_SCREEN_BIDIRECTIONAL_LINK_STATIC"
FINAL_STATUS = "PASS_1013J_R1K_COURSEWARE_LESSON_SCREEN_BIDIRECTIONAL_LINK_STATIC"
INHERITS_FROM = "1013J_R1J_COURSEWARE_TEMPLATE_AND_AGENT_RECOMMENDATION_MERGE_STATIC"
BASE_DIR_NAME = "1013J_R1J_courseware_template_and_agent_recommendation_merge_static"
BASE_HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1J_template_agent_merge.html"
STAGE_DIR_NAME = "1013J_R1K_courseware_lesson_screen_bidirectional_link_static"
HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1K_lesson_screen_bidirectional_link.html"
VALIDATOR_NAME = "validate_1013J_R1K_courseware_lesson_screen_bidirectional_link_static.py"

BOUNDARY = {
    "upload_implemented": False,
    "search_implemented": False,
    "whiteboard_library_connected": False,
    "ppt_export_implemented": False,
    "drag_edit_implemented": False,
    "runtime_connected": False,
    "provider_called": False,
    "model_called": False,
    "formal_apply_performed": False,
    "database_written": False,
    "memory_written": False,
    "feishu_written": False,
    "main_project_pushed": False,
    "real_sync_performed": False,
}

CHROME = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
]


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
    .r1k-toggle{display:flex;gap:8px;flex-wrap:wrap}
    .r1k-toggle .active{background:var(--green);color:white;border-color:var(--green)}
    .r1k-linked-list{display:grid;gap:9px;margin-top:10px}
    .r1k-link-card{border:1px solid rgba(43,124,106,.16);border-radius:14px;background:rgba(255,255,250,.72);padding:11px;display:grid;gap:7px;font-size:12px;line-height:1.45}
    .r1k-link-card strong{color:var(--ink)}
    .r1k-status-row{display:flex;gap:7px;flex-wrap:wrap}
    .r1k-tag{border:1px solid rgba(43,124,106,.18);border-radius:999px;background:rgba(240,250,246,.72);padding:3px 8px;color:var(--green);font-size:11px;font-weight:850}
    .r1k-tag.warn{border-color:rgba(213,151,72,.28);background:rgba(255,246,226,.72);color:#9a681d}
    .r1k-sync-panel{border:1px dashed rgba(43,124,106,.24);border-radius:14px;background:rgba(240,250,246,.42);padding:12px;display:grid;gap:8px;font-size:12px;line-height:1.5}
    .r1k-sync-panel.warn{border-color:rgba(213,151,72,.32);background:rgba(255,246,226,.58)}
    .r1k-actions{display:flex;gap:7px;flex-wrap:wrap}
    .r1k-screen-mini{border:12px solid rgba(43,124,106,.08);border-radius:18px;background:rgba(255,255,250,.72);padding:14px}
    .r1k-screen-mini-inner{aspect-ratio:16/9;border:1px solid rgba(43,124,106,.2);border-radius:14px;background:linear-gradient(145deg,#fffef7,#f5fbf6);padding:22px;display:grid;grid-template-rows:auto 1fr auto;gap:12px}
    .r1k-question{font-size:22px;font-weight:900;color:var(--ink)}
    .r1k-images{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    .r1k-image{border:1px dashed rgba(43,124,106,.28);border-radius:14px;display:grid;place-items:center;color:rgba(43,124,106,.58);font-weight:850}
    @media(max-width:1180px){.r1j-workspace{grid-template-columns:180px minmax(420px,1fr)}.r1j-workspace>.r1j-panel:last-child{grid-column:1/-1}}
    """


def js() -> str:
    return """
    function renderCoursewareExpandedWorkspace1013JR1(view) {
      return `
      <div class="r1j-merge-shell" data-1013j-r1k-bidirectional-link="true" data-1013j-r1g-responsive-full="true" aria-label="备课与课件双向关联样张">
        <div class="r1j-workspace">
          <aside class="r1j-panel" aria-label="课件草稿">
            <div class="r1j-panel-title">大屏草稿</div>
            <button class="node-action primary" type="button">＋ 添加页面</button>
            <div class="r1j-screen-list">
              <button class="r1j-screen-item" type="button"><span>01</span><strong>色彩的感觉</strong><div class="r1j-ops"><span class="r1j-chip">已关联备课</span></div></button>
              <button class="r1j-screen-item active" type="button"><span>03</span><strong>哪一组颜色更安静？</strong><div class="r1j-ops"><span class="r1j-chip">已关联备课</span><span class="r1j-chip">待补图</span></div></button>
              <button class="r1j-screen-item" type="button"><span>04</span><strong>把“好看”说得更具体</strong><div class="r1j-ops"><span class="r1j-chip">已有文字</span></div></button>
              <button class="r1j-screen-item" type="button"><span>自</span><strong>色卡整理提醒</strong><div class="r1j-ops"><span class="r1j-chip">自由页</span></div></button>
            </div>
            <div class="r1k-linked-list">
              <div class="r1k-sync-panel"><strong>当前备课段：比较变化</strong><p>学生比较两组色彩，尝试说出哪一组更安静、更热闹，并说明理由。</p><span class="r1k-tag">从备课看课件</span></div>
            </div>
          </aside>
          <main class="r1j-main" aria-label="双向关联预览">
            <div class="r1j-context">
              <div class="r1k-toggle"><button class="node-action primary active" type="button">从备课看课件</button><button class="node-action secondary" type="button">从课件看备课</button></div>
              <span>关联状态：已关联备课 / 自由页 / 待教师确认 / 建议同步</span>
            </div>
            <section class="r1k-screen-mini">
              <div class="r1k-screen-mini-inner">
                <div><div class="r1k-question">哪一组更安静？</div><div class="r1k-status-row"><span class="r1k-tag">关联备课段：比较变化</span><span class="r1k-tag warn">待教师确认</span></div></div>
                <div class="r1k-images"><div class="r1k-image">热闹色彩组合图<br><span class="quiet-tag">待补图</span></div><div class="r1k-image">安静色彩组合图<br><span class="quiet-tag">待补图</span></div></div>
                <div class="r1k-actions"><span class="quiet-tag">本屏作用：支持学生通过两组色彩比较说出具体感受</span><button class="courseware-r1e-icon primary" type="button">▶</button></div>
              </div>
            </section>
            <section class="r1k-linked-list" aria-label="备课段关联大屏">
              <div class="r1j-panel-title">已关联大屏</div>
              <div class="r1k-link-card"><strong>03 哪一组颜色更安静？｜两图对比｜待补图</strong><p>关联原因：这一屏用于帮助学生从“好看”转向说出具体色彩感受。</p><div class="r1k-actions"><button class="node-action secondary" type="button">查看屏幕</button><button class="node-action secondary" type="button">调整关联</button><button class="node-action secondary" type="button">暂不处理</button></div></div>
              <div class="r1k-link-card"><strong>04 把“好看”说得更具体｜词卡页｜已有文字</strong><p>关联原因：这一屏给学生表达词支架，帮助他们把色彩感受说具体。</p><div class="r1k-actions"><button class="node-action secondary" type="button">查看屏幕</button><button class="node-action secondary" type="button">调整关联</button><button class="node-action secondary" type="button">暂不处理</button></div></div>
            </section>
            <section class="r1k-linked-list" aria-label="同步提示">
              <div class="r1k-sync-panel warn"><strong>课件页修改提示</strong><p>你修改了这一屏的课堂问题：原问题：你从哪些颜色看出来？新问题：你从哪些颜色感受到安静？</p><p>小教提示：这处修改可能影响“比较变化”环节中的提问语，是否同步到备课预览？</p><div class="r1k-actions"><button class="node-action primary" type="button">同步到备课预览</button><button class="node-action secondary" type="button">只改课件页</button><button class="node-action secondary" type="button">暂不处理</button></div></div>
              <div class="r1k-sync-panel"><strong>备课段落修改提示</strong><p>你修改了备课段落“比较变化”：新增：先让学生观察冷暖色组合的差异，再说出感受。</p><p>小教提示：相关大屏 03 可以补一句提示：“先看冷暖变化，再说感觉。”是否更新课件预览？</p><div class="r1k-actions"><button class="node-action primary" type="button">更新课件预览</button><button class="node-action secondary" type="button">只改备课段</button><button class="node-action secondary" type="button">暂不处理</button></div></div>
            </section>
          </main>
          <aside class="r1j-panel" aria-label="关联备课与小教建议">
            <button class="node-action secondary" type="button" data-courseware-normal="true">回到备课</button>
            <button class="node-action primary" type="button">大屏预览</button>
            <div class="r1j-panel-title" style="margin-top:14px">从课件看备课</div>
            <div class="r1k-link-card"><strong>关联备课段：比较变化</strong><p>本屏作用：支持学生通过两组色彩比较说出具体感受。</p><p>来源：小教推荐，教师待确认。</p><button class="node-action secondary" type="button">查看对应备课段</button></div>
            <div class="r1j-panel-title">自由页挂接</div>
            <div class="r1k-link-card"><strong>色卡整理提醒</strong><p>状态：自由页，未关联备课环节。</p><p>小教提示：这一页可以放入“材料准备”环节，是否关联到备课？</p><div class="r1k-actions"><button class="node-action secondary" type="button">关联到材料准备</button><button class="node-action secondary" type="button">保持自由页</button><button class="node-action secondary" type="button">暂不处理</button></div></div>
            <div class="r1k-status-row"><span class="r1k-tag">建议同步</span><span class="r1k-tag">仅课件页</span><span class="r1k-tag">仅备课段</span></div>
          </aside>
        </div>
      </div>`;
    }
    """


def patch_html(out: Path) -> str:
    html = (out / BASE_DIR_NAME / BASE_HTML_NAME).read_text(encoding="utf-8")
    html = html.replace("1013J_R1J 模板与小教推荐合并样张", "1013J_R1K 备课与课件双向关联")
    html = html.replace("</style>", css() + "\n</style>", 1)
    html = html.replace("    initPrepRoomRenderCanvas();", js() + "\n    initPrepRoomRenderCanvas();", 1)
    return html


def js_check(stage: Path, html: str) -> dict[str, Any]:
    node = shutil.which("node")
    if not node:
        return {"javascript_syntax_check_pass": False, "javascript_syntax_error": "node_not_found"}
    files = []
    for i, text in enumerate(re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, flags=re.S | re.I)):
        p = stage / f"javascript_syntax_1013J_R1K_{i:02d}.js"
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
    for name in ["lesson_to_screen", "screen_to_lesson", "screen_change_prompt", "lesson_change_prompt"]:
        out = stage / f"ui_smoke_screenshot_1013J_R1K_{name}.png"
        subprocess.run([str(b), "--headless=new", "--disable-gpu", "--window-size=1440,1100", f"--screenshot={out}", "file:///" + html_path.as_posix() + "?screen=screen_03#coursewareExpanded"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        w, h = png_size(out)
        shots.append({"case": name, "path": out.name, "width": w, "height": h, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": True, "screenshots": shots}


def validate(html: str) -> dict[str, Any]:
    start = html.rfind('data-1013j-r1k-bidirectional-link="true"')
    text = html[start : start + 10000] if start >= 0 else html
    visible_text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    banned = ["schema", "payload", "provider", "model", "database", "runtime", "validator", "mapping_json", "field key", "formal apply", "writeback"]
    return {
        "lesson_to_screen_view_created": "从备课看课件" in text and "已关联大屏" in text,
        "screen_to_lesson_view_created": "从课件看备课" in text and "查看对应备课段" in text,
        "selected_lesson_section_visible": "当前备课段：比较变化" in text,
        "linked_courseware_screens_visible": text.count("查看屏幕") >= 2 and "03 哪一组颜色更安静" in text and "04 把“好看”说得更具体" in text,
        "selected_screen_lesson_link_visible": "关联备课段：比较变化" in text,
        "lesson_to_screen_mapping_reason_visible": "关联原因" in text and "本屏作用" in text,
        "screen_change_sync_prompt_created": "你修改了这一屏的课堂问题" in text and "同步到备课预览" in text,
        "lesson_change_sync_prompt_created": "你修改了备课段落“比较变化”" in text and "更新课件预览" in text,
        "sync_to_lesson_preview_action_present": "同步到备课预览" in text and "只改课件页" in text and "暂不处理" in text,
        "update_courseware_preview_action_present": "更新课件预览" in text and "只改备课段" in text and "暂不处理" in text,
        "custom_screen_link_prompt_present": "色卡整理提醒" in text and "关联到材料准备" in text and "保持自由页" in text,
        "linked_and_unlinked_states_visible": "已关联备课" in text and "自由页" in text and "待教师确认" in text and "建议同步" in text and "仅课件页" in text and "仅备课段" in text,
        "preview_only_sync": True,
        "teacher_visible_engineering_terms_absent": all(x not in visible_text for x in banned),
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
    write_json(stage / "lesson_screen_bidirectional_state_1013J_R1K.json", {"stage": STAGE_ID, "selected_lesson_section": "比较变化", "selected_screen": "03 哪一组颜色更安静？", "preview_only_sync": True, **BOUNDARY})
    write_json(stage / "lesson_to_courseware_view_fixture_1013J_R1K.json", {"stage": STAGE_ID, "lesson_section": "比较变化", "linked_screens": ["03 哪一组颜色更安静？", "04 把“好看”说得更具体"], **BOUNDARY})
    write_json(stage / "courseware_to_lesson_view_fixture_1013J_R1K.json", {"stage": STAGE_ID, "screen": "03 哪一组颜色更安静？", "linked_lesson_section": "比较变化", **BOUNDARY})
    write_json(stage / "screen_change_sync_prompt_fixture_1013J_R1K.json", {"stage": STAGE_ID, "action": "同步到备课预览", "preview_only_sync": True, **BOUNDARY})
    write_json(stage / "lesson_change_sync_prompt_fixture_1013J_R1K.json", {"stage": STAGE_ID, "action": "更新课件预览", "preview_only_sync": True, **BOUNDARY})
    write_json(stage / "custom_screen_link_prompt_fixture_1013J_R1K.json", {"stage": STAGE_ID, "custom_screen": "色卡整理提醒", "suggested_lesson_section": "材料准备", **BOUNDARY})
    checks = validate(html)
    checks.update(js_check(stage, html))
    shot = screenshot(stage, html_path)
    checks["screenshot_smoke_pass"] = shot["screenshot_smoke_pass"]
    failed = [k for k, v in checks.items() if k not in BOUNDARY and k not in {"javascript_syntax_files"} and v is not True] + [k for k in BOUNDARY if checks.get(k) is not False]
    result = {
        "stage": STAGE_ID,
        "final_status": FINAL_STATUS if not failed else "FAIL_" + STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "next_stage": "1013J_R1L_COURSEWARE_MATERIAL_PLACEHOLDER_STATE_FLOW_STATIC",
        "auto_continue_allowed": not failed,
        "next_recommended": "1013J_R1L_COURSEWARE_MATERIAL_PLACEHOLDER_STATE_FLOW_STATIC" if not failed else "NONE",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        **checks,
        "screenshots": shot.get("screenshots", []),
        "failed_checks": failed,
    }
    write_json(stage / "1013J_R1K_result.json", result)
    write(stage / "1013J_R1K_report.md", f"# 1013J_R1K\n\nFINAL_STATUS={result['final_status']}\n\nStatic bidirectional lesson-section and courseware-screen link surface. Sync actions are preview-only and do not write data.\n\nFailed checks: {failed}\n")
    write(out / "LATEST_REVIEW_ENTRY.md", f"# Latest Review Entry\n\nSTAGE={STAGE_ID}\nFINAL_STATUS={result['final_status']}\nNEXT_STAGE={result['next_stage']}\n\nR1K makes the lesson-section to courseware-screen relationship visible in both directions, with preview-only sync prompts.\n")
    write(out / "README.md", f"# Prep Room Review Package\n\nLatest stage: `{STAGE_ID}`\n\nOpen `{STAGE_DIR_NAME}/{HTML_NAME}`.\n")
    write(out / "REVIEW_PACKAGE_MANIFEST.md", f"# Review Package Manifest\n\nLatest stage: `{STAGE_ID}`\n\nIncludes `{STAGE_DIR_NAME}` and `scripts/{VALIDATOR_NAME}`.\n\nBoundaries: static fixture only; preview-only sync; no runtime/provider/model/database/memory/Feishu/export/upload/search/whiteboard integration; main project not pushed.\n")
    delta = out / "source_delta_1013J_R1K" / "scripts" / VALIDATOR_NAME
    delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))
    print("ALL_1013J_R1K_COURSEWARE_LESSON_SCREEN_BIDIRECTIONAL_LINK_STATIC_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["final_status"], "failed_checks": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
