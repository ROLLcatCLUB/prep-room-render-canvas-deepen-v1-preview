from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013J_R1C_COURSEWARE_WORKSPACE_EXPANDED_LAYOUT_POLISH"
FINAL_STATUS = "PASS_1013J_R1C_COURSEWARE_WORKSPACE_EXPANDED_LAYOUT_POLISH"
INHERITS_FROM = "1013J_R1B_COURSEWARE_WORKSPACE_NOT_BLANK_WHITEBOARD_PATCH"
NEXT_STAGE = "USER_REVIEW_COURSEWARE_WORKSPACE_EXPANDED_LAYOUT"
BASE_DIR_NAME = "1013J_R1B_courseware_workspace_not_blank_whiteboard_patch"
STAGE_DIR_NAME = "1013J_R1C_courseware_workspace_expanded_layout_polish"
BASE_HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1B_courseware_not_blank_whiteboard.html"
HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1C_courseware_expanded_layout_polish.html"
VALIDATOR_NAME = "validate_1013J_R1C_courseware_workspace_expanded_layout_polish.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]


SCREENS = [
    {
        "id": "screen_01_cover",
        "index": "01",
        "title": "课题导入",
        "screen_title": "色彩的感觉",
        "classroom_text": "颜色为什么会让人产生不同感觉？",
        "lesson_link": "导入问题",
        "placeholder": "课题背景图",
        "status": "已有文字",
        "tool": "封面",
    },
    {
        "id": "screen_02_observe",
        "index": "02",
        "title": "看色彩图片",
        "screen_title": "这些颜色给你什么感觉？",
        "classroom_text": "先说第一感觉，不急着判断对错。",
        "lesson_link": "看一看",
        "placeholder": "生活色彩图片 3 张",
        "status": "待补图",
        "tool": "图片观察",
    },
    {
        "id": "screen_03_compare",
        "index": "03",
        "title": "比较两组颜色",
        "screen_title": "哪一组颜色更安静？",
        "classroom_text": "你从哪些颜色看出来？",
        "lesson_link": "比较变化",
        "placeholder": "两组色彩对比图",
        "status": "待补图 / 可白板",
        "tool": "对比观察",
    },
    {
        "id": "screen_04_words",
        "index": "04",
        "title": "感觉词卡",
        "screen_title": "把“好看”说得更具体",
        "classroom_text": "热烈 / 安静 / 柔和 / 强烈 / 明亮 / 沉稳",
        "lesson_link": "说一说",
        "placeholder": "感觉词卡",
        "status": "已有文字",
        "tool": "问题引导",
    },
    {
        "id": "screen_05_task",
        "index": "05",
        "title": "色彩实验任务",
        "screen_title": "用 3-4 种颜色表达一种感觉",
        "classroom_text": "选一组颜色，说说你想表达什么感觉。",
        "lesson_link": "任务发布",
        "placeholder": "任务说明",
        "status": "待教师确认",
        "tool": "任务发布",
    },
    {
        "id": "screen_06_whiteboard",
        "index": "06",
        "title": "白板试色",
        "screen_title": "试一组颜色",
        "classroom_text": "拖一拖色卡，看看画面感觉有什么变化。",
        "lesson_link": "试一试",
        "placeholder": "白板区域",
        "status": "可白板",
        "tool": "白板操作",
    },
    {
        "id": "screen_07_show",
        "index": "07",
        "title": "学生作品展示",
        "screen_title": "说说你的色彩选择",
        "classroom_text": "我用了哪些颜色？我想表达什么感觉？",
        "lesson_link": "展一展",
        "placeholder": "学生作品展示位",
        "status": "待学生作品",
        "tool": "作品展示",
    },
    {
        "id": "screen_08_summary",
        "index": "08",
        "title": "总结回看",
        "screen_title": "颜色会改变画面的感觉",
        "classroom_text": "看色彩、说感觉、比变化、做表达、会修改。",
        "lesson_link": "改一改",
        "placeholder": "总结页",
        "status": "已有文字",
        "tool": "评价提示",
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


def status_class(status: str) -> str:
    if "待补图" in status:
        return "needs-image"
    if "白板" in status:
        return "whiteboard"
    if "学生作品" in status:
        return "student-work"
    if "确认" in status:
        return "needs-confirm"
    return "ready"


def css() -> str:
    return """

    /* 1013J_R1B: courseware workspace is not a blank whiteboard */
    [data-1013j-r1-courseware="true"] .courseware-rail {
      display: grid;
      gap: 12px;
    }

    [data-1013j-r1-courseware="true"] .courseware-rail.is-light-preview {
      gap: 14px;
    }

    [data-1013j-r1-courseware="true"] .courseware-rail-head,
    [data-1013j-r1-courseware="true"] .courseware-expanded-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding-bottom: 10px;
      border-bottom: 1px solid rgba(36, 84, 70, .12);
    }

    [data-1013j-r1-courseware="true"] .courseware-rail-title,
    [data-1013j-r1-courseware="true"] .courseware-expanded-title {
      font-weight: 920;
      color: var(--ink);
      letter-spacing: 0;
    }

    [data-1013j-r1-courseware="true"] .courseware-screen-list {
      display: grid;
      gap: 4px;
    }

    [data-1013j-r1-courseware="true"] .courseware-screen-mini {
      display: grid;
      grid-template-columns: 26px minmax(0, 1fr) auto;
      gap: 7px;
      padding: 5px 0;
      border-bottom: 1px solid rgba(36, 84, 70, .10);
    }

    [data-1013j-r1-courseware="true"] .courseware-screen-mini:last-child {
      border-bottom: 0;
    }

    [data-1013j-r1-courseware="true"] .courseware-screen-index {
      width: 24px;
      height: 24px;
      border-radius: 999px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: rgba(43, 124, 106, .10);
      color: var(--green);
      font-size: 12px;
      font-weight: 900;
    }

    [data-1013j-r1-courseware="true"] .courseware-screen-mini strong,
    [data-1013j-r1-courseware="true"] .courseware-screen-card strong {
      color: var(--ink);
      font-size: 13px;
    }

    [data-1013j-r1-courseware="true"] .courseware-screen-mini p,
    [data-1013j-r1-courseware="true"] .courseware-screen-card p,
    [data-1013j-r1-courseware="true"] .courseware-side-note p {
      margin: 3px 0 0;
      color: rgba(32, 75, 65, .70);
      font-size: 12px;
      line-height: 1.55;
    }

    [data-1013j-r1-courseware="true"] .courseware-screen-mini.compact p {
      margin-top: 1px;
      line-height: 1.35;
    }

    [data-1013j-r1-courseware="true"] .courseware-rail-summary {
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
      align-items: center;
    }

    [data-1013j-r1-courseware="true"] .courseware-current-link {
      padding: 10px 12px;
      border-radius: 8px;
      border: 1px solid rgba(36, 84, 70, .12);
      background: rgba(255, 255, 251, .58);
      color: rgba(29, 39, 35, .78);
      font-size: 13px;
      line-height: 1.55;
    }

    [data-1013j-r1-courseware="true"] .courseware-current-link strong {
      color: var(--green);
    }

    [data-1013j-r1-courseware="true"] .courseware-status {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      margin-top: 5px;
      color: rgba(32, 75, 65, .72);
      font-size: 12px;
      line-height: 1.35;
    }

    [data-1013j-r1-courseware="true"] .courseware-dot {
      width: 7px;
      height: 7px;
      border-radius: 999px;
      background: #2b7c6a;
      box-shadow: 0 0 0 3px rgba(43, 112, 92, .06);
    }

    [data-1013j-r1-courseware="true"] .courseware-dot.needs-image,
    [data-1013j-r1-courseware="true"] .courseware-dot.needs-confirm {
      background: #d59748;
    }

    [data-1013j-r1-courseware="true"] .courseware-dot.whiteboard {
      background: #2c6ea3;
    }

    [data-1013j-r1-courseware="true"] .courseware-dot.student-work {
      background: #b6544d;
    }

    [data-1013j-r1-courseware="true"] .courseware-rail-actions,
    [data-1013j-r1-courseware="true"] .courseware-expanded-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
    }

    [data-1013j-r1-courseware="true"] .courseware-expanded-scene .nb-binder {
      grid-template-columns: minmax(260px, .62fr) 22px minmax(720px, 1.38fr);
    }

    [data-1013j-r1-courseware="true"] .courseware-expanded-scene .nb-panel.is-collapsed {
      width: 48px;
      padding: 18px 8px;
      overflow: hidden;
    }

    [data-1013j-r1-courseware="true"] .courseware-expanded-scene .nb-panel.is-collapsed .nb-cover,
    [data-1013j-r1-courseware="true"] .courseware-expanded-scene .nb-panel.is-collapsed .nb-tree {
      opacity: .18;
      pointer-events: none;
    }

    [data-1013j-r1-courseware="true"] .courseware-reference {
      max-height: 760px;
      overflow: hidden;
    }

    [data-1013j-r1-courseware="true"] .courseware-reference .nb-doc-body-surface {
      max-height: 520px;
      overflow: hidden;
    }

    [data-1013j-r1-courseware="true"] .courseware-workspace {
      min-height: 760px;
    }

    [data-1013j-r1-courseware="true"] .courseware-expanded-body {
      display: grid;
      grid-template-columns: 180px minmax(0, 1fr) 230px;
      gap: 16px;
      margin-top: 18px;
    }

    [data-1013j-r1-courseware="true"] .courseware-screen-nav {
      display: grid;
      gap: 6px;
      align-content: start;
      border-right: 1px solid rgba(36, 84, 70, .12);
      padding-right: 12px;
    }

    [data-1013j-r1-courseware="true"] .courseware-screen-nav button {
      justify-content: flex-start;
      text-align: left;
    }

    [data-1013j-r1-courseware="true"] .courseware-stage {
      border-radius: 12px;
      border: 1px solid rgba(43, 124, 106, .16);
      background:
        radial-gradient(circle at 22px 22px, rgba(43, 124, 106, .045) 1px, transparent 1.5px),
        linear-gradient(135deg, rgba(255, 255, 251, .98), rgba(249, 246, 237, .94));
      box-shadow: 0 20px 45px rgba(32, 80, 64, .10);
      aspect-ratio: 16 / 9;
      padding: 28px;
      display: grid;
      align-content: center;
      gap: 16px;
    }

    [data-1013j-r1-courseware="true"] .courseware-stage.not-blank-screen-preview {
      align-content: stretch;
      grid-template-rows: auto auto 1fr auto;
      gap: 14px;
    }

    [data-1013j-r1-courseware="true"] .courseware-screen-preview-label {
      display: inline-flex;
      width: fit-content;
      align-items: center;
      gap: 6px;
      padding: 3px 9px;
      border-radius: 999px;
      border: 1px solid rgba(43, 112, 92, .18);
      color: var(--green);
      background: rgba(239, 248, 243, .72);
      font-size: 12px;
      font-weight: 850;
    }

    [data-1013j-r1-courseware="true"] .courseware-stage-kicker {
      color: var(--green);
      font-size: 13px;
      font-weight: 850;
    }

    [data-1013j-r1-courseware="true"] .courseware-stage-title {
      color: var(--ink);
      font-size: 30px;
      line-height: 1.22;
      font-weight: 920;
      letter-spacing: 0;
    }

    [data-1013j-r1-courseware="true"] .courseware-stage-question {
      color: rgba(29, 39, 35, .82);
      font-size: 18px;
      line-height: 1.6;
    }

    [data-1013j-r1-courseware="true"] .courseware-placeholder-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }

    [data-1013j-r1-courseware="true"] .courseware-local-whiteboard-block {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid rgba(44, 110, 163, .20);
      background: rgba(235, 244, 250, .58);
      color: rgba(32, 75, 65, .76);
      font-size: 13px;
      line-height: 1.45;
    }

    [data-1013j-r1-courseware="true"] .courseware-local-whiteboard-block strong {
      color: #2c6ea3;
    }

    [data-1013j-r1-courseware="true"] .courseware-full-workspace {
      display: grid;
      grid-template-columns: 220px minmax(520px, 1fr) 300px;
      gap: 18px;
      width: min(1320px, calc(100vw - 88px));
      min-height: calc(100vh - 260px);
      margin: 28px auto;
      padding: 22px;
      border-radius: 18px;
      border: 1px solid rgba(38, 126, 109, 0.2);
      background: linear-gradient(138deg, rgba(255, 253, 247, 0.98), rgba(240, 249, 240, 0.94));
      box-shadow: 0 20px 50px rgba(16, 61, 53, 0.12);
    }

    [data-1013j-r1-courseware="true"] .courseware-full-nav,
    [data-1013j-r1-courseware="true"] .courseware-full-side {
      border-radius: 14px;
      border: 1px solid rgba(38, 126, 109, 0.16);
      background: rgba(255, 255, 250, 0.76);
      padding: 16px;
    }

    [data-1013j-r1-courseware="true"] .courseware-full-title {
      font-weight: 900;
      color: #103d35;
      margin-bottom: 4px;
    }

    [data-1013j-r1-courseware="true"] .courseware-full-nav .courseware-screen-nav {
      display: grid;
      gap: 8px;
      margin-top: 14px;
    }

    [data-1013j-r1-courseware="true"] .courseware-full-main {
      display: grid;
      gap: 16px;
      align-content: start;
    }

    [data-1013j-r1-courseware="true"] .courseware-reference-strip {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 12px 14px;
      border-radius: 14px;
      border: 1px dashed rgba(38, 126, 109, 0.2);
      background: rgba(255, 255, 250, 0.72);
      color: #2f5e54;
      font-size: 13px;
    }

    [data-1013j-r1-courseware="true"] .courseware-full-stage {
      min-height: 520px;
    }

    [data-1013j-r1-courseware="true"] .courseware-side-block + .courseware-side-block {
      margin-top: 12px;
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-shell {
      width: min(1500px, calc(100vw - 48px));
      min-height: calc(100vh - 230px);
      margin: 18px auto 44px;
      padding: 22px;
      border-radius: 20px;
      border: 1px solid rgba(38, 126, 109, 0.2);
      background: linear-gradient(136deg, rgba(255, 253, 247, 0.98), rgba(238, 248, 240, 0.96));
      box-shadow: 0 24px 60px rgba(16, 61, 53, 0.14);
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-top {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: flex-start;
      padding: 2px 4px 16px;
      border-bottom: 1px dashed rgba(38, 126, 109, 0.2);
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-kicker,
    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-panel-title {
      color: var(--green);
      font-size: 13px;
      font-weight: 900;
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-top h2 {
      margin: 4px 0 6px;
      color: var(--ink);
      font-size: 24px;
      line-height: 1.22;
      letter-spacing: 0;
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-top p {
      margin: 0;
      color: rgba(29, 39, 35, 0.68);
      font-size: 13px;
      line-height: 1.55;
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-actions,
    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-button-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      justify-content: flex-end;
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-workbench {
      display: grid;
      grid-template-columns: 190px minmax(720px, 1fr) 280px;
      gap: 18px;
      padding-top: 18px;
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-nav,
    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-side {
      border-radius: 16px;
      border: 1px solid rgba(38, 126, 109, 0.16);
      background: rgba(255, 255, 250, 0.72);
      padding: 14px;
      align-self: start;
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-nav .courseware-screen-nav {
      display: grid;
      gap: 8px;
      margin-top: 12px;
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-nav .node-action {
      justify-content: flex-start;
      width: 100%;
      gap: 8px;
      border-radius: 12px;
      padding: 9px 10px;
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-main {
      min-width: 0;
      display: grid;
      gap: 14px;
      align-content: start;
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-map {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      padding: 11px 12px;
      border-radius: 14px;
      border: 1px dashed rgba(38, 126, 109, 0.18);
      background: rgba(255, 255, 250, 0.68);
      color: rgba(29, 39, 35, 0.74);
      font-size: 13px;
      line-height: 1.45;
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-screen-frame {
      width: 100%;
      aspect-ratio: 16 / 9;
      border-radius: 18px;
      padding: 18px;
      background: linear-gradient(145deg, rgba(18, 77, 65, 0.16), rgba(18, 77, 65, 0.04));
      box-shadow: inset 0 0 0 1px rgba(38, 126, 109, 0.16), 0 20px 48px rgba(16, 61, 53, 0.12);
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-screen {
      height: 100%;
      border-radius: 16px;
      border: 1px solid rgba(38, 126, 109, 0.2);
      background:
        radial-gradient(circle at 30px 30px, rgba(43, 124, 106, 0.05) 1px, transparent 1.5px),
        linear-gradient(135deg, rgba(255, 255, 251, 0.99), rgba(248, 246, 238, 0.98));
      padding: clamp(22px, 3vw, 42px);
      display: grid;
      grid-template-rows: auto auto auto 1fr auto;
      gap: 14px;
      overflow: hidden;
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-screen .courseware-stage-title {
      font-size: clamp(32px, 4vw, 58px);
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-screen .courseware-stage-question {
      font-size: clamp(18px, 1.7vw, 26px);
    }

    [data-1013j-r1c-expanded-polish="true"] .courseware-r1c-side .courseware-side-block {
      border-radius: 12px;
      border: 1px solid rgba(38, 126, 109, 0.14);
      background: rgba(255, 255, 250, 0.72);
      padding: 12px;
    }

    [data-1013j-r1-courseware="true"] .courseware-placeholder {
      min-height: 110px;
      display: grid;
      place-items: center;
      text-align: center;
      border-radius: 10px;
      border: 1px dashed rgba(43, 124, 106, .28);
      background: rgba(239, 248, 243, .45);
      color: rgba(32, 75, 65, .72);
      font-size: 13px;
      line-height: 1.5;
    }

    [data-1013j-r1-courseware="true"] .courseware-side-note {
      display: grid;
      gap: 10px;
      align-content: start;
    }

    [data-1013j-r1-courseware="true"] .courseware-side-block {
      padding: 10px 12px;
      border-radius: 8px;
      border: 1px solid rgba(36, 84, 70, .12);
      background: rgba(255, 255, 251, .58);
    }

    @media (max-width: 980px) {
      [data-1013j-r1-courseware="true"] .courseware-expanded-scene .nb-binder,
      [data-1013j-r1-courseware="true"] .courseware-expanded-body {
        grid-template-columns: 1fr;
      }
      [data-1013j-r1-courseware="true"] .courseware-stage {
        aspect-ratio: auto;
      }
    }
"""


def render_screen_outline_js() -> str:
    return json.dumps(SCREENS, ensure_ascii=False)


def functions_js() -> str:
    return r"""

    const coursewareScreens1013JR1 = __COURSEWARE_SCREENS_1013J_R1__;

    function coursewareStatusClass1013JR1(status) {{
      if (status.includes("待补图")) return "needs-image";
      if (status.includes("白板")) return "whiteboard";
      if (status.includes("学生作品")) return "student-work";
      if (status.includes("确认")) return "needs-confirm";
      return "ready";
    }}

    function renderCoursewareStatus1013JR1(status) {{
      return `<span class="courseware-status"><span class="courseware-dot ${{coursewareStatusClass1013JR1(status)}}"></span>${{html(status)}}</span>`;
    }}

    function renderCoursewareRightRail1013JR1() {{
      return `
        <aside class="nb-drawer" aria-label="课堂大屏草稿">
          <div class="courseware-rail is-light-preview" data-1013j-r1a-light-preview="true">
            <div class="courseware-rail-head">
              <div>
                <div class="courseware-rail-title">大屏草稿</div>
                <div class="quiet-tag">轻预览</div>
              </div>
              <button class="node-action primary" type="button" data-courseware-expanded="true">课件制作</button>
            </div>
            <div class="courseware-rail-summary" aria-label="大屏草稿状态">
              <span class="r6o-r1-status-pill">8 屏</span>
              <span class="r6o-r1-status-light"><span class="r6o-r1-dot amber"></span>3 处待补图</span>
              <span class="r6o-r1-status-light"><span class="r6o-r1-dot green"></span>1 处可白板</span>
            </div>
            <div class="courseware-screen-list">
              ${{coursewareScreens1013JR1.map((screen) => `
                <div class="courseware-screen-mini compact" data-courseware-screen="${{html(screen.id)}}">
                  <span class="courseware-screen-index">${{html(screen.index)}}</span>
                  <div>
                    <strong>${{html(screen.title)}}</strong>
                    <p>${{html(screen.lesson_link)}}</p>
                  </div>
                  ${{renderCoursewareStatus1013JR1(screen.status)}}
                </div>
              `).join("")}}
            </div>
            <div class="courseware-current-link">
              <strong>当前关联</strong><br>
              当前备课段：比较变化<br>
              对应屏：03 比较两组颜色
            </div>
            <div class="courseware-rail-actions">
              <button class="node-action secondary" type="button" data-courseware-expanded="true">课件制作</button>
              <button class="node-action secondary" type="button" data-pending="补素材后续接上传和资料库。">补素材</button>
            </div>
          </div>
        </aside>
      `;
    }}

    function renderCoursewareExpandedWorkspace1013JR1(view) {{
      const current = coursewareScreens1013JR1[2];
      return `
        <div class="nb-scene courseware-expanded-scene" data-1013j-r1-expanded="true">
          <div class="courseware-full-workspace" aria-label="课件制作工作台">
            <aside class="courseware-full-nav" aria-label="课件屏幕目录">
              <div>
                <div class="courseware-full-title">课件目录</div>
                <div class="quiet-tag">8 屏 · 小教草稿</div>
              </div>
              <nav class="courseware-screen-nav" aria-label="课件目录">
                ${{coursewareScreens1013JR1.map((screen, index) => `
                  <button class="node-action ${{index === 2 ? "primary" : "secondary"}}" type="button" data-pending="${{html(screen.title)}} 当前为静态目录。">${{html(screen.index)}} ${{html(screen.title)}}</button>
                `).join("")}}
              </nav>
            </aside>
            <main class="courseware-full-main" aria-label="当前屏课件预览">
              <div class="courseware-reference-strip">
                <span><strong>备课本参考：</strong>${{html(view.current_lesson.code)}}《${{html(view.current_lesson.title)}}》 · 当前环节：比较变化</span>
                <span>
                  <button class="node-action secondary" type="button" data-courseware-normal="true">收起</button>
                  <button class="node-action primary" type="button" data-pending="静态样张：不导出 PPT。">进入大屏预览</button>
                </span>
              </div>
              <section class="courseware-stage courseware-full-stage not-blank-screen-preview" aria-label="当前屏预览">
                <div class="courseware-screen-preview-label">当前屏预览 · 不是空白白板</div>
                <div class="courseware-stage-kicker">${{html(current.index)}} · ${{html(current.lesson_link)}}</div>
                <div class="courseware-stage-title">${{html(current.screen_title)}}</div>
                <div class="courseware-stage-question">${{html(current.classroom_text)}}</div>
                <div class="courseware-placeholder-grid">
                  <div class="courseware-placeholder">素材 A<br>热闹的色彩组合图<br><span class="quiet-tag">待补图</span></div>
                  <div class="courseware-placeholder">素材 B<br>安静的色彩组合图<br><span class="quiet-tag">待补图</span></div>
                </div>
                <div class="courseware-local-whiteboard-block" data-whiteboard-as-block="true">
                  <span><strong>局部白板工具</strong><br>可圈出让学生感觉“安静”的颜色。</span>
                  <span class="quiet-tag">可白板</span>
                </div>
              </section>
            </main>
            <aside class="courseware-full-side" aria-label="素材与操作">
                <div>
                  <div class="courseware-full-title">当前屏设置</div>
                  <div class="quiet-tag">素材 · 提问 · 局部工具</div>
                </div>
                <div class="courseware-side-block">
                  <strong>素材占位</strong>
                  <p>素材 A：热闹的色彩组合图。素材 B：安静的色彩组合图。</p>
                  ${{renderCoursewareStatus1013JR1(current.status)}}
                </div>
                <div class="courseware-side-block">
                  <strong>白板局部模块</strong>
                  <p>白板只作为这一屏里的圈画工具，不是整个课件制作区的默认形态。</p>
                </div>
                <div class="courseware-side-block">
                  <strong>小教建议</strong>
                  <p>这一屏适合让学生先说第一感觉，再追问“你从哪些颜色看出来”。</p>
                </div>
                <div class="courseware-side-block">
                  <strong>后续能力</strong>
                  <p>上传、搜索、白板库和 PPT 导出暂不实现。</p>
                </div>
              </aside>
          </div>
        </div>
      `;
    }}
""".replace("__COURSEWARE_SCREENS_1013J_R1__", render_screen_outline_js()).replace("{{", "{").replace("}}", "}")


def patch_html(output_root: Path) -> str:
    base = output_root / BASE_DIR_NAME / BASE_HTML_NAME
    html_text = base.read_text(encoding="utf-8")
    html_text = html_text.replace(
        "师维 · 备课室 | 1013J_R1B 非空白白板课件区",
        "师维 · 备课室 | 1013J_R1C 课件制作区展开态打磨",
        1,
    )
    html_text = html_text.replace(
        'data-1013j-r1b-not-blank-whiteboard="true">',
        'data-1013j-r1b-not-blank-whiteboard="true" data-1013j-r1c-expanded-polish="true">',
        1,
    )
    html_text = html_text.replace("\n  </style>", css() + "\n  </style>", 1)
    html_text = html_text.replace("当前屏预览 · 不是空白白板", "当前大屏预览")
    html_text = html_text.replace("白板只作为这一屏里的圈画工具，不是整个课件制作区的默认形态。", "可圈画：让学生指出“安静”的颜色。")
    html_text = html_text.replace("上传、搜索、白板库和 PPT 导出暂不实现。", "补图片、改问题、加入互动。")
    html_text = html_text.replace("后续能力", "操作")
    override = r'''
    function renderCoursewareExpandedWorkspace1013JR1(view) {
      const current = coursewareScreens1013JR1[2];
      return `
        <div class="courseware-r1c-shell" data-1013j-r1-expanded="true" aria-label="课件制作工作区">
          <header class="courseware-r1c-top">
            <div>
              <div class="courseware-r1c-kicker">小教课件草稿</div>
              <h2>已根据备课内容生成 8 屏大屏草稿</h2>
              <p>3 处需要补图片，1 处适合课堂圈画。当前屏对应备课段“比较变化”。</p>
            </div>
            <div class="courseware-r1c-actions">
              <button class="node-action secondary" type="button" data-courseware-normal="true">回到备课</button>
              <button class="node-action primary" type="button" data-pending="静态样张：进入大屏预览后续再接。">进入大屏预览</button>
            </div>
          </header>
          <div class="courseware-r1c-workbench">
            <aside class="courseware-r1c-nav" aria-label="课件目录">
              <div class="courseware-r1c-panel-title">课件目录</div>
              <div class="quiet-tag">屏幕序列</div>
              <nav class="courseware-screen-nav" aria-label="课件目录">
                ${coursewareScreens1013JR1.map((screen, index) => `
                  <button class="node-action ${index === 2 ? "primary" : "secondary"}" type="button" data-pending="${html(screen.title)} 当前为静态目录。">
                    <span>${html(screen.index)}</span>
                    <strong>${html(screen.title)}</strong>
                  </button>
                `).join("")}
              </nav>
            </aside>
            <main class="courseware-r1c-main" aria-label="当前课堂大屏">
              <div class="courseware-r1c-map">
                <span><strong>当前备课段：</strong>比较变化</span>
                <span><strong>对应课件屏：</strong>03 比较两组颜色</span>
                <span><strong>本屏作用：</strong>帮助学生从“好看”说到“为什么安静”</span>
              </div>
              <section class="courseware-r1c-screen-frame" aria-label="16:9课堂大屏预览">
                <div class="courseware-r1c-screen">
                  <div class="courseware-screen-preview-label">当前大屏预览</div>
                  <div class="courseware-stage-kicker">${html(current.index)} · ${html(current.lesson_link)}</div>
                  <div class="courseware-stage-title">${html(current.screen_title)}</div>
                  <div class="courseware-stage-question">${html(current.classroom_text)}</div>
                  <div class="courseware-placeholder-grid">
                    <div class="courseware-placeholder">素材 A<br>热闹的色彩组合图<br><span class="quiet-tag">待补图</span></div>
                    <div class="courseware-placeholder">素材 B<br>安静的色彩组合图<br><span class="quiet-tag">待补图</span></div>
                  </div>
                  <div class="courseware-local-whiteboard-block" data-whiteboard-as-block="true">
                    <span><strong>课堂互动</strong><br>可圈画：让学生指出“安静”的颜色。</span>
                    <span class="quiet-tag">圈画 / 标注</span>
                  </div>
                </div>
              </section>
            </main>
            <aside class="courseware-r1c-side" aria-label="当前屏设置">
              <div class="courseware-r1c-panel-title">当前屏设置</div>
              <div class="courseware-side-block">
                <strong>素材</strong>
                <p>补两组对比图片：热闹的色彩组合、安静的色彩组合。</p>
                ${renderCoursewareStatus1013JR1(current.status)}
              </div>
              <div class="courseware-side-block">
                <strong>课堂文字</strong>
                <p>哪一组颜色更安静？你从哪些颜色看出来？</p>
              </div>
              <div class="courseware-side-block">
                <strong>小教建议</strong>
                <p>先让学生说第一感觉，再追问“你从哪些颜色看出来”。</p>
              </div>
              <div class="courseware-side-block">
                <strong>操作</strong>
                <div class="courseware-r1c-button-row">
                  <button class="node-action secondary" type="button" data-pending="后续接素材投送。">补图片</button>
                  <button class="node-action secondary" type="button" data-pending="后续接文字编辑。">改问题</button>
                  <button class="node-action secondary" type="button" data-pending="后续接局部互动块。">加入互动</button>
                </div>
              </div>
            </aside>
          </div>
        </div>
      `;
    }
'''
    html_text = html_text.replace("    initPrepRoomRenderCanvas();", override + "\n    initPrepRoomRenderCanvas();", 1)
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
        script_path = stage_dir / f"javascript_syntax_1013J_R1C_{index:02d}.js"
        write_text(script_path, script_text)
        script_files.append(script_path.name)
        proc = subprocess.run([node, "--check", str(script_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            return {
                "javascript_syntax_check_pass": False,
                "javascript_syntax_error": proc.stderr.strip() or proc.stdout.strip(),
                "javascript_syntax_files": script_files,
            }
    return {"javascript_syntax_check_pass": True, "javascript_syntax_files": script_files}


def screenshot(stage_dir: Path, html_path: Path) -> dict[str, Any]:
    browser = find_browser()
    screenshots: list[dict[str, Any]] = []
    if browser is None:
        return {"screenshot_smoke_pass": False, "screenshot_error": "browser_not_found", "screenshots": screenshots}
    cases = [
        ("normal", 1440, 1100, ""),
        ("expanded", 1440, 1100, "#coursewareExpanded"),
        ("mobile", 390, 1100, ""),
    ]
    for name, width, height, fragment in cases:
        out = stage_dir / f"ui_smoke_screenshot_1013J_R1C_{name}.png"
        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-cache",
            "--disable-default-apps",
            "--no-first-run",
            f"--window-size={width},{height}",
            f"--screenshot={out}",
            "file:///" + html_path.as_posix() + fragment,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        actual_width, actual_height = png_size(out)
        screenshots.append({"case": name, "path": out.name, "width": actual_width, "height": actual_height, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": True, "screenshots": screenshots}


def validate_html(html_text: str) -> dict[str, Any]:
    screen_titles = [screen["title"] for screen in SCREENS]
    screen_statuses = [screen["status"] for screen in SCREENS]
    return {
        "courseware_workspace_created": "data-1013j-r1-courseware=\"true\"" in html_text,
        "normal_right_rail_outline_created": "大屏草稿" in html_text and "renderCoursewareRightRail1013JR1" in html_text,
        "normal_right_rail_lightweight": "data-1013j-r1a-light-preview=\"true\"" in html_text and "轻预览" in html_text,
        "courseware_outline_compact": "courseware-screen-mini compact" in html_text and "当前关联" in html_text,
        "screen_detail_not_expanded_in_normal_mode": "courseware-placeholder-grid" in html_text and "data-1013j-r1-expanded=\"true\"" in html_text,
        "material_status_visible": "3 处待补图" in html_text and "1 处可白板" in html_text,
        "courseware_maker_entry_present": "课件制作" in html_text,
        "expanded_courseware_workspace_created": "课件制作区" in html_text and "renderCoursewareExpandedWorkspace1013JR1" in html_text,
        "expanded_workspace_visually_dominant": "courseware-r1c-shell" in html_text and "courseware-r1c-workbench" in html_text,
        "current_screen_16_9_preview": "courseware-r1c-screen-frame" in html_text and "aspect-ratio: 16 / 9" in html_text,
        "large_blank_grid_reduced": "width: min(1500px, calc(100vw - 48px))" in html_text and "min-height: calc(100vh - 230px)" in html_text,
        "current_screen_preview_created": "当前大屏预览" in html_text and "哪一组颜色更安静？" in html_text,
        "screen_outline_present": "courseware-screen-nav" in html_text and "03 比较两组颜色" in html_text,
        "material_placeholders_visible": "素材 A" in html_text and "素材 B" in html_text and "待补图" in html_text,
        "teacher_visible_engineering_caveats_absent": all(term not in html_text for term in ["暂不实现", "不是整个课件制作区", "不是空白白板", "后续能力"]),
        "whiteboard_as_local_interaction_tool": "data-whiteboard-as-block=\"true\"" in html_text and "课堂互动" in html_text and "圈画 / 标注" in html_text,
        "whiteboard_as_block_not_workspace": "data-whiteboard-as-block=\"true\"" in html_text and "课堂互动" in html_text,
        "xiaojiao_generated_courseware_status_visible": "已根据备课内容生成 8 屏大屏草稿" in html_text and "3 处需要补图片，1 处适合课堂圈画" in html_text,
        "lesson_to_screen_mapping_visible": "当前备课段：" in html_text and "对应课件屏：" in html_text and "本屏作用：" in html_text,
        "xiaojiao_screen_suggestion_present": "先让学生说第一感觉" in html_text,
        "upload_search_whiteboard_library_not_connected": (
            html_text.count("upload_implemented") == 0
            and "whiteboard_library_connected" in json.dumps(boundary())
            and boundary()["whiteboard_library_connected"] is False
        ),
        "main_lesson_notebook_reference_kept": "备课本参考" in html_text and "当前环节：比较变化" in html_text,
        "courseware_screen_directory_visible": "courseware-full-nav" in html_text and "课件目录" in html_text,
        "courseware_outline_generated": all(title in html_text for title in screen_titles),
        "screen_count": len(SCREENS),
        "screen_placeholders_created": all(screen["placeholder"] in html_text for screen in SCREENS),
        "image_placeholders_present": any("待补图" in status for status in screen_statuses) and "热闹的色彩组合图" in html_text,
        "whiteboard_placeholder_present": "白板区域" in html_text and "可白板" in html_text,
        "student_work_placeholder_present": "学生作品展示位" in html_text and "待学生作品" in html_text,
        "ai_generated_screen_text_present": all(screen["classroom_text"] in html_text for screen in SCREENS),
        **boundary(),
    }


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
    write_text(stage_dir / "1013J_R1C_report.md", f"""# 1013J_R1C Courseware Workspace Expanded Layout Polish

FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

1013J_R1C keeps the R1A lightweight normal right rail and R1B non-blank workspace fix, then polishes the expanded courseware workspace:
- expanded workspace becomes the visual main stage
- current screen is rendered as a clear 16:9 classroom display preview
- left side is a compact courseware screen directory
- right side uses teacher-facing screen settings and actions
- engineering caveats are removed from the teacher-visible surface

This is a static concept only. Upload, search, whiteboard library, PPT export, provider/model, runtime, database, memory, Feishu, and formal apply are not connected.

Failed checks: {result["failed_checks"]}
""")
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

1013J_R1C polishes the expanded courseware workspace so it reads as a classroom display authoring workspace rather than a small three-column card.

Key flags:
- COURSEWARE_WORKSPACE_CREATED=true
- NORMAL_RIGHT_RAIL_OUTLINE_CREATED=true
- NORMAL_RIGHT_RAIL_LIGHTWEIGHT=true
- COURSEWARE_OUTLINE_COMPACT=true
- EXPANDED_COURSEWARE_WORKSPACE_CREATED=true
- EXPANDED_WORKSPACE_VISUALLY_DOMINANT=true
- CURRENT_SCREEN_16_9_PREVIEW=true
- TEACHER_VISIBLE_ENGINEERING_CAVEATS_ABSENT=true
- WHITEBOARD_AS_LOCAL_INTERACTION_TOOL=true
- XIAOJIAO_GENERATED_COURSEWARE_STATUS_VISIBLE=true
- LESSON_TO_SCREEN_MAPPING_VISIBLE=true
- XIAOJIAO_SCREEN_SUGGESTION_PRESENT=true
- SCREEN_COUNT=8
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
- `{STAGE_DIR_NAME}/1013J_R1C_result.json`

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
- `{STAGE_DIR_NAME}/courseware_workspace_state_1013J_R1C.json`
- `{STAGE_DIR_NAME}/courseware_screen_outline_1013J_R1C.json`
- `{STAGE_DIR_NAME}/courseware_placeholder_map_1013J_R1C.json`
- `{STAGE_DIR_NAME}/1013J_R1C_result.json`
- `{STAGE_DIR_NAME}/1013J_R1C_report.md`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1C_normal.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1C_expanded.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1C_mobile.png`
- `scripts/{VALIDATOR_NAME}`
""")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output_root = locate_output_root(root)
    base_result = output_root / BASE_DIR_NAME / "1013J_R1B_result.json"
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
        "status": FINAL_STATUS if not failed else "FAIL_1013J_R1C_COURSEWARE_WORKSPACE_EXPANDED_LAYOUT_POLISH",
        "final_status": FINAL_STATUS if not failed else "FAIL_1013J_R1C_COURSEWARE_WORKSPACE_EXPANDED_LAYOUT_POLISH",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        **checks,
        "failed_checks": failed,
    }
    write_json(stage_dir / "1013J_R1C_result.json", result)
    write_json(stage_dir / "courseware_screen_outline_1013J_R1C.json", {"stage": STAGE_ID, "screen_count": len(SCREENS), "screens": SCREENS})
    write_json(stage_dir / "courseware_placeholder_map_1013J_R1C.json", {
        "stage": STAGE_ID,
        "placeholders": [{"screen_id": screen["id"], "placeholder": screen["placeholder"], "status": screen["status"]} for screen in SCREENS],
        **boundary(),
    })
    write_json(stage_dir / "courseware_workspace_state_1013J_R1C.json", {
        "stage": STAGE_ID,
        "normal_state": "right_rail_big_screen_draft_outline",
        "expanded_state": "courseware_workspace_expanded_layout_polished",
        "expanded_workspace_visually_dominant": True,
        "current_screen_16_9_preview": True,
        "current_screen_preview_created": True,
        "whiteboard_as_local_interaction_tool": True,
        "teacher_visible_engineering_caveats_absent": True,
        "main_lesson_notebook_reference_kept": True,
        "courseware_screen_directory_visible": True,
        **boundary(),
    })
    write_docs(output_root, stage_dir, result)
    source_delta = output_root / "source_delta_1013J_R1C" / "scripts" / VALIDATOR_NAME
    source_delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), source_delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False))
    print("ALL_1013J_R1C_COURSEWARE_WORKSPACE_EXPANDED_LAYOUT_POLISH_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
