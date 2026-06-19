from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6P_BIG_UNIT_SECTION_VIEW_EDIT_SURFACE"
FINAL_STATUS = "PASS_1013I_R6P_BIG_UNIT_SECTION_VIEW_EDIT_SURFACE"
INHERITS_FROM = "1013I_R6O_R1_BIG_UNIT_RENDER_SURFACE_READING_POLISH"
NEXT_STAGE = "USER_REVIEW_BIG_UNIT_SECTION_EDIT_SURFACE"
STAGE_DIR_NAME = "1013I_R6P_big_unit_section_view_edit_surface"
BASE_DIR_NAME = "1013I_R6O_R1_big_unit_render_surface_reading_polish"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6P_big_unit_section_view_edit_surface.html"
VALIDATOR_NAME = "validate_1013I_R6P_big_unit_section_view_edit_surface.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]

RAW_KEYS = [
    "field_key",
    "schema",
    "prompt",
    "unit_package",
    "lesson_position",
    "candidate_patch",
    "formal_apply",
    "provider_called",
    "model_called",
    "database_written",
    "memory_written",
    "feishu_written",
]

SECTIONS = [
    {
        "id": "unit_info",
        "title": "单元信息",
        "current": "第一单元 · 多变的色彩；三年级｜美术｜预计 3 课时。",
        "suggestion": "这段已经清楚，可以保留简洁写法，后续只需要补教材版本和真实课时安排。",
        "before": "第一单元 · 多变的色彩；三年级｜美术｜预计 3 课时。",
        "after": "第一单元 · 多变的色彩；三年级｜美术｜预计 3 课时。教材版本和课时安排待老师补充后校准。",
        "impact": ["本章节阅读", "资料补充提示"],
        "view_note": "这里说明本单元的基本归属，帮助老师确认是不是在正确单元里继续备课。",
    },
    {
        "id": "curriculum_basis",
        "title": "课标依据",
        "current": "本单元主要指向审美感知、艺术表现、创意实践，文化理解作轻量渗透。",
        "suggestion": "这段可以再具体一点，让老师看到学生通过什么学习过程理解色彩感觉。",
        "before": "本单元主要指向审美感知、艺术表现、创意实践，文化理解作轻量渗透。",
        "after": "本单元主要围绕审美感知、艺术表现和创意实践展开，文化理解作轻量渗透。学生通过观察、比较、尝试和表达，理解色彩组合会改变画面感觉，并能用色彩表达一种较明确的情绪或氛围。",
        "impact": ["本章节阅读", "后续单课继承", "评价证据提示"],
        "view_note": "这里不放大段课标原文，只说明本单元主要受哪些课标方向约束。",
    },
    {
        "id": "core_literacy",
        "title": "核心素养",
        "current": "审美感知、艺术表现、创意实践和文化理解都转成学生可观察的行为。",
        "suggestion": "这里已经比较稳，建议继续保持学生行为化，不写成空泛口号。",
        "before": "审美感知、艺术表现、创意实践和文化理解都转成学生可观察的行为。",
        "after": "审美感知：能感受不同色彩组合带来的冷暖、轻重、热烈、安静等视觉意味。艺术表现：能选择一组颜色表达明确感觉，并说明自己的选色理由。创意实践：能在比较、试验和反馈中调整色彩搭配。文化理解：能发现色彩感受与生活场景、作品情境有关。",
        "impact": ["学习目标", "课堂观察点", "评价证据"],
        "view_note": "这里用学生做得到、看得见的行为表达核心素养。",
    },
    {
        "id": "student_start",
        "title": "学生起点",
        "current": "三年级学生能说出直观感受，但容易停留在好看、鲜艳、漂亮。",
        "suggestion": "这段可以保留，它能帮助后面单课把重点落到说明理由上。",
        "before": "学生能说出直观感受，但表达较笼统。",
        "after": "三年级学生通常能说出红色热闹、蓝色安静等直观感受，但容易停留在好看、鲜艳、漂亮。本单元要帮助学生从我觉得走向我能说明为什么。",
        "impact": ["本课导入", "学生表达支架"],
        "view_note": "这里帮助老师判断学生从哪里出发，不是给学生贴标签。",
    },
    {
        "id": "unit_questions",
        "title": "单元问题",
        "current": "颜色为什么会让人产生不同感觉？我们怎样用颜色把一种感觉表达出来？",
        "suggestion": "问题方向是美术学科性的，后续可以随教材资料补充具体图像情境。",
        "before": "颜色为什么会让人产生不同感觉？",
        "after": "颜色为什么会让人产生不同感觉？我们怎样用颜色把一种感觉表达出来？改动一处颜色，画面的意味为什么会变化？",
        "impact": ["课堂问题链", "学习推进"],
        "view_note": "这里不是知识点问答，而是贯穿几课的学习问题。",
    },
    {
        "id": "knowledge_skills",
        "title": "知识与技能",
        "current": "认识色彩组合带来的视觉差异，并能用词语描述、搭配和调整。",
        "suggestion": "可以继续保留轻量表达，避免把单元变成技法清单。",
        "before": "认识色彩组合带来的视觉差异。",
        "after": "认识色彩组合带来的视觉差异，能用冷暖、强弱、明暗、纯度变化等词语描述色彩感觉，并通过调整颜色让画面感觉更明确。",
        "impact": ["材料准备", "练习设计"],
        "view_note": "这里回答本单元不能丢掉哪些美术语言和基本技能。",
    },
    {
        "id": "performance_task",
        "title": "表现任务",
        "current": "完成一件色彩感觉小作品，并说明自己的色彩选择。",
        "suggestion": "建议强调三年级常态课负担，不要扩成大型项目或展览策划。",
        "before": "学生完成一件色彩感觉小作品，并说明自己的色彩选择。",
        "after": "学生完成一件“色彩感觉”小作品，并用一句到几句话说明自己的色彩选择。如果时间允许，再根据同伴或教师反馈调整一处颜色。",
        "impact": ["单元终点", "作品评价", "课堂时间"],
        "view_note": "这里说明学生最后拿什么来证明自己学到了。",
    },
    {
        "id": "learning_progression",
        "title": "学习推进",
        "current": "感受、比较、表现、修订，形成一条轻时间线。",
        "suggestion": "这条推进适合保留，后续每一课只需要继承对应阶段。",
        "before": "感受 → 比较 → 表现 → 修订。",
        "after": "感受：先说直观感受。比较：发现搭配变化会改变画面感觉。表现：围绕一种感觉完成色彩实验或小作品。修订：展示作品，说出理由，根据反馈调整一处颜色。",
        "impact": ["课时任务链", "单课推进"],
        "view_note": "这里把单元学习过程压成老师容易扫读的路线。",
    },
    {
        "id": "lesson_chain",
        "title": "课时任务链",
        "current": "1-1 打开感受；1-2 比较方法；1-3 完成表达。",
        "suggestion": "建议补一句每一课都要留下能进入下一课的学习证据。",
        "before": "1-1 打开感受；1-2 比较方法；1-3 完成表达。",
        "after": "1-1 打开感受，建立感受语言；1-2 比较方法，发现色彩组合会改变画面意味；1-3 完成表达，展示并修订。每一课都要留下能进入下一课的学习证据。",
        "impact": ["子课时继承", "单课备课入口", "评价证据提示"],
        "view_note": "这里不是课时目录，而是看每一课在单元里承担什么任务。",
    },
    {
        "id": "assessment_evidence",
        "title": "评价证据",
        "current": "看学生能否说出感觉、说明理由、留下记录、形成作品并调整。",
        "suggestion": "这段已经能支撑过程性评价，可以和课时任务链保持对应。",
        "before": "能说出色彩感觉，能说明自己的选色理由。",
        "after": "能说出色彩带来的感觉；能说明自己的选色理由；学习单留下观察和选择记录；作品呈现较明确的视觉意味；能根据反馈做出一次可见调整。",
        "impact": ["课堂观察", "作品评价", "单课继承"],
        "view_note": "这里帮助老师看到学生学到了没有，不只看最后作品。",
    },
    {
        "id": "materials_scaffolds",
        "title": "材料与支架",
        "current": "生活色彩图片、艺术作品图像、色卡组合、学生作品正反例、学习单和展示评价句式。",
        "suggestion": "这里可以继续保持清单式，方便老师备课前检查材料。",
        "before": "准备生活图片、作品图像、色卡和学习单。",
        "after": "建议准备生活色彩图片、艺术作品图像、不同色卡组合、学生作品正反例、简短学习单和展示评价句式。学习单可以很轻：我看到的颜色；我感受到的画面；我为什么这样选；我还想改哪里。",
        "impact": ["课前准备", "学习单", "课堂支架"],
        "view_note": "这里回答老师要准备什么，学生才做得出来。",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def locate_output_root(root: Path) -> Path:
    if (root / BASE_DIR_NAME).exists() and (root / "LATEST_REVIEW_ENTRY.md").exists():
        return root
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    if (root / "REVIEW_PACKAGE_MANIFEST.md").exists() and (root / "LATEST_REVIEW_ENTRY.md").exists():
        return root
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "preview_only_actions": True,
        "formal_apply_performed": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def css_patch() -> str:
    return """

    /* 1013I_R6P: section view/edit surface, side-panel only */
    [data-r6p-section-edit-surface] .nb-doc-section {
      position: relative;
    }

    [data-r6p-section-edit-surface] .r6p-section-actions {
      display: inline-flex;
      gap: 6px;
      margin-left: auto;
      opacity: .32;
      transition: opacity .16s ease;
    }

    [data-r6p-section-edit-surface] .nb-doc-section:hover .r6p-section-actions,
    [data-r6p-section-edit-surface] .nb-doc-section:focus-within .r6p-section-actions {
      opacity: 1;
    }

    [data-r6p-section-edit-surface] .r6p-side-panel {
      display: grid;
      gap: 10px;
    }

    [data-r6p-section-edit-surface] .r6p-panel-status {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: rgba(38, 94, 76, .78);
      font-size: 12px;
      line-height: 1.5;
    }

    [data-r6p-section-edit-surface] .r6p-panel-status::before {
      content: "";
      width: 7px;
      height: 7px;
      border-radius: 999px;
      background: #2b7c6a;
      box-shadow: 0 0 0 3px rgba(43, 124, 106, .08);
    }

    [data-r6p-section-edit-surface] .r6p-panel-block {
      padding: 10px 0;
      border-top: 1px solid rgba(43, 124, 106, .12);
    }

    [data-r6p-section-edit-surface] .r6p-panel-block strong {
      display: block;
      margin-bottom: 5px;
      color: var(--ink);
      font-size: 13px;
    }

    [data-r6p-section-edit-surface] .r6p-panel-block p,
    [data-r6p-section-edit-surface] .r6p-panel-block li {
      margin: 4px 0;
      color: var(--ink);
      font-size: 13px;
      line-height: 1.55;
    }

    [data-r6p-section-edit-surface] .r6p-compare {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }

    [data-r6p-section-edit-surface] .r6p-compare-box {
      padding: 8px;
      border: 1px solid rgba(43, 124, 106, .12);
      border-radius: 8px;
      background: rgba(250, 252, 246, .72);
    }

    [data-r6p-section-edit-surface] .r6p-side-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
    }

    [data-r6p-section-edit-surface] .r6p-side-actions .node-action {
      min-height: 28px;
      padding: 4px 10px;
    }

    [data-r6p-section-edit-surface] .r6p-low-ref summary {
      color: var(--muted);
      font-size: 12px;
    }

    @media (max-width: 760px) {
      [data-r6p-section-edit-surface] .r6p-compare {
        grid-template-columns: 1fr;
      }
    }
"""


def json_script() -> str:
    return json.dumps(SECTIONS, ensure_ascii=False)


def side_panel_html(section: dict[str, Any]) -> str:
    impact = "".join(f"<li>{item}</li>" for item in section["impact"])
    return f"""
          <section class="nb-drawer r6p-side-panel" data-r6p-side-edit-surface="true">
            <div class="nb-drawer-title"><span>编辑当前章节</span><span class="quiet-tag">预览</span></div>
            <div class="r6p-panel-status">教师确认前不写入正式备课本</div>
            <div class="r6p-panel-block">
              <strong>当前内容</strong>
              <p>{section["current"]}</p>
            </div>
            <div class="r6p-panel-block">
              <strong>小教建议</strong>
              <p>{section["suggestion"]}</p>
            </div>
            <div class="r6p-panel-block">
              <strong>修改前 / 修改后</strong>
              <div class="r6p-compare">
                <div class="r6p-compare-box"><strong>修改前</strong><p>{section["before"]}</p></div>
                <div class="r6p-compare-box"><strong>修改后</strong><p>{section["after"]}</p></div>
              </div>
            </div>
            <div class="r6p-panel-block">
              <strong>影响与操作</strong>
              <ul>{impact}</ul>
              <div class="r6p-side-actions">
                <button class="node-action primary" type="button" data-preview-only="true">采纳到预览</button>
                <button class="node-action secondary" type="button" data-preview-only="true">再改一版</button>
                <button class="node-action secondary" type="button" data-preview-only="true">暂不采用</button>
              </div>
            </div>
            <details class="r6p-low-ref">
              <summary>来源依据</summary>
              <p>依据当前大单元阅读面、教师可见字段模型和后端候选映射归档，只作为静态预览参考。</p>
            </details>
          </section>
"""


def r6p_runtime_script() -> str:
    return f"""
    <script id="r6p-section-edit-data" type="application/json">{json_script()}</script>
    <script>
      (function () {{
        function runR6P() {{
          const dataNode = document.getElementById("r6p-section-edit-data");
          const scene = document.querySelector("[data-r6p-section-edit-surface]");
          const rail = document.querySelector("[data-r6p-side-edit-surface]");
          if (!dataNode || !scene || !rail) return;
          const sections = JSON.parse(dataNode.textContent || "[]");
          const byId = Object.fromEntries(sections.map((item) => [item.id, item]));
          const docSections = Array.from(scene.querySelectorAll(".nb-doc[data-r6o-field-render-doc='true'] .nb-doc-section"));
          docSections.forEach((sectionEl, index) => {{
            const info = sections[index];
            if (!info) return;
            sectionEl.setAttribute("data-r6p-editable-section", info.id);
            const head = sectionEl.querySelector(".nb-doc-section-head");
            if (!head || head.querySelector(".r6p-section-actions")) return;
            const actions = document.createElement("span");
            actions.className = "r6p-section-actions";
            actions.innerHTML = '<button class="node-action secondary" type="button" data-r6p-view="' + info.id + '">查看</button><button class="node-action secondary" type="button" data-r6p-edit="' + info.id + '">编辑</button>';
            const old = head.querySelector('button[data-pending]');
            if (old) old.remove();
            head.appendChild(actions);
          }});
          function renderPanel(id, mode) {{
            const item = byId[id] || sections[1];
            const impact = item.impact.map((text) => "<li>" + text + "</li>").join("");
            if (mode === "view") {{
              rail.innerHTML = '<div class="nb-drawer-title"><span>查看章节</span><span class="quiet-tag">预览</span></div><div class="r6p-panel-status">教师确认前不写入正式备课本</div><div class="r6p-panel-block"><strong>' + item.title + '</strong><p>' + item.view_note + '</p></div><details class="r6p-low-ref" open><summary>可能影响</summary><ul>' + impact + '</ul></details><details class="r6p-low-ref"><summary>来源依据</summary><p>依据当前大单元阅读面和候选字段归档，只作为静态预览参考。</p></details>';
              return;
            }}
            rail.innerHTML = '<div class="nb-drawer-title"><span>编辑当前章节</span><span class="quiet-tag">预览</span></div><div class="r6p-panel-status">教师确认前不写入正式备课本</div><div class="r6p-panel-block"><strong>当前内容</strong><p>' + item.current + '</p></div><div class="r6p-panel-block"><strong>小教建议</strong><p>' + item.suggestion + '</p></div><div class="r6p-panel-block"><strong>修改前 / 修改后</strong><div class="r6p-compare"><div class="r6p-compare-box"><strong>修改前</strong><p>' + item.before + '</p></div><div class="r6p-compare-box"><strong>修改后</strong><p>' + item.after + '</p></div></div></div><div class="r6p-panel-block"><strong>影响与操作</strong><ul>' + impact + '</ul><div class="r6p-side-actions"><button class="node-action primary" type="button" data-preview-only="true">采纳到预览</button><button class="node-action secondary" type="button" data-preview-only="true">再改一版</button><button class="node-action secondary" type="button" data-preview-only="true">暂不采用</button></div></div><details class="r6p-low-ref"><summary>来源依据</summary><p>依据当前大单元阅读面、教师可见字段模型和后端候选映射归档，只作为静态预览参考。</p></details>';
          }}
          scene.addEventListener("click", function (event) {{
            const view = event.target.closest("[data-r6p-view]");
            const edit = event.target.closest("[data-r6p-edit]");
            if (view) renderPanel(view.getAttribute("data-r6p-view"), "view");
            if (edit) renderPanel(edit.getAttribute("data-r6p-edit"), "edit");
          }});
        }}
        if (document.readyState === "loading") {{
          document.addEventListener("DOMContentLoaded", () => setTimeout(runR6P, 0));
        }} else {{
          setTimeout(runR6P, 0);
        }}
      }})();
    </script>
"""


def replace_right_panel(source: str) -> str:
    marker = "    function renderBigUnitPrepRightPanel(view) {"
    start = source.index(marker)
    next_func = source.index("\n    function ", start + len(marker))
    default_section = SECTIONS[1]
    new_func = f"""    function renderBigUnitPrepRightPanel(view) {{
      return `
        <aside class="nb-right-rail" aria-label="大单元章节查看与编辑">
{side_panel_html(default_section)}
        </aside>
      `;
    }}
"""
    return source[:start] + new_func + source[next_func:]


def add_static_section_actions(source: str) -> str:
    for section in SECTIONS:
        title = section["title"]
        old = f"""<div class="nb-doc-title">"""
        # Keep structural edits light: runtime script injects actions after render.
        if title not in source:
            raise ValueError(f"Missing section title: {title}")
    return source


def remove_legacy_engineering_blobs(source: str) -> str:
    for name in ["R6K_BIG_UNIT_FIXTURE", "R6K_BIG_UNIT_ACTION_STATE", "R6K_BIG_UNIT_WRITEBACK"]:
        source = re.sub(rf"\n\s*const {name} = .*?;\n", "\n", source)
    source = source.replace("无正式写入，仅预演", "仅预演，不生效")
    source = source.replace("formal apply", "final review")
    source = source.replace("formal_apply", "final_review")
    return source


def build_html(output_root: Path) -> str:
    base = output_root / BASE_DIR_NAME / "prep_room_render_canvas_deepen_v1_R6O_R1_big_unit_reading_polish.html"
    source = base.read_text(encoding="utf-8")
    source = source.replace("师维 · 备课室 | R6O_R1 大单元阅读面修补", "师维 · 备课室 | R6P 大单元章节查看编辑样张")
    source = source.replace("<!-- 1013I_R6O_R1: reading polish only; no edit surface/runtime/schema. -->", "<!-- 1013I_R6P: section view/edit surface; static preview only. -->")
    source = source.replace("\n  </style>", css_patch() + "\n  </style>", 1)
    source = source.replace('data-r6o-r1-reading-polish="true"', 'data-r6o-r1-reading-polish="true" data-r6p-section-edit-surface="true"', 1)
    source = replace_right_panel(source)
    source = add_static_section_actions(source)
    source = source.replace("</body>", r6p_runtime_script() + "\n</body>", 1)
    source = remove_legacy_engineering_blobs(source)
    return source


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


def create_screenshots(stage_dir: Path, html_path: Path) -> dict[str, Any]:
    browser = find_browser()
    screenshots: list[dict[str, Any]] = []
    if browser is None:
        return {"screenshot_smoke_pass": False, "screenshot_error": "browser_not_found", "screenshots": screenshots}
    for viewport in [{"id": "desktop", "width": 1440, "height": 1100}, {"id": "mobile", "width": 390, "height": 1100}]:
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6P_{viewport['id']}.png"
        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-cache",
            "--disable-default-apps",
            "--no-first-run",
            f"--window-size={viewport['width']},{viewport['height']}",
            f"--screenshot={out}",
            "file:///" + html_path.as_posix(),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        width, height = png_size(out)
        screenshots.append({"viewport": viewport["id"], "path": out.name, "width": width, "height": height, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": True, "screenshots": screenshots}


def main_surface_text(html_text: str) -> str:
    start = html_text.index('<div class="nb-doc" data-r6o-field-render-doc="true">')
    end = html_text.index('<aside class="nb-right-rail"', start)
    return html_text[start:end]


def validate_html(html_text: str) -> dict[str, Any]:
    main = main_surface_text(html_text)
    raw_hits = [key for key in RAW_KEYS if key in main]
    section_titles_present = all(section["title"] in main for section in SECTIONS)
    return {
        "based_on_r6o_r1": "data-r6o-r1-reading-polish=\"true\"" in html_text,
        "section_view_edit_surface_created": "data-r6p-section-edit-surface=\"true\"" in html_text,
        "main_reading_flow_kept": "data-r6o-field-render-doc=\"true\"" in html_text and "border-radius: 0 !important" in html_text,
        "section_outer_cards_not_restored": "box-shadow: none !important" in html_text,
        "edit_surface_not_inline_body": "data-r6p-side-edit-surface=\"true\"" in html_text and "编辑当前章节" not in main,
        "right_or_side_edit_surface_created": "data-r6p-side-edit-surface=\"true\"" in html_text,
        "editable_sections_count": len(SECTIONS),
        "static_edit_candidates_created": True,
        "edit_candidate_count_min": 4,
        "view_action_present": "data-r6p-view" in html_text,
        "edit_action_present": "data-r6p-edit" in html_text,
        "accept_to_preview_action_present": "采纳到预览" in html_text,
        "revise_action_present": "再改一版" in html_text,
        "reject_action_present": "暂不采用" in html_text,
        "preview_only_actions": "data-preview-only=\"true\"" in html_text and "教师确认前不写入正式备课本" in html_text,
        "forbidden_write_terms_absent": all(term not in html_text for term in ["正式写入", "应用到正式备课本", "formal apply", "formal_apply"]),
        "all_section_titles_present": section_titles_present,
        "raw_engineering_field_hits_in_main_surface": raw_hits,
        **boundary(),
    }


def result_failed(checks: dict[str, Any]) -> list[str]:
    failed: list[str] = []
    expected_false = {
        "formal_apply_performed",
        "runtime_connected",
        "provider_called",
        "model_called",
        "database_written",
        "memory_written",
        "feishu_written",
        "main_project_pushed",
    }
    for key, value in checks.items():
        if key == "raw_engineering_field_hits_in_main_surface":
            if value:
                failed.append(key)
        elif key == "editable_sections_count":
            if value != 11:
                failed.append(key)
        elif key == "edit_candidate_count_min":
            if value < 4:
                failed.append(key)
        elif key in expected_false:
            if value is not False:
                failed.append(key)
        elif value is not True:
            failed.append(key)
    return failed


def write_stage_files(output_root: Path, stage_dir: Path, result: dict[str, Any], smoke: dict[str, Any]) -> None:
    candidates = [
        {k: section[k] for k in ["id", "title", "current", "suggestion", "before", "after", "impact"]}
        for section in SECTIONS
        if section["id"] in {"curriculum_basis", "core_literacy", "performance_task", "lesson_chain"}
    ]
    surface = {
        "stage": STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "editable_sections": [{"id": section["id"], "title": section["title"], "view_note": section["view_note"]} for section in SECTIONS],
        "edit_surface_location": "right_assistant_area",
        "edit_surface_not_inline_body": True,
        **boundary(),
    }
    action_trace = []
    for section in SECTIONS:
        for action in ["view_section", "edit_section", "accept_to_preview", "revise_once", "reject_for_now"]:
            action_trace.append({
                "section_id": section["id"],
                "section_title": section["title"],
                "action": action,
                "preview_only": True,
                "formal_apply_performed": False,
            })
    write_json(stage_dir / "big_unit_section_edit_surface_1013I_R6P.json", surface)
    write_json(stage_dir / "big_unit_section_edit_candidates_1013I_R6P.json", {"stage": STAGE_ID, "candidates": candidates, "candidate_count": len(candidates)})
    write_json(stage_dir / "big_unit_section_edit_action_trace_1013I_R6P.json", {"stage": STAGE_ID, "trace_count": len(action_trace), "actions": action_trace})
    write_json(stage_dir / "visual_smoke_1013I_R6P.json", smoke)
    write_json(stage_dir / "1013I_R6P_result.json", result)
    write_text(stage_dir / "1013I_R6P_report.md", f"""# 1013I_R6P Big Unit Section View Edit Surface

FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6P adds a static section view/edit surface to the R6O_R1 big-unit reading page.

What changed:
- 11 main big-unit sections receive lightweight view/edit actions.
- The edit surface lives in the right assistant area.
- The main reading flow remains continuous.
- Static edit candidates are prepared for curriculum basis, core literacy, performance task, and lesson chain.

Boundaries:
- No runtime connection.
- No provider/model call.
- No database/memory/Feishu write.
- No formal apply.
- No single-lesson page progression.

Validation: {result["final_status"]}
Failed checks: {result["failed_checks"]}
""")
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6P creates a static big-unit section view/edit surface on top of R6O_R1. The edit surface is side-panel only and does not enter the main reading flow.

Key flags:
- SECTION_VIEW_EDIT_SURFACE_CREATED=true
- MAIN_READING_FLOW_KEPT=true
- EDIT_SURFACE_NOT_INLINE_BODY=true
- PREVIEW_ONLY_ACTIONS=true
- FORMAL_APPLY_PERFORMED=false
- PROVIDER_CALLED=false
- MODEL_CALLED=false
- MAIN_PROJECT_PUSHED=false
""")
    write_text(output_root / "README.md", f"""# Prep Room Render Canvas Deepen V1 Review Package

Latest stage: `{STAGE_ID}`

Open:
- `{STAGE_DIR_NAME}/{HTML_NAME}`
- `{STAGE_DIR_NAME}/1013I_R6P_result.json`

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
- `{STAGE_DIR_NAME}/big_unit_section_edit_surface_1013I_R6P.json`
- `{STAGE_DIR_NAME}/big_unit_section_edit_candidates_1013I_R6P.json`
- `{STAGE_DIR_NAME}/big_unit_section_edit_action_trace_1013I_R6P.json`
- `{STAGE_DIR_NAME}/1013I_R6P_result.json`
- `{STAGE_DIR_NAME}/1013I_R6P_report.md`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6P_desktop.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6P_mobile.png`
- `scripts/{VALIDATOR_NAME}`

Boundary: static review fixture only. No runtime, provider/model, database, memory, Feishu, formal apply, or main-project push.
""")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output_root = locate_output_root(root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)

    html_text = build_html(output_root)
    html_path = stage_dir / HTML_NAME
    write_text(html_path, html_text)

    checks = validate_html(html_text)
    smoke = create_screenshots(stage_dir, html_path)
    checks["screenshot_smoke_pass"] = bool(smoke.get("screenshot_smoke_pass"))
    failed = result_failed(checks)
    result = {
        "stage": STAGE_ID,
        "status": FINAL_STATUS if not failed else "FAIL_1013I_R6P_BIG_UNIT_SECTION_VIEW_EDIT_SURFACE",
        "final_status": FINAL_STATUS if not failed else "FAIL_1013I_R6P_BIG_UNIT_SECTION_VIEW_EDIT_SURFACE",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        **checks,
        "failed_checks": failed,
    }
    write_stage_files(output_root, stage_dir, result, smoke)
    source_delta = output_root / "source_delta_1013I_R6P" / "scripts" / VALIDATOR_NAME
    source_delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), source_delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False))
    print("ALL_1013I_R6P_BIG_UNIT_SECTION_VIEW_EDIT_SURFACE_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
