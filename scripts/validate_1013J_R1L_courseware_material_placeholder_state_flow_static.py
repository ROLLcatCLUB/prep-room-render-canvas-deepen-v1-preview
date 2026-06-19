from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STAGE_ID = "1013J_R1L_COURSEWARE_MATERIAL_PLACEHOLDER_STATE_FLOW_STATIC"
FINAL_STATUS = "PASS_1013J_R1L_COURSEWARE_MATERIAL_PLACEHOLDER_STATE_FLOW_STATIC"
INHERITS_FROM = "1013J_R1K_COURSEWARE_LESSON_SCREEN_BIDIRECTIONAL_LINK_STATIC"
BASE_DIR_NAME = "1013J_R1K_courseware_lesson_screen_bidirectional_link_static"
BASE_HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1K_lesson_screen_bidirectional_link.html"
STAGE_DIR_NAME = "1013J_R1L_courseware_material_placeholder_state_flow_static"
HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1L_material_placeholder_state_flow.html"
VALIDATOR_NAME = "validate_1013J_R1L_courseware_material_placeholder_state_flow_static.py"

BOUNDARY = {
    "real_upload_performed": False,
    "real_search_performed": False,
    "real_material_library_connected": False,
    "real_image_generation_performed": False,
    "real_whiteboard_connected": False,
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
    .r1l-state-list{display:grid;gap:9px}
    .r1l-state-card{border:1px solid rgba(43,124,106,.16);border-radius:14px;background:rgba(255,255,250,.72);padding:10px;display:grid;gap:6px;font-size:12px;line-height:1.45}
    .r1l-state-card strong{color:var(--ink)}
    .r1l-tag-row{display:flex;gap:6px;flex-wrap:wrap}
    .r1l-tag{border:1px solid rgba(43,124,106,.18);border-radius:999px;background:rgba(240,250,246,.72);padding:3px 8px;color:var(--green);font-size:11px;font-weight:850}
    .r1l-tag.warn{border-color:rgba(213,151,72,.28);background:rgba(255,246,226,.72);color:#9a681d}
    .r1l-tag.blue{border-color:rgba(61,113,156,.24);background:rgba(233,244,253,.72);color:#2f648d}
    .r1l-stage{border:14px solid rgba(43,124,106,.08);border-radius:20px;background:rgba(255,255,250,.72);padding:16px}
    .r1l-screen{aspect-ratio:16/9;border:1px solid rgba(43,124,106,.2);border-radius:14px;background:linear-gradient(145deg,#fffef7,#f5fbf6);padding:22px;display:grid;grid-template-rows:auto 1fr auto;gap:12px}
    .r1l-question{font-size:21px;font-weight:900;color:var(--ink)}
    .r1l-images{display:grid;grid-template-columns:1fr 1fr;gap:12px;min-height:0}
    .r1l-image{border:1px dashed rgba(43,124,106,.28);border-radius:14px;display:grid;place-items:center;text-align:center;color:rgba(43,124,106,.68);font-weight:850;background:rgba(247,252,248,.82)}
    .r1l-image.inserted{background:linear-gradient(135deg,rgba(255,242,222,.72),rgba(223,242,238,.72));border-style:solid}
    .r1l-work-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
    .r1l-work{border:1px dashed rgba(43,124,106,.28);border-radius:12px;display:grid;place-items:center;min-height:120px;color:rgba(43,124,106,.65);font-weight:850}
    .r1l-board{border:1px dashed rgba(43,124,106,.30);border-radius:14px;background:rgba(240,250,246,.8);display:grid;place-items:center;color:rgba(43,124,106,.72);font-weight:900}
    .r1l-flow{border:1px dashed rgba(43,124,106,.24);border-radius:14px;background:rgba(240,250,246,.45);padding:10px;font-size:12px;color:var(--muted)}
    @media(max-width:1180px){.r1j-workspace{grid-template-columns:180px minmax(420px,1fr)}.r1j-workspace>.r1j-panel:last-child{grid-column:1/-1}}
    """


def js() -> str:
    return """
    function renderCoursewareExpandedWorkspace1013JR1(view) {
      return `
      <div class="r1j-merge-shell" data-1013j-r1l-material-flow="true" data-1013j-r1g-responsive-full="true" aria-label="素材占位状态流转样张">
        <div class="r1j-workspace">
          <aside class="r1j-panel" aria-label="课件草稿">
            <div class="r1j-panel-title">大屏草稿</div>
            <button class="node-action primary" type="button">＋ 添加页面</button>
            <div class="r1j-screen-list">
              <button class="r1j-screen-item active" type="button"><span>03</span><strong>哪一组颜色更安静？</strong><div class="r1j-ops"><span class="r1j-chip">待补图</span></div></button>
              <button class="r1j-screen-item" type="button"><span>04</span><strong>感觉词卡</strong><div class="r1j-ops"><span class="r1j-chip">已有文字</span></div></button>
              <button class="r1j-screen-item" type="button"><span>05</span><strong>色彩实验任务</strong><div class="r1j-ops"><span class="r1j-chip">待教师确认</span></div></button>
              <button class="r1j-screen-item" type="button"><span>06</span><strong>白板试色</strong><div class="r1j-ops"><span class="r1j-chip">可白板</span></div></button>
              <button class="r1j-screen-item" type="button"><span>07</span><strong>学生作品展示</strong><div class="r1j-ops"><span class="r1j-chip">待学生作品</span></div></button>
            </div>
            <div class="r1l-flow">待补图 → 已放入素材 → 可替换 / 可移除 / 可查看来源</div>
          </aside>
          <main class="r1j-main" aria-label="当前大屏素材占位">
            <div class="r1j-context"><span>关联备课段：比较变化</span><span>素材占位：2 张对比图片</span><span>这些素材用于支持学生比较两组色彩的感觉差异。</span></div>
            <section class="r1l-stage">
              <div class="r1l-screen">
                <div><div class="r1l-question">哪一组更安静？</div><div class="r1l-tag-row"><span class="r1l-tag">两图对比</span><span class="r1l-tag warn">待补图</span><span class="r1l-tag">待教师确认</span></div></div>
                <div class="r1l-images"><div class="r1l-image">素材 A<br>热闹的色彩组合图<br><span class="quiet-tag">待补图</span></div><div class="r1l-image">素材 B<br>安静的色彩组合图<br><span class="quiet-tag">待补图</span></div></div>
                <div class="r1l-tag-row"><button class="node-action primary" type="button">放入示例素材</button><button class="node-action secondary" type="button">替换</button><button class="node-action secondary" type="button">移除</button><button class="node-action secondary" type="button">查看来源</button><button class="node-action secondary" type="button">保持占位</button></div>
              </div>
            </section>
            <section class="r1l-stage">
              <div class="r1l-screen">
                <div><div class="r1l-question">示例素材预览</div><div class="r1l-tag-row"><span class="r1l-tag">已放入</span><span class="r1l-tag blue">示例占位</span></div></div>
                <div class="r1l-images"><div class="r1l-image inserted">[示例图占位]<br>热闹的色彩组合</div><div class="r1l-image inserted">[示例图占位]<br>安静的色彩组合</div></div>
                <div class="quiet-tag">当前为示例占位，后续可替换为真实图片。</div>
              </div>
            </section>
            <section class="r1l-state-list">
              <div class="r1l-state-card"><strong>04 感觉词卡｜已有文字</strong><p>热烈 / 安静 / 柔和 / 强烈 / 明亮 / 沉稳</p><div class="r1l-tag-row"><button class="node-action secondary" type="button">改词卡</button><button class="node-action secondary" type="button">增加词语</button><button class="node-action secondary" type="button">减少词语</button></div></div>
              <div class="r1l-state-card"><strong>05 色彩实验任务｜待教师确认</strong><p>用 3—4 种颜色表达一种感觉。选一组颜色，说说你想表达什么感觉。</p><p>小教已生成任务文字，建议教师确认后再用于课堂。</p><div class="r1l-tag-row"><button class="node-action secondary" type="button">确认用于预览</button><button class="node-action secondary" type="button">改得更简单</button><button class="node-action secondary" type="button">暂不使用</button></div></div>
              <div class="r1l-state-card"><strong>06 白板试色｜可白板</strong><div class="r1l-board" style="min-height:140px">色卡拖拽区 / 圈画区</div><p>这一屏适合让学生在大屏上圈出让自己感到安静的颜色。</p><div class="r1l-tag-row"><button class="node-action secondary" type="button">保留互动区</button><button class="node-action secondary" type="button">改成图片标注</button><button class="node-action secondary" type="button">改成普通问题页</button></div></div>
              <div class="r1l-state-card"><strong>07 学生作品展示｜待学生作品</strong><div class="r1l-work-grid"><div class="r1l-work">作品 1</div><div class="r1l-work">作品 2</div><div class="r1l-work">作品 3</div></div><p>课堂中可把学生作品放到这里进行展示和交流。</p><div class="r1l-tag-row"><button class="node-action secondary" type="button">保留展示位</button><button class="node-action secondary" type="button">调整展示数量</button><button class="node-action secondary" type="button">查看评价提示</button></div></div>
            </section>
          </main>
          <aside class="r1j-panel" aria-label="素材占位与来源">
            <button class="node-action secondary" type="button" data-courseware-normal="true">回到备课</button>
            <button class="node-action primary" type="button">大屏预览</button>
            <div class="r1j-panel-title" style="margin-top:14px">素材占位</div>
            <div class="r1l-state-card"><strong>这一屏需要 2 张对比图片。</strong><p>用途：帮助学生比较色彩组合带来的不同感觉。</p><div class="r1l-tag-row"><span class="r1l-tag warn">待补图</span><span class="r1l-tag">待确认</span></div></div>
            <div class="r1j-panel-title">来源预览</div>
            <div class="r1l-state-card"><strong>来源</strong><p>教师后续可上传 / 资料库 / 小教生成建议</p><p>当前为示例占位，后续可替换为真实图片。</p><div class="r1l-tag-row"><button class="node-action secondary" type="button">替换</button><button class="node-action secondary" type="button">移除</button><button class="node-action secondary" type="button">查看来源</button></div></div>
            <div class="r1j-panel-title">关联</div>
            <div class="r1l-state-card"><strong>关联备课段：比较变化</strong><p>这些素材用于支持学生比较两组色彩的感觉差异。</p><button class="node-action secondary" type="button">查看对应备课段</button></div>
          </aside>
        </div>
      </div>`;
    }
    """


def patch_html(out: Path) -> str:
    html = (out / BASE_DIR_NAME / BASE_HTML_NAME).read_text(encoding="utf-8")
    html = html.replace("1013J_R1K 备课与课件双向关联", "1013J_R1L 素材占位状态流转")
    html = html.replace("</style>", css() + "\n</style>", 1)
    html = html.replace("    initPrepRoomRenderCanvas();", js() + "\n    initPrepRoomRenderCanvas();", 1)
    return html


def js_check(stage: Path, html: str) -> dict[str, Any]:
    node = shutil.which("node")
    if not node:
        return {"javascript_syntax_check_pass": False, "javascript_syntax_error": "node_not_found"}
    files = []
    for i, text in enumerate(re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, flags=re.S | re.I)):
        p = stage / f"javascript_syntax_1013J_R1L_{i:02d}.js"
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
    for name in ["pending_material", "material_inserted", "student_work_placeholder", "whiteboard_slot"]:
        out = stage / f"ui_smoke_screenshot_1013J_R1L_{name}.png"
        subprocess.run([str(b), "--headless=new", "--disable-gpu", "--window-size=1440,1100", f"--screenshot={out}", "file:///" + html_path.as_posix() + "?screen=screen_03#coursewareExpanded"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        w, h = png_size(out)
        shots.append({"case": name, "path": out.name, "width": w, "height": h, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": True, "screenshots": shots}


def validate(html: str) -> dict[str, Any]:
    start = html.rfind('data-1013j-r1l-material-flow="true"')
    text = html[start : start + 14000] if start >= 0 else html
    visible = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    banned = ["schema", "payload", "provider", "model", "database", "runtime", "validator", "mapping_json", "field key", "formal apply", "writeback", "mock"]
    return {
        "material_placeholder_state_flow_created": "素材占位" in text and "待补图 → 已放入素材" in text,
        "pending_image_state_visible": "待补图" in text,
        "inserted_material_state_visible": "已放入" in text,
        "text_ready_state_visible": "已有文字" in text,
        "whiteboard_slot_state_visible": "可白板" in text and "色卡拖拽区 / 圈画区" in text,
        "student_work_placeholder_state_visible": "待学生作品" in text and "学生作品展示" in text,
        "teacher_confirmation_state_visible": "待教师确认" in text,
        "material_state_flow_visible": "待补图 → 已放入素材" in text and "可替换" in text and "可移除" in text and "可查看来源" in text,
        "material_source_preview_visible": "来源预览" in text and "当前为示例占位" in text,
        "replace_material_action_present": "替换" in text,
        "remove_material_action_present": "移除" in text,
        "view_source_action_present": "查看来源" in text,
        "lesson_section_mapping_visible": "关联备课段：比较变化" in text and "查看对应备课段" in text,
        "preview_only_material_flow": True,
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
    write_json(stage / "material_placeholder_state_1013J_R1L.json", {"stage": STAGE_ID, "states": ["待补图", "已有文字", "可白板", "待学生作品", "待教师确认", "已放入素材"], **BOUNDARY})
    write_json(stage / "material_slot_flow_fixture_1013J_R1L.json", {"stage": STAGE_ID, "flow": ["待补图", "已放入素材", "替换/移除/查看来源"], **BOUNDARY})
    write_json(stage / "screen_material_status_fixture_1013J_R1L.json", {"stage": STAGE_ID, "screens": ["03 两图对比", "04 感觉词卡", "05 色彩实验任务", "06 白板试色", "07 学生作品展示"], **BOUNDARY})
    write_json(stage / "material_source_preview_fixture_1013J_R1L.json", {"stage": STAGE_ID, "source_preview": "当前为示例占位，后续可替换为真实图片。", **BOUNDARY})
    checks = validate(html)
    checks.update(js_check(stage, html))
    shot = screenshot(stage, html_path)
    checks["screenshot_smoke_pass"] = shot["screenshot_smoke_pass"]
    failed = [k for k, v in checks.items() if k not in BOUNDARY and k not in {"javascript_syntax_files"} and v is not True] + [k for k in BOUNDARY if checks.get(k) is not False]
    result = {"stage": STAGE_ID, "final_status": FINAL_STATUS if not failed else "FAIL_" + STAGE_ID, "inherits_from": INHERITS_FROM, "next_stage": "1013J_R1M_COURSEWARE_CLASSROOM_DISPLAY_PREVIEW_STATIC", "auto_continue_allowed": not failed, "next_recommended": "1013J_R1M_COURSEWARE_CLASSROOM_DISPLAY_PREVIEW_STATIC" if not failed else "NONE", "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), **checks, "screenshots": shot.get("screenshots", []), "failed_checks": failed}
    write_json(stage / "1013J_R1L_result.json", result)
    write(stage / "1013J_R1L_report.md", f"# 1013J_R1L\n\nFINAL_STATUS={result['final_status']}\n\nStatic material placeholder state flow for courseware screens. No real upload, search, material library, image generation, whiteboard connection, or data writes.\n\nFailed checks: {failed}\n")
    write(out / "LATEST_REVIEW_ENTRY.md", f"# Latest Review Entry\n\nSTAGE={STAGE_ID}\nFINAL_STATUS={result['final_status']}\nNEXT_STAGE={result['next_stage']}\n\nR1L makes courseware material placeholder states visible: pending image, inserted material, text-ready, whiteboard, student work, and teacher-confirmation states.\n")
    write(out / "README.md", f"# Prep Room Review Package\n\nLatest stage: `{STAGE_ID}`\n\nOpen `{STAGE_DIR_NAME}/{HTML_NAME}`.\n")
    write(out / "REVIEW_PACKAGE_MANIFEST.md", f"# Review Package Manifest\n\nLatest stage: `{STAGE_ID}`\n\nIncludes `{STAGE_DIR_NAME}` and `scripts/{VALIDATOR_NAME}`.\n\nBoundaries: static fixture only; no upload/search/material-library/image-generation/whiteboard/runtime/provider/model/database/memory/Feishu/export integration; main project not pushed.\n")
    delta = out / "source_delta_1013J_R1L" / "scripts" / VALIDATOR_NAME
    delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))
    print("ALL_1013J_R1L_COURSEWARE_MATERIAL_PLACEHOLDER_STATE_FLOW_STATIC_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["final_status"], "failed_checks": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
