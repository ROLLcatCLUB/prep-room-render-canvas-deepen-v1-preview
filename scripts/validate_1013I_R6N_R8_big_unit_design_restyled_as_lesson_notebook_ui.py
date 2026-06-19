from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6N_R8_BIG_UNIT_DESIGN_RESTYLED_AS_LESSON_NOTEBOOK_UI"
FINAL_STATUS = "PASS_1013I_R6N_R8_BIG_UNIT_DESIGN_RESTYLED_AS_LESSON_NOTEBOOK_UI"
INHERITS_FROM = "1013I_R6N_R7_BIG_UNIT_PAGE_USER_REVIEW_AND_CONTENT_POLISH"
NEXT_STAGE = "USER_REVIEW_BIG_UNIT_NOTEBOOK_UI_STYLE"
STAGE_DIR_NAME = "1013I_R6N_R8_big_unit_design_restyled_as_lesson_notebook_ui"
R6N_R7_DIR_NAME = "1013I_R6N_R7_big_unit_page_user_review_and_content_polish"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6N_R8_big_unit_design_lesson_notebook_ui.html"
VALIDATOR_NAME = "validate_1013I_R6N_R8_big_unit_design_restyled_as_lesson_notebook_ui.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
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
        "standalone_static_sample": True,
        "not_integrated_into_directory": True,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "lesson_body_written": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def r6n_r8_css() -> str:
    return """

    /* 1013I_R6N_R8: big-unit page restyled as the polished single-lesson notebook UI */
    [data-r6n-r8-notebook-ui] .nb-workspace {
      padding-left: 34px;
    }

    [data-r6n-r8-notebook-ui] .nb-hero {
      border-bottom: 1px dashed rgba(36, 84, 70, .2);
      padding-bottom: 22px;
      margin-bottom: 12px;
    }

    [data-r6n-r8-notebook-ui] .nb-doc-body-surface {
      max-width: 880px;
      margin: 0 auto;
    }

    [data-r6n-r8-notebook-ui] .nb-doc-section {
      border-radius: 8px;
      background: rgba(255, 255, 252, .72);
      box-shadow: inset 0 0 0 1px rgba(38, 94, 76, .08);
    }

    [data-r6n-r8-notebook-ui] .nb-doc-section p,
    [data-r6n-r8-notebook-ui] .nb-doc-section li {
      font-size: 15px;
      line-height: 1.95;
    }

    [data-r6n-r8-notebook-ui] .nb-doc-section ul {
      margin: 10px 0 0;
      padding-left: 24px;
    }

    [data-r6n-r8-notebook-ui] .nb-doc-subnote {
      margin-top: 10px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.7;
    }

    [data-r6n-r8-notebook-ui] .nb-material-front-prompt {
      max-width: 880px;
      margin: 14px auto 18px;
    }

    [data-r6n-r8-notebook-ui] .nb-r8-inline-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 12px;
    }
"""


def big_unit_surface_and_panel() -> str:
    return r'''    function renderBigUnitPrepSurface(view) {
      const materialActions = [
        ["上传教材目录", "确认单元位置和前后课关系。"],
        ["上传单元页", "补充教材活动和单元目标。"],
        ["补课时安排", "按真实课时重排任务链。"],
        ["先按 3 课时预览", "仅生成临时预览。"]
      ];
      return `
            <section class="nb-workspace" aria-label="第一单元多变的色彩大单元设计">
              <div class="nb-hero">
                <div>
                  <div class="nb-kicker">大单元设计</div>
                  <div class="nb-title">第一单元《多变的色彩》</div>
                </div>
                <div class="nb-hero-actions">
                  <button class="node-action primary" data-pending="已保留为预览候选，教师确认前不写入正式备课本。">${iconButtonLabel("确认到预览", "check")}</button>
                  <button class="node-action secondary" data-clear-big-unit="true">${iconButtonLabel("回到当前课时", "arrow")}</button>
                </div>
              </div>

              <section class="nb-material-front-prompt" aria-label="资料补充提示">
                <div class="nb-material-front-copy">
                  <div class="nb-material-front-title"><span class="nb-material-icon">!</span><span>还缺教材材料</span></div>
                  <p class="nb-material-front-note">缺教材目录、单元页或课时安排时，小教只能先给临时预览；补齐后才能生成更稳定的大单元设计。</p>
                </div>
                <div class="nb-material-front-actions">
                  ${materialActions.map(([label, note]) => `<button class="node-action secondary" type="button" data-pending="${html(note)}">${html(label)}</button>`).join("")}
                </div>
              </section>

              <div class="nb-state-bar">
                <div class="nb-state-main">
                  <span class="state-tag">查看状态</span>
                  <span class="quiet-tag">大单元</span>
                  <span class="quiet-tag" title="当前内容仅为预览候选，教师确认前不写入正式备课本。">预览</span>
                  <span class="status-dot green"></span><span class="quiet-tag">可阅读</span>
                  <span class="status-dot amber"></span><span class="quiet-tag">资料待补充</span>
                </div>
                <div class="nb-mode-toggle" aria-label="大单元状态">
                  <button class="nb-mode-btn active" type="button">查看</button>
                  <button class="nb-mode-btn" type="button" data-pending="大单元编辑暂不接入，只做静态样张。">编辑</button>
                </div>
              </div>

              <div class="nb-doc" data-r6n-r8-big-unit-doc="true">
                <div class="nb-doc-body-surface">
                  <section class="nb-doc-section">
                    <div class="nb-doc-section-head">
                      <div class="nb-doc-title">一、课标依据</div>
                      <button class="node-action secondary" type="button" data-pending="只呈现课标方向，不替代正式课标原文。">查看说明</button>
                    </div>
                    <p>本单元主要关联审美感知、艺术表现和创意实践，文化理解随生活情境和作品欣赏轻量渗透。</p>
                    <p>学生通过观察、比较、尝试和表达，理解色彩组合会改变画面感觉，并能用色彩表达一种较明确的情绪或氛围。</p>
                    <div class="nb-doc-subnote">具体课标原文待教材与资料确认，当前先按课标方向生成预览。</div>
                  </section>

                  <section class="nb-doc-section">
                    <div class="nb-doc-section-head">
                      <div class="nb-doc-title">二、核心素养</div>
                      <button class="node-action secondary" type="button" data-pending="这里直接写学生可观察的行为。">查看说明</button>
                    </div>
                    <ul>
                      <li><strong>审美感知：</strong>感受不同色彩组合带来的冷暖、轻重、热烈、安静等视觉意味。</li>
                      <li><strong>艺术表现：</strong>选择一组颜色表达明确感觉，并说明自己的选色理由。</li>
                      <li><strong>创意实践：</strong>在比较、试验和反馈中调整色彩搭配。</li>
                      <li><strong>文化理解：</strong>发现色彩感受与生活场景、作品情境有关。</li>
                    </ul>
                  </section>

                  <section class="nb-doc-section">
                    <div class="nb-doc-section-head">
                      <div class="nb-doc-title">三、学生起点</div>
                      <button class="node-action secondary" type="button" data-pending="体现三年级学生从直观感受到说明理由的过渡。">查看说明</button>
                    </div>
                    <p>三年级学生通常能说出“红色热闹、蓝色安静”这样的直观感受，但容易停留在“好看、鲜艳、漂亮”等词语上。</p>
                    <p>本单元要帮助学生从“我觉得”走向“我能说明为什么”。</p>
                  </section>

                  <section class="nb-doc-section">
                    <div class="nb-doc-section-head">
                      <div class="nb-doc-title">四、单元问题</div>
                      <button class="node-action secondary" type="button" data-pending="问题要回到美术表达，不做术语问答。">查看说明</button>
                    </div>
                    <ul>
                      <li>颜色为什么会让人产生不同感觉？</li>
                      <li>我们怎样用颜色把一种感觉表达出来？</li>
                      <li>改动一处颜色，画面的意味为什么会变化？</li>
                    </ul>
                  </section>

                  <section class="nb-doc-section">
                    <div class="nb-doc-section-head">
                      <div class="nb-doc-title">五、表现任务</div>
                      <button class="node-action secondary" type="button" data-pending="这是单元结果证据，不是复杂项目。">查看说明</button>
                    </div>
                    <p>学生完成一件“色彩感觉”小作品，并用一句到几句话说明：我用了哪些颜色；我想表达什么感觉；我为什么这样搭配。</p>
                    <p>如果时间允许，再根据同伴或教师反馈调整一处颜色，并说明为什么改。</p>
                  </section>

                  <section class="nb-doc-section">
                    <div class="nb-doc-section-head">
                      <div class="nb-doc-title">六、学习推进</div>
                      <button class="node-action secondary" type="button" data-pending="默认先读轻时间线，需要时再展开。">查看说明</button>
                    </div>
                    <p><strong>感受 → 比较 → 表现 → 修订</strong></p>
                    <ul>
                      <li><strong>感受：</strong>看生活图片、作品、色卡或真实物件，先说直观感受。</li>
                      <li><strong>比较：</strong>比较不同色彩组合，发现搭配变化会改变画面感觉。</li>
                      <li><strong>表现：</strong>围绕一种感觉完成色彩实验或小作品。</li>
                      <li><strong>修订：</strong>展示作品，说出理由，根据反馈调整一处颜色。</li>
                    </ul>
                  </section>

                  <section class="nb-doc-section">
                    <div class="nb-doc-section-head">
                      <div class="nb-doc-title">七、课时任务链</div>
                      <button class="node-action secondary" type="button" data-pending="看每一课承担什么任务，以及为下一课留下什么基础。">查看说明</button>
                    </div>
                    <p><strong>1-1 色彩初体验：</strong>打开感受，让学生说出颜色带来的直观感觉。</p>
                    <p><strong>1-2 色彩的感觉：</strong>比较方法，让学生发现色彩组合会改变画面意味。</p>
                    <p><strong>1-3 色彩表达：</strong>完成表达，让学生用色彩表达一种感觉，并说明选择理由。</p>
                    <div class="nb-doc-subnote">进入单课备课时，只在顶部轻提示“单元：多变的色彩 / 本课位置：比较方法”，详细承接关系放在旁注或右侧依据中。</div>
                  </section>

                  <section class="nb-doc-section">
                    <div class="nb-doc-section-head">
                      <div class="nb-doc-title">八、评价证据</div>
                      <button class="node-action secondary" type="button" data-pending="评价证据独立呈现，不藏在表现任务里。">查看说明</button>
                    </div>
                    <ul>
                      <li>能说出色彩带来的感觉；</li>
                      <li>能说明自己的选色理由；</li>
                      <li>学习单留下观察和选择记录；</li>
                      <li>作品呈现较明确的视觉意味；</li>
                      <li>能根据反馈做出一次可见调整。</li>
                    </ul>
                  </section>

                  <section class="nb-doc-section">
                    <div class="nb-doc-section-head">
                      <div class="nb-doc-title">九、技能与支架</div>
                      <button class="node-action secondary" type="button" data-pending="技能训练和艺术语言运用不能丢。">查看说明</button>
                    </div>
                    <p>生活色彩图片；艺术作品图像；不同色卡组合；学生作品正反例；简短学习单；展示评价句式。</p>
                    <p>学习单可以很轻：我看到的颜色；我感受到的画面；我为什么这样选；我还想改哪里。</p>
                    <div class="nb-r8-inline-actions">
                      <button class="node-action secondary" type="button" data-pending="补充后可重新校准材料支架。">补充教材页</button>
                      <button class="node-action secondary" type="button" data-pending="补充后可重新校准表现任务。">补充单元目标</button>
                      <button class="node-action secondary" type="button" data-pending="补充后可重新校准课时任务链。">补充课时安排</button>
                    </div>
                  </section>
                </div>
              </div>
            </section>
      `;
    }

    function renderBigUnitPrepRightPanel(view) {
      return `
        <aside class="nb-right-rail" aria-label="大单元阅读辅助">
          <section class="nb-drawer">
            <div class="nb-drawer-title"><span>阅读辅助</span><button class="node-action secondary" type="button">按需打开</button></div>
            <div class="nb-drawer-card">
              <div class="nb-drawer-title"><span>本单元设计判断</span><span class="quiet-tag">可收起</span></div>
              <div class="nb-insight-block">
                <strong>单元方向</strong>
                <p>不是记住颜色名称，而是让学生通过观察、比较和表达，理解色彩组合会改变画面感觉。</p>
              </div>
              <div class="nb-insight-block">
                <strong>课时承接</strong>
                <p>1-1 打开感受；1-2 比较方法；1-3 完成表达与展示修改。</p>
              </div>
              <div class="nb-insight-block">
                <strong>怎样看达成</strong>
                <p>看学生能否说出理由、完成色彩实验、并根据反馈调整一处颜色。</p>
              </div>
            </div>
            <details class="nb-drawer-card">
              <summary>只读依据和风险提醒</summary>
              <p>课标方向：审美感知、艺术表现、创意实践，文化理解轻量渗透。</p>
              <p>教材候选：第一单元《多变的色彩》。教材目录、单元页和教参目标仍待教师补充。</p>
              <p>当前为独立静态样张，不接入目录，不写正式备课本，不调用模型。</p>
            </details>
          </section>
        </aside>
      `;
    }
'''


def build_html(output_root: Path) -> str:
    base = output_root / R6N_R7_DIR_NAME / "prep_room_render_canvas_deepen_v1_R6N_R7_big_unit_page_user_review_and_content_polish.html"
    source = base.read_text(encoding="utf-8")
    source = source.replace("师维 · 备课室 | R6N_R7 内容审核打磨", "师维 · 备课室 | R6N_R8 大单元教学设计式样张")
    source = source.replace("<!-- 1013I_R6N_R7: user-view content polish; preview only, no runtime/provider/formal apply. -->", "<!-- 1013I_R6N_R8: big-unit design restyled as the polished single-lesson notebook UI; standalone static sample. -->")
    source = source.replace("\n  </style>", r6n_r8_css() + "\n  </style>", 1)
    source = replace_block(
        source,
        "    function renderBigUnitPrepSurface(view) {",
        "    function renderPrepNotebookBigUnitCanvas(view) {",
        big_unit_surface_and_panel(),
    )
    source = source.replace(
        '<div class="nb-scene" data-r6k-integrated-static="true" data-r6l-teacher-guidance-patch="true" data-r6m-big-unit-design-static="true" data-r6n-text-reading-static="true" data-r6n-r1-centered-numbered-static="true" data-r6n-r2-left-aligned-text="true" data-r6n-r3-minimal-copy="true" data-r6n-r4-content-rewrite="true" data-r6n-r4-content-rewrite="true" data-r6n-r4-content-rewrite="true" data-r6n-r4-content-rewrite="true">',
        '<div class="nb-scene" data-r6k-integrated-static="true" data-r6l-teacher-guidance-patch="true" data-r6m-big-unit-design-static="true" data-r6n-text-reading-static="true" data-r6n-r7-content-polish="true" data-r6n-r8-notebook-ui="true">',
        1,
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
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6N_R8_{viewport['id']}.png"
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


def validate_html(html_text: str) -> dict[str, bool]:
    try:
        main_start = html_text.index('<div class="nb-doc" data-r6n-r8-big-unit-doc="true">')
        main_end = html_text.index('<aside class="nb-right-rail"', main_start)
        main_text = html_text[main_start:main_end]
    except ValueError:
        main_text = html_text
    raw_terms = ["unit_theme", "big_idea", "formal_apply", "unit_package", "normal_candidate_card_generation_allowed"]
    checks = {
        "lesson_notebook_ui_marker_present": 'data-r6n-r8-notebook-ui="true"' in html_text,
        "big_unit_doc_uses_nb_doc_sections": "data-r6n-r8-big-unit-doc" in html_text and html_text.count("nb-doc-section") >= 9,
        "material_prompt_frontloaded": "还缺教材材料" in html_text and "上传教材目录" in html_text,
        "lesson_design_tone_reused": "查看状态" in html_text and "阅读辅助" in html_text and "按需打开" in html_text,
        "big_unit_content_kept": all(term in html_text for term in ["课标依据", "核心素养", "学生起点", "单元问题", "表现任务", "学习推进", "课时任务链", "评价证据", "技能与支架"]),
        "not_integrated_into_directory": "standalone static sample" in html_text or "独立静态样张" in html_text,
        "main_surface_no_raw_fields": not any(term in main_text for term in raw_terms),
        "preview_only_semantics": "教师确认前不写入正式备课本" in html_text,
    }
    return checks


def write_review_files(output_root: Path, stage_dir: Path, result: dict[str, Any], smoke: dict[str, Any]) -> None:
    manifest = {
        "stage": STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "html": HTML_NAME,
        "result": "1013I_R6N_R8_result.json",
        "report": "1013I_R6N_R8_report.md",
        "validator": f"scripts/{VALIDATOR_NAME}",
        "boundary": boundary(),
    }
    write_json(stage_dir / "big_unit_notebook_ui_manifest_1013I_R6N_R8.json", manifest)
    write_json(stage_dir / "visual_smoke_1013I_R6N_R8.json", smoke)
    write_json(stage_dir / "1013I_R6N_R8_result.json", result)
    report = f"""# 1013I_R6N_R8 Big Unit Design Restyled As Lesson Notebook UI

FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

本阶段把大单元设计页改成与 `1-2《色彩的感觉》` 单课教学设计页一致的备课本正文阅读形式。

- 保留大单元内容基线：课标依据、核心素养、学生起点、单元问题、表现任务、学习推进、课时任务链、评价证据、技能与支架。
- 采用单课教学设计页的 UI 语气：标题区、状态胶囊、正文分节、右侧阅读辅助。
- 资料补充前置横向提示，但不放大成系统报错。
- 当前仍是独立静态样张，不接入目录，不写正式备课本，不接 runtime/provider/model。

Validation: {FINAL_STATUS}
Failed checks: {result["failed_checks"]}
"""
    write_text(stage_dir / "1013I_R6N_R8_report.md", report)
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6N_R8 creates a standalone static big-unit design sample restyled to match the polished `1-2 色彩的感觉` lesson notebook UI. It is not integrated into the prep-room directory and does not modify the main system.

Boundaries:
- runtime_connected=false
- provider_called=false
- model_called=false
- formal_apply_performed=false
- lesson_body_written=false
- database_written=false
- memory_written=false
- feishu_written=false
- main_project_pushed=false
""")
    write_text(output_root / "README.md", f"""# Prep Room Render Canvas Deepen V1 Review Package

Latest stage: `{STAGE_ID}`

Open:
- `{STAGE_DIR_NAME}/{HTML_NAME}`

Run:
- `python scripts/{VALIDATOR_NAME}`
""")
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", f"""# Review Package Manifest

Latest stage: `{STAGE_ID}`

Files:
- `{STAGE_DIR_NAME}/{HTML_NAME}`
- `{STAGE_DIR_NAME}/1013I_R6N_R8_result.json`
- `{STAGE_DIR_NAME}/1013I_R6N_R8_report.md`
- `{STAGE_DIR_NAME}/big_unit_notebook_ui_manifest_1013I_R6N_R8.json`
- `{STAGE_DIR_NAME}/visual_smoke_1013I_R6N_R8.json`
- `scripts/{VALIDATOR_NAME}`

Boundary: standalone static sample only; no runtime/provider/model/formal apply/database/memory/Feishu writes.
""")


def run(root: Path) -> dict[str, Any]:
    output_root = resolve_output_root(root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)
    html_text = build_html(output_root)
    html_path = stage_dir / HTML_NAME
    write_text(html_path, html_text)
    checks = validate_html(html_text)
    smoke = create_screenshots(stage_dir, html_path)
    checks["screenshot_smoke_pass"] = bool(smoke.get("screenshot_smoke_pass"))
    failed = [k for k, v in checks.items() if not v]
    result = {
        "stage": STAGE_ID,
        "status": FINAL_STATUS if not failed else "FAIL_1013I_R6N_R8_BIG_UNIT_DESIGN_RESTYLED_AS_LESSON_NOTEBOOK_UI",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        **checks,
        **boundary(),
        "failed_checks": failed,
    }
    write_review_files(output_root, stage_dir, result, smoke)
    source_delta = output_root / "source_delta_1013I_R6N_R8" / "scripts" / VALIDATOR_NAME
    source_delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), source_delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=None)
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else repo_root_from_script()
    result = run(root)
    print("ALL_1013I_R6N_R8_BIG_UNIT_DESIGN_RESTYLED_AS_LESSON_NOTEBOOK_UI_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
