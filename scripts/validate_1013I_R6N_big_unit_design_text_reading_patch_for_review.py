from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6N_BIG_UNIT_DESIGN_TEXT_READING_PATCH_FOR_REVIEW"
FINAL_STATUS = "PASS_1013I_R6N_BIG_UNIT_DESIGN_TEXT_READING_PATCH_FOR_REVIEW"
INHERITS_FROM = "1013I_R6M_BIG_UNIT_DESIGN_TEACHER_READABLE_STATIC_PATCH_FOR_REVIEW"
NEXT_STAGE = "USER_REVIEW_BIG_UNIT_TEXT_READING_PAGE"
STAGE_DIR_NAME = "1013I_R6N_big_unit_design_text_reading_patch_for_review"
R6M_DIR_NAME = "1013I_R6M_big_unit_design_teacher_readable_static_patch_for_review"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6N_big_unit_design_text_reading.html"
VALIDATOR_NAME = "validate_1013I_R6N_big_unit_design_text_reading_patch_for_review.py"

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
    "student_context",
    "performance_task",
    "unit_learning_goals",
    "assessment_criteria",
    "learning_stages",
    "stage_tasks",
    "stage_questions",
    "learning_activities",
    "stage_assessment",
    "unit_process_summary",
    "context_scaffold",
    "task_scaffold",
    "resource_scaffold",
    "strategy_scaffold",
    "worksheet_support",
    "assessment_scaffold",
    "learning_assessment_alignment",
    "formal_apply",
]

SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)app[_-]?secret\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)tenant[_-]?access[_-]?token\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)cookie\s*[:=]\s*['\"][^'\"]{20,}"),
]


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
        "product_runtime_called": False,
        "ui_implementation_started": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "official_export_created": False,
        "official_archive_created": False,
        "main_project_pushed": False,
    }


def replace_block(source: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = source.index(start_marker)
    end = source.index(end_marker, start)
    return source[:start] + replacement.rstrip() + "\n\n" + source[end:]


def r6n_css() -> str:
    return """

    /* 1013I_R6N text-reading patch: no section cards, no visible field chips */
    .nb-unit-reading-doc {
      max-width: 760px;
      display: block;
      padding: 4px 0 28px;
    }

    .nb-unit-reading-kicker {
      margin: 0 0 8px;
      color: var(--green);
      font-size: 15px;
      font-weight: 900;
    }

    .nb-unit-reading-title {
      margin: 0 0 12px;
      color: var(--ink);
      font-size: 23px;
      line-height: 1.32;
      font-weight: 950;
    }

    .nb-unit-reading-doc p {
      margin: 0 0 13px;
      color: #20372f;
      font-size: 15px;
      line-height: 1.95;
    }

    .nb-unit-reading-doc h3 {
      margin: 24px 0 9px;
      padding-top: 12px;
      border-top: 1px solid rgba(43, 124, 106, 0.16);
      color: var(--ink);
      font-size: 18px;
      line-height: 1.35;
      font-weight: 950;
    }

    .nb-unit-reading-doc h3:first-of-type {
      margin-top: 8px;
      padding-top: 0;
      border-top: 0;
    }

    .nb-inline-note {
      display: inline-flex;
      align-items: center;
      min-height: 22px;
      margin: 0 2px;
      padding: 0 7px;
      border: 1px solid #cfe0d9;
      border-radius: 999px;
      color: var(--green);
      background: #f8fcf9;
      font-size: 12px;
      font-weight: 800;
      cursor: help;
      vertical-align: baseline;
    }

    .nb-reading-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 14px 0 18px;
      padding-bottom: 14px;
      border-bottom: 1px solid rgba(43, 124, 106, 0.12);
    }

    .nb-reading-materials {
      margin-top: 22px;
      padding: 12px 0 0;
      border-top: 1px solid rgba(43, 124, 106, 0.16);
    }

    .nb-reading-material-buttons {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
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


def r6n_surface() -> str:
    return r'''    function r6nTip(label, tip) {
      return `<span class="nb-inline-note" title="${html(tip)}">${html(label)}</span>`;
    }

    function r6nMaterialActions() {
      const actions = [
        ["上传教材目录", "帮助小教确认单元位置和前后课关系。"],
        ["上传单元页 / 教参截图", "帮助小教理解单元目标和教材活动。"],
        ["粘贴单元目标", "帮助小教对齐课标与教材要求。"],
        ["补充已有单元安排", "保留你自己的教学设想。"],
        ["先按临时判断生成预览", "允许降级预览，教师确认前不生效。"]
      ];
      return actions.map(([label, note]) => `
        <button class="node-action secondary" type="button" data-pending="${html(note)}">${iconButtonLabel(label, label.includes("上传") ? "upload" : "arrow")}</button>
      `).join("");
    }

    function renderBigUnitPrepSurface(view) {
      return `
        <section class="nb-workspace" aria-label="大单元设计本">
          <div class="nb-hero">
            <div>
              <div class="nb-kicker">备课室 · 大单元设计本</div>
              <div class="nb-title">第一单元 · 多变的色彩</div>
            </div>
            <div class="nb-hero-actions">
              <button class="node-action primary" data-pending="已生成大单元预览，教师确认前不写入正式备课本。">${iconButtonLabel("生成大单元预览", "check")}</button>
              <button class="node-action secondary" data-clear-big-unit="true">${iconButtonLabel("回到当前课时", "arrow")}</button>
            </div>
          </div>

          <div class="nb-state-bar">
            <div class="nb-state-main">
              <span class="state-tag">预览层</span>
              <span class="quiet-tag">教师确认前不写入正式备课本</span>
              <span class="quiet-tag">文本式阅读</span>
            </div>
          </div>

          <article class="nb-unit-reading-doc" data-r6n-text-reading-page="true">
            <div class="nb-unit-reading-kicker">单元方向</div>
            <h2 class="nb-unit-reading-title">把“多变的色彩”设计成一条从感受到表达的学习路线</h2>
            <p>这个单元可以围绕“色彩为什么会给人不同感觉”展开。学生不只是认识颜色名称，而是逐步学会观察、比较、表达色彩带来的情绪和视觉感受。${r6nTip("说明", "对应教师可见线索：这个单元围绕什么学 / 这个单元最终想让学生明白什么 / 用什么大问题带着学生学")}</p>
            <p>如果把这组课连起来看，前面的课可以先打开学生对色彩变化的感受，中间让学生比较不同颜色组合带来的差异，后面再进入有目的的色彩表现。这样进入单课备课时，每一课都能知道自己在单元里承担什么。</p>

            <div class="nb-reading-actions">
              <button class="node-action primary" type="button" data-pending="已生成大单元预览，教师确认前不写入正式备课本。">${iconButtonLabel("生成大单元预览", "check")}</button>
              <button class="node-action secondary" type="button" data-pending="已保存为候选，尚未写入正式备课本。">${iconButtonLabel("保存为候选", "star")}</button>
              <button class="node-action secondary" type="button" data-pending="本次暂不处理。">${iconButtonLabel("暂不处理", "arrow")}</button>
            </div>

            <h3>学生现在在哪里</h3>
            <p>三年级学生通常能说出“红色热闹、蓝色安静”这样的直观感受，但容易停留在颜色名称，不能说明为什么有这种感觉。本单元要帮助学生从“我觉得好看”走向“我能说出色彩搭配带来的感觉”。${r6nTip("学情旁注", "对应教师可见线索：学生已有基础 / 学生可能卡住的地方 / 和本单元有关的生活经验")}</p>

            <h3>学生最后要完成什么</h3>
            <p>单元最后可以让学生完成一件以“色彩感觉”为主题的小作品，并用一两句话说明自己的色彩选择。评价时不只看画得整不整齐，更要看学生能不能把颜色选择和想表达的感觉联系起来。${r6nTip("任务旁注", "对应教师可见线索：最后完成什么作品或展示 / 学完能看出什么 / 怎么判断完成得好不好")}</p>

            <h3>单元怎么一步步推进</h3>
            <p>第一步先感受：让学生从生活图片、作品图片或色卡中说出直观感觉。第二步再比较：让学生比较不同色彩组合带来的差异，并尝试说出原因。第三步尝试表现：让学生用一组颜色表达一个明确感受。第四步交流修改：让学生展示作品，说出色彩选择，并根据同伴反馈做小调整。${r6nTip("推进旁注", "对应教师可见线索：学习阶段 / 学习任务 / 小问题 / 学习活动 / 学习评价 / 单元教学过程摘要")}</p>

            <h3>老师需要准备哪些支架</h3>
            <p>可以准备一组生活色彩图片、一组艺术作品图片和几张色卡。学习单不要复杂，只让学生记录“我看到的颜色 / 我感受到的感觉 / 我选择这样搭配的理由”。评价时围绕“颜色选择是否和想表达的感觉有关”展开，让学生知道该往哪里改。${r6nTip("支架旁注", "对应教师可见线索：情境支架 / 任务支架 / 资源支架 / 策略支架 / 学习单 / 评价支架 / 学评一致")}</p>

            <div class="nb-reading-materials">
              <div class="nb-unit-reading-kicker">资料补充</div>
              <p>小教还需要一点资料，才能把这个单元设计得更准。你可以补教材目录、单元页、教参截图或已有单元安排；也可以先按临时判断生成预览，后面再确认。</p>
              <div class="nb-reading-material-buttons">${r6nMaterialActions()}</div>
            </div>
          </article>
        </section>
      `;
    }'''


def r6n_right_panel() -> str:
    return r'''    function renderBigUnitPrepRightPanel(view) {
      return `
        <aside class="nb-right-rail" aria-label="大单元只读依据">
          <section class="nb-drawer nb-reading-side">
            <div class="nb-drawer-title"><span>只读依据</span><span class="quiet-tag">默认折叠</span></div>
            <p>主阅读区只保留连续文本。字段来源和风险提醒放在这里，供审阅追溯。</p>
            <details>
              <summary>查看字段来源和边界</summary>
              <p><code>unit_theme</code><code>big_idea</code><code>essential_question</code></p>
              <p><code>student_context</code><code>performance_task</code><code>unit_learning_goals</code><code>assessment_criteria</code></p>
              <p><code>learning_stages</code><code>stage_tasks</code><code>stage_questions</code><code>learning_activities</code><code>stage_assessment</code><code>unit_process_summary</code></p>
              <p><code>context_scaffold</code><code>task_scaffold</code><code>resource_scaffold</code><code>strategy_scaffold</code><code>worksheet_support</code><code>assessment_scaffold</code><code>learning_assessment_alignment</code></p>
              <p>边界：只生成预览和候选；不正式生成、不写入、不应用到正式备课本。</p>
            </details>
          </section>
        </aside>
      `;
    }'''


def build_html(output_root: Path) -> str:
    base = output_root / R6M_DIR_NAME / "prep_room_render_canvas_deepen_v1_R6M_big_unit_design_teacher_readable_static.html"
    source = base.read_text(encoding="utf-8")
    source = source.replace("师维 · 备课室 | R6M 大单元设计本", "师维 · 备课室 | R6N 文本式大单元设计本")
    source = source.replace("\n  </style>", r6n_css() + "\n  </style>", 1)
    source = replace_block(source, "    function r6mChips(items) {", "    function renderBigUnitPrepRightPanel(view) {", r6n_surface())
    source = replace_block(source, "    function renderBigUnitPrepRightPanel(view) {", "    function renderPrepNotebookBigUnitCanvas(view) {", r6n_right_panel())
    source = source.replace('data-r6m-big-unit-design-static="true"', 'data-r6m-big-unit-design-static="true" data-r6n-text-reading-static="true"')
    source = source.replace(
        "<!-- 1013I_R6M: big-unit design teacher-readable static patch; preview only, no runtime/provider/formal apply. -->",
        "<!-- 1013I_R6N: text-reading big-unit design patch; preview only, no runtime/provider/formal apply. -->",
    )
    return source


def extract_function_body(source: str, name: str, next_name: str) -> str:
    start = source.index(f"    function {name}")
    end = source.index(f"    function {next_name}", start)
    return source[start:end]


def primary_body(html_text: str) -> str:
    return extract_function_body(html_text, "renderBigUnitPrepSurface(view)", "renderBigUnitPrepRightPanel(view)")


def primary_raw_hits(html_text: str) -> list[str]:
    body = primary_body(html_text)
    # title attributes are acceptable hover annotations; raw keys should still not appear there.
    return [key for key in RAW_KEYS if key in body]


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
    for viewport in [
        {"id": "desktop", "width": 1440, "height": 1100},
        {"id": "mobile", "width": 390, "height": 1100},
    ]:
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6N_{viewport['id']}.png"
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
    return {
        "screenshot_smoke_pass": all(item["bytes"] > 10000 for item in screenshots),
        "screenshot_error": None,
        "screenshots": screenshots,
    }


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
    body = primary_body(html_text)
    hits = primary_raw_hits(html_text)
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "html_fixture_created": html_path.exists(),
        "based_on_r6m_static_copy": "data-r6m-big-unit-design-static" in html_text,
        "text_reading_page_created": 'data-r6n-text-reading-page="true"' in html_text,
        "card_layout_removed_from_primary_surface": all(token not in body for token in ["nb-unit-design-section", "nb-unit-design-chip", "nb-unit-design-material", "nb-bigunit-card"]),
        "duplicate_unit_title_removed": body.count("第一单元 · 多变的色彩") == 1,
        "unit_direction_prominent": "单元方向" in body and "把“多变的色彩”设计成一条从感受到表达的学习路线" in body,
        "field_labels_moved_to_hover_notes": "nb-inline-note" in html_text and "r6nTip(\"说明\", \"对应教师可见线索" in body,
        "default_surface_is_generated_reading_text": all(text in body for text in [
            "这个单元可以围绕",
            "三年级学生通常能说出",
            "单元最后可以让学生完成",
            "第一步先感受",
            "可以准备一组生活色彩图片",
        ]),
        "main_surface_raw_engineering_field_hits": hits,
        "engineering_fields_not_primary_surface": hits == [],
        "right_reference_area_allows_raw_fields": "unit_theme" in extract_function_body(html_text, "renderBigUnitPrepRightPanel(view)", "renderPrepNotebookBigUnitCanvas(view)"),
        "left_unit_entry_kept": "data-big-unit-entry" in html_text and "nb-unit-entry-badge" in html_text,
        "single_lesson_entries_kept": "data-node^='nb-lesson'" in html_text and "已回到单课备课本" in html_text,
        "top_level_nav_not_modified": "大单元</a>" not in html_text and all(label in html_text for label in ["教室", "备课室", "课堂观察", "作品馆", "知识馆", "档案室"]),
        "material_upload_actions_present": all(text in html_text for text in ["上传教材目录", "上传单元页 / 教参截图", "粘贴单元目标", "补充已有单元安排", "先按临时判断生成预览"]),
        "preview_only_badges_visible": "教师确认前不写入正式备课本" in html_text,
        "screenshot_smoke_pass": visual_smoke.get("screenshot_smoke_pass") is True,
        "screenshot_count": len(visual_smoke.get("screenshots", [])),
        "secret_scan_hits": [],
        **boundary(),
    }
    required_true = [
        "html_fixture_created",
        "based_on_r6m_static_copy",
        "text_reading_page_created",
        "card_layout_removed_from_primary_surface",
        "duplicate_unit_title_removed",
        "unit_direction_prominent",
        "field_labels_moved_to_hover_notes",
        "default_surface_is_generated_reading_text",
        "engineering_fields_not_primary_surface",
        "right_reference_area_allows_raw_fields",
        "left_unit_entry_kept",
        "single_lesson_entries_kept",
        "top_level_nav_not_modified",
        "material_upload_actions_present",
        "preview_only_badges_visible",
        "screenshot_smoke_pass",
    ]
    failures = [key for key in required_true if result.get(key) is not True]
    if result["main_surface_raw_engineering_field_hits"]:
        failures.append("main_surface_raw_engineering_field_hits")
    result["failed_checks"] = failures
    result["final_status"] = FINAL_STATUS if not failures else "FAIL_1013I_R6N_BIG_UNIT_DESIGN_TEXT_READING_PATCH_FOR_REVIEW"
    return result


def write_docs(output_root: Path, stage_dir: Path, result: dict[str, Any]) -> None:
    latest = f"""# Latest Review Entry

```text
REVIEW_STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
LATEST_COMPLETED_BIG_UNIT_DESIGN_STATIC_PATCH=1013I_R6M_BIG_UNIT_DESIGN_TEACHER_READABLE_STATIC_PATCH_FOR_REVIEW
LATEST_COMPLETED_BIG_UNIT_TEXT_READING_PATCH={STAGE_ID}
INHERITS_FROM={INHERITS_FROM}
NEXT_RECOMMENDED_STAGE={NEXT_STAGE}
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
TEXT_READING_PAGE_CREATED={str(result["text_reading_page_created"]).lower()}
CARD_LAYOUT_REMOVED_FROM_PRIMARY_SURFACE={str(result["card_layout_removed_from_primary_surface"]).lower()}
DUPLICATE_UNIT_TITLE_REMOVED={str(result["duplicate_unit_title_removed"]).lower()}
UNIT_DIRECTION_PROMINENT={str(result["unit_direction_prominent"]).lower()}
FIELD_LABELS_MOVED_TO_HOVER_NOTES={str(result["field_labels_moved_to_hover_notes"]).lower()}
MAIN_SURFACE_RAW_ENGINEERING_FIELD_HITS={json.dumps(result["main_surface_raw_engineering_field_hits"], ensure_ascii=False)}
RUNTIME_CONNECTED=false
HTML_MODIFIED=false
```

## Summary

R6N fixes the R6M reading problem. It removes the card-like primary surface, removes the duplicate unit-title intro block, makes `单元方向` the lead, and moves field explanations into hover notes. The default surface now reads as continuous generated teacher-facing text.

## Start Here

```text
{STAGE_DIR_NAME}/1013I_R6N_report.md
{STAGE_DIR_NAME}/1013I_R6N_result.json
{STAGE_DIR_NAME}/{HTML_NAME}
{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6N_desktop.png
{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6N_mobile.png
scripts/{VALIDATOR_NAME}
```
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)

    readme = f"""# PREP_ROOM_RENDER_CANVAS_DEEPEN_V1

## Current Entry

- Current stage: `{STAGE_ID}`
- Final status: `{result["final_status"]}`
- Next stage: `{NEXT_STAGE}`

R6N changes the big-unit design page from card-by-card reading into continuous text reading. Field labels are hover notes; raw schema keys stay only in the right collapsed reference area.

## Key Files

```text
{STAGE_DIR_NAME}/{HTML_NAME}
{STAGE_DIR_NAME}/1013I_R6N_result.json
{STAGE_DIR_NAME}/1013I_R6N_report.md
{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6N_desktop.png
{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6N_mobile.png
scripts/{VALIDATOR_NAME}
```
"""
    write_text(output_root / "README.md", readme)

    manifest = f"""# Review Package Manifest

```text
package_line=PREP_ROOM_RENDER_CANVAS_DEEPEN_V1
current_stage={STAGE_ID}
final_status={result["final_status"]}
main_project_committed=false
main_project_pushed=false
```

## Current Product Baseline

R6N is a static review patch based on R6M. It removes the primary card layout and turns the big-unit design surface into a continuous text-reading page. It does not modify the original main HTML and does not connect runtime.

Recommended next stage:

```text
{NEXT_STAGE}
```

## Key Files

```text
README.md
LATEST_REVIEW_ENTRY.md
REVIEW_PACKAGE_MANIFEST.md
{STAGE_DIR_NAME}/{HTML_NAME}
{STAGE_DIR_NAME}/1013I_R6N_result.json
{STAGE_DIR_NAME}/1013I_R6N_report.md
{STAGE_DIR_NAME}/visual_smoke_1013I_R6N.json
scripts/{VALIDATOR_NAME}
source_delta_1013I_R6N/scripts/{VALIDATOR_NAME}
```
"""
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)

    report = f"""# 1013I_R6N Report

`{STAGE_ID}` patches R6M into a text-reading big-unit design page.

## Result

- Text reading page created: `{result["text_reading_page_created"]}`
- Card layout removed from primary surface: `{result["card_layout_removed_from_primary_surface"]}`
- Duplicate unit title removed: `{result["duplicate_unit_title_removed"]}`
- Unit direction prominent: `{result["unit_direction_prominent"]}`
- Field labels moved to hover notes: `{result["field_labels_moved_to_hover_notes"]}`
- Main surface raw engineering field hits: `{result["main_surface_raw_engineering_field_hits"]}`
- Screenshot smoke pass: `{result["screenshot_smoke_pass"]}`

## Boundary

No runtime, provider/model, formal apply, database, memory, Feishu, export, archive, original HTML modification, or main project push.
"""
    write_text(stage_dir / "1013I_R6N_report.md", report)


def validate_result(result: dict[str, Any]) -> None:
    if result.get("failed_checks"):
        raise SystemExit("R6N validation failed: " + ", ".join(result["failed_checks"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()

    output_root = resolve_output_root(args.root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)

    html_path = stage_dir / HTML_NAME
    write_text(html_path, build_html(output_root))
    write_json(
        stage_dir / "text_reading_patch_manifest_1013I_R6N.json",
        {
            "stage": STAGE_ID,
            "inherits_from": INHERITS_FROM,
            "primary_surface_mode": "continuous_text_reading",
            "cards_removed_from_primary_surface": True,
            "field_labels_in_hover_notes": True,
            "boundary": boundary(),
        },
    )
    visual_smoke = create_screenshots(stage_dir, html_path)
    write_json(stage_dir / "visual_smoke_1013I_R6N.json", visual_smoke)
    result = build_result(html_path, visual_smoke)
    write_json(stage_dir / "1013I_R6N_result.json", result)
    write_docs(output_root, stage_dir, result)

    source_delta = output_root / "source_delta_1013I_R6N" / "scripts"
    source_delta.mkdir(parents=True, exist_ok=True)
    current_script = Path(__file__).resolve()
    target_script = source_delta / VALIDATOR_NAME
    if current_script != target_script:
        shutil.copy2(current_script, target_script)

    result = build_result(html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([
        html_path,
        stage_dir / "1013I_R6N_report.md",
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "README.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ])
    write_json(stage_dir / "1013I_R6N_result.json", result)
    write_docs(output_root, stage_dir, result)
    validate_result(result)
    print("ALL_1013I_R6N_BIG_UNIT_DESIGN_TEXT_READING_PATCH_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["final_status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
