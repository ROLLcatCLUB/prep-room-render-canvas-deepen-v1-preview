from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6P_SINGLE_LESSON_READING_SURFACE_INHERITS_BIG_UNIT_STATIC_UPGRADE"
REQUESTED_STAGE_ALIAS = "1013I_R6O_SINGLE_LESSON_READING_SURFACE_INHERITS_BIG_UNIT_STATIC_UPGRADE"
FINAL_STATUS = "PASS_1013I_R6P_SINGLE_LESSON_READING_SURFACE_INHERITS_BIG_UNIT_STATIC_UPGRADE"
INHERITS_FROM = "1013I_R6N_R7_BIG_UNIT_PAGE_USER_REVIEW_AND_CONTENT_POLISH"
NEXT_STAGE = "USER_REVIEW_SINGLE_LESSON_INHERITANCE_SURFACE"
STAGE_DIR_NAME = "1013I_R6P_single_lesson_reading_surface_inherits_big_unit_static_upgrade"
R6N_R7_DIR_NAME = "1013I_R6N_R7_big_unit_page_user_review_and_content_polish"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6P_single_lesson_inherits_big_unit.html"
VALIDATOR_NAME = "validate_1013I_R6P_single_lesson_reading_surface_inherits_big_unit_static_upgrade.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]
RAW_KEYS = [
    "unit_theme",
    "big_idea",
    "essential_question",
    "lesson_position",
    "textbook_anchor",
    "normal_candidate_card_generation_allowed",
    "teacher_confirmation_required",
    "formal_apply",
    "unit_package",
]
FORBIDDEN_MAIN_TEXT = ["正式生成", "写入正式备课本", "formal apply", "系统提示词", "schema"]
SECRET_PATTERNS = [re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"), re.compile(r"(?i)bearer\s+[A-Za-z0-9_.-]{20,}")]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_output_root(root: Path) -> Path:
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


def replace_once(source: str, old: str, new: str) -> str:
    if old not in source:
        raise ValueError(f"missing replacement marker: {old[:80]}")
    return source.replace(old, new, 1)


def boundary() -> dict[str, bool]:
    return {
        "static_upgrade_only": True,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def r6p_css() -> str:
    return """

    /* 1013I_R6P: single-lesson reading surface inherits big-unit direction */
    .nb-single-lesson-doc {
      display: grid;
      gap: 0;
      max-width: 760px;
      margin: 0 auto;
    }

    .nb-single-inherit-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 9px;
    }

    .nb-single-inherit-tag {
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 3px 9px;
      border: 1px solid rgba(46, 123, 103, .22);
      border-radius: 999px;
      background: rgba(236, 248, 244, .82);
      color: var(--green);
      font-size: 12px;
      font-weight: 800;
      line-height: 1.3;
    }

    .nb-single-section {
      display: grid;
      grid-template-columns: 44px minmax(0, 1fr);
      gap: 14px;
      padding: 26px 0;
      border-top: 1px solid rgba(42, 86, 72, .12);
    }

    .nb-single-no {
      width: 34px;
      height: 34px;
      display: inline-grid;
      place-items: center;
      border-radius: 50%;
      color: #fff;
      background: var(--green);
      font-size: 13px;
      font-weight: 900;
    }

    .nb-single-section h3 {
      margin: 0 0 12px;
      font-size: 20px;
      line-height: 1.35;
      color: var(--ink);
    }

    .nb-single-section p,
    .nb-single-section li {
      font-size: 15px;
      line-height: 1.9;
    }

    .nb-single-timeline {
      display: grid;
      gap: 12px;
      margin-top: 6px;
    }

    .nb-single-step {
      display: grid;
      grid-template-columns: 42px minmax(0, 1fr);
      gap: 12px;
      align-items: start;
    }

    .nb-single-step code {
      display: inline-grid;
      place-items: center;
      width: 34px;
      height: 34px;
      border-radius: 50%;
      background: rgba(34, 126, 104, .1);
      color: var(--green);
      font-family: inherit;
      font-weight: 900;
    }

    .nb-single-mini-note {
      margin-top: 8px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.65;
    }

    .nb-single-material-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
    }
"""


def single_lesson_functions() -> str:
    return r'''
    function renderSingleLessonReadingSurface(view) {
      return `
        <section class="nb-workspace" aria-label="1-2 色彩的感觉单课备课">
          <div class="nb-hero">
            <div>
              <div class="nb-kicker">备课室 · 单课备课</div>
              <div class="nb-title">1-2 色彩的感觉</div>
              <div class="nb-single-inherit-tags">
                <span class="nb-single-inherit-tag" title="来自第一单元 · 多变的色彩">单元：多变的色彩</span>
                <span class="nb-single-inherit-tag" title="上一课：学生已经打开色彩感受。本课：比较不同色彩组合带来的感觉变化。下一课：用色彩完成表达并展示修改。">本课位置：比较方法</span>
                <span class="nb-single-inherit-tag" title="当前为静态升级样张，只保留预览，不保存为正式版本。">● 预览</span>
              </div>
            </div>
            <div class="nb-hero-actions">
              <button class="node-action primary" type="button" data-pending="已保留到预览层，不保存为正式版本。">${iconButtonLabel("确认到预览", "check")}</button>
              <button class="node-action secondary" type="button" data-big-unit-entry="nb-unit-color">${iconButtonLabel("回到大单元", "arrow")}</button>
            </div>
          </div>

          <article class="nb-single-lesson-doc" data-r6p-single-lesson-surface="true">
            <section class="nb-single-section">
              <span class="nb-single-no">01</span>
              <div>
                <h3>本课方向</h3>
                <p>让学生从“颜色让我有什么感觉”，走向“为什么这样搭配会有这种感觉”。</p>
              </div>
            </section>

            <section class="nb-single-section">
              <span class="nb-single-no">02</span>
              <div>
                <h3>学生起点</h3>
                <p>学生已经能说出一些直观感受，比如“红色热闹、蓝色安静”。本课重点是让学生通过比较，发现色彩组合变化会改变画面感觉。</p>
              </div>
            </section>

            <section class="nb-single-section">
              <span class="nb-single-no">03</span>
              <div>
                <h3>学习目标</h3>
                <ul>
                  <li>能说出两组色彩搭配带来的不同感觉。</li>
                  <li>能说明一种搭配为什么更热闹、安静、强烈或柔和。</li>
                  <li>能完成一张色彩实验小练习。</li>
                  <li>能尝试调整一处色彩搭配。</li>
                </ul>
              </div>
            </section>

            <section class="nb-single-section">
              <span class="nb-single-no">04</span>
              <div>
                <h3>课堂推进</h3>
                <div class="nb-single-timeline">
                  <div class="nb-single-step"><code>01</code><p><strong>看色彩：</strong>看两组色彩图片或色卡，说出第一感觉。</p></div>
                  <div class="nb-single-step"><code>02</code><p><strong>说感觉：</strong>把“好看、鲜艳”换成更具体的词：热闹、安静、强烈、柔和。</p></div>
                  <div class="nb-single-step"><code>03</code><p><strong>比变化：</strong>比较同一颜色在不同搭配中的变化，发现组合会改变画面意味。</p></div>
                  <div class="nb-single-step"><code>04</code><p><strong>做实验：</strong>选一组颜色，完成一张表达感觉的小练习。</p></div>
                  <div class="nb-single-step"><code>05</code><p><strong>说理由：</strong>展示练习，说出自己为什么这样选色。</p></div>
                </div>
                <p class="nb-single-mini-note">如果学生卡住，可以先给感觉词卡；如果时间紧，就先完成色彩实验卡。</p>
              </div>
            </section>

            <section class="nb-single-section">
              <span class="nb-single-no">05</span>
              <div>
                <h3>看什么证据</h3>
                <ul>
                  <li>学生能说出色彩带来的感觉；</li>
                  <li>能比较两组搭配的差异；</li>
                  <li>能说明自己的选色理由；</li>
                  <li>实验小练习呈现出明确感觉；</li>
                  <li>能根据反馈调整一处颜色。</li>
                </ul>
              </div>
            </section>

            <section class="nb-single-section">
              <span class="nb-single-no">06</span>
              <div>
                <h3>课前准备</h3>
                <p>两组对比明显的色彩图片；几组色卡；学生作品正反例；一张轻量学习单；展示评价句式。</p>
                <p class="nb-single-mini-note">学习单可以很轻：我看到的颜色；我感受到的感觉；我为什么这样选；我还想改哪里。</p>
              </div>
            </section>

            <section class="nb-single-section">
              <span class="nb-single-no">07</span>
              <div>
                <h3>可调整处</h3>
                <ul>
                  <li>如果学生说不出理由，先给感觉词卡。</li>
                  <li>如果创作时间紧，只做色彩实验卡，不急着完成完整作品。</li>
                  <li>如果学生颜色选择太散，先限制在 3-4 种颜色内尝试。</li>
                </ul>
                <div class="nb-single-material-actions">
                  <button class="node-action secondary" type="button" data-pending="补充后，小教可以把课堂活动和材料支架调得更贴近你的教材。">${iconButtonLabel("补充本课教材页", "upload")}</button>
                  <button class="node-action secondary" type="button" data-pending="补充后，小教可以把课堂活动和材料支架调得更贴近你的教材。">${iconButtonLabel("上传参考作品", "upload")}</button>
                  <button class="node-action secondary" type="button" data-pending="补充后，小教可以把课堂活动和材料支架调得更贴近你的教材。">${iconButtonLabel("粘贴你的课堂材料", "list")}</button>
                  <button class="node-action secondary" type="button" data-pending="补充后，小教可以把课堂活动和材料支架调得更贴近你的教材。">${iconButtonLabel("补充已有教学想法", "arrow")}</button>
                </div>
              </div>
            </section>
          </article>
        </section>
      `;
    }

    function renderSingleLessonInheritanceRightPanel(view) {
      return `
        <aside class="nb-right-rail" aria-label="单课继承依据">
          <section class="nb-drawer" data-r6p-single-right-rail="true">
            <div class="nb-drawer-title"><span>依据</span><span class="quiet-tag">默认折叠</span></div>
            <details>
              <summary>查看单元继承、课标方向和风险提醒</summary>
              <p>单元继承：上一课打开色彩感受；本课比较色彩组合变化；下一课用色彩完成表达并展示修改。</p>
              <p>课标方向：审美感知、艺术表现、创意实践。</p>
              <p>评价证据来源：表达理由、实验小练习、调整一处颜色。</p>
              <p>风险提醒：不要把大单元内容整块搬进单课页；本页只显示轻继承。</p>
            </details>
          </section>
        </aside>
      `;
    }

    function renderPrepNotebookSingleLessonInheritanceCanvas(view) {
      return `
        <div class="nb-scene" data-r6k-integrated-static="true" data-r6l-teacher-guidance-patch="true" data-r6m-big-unit-design-static="true" data-r6n-text-reading-static="true" data-r6n-r1-centered-numbered-static="true" data-r6n-r2-left-aligned-text="true" data-r6n-r3-minimal-copy="true" data-r6n-r4-content-rewrite="true" data-r6n-r7-content-polish="true" data-r6p-single-lesson-static="true">
          <div class="nb-binder" aria-label="备课本活页夹">
            <aside class="nb-panel" aria-label="备课本目录">
              <div class="nb-cover">
                <div class="nb-cover-title">${html(view.cover.title)}</div>
                <div class="nb-cover-sub">${html(view.cover.subtitle)}</div>
                <div class="nb-metrics">
                  ${view.cover.metrics.map(([label, value]) => `
                    <div class="nb-metric ${nbMetricTone(label)}">
                      <span class="nb-metric-light" aria-hidden="true"></span>
                      <strong>${html(value)}</strong>
                      <span>${html(label)}</span>
                    </div>
                  `).join("")}
                </div>
              </div>
              <div class="nb-tree">${renderPrepNotebookTree(view)}</div>
            </aside>

            <div class="nb-gutter" aria-hidden="true"></div>

            <main class="nb-main">
              ${renderSingleLessonReadingSurface(view)}
            </main>
          </div>
          ${renderSingleLessonInheritanceRightPanel(view)}
        </div>
      `;
    }

    function openSingleLessonInheritanceSurface(nodeId, options = {}) {
      const prepView = model.views.find((view) => view.id === "prepNotebook");
      if (!prepView) return;
      if (!options.skipRemember) rememberActiveScroll();
      model.active_view = "prepNotebook";
      prepView.prep_notebook_mode = "view";
      prepView.active_big_unit_id = "";
      prepView.active_single_lesson_surface = nodeId || "nb-lesson-1-2";
      prepView.active_node = nodeId || "nb-lesson-1-2";
      prepView.active_edit_target = null;
      prepView.selected_paragraph_id = "";
      if (!options.skipRender) {
        renderPrepRoomCanvas();
        showToast("已打开 1-2 单课继承阅读面");
      }
    }
'''


def build_html(output_root: Path) -> str:
    base = output_root / R6N_R7_DIR_NAME / "prep_room_render_canvas_deepen_v1_R6N_R7_big_unit_page_user_review_and_content_polish.html"
    source = base.read_text(encoding="utf-8")
    source = source.replace("师维 · 备课室 | R6N_R7 内容审核打磨", "师维 · 备课室 | R6P 单课继承阅读面")
    source = replace_once(source, "\n  </style>", r6p_css() + "\n  </style>")
    source = replace_once(source, "    function renderPrepNotebookBigUnitCanvas(view) {", single_lesson_functions() + "\n    function renderPrepNotebookBigUnitCanvas(view) {")
    source = replace_once(
        source,
        '      prepView.active_big_unit_id = unitId || "nb-unit-color";',
        '      prepView.active_big_unit_id = unitId || "nb-unit-color";\n      prepView.active_single_lesson_surface = "";',
    )
    source = replace_once(
        source,
        '      prepView.active_big_unit_id = "";',
        '      prepView.active_big_unit_id = "";\n      prepView.active_single_lesson_surface = "";',
    )
    source = replace_once(
        source,
        '      openBigUnitPrepSurface("nb-unit-color", { skipRemember: true, skipRender: true });',
        '      openSingleLessonInheritanceSurface("nb-lesson-1-2", { skipRemember: true, skipRender: true });',
    )
    source = replace_once(
        source,
        '      if (view.active_big_unit_id) return renderPrepNotebookBigUnitCanvas(view);',
        '      if (view.active_single_lesson_surface === "nb-lesson-1-2") return renderPrepNotebookSingleLessonInheritanceCanvas(view);\n      if (view.active_big_unit_id) return renderPrepNotebookBigUnitCanvas(view);',
    )
    source = replace_once(
        source,
        '''        const prepLessonButton = event.target.closest("[data-node^='nb-lesson']");
        if (prepLessonButton && model.active_view === "prepNotebook") {
          closeBigUnitPrepSurface({ skipRender: true });
          renderPrepRoomCanvas();
          showToast("已回到单课备课本");
          return;
        }''',
        '''        const prepLessonButton = event.target.closest("[data-node^='nb-lesson']");
        if (prepLessonButton && model.active_view === "prepNotebook") {
          if (prepLessonButton.dataset.node === "nb-lesson-1-2") {
            openSingleLessonInheritanceSurface("nb-lesson-1-2");
          } else {
            closeBigUnitPrepSurface({ skipRender: true });
            renderPrepRoomCanvas();
            showToast("已回到单课备课本");
          }
          return;
        }''',
    )
    source = source.replace(
        '<!-- 1013I_R6N_R7: user-view content polish; preview only, no runtime/provider/formal apply. -->',
        '<!-- 1013I_R6P: single-lesson reading surface inherits big-unit direction; static upgrade only. -->',
    )
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
        run = subprocess.run(cmd, text=True, capture_output=True, timeout=60)
        if run.returncode != 0:
            return {"screenshot_smoke_pass": False, "screenshot_error": run.stderr[-500:], "screenshots": screenshots}
        width, height = png_size(out)
        screenshots.append({"viewport": viewport["id"], "path": out.name, "width": width, "height": height, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": all(item["bytes"] > 10000 for item in screenshots), "screenshot_error": None, "screenshots": screenshots}


def extract_function_body(html_text: str, start: str, end: str) -> str:
    s = html_text.index(start)
    e = html_text.index(end, s)
    return html_text[s:e]


def scan_secrets(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() and path.suffix.lower() != ".png" else ""
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append(str(path))
                break
    return hits


def build_result(html_path: Path, visual_smoke: dict[str, Any]) -> dict[str, Any]:
    html_text = html_path.read_text(encoding="utf-8")
    main = extract_function_body(html_text, "function renderSingleLessonReadingSurface(view)", "function renderSingleLessonInheritanceRightPanel(view)")
    hits = [key for key in RAW_KEYS if key in main]
    forbidden_hits = [text for text in FORBIDDEN_MAIN_TEXT if text in main]
    result = {
        "stage": STAGE_ID,
        "requested_stage_alias": REQUESTED_STAGE_ALIAS,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "based_on_r6n_r7": True,
        "single_lesson_surface_created": "data-r6p-single-lesson-surface" in html_text,
        "big_unit_entry_kept": "data-big-unit-entry" in html_text and "大单元" in html_text,
        "single_lesson_entry_created_or_kept": 'data-node="${html(item.id)}"' in html_text and "1-2" in html_text and "色彩的感觉" in html_text,
        "lesson_1_2_opens_single_lesson_surface": 'prepLessonButton.dataset.node === "nb-lesson-1-2"' in html_text and "openSingleLessonInheritanceSurface" in html_text,
        "big_unit_inheritance_lightweight": "单元：多变的色彩" in main and "本课位置：比较方法" in main and "上一课：学生已经打开色彩感受" in main,
        "unit_tag_visible": "单元：多变的色彩" in main,
        "lesson_position_tag_visible": "本课位置：比较方法" in main,
        "hover_or_collapsed_inheritance_detail": "title=\"上一课：学生已经打开色彩感受" in main and "默认折叠" in html_text,
        "main_surface_not_overloaded_by_big_unit": main.count("大单元") <= 1 and "课标依据" not in main,
        "lesson_direction_present": "本课方向" in main and "为什么这样搭配会有这种感觉" in main,
        "student_start_present": "学生起点" in main and "红色热闹、蓝色安静" in main,
        "student_behavior_goals_present": all(text in main for text in ["能说出两组色彩搭配", "能说明一种搭配", "能完成一张色彩实验小练习", "能尝试调整一处色彩搭配"]),
        "classroom_process_present": all(text in main for text in ["看色彩", "说感觉", "比变化", "做实验", "说理由"]),
        "assessment_evidence_present": "看什么证据" in main and "能比较两组搭配的差异" in main,
        "lesson_materials_present": "课前准备" in main and "色卡" in main and "轻量学习单" in main,
        "adjustment_notes_present": "可调整处" in main and "如果学生说不出理由" in main,
        "raw_engineering_field_hits_in_main_surface": hits,
        "forbidden_main_text_hits": forbidden_hits,
        "screenshot_smoke_pass": visual_smoke.get("screenshot_smoke_pass") is True,
        "screenshot_count": len(visual_smoke.get("screenshots", [])),
        "secret_scan_hits": [],
        **boundary(),
    }
    required = [
        "single_lesson_surface_created",
        "big_unit_entry_kept",
        "single_lesson_entry_created_or_kept",
        "lesson_1_2_opens_single_lesson_surface",
        "big_unit_inheritance_lightweight",
        "unit_tag_visible",
        "lesson_position_tag_visible",
        "hover_or_collapsed_inheritance_detail",
        "main_surface_not_overloaded_by_big_unit",
        "lesson_direction_present",
        "student_start_present",
        "student_behavior_goals_present",
        "classroom_process_present",
        "assessment_evidence_present",
        "lesson_materials_present",
        "adjustment_notes_present",
        "screenshot_smoke_pass",
    ]
    failures = [key for key in required if result.get(key) is not True]
    if hits:
        failures.append("raw_engineering_field_hits_in_main_surface")
    if forbidden_hits:
        failures.append("forbidden_main_text_hits")
    result["failed_checks"] = failures
    result["final_status"] = FINAL_STATUS if not failures else "FAIL_1013I_R6P_SINGLE_LESSON_READING_SURFACE_INHERITS_BIG_UNIT_STATIC_UPGRADE"
    return result


def write_docs(output_root: Path, stage_dir: Path, result: dict[str, Any]) -> None:
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

```text
REVIEW_STAGE={STAGE_ID}
REQUESTED_STAGE_ALIAS={REQUESTED_STAGE_ALIAS}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_RECOMMENDED_STAGE={NEXT_STAGE}
SINGLE_LESSON_SURFACE_CREATED={str(result["single_lesson_surface_created"]).lower()}
BIG_UNIT_INHERITANCE_LIGHTWEIGHT={str(result["big_unit_inheritance_lightweight"]).lower()}
LESSON_1_2_OPENS_SINGLE_LESSON_SURFACE={str(result["lesson_1_2_opens_single_lesson_surface"]).lower()}
MAIN_SURFACE_NOT_OVERLOADED_BY_BIG_UNIT={str(result["main_surface_not_overloaded_by_big_unit"]).lower()}
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Summary

R6P continues the prep-room static upgrade branch and implements the requested R6O single-lesson inheritance surface without touching the main system. Clicking `1-2 色彩的感觉` opens a lightweight single-lesson reading surface that inherits the big-unit direction.
""")
    write_text(output_root / "README.md", f"""# PREP_ROOM_RENDER_CANVAS_DEEPEN_V1

Current stage: `{STAGE_ID}`

R6P implements the requested single-lesson reading surface that inherits the big-unit direction, as a static upgrade sample only.
""")
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", f"""# Review Package Manifest

```text
current_stage={STAGE_ID}
requested_stage_alias={REQUESTED_STAGE_ALIAS}
final_status={result["final_status"]}
main_project_pushed=false
```

## Key Files

```text
{STAGE_DIR_NAME}/{HTML_NAME}
{STAGE_DIR_NAME}/1013I_R6P_result.json
{STAGE_DIR_NAME}/1013I_R6P_report.md
{STAGE_DIR_NAME}/visual_smoke_1013I_R6P.json
scripts/{VALIDATOR_NAME}
source_delta_1013I_R6P/scripts/{VALIDATOR_NAME}
```
""")
    write_text(stage_dir / "1013I_R6P_report.md", f"""# 1013I_R6P Report

This stage implements the requested R6O single-lesson inheritance surface as R6P because R6O is already occupied by prep-mode planning.

- single lesson surface created: `{result["single_lesson_surface_created"]}`
- big unit entry kept: `{result["big_unit_entry_kept"]}`
- 1-2 opens single lesson surface: `{result["lesson_1_2_opens_single_lesson_surface"]}`
- big unit inheritance lightweight: `{result["big_unit_inheritance_lightweight"]}`
- main surface raw engineering field hits: `{result["raw_engineering_field_hits_in_main_surface"]}`
- screenshot smoke pass: `{result["screenshot_smoke_pass"]}`

Boundary: static upgrade only; no runtime, provider/model, database, memory, Feishu, formal apply, or main-project push.
""")


def validate_result(result: dict[str, Any]) -> None:
    if result.get("failed_checks"):
        raise SystemExit("R6P validation failed: " + ", ".join(result["failed_checks"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    output_root = resolve_output_root(args.root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)
    html_path = stage_dir / HTML_NAME
    write_text(html_path, build_html(output_root))
    visual_smoke = create_screenshots(stage_dir, html_path)
    write_json(stage_dir / "visual_smoke_1013I_R6P.json", visual_smoke)
    result = build_result(html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([html_path])
    write_json(stage_dir / "1013I_R6P_result.json", result)
    write_json(stage_dir / "single_lesson_inheritance_manifest_1013I_R6P.json", {"stage": STAGE_ID, "requested_stage_alias": REQUESTED_STAGE_ALIAS, "inherits_from": INHERITS_FROM, "boundary": boundary()})
    write_docs(output_root, stage_dir, result)
    source_delta = output_root / "source_delta_1013I_R6P" / "scripts"
    source_delta.mkdir(parents=True, exist_ok=True)
    target = source_delta / VALIDATOR_NAME
    if Path(__file__).resolve() != target:
        shutil.copy2(Path(__file__).resolve(), target)
    result = build_result(html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([html_path, output_root / "LATEST_REVIEW_ENTRY.md", output_root / "README.md"])
    write_json(stage_dir / "1013I_R6P_result.json", result)
    write_docs(output_root, stage_dir, result)
    validate_result(result)
    print("ALL_1013I_R6P_SINGLE_LESSON_READING_SURFACE_INHERITS_BIG_UNIT_STATIC_UPGRADE_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "requested_stage_alias": REQUESTED_STAGE_ALIAS, "status": result["final_status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
