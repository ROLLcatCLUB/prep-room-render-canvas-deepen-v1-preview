from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6N_R1_CENTERED_NUMBERED_TEXT_READING_PATCH"
FINAL_STATUS = "PASS_1013I_R6N_R1_CENTERED_NUMBERED_TEXT_READING_PATCH"
INHERITS_FROM = "1013I_R6N_BIG_UNIT_DESIGN_TEXT_READING_PATCH_FOR_REVIEW"
NEXT_STAGE = "USER_REVIEW_BIG_UNIT_TEXT_READING_PAGE"
STAGE_DIR_NAME = "1013I_R6N_R1_centered_numbered_text_reading_patch"
R6N_DIR_NAME = "1013I_R6N_big_unit_design_text_reading_patch_for_review"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6N_R1_centered_numbered_text_reading.html"
VALIDATOR_NAME = "validate_1013I_R6N_R1_centered_numbered_text_reading_patch.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]

RAW_KEYS = ["unit_theme", "big_idea", "essential_question", "student_context", "performance_task", "learning_stages", "formal_apply"]
SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_.-]{20,}"),
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


def replace_block(source: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = source.index(start_marker)
    end = source.index(end_marker, start)
    return source[:start] + replacement.rstrip() + "\n\n" + source[end:]


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


def r6n_r1_css() -> str:
    return """

    /* 1013I_R6N_R1: centered, numbered text-reading patch */
    .nb-unit-reading-doc {
      max-width: 720px;
      margin: 0 auto;
      padding: 8px 0 32px;
    }

    .nb-unit-reading-head {
      text-align: center;
      margin-bottom: 18px;
      padding-bottom: 16px;
      border-bottom: 1px solid rgba(43, 124, 106, 0.16);
    }

    .nb-unit-reading-head h2 {
      margin: 0 0 8px;
      color: var(--ink);
      font-size: 24px;
      line-height: 1.25;
      font-weight: 950;
    }

    .nb-unit-reading-head p {
      max-width: 560px;
      margin: 0 auto;
      color: var(--muted);
      line-height: 1.75;
    }

    .nb-unit-reading-section {
      display: grid;
      grid-template-columns: 48px minmax(0, 1fr);
      gap: 14px;
      padding: 20px 0;
      border-top: 1px solid rgba(43, 124, 106, 0.13);
    }

    .nb-unit-reading-section:first-of-type {
      border-top: 0;
    }

    .nb-section-no {
      width: 40px;
      height: 40px;
      display: grid;
      place-items: center;
      border-radius: 50%;
      color: #fff;
      background: var(--green);
      font-size: 14px;
      font-weight: 950;
      letter-spacing: 0;
    }

    .nb-unit-reading-section h3 {
      margin: 0 0 8px;
      color: var(--ink);
      font-size: 20px;
      line-height: 1.35;
      font-weight: 950;
    }

    .nb-unit-reading-section p {
      margin: 0 0 10px;
      color: #20372f;
      font-size: 15px;
      line-height: 1.95;
    }

    .nb-section-explain {
      display: inline-flex;
      margin-left: 6px;
      color: var(--green);
      font-size: 12px;
      font-weight: 850;
      cursor: help;
      vertical-align: middle;
    }

    .nb-reading-actions,
    .nb-reading-material-buttons {
      justify-content: center;
    }

    @media (max-width: 900px) {
      .nb-unit-reading-doc {
        max-width: 100%;
      }
      .nb-unit-reading-section {
        grid-template-columns: 38px minmax(0, 1fr);
        gap: 10px;
      }
      .nb-section-no {
        width: 32px;
        height: 32px;
        font-size: 12px;
      }
    }
"""


def r6n_r1_surface() -> str:
    return r'''    function r6nR1Explain(text) {
      return `<span class="nb-section-explain" title="${html(text)}">说明</span>`;
    }

    function r6nR1MaterialActions() {
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
              <span class="quiet-tag">居中文本阅读</span>
            </div>
          </div>

          <article class="nb-unit-reading-doc" data-r6n-r1-centered-numbered-page="true">
            <header class="nb-unit-reading-head">
              <h2>把“多变的色彩”设计成一条从感受到表达的学习路线</h2>
              <p>先把这个单元的学习路线搭起来，再进入每一课的具体备课。</p>
            </header>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">01</span>
              <div>
                <h3>单元方向 ${r6nR1Explain("这个单元想带学生走向哪里：默认只读生成后的方向判断；字段线索放在旁注里。")}</h3>
                <p>这个单元可以围绕“色彩为什么会给人不同感觉”展开。学生不只是认识颜色名称，而是逐步学会观察、比较、表达色彩带来的情绪和视觉感受。</p>
                <p>如果把这组课连起来看，前面的课可以先打开学生对色彩变化的感受，中间让学生比较不同颜色组合带来的差异，后面再进入有目的的色彩表现。这样进入单课备课时，每一课都能知道自己在单元里承担什么。</p>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">02</span>
              <div>
                <h3>学生起点 ${r6nR1Explain("说明学生已有基础、可能卡住的地方，以及和本单元有关的生活经验。")}</h3>
                <p>三年级学生通常能说出“红色热闹、蓝色安静”这样的直观感受，但容易停留在颜色名称，不能说明为什么有这种感觉。本单元要帮助学生从“我觉得好看”走向“我能说出色彩搭配带来的感觉”。</p>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">03</span>
              <div>
                <h3>表现任务 ${r6nR1Explain("说明学生最后完成什么、学完能看出什么、怎么判断完成得好不好。")}</h3>
                <p>单元最后可以让学生完成一件以“色彩感觉”为主题的小作品，并用一两句话说明自己的色彩选择。评价时不只看画得整不整齐，更要看学生能不能把颜色选择和想表达的感觉联系起来。</p>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">04</span>
              <div>
                <h3>学习推进 ${r6nR1Explain("说明学习阶段、学习任务、小问题、学习活动和学习评价。")}</h3>
                <p>第一步先感受：让学生从生活图片、作品图片或色卡中说出直观感觉。第二步再比较：让学生比较不同色彩组合带来的差异，并尝试说出原因。第三步尝试表现：让学生用一组颜色表达一个明确感受。第四步交流修改：让学生展示作品，说出色彩选择，并根据同伴反馈做小调整。</p>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">05</span>
              <div>
                <h3>课堂支架 ${r6nR1Explain("说明情境、任务、资源、策略、学习单、评价和学评一致。")}</h3>
                <p>可以准备一组生活色彩图片、一组艺术作品图片和几张色卡。学习单不要复杂，只让学生记录“我看到的颜色 / 我感受到的感觉 / 我选择这样搭配的理由”。评价时围绕“颜色选择是否和想表达的感觉有关”展开，让学生知道该往哪里改。</p>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">06</span>
              <div>
                <h3>资料补充</h3>
                <p>小教还需要一点资料，才能把这个单元设计得更准。你可以补教材目录、单元页、教参截图或已有单元安排；也可以先按临时判断生成预览，后面再确认。</p>
                <div class="nb-reading-material-buttons">${r6nR1MaterialActions()}</div>
              </div>
            </section>
          </article>
        </section>
      `;
    }'''


def build_html(output_root: Path) -> str:
    base = output_root / R6N_DIR_NAME / "prep_room_render_canvas_deepen_v1_R6N_big_unit_design_text_reading.html"
    source = base.read_text(encoding="utf-8")
    source = source.replace("师维 · 备课室 | R6N 文本式大单元设计本", "师维 · 备课室 | R6N_R1 居中序号文本")
    source = source.replace("\n  </style>", r6n_r1_css() + "\n  </style>", 1)
    source = replace_block(source, "    function r6nTip(label, tip) {", "    function renderBigUnitPrepRightPanel(view) {", r6n_r1_surface())
    source = source.replace('data-r6n-text-reading-static="true"', 'data-r6n-text-reading-static="true" data-r6n-r1-centered-numbered-static="true"')
    source = source.replace(
        "<!-- 1013I_R6N: text-reading big-unit design patch; preview only, no runtime/provider/formal apply. -->",
        "<!-- 1013I_R6N_R1: centered numbered text-reading patch; preview only, no runtime/provider/formal apply. -->",
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
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6N_R1_{viewport['id']}.png"
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
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "html_fixture_created": html_path.exists(),
        "centered_reading_doc": "margin: 0 auto;" in html_text and "nb-unit-reading-head" in html_text,
        "numbered_sections_present": all(f">{i:02d}<" in body for i in range(1, 7)),
        "section_titles_corrected": all(text in body for text in ["单元方向", "学生起点", "表现任务", "学习推进", "课堂支架", "资料补充"]),
        "old_explanation_not_section_title": "<h3>这个单元想带学生走向哪里" not in body and "这个单元想带学生走向哪里：" in body,
        "duplicate_unit_title_removed": body.count("第一单元 · 多变的色彩") == 1,
        "card_layout_removed_from_primary_surface": all(token not in body for token in ["nb-unit-design-section", "nb-unit-design-chip", "nb-bigunit-card"]),
        "main_surface_raw_engineering_field_hits": hits,
        "engineering_fields_not_primary_surface": hits == [],
        "left_unit_entry_kept": "data-big-unit-entry" in html_text and "nb-unit-entry-badge" in html_text,
        "single_lesson_entries_kept": "data-node^='nb-lesson'" in html_text,
        "top_level_nav_not_modified": "大单元</a>" not in html_text,
        "preview_only_badges_visible": "教师确认前不写入正式备课本" in html_text,
        "screenshot_smoke_pass": visual_smoke.get("screenshot_smoke_pass") is True,
        "screenshot_count": len(visual_smoke.get("screenshots", [])),
        "secret_scan_hits": [],
        **boundary(),
    }
    required = [
        "html_fixture_created",
        "centered_reading_doc",
        "numbered_sections_present",
        "section_titles_corrected",
        "old_explanation_not_section_title",
        "duplicate_unit_title_removed",
        "card_layout_removed_from_primary_surface",
        "engineering_fields_not_primary_surface",
        "left_unit_entry_kept",
        "single_lesson_entries_kept",
        "top_level_nav_not_modified",
        "preview_only_badges_visible",
        "screenshot_smoke_pass",
    ]
    failures = [key for key in required if result.get(key) is not True]
    if hits:
        failures.append("main_surface_raw_engineering_field_hits")
    result["failed_checks"] = failures
    result["final_status"] = FINAL_STATUS if not failures else "FAIL_1013I_R6N_R1_CENTERED_NUMBERED_TEXT_READING_PATCH"
    return result


def write_docs(output_root: Path, stage_dir: Path, result: dict[str, Any]) -> None:
    latest = f"""# Latest Review Entry

```text
REVIEW_STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_RECOMMENDED_STAGE={NEXT_STAGE}
CENTERED_READING_DOC={str(result["centered_reading_doc"]).lower()}
NUMBERED_SECTIONS_PRESENT={str(result["numbered_sections_present"]).lower()}
SECTION_TITLES_CORRECTED={str(result["section_titles_corrected"]).lower()}
OLD_EXPLANATION_NOT_SECTION_TITLE={str(result["old_explanation_not_section_title"]).lower()}
CARD_LAYOUT_REMOVED_FROM_PRIMARY_SURFACE={str(result["card_layout_removed_from_primary_surface"]).lower()}
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Summary

R6N_R1 centers the text-reading page and turns the body into numbered sections. `单元方向` and `学生起点` are the section names; `这个单元想带学生走向哪里` is only a hover explanation, not a visible section title.
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "README.md", f"""# PREP_ROOM_RENDER_CANVAS_DEEPEN_V1

Current stage: `{STAGE_ID}`

R6N_R1 centers the big-unit text-reading page, adds numbered sections, and fixes the heading hierarchy so teacher-facing chapters are `单元方向 / 学生起点 / 表现任务 / 学习推进 / 课堂支架 / 资料补充`.
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
{STAGE_DIR_NAME}/1013I_R6N_R1_result.json
{STAGE_DIR_NAME}/1013I_R6N_R1_report.md
scripts/{VALIDATOR_NAME}
source_delta_1013I_R6N_R1/scripts/{VALIDATOR_NAME}
```
""")
    write_text(stage_dir / "1013I_R6N_R1_report.md", f"""# 1013I_R6N_R1 Report

This patch fixes the text-reading hierarchy:

- centered reading document: `{result["centered_reading_doc"]}`
- numbered sections present: `{result["numbered_sections_present"]}`
- section titles corrected: `{result["section_titles_corrected"]}`
- old explanation no longer section title: `{result["old_explanation_not_section_title"]}`
- card layout removed: `{result["card_layout_removed_from_primary_surface"]}`

Boundary: no runtime, provider/model, formal apply, database, memory, Feishu, or main-project push.
""")


def validate_result(result: dict[str, Any]) -> None:
    if result.get("failed_checks"):
        raise SystemExit("R6N_R1 validation failed: " + ", ".join(result["failed_checks"]))


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
    write_json(stage_dir / "visual_smoke_1013I_R6N_R1.json", visual_smoke)
    result = build_result(html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([html_path])
    write_json(stage_dir / "1013I_R6N_R1_result.json", result)
    write_json(stage_dir / "centered_numbered_text_patch_manifest_1013I_R6N_R1.json", {"stage": STAGE_ID, "inherits_from": INHERITS_FROM, "boundary": boundary()})
    write_docs(output_root, stage_dir, result)
    source_delta = output_root / "source_delta_1013I_R6N_R1" / "scripts"
    source_delta.mkdir(parents=True, exist_ok=True)
    target = source_delta / VALIDATOR_NAME
    if Path(__file__).resolve() != target:
        shutil.copy2(Path(__file__).resolve(), target)
    result = build_result(html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([html_path, output_root / "LATEST_REVIEW_ENTRY.md", output_root / "README.md"])
    write_json(stage_dir / "1013I_R6N_R1_result.json", result)
    write_docs(output_root, stage_dir, result)
    validate_result(result)
    print("ALL_1013I_R6N_R1_CENTERED_NUMBERED_TEXT_READING_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["final_status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
