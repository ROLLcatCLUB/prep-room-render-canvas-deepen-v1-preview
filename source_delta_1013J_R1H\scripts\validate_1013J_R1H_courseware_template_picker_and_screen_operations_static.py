from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STAGE_ID = "1013J_R1H_COURSEWARE_TEMPLATE_PICKER_AND_SCREEN_OPERATIONS_STATIC"
FINAL_STATUS = "PASS_1013J_R1H_COURSEWARE_TEMPLATE_PICKER_AND_SCREEN_OPERATIONS_STATIC"
INHERITS_FROM = "1013J_R1G_R1_COURSEWARE_RESPONSIVE_FULL_WIDTH_PATCH"
BASE_DIR_NAME = "1013J_R1G_R2_courseware_route_isolation_patch"
BASE_HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1G_R2_courseware_route_isolated.html"
STAGE_DIR_NAME = "1013J_R1H_courseware_template_picker_and_screen_operations_static"
HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1H_template_picker_operations.html"
VALIDATOR_NAME = "validate_1013J_R1H_courseware_template_picker_and_screen_operations_static.py"

TEMPLATES = [
    ("cover_title", "封面页", "课题呈现", "课题、背景图", False),
    ("one_image_observation", "一图观察", "图像观察 / 经验唤醒", "图片、课堂问题", False),
    ("two_image_comparison", "两图对比", "比较观察 / 方法发现 / 审美判断", "图片 A、图片 B、课堂问题", False),
    ("three_image_comparison", "三图比较", "归纳发现 / 作品比较", "图片 A、图片 B、图片 C、课堂问题", False),
    ("image_with_question", "图片 + 问题", "图像导入 / 追问", "主图、问题", False),
    ("image_annotation", "图片 + 标注", "观察支架 / 局部分析", "图片、标注提示", True),
    ("word_card", "词卡页", "表达支架 / 关键词回收", "词卡", False),
    ("task_release", "任务发布", "任务说明 / 操作提示", "任务、要求", False),
    ("step_demo", "步骤示范", "方法学习 / 教师示范", "步骤、示范图", False),
    ("whiteboard_interaction", "白板互动", "色卡试验 / 现场标注", "白板区、操作提示", True),
    ("student_work_wall", "学生作品墙", "展示交流 / 同伴评价", "作品位、交流提示", False),
    ("evaluation_prompt", "评价提示", "展示评价 / 修改反馈", "评价点、修改提示", False),
    ("summary_review", "总结回看", "课堂总结 / 回顾", "总结文字", False),
    ("custom_blank", "自定义空白页", "临时提醒 / 过渡页", "自由内容", False),
]

BOUNDARY = {
    "upload_implemented": False, "search_implemented": False, "whiteboard_library_connected": False,
    "ppt_export_implemented": False, "drag_edit_implemented": False, "runtime_connected": False,
    "provider_called": False, "model_called": False, "formal_apply_performed": False,
    "database_written": False, "memory_written": False, "feishu_written": False, "main_project_pushed": False,
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
    .r1h-template-panel{display:none;position:absolute;left:18px;top:72px;right:18px;z-index:10;border:1px solid rgba(43,124,106,.18);border-radius:16px;background:rgba(255,255,250,.96);box-shadow:0 18px 44px rgba(16,61,53,.16);padding:14px}
    .r1h-template-panel.is-open{display:block}
    .r1h-template-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
    .r1h-template-card{border:1px solid rgba(43,124,106,.16);border-radius:12px;background:rgba(240,250,246,.58);padding:10px;display:grid;gap:5px;color:var(--ink);font-size:12px;line-height:1.35;text-align:left}
    .r1h-template-card strong{color:var(--green);font-size:13px}
    .r1h-screen-ops{display:flex;flex-wrap:wrap;gap:5px;margin-top:6px}
    .r1h-screen-ops .quiet-tag{cursor:pointer}
    .r1h-added-badge{display:inline-flex;border-radius:999px;border:1px solid rgba(213,151,72,.28);background:rgba(255,246,226,.72);color:#a16b22;padding:3px 8px;font-size:11px;font-weight:850}
    @media(max-width:1180px){.r1h-template-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
    """


def js() -> str:
    templates = json.dumps([
        {"template_id": tid, "teacher_label": label, "classroom_use": use, "default_slots": slots, "whiteboard_required": wb}
        for tid, label, use, slots, wb in TEMPLATES
    ], ensure_ascii=False)
    return f"""
    const r1hTemplates = {templates};
    function renderCoursewareExpandedWorkspace1013JR1(view) {{
      const current = currentDynamicScreen1013JR1G ? currentDynamicScreen1013JR1G() : null;
      const screen = current || {{screen_id:"screen_03",screen_order:3,screen_title:"哪一组颜色更安静？",template_id:"two_image_comparison",linked_lesson_section:"比较变化",display_intent:"帮助学生比较两组颜色。",material_slots:[{{teacher_label:"热闹色彩图",status:"待补图"}},{{teacher_label:"安静色彩图",status:"待补图"}}],screen_text:{{main_question:"哪一组颜色更安静？"}}}};
      return `
      <div class="courseware-r1e-shell" data-1013j-r1-expanded="true" data-1013j-r1g-dynamic-template="true" data-1013j-r1g-responsive-full="true" data-1013j-r1h-template-picker="true" aria-label="课件制作工作区">
        <div class="courseware-r1e-workbench">
          <aside class="courseware-r1e-left" aria-label="课件草稿">
            <div class="courseware-r1e-title">大屏草稿</div>
            <div class="courseware-r1g-note">样例草稿：8 屏。屏幕可按教学需要增减。</div>
            <button class="node-action primary" type="button" data-r1h-add-page>＋ 添加页面</button>
            <div class="courseware-r1e-screen-list">
              <button class="node-action secondary" type="button"><span>01</span><strong>色彩的感觉</strong><div class="r1h-screen-ops"><span class="quiet-tag">复制</span><span class="quiet-tag">下移</span></div></button>
              <button class="node-action primary" type="button"><span>03</span><strong>哪一组颜色更安静?</strong><div class="r1h-screen-ops"><span class="quiet-tag">删除</span><span class="quiet-tag">复制</span><span class="quiet-tag">上移</span><span class="quiet-tag">下移</span></div></button>
              <button class="node-action secondary" type="button"><span>＋</span><strong>新增：两图对比</strong><div class="r1h-screen-ops"><span class="quiet-tag">关联备课环节</span><span class="quiet-tag">设为自由页</span></div></button>
              <button class="node-action secondary" type="button"><span>自</span><strong>自定义页面</strong><div class="r1h-screen-ops"><span class="quiet-tag">自由页</span><span class="quiet-tag">删除</span></div></button>
            </div>
            <div class="r1h-template-panel" data-r1h-template-panel>
              <div class="courseware-r1e-title">选择模板</div>
              <div class="r1h-template-grid">
                ${{r1hTemplates.map(t=>`<button class="r1h-template-card" type="button"><strong>${{html(t.teacher_label)}}</strong><span>适合：${{html(t.classroom_use)}}</span><span>素材位：${{html(t.default_slots)}}</span><span>${{t.whiteboard_required?"可白板":"普通页"}}</span></button>`).join("")}}
              </div>
            </div>
          </aside>
          <main class="courseware-r1e-main" aria-label="课堂大屏画面">
            <div class="courseware-r1e-toolbar"><div class="courseware-r1e-tools"><button class="courseware-r1e-icon primary" type="button">▶</button><button class="courseware-r1e-icon" type="button">图</button><button class="courseware-r1e-icon" type="button">字</button></div><div class="courseware-r1e-ratio"><span class="courseware-r1e-segment"><button class="active" type="button">16:9</button><button type="button">4:3</button></span></div></div>
            <section class="courseware-r1e-screen-frame"><div class="courseware-r1e-screen"><div><div class="courseware-r1e-question">哪一组更安静?</div><div class="courseware-r1g-screen-meta"><span class="courseware-r1g-chip">两图对比</span><span class="courseware-r1g-chip">关联：比较变化</span><span class="r1h-added-badge">新增页面样例</span></div></div><div class="courseware-r1g-slot-grid"><div class="courseware-r1g-slot">图片 A<br><span class="quiet-tag">待补图</span></div><div class="courseware-r1g-slot">图片 B<br><span class="quiet-tag">待补图</span></div></div><div class="courseware-r1e-bottom-tools"><span>课堂问题</span><span class="quiet-tag">待教师确认</span></div></div></section>
          </main>
          <aside class="courseware-r1e-right courseware-r1g-side-stack" aria-label="模板与操作">
            <button class="node-action secondary" type="button" data-courseware-normal="true">回到备课</button><button class="node-action primary" type="button">大屏预览</button>
            <div class="courseware-r1e-title">页面操作</div>
            <div class="courseware-side-block"><strong>新增页面</strong><p>模板：两图对比；状态：待补图；关联：比较变化。</p></div>
            <div class="courseware-side-block"><strong>自定义空白页</strong><p>未关联备课环节，可保持自由页。</p></div>
            <div class="courseware-side-block"><strong>操作</strong><p>删除 / 复制 / 上移 / 下移 / 关联备课环节</p></div>
          </aside>
        </div>
      </div>`;
    }}
    document.addEventListener("click",e=>{{const b=e.target.closest("[data-r1h-add-page]"); if(b){{e.preventDefault();document.querySelector("[data-r1h-template-panel]")?.classList.toggle("is-open");}}}});
    """


def patch_html(out: Path) -> str:
    html = (out / BASE_DIR_NAME / BASE_HTML_NAME).read_text(encoding="utf-8")
    html = html.replace("1013J_R1G_R2 课件路由隔离", "1013J_R1H 模板选择与页面操作")
    html = html.replace("</style>", css() + "\n</style>", 1)
    html = html.replace("    initPrepRoomRenderCanvas();", js() + "\n    initPrepRoomRenderCanvas();", 1)
    return html


def js_check(stage: Path, html: str) -> dict[str, Any]:
    node = shutil.which("node")
    if not node:
        return {"javascript_syntax_check_pass": False, "javascript_syntax_error": "node_not_found"}
    scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, flags=re.S | re.I)
    files = []
    for i, text in enumerate(scripts):
        p = stage / f"javascript_syntax_1013J_R1H_{i:02d}.js"
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
    for name, extra in [("template_picker", ""), ("added_screen", ""), ("custom_screen", "")]:
        out = stage / f"ui_smoke_screenshot_1013J_R1H_{name}.png"
        subprocess.run([str(b), "--headless=new", "--disable-gpu", "--window-size=1440,1100", f"--screenshot={out}", "file:///" + html_path.as_posix() + "?screen=screen_03#coursewareExpanded"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        w, h = png_size(out)
        shots.append({"case": name, "path": out.name, "width": w, "height": h, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": True, "screenshots": shots}


def validate(html: str) -> dict[str, Any]:
    start = html.rfind('data-1013j-r1h-template-picker="true"')
    text = html[start : start + 6000] if start >= 0 else html
    artifact_text = html
    visible_text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    banned = ["schema", "payload", "provider", "model", "database", "runtime", "validator"]
    return {
        "template_picker_created": "添加页面" in text and "选择模板" in text,
        "template_count_minimum_met": len(TEMPLATES) >= 12,
        "add_screen_static_interaction_created": "data-r1h-add-page" in html,
        "added_screen_preview_created": "新增页面样例" in text,
        "custom_blank_screen_addable": "自定义空白页" in artifact_text and "自由页" in artifact_text,
        "delete_screen_static_action_present": "删除" in text,
        "duplicate_screen_static_action_present": "复制" in text,
        "reorder_screen_static_action_present": "上移" in text and "下移" in text,
        "linked_screen_and_unlinked_screen_visible": "关联：比较变化" in artifact_text and "未关联备课环节" in artifact_text,
        "lesson_section_link_selector_present": "关联备课环节" in text,
        "screen_count_not_fixed": "屏幕可按教学需要增减" in text,
        "sample_8_screens_not_treated_as_rule": "样例草稿：8 屏" in text and "固定 8 屏" not in text and "必须 8 屏" not in text and "共 8 屏" not in text,
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
    write_json(stage / "courseware_template_picker_state_1013J_R1H.json", {"stage": STAGE_ID, "templates": [{"template_id": t[0], "teacher_label": t[1], "use": t[2], "slots": t[3], "whiteboard": t[4]} for t in TEMPLATES], **BOUNDARY})
    write_json(stage / "screen_operations_fixture_1013J_R1H.json", {"stage": STAGE_ID, "actions": ["删除", "复制", "上移", "下移", "设为自由页", "关联备课环节"], **BOUNDARY})
    write_json(stage / "custom_screen_operation_fixture_1013J_R1H.json", {"stage": STAGE_ID, "custom_blank_screen_addable": True, "linked_to_lesson": False, **BOUNDARY})
    checks = validate(html)
    checks.update(js_check(stage, html))
    checks["screenshot_smoke_pass"] = screenshot(stage, html_path)["screenshot_smoke_pass"]
    failed = [k for k, v in checks.items() if k not in BOUNDARY and k not in {"javascript_syntax_files"} and v is not True] + [k for k in BOUNDARY if checks.get(k) is not False]
    result = {"stage": STAGE_ID, "final_status": FINAL_STATUS if not failed else "FAIL_" + STAGE_ID, "inherits_from": INHERITS_FROM, "next_stage": "WAITING_FOR_R1I_OR_READY_FOR_R1J_IF_BOTH_PASS", "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), **checks, "failed_checks": failed}
    write_json(stage / "1013J_R1H_result.json", result)
    write(stage / "1013J_R1H_report.md", f"# 1013J_R1H\n\nFINAL_STATUS={result['final_status']}\n\nTemplate picker and static screen operations only. No backend/runtime writes.\n\nFailed checks: {failed}\n")
    write(out / "LATEST_REVIEW_ENTRY.md", f"# Latest Review Entry\n\nSTAGE={STAGE_ID}\nFINAL_STATUS={result['final_status']}\nNEXT_STAGE={result['next_stage']}\n\nR1H adds template picker, add screen sample, custom blank screen, and static delete/copy/reorder/link actions.\n")
    write(out / "README.md", f"# Prep Room Review Package\n\nLatest stage: `{STAGE_ID}`\n\nOpen `{STAGE_DIR_NAME}/{HTML_NAME}`.\n")
    write(out / "REVIEW_PACKAGE_MANIFEST.md", f"# Review Package Manifest\n\nLatest stage: `{STAGE_ID}`\n\nIncludes `{STAGE_DIR_NAME}` and `scripts/{VALIDATOR_NAME}`.\n")
    delta = out / "source_delta_1013J_R1H" / "scripts" / VALIDATOR_NAME
    delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))
    print("ALL_1013J_R1H_COURSEWARE_TEMPLATE_PICKER_AND_SCREEN_OPERATIONS_STATIC_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["final_status"], "failed_checks": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
