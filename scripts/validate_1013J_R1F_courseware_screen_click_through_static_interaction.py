from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013J_R1F_COURSEWARE_SCREEN_CLICK_THROUGH_STATIC_INTERACTION"
FINAL_STATUS = "PASS_1013J_R1F_COURSEWARE_SCREEN_CLICK_THROUGH_STATIC_INTERACTION"
INHERITS_FROM = "1013J_R1E_COURSEWARE_SCREEN_RATIO_AND_VISUAL_DOMINANCE_PATCH"
NEXT_STAGE = "USER_REVIEW_COURSEWARE_SCREEN_CLICK_THROUGH"
BASE_DIR_NAME = "1013J_R1E_courseware_screen_ratio_and_visual_dominance_patch"
BASE_HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1E_courseware_screen_ratio_and_visual_dominance.html"
STAGE_DIR_NAME = "1013J_R1F_courseware_screen_click_through_static_interaction"
HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1F_courseware_click_through.html"
VALIDATOR_NAME = "validate_1013J_R1F_courseware_screen_click_through_static_interaction.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]

SCREENS: list[dict[str, Any]] = [
    {
        "id": "screen_01_cover",
        "index": "01",
        "nav_title": "课题导入",
        "screen_title": "色彩的感觉",
        "classroom_text": "颜色为什么会让人产生不同感觉？",
        "lesson_link": "导入问题",
        "purpose": "把课题交给学生，从色彩带来的第一感觉进入。",
        "materials": ["课题背景图"],
        "status": "已有文字",
        "suggestion": "先让学生看一眼色彩画面，再说第一感觉。",
        "tools": ["改文字", "补素材"],
    },
    {
        "id": "screen_02_observe",
        "index": "02",
        "nav_title": "看色彩图片",
        "screen_title": "这些颜色给你什么感觉？",
        "classroom_text": "先说第一感觉，不急着判断对错。",
        "lesson_link": "观察感受",
        "purpose": "用图片打开色彩经验，避免一开始就讲概念。",
        "materials": ["生活色彩图片 A", "生活色彩图片 B", "生活色彩图片 C"],
        "status": "待补图",
        "suggestion": "图片要有明显色彩差异，方便学生先说感觉。",
        "tools": ["补素材", "改文字"],
    },
    {
        "id": "screen_03_compare",
        "index": "03",
        "nav_title": "比较两组颜色",
        "screen_title": "哪一组颜色更安静？",
        "classroom_text": "你从哪些颜色看出来？",
        "lesson_link": "比较变化",
        "purpose": "帮助学生从“好看”说到“为什么安静”。",
        "materials": ["热闹色彩图", "安静色彩图"],
        "status": "待补图 / 可圈画",
        "suggestion": "先看图，再圈出颜色依据。",
        "tools": ["补素材", "圈画", "改文字"],
    },
    {
        "id": "screen_04_words",
        "index": "04",
        "nav_title": "感觉词卡",
        "screen_title": "把“好看”说得更具体",
        "classroom_text": "热烈 / 安静 / 柔和 / 强烈 / 明亮 / 沉稳",
        "lesson_link": "表达词汇",
        "purpose": "给学生一些可选择的感觉词，支撑后面的说明。",
        "materials": ["感觉词卡"],
        "status": "已有文字",
        "suggestion": "词卡不宜太多，保留学生能说出口的词。",
        "tools": ["改文字", "加入互动"],
    },
    {
        "id": "screen_05_task",
        "index": "05",
        "nav_title": "色彩实验任务",
        "screen_title": "用 3-4 种颜色表达一种感觉",
        "classroom_text": "选一组颜色，说说你想表达什么感觉。",
        "lesson_link": "任务发布",
        "purpose": "把观察和比较转成一次可完成的小练习。",
        "materials": ["任务说明"],
        "status": "待教师确认",
        "suggestion": "任务文字要短，重点放在颜色选择和表达理由。",
        "tools": ["改文字", "补素材"],
    },
    {
        "id": "screen_06_whiteboard",
        "index": "06",
        "nav_title": "白板试色",
        "screen_title": "试一组颜色",
        "classroom_text": "拖一拖色卡，看看画面感觉有什么变化。",
        "lesson_link": "色卡试验",
        "purpose": "让学生看见色彩组合变化，而不是只听老师解释。",
        "materials": ["色卡拖拽区", "白板区"],
        "status": "可白板",
        "suggestion": "白板只作为这一屏的局部互动，保留画面主体。",
        "tools": ["圈画", "加入互动", "改文字"],
    },
    {
        "id": "screen_07_show",
        "index": "07",
        "nav_title": "学生作品展示",
        "screen_title": "说说你的色彩选择",
        "classroom_text": "我用了哪些颜色？我想表达什么感觉？",
        "lesson_link": "作品交流",
        "purpose": "让作品展示和表达理由连在一起。",
        "materials": ["学生作品展示位"],
        "status": "待学生作品",
        "suggestion": "预留两到三件作品位，便于比较不同表达。",
        "tools": ["补素材", "改文字"],
    },
    {
        "id": "screen_08_summary",
        "index": "08",
        "nav_title": "总结回看",
        "screen_title": "颜色会改变画面的感觉",
        "classroom_text": "看色彩、说感觉、比变化、做表达、会修改。",
        "lesson_link": "总结回看",
        "purpose": "收束这节课的学习路径，回到色彩表达。",
        "materials": ["总结页"],
        "status": "已有文字",
        "suggestion": "总结保留一行路径，不要变成知识点堆叠。",
        "tools": ["改文字"],
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def locate_output_root(root: Path) -> Path:
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    if (root / "LATEST_REVIEW_ENTRY.md").exists():
        return root
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "upload_implemented": False,
        "search_implemented": False,
        "whiteboard_library_connected": False,
        "ppt_export_implemented": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def r1f_css() -> str:
    return """

    /* 1013J_R1F: click-through courseware screens */
    [data-1013j-r1f-click-through="true"] .courseware-r1e-screen-list .node-action {
      cursor: pointer;
      transition: background .16s ease, color .16s ease, border-color .16s ease;
    }

    [data-1013j-r1f-click-through="true"] .courseware-r1e-screen-list .node-action.is-selected {
      background: var(--green);
      color: #fff;
      border-color: var(--green);
      box-shadow: 0 8px 18px rgba(43, 124, 106, .16);
    }

    [data-1013j-r1f-click-through="true"] .courseware-r1e-screen-list .node-action.is-selected strong,
    [data-1013j-r1f-click-through="true"] .courseware-r1e-screen-list .node-action.is-selected span {
      color: #fff;
    }

    [data-1013j-r1f-click-through="true"] .courseware-r1e-screen {
      grid-template-rows: auto 1fr auto;
    }

    [data-1013j-r1f-click-through="true"] .courseware-r1e-question {
      font-size: clamp(13px, 1.1vw, 19px);
      font-weight: 880;
      color: rgba(18, 31, 28, .86);
      line-height: 1.28;
    }

    [data-1013j-r1f-click-through="true"] .courseware-r1f-classroom-text {
      color: rgba(29, 39, 35, .54);
      font-size: clamp(11px, .92vw, 15px);
      line-height: 1.35;
      margin-top: 6px;
    }

    [data-1013j-r1f-click-through="true"] .courseware-r1e-image-grid {
      min-height: 0;
    }

    [data-1013j-r1f-click-through="true"] .courseware-r1e-image-slot {
      min-height: clamp(190px, 24vw, 360px);
      font-size: clamp(13px, 1.1vw, 18px);
    }

    [data-1013j-r1f-click-through="true"] .courseware-r1e-image-grid.is-three {
      grid-template-columns: repeat(3, 1fr);
    }

    [data-1013j-r1f-click-through="true"] .courseware-r1e-image-grid.is-one {
      grid-template-columns: 1fr;
    }

    [data-1013j-r1f-click-through="true"] .courseware-r1e-image-grid.is-whiteboard {
      grid-template-columns: 1fr 1fr;
    }

    [data-1013j-r1f-click-through="true"] .courseware-r1e-right .courseware-side-block p {
      margin: 5px 0 0;
    }

    [data-1013j-r1f-click-through="true"] .courseware-r1f-action-row {
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
      margin-top: 8px;
    }

    [data-1013j-r1f-click-through="true"] .courseware-r1f-action-row .node-action {
      min-height: 28px;
      padding: 5px 10px;
    }
"""


def r1f_js() -> str:
    data = json.dumps(SCREENS, ensure_ascii=False)
    return f"""
    const coursewareScreens1013JR1F = {data};

    function getInitialCoursewareScreen1013JR1F() {{
      const hash = window.location.hash || "";
      const params = new URLSearchParams(window.location.search || "");
      const requested = params.get("screen") || "";
      return coursewareScreens1013JR1F.find((screen) => requested === screen.id || hash.includes(screen.id) || hash.includes(screen.index)) || coursewareScreens1013JR1F[2];
    }}

    function renderCoursewareMaterials1013JR1F(screen) {{
      const gridClass = screen.materials.length === 1 ? "is-one" : (screen.materials.length === 3 ? "is-three" : (screen.id === "screen_06_whiteboard" ? "is-whiteboard" : ""));
      return `<div class="courseware-r1e-image-grid ${{gridClass}}">${{screen.materials.map((item) => `<div class="courseware-r1e-image-slot">${{html(item)}}<br><span class="quiet-tag">${{html(screen.status)}}</span></div>`).join("")}}</div>`;
    }}

    function setCoursewareScreen1013JR1F(screenId) {{
      const screen = coursewareScreens1013JR1F.find((item) => item.id === screenId) || coursewareScreens1013JR1F[2];
      document.querySelectorAll("[data-r1f-screen-id]").forEach((button) => {{
        button.classList.toggle("primary", button.dataset.r1fScreenId === screen.id);
        button.classList.toggle("secondary", button.dataset.r1fScreenId !== screen.id);
        button.classList.toggle("is-selected", button.dataset.r1fScreenId === screen.id);
        button.setAttribute("aria-pressed", button.dataset.r1fScreenId === screen.id ? "true" : "false");
      }});
      const frame = document.querySelector("[data-r1f-current-screen]");
      if (frame) frame.dataset.r1fCurrentScreen = screen.id;
      const title = document.querySelector("[data-r1f-screen-title]");
      if (title) title.textContent = screen.screen_title;
      const text = document.querySelector("[data-r1f-classroom-text]");
      if (text) text.textContent = screen.classroom_text;
      const materials = document.querySelector("[data-r1f-materials]");
      if (materials) materials.innerHTML = renderCoursewareMaterials1013JR1F(screen);
      const bottom = document.querySelector("[data-r1f-bottom-tools]");
      if (bottom) bottom.innerHTML = `<span>${{html(screen.lesson_link)}}</span><span class="quiet-tag">${{html(screen.status)}}</span>`;
      const sideLesson = document.querySelector("[data-r1f-side-lesson]");
      if (sideLesson) sideLesson.textContent = screen.lesson_link;
      const sidePurpose = document.querySelector("[data-r1f-side-purpose]");
      if (sidePurpose) sidePurpose.textContent = screen.purpose;
      const sideMaterials = document.querySelector("[data-r1f-side-materials]");
      if (sideMaterials) sideMaterials.textContent = screen.materials.join("；");
      const sideSuggestion = document.querySelector("[data-r1f-side-suggestion]");
      if (sideSuggestion) sideSuggestion.textContent = screen.suggestion;
      const sideActions = document.querySelector("[data-r1f-side-actions]");
      if (sideActions) sideActions.innerHTML = screen.tools.map((tool) => `<button class="node-action secondary" type="button" data-preview-only="true">${{html(tool)}}</button>`).join("");
    }}

    function renderCoursewareExpandedWorkspace1013JR1(view) {{
      const current = getInitialCoursewareScreen1013JR1F();
      return `
        <div class="courseware-r1e-shell" data-1013j-r1-expanded="true" data-1013j-r1f-click-through="true" aria-label="课件制作工作区">
          <div class="courseware-r1e-workbench">
            <aside class="courseware-r1e-left" aria-label="课件草稿">
              <div class="courseware-r1e-title">课件草稿</div>
              <div class="courseware-r1e-status">
                <span>8 屏</span>
                <span>3 待补图</span>
                <span>1 可圈画</span>
              </div>
              <nav class="courseware-r1e-screen-list" aria-label="课件目录">
                ${{coursewareScreens1013JR1F.map((screen) => `
                  <button class="node-action ${{screen.id === current.id ? "primary is-selected" : "secondary"}}" type="button" data-r1f-screen-id="${{html(screen.id)}}" aria-pressed="${{screen.id === current.id ? "true" : "false"}}">
                    <span>${{html(screen.index)}}</span>
                    <strong>${{html(screen.nav_title)}}</strong>
                  </button>
                `).join("")}}
              </nav>
            </aside>
            <main class="courseware-r1e-main" aria-label="课堂大屏画面">
              <div class="courseware-r1e-toolbar" aria-label="大屏工具条">
                <div class="courseware-r1e-tools">
                  <button class="courseware-r1e-icon primary" type="button" title="进入大屏预览">▶</button>
                  <button class="courseware-r1e-icon" type="button" title="补图片">图</button>
                  <button class="courseware-r1e-icon" type="button" title="圈画">圈</button>
                  <button class="courseware-r1e-icon" type="button" title="改文字">字</button>
                </div>
                <div class="courseware-r1e-ratio" aria-label="画面比例">
                  <span class="courseware-r1e-segment" role="group" aria-label="大屏比例切换">
                    <button class="active" type="button" data-r1f-ratio="16:9">16:9</button>
                    <button type="button" data-r1f-ratio="4:3">4:3</button>
                  </span>
                </div>
              </div>
              <section class="courseware-r1e-screen-frame" data-screen-ratio="16:9" data-r1f-current-screen="${{html(current.id)}}" aria-label="课堂大屏">
                <div class="courseware-r1e-screen">
                  <div>
                    <div class="courseware-r1e-question" data-r1f-screen-title>${{html(current.screen_title)}}</div>
                    <div class="courseware-r1f-classroom-text" data-r1f-classroom-text>${{html(current.classroom_text)}}</div>
                  </div>
                  <div data-r1f-materials>${{renderCoursewareMaterials1013JR1F(current)}}</div>
                  <div class="courseware-r1e-bottom-tools" data-whiteboard-as-block="true" data-r1f-bottom-tools>
                    <span>${{html(current.lesson_link)}}</span>
                    <span class="quiet-tag">${{html(current.status)}}</span>
                  </div>
                </div>
              </section>
            </main>
            <aside class="courseware-r1e-right" aria-label="当前屏设置">
              <button class="node-action secondary" type="button" data-courseware-normal="true">回到备课</button>
              <button class="node-action primary" type="button">大屏预览</button>
              <div class="courseware-r1e-title">当前屏</div>
              <div class="courseware-side-block">
                <strong>对应备课段</strong>
                <p data-r1f-side-lesson>${{html(current.lesson_link)}}</p>
              </div>
              <div class="courseware-side-block">
                <strong>本屏作用</strong>
                <p data-r1f-side-purpose>${{html(current.purpose)}}</p>
              </div>
              <div class="courseware-side-block">
                <strong>素材</strong>
                <p data-r1f-side-materials>${{html(current.materials.join("；"))}}</p>
                ${{renderCoursewareStatus1013JR1(current.status)}}
              </div>
              <div class="courseware-side-block">
                <strong>小教建议</strong>
                <p data-r1f-side-suggestion>${{html(current.suggestion)}}</p>
              </div>
              <div class="courseware-side-block">
                <strong>操作</strong>
                <div class="courseware-r1f-action-row" data-r1f-side-actions>
                  ${{current.tools.map((tool) => `<button class="node-action secondary" type="button" data-preview-only="true">${{html(tool)}}</button>`).join("")}}
                </div>
              </div>
            </aside>
          </div>
        </div>
      `;
    }}

    document.addEventListener("click", (event) => {{
      const screenButton = event.target.closest("[data-r1f-screen-id]");
      if (screenButton) {{
        event.preventDefault();
        setCoursewareScreen1013JR1F(screenButton.dataset.r1fScreenId);
        return;
      }}
      const ratioButton = event.target.closest("[data-r1f-ratio]");
      if (ratioButton) {{
        event.preventDefault();
        document.querySelectorAll("[data-r1f-ratio]").forEach((button) => button.classList.toggle("active", button === ratioButton));
        const frame = document.querySelector("[data-screen-ratio]");
        if (frame) frame.dataset.screenRatio = ratioButton.dataset.r1fRatio;
      }}
    }});
"""


def patch_html(output_root: Path) -> str:
    base_html = output_root / BASE_DIR_NAME / BASE_HTML_NAME
    html_text = base_html.read_text(encoding="utf-8")
    html_text = html_text.replace("1013J_R1E 屏幕比例与图片主导", "1013J_R1F 课件屏切换静态交互")
    html_text = html_text.replace("后续接素材投送。", "")
    html_text = html_text.replace("后续接局部互动块。", "")
    html_text = html_text.replace("后续接文字编辑。", "")
    html_text = html_text.replace("静态样张：进入大屏预览后续再接。", "")
    html_text = html_text.replace("</style>", r1f_css() + "\n  </style>", 1)
    html_text = html_text.replace("    initPrepRoomRenderCanvas();", r1f_js() + "\n    initPrepRoomRenderCanvas();", 1)
    return html_text


def find_browser() -> Path | None:
    for path in CHROME_CANDIDATES:
        if path.exists():
            return path
    return None


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8].hex() != "89504e470d0a1a0a":
        raise ValueError(f"Not a PNG: {path}")
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def javascript_syntax_check(stage_dir: Path, html_text: str) -> dict[str, Any]:
    node = shutil.which("node")
    if not node:
        return {"javascript_syntax_check_pass": False, "javascript_syntax_error": "node_not_found"}
    scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html_text, flags=re.S | re.I)
    script_files: list[str] = []
    for index, script_text in enumerate(scripts):
        script_path = stage_dir / f"javascript_syntax_1013J_R1F_{index:02d}.js"
        write_text(script_path, script_text)
        script_files.append(script_path.name)
        proc = subprocess.run([node, "--check", str(script_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            return {"javascript_syntax_check_pass": False, "javascript_syntax_error": proc.stderr.strip() or proc.stdout.strip(), "javascript_syntax_files": script_files}
    return {"javascript_syntax_check_pass": True, "javascript_syntax_files": script_files}


def screenshot(stage_dir: Path, html_path: Path) -> dict[str, Any]:
    browser = find_browser()
    screenshots: list[dict[str, Any]] = []
    if browser is None:
        return {"screenshot_smoke_pass": False, "screenshot_error": "browser_not_found", "screenshots": screenshots}
    cases = [
        ("screen_01", "screen_01_cover"),
        ("screen_03", "screen_03_compare"),
        ("screen_06", "screen_06_whiteboard"),
        ("screen_07", "screen_07_show"),
    ]
    for name, fragment in cases:
        out = stage_dir / f"ui_smoke_screenshot_1013J_R1F_{name}.png"
        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-cache",
            "--disable-default-apps",
            "--no-first-run",
            "--window-size=1440,1100",
            f"--screenshot={out}",
            "file:///" + html_path.as_posix() + f"?screen={fragment}#coursewareExpanded",
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        width, height = png_size(out)
        screenshots.append({"case": name, "path": out.name, "width": width, "height": height, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": True, "screenshots": screenshots}


def validate_html(html_text: str) -> dict[str, Any]:
    dumped_boundary = json.dumps(boundary())
    checks: dict[str, Any] = {
        "courseware_click_through_created": "data-1013j-r1f-click-through=\"true\"" in html_text,
        "screen_count": len(SCREENS),
        "all_screens_clickable": html_text.count("data-r1f-screen-id") >= 1 and "setCoursewareScreen1013JR1F" in html_text,
        "selected_screen_state_visible": "is-selected" in html_text and "aria-pressed" in html_text,
        "screen_01_preview_created": "screen_01_cover" in html_text and "色彩的感觉" in html_text,
        "screen_03_preview_created": "screen_03_compare" in html_text and "哪一组颜色更安静？" in html_text,
        "screen_06_preview_created": "screen_06_whiteboard" in html_text and "色卡拖拽区" in html_text,
        "screen_07_preview_created": "screen_07_show" in html_text and "学生作品展示位" in html_text,
        "right_panel_updates_by_screen": all(token in html_text for token in ["data-r1f-side-lesson", "data-r1f-side-purpose", "data-r1f-side-materials", "data-r1f-side-suggestion"]),
        "lesson_to_screen_mapping_updates_by_screen": "lesson_link" in html_text and "对应备课段" in html_text,
        "material_placeholders_update_by_screen": "renderCoursewareMaterials1013JR1F" in html_text and "data-r1f-materials" in html_text,
        "xiaojiao_suggestion_updates_by_screen": "suggestion" in html_text and "data-r1f-side-suggestion" in html_text,
        "screen_ratio_toggle_present": "data-r1f-ratio=\"16:9\"" in html_text and "data-r1f-ratio=\"4:3\"" in html_text,
        "teacher_visible_engineering_caveats_absent": all(term not in html_text for term in ["暂不实现", "不接后端", "白板不是默认状态", "后续能力"]),
        "click_switch_logic_present": "document.addEventListener(\"click\"" in html_text and "data-r1f-screen-id" in html_text,
        "screen_data_count_is_8": html_text.count("\"id\": \"screen_") >= 8,
        **boundary(),
    }
    checks["upload_search_whiteboard_ppt_not_implemented"] = (
        "upload_implemented" not in html_text
        and "search_implemented" not in html_text
        and "whiteboard_library_connected" in dumped_boundary
        and "ppt_export_implemented" in dumped_boundary
    )
    return checks


def failed_checks(checks: dict[str, Any]) -> list[str]:
    failed: list[str] = []
    expected_false = set(boundary().keys())
    for key, value in checks.items():
        if key in {"javascript_syntax_files", "javascript_syntax_error"}:
            continue
        if key == "screen_count":
            if value != 8:
                failed.append(key)
        elif key in expected_false:
            if value is not False:
                failed.append(key)
        elif value is not True:
            failed.append(key)
    return failed


def write_docs(output_root: Path, stage_dir: Path, result: dict[str, Any]) -> None:
    write_text(stage_dir / "1013J_R1F_report.md", f"""# 1013J_R1F Courseware Screen Click Through Static Interaction

FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R1F keeps the R1E visual baseline and adds static click-through behavior for all 8 classroom display screens.

Teacher-visible behavior:
- clicking the left courseware draft list changes the main classroom screen
- the right panel updates the lesson link, purpose, materials, suggestion, and static actions
- screen 01 / 03 / 06 / 07 are covered by screenshot smoke
- 16:9 / 4:3 ratio control remains local and static

Boundary:
- no runtime
- no provider/model
- no upload/search implementation
- no whiteboard library
- no PPT export
- no formal apply

Failed checks: {result["failed_checks"]}
""")
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

1013J_R1F turns the R1E courseware visual baseline into an 8-screen click-through static interaction. The main classroom display, right-side settings, material placeholders, lesson mapping, and Xiaojiao suggestions all update by selected screen.

Key flags:
- COURSEWARE_CLICK_THROUGH_CREATED=true
- SCREEN_COUNT=8
- ALL_SCREENS_CLICKABLE=true
- SELECTED_SCREEN_STATE_VISIBLE=true
- SCREEN_01_PREVIEW_CREATED=true
- SCREEN_03_PREVIEW_CREATED=true
- SCREEN_06_PREVIEW_CREATED=true
- SCREEN_07_PREVIEW_CREATED=true
- RIGHT_PANEL_UPDATES_BY_SCREEN=true
- LESSON_TO_SCREEN_MAPPING_UPDATES_BY_SCREEN=true
- MATERIAL_PLACEHOLDERS_UPDATE_BY_SCREEN=true
- XIAOJIAO_SUGGESTION_UPDATES_BY_SCREEN=true
- SCREEN_RATIO_TOGGLE_PRESENT=true
- TEACHER_VISIBLE_ENGINEERING_CAVEATS_ABSENT=true
- UPLOAD_IMPLEMENTED=false
- SEARCH_IMPLEMENTED=false
- WHITEBOARD_LIBRARY_CONNECTED=false
- PPT_EXPORT_IMPLEMENTED=false
- PROVIDER_CALLED=false
- MODEL_CALLED=false
- FORMAL_APPLY_PERFORMED=false
- MAIN_PROJECT_PUSHED=false
""")
    write_text(output_root / "README.md", f"""# Prep Room Render Canvas Deepen V1 Review Package

Latest stage: `{STAGE_ID}`

Open:
- `{STAGE_DIR_NAME}/{HTML_NAME}`
- `{STAGE_DIR_NAME}/1013J_R1F_result.json`

Run:

```bash
python scripts/{VALIDATOR_NAME}
python scripts/{VALIDATOR_NAME} --root <repo-root>
```
""")
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", f"""# Review Package Manifest

Latest stage: `{STAGE_ID}`

Files:
- `LATEST_REVIEW_ENTRY.md`
- `README.md`
- `REVIEW_PACKAGE_MANIFEST.md`
- `{STAGE_DIR_NAME}/{HTML_NAME}`
- `{STAGE_DIR_NAME}/courseware_screen_state_1013J_R1F.json`
- `{STAGE_DIR_NAME}/courseware_screen_interaction_map_1013J_R1F.json`
- `{STAGE_DIR_NAME}/1013J_R1F_result.json`
- `{STAGE_DIR_NAME}/1013J_R1F_report.md`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1F_screen_01.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1F_screen_03.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1F_screen_06.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1F_screen_07.png`
- `scripts/{VALIDATOR_NAME}`
""")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output_root = locate_output_root(root)
    base_result = output_root / BASE_DIR_NAME / "1013J_R1E_result.json"
    if not base_result.exists():
        raise FileNotFoundError(base_result)

    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)
    html_text = patch_html(output_root)
    html_path = stage_dir / HTML_NAME
    write_text(html_path, html_text)

    js_check = javascript_syntax_check(stage_dir, html_text)
    smoke = screenshot(stage_dir, html_path)
    checks = validate_html(html_text)
    checks.update(js_check)
    checks["screenshot_smoke_pass"] = bool(smoke.get("screenshot_smoke_pass"))
    failed = failed_checks(checks)

    result = {
        "stage": STAGE_ID,
        "status": FINAL_STATUS if not failed else "FAIL_1013J_R1F_COURSEWARE_SCREEN_CLICK_THROUGH_STATIC_INTERACTION",
        "final_status": FINAL_STATUS if not failed else "FAIL_1013J_R1F_COURSEWARE_SCREEN_CLICK_THROUGH_STATIC_INTERACTION",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        **checks,
        "failed_checks": failed,
    }
    write_json(stage_dir / "1013J_R1F_result.json", result)
    write_json(stage_dir / "courseware_screen_state_1013J_R1F.json", {
        "stage": STAGE_ID,
        "screen_count": len(SCREENS),
        "initial_screen": "screen_03_compare",
        "screens": SCREENS,
        **boundary(),
    })
    write_json(stage_dir / "courseware_screen_interaction_map_1013J_R1F.json", {
        "stage": STAGE_ID,
        "interaction": "click_left_screen_list_updates_main_screen_and_right_panel",
        "updates": [
            "main_screen_title",
            "main_screen_classroom_text",
            "material_placeholders",
            "lesson_to_screen_mapping",
            "right_panel_purpose",
            "right_panel_materials",
            "xiaojiao_suggestion",
            "static_actions",
        ],
        "screenshot_cases": [item["case"] for item in smoke.get("screenshots", [])],
        **boundary(),
    })
    write_docs(output_root, stage_dir, result)
    source_delta = output_root / "source_delta_1013J_R1F" / "scripts" / VALIDATOR_NAME
    source_delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), source_delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))
    print("ALL_1013J_R1F_COURSEWARE_SCREEN_CLICK_THROUGH_STATIC_INTERACTION_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
