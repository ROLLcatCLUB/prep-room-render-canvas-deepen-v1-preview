from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6N_R3_BIG_UNIT_DESIGN_READING_SURFACE_MINIMAL_COPY"
FINAL_STATUS = "PASS_1013I_R6N_R3_BIG_UNIT_DESIGN_READING_SURFACE_MINIMAL_COPY"
INHERITS_FROM = "1013I_R6N_R2_CENTERED_PAGE_LEFT_ALIGNED_TEXT_PATCH"
NEXT_STAGE = "USER_REVIEW_BIG_UNIT_DESIGN_READING_SURFACE"
STAGE_DIR_NAME = "1013I_R6N_R3_big_unit_design_reading_surface_minimal_copy"
R6N_R2_DIR_NAME = "1013I_R6N_R2_centered_page_left_aligned_text_patch"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6N_R3_big_unit_design_reading_surface_minimal_copy.html"
VALIDATOR_NAME = "validate_1013I_R6N_R3_big_unit_design_reading_surface_minimal_copy.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]
RAW_KEYS = ["unit_theme", "big_idea", "student_context", "performance_task", "learning_stages", "formal_apply", "lesson_position"]
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


def boundary() -> dict[str, bool]:
    return {
        "html_modified": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def replace_block(source: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = source.index(start_marker)
    end = source.index(end_marker, start)
    return source[:start] + replacement.rstrip() + "\n\n" + source[end:]


def r6n_r3_css() -> str:
    return """

    /* 1013I_R6N_R3: minimal reading surface, content first */
    .nb-unit-reading-doc {
      max-width: 720px;
      margin-left: auto;
      margin-right: auto;
      text-align: left;
      padding-top: 8px;
    }

    .nb-unit-hero-minimal {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding-bottom: 14px;
      border-bottom: 1px solid rgba(43, 124, 106, 0.16);
    }

    .nb-unit-hero-minimal h2 {
      margin: 0;
      color: var(--ink);
      font-size: 25px;
      line-height: 1.25;
      font-weight: 950;
    }

    .nb-light-tags {
      display: inline-flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 8px;
    }

    .nb-light-tag {
      min-height: 22px;
      display: inline-flex;
      align-items: center;
      padding: 0 8px;
      border: 1px solid #cfe0d9;
      border-radius: 999px;
      color: var(--green);
      background: #f8fcf9;
      font-size: 12px;
      font-weight: 850;
    }

    .nb-unit-reading-section {
      display: grid;
      grid-template-columns: 42px minmax(0, 1fr);
      gap: 14px;
      padding: 17px 0;
      border-top: 1px solid rgba(43, 124, 106, 0.12);
    }

    .nb-unit-reading-section:first-of-type {
      border-top: 0;
    }

    .nb-section-no {
      width: 34px;
      height: 34px;
      display: grid;
      place-items: center;
      border-radius: 999px;
      color: #fff;
      background: var(--green);
      font-size: 12px;
      font-weight: 950;
      letter-spacing: 0;
    }

    .nb-unit-reading-section h3 {
      margin: 0 0 7px;
      color: var(--ink);
      font-size: 18px;
      line-height: 1.35;
      font-weight: 950;
      text-align: left;
    }

    .nb-unit-reading-section p,
    .nb-unit-reading-section li {
      color: #20372f;
      font-size: 15px;
      line-height: 1.85;
      text-align: left;
    }

    .nb-unit-reading-section p {
      margin: 0 0 8px;
    }

    .nb-unit-reading-section ul {
      margin: 0;
      padding-left: 18px;
    }

    .nb-section-help {
      display: inline-flex;
      width: 18px;
      height: 18px;
      align-items: center;
      justify-content: center;
      margin-left: 6px;
      border: 1px solid #cfe0d9;
      border-radius: 999px;
      color: var(--green);
      background: #f8fcf9;
      font-size: 11px;
      font-weight: 950;
      cursor: help;
      vertical-align: middle;
    }

    .nb-mini-timeline summary {
      cursor: pointer;
      color: var(--ink);
      font-weight: 900;
    }

    .nb-mini-timeline ol {
      margin: 10px 0 0;
      padding-left: 20px;
    }

    .nb-material-dot {
      color: #c47a1a;
      font-size: 13px;
      cursor: help;
    }

    .nb-reading-material-buttons {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      justify-content: flex-start;
      margin-top: 8px;
    }

    .nb-reading-side {
      color: var(--muted);
      opacity: 0.78;
    }

    .nb-reading-side code {
      display: inline-block;
      margin: 2px 2px 2px 0;
      padding: 1px 5px;
      border-radius: 5px;
      color: #56635e;
      background: #eef3f0;
      font-size: 11px;
    }
"""


def r6n_r3_surface() -> str:
    return r'''    function r6nR3Help(text) {
      return `<span class="nb-section-help" title="${html(text)}">?</span>`;
    }

    function r6nR3MaterialActions() {
      const actions = [
        ["上传教材目录", "帮助小教确认单元位置和前后课关系。"],
        ["上传单元页", "帮助小教理解单元目标和教材活动。"],
        ["粘贴单元目标", "帮助小教对齐课标与教材要求。"],
        ["补充已有安排", "保留你的教学设想。"],
        ["先按临时判断看预览", "不会写入正式备课本，后面仍需教师确认。"]
      ];
      return actions.map(([label, note]) => `
        <button class="node-action secondary" type="button" data-pending="${html(note)}">${iconButtonLabel(label, label.includes("上传") ? "upload" : "arrow")}</button>
      `).join("");
    }

    function renderBigUnitPrepSurface(view) {
      return `
        <section class="nb-workspace" aria-label="大单元设计">
          <div class="nb-hero">
            <div>
              <div class="nb-kicker">备课室 · 大单元设计</div>
              <div class="nb-title">第一单元 · 多变的色彩</div>
              <div class="nb-light-tags">
                <span class="nb-light-tag">大单元</span>
                <span class="nb-light-tag" title="当前内容仅为预览候选，教师确认前不写入正式备课本。">● 预览</span>
              </div>
            </div>
            <div class="nb-hero-actions">
              <button class="node-action primary" data-pending="已生成大单元预览，教师确认前不写入正式备课本。">${iconButtonLabel("生成大单元预览", "check")}</button>
              <button class="node-action secondary" data-clear-big-unit="true">${iconButtonLabel("回到当前课时", "arrow")}</button>
            </div>
          </div>

          <article class="nb-unit-reading-doc" data-r6n-r3-minimal-reading-page="true">
            <section class="nb-unit-reading-section">
              <span class="nb-section-no">01</span>
              <div>
                <h3>课标依据 ${r6nR3Help("只显示课标方向，不展开课标原文；详细依据在右侧折叠区。")}</h3>
                <p>本单元主要关联审美感知、艺术表现、创意实践，文化理解作轻量渗透。</p>
                <p>具体课标原文待教材/资料确认，当前先按课标方向生成预览。</p>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">02</span>
              <div>
                <h3>核心素养 ${r6nR3Help("把审美感知、艺术表现、创意实践、文化理解转成学生可观察的学习表现。")}</h3>
                <ul>
                  <li>审美感知：感受不同色彩组合带来的冷暖、轻重、热烈、安静等视觉意味。</li>
                  <li>艺术表现：选择一组颜色表达明确感觉，并说明选择理由。</li>
                  <li>创意实践：在比较和反馈中调整色彩搭配。</li>
                  <li>文化理解：发现色彩感受与生活场景、作品情境有关。</li>
                </ul>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">03</span>
              <div>
                <h3>学生起点 ${r6nR3Help("说明学生已有基础和最容易卡住的地方。")}</h3>
                <p>学生能说出“红色热闹、蓝色安静”等直观感受，但容易停留在“好看、鲜艳、漂亮”。本单元重点帮助学生从“我觉得”走向“我能说明为什么”。</p>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">04</span>
              <div>
                <h3>单元问题 ${r6nR3Help("问题要有美术学科性，指向色彩表达，不做术语问答。")}</h3>
                <ul>
                  <li>颜色为什么会让人产生不同感觉？</li>
                  <li>我们怎样用颜色把一种感觉表达出来？</li>
                  <li>改动一处颜色，画面的意味为什么会变化？</li>
                </ul>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">05</span>
              <div>
                <h3>表现任务 ${r6nR3Help("作为单元结果证据，不是复杂大项目。")}</h3>
                <p>完成一件“色彩感觉”小作品，并用一句话说明：我用了哪些颜色；我想表达什么感觉；我为什么这样搭配。</p>
                <p>如果时间允许，再根据同伴或教师反馈调整一处颜色，并说明为什么改。</p>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">06</span>
              <div>
                <h3>学习推进 ${r6nR3Help("默认只显示轻时间线，展开后再看每一步。")}</h3>
                <details class="nb-mini-timeline">
                  <summary>感受 → 比较 → 表现 → 修订</summary>
                  <ol>
                    <li>感受：看生活图片、作品、色卡或真实物件，先说直观感受。</li>
                    <li>比较：比较不同色彩组合，发现颜色搭配变化会改变画面感觉。</li>
                    <li>表现：用一组颜色表达一种明确感觉，完成色彩实验或小作品。</li>
                    <li>修订：展示作品，说出选择理由，根据反馈调整一处颜色。</li>
                  </ol>
                </details>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">07</span>
              <div>
                <h3>评价证据 ${r6nR3Help("评价不只看最后作品，也看观察、说明、记录和调整。")}</h3>
                <ul>
                  <li>能说出色彩感觉。</li>
                  <li>能说明选色理由。</li>
                  <li>学习单留下观察记录。</li>
                  <li>作品呈现明确意味。</li>
                  <li>能根据反馈调整一处颜色。</li>
                </ul>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">08</span>
              <div>
                <h3>材料支架 ${r6nR3Help("技能训练和艺术语言运用不能丢，材料与评价支架要可用。")}</h3>
                <p>生活色彩图片；艺术作品图像；色卡组合；学生作品正反例；简短学习单；展示评价句式。</p>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">09</span>
              <div>
                <h3>资料补充 <span class="nb-material-dot" title="补充教材目录、单元页或教参目标后，单元设计会更贴合教材。">●</span></h3>
                <div class="nb-reading-material-buttons">${r6nR3MaterialActions()}</div>
              </div>
            </section>
          </article>
        </section>
      `;
    }'''


def r6n_r3_right_panel() -> str:
    return r'''    function renderBigUnitPrepRightPanel(view) {
      return `
        <aside class="nb-right-rail" aria-label="大单元只读依据">
          <section class="nb-drawer nb-reading-side">
            <div class="nb-drawer-title"><span>依据</span><span class="quiet-tag">默认折叠</span></div>
            <details>
              <summary>查看课标方向、教材候选和风险提醒</summary>
              <p>课标方向：审美感知、艺术表现、创意实践、文化理解轻量渗透。</p>
              <p>教材候选：第一单元 多变的色彩；具体版本、单元页和教参目标待教师补充。</p>
              <p>风险提醒：当前为预览候选，不写正式备课本，不生成正式大单元正文。</p>
              <p><code>unit_theme</code><code>big_idea</code><code>student_context</code><code>performance_task</code><code>learning_stages</code></p>
            </details>
          </section>
        </aside>
      `;
    }'''


def build_html(output_root: Path) -> str:
    base = output_root / R6N_R2_DIR_NAME / "prep_room_render_canvas_deepen_v1_R6N_R2_centered_page_left_aligned_text.html"
    source = base.read_text(encoding="utf-8")
    source = source.replace("师维 · 备课室 | R6N_R2 居中版心左对齐文本", "师维 · 备课室 | R6N_R3 大单元阅读面")
    source = source.replace("\n  </style>", r6n_r3_css() + "\n  </style>", 1)
    source = replace_block(source, "    function r6nR1Explain(text) {", "    function renderBigUnitPrepRightPanel(view) {", r6n_r3_surface())
    source = replace_block(source, "    function renderBigUnitPrepRightPanel(view) {", "    function renderPrepNotebookBigUnitCanvas(view) {", r6n_r3_right_panel())
    source = source.replace('data-r6n-r2-left-aligned-text="true"', 'data-r6n-r2-left-aligned-text="true" data-r6n-r3-minimal-copy="true"')
    source = source.replace(
        "<!-- 1013I_R6N_R2: centered page block with left-aligned text; preview only, no runtime/provider/formal apply. -->",
        "<!-- 1013I_R6N_R3: minimal copy reading surface; preview only, no runtime/provider/formal apply. -->",
    )
    return source


def extract_function_body(source: str, name: str, next_name: str) -> str:
    start = source.index(f"    function {name}")
    end = source.index(f"    function {next_name}", start)
    return source[start:end]


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
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6N_R3_{viewport['id']}.png"
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
    body = extract_function_body(html_text, "renderBigUnitPrepSurface(view)", "renderBigUnitPrepRightPanel(view)")
    hits = [key for key in RAW_KEYS if key in body]
    titles = ["课标依据", "核心素养", "学生起点", "单元问题", "表现任务", "学习推进", "评价证据", "材料支架", "资料补充"]
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "html_fixture_created": html_path.exists(),
        "long_intro_removed": "先搭好这个单元的学习路线，再进入每一课的具体备课" not in body and "先把这个单元的学习路线搭起来，再进入每一课的具体备课" not in body,
        "status_bar_lightweight": "● 预览" in body and "当前内容仅为预览候选" in body and "nb-state-bar" not in body,
        "hover_explanations_used": html_text.count("nb-section-help") >= 2 and "把审美感知、艺术表现、创意实践、文化理解转成学生可观察的学习表现" in body,
        "main_reading_surface_minimal": all(title in body for title in titles) and "大段课标原文" not in body,
        "teacher_content_first": "核心素养" in body and "审美感知：感受不同色彩组合" in body and "评价证据" in body,
        "reference_details_collapsed": "<details>" in extract_function_body(html_text, "renderBigUnitPrepRightPanel(view)", "renderPrepNotebookBigUnitCanvas(view)"),
        "missing_materials_as_light_actions": all(text in html_text for text in ["上传教材目录", "上传单元页", "粘贴单元目标", "补充已有安排", "先按临时判断看预览"]),
        "raw_fields_not_primary_surface": hits == [],
        "main_surface_raw_engineering_field_hits": hits,
        "learning_progress_collapsed": "<details class=\"nb-mini-timeline\">" in body and "<summary>感受 → 比较 → 表现 → 修订</summary>" in body,
        "left_unit_entry_kept": "data-big-unit-entry" in html_text and "nb-unit-entry-badge" in html_text,
        "single_lesson_entries_kept": "data-node^='nb-lesson'" in html_text,
        "top_level_nav_not_modified": "大单元</a>" not in html_text,
        "screenshot_smoke_pass": visual_smoke.get("screenshot_smoke_pass") is True,
        "screenshot_count": len(visual_smoke.get("screenshots", [])),
        "secret_scan_hits": [],
        **boundary(),
    }
    required = [
        "html_fixture_created",
        "long_intro_removed",
        "status_bar_lightweight",
        "hover_explanations_used",
        "main_reading_surface_minimal",
        "teacher_content_first",
        "reference_details_collapsed",
        "missing_materials_as_light_actions",
        "raw_fields_not_primary_surface",
        "learning_progress_collapsed",
        "left_unit_entry_kept",
        "single_lesson_entries_kept",
        "top_level_nav_not_modified",
        "screenshot_smoke_pass",
    ]
    failures = [key for key in required if result.get(key) is not True]
    if hits:
        failures.append("main_surface_raw_engineering_field_hits")
    result["failed_checks"] = failures
    result["final_status"] = FINAL_STATUS if not failures else "FAIL_1013I_R6N_R3_BIG_UNIT_DESIGN_READING_SURFACE_MINIMAL_COPY"
    return result


def write_docs(output_root: Path, stage_dir: Path, result: dict[str, Any]) -> None:
    latest = f"""# Latest Review Entry

```text
REVIEW_STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_RECOMMENDED_STAGE={NEXT_STAGE}
LONG_INTRO_REMOVED={str(result["long_intro_removed"]).lower()}
STATUS_BAR_LIGHTWEIGHT={str(result["status_bar_lightweight"]).lower()}
HOVER_EXPLANATIONS_USED={str(result["hover_explanations_used"]).lower()}
MAIN_READING_SURFACE_MINIMAL={str(result["main_reading_surface_minimal"]).lower()}
TEACHER_CONTENT_FIRST={str(result["teacher_content_first"]).lower()}
REFERENCE_DETAILS_COLLAPSED={str(result["reference_details_collapsed"]).lower()}
MISSING_MATERIALS_AS_LIGHT_ACTIONS={str(result["missing_materials_as_light_actions"]).lower()}
RAW_FIELDS_NOT_PRIMARY_SURFACE={str(result["raw_fields_not_primary_surface"]).lower()}
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Summary

R6N_R3 rebuilds the big-unit page as a minimal reading surface. The main area shows teacher-facing content first; explanations move to hover marks, status becomes light tags, and source details stay collapsed on the right.
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "README.md", f"""# PREP_ROOM_RENDER_CANVAS_DEEPEN_V1

Current stage: `{STAGE_ID}`

R6N_R3 is a minimal-copy big-unit design reading surface: short section titles, content first, hover explanations, collapsed references, and light material actions.
""")
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", f"""# Review Package Manifest

```text
current_stage={STAGE_ID}
final_status={result["final_status"]}
main_project_pushed=false
```

## Key Files

```text
{STAGE_DIR_NAME}/{HTML_NAME}
{STAGE_DIR_NAME}/1013I_R6N_R3_result.json
{STAGE_DIR_NAME}/1013I_R6N_R3_report.md
scripts/{VALIDATOR_NAME}
source_delta_1013I_R6N_R3/scripts/{VALIDATOR_NAME}
```
""")
    write_text(stage_dir / "1013I_R6N_R3_report.md", f"""# 1013I_R6N_R3 Report

This patch converts the big-unit page to a minimal reading surface.

- long intro removed: `{result["long_intro_removed"]}`
- status bar lightweight: `{result["status_bar_lightweight"]}`
- hover explanations used: `{result["hover_explanations_used"]}`
- teacher content first: `{result["teacher_content_first"]}`
- reference details collapsed: `{result["reference_details_collapsed"]}`
- screenshot smoke pass: `{result["screenshot_smoke_pass"]}`

Boundary: no runtime, provider/model, formal apply, database, memory, Feishu, or main-project push.
""")


def validate_result(result: dict[str, Any]) -> None:
    if result.get("failed_checks"):
        raise SystemExit("R6N_R3 validation failed: " + ", ".join(result["failed_checks"]))


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
    write_json(stage_dir / "visual_smoke_1013I_R6N_R3.json", visual_smoke)
    result = build_result(html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([html_path])
    write_json(stage_dir / "1013I_R6N_R3_result.json", result)
    write_json(stage_dir / "minimal_copy_reading_surface_manifest_1013I_R6N_R3.json", {"stage": STAGE_ID, "inherits_from": INHERITS_FROM, "boundary": boundary()})
    write_docs(output_root, stage_dir, result)
    source_delta = output_root / "source_delta_1013I_R6N_R3" / "scripts"
    source_delta.mkdir(parents=True, exist_ok=True)
    target = source_delta / VALIDATOR_NAME
    if Path(__file__).resolve() != target:
        shutil.copy2(Path(__file__).resolve(), target)
    result = build_result(html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([html_path, output_root / "LATEST_REVIEW_ENTRY.md", output_root / "README.md"])
    write_json(stage_dir / "1013I_R6N_R3_result.json", result)
    write_docs(output_root, stage_dir, result)
    validate_result(result)
    print("ALL_1013I_R6N_R3_BIG_UNIT_DESIGN_READING_SURFACE_MINIMAL_COPY_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["final_status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
