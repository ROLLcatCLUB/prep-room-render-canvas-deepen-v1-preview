from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STAGE_ID = "1013J_R1J_COURSEWARE_TEMPLATE_AND_AGENT_RECOMMENDATION_MERGE_STATIC"
FINAL_STATUS = "PASS_1013J_R1J_COURSEWARE_TEMPLATE_AND_AGENT_RECOMMENDATION_MERGE_STATIC"
INHERITS_FROM = [
    "1013J_R1H_COURSEWARE_TEMPLATE_PICKER_AND_SCREEN_OPERATIONS_STATIC",
    "1013J_R1I_LESSON_SECTION_TO_COURSEWARE_AGENT_RECOMMENDATION_STATIC",
]
BASE_DIR_NAME = "1013J_R1G_R2_courseware_route_isolation_patch"
BASE_HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1G_R2_courseware_route_isolated.html"
STAGE_DIR_NAME = "1013J_R1J_courseware_template_and_agent_recommendation_merge_static"
HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1J_courseware_template_agent_merge.html"
VALIDATOR_NAME = "validate_1013J_R1J_courseware_template_and_agent_recommendation_merge_static.py"

BOUNDARY = {
    "runtime_connected": False,
    "provider_called": False,
    "model_called": False,
    "formal_apply_performed": False,
    "database_written": False,
    "memory_written": False,
    "feishu_written": False,
    "main_project_pushed": False,
    "upload_implemented": False,
    "search_implemented": False,
    "whiteboard_library_connected": False,
    "ppt_export_implemented": False,
    "drag_edit_implemented": False,
}

TEMPLATES = ["封面页", "一图观察", "两图对比", "三图比较", "图片 + 问题", "图片 + 标注", "词卡页", "任务发布", "白板互动", "学生作品墙", "评价提示", "自定义空白页"]
RECOMMENDATIONS = [
    {"template": "两图对比", "title": "哪一组颜色更安静？", "section": "比较变化", "slots": "热闹色彩组合图 / 安静色彩组合图", "reason": "这一段适合用两组图片帮助学生比较色彩感受。"},
    {"template": "词卡页", "title": "把“好看”说得更具体", "section": "比较变化", "slots": "感觉词卡", "reason": "学生需要表达支架，把直观感受说具体。"},
]
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
    .r1j-merge-shell{position:relative;min-height:calc(100vh - 150px);padding:24px;background:linear-gradient(135deg,rgba(245,251,246,.92),rgba(232,246,238,.72));border:1px solid rgba(43,124,106,.18);border-radius:18px}
    .r1j-workspace{display:grid;grid-template-columns:220px minmax(560px,1fr) 260px;gap:16px;min-height:760px}
    .r1j-panel{border:1px solid rgba(43,124,106,.18);border-radius:16px;background:rgba(255,255,250,.74);padding:14px;box-shadow:0 14px 34px rgba(16,61,53,.08)}
    .r1j-panel-title{font-weight:900;color:var(--green);font-size:14px;margin-bottom:10px}
    .r1j-screen-list{display:grid;gap:9px}
    .r1j-screen-item{border:1px solid rgba(43,124,106,.18);border-radius:13px;background:rgba(231,246,241,.8);padding:9px 10px;display:grid;grid-template-columns:28px 1fr;gap:8px;align-items:center;font-size:12px;font-weight:850;color:var(--green);text-align:left}
    .r1j-screen-item.active{background:var(--green);color:white;border-color:var(--green)}
    .r1j-ops{display:flex;flex-wrap:wrap;gap:5px;grid-column:2}
    .r1j-chip{border:1px solid rgba(43,124,106,.18);border-radius:999px;padding:3px 7px;background:rgba(255,255,255,.7);font-size:11px;color:var(--green);font-weight:800}
    .r1j-template-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:10px}
    .r1j-template{border:1px solid rgba(43,124,106,.16);border-radius:12px;background:rgba(240,250,246,.62);padding:8px;font-size:12px;color:var(--ink);font-weight:850}
    .r1j-main{display:grid;gap:12px;align-content:start}
    .r1j-context{display:flex;justify-content:space-between;gap:10px;border-bottom:1px dashed rgba(43,124,106,.20);padding-bottom:8px;font-size:12px;color:var(--muted)}
    .r1j-stage{border:14px solid rgba(43,124,106,.08);border-radius:20px;background:rgba(255,255,250,.72);padding:16px}
    .r1j-screen{aspect-ratio:16/9;border:1px solid rgba(43,124,106,.20);border-radius:14px;background:linear-gradient(145deg,#fffef7,#f5fbf6);padding:24px;display:grid;grid-template-rows:auto 1fr auto;gap:14px}
    .r1j-question{font-size:22px;line-height:1.15;font-weight:900;color:var(--ink)}
    .r1j-images{display:grid;grid-template-columns:1fr 1fr;gap:14px;min-height:0}
    .r1j-image{border:1px dashed rgba(43,124,106,.28);border-radius:14px;display:grid;place-items:center;color:rgba(43,124,106,.55);font-weight:850}
    .r1j-recs{display:grid;gap:9px}
    .r1j-rec{border:1px solid rgba(43,124,106,.15);border-radius:14px;background:rgba(255,255,250,.72);padding:10px;font-size:12px;line-height:1.45}
    .r1j-rec strong{display:block;margin-bottom:4px;color:var(--ink)}
    .r1j-actions{display:flex;flex-wrap:wrap;gap:7px;margin-top:8px}
    @media(max-width:1180px){.r1j-workspace{grid-template-columns:170px minmax(420px,1fr);}.r1j-workspace>.r1j-panel:last-child{grid-column:1/-1}.r1j-template-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
    """


def js() -> str:
    templates = json.dumps(TEMPLATES, ensure_ascii=False)
    recs = json.dumps(RECOMMENDATIONS, ensure_ascii=False)
    return f"""
    const r1jTemplates = {templates};
    const r1jRecommendations = {recs};
    function renderCoursewareExpandedWorkspace1013JR1(view) {{
      return `
      <div class="r1j-merge-shell" data-1013j-r1j-merge="true" data-1013j-r1g-responsive-full="true" aria-label="课件制作合并样张">
        <div class="r1j-workspace">
          <aside class="r1j-panel" aria-label="大屏草稿">
            <div class="r1j-panel-title">大屏草稿</div>
            <button class="node-action primary" type="button">＋ 添加页面</button>
            <div class="r1j-screen-list">
              <button class="r1j-screen-item" type="button"><span>01</span><strong>色彩的感觉</strong><div class="r1j-ops"><span class="r1j-chip">复制</span><span class="r1j-chip">下移</span></div></button>
              <button class="r1j-screen-item active" type="button"><span>03</span><strong>哪一组颜色更安静？</strong><div class="r1j-ops"><span class="r1j-chip">删除</span><span class="r1j-chip">复制</span><span class="r1j-chip">上移</span><span class="r1j-chip">下移</span></div></button>
              <button class="r1j-screen-item" type="button"><span>＋</span><strong>新增：两图对比</strong><div class="r1j-ops"><span class="r1j-chip">关联备课环节</span><span class="r1j-chip">设为自由页</span></div></button>
              <button class="r1j-screen-item" type="button"><span>自</span><strong>自定义页面</strong><div class="r1j-ops"><span class="r1j-chip">自由页</span><span class="r1j-chip">删除</span></div></button>
            </div>
            <div class="r1j-panel-title" style="margin-top:14px">选择模板</div>
            <div class="r1j-template-grid">${{r1jTemplates.map(t=>`<button class="r1j-template" type="button">${{html(t)}}</button>`).join("")}}</div>
          </aside>
          <main class="r1j-main" aria-label="当前大屏与小教推荐">
            <div class="r1j-context"><span>当前备课段：比较变化</span><span>对应课件屏：03 比较两组颜色</span><span>本屏作用：帮助学生从“好看”说到“为什么安静”</span></div>
            <section class="r1j-stage"><div class="r1j-screen"><div><div class="r1j-question">哪一组更安静？</div><div class="r1j-actions"><span class="r1j-chip">两图对比</span><span class="r1j-chip">关联：比较变化</span><span class="r1j-chip">待教师确认</span></div></div><div class="r1j-images"><div class="r1j-image">热闹色彩组合图<br><span class="quiet-tag">待补图</span></div><div class="r1j-image">安静色彩组合图<br><span class="quiet-tag">待补图</span></div></div><div class="r1j-actions"><span class="quiet-tag">课堂问题：你从哪些颜色看出来？</span><button class="courseware-r1e-icon primary" type="button">▶</button><button class="courseware-r1e-icon" type="button">图</button><span class="courseware-r1e-segment"><button class="active" type="button">16:9</button><button type="button">4:3</button></span></div></div></section>
            <section class="r1j-recs" aria-label="小教推荐">${{r1jRecommendations.map(r=>`<div class="r1j-rec"><strong>${{html(r.template)}}｜${{html(r.title)}}</strong><p>对应备课段：${{html(r.section)}}；素材占位：${{html(r.slots)}}</p><p>推荐理由：${{html(r.reason)}}</p><div class="r1j-actions"><button class="node-action primary" type="button">采纳为课件页</button><button class="node-action secondary" type="button">换模板</button><button class="node-action secondary" type="button">暂不生成</button></div></div>`).join("")}}</section>
          </main>
          <aside class="r1j-panel" aria-label="映射与补充">
            <button class="node-action secondary" type="button" data-courseware-normal="true">回到备课</button>
            <button class="node-action primary" type="button">大屏预览</button>
            <div class="r1j-panel-title" style="margin-top:14px">小教建议</div>
            <div class="r1j-rec"><strong>备课段映射</strong><p>比较变化 → 两图对比 / 词卡页</p></div>
            <div class="r1j-rec"><strong>自由页反向关联</strong><p>“色卡整理提醒”可关联到“材料准备”，也可保持自由页。</p><div class="r1j-actions"><button class="node-action secondary" type="button">关联到材料准备</button><button class="node-action secondary" type="button">保持自由页</button></div></div>
            <div class="r1j-rec"><strong>屏幕数量</strong><p>大屏页数随课堂需要增减，不固定为 8 屏。</p></div>
          </aside>
        </div>
      </div>`;
    }}
    """


def patch_html(out: Path) -> str:
    html = (out / BASE_DIR_NAME / BASE_HTML_NAME).read_text(encoding="utf-8")
    html = html.replace("1013J_R1G_R2 课件路由隔离", "1013J_R1J 模板与小教推荐合并样张")
    html = html.replace("</style>", css() + "\n</style>", 1)
    html = html.replace("    initPrepRoomRenderCanvas();", js() + "\n    initPrepRoomRenderCanvas();", 1)
    return html


def js_check(stage: Path, html: str) -> dict[str, Any]:
    node = shutil.which("node")
    if not node:
        return {"javascript_syntax_check_pass": False, "javascript_syntax_error": "node_not_found"}
    files = []
    for i, text in enumerate(re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, flags=re.S | re.I)):
        p = stage / f"javascript_syntax_1013J_R1J_{i:02d}.js"
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
    for name, size in [("merge", "1440,1100"), ("compact", "1180,920")]:
        out = stage / f"ui_smoke_screenshot_1013J_R1J_{name}.png"
        subprocess.run([str(b), "--headless=new", "--disable-gpu", f"--window-size={size}", f"--screenshot={out}", "file:///" + html_path.as_posix() + "?screen=screen_03#coursewareExpanded"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        w, h = png_size(out)
        shots.append({"case": name, "path": out.name, "width": w, "height": h, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": True, "screenshots": shots}


def validate(html: str) -> dict[str, Any]:
    start = html.rfind('data-1013j-r1j-merge="true"')
    text = html[start : start + 9000] if start >= 0 else html
    artifact_text = html
    visible_text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    banned = ["schema", "payload", "provider", "model", "database", "runtime", "validator"]
    return {
        "template_picker_integrated": "添加页面" in text and "选择模板" in text and "自定义空白页" in artifact_text,
        "agent_recommendation_integrated": "小教推荐" in text and "采纳为课件页" in text and "推荐理由" in text,
        "add_screen_and_agent_recommendation_coexist": "新增：两图对比" in text and "小教建议" in text,
        "lesson_to_screen_mapping_integrated": "比较变化 → 两图对比" in text and "对应课件屏" in text,
        "custom_screen_backlink_integrated": "色卡整理提醒" in text and "保持自由页" in text,
        "screen_count_dynamic": "随课堂需要增减" in text,
        "fixed_8_screen_rule_absent": "固定 8 屏" not in text and "必须 8 屏" not in text and "共 8 屏" not in text,
        "route_isolation_inherited": "prepNotebook" in html and "coursewareExpanded" in html,
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
    write_json(stage / "courseware_template_and_recommendation_merge_state_1013J_R1J.json", {"stage": STAGE_ID, "templates": TEMPLATES, "recommendations": RECOMMENDATIONS, **BOUNDARY})
    write_json(stage / "courseware_screen_operations_merged_fixture_1013J_R1J.json", {"stage": STAGE_ID, "actions": ["添加页面", "删除", "复制", "上移", "下移", "关联备课环节", "设为自由页"], **BOUNDARY})
    write_json(stage / "lesson_to_courseware_mapping_merged_fixture_1013J_R1J.json", {"stage": STAGE_ID, "lesson_section": "比较变化", "screen_candidates": ["两图对比", "词卡页"], **BOUNDARY})
    checks = validate(html)
    checks.update(js_check(stage, html))
    shot = screenshot(stage, html_path)
    checks["screenshot_smoke_pass"] = shot["screenshot_smoke_pass"]
    failed = [k for k, v in checks.items() if k not in BOUNDARY and k not in {"javascript_syntax_files"} and v is not True] + [k for k in BOUNDARY if checks.get(k) is not False]
    result = {
        "stage": STAGE_ID,
        "final_status": FINAL_STATUS if not failed else "FAIL_" + STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "next_stage": "USER_REVIEW_1013J_R1J_COURSEWARE_VISIBLE_WORKFLOW_MERGE_STATIC",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        **checks,
        "screenshots": shot.get("screenshots", []),
        "failed_checks": failed,
    }
    write_json(stage / "1013J_R1J_result.json", result)
    write(stage / "1013J_R1J_report.md", f"# 1013J_R1J\n\nFINAL_STATUS={result['final_status']}\n\nMerged R1H template/screen operations and R1I lesson-section recommendation into one static courseware workspace. Static fixture only; no runtime, provider/model, storage, export, upload, search, or whiteboard library integration.\n\nFailed checks: {failed}\n")
    write(out / "LATEST_REVIEW_ENTRY.md", f"# Latest Review Entry\n\nSTAGE={STAGE_ID}\nFINAL_STATUS={result['final_status']}\nNEXT_STAGE={result['next_stage']}\n\nR1J merges template picker/screen operations with Xiaojiao lesson-section courseware recommendations in a static review fixture.\n")
    write(out / "README.md", f"# Prep Room Review Package\n\nLatest stage: `{STAGE_ID}`\n\nOpen `{STAGE_DIR_NAME}/{HTML_NAME}`.\n")
    write(out / "REVIEW_PACKAGE_MANIFEST.md", f"# Review Package Manifest\n\nLatest stage: `{STAGE_ID}`\n\nIncludes:\n- `{STAGE_DIR_NAME}`\n- `1013J_R1H_courseware_template_picker_and_screen_operations_static`\n- `1013J_R1I_lesson_section_to_courseware_agent_recommendation_static`\n- `scripts/{VALIDATOR_NAME}`\n\nBoundaries: static fixture only; no runtime/provider/model/database/memory/Feishu/export/upload/search/whiteboard integration; main project not pushed.\n")
    delta = out / "source_delta_1013J_R1J" / "scripts" / VALIDATOR_NAME
    delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))
    print("ALL_1013J_R1J_COURSEWARE_TEMPLATE_AND_AGENT_RECOMMENDATION_MERGE_STATIC_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["final_status"], "failed_checks": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
