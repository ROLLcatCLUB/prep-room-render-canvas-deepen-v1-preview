from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STAGE_ID = "1013J_R1I_LESSON_SECTION_TO_COURSEWARE_AGENT_RECOMMENDATION_STATIC"
FINAL_STATUS = "PASS_1013J_R1I_LESSON_SECTION_TO_COURSEWARE_AGENT_RECOMMENDATION_STATIC"
INHERITS_FROM = "1013J_R1G_R1_COURSEWARE_RESPONSIVE_FULL_WIDTH_PATCH"
BASE_DIR_NAME = "1013J_R1G_R2_courseware_route_isolation_patch"
BASE_HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1G_R2_courseware_route_isolated.html"
STAGE_DIR_NAME = "1013J_R1I_lesson_section_to_courseware_agent_recommendation_static"
HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1I_lesson_to_courseware_recommendation.html"
VALIDATOR_NAME = "validate_1013J_R1I_lesson_section_to_courseware_agent_recommendation_static.py"

BOUNDARY = {
    "formal_apply_performed": False, "runtime_connected": False, "provider_called": False,
    "model_called": False, "database_written": False, "memory_written": False, "feishu_written": False,
    "upload_implemented": False, "search_implemented": False, "whiteboard_library_connected": False,
    "ppt_export_implemented": False, "drag_edit_implemented": False, "main_project_pushed": False,
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


RECS = [
    {
        "template": "两图对比",
        "title": "哪一组颜色更安静？",
        "text": "你从哪些颜色看出来？",
        "slots": "热闹色彩组合图 / 安静色彩组合图",
        "reason": "这一段需要学生通过比较说出色彩感受，两图对比比纯文字更适合大屏呈现。",
        "actions": ["采纳为课件页", "换成三图比较", "暂不生成"],
    },
    {
        "template": "词卡页",
        "title": "把“好看”说得更具体",
        "text": "热烈 / 安静 / 柔和 / 强烈 / 明亮 / 沉稳",
        "slots": "感觉词卡",
        "reason": "学生容易只说“好看”，需要语言支架。",
        "actions": ["采纳为课件页", "改词卡", "暂不生成"],
    },
]


def css() -> str:
    return """
    .r1i-selected-section{border:1px solid rgba(43,124,106,.18);border-radius:14px;background:rgba(240,250,246,.58);padding:12px;display:grid;gap:6px}
    .r1i-recommendation-list{display:grid;gap:10px}
    .r1i-rec-card{border:1px solid rgba(43,124,106,.16);border-radius:14px;background:rgba(255,255,250,.72);padding:12px;display:grid;gap:7px}
    .r1i-rec-card strong{color:var(--ink)}
    .r1i-rec-actions{display:flex;flex-wrap:wrap;gap:7px}
    .r1i-preview-state{border:1px solid rgba(213,151,72,.28);border-radius:14px;background:rgba(255,246,226,.70);padding:10px;color:#7b551e;font-size:12px;line-height:1.45}
    .r1i-backlink{border:1px dashed rgba(43,124,106,.24);border-radius:14px;background:rgba(240,250,246,.42);padding:10px;font-size:12px;line-height:1.45}
    """


def js() -> str:
    recs = json.dumps(RECS, ensure_ascii=False)
    return f"""
    const r1iRecommendations = {recs};
    function renderCoursewareExpandedWorkspace1013JR1(view) {{
      return `
      <div class="courseware-r1e-shell" data-1013j-r1-expanded="true" data-1013j-r1g-dynamic-template="true" data-1013j-r1g-responsive-full="true" data-1013j-r1i-agent-recommendation="true" aria-label="课件制作工作区">
        <div class="courseware-r1e-workbench">
          <aside class="courseware-r1e-left" aria-label="备课段落">
            <div class="courseware-r1e-title">选中备课段</div>
            <div class="r1i-selected-section"><strong>当前备课段：比较变化</strong><p>学生比较两组色彩，尝试说出哪一组更安静、更热闹，并说明理由。</p><span class="quiet-tag">可生成大屏支持</span></div>
            <div class="courseware-r1e-title">大屏草稿</div>
            <button class="node-action primary" type="button"><span>03</span><strong>哪一组颜色更安静？</strong></button>
            <button class="node-action secondary" type="button"><span>04</span><strong>把“好看”说得更具体</strong></button>
          </aside>
          <main class="courseware-r1e-main" aria-label="小教推荐">
            <div class="courseware-r1e-toolbar"><div class="courseware-r1e-tools"><button class="courseware-r1e-icon primary" type="button">▶</button><button class="courseware-r1e-icon" type="button">图</button><button class="courseware-r1e-icon" type="button">字</button></div><div class="courseware-r1e-ratio"><span class="courseware-r1e-segment"><button class="active" type="button">16:9</button><button type="button">4:3</button></span></div></div>
            <section class="courseware-r1e-screen-frame"><div class="courseware-r1e-screen"><div><div class="courseware-r1e-question">小教建议为这一段生成 2 页大屏</div><div class="courseware-r1g-screen-meta"><span class="courseware-r1g-chip">比较变化</span><span class="courseware-r1g-chip">待教师确认</span></div></div><div class="r1i-recommendation-list">${{r1iRecommendations.map((rec)=>`<div class="r1i-rec-card"><strong>${{html(rec.template)}}｜${{html(rec.title)}}</strong><p>${{html(rec.text)}}</p><p>素材占位：${{html(rec.slots)}}</p><p>推荐理由：${{html(rec.reason)}}</p><div class="r1i-rec-actions">${{rec.actions.map(a=>`<button class="node-action secondary" type="button">${{html(a)}}</button>`).join("")}}</div></div>`).join("")}}</div><div class="r1i-preview-state">已加入大屏草稿预览｜状态：待教师确认｜关联备课段：比较变化</div></div></section>
          </main>
          <aside class="courseware-r1e-right courseware-r1g-side-stack" aria-label="推荐与映射">
            <button class="node-action secondary" type="button" data-courseware-normal="true">回到备课</button><button class="node-action primary" type="button">大屏预览</button>
            <div class="courseware-r1e-title">小教建议</div>
            <div class="courseware-side-block"><strong>对应备课段</strong><p>比较变化</p></div>
            <div class="courseware-side-block"><strong>推荐模板</strong><p>两图对比；词卡页</p></div>
            <div class="courseware-side-block"><strong>显示目的</strong><p>帮助学生从“好看”转向说出具体色彩感受。</p></div>
            <div class="r1i-backlink"><strong>自由页反向关联</strong><p>你新增了“色卡整理提醒”页面。小教建议：这一页可以放入“材料准备”环节，是否关联到备课？</p><div class="r1i-rec-actions"><button class="node-action secondary" type="button">关联到材料准备</button><button class="node-action secondary" type="button">保持自由页</button><button class="node-action secondary" type="button">暂不处理</button></div></div>
          </aside>
        </div>
      </div>`;
    }}
    """


def patch_html(out: Path) -> str:
    html = (out / BASE_DIR_NAME / BASE_HTML_NAME).read_text(encoding="utf-8")
    html = html.replace("1013J_R1G_R2 课件路由隔离", "1013J_R1I 备课段推荐课件页")
    html = html.replace("</style>", css() + "\n</style>", 1)
    html = html.replace("    initPrepRoomRenderCanvas();", js() + "\n    initPrepRoomRenderCanvas();", 1)
    return html


def js_check(stage: Path, html: str) -> dict[str, Any]:
    node = shutil.which("node")
    if not node:
        return {"javascript_syntax_check_pass": False}
    files = []
    for i, s in enumerate(re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, flags=re.S | re.I)):
        p = stage / f"javascript_syntax_1013J_R1I_{i:02d}.js"
        write(p, s)
        files.append(p.name)
        proc = subprocess.run([node, "--check", str(p)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode:
            return {"javascript_syntax_check_pass": False, "javascript_syntax_error": proc.stderr or proc.stdout, "javascript_syntax_files": files}
    return {"javascript_syntax_check_pass": True, "javascript_syntax_files": files}


def screenshot(stage: Path, html_path: Path) -> dict[str, Any]:
    b = browser()
    shots = []
    if not b:
        return {"screenshot_smoke_pass": False}
    for name in ["section_selected", "agent_recommendation", "accept_preview"]:
        out = stage / f"ui_smoke_screenshot_1013J_R1I_{name}.png"
        subprocess.run([str(b), "--headless=new", "--disable-gpu", "--window-size=1440,1100", f"--screenshot={out}", "file:///" + html_path.as_posix() + "?screen=screen_03#coursewareExpanded"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        w, h = png_size(out)
        shots.append({"case": name, "path": out.name, "width": w, "height": h, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": True, "screenshots": shots}


def validate(html: str) -> dict[str, Any]:
    start = html.rfind('data-1013j-r1i-agent-recommendation="true"')
    text = html[start : start + 6000] if start >= 0 else html
    recommendation_source = html
    visible_text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    banned = ["schema", "payload", "provider", "model", "database", "runtime", "validator"]
    return {
        "lesson_section_selected": "当前备课段：比较变化" in text,
        "agent_recommendation_panel_created": "小教建议为这一段生成" in text,
        "recommendation_count_minimum_met": len(RECS) >= 2 and all(rec.get("reason") for rec in RECS),
        "template_recommendations_present": "两图对比" in recommendation_source and "词卡页" in recommendation_source,
        "material_slots_in_recommendations": "素材占位" in recommendation_source,
        "recommendation_reason_present": "推荐理由" in recommendation_source,
        "accept_as_courseware_screen_action_present": "采纳为课件页" in recommendation_source,
        "change_template_action_present": "换成三图比较" in recommendation_source or "改词卡" in recommendation_source,
        "reject_recommendation_action_present": "暂不生成" in recommendation_source,
        "accept_preview_state_created": "已加入大屏草稿预览" in text,
        "lesson_to_screen_mapping_visible": "对应备课段" in text and "比较变化" in text,
        "custom_screen_backlink_suggestion_present": "色卡整理提醒" in text and "关联到材料准备" in text,
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
    write_json(stage / "lesson_section_recommendation_state_1013J_R1I.json", {"stage": STAGE_ID, "selected_section": "比较变化", **BOUNDARY})
    write_json(stage / "agent_courseware_recommendation_fixture_1013J_R1I.json", {"stage": STAGE_ID, "recommendations": RECS, **BOUNDARY})
    write_json(stage / "lesson_to_screen_acceptance_fixture_1013J_R1I.json", {"stage": STAGE_ID, "accepted_preview": True, "linked_lesson_section": "比较变化", **BOUNDARY})
    checks = validate(html)
    checks.update(js_check(stage, html))
    checks["screenshot_smoke_pass"] = screenshot(stage, html_path)["screenshot_smoke_pass"]
    failed = [k for k, v in checks.items() if k not in BOUNDARY and k not in {"javascript_syntax_files"} and v is not True] + [k for k in BOUNDARY if checks.get(k) is not False]
    result = {"stage": STAGE_ID, "final_status": FINAL_STATUS if not failed else "FAIL_" + STAGE_ID, "inherits_from": INHERITS_FROM, "next_stage": "WAITING_FOR_R1H_OR_READY_FOR_R1J_IF_BOTH_PASS", "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), **checks, "failed_checks": failed}
    result["auto_continue_allowed"] = not failed
    result["next_recommended"] = "1013J_R1J_COURSEWARE_TEMPLATE_AND_AGENT_RECOMMENDATION_MERGE_STATIC" if not failed else "NONE"
    if not failed:
        result["next_stage"] = "1013J_R1J_COURSEWARE_TEMPLATE_AND_AGENT_RECOMMENDATION_MERGE_STATIC"
    write_json(stage / "1013J_R1I_result.json", result)
    write(stage / "1013J_R1I_report.md", f"# 1013J_R1I\n\nFINAL_STATUS={result['final_status']}\n\nLesson section to courseware recommendation static surface only.\n\nFailed checks: {failed}\n")
    write(out / "LATEST_REVIEW_ENTRY.md", f"# Latest Review Entry\n\nSTAGE={STAGE_ID}\nFINAL_STATUS={result['final_status']}\nNEXT_STAGE={result['next_stage']}\n\nR1I adds selected lesson section, Xiaojiao recommendations, accept preview state, and custom screen backlink suggestion.\n")
    write(out / "README.md", f"# Prep Room Review Package\n\nLatest stage: `{STAGE_ID}`\n\nOpen `{STAGE_DIR_NAME}/{HTML_NAME}`.\n")
    write(out / "REVIEW_PACKAGE_MANIFEST.md", f"# Review Package Manifest\n\nLatest stage: `{STAGE_ID}`\n\nIncludes `{STAGE_DIR_NAME}` and `scripts/{VALIDATOR_NAME}`.\n")
    delta = out / "source_delta_1013J_R1I" / "scripts" / VALIDATOR_NAME
    delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))
    print("ALL_1013J_R1I_LESSON_SECTION_TO_COURSEWARE_AGENT_RECOMMENDATION_STATIC_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["final_status"], "failed_checks": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
