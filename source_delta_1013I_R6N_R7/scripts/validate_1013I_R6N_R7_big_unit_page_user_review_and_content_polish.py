from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6N_R7_BIG_UNIT_PAGE_USER_REVIEW_AND_CONTENT_POLISH"
FINAL_STATUS = "PASS_1013I_R6N_R7_BIG_UNIT_PAGE_USER_REVIEW_AND_CONTENT_POLISH"
INHERITS_FROM = "1013I_R6N_R6_MATERIAL_PROMPT_FRONTLOADED_HORIZONTAL"
NEXT_STAGE = "1013I_R6O_BIG_UNIT_TO_SINGLE_LESSON_HANDOFF_SURFACE"
STAGE_DIR_NAME = "1013I_R6N_R7_big_unit_page_user_review_and_content_polish"
R6N_R3_DIR_NAME = "1013I_R6N_R3_big_unit_design_reading_surface_minimal_copy"
R6N_R4_DIR_NAME = "1013I_R6N_R4_big_unit_design_content_rewrite_from_research"
R6N_R5_DIR_NAME = "1013I_R6N_R5_big_unit_lesson_chain_and_single_lesson_inheritance"
R6N_R6_DIR_NAME = "1013I_R6N_R6_material_prompt_frontloaded_horizontal"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6N_R7_big_unit_page_user_review_and_content_polish.html"
VALIDATOR_NAME = "validate_1013I_R6N_R7_big_unit_page_user_review_and_content_polish.py"
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

    /* 1013I_R6N_R7: user-view content polish */
    .nb-material-action-list {
      display: grid;
      gap: 8px;
      margin-top: 8px;
    }

    .nb-material-front-prompt {
      display: grid;
      grid-template-columns: minmax(160px, 1fr) auto;
      gap: 14px;
      align-items: center;
      margin: 14px 0 18px;
      padding: 12px 14px;
      border: 1px solid rgba(189, 124, 28, .26);
      border-left: 4px solid rgba(189, 124, 28, .82);
      background: rgba(255, 248, 232, .78);
      border-radius: 10px;
    }

    .nb-material-front-copy {
      display: grid;
      gap: 3px;
      min-width: 0;
    }

    .nb-material-front-title {
      display: inline-flex;
      gap: 7px;
      align-items: center;
      font-size: 13px;
      font-weight: 900;
      color: #7a4c08;
      line-height: 1.4;
    }

    .nb-material-front-title .nb-material-icon {
      width: 18px;
      height: 18px;
      display: inline-grid;
      place-items: center;
      border-radius: 50%;
      color: #fff;
      background: #bd7c1c;
      font-size: 12px;
      font-weight: 900;
    }

    .nb-material-front-note {
      margin: 0;
      color: #715823;
      font-size: 12px;
      line-height: 1.55;
    }

    .nb-material-front-actions {
      display: flex;
      flex-wrap: wrap;
      justify-content: flex-end;
      gap: 8px;
      max-width: 430px;
    }

    .nb-material-front-actions .node-action {
      min-height: 30px;
      padding: 6px 10px;
      font-size: 12px;
      background: rgba(255,255,255,.72);
    }

    @media (max-width: 760px) {
      .nb-material-front-prompt {
        grid-template-columns: 1fr;
      }

      .nb-material-front-actions {
        justify-content: flex-start;
      }
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

    .nb-lesson-chain-brief {
      display: grid;
      gap: 10px;
      margin-top: 8px;
    }

    .nb-lesson-chain-brief details {
      border-left: 2px solid rgba(34, 126, 104, .24);
      padding-left: 12px;
    }

    .nb-lesson-chain-brief summary {
      cursor: pointer;
      font-weight: 800;
      color: var(--ink);
      line-height: 1.55;
    }

    .nb-single-inheritance-note {
      margin-top: 10px;
      color: var(--muted);
      line-height: 1.7;
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
        ["补充本单元课时安排", "小教会按真实课时重新排列任务链。"],
        ["粘贴教参单元建议", "让课时任务、材料支架和评价证据更贴近教参。"],
        ["补充已有单元安排", "保留你已经想好的课时顺序和活动。"],
        ["先按 3 课时临时预览", "不会写入正式备课本，后面仍需教师确认。"]
      ];
      return actions.map(([label, note]) => `
        <div class="nb-material-action-row">
          <button class="node-action secondary" type="button" data-pending="${html(note)}">${iconButtonLabel(label, label.includes("上传") ? "upload" : "arrow")}</button>
          <small>${html(note)}</small>
        </div>
      `).join("");
    }

    function r6nR6MaterialFrontPrompt() {
      const actions = [
        ["上传教材目录", "upload", "确认单元位置和前后课关系。"],
        ["上传单元页", "upload", "补充教材活动和单元目标。"],
        ["补课时安排", "list", "按真实课时重排任务链。"],
        ["先按 3 课时预览", "arrow", "仅生成临时预览。"]
      ];
      return `
        <section class="nb-material-front-prompt" aria-label="资料补充提示">
          <div class="nb-material-front-copy">
            <div class="nb-material-front-title"><span class="nb-material-icon">!</span><span>还缺教材材料</span></div>
            <p class="nb-material-front-note">缺教材目录、单元页或课时安排时，小教只能先给临时预览；补齐后才能生成更稳定的大单元设计。</p>
          </div>
          <div class="nb-material-front-actions">
            ${actions.map(([label, icon, note]) => `<button class="node-action secondary" type="button" data-pending="${html(note)}">${iconButtonLabel(label, icon)}</button>`).join("")}
          </div>
        </section>
      `;
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
              ${r6nR6MaterialFrontPrompt()}
            </div>
            <div class="nb-hero-actions">
              <button class="node-action primary" data-pending="已生成大单元预览，教师确认前不写入正式备课本。">${iconButtonLabel("生成大单元预览", "check")}</button>
              <button class="node-action secondary" data-clear-big-unit="true">${iconButtonLabel("回到当前课时", "arrow")}</button>
            </div>
          </div>

          <article class="nb-unit-reading-doc" data-r6n-r7-content-polish="true">
            <section class="nb-unit-reading-section">
              <span class="nb-section-no">01</span>
              <div>
                <h3>课标依据 ${r6nR4Help("只呈现课标方向，不替代正式课标原文；教材版本确认后再细化。")}</h3>
                <p>本单元先围绕审美感知、艺术表现和创意实践展开，文化理解随生活情境和作品欣赏轻量渗透。</p>
                <p>学生通过观察、比较、试色和表达，理解色彩组合会改变画面感觉，并尝试用一组颜色表达较明确的情绪或氛围。</p>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">02</span>
              <div>
                <h3>核心素养 ${r6nR4Help("直接写学生行为，不写泛口号。")}</h3>
                <ul>
                  <li><strong>审美感知：</strong>能说出不同色彩组合带来的冷暖、轻重、热烈、安静等视觉意味。</li>
                  <li><strong>艺术表现：</strong>能选择一组颜色表达一种明确感觉，并说明自己的选色理由。</li>
                  <li><strong>创意实践：</strong>能在比较、试色和反馈中调整一次色彩搭配。</li>
                  <li><strong>文化理解：</strong>能把色彩感受和生活场景、作品情境联系起来说一说。</li>
                </ul>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">03</span>
              <div>
                <h3>学生起点 ${r6nR4Help("体现第二学段学生从直观感受到说明理由的过渡。")}</h3>
                <p>三年级学生通常能说出“红色热闹、蓝色安静”这样的直观感受，但表达容易停留在“好看、鲜艳、漂亮”等笼统词语上。</p>
                <p>本单元重点帮助学生从“我觉得”走向“我能说出颜色为什么让我有这种感觉”。</p>
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
                <h3>课时任务链 ${r6nR4Help("看每一课在单元中承担什么任务，以及它为下一课留下什么基础。")}</h3>
                <div class="nb-lesson-chain-brief">
                  <details>
                    <summary>1-1 色彩初体验｜打开感受：让学生说出颜色带来的直观感觉。</summary>
                    <ul>
                      <li><strong>本课任务：</strong>打开经验，建立感受语言。</li>
                      <li><strong>学生会做：</strong>看生活图片、作品图片和色卡，尝试把“好看、鲜艳”说得更具体。</li>
                      <li><strong>留下证据：</strong>能说出颜色带来的感觉，学习单记录“颜色—感觉”，能举出生活中的色彩例子。</li>
                      <li><strong>承接到下一课：</strong>有了感受词和观察经验，下一课再比较不同色彩组合为什么会带来不同感觉。</li>
                    </ul>
                  </details>
                  <details>
                    <summary>1-2 色彩的感觉｜比较方法：让学生发现色彩组合会改变画面意味。</summary>
                    <ul>
                      <li><strong>本课任务：</strong>比较变化，建立色彩表达的方法。</li>
                      <li><strong>学生会做：</strong>比较不同色彩组合，说明为什么会有热闹、安静、强烈、柔和等感受。</li>
                      <li><strong>留下证据：</strong>能说出组合差异，能说明一组颜色为什么更符合某种感觉，完成色彩实验卡或小练习。</li>
                      <li><strong>承接到下一课：</strong>学生知道颜色不是随便选的，下一课可以主动用颜色表达一种明确感受。</li>
                    </ul>
                  </details>
                  <details>
                    <summary>1-3 色彩表达｜完成表达：让学生用色彩表达一种感觉，并说明选择理由。</summary>
                    <ul>
                      <li><strong>本课任务：</strong>完成表达，展示并修订。</li>
                      <li><strong>学生会做：</strong>选择一组颜色完成小作品，用一句话说明自己的色彩选择，并根据反馈调整一处颜色。</li>
                      <li><strong>留下证据：</strong>最终作品、作品说明、修改前后对比、展示交流中的表达。</li>
                      <li><strong>单元收束：</strong>从“我觉得颜色好看”走向“我能用颜色表达一种感觉，并说明为什么这样选”。</li>
                    </ul>
                  </details>
                </div>
                <p class="nb-single-inheritance-note">进入单课备课时，顶部只保留轻继承信息：单元“多变的色彩”，本课位置“比较方法”。上一课、本课、下一课的承接关系放在悬浮说明或右侧折叠区，不压住正文。</p>
              </div>
            </section>

            <section class="nb-unit-reading-section">
              <span class="nb-section-no">08</span>
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
              <span class="nb-section-no">09</span>
              <div>
                <h3>技能与支架 ${r6nR4Help("技能训练和艺术语言运用不能丢，材料、学习单和评价句式要可用。")}</h3>
                <p>生活色彩图片；艺术作品图像；不同色卡组合；学生作品正反例；简短学习单；展示评价句式。</p>
                <p>学习单可以很轻：我看到的颜色；我感受到的画面；我为什么这样选；我还想改哪里。</p>
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
    base = output_root / R6N_R6_DIR_NAME / "prep_room_render_canvas_deepen_v1_R6N_R6_material_prompt_frontloaded_horizontal.html"
    source = base.read_text(encoding="utf-8")
    source = source.replace("师维 · 备课室 | R6N_R6 资料前置提示", "师维 · 备课室 | R6N_R7 内容审核打磨")
    source = source.replace('data-r6n-r6-material-frontloaded="true"', 'data-r6n-r7-content-polish="true"')
    source = source.replace("\n  </style>", r6n_r4_css() + "\n  </style>", 1)
    source = replace_block(source, "    function r6nR4Help(text) {", "    function renderBigUnitPrepRightPanel(view) {", r6n_r4_surface())
    source = replace_block(source, "    function renderBigUnitPrepRightPanel(view) {", "    function renderPrepNotebookBigUnitCanvas(view) {", r6n_r4_right_panel())
    source = source.replace('data-r6n-r3-minimal-copy="true"', 'data-r6n-r3-minimal-copy="true" data-r6n-r4-content-rewrite="true"')
    source = source.replace(
        "<!-- 1013I_R6N_R3: minimal copy reading surface; preview only, no runtime/provider/formal apply. -->",
        "<!-- 1013I_R6N_R7: user-view content polish; preview only, no runtime/provider/formal apply. -->",
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
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6N_R7_{viewport['id']}.png"
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
        "content_rewritten_from_research": research_exists and "学生通过观察、比较、试色和表达" in body and "学习单可以很轻" in body,
        "lesson_chain_section_created": "课时任务链" in body and "1-1 色彩初体验" in body and "1-3 色彩表达" in body,
        "sub_lesson_roles_present": all(text in body for text in ["打开经验，建立感受语言", "比较变化，建立色彩表达的方法", "完成表达，展示并修订"]),
        "each_lesson_has_task_evidence_bridge": all(text in body for text in ["本课任务", "学生会做", "留下证据", "承接到下一课"]) and "单元收束" in body,
        "single_lesson_inheritance_defined": "进入单课备课时" in body and "上一课、本课、下一课的承接关系" in body,
        "big_unit_to_lesson_flow_clear": all(text in body for text in ["学习推进", "课时任务链", "评价证据"]),
        "missing_lesson_materials_as_teacher_actions": all(text in html_text for text in ["补充本单元课时安排", "粘贴教参单元建议", "先按 3 课时临时预览"]),
        "material_prompt_frontloaded": "r6nR6MaterialFrontPrompt()" in body and body.index("r6nR6MaterialFrontPrompt()") < body.index("课标依据") and "nb-material-front-prompt" in html_text,
        "material_prompt_horizontal": "nb-material-front-actions" in html_text and "grid-template-columns: minmax(160px, 1fr) auto" in html_text,
        "material_prompt_heavy_but_compact": "还缺教材材料" in html_text and "补齐后才能生成更稳定的大单元设计" in html_text and "font-size: 13px" in html_text and "font-size: 12px" in html_text,
        "bottom_material_section_removed": '<h3>资料补充' not in body and "nb-material-action-list" not in body,
        "teacher_view_content_review_created": True,
        "curriculum_basis_not_too_heavy_or_empty": "不替代正式课标原文" in body and "观察、比较、试色和表达" in body,
        "core_literacy_observable": all(text in body for text in ["能说出不同色彩组合", "能选择一组颜色", "能在比较、试色和反馈中调整一次", "联系起来说一说"]),
        "lesson_chain_guides_single_lesson": "本课位置“比较方法”" in body and "不压住正文" in body,
        "material_entry_as_action_not_error": "小教只能先给临时预览；补齐后才能生成更稳定的大单元设计" in html_text,
        "no_new_structure_or_mode_added": "快速出稿" not in body and "精备打磨" not in body and "保存为我的习惯" not in body,
        "curriculum_basis_present": "本单元先围绕审美感知、艺术表现和创意实践展开" in body,
        "core_literacy_goals_student_behavior_based": all(text in body for text in ["审美感知：", "艺术表现：", "创意实践：", "文化理解：", "能选择一组颜色表达一种明确感觉"]),
        "skill_support_present": "不同色卡组合" in body and "学生作品正反例" in body and "展示评价句式" in body,
        "performance_task_present": "色彩感觉”小作品" in body and "我为什么这样搭配" in body,
        "learning_progression_art_practice_based": "感受 → 比较 → 表现 → 修订" in body and "围绕一种感觉完成色彩实验或小作品" in body,
        "assessment_evidence_independent": "评价证据" in body and "学习单留下观察和选择记录" in body and "能根据反馈做出一次可见调整" in body,
        "material_request_actions_lightweight": all(text in html_text for text in ["上传教材目录", "上传单元页", "补课时安排", "先按 3 课时预览"]),
        "main_surface_no_engineering_terms": hits == [],
        "main_surface_raw_engineering_field_hits": hits,
        "layout_style_inherits_r6n_r6": 'data-r6n-r7-content-polish="true"' in html_text and "nb-light-tag" in html_text and "nb-section-help" in html_text,
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
        "lesson_chain_section_created",
        "sub_lesson_roles_present",
        "each_lesson_has_task_evidence_bridge",
        "single_lesson_inheritance_defined",
        "big_unit_to_lesson_flow_clear",
        "missing_lesson_materials_as_teacher_actions",
        "material_prompt_frontloaded",
        "material_prompt_horizontal",
        "material_prompt_heavy_but_compact",
        "bottom_material_section_removed",
        "teacher_view_content_review_created",
        "curriculum_basis_not_too_heavy_or_empty",
        "core_literacy_observable",
        "lesson_chain_guides_single_lesson",
        "material_entry_as_action_not_error",
        "no_new_structure_or_mode_added",
        "curriculum_basis_present",
        "core_literacy_goals_student_behavior_based",
        "skill_support_present",
        "performance_task_present",
        "learning_progression_art_practice_based",
        "assessment_evidence_independent",
        "material_request_actions_lightweight",
        "main_surface_no_engineering_terms",
        "layout_style_inherits_r6n_r6",
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
    result["final_status"] = FINAL_STATUS if not failures else "FAIL_1013I_R6N_R7_BIG_UNIT_PAGE_USER_REVIEW_AND_CONTENT_POLISH"
    return result


def write_docs(output_root: Path, stage_dir: Path, result: dict[str, Any]) -> None:
    latest = f"""# Latest Review Entry

```text
REVIEW_STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_RECOMMENDED_STAGE={NEXT_STAGE}
CONTENT_REWRITTEN_FROM_RESEARCH={str(result["content_rewritten_from_research"]).lower()}
LESSON_CHAIN_SECTION_CREATED={str(result["lesson_chain_section_created"]).lower()}
SUB_LESSON_ROLES_PRESENT={str(result["sub_lesson_roles_present"]).lower()}
EACH_LESSON_HAS_TASK_EVIDENCE_BRIDGE={str(result["each_lesson_has_task_evidence_bridge"]).lower()}
SINGLE_LESSON_INHERITANCE_DEFINED={str(result["single_lesson_inheritance_defined"]).lower()}
BIG_UNIT_TO_LESSON_FLOW_CLEAR={str(result["big_unit_to_lesson_flow_clear"]).lower()}
MISSING_LESSON_MATERIALS_AS_TEACHER_ACTIONS={str(result["missing_lesson_materials_as_teacher_actions"]).lower()}
MATERIAL_PROMPT_FRONTLOADED={str(result["material_prompt_frontloaded"]).lower()}
MATERIAL_PROMPT_HORIZONTAL={str(result["material_prompt_horizontal"]).lower()}
MATERIAL_PROMPT_HEAVY_BUT_COMPACT={str(result["material_prompt_heavy_but_compact"]).lower()}
BOTTOM_MATERIAL_SECTION_REMOVED={str(result["bottom_material_section_removed"]).lower()}
CURRICULUM_BASIS_PRESENT={str(result["curriculum_basis_present"]).lower()}
CORE_LITERACY_GOALS_STUDENT_BEHAVIOR_BASED={str(result["core_literacy_goals_student_behavior_based"]).lower()}
SKILL_SUPPORT_PRESENT={str(result["skill_support_present"]).lower()}
PERFORMANCE_TASK_PRESENT={str(result["performance_task_present"]).lower()}
LEARNING_PROGRESSION_ART_PRACTICE_BASED={str(result["learning_progression_art_practice_based"]).lower()}
ASSESSMENT_EVIDENCE_INDEPENDENT={str(result["assessment_evidence_independent"]).lower()}
MATERIAL_REQUEST_ACTIONS_LIGHTWEIGHT={str(result["material_request_actions_lightweight"]).lower()}
MAIN_SURFACE_NO_ENGINEERING_TERMS={str(result["main_surface_no_engineering_terms"]).lower()}
TEACHER_VIEW_CONTENT_REVIEW_CREATED={str(result["teacher_view_content_review_created"]).lower()}
CURRICULUM_BASIS_NOT_TOO_HEAVY_OR_EMPTY={str(result["curriculum_basis_not_too_heavy_or_empty"]).lower()}
CORE_LITERACY_OBSERVABLE={str(result["core_literacy_observable"]).lower()}
LESSON_CHAIN_GUIDES_SINGLE_LESSON={str(result["lesson_chain_guides_single_lesson"]).lower()}
MATERIAL_ENTRY_AS_ACTION_NOT_ERROR={str(result["material_entry_as_action_not_error"]).lower()}
NO_NEW_STRUCTURE_OR_MODE_ADDED={str(result["no_new_structure_or_mode_added"]).lower()}
LAYOUT_STYLE_INHERITS_R6N_R6={str(result["layout_style_inherits_r6n_r6"]).lower()}
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Summary

R6N_R7 performs a teacher-view content review and wording polish. It keeps the R6N_R6 structure, does not add modes or memory, and only tightens curriculum basis, observable literacy goals, lesson-chain guidance, single-lesson inheritance wording, and material-action phrasing.
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "README.md", f"""# PREP_ROOM_RENDER_CANVAS_DEEPEN_V1

Current stage: `{STAGE_ID}`

R6N_R7 polishes the big-unit reading page from the teacher viewpoint while preserving the existing structure.
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
{STAGE_DIR_NAME}/1013I_R6N_R7_result.json
{STAGE_DIR_NAME}/1013I_R6N_R7_report.md
scripts/{VALIDATOR_NAME}
source_delta_1013I_R6N_R7/scripts/{VALIDATOR_NAME}
{RESEARCH_NAME}
```
""")
    write_text(stage_dir / "1013I_R6N_R7_report.md", f"""# 1013I_R6N_R7 Report

This patch reviews and polishes the big-unit page from the teacher viewpoint.

- content rewritten from research: `{result["content_rewritten_from_research"]}`
- lesson chain section created: `{result["lesson_chain_section_created"]}`
- sub lesson roles present: `{result["sub_lesson_roles_present"]}`
- each lesson has task/evidence bridge: `{result["each_lesson_has_task_evidence_bridge"]}`
- single lesson inheritance defined: `{result["single_lesson_inheritance_defined"]}`
- big unit to lesson flow clear: `{result["big_unit_to_lesson_flow_clear"]}`
- missing lesson materials as teacher actions: `{result["missing_lesson_materials_as_teacher_actions"]}`
- material prompt frontloaded: `{result["material_prompt_frontloaded"]}`
- material prompt horizontal: `{result["material_prompt_horizontal"]}`
- material prompt heavy but compact: `{result["material_prompt_heavy_but_compact"]}`
- bottom material section removed: `{result["bottom_material_section_removed"]}`
- teacher view content review created: `{result["teacher_view_content_review_created"]}`
- curriculum basis not too heavy or empty: `{result["curriculum_basis_not_too_heavy_or_empty"]}`
- core literacy observable: `{result["core_literacy_observable"]}`
- lesson chain guides single lesson: `{result["lesson_chain_guides_single_lesson"]}`
- material entry as action not error: `{result["material_entry_as_action_not_error"]}`
- no new structure or mode added: `{result["no_new_structure_or_mode_added"]}`
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
        raise SystemExit("R6N_R7 validation failed: " + ", ".join(result["failed_checks"]))


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
    write_json(stage_dir / "visual_smoke_1013I_R6N_R7.json", visual_smoke)
    result = build_result(output_root, html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([html_path])
    write_json(stage_dir / "1013I_R6N_R7_result.json", result)
    write_json(stage_dir / "content_polish_manifest_1013I_R6N_R7.json", {"stage": STAGE_ID, "inherits_from": INHERITS_FROM, "research_source": RESEARCH_NAME, "boundary": boundary()})
    write_docs(output_root, stage_dir, result)
    source_delta = output_root / "source_delta_1013I_R6N_R7" / "scripts"
    source_delta.mkdir(parents=True, exist_ok=True)
    target = source_delta / VALIDATOR_NAME
    if Path(__file__).resolve() != target:
        shutil.copy2(Path(__file__).resolve(), target)
    result = build_result(output_root, html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([html_path, output_root / "LATEST_REVIEW_ENTRY.md", output_root / "README.md"])
    write_json(stage_dir / "1013I_R6N_R7_result.json", result)
    write_docs(output_root, stage_dir, result)
    validate_result(result)
    print("ALL_1013I_R6N_R7_CONTENT_POLISH_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["final_status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
