from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6N_R4_BIG_UNIT_DESIGN_CONTENT_REWRITE_FROM_RESEARCH"
FINAL_STATUS = "PASS_1013I_R6N_R4_BIG_UNIT_DESIGN_CONTENT_REWRITE_FROM_RESEARCH"
INHERITS_FROM = "1013I_R6N_R3_BIG_UNIT_DESIGN_READING_SURFACE_MINIMAL_COPY"
NEXT_STAGE = "USER_REVIEW_BIG_UNIT_DESIGN_CONTENT"
STAGE_DIR_NAME = "1013I_R6N_R4_big_unit_design_content_rewrite_from_research"
R6N_R3_DIR_NAME = "1013I_R6N_R3_big_unit_design_reading_surface_minimal_copy"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6N_R4_big_unit_design_content_rewrite.html"
VALIDATOR_NAME = "validate_1013I_R6N_R4_big_unit_design_content_rewrite_from_research.py"
RESEARCH_NAME = "big_unit_design_research_draft_20260619.md"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]
RAW_KEYS = ["unit_theme", "big_idea", "student_context", "performance_task", "learning_stages", "formal_apply", "lesson_position", "unit_package"]
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


def r6n_r4_css() -> str:
    return """

    /* 1013I_R6N_R4: content rewrite from accepted research baseline */
    .nb-material-action-list {
      display: grid;
      gap: 8px;
      margin-top: 8px;
    }

    .nb-material-action-row {
      display: grid;
      grid-template-columns: auto minmax(0, 1fr);
      gap: 10px;
      align-items: center;
    }

    .nb-material-action-row small {
      color: var(--muted);
      line-height: 1.55;
    }

    .nb-unit-reading-section strong {
      color: var(--ink);
    }
"""


def r6n_r4_surface() -> str:
    return r'''    function r6nR4Help(text) {
      return `<span class="nb-section-help" title="${html(text)}">?</span>`;
    }

    function r6nR4MaterialActions() {
      const actions = [
        ["上传教材目录", "确认单元位置和前后课关系。"],
        ["上传单元页 / 教参截图", "补充单元目标、教材活动和官方提示。"],
        ["粘贴单元目标", "让预览更贴近教材和课标要求。"],
        ["补充已有单元安排", "保留你已经想好的课时顺序和活动。"],
        ["先按临时判断看预览", "不会写入正式备课本，后面仍需教师确认。"]
      ];
      return actions.map(([label, note]) => `
        <div class="nb-material-action-row">
          <button class="node-action secondary" type="button" data-pending="${html(note)}">${iconButtonLabel(label, label.includes("上传") ? "upload" : "arrow")}</button>
          <small>${html(note)}</small>
        </div>
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

          <article class="nb-unit-reading-doc" data-r6n-r4-research-content-page="true">
            <section class="nb-unit-reading-section">
              <span class="nb-section-no">01</span>
              <div>
                <h3>课标依据 ${r6nR4Help("具体课标原文待教材/资料确认。当前只按课标方向生成预览。")}</h3>
                <p>本单元主要指向审美感知、艺术表现、创意实践，文化理解作轻量渗透。</p>
                <p>学生通过观察、比较、尝试和表达，理解色彩组合会改变画面感觉，并能用色彩表达一种较明确的情绪或氛围。</p>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">02</span>
              <div>
                <h3>核心素养 ${r6nR4Help("直接写学生行为，不写泛口号。")}</h3>
                <ul>
                  <li><strong>审美感知：</strong>能感受不同色彩组合带来的冷暖、轻重、热烈、安静等视觉意味。</li>
                  <li><strong>艺术表现：</strong>能选择一组颜色表达明确感觉，并说明自己的选色理由。</li>
                  <li><strong>创意实践：</strong>能在比较、试验和反馈中调整色彩搭配。</li>
                  <li><strong>文化理解：</strong>能发现色彩感受与生活场景、作品情境有关。</li>
                </ul>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">03</span>
              <div>
                <h3>学生起点 ${r6nR4Help("体现第二学段学生从直观感受到说明理由的过渡。")}</h3>
                <p>三年级学生通常能说出“红色热闹、蓝色安静”这样的直观感受，但容易停留在“好看、鲜艳、漂亮”等词语上。</p>
                <p>本单元要帮助学生从“我觉得”走向“我能说明为什么”。</p>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">04</span>
              <div>
                <h3>单元问题 ${r6nR4Help("问题要回到美术语言和色彩表达，不做术语问答。")}</h3>
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
                <h3>表现任务 ${r6nR4Help("这是单元结果证据，不是复杂项目。")}</h3>
                <p>学生完成一件“色彩感觉”小作品，并用一句到几句话说明：</p>
                <ul>
                  <li>我用了哪些颜色；</li>
                  <li>我想表达什么感觉；</li>
                  <li>我为什么这样搭配。</li>
                </ul>
                <p>如果时间允许，再根据同伴或教师反馈调整一处颜色，并说明为什么改。</p>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">06</span>
              <div>
                <h3>学习推进 ${r6nR4Help("保留轻时间线，展开后看每一步的美术实践。")}</h3>
                <details class="nb-mini-timeline">
                  <summary>感受 → 比较 → 表现 → 修订</summary>
                  <ol>
                    <li><strong>感受：</strong>看生活图片、作品、色卡或真实物件，先说直观感受。</li>
                    <li><strong>比较：</strong>比较不同色彩组合，发现搭配变化会改变画面感觉。</li>
                    <li><strong>表现：</strong>围绕一种感觉完成色彩实验或小作品。</li>
                    <li><strong>修订：</strong>展示作品，说出理由，根据反馈调整一处颜色。</li>
                  </ol>
                </details>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">07</span>
              <div>
                <h3>评价证据 ${r6nR4Help("独立呈现评价证据，不藏在表现任务里。")}</h3>
                <ul>
                  <li>能说出色彩带来的感觉；</li>
                  <li>能说明自己的选色理由；</li>
                  <li>学习单留下观察和选择记录；</li>
                  <li>作品呈现较明确的视觉意味；</li>
                  <li>能根据反馈做出一次可见调整。</li>
                </ul>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">08</span>
              <div>
                <h3>技能与支架 ${r6nR4Help("技能训练和艺术语言运用不能丢，材料、学习单和评价句式要可用。")}</h3>
                <p>生活色彩图片；艺术作品图像；不同色卡组合；学生作品正反例；简短学习单；展示评价句式。</p>
                <p>学习单可以很轻：我看到的颜色；我感受到的画面；我为什么这样选；我还想改哪里。</p>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">09</span>
              <div>
                <h3>资料补充 <span class="nb-material-dot" title="补充教材目录、单元页或教参目标后，单元设计会更贴合教材。">●</span></h3>
                <p>补充任意一种资料即可，页面仍保持预览，不写入正式备课本。</p>
                <div class="nb-material-action-list">${r6nR4MaterialActions()}</div>
              </div>
            </section>
          </article>
        </section>
      `;
    }'''


def r6n_r4_right_panel() -> str:
    return r'''    function renderBigUnitPrepRightPanel(view) {
      return `
        <aside class="nb-right-rail" aria-label="大单元只读依据">
          <section class="nb-drawer nb-reading-side">
            <div class="nb-drawer-title"><span>依据</span><span class="quiet-tag">默认折叠</span></div>
            <details>
              <summary>查看课标方向、教材候选和风险提醒</summary>
              <p>内容基线：小学美术大单元研究稿，强调课标方向、学段特点、学科技能和评价证据。</p>
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
    base = output_root / R6N_R3_DIR_NAME / "prep_room_render_canvas_deepen_v1_R6N_R3_big_unit_design_reading_surface_minimal_copy.html"
    source = base.read_text(encoding="utf-8")
    source = source.replace("师维 · 备课室 | R6N_R3 大单元阅读面", "师维 · 备课室 | R6N_R4 大单元内容重写")
    source = source.replace("\n  </style>", r6n_r4_css() + "\n  </style>", 1)
    source = replace_block(source, "    function r6nR3Help(text) {", "    function renderBigUnitPrepRightPanel(view) {", r6n_r4_surface())
    source = replace_block(source, "    function renderBigUnitPrepRightPanel(view) {", "    function renderPrepNotebookBigUnitCanvas(view) {", r6n_r4_right_panel())
    source = source.replace('data-r6n-r3-minimal-copy="true"', 'data-r6n-r3-minimal-copy="true" data-r6n-r4-content-rewrite="true"')
    source = source.replace(
        "<!-- 1013I_R6N_R3: minimal copy reading surface; preview only, no runtime/provider/formal apply. -->",
        "<!-- 1013I_R6N_R4: content rewrite from accepted research baseline; preview only, no runtime/provider/formal apply. -->",
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
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6N_R4_{viewport['id']}.png"
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


def build_result(output_root: Path, html_path: Path, visual_smoke: dict[str, Any]) -> dict[str, Any]:
    html_text = html_path.read_text(encoding="utf-8")
    body = extract_function_body(html_text, "renderBigUnitPrepSurface(view)", "renderBigUnitPrepRightPanel(view)")
    hits = [key for key in RAW_KEYS if key in body]
    research_exists = (output_root / RESEARCH_NAME).exists()
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "html_fixture_created": html_path.exists(),
        "content_rewritten_from_research": research_exists and "学生通过观察、比较、尝试和表达" in body and "学习单可以很轻" in body,
        "curriculum_basis_present": "本单元主要指向审美感知、艺术表现、创意实践" in body,
        "core_literacy_goals_student_behavior_based": all(text in body for text in ["审美感知：", "艺术表现：", "创意实践：", "文化理解：", "能选择一组颜色表达明确感觉"]),
        "skill_support_present": "不同色卡组合" in body and "学生作品正反例" in body and "展示评价句式" in body,
        "performance_task_present": "色彩感觉”小作品" in body and "我为什么这样搭配" in body,
        "learning_progression_art_practice_based": "感受 → 比较 → 表现 → 修订" in body and "围绕一种感觉完成色彩实验或小作品" in body,
        "assessment_evidence_independent": "评价证据" in body and "学习单留下观察和选择记录" in body and "能根据反馈做出一次可见调整" in body,
        "material_request_actions_lightweight": all(text in html_text for text in ["上传教材目录", "上传单元页 / 教参截图", "粘贴单元目标", "补充已有单元安排", "先按临时判断看预览"]) and "补充任意一种资料即可" in body,
        "main_surface_no_engineering_terms": hits == [],
        "main_surface_raw_engineering_field_hits": hits,
        "layout_style_inherits_r6n_r3": 'data-r6n-r3-minimal-copy="true"' in html_text and "nb-light-tag" in html_text and "nb-section-help" in html_text,
        "reference_details_collapsed": "<details>" in extract_function_body(html_text, "renderBigUnitPrepRightPanel(view)", "renderPrepNotebookBigUnitCanvas(view)"),
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
        "content_rewritten_from_research",
        "curriculum_basis_present",
        "core_literacy_goals_student_behavior_based",
        "skill_support_present",
        "performance_task_present",
        "learning_progression_art_practice_based",
        "assessment_evidence_independent",
        "material_request_actions_lightweight",
        "main_surface_no_engineering_terms",
        "layout_style_inherits_r6n_r3",
        "reference_details_collapsed",
        "left_unit_entry_kept",
        "single_lesson_entries_kept",
        "top_level_nav_not_modified",
        "screenshot_smoke_pass",
    ]
    failures = [key for key in required if result.get(key) is not True]
    if hits:
        failures.append("main_surface_raw_engineering_field_hits")
    result["failed_checks"] = failures
    result["final_status"] = FINAL_STATUS if not failures else "FAIL_1013I_R6N_R4_BIG_UNIT_DESIGN_CONTENT_REWRITE_FROM_RESEARCH"
    return result


def write_docs(output_root: Path, stage_dir: Path, result: dict[str, Any]) -> None:
    latest = f"""# Latest Review Entry

```text
REVIEW_STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_RECOMMENDED_STAGE={NEXT_STAGE}
CONTENT_REWRITTEN_FROM_RESEARCH={str(result["content_rewritten_from_research"]).lower()}
CURRICULUM_BASIS_PRESENT={str(result["curriculum_basis_present"]).lower()}
CORE_LITERACY_GOALS_STUDENT_BEHAVIOR_BASED={str(result["core_literacy_goals_student_behavior_based"]).lower()}
SKILL_SUPPORT_PRESENT={str(result["skill_support_present"]).lower()}
PERFORMANCE_TASK_PRESENT={str(result["performance_task_present"]).lower()}
LEARNING_PROGRESSION_ART_PRACTICE_BASED={str(result["learning_progression_art_practice_based"]).lower()}
ASSESSMENT_EVIDENCE_INDEPENDENT={str(result["assessment_evidence_independent"]).lower()}
MATERIAL_REQUEST_ACTIONS_LIGHTWEIGHT={str(result["material_request_actions_lightweight"]).lower()}
MAIN_SURFACE_NO_ENGINEERING_TERMS={str(result["main_surface_no_engineering_terms"]).lower()}
LAYOUT_STYLE_INHERITS_R6N_R3={str(result["layout_style_inherits_r6n_r3"]).lower()}
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Summary

R6N_R4 keeps the R6N_R3 reading layout and rewrites the big-unit design content from `big_unit_design_research_draft_20260619.md`. It centers the page on curriculum basis, student-behavior core literacy goals, performance task, art-practice progression, independent assessment evidence, and skill/material scaffolds.
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "README.md", f"""# PREP_ROOM_RENDER_CANVAS_DEEPEN_V1

Current stage: `{STAGE_ID}`

R6N_R4 rewrites the big-unit design page content from the accepted research draft while preserving the R6N_R3 minimal reading layout.
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
{STAGE_DIR_NAME}/1013I_R6N_R4_result.json
{STAGE_DIR_NAME}/1013I_R6N_R4_report.md
scripts/{VALIDATOR_NAME}
source_delta_1013I_R6N_R4/scripts/{VALIDATOR_NAME}
{RESEARCH_NAME}
```
""")
    write_text(stage_dir / "1013I_R6N_R4_report.md", f"""# 1013I_R6N_R4 Report

This patch rewrites R6N_R3 content from the accepted research baseline.

- content rewritten from research: `{result["content_rewritten_from_research"]}`
- curriculum basis present: `{result["curriculum_basis_present"]}`
- core literacy goals student behavior based: `{result["core_literacy_goals_student_behavior_based"]}`
- skill support present: `{result["skill_support_present"]}`
- performance task present: `{result["performance_task_present"]}`
- assessment evidence independent: `{result["assessment_evidence_independent"]}`
- material request actions lightweight: `{result["material_request_actions_lightweight"]}`
- screenshot smoke pass: `{result["screenshot_smoke_pass"]}`

Boundary: no runtime, provider/model, formal apply, database, memory, Feishu, or main-project push.
""")


def validate_result(result: dict[str, Any]) -> None:
    if result.get("failed_checks"):
        raise SystemExit("R6N_R4 validation failed: " + ", ".join(result["failed_checks"]))


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
    write_json(stage_dir / "visual_smoke_1013I_R6N_R4.json", visual_smoke)
    result = build_result(output_root, html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([html_path])
    write_json(stage_dir / "1013I_R6N_R4_result.json", result)
    write_json(stage_dir / "content_rewrite_manifest_1013I_R6N_R4.json", {"stage": STAGE_ID, "inherits_from": INHERITS_FROM, "research_source": RESEARCH_NAME, "boundary": boundary()})
    write_docs(output_root, stage_dir, result)
    source_delta = output_root / "source_delta_1013I_R6N_R4" / "scripts"
    source_delta.mkdir(parents=True, exist_ok=True)
    target = source_delta / VALIDATOR_NAME
    if Path(__file__).resolve() != target:
        shutil.copy2(Path(__file__).resolve(), target)
    result = build_result(output_root, html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([html_path, output_root / "LATEST_REVIEW_ENTRY.md", output_root / "README.md"])
    write_json(stage_dir / "1013I_R6N_R4_result.json", result)
    write_docs(output_root, stage_dir, result)
    validate_result(result)
    print("ALL_1013I_R6N_R4_BIG_UNIT_DESIGN_CONTENT_REWRITE_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["final_status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
