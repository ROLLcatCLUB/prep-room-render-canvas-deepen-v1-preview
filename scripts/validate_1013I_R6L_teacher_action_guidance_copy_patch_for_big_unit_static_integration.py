from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6L_TEACHER_ACTION_GUIDANCE_COPY_PATCH_FOR_BIG_UNIT_STATIC_INTEGRATION"
FINAL_STATUS = "PASS_1013I_R6L_TEACHER_ACTION_GUIDANCE_COPY_PATCH_FOR_BIG_UNIT_STATIC_INTEGRATION"
INHERITS_FROM = "1013I_R6K_BIG_UNIT_PREP_ORIGINAL_PAGE_STATIC_INTEGRATION_RUN"
NEXT_STAGE = "1013I_R6M_BIG_UNIT_STATIC_INTEGRATION_USER_REVIEW_OR_RUNTIME_HOLD"
STAGE_DIR_NAME = "1013I_R6L_teacher_action_guidance_copy_patch_for_big_unit_static_integration"
R6K_DIR_NAME = "1013I_R6K_big_unit_prep_original_page_static_integration_run"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6L_teacher_guidance_patch.html"
VALIDATOR_NAME = "validate_1013I_R6L_teacher_action_guidance_copy_patch_for_big_unit_static_integration.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]

PRIMARY_FORBIDDEN_RAW_KEYS = [
    "textbook_anchor_candidate",
    "big_unit_chain_candidate",
    "lesson_position_candidate",
    "teacher_confirmation_required",
    "normal_candidate_card_generation_allowed",
    "blocked_without_textbook_anchor",
    "source_request_lesson",
    "candidate_anchor",
    "teacher_confirmation_status",
    "pending_teacher_confirm",
    "unit_package",
    "lesson_body",
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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "runtime_connected": False,
        "product_runtime_called": False,
        "html_ui_implementation_allowed": False,
        "ui_implementation_started": False,
        "r7_visual_review_entered": False,
        "normal_candidate_card_generation_allowed": False,
        "writes_unit_package": False,
        "writes_lesson_body": False,
        "big_unit_generation_performed": False,
        "single_lesson_generation_performed": False,
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


def replace_block(source: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = source.index(start_marker)
    end = source.index(end_marker, start)
    return source[:start] + replacement.rstrip() + "\n\n" + source[end:]


def r6l_css() -> str:
    return """

    /* 1013I_R6L teacher action guidance copy patch */
    .nb-bigunit-guidance {
      display: grid;
      gap: 14px;
    }

    .nb-bigunit-guidance-hero {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 14px;
      align-items: start;
      padding: 18px;
      border: 1px solid #d4e2dc;
      border-left: 5px solid var(--green);
      border-radius: var(--radius);
      background: linear-gradient(135deg, #f5fbf8, #fffdf8);
    }

    .nb-bigunit-guidance-hero h2 {
      margin: 0 0 8px;
      font-size: 22px;
      line-height: 1.25;
    }

    .nb-bigunit-guidance-hero p,
    .nb-bigunit-reading-card p,
    .nb-bigunit-material-card p {
      margin: 0;
      color: var(--muted);
      line-height: 1.75;
    }

    .nb-bigunit-action-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 14px;
    }

    .nb-bigunit-action-row .node-action {
      min-height: 34px;
    }

    .nb-bigunit-reading-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
      gap: 12px;
    }

    .nb-bigunit-reading-card,
    .nb-bigunit-material-card {
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: rgba(255, 255, 255, 0.94);
    }

    .nb-bigunit-reading-card h3,
    .nb-bigunit-material-card h3 {
      margin: 0 0 8px;
      font-size: 17px;
      line-height: 1.35;
    }

    .nb-bigunit-teacher-tasks {
      display: grid;
      gap: 8px;
      margin: 0;
      padding: 0;
      list-style: none;
    }

    .nb-bigunit-teacher-tasks li {
      display: grid;
      grid-template-columns: 28px minmax(0, 1fr);
      gap: 10px;
      align-items: start;
      padding: 10px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #fff;
    }

    .nb-bigunit-task-number {
      width: 26px;
      height: 26px;
      display: grid;
      place-items: center;
      border-radius: 999px;
      color: #fff;
      background: var(--green);
      font-size: 12px;
      font-weight: 900;
    }

    .nb-bigunit-material-actions {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
      margin-top: 12px;
    }

    .nb-bigunit-soft-note {
      margin-top: 10px;
      padding: 10px;
      border: 1px dashed #d8c599;
      border-radius: var(--radius);
      background: #fffaf0;
      color: var(--muted);
      line-height: 1.7;
    }

    .nb-bigunit-side-note.r6l-low-weight {
      color: var(--muted);
      opacity: 0.82;
    }

    .nb-bigunit-side-note.r6l-low-weight code {
      font-size: 11px;
      color: #5c6762;
      background: #f1f5f2;
      border-radius: 5px;
      padding: 1px 4px;
    }

    @media (max-width: 900px) {
      .nb-bigunit-guidance-hero,
      .nb-bigunit-reading-grid,
      .nb-bigunit-material-actions {
        grid-template-columns: 1fr;
      }
    }
"""


def r6l_helpers_and_surface() -> str:
    return r'''    function r6lTeacherTasks() {
      const tasks = [
        {
          title: "这节课属于哪个单元？",
          text: "先确认它是不是放在「多变的色彩」这一组里，前后课是不是同一条学习线。"
        },
        {
          title: "这节课在单元里承担什么任务？",
          text: "它更像单元开头、方法学习，还是创作表现？这个判断会影响后面备课预览的重点。"
        },
        {
          title: "是否需要先补充教材或教参资料？",
          text: "如果你手边有目录、单元页或教参目标，小教可以用它们把判断做得更稳。"
        }
      ];
      return tasks.map((task, index) => `
        <li>
          <span class="nb-bigunit-task-number">${index + 1}</span>
          <div>
            <strong>${html(task.title)}</strong>
            <p>${html(task.text)}</p>
          </div>
        </li>
      `).join("");
    }

    function r6lMaterialActions() {
      const actions = [
        ["上传教材目录", "小教会先放进预览依据，不会写入正式备课本。", "upload"],
        ["上传单元页 / 教参截图", "用于判断前后课关系和本课任务，教师确认前不生效。", "image"],
        ["粘贴单元目标", "把单元目标作为只读参考，先进入预览判断。", "paste"],
        ["暂时跳过，先按临时判断预览", "继续看预览，但页面会保留需要确认的提示。", "arrow"]
      ];
      return actions.map(([label, note, icon]) => `
        <button class="nb-bigunit-action" type="button" data-pending="${html(note)}">
          <span>${html(label)}</span>
          ${r6kRenderBadge(label.includes("跳过") ? "临时预览" : "补充资料")}
        </button>
      `).join("");
    }

    function r6lPositionOptions() {
      const labels = [
        "单元开头：先激发兴趣、建立问题",
        "概念建立：先让学生弄清楚一个关键概念",
        "方法学习：重点学一种观察/表现方法",
        "创作表现：主要完成一件作品",
        "交流修改：主要展示、评价、调整作品",
        "暂不确定：需要老师补充单元材料"
      ];
      return labels.map((label) => `
        <button class="nb-bigunit-option" type="button" data-pending="小教已把「${html(label)}」放进预览判断，教师确认前不生效。">
          <span>${html(label)}</span>
          ${r6kRenderBadge("确认到预览")}
        </button>
      `).join("");
    }

    function r6lLightTimeline() {
      const items = [
        ["先看前一课", "前面是否已经让学生观察过颜色变化，决定本课要不要继续铺垫。"],
        ["再定本课重点", "本课更适合先建立色彩感受，让学生能说出颜色带来的感觉和理由。"],
        ["接着想后续发展", "后面如果进入创作表现，本课就要把表达词、色卡和生活图例准备好。"],
        ["最后留给老师确认", "这些只是预览判断，正式进入单课备课前还需要你确认。"]
      ];
      return items.map(([title, text], index) => `
        <li>
          <span class="nb-bigunit-index">${index + 1}</span>
          <div>
            <strong>${html(title)}</strong>
            <p>${html(text)}</p>
          </div>
        </li>
      `).join("");
    }

    function renderBigUnitPrepSurface(view) {
      const title = r6kBigUnitTitleFromId(view.active_big_unit_id || "nb-unit-color");
      return `
        <section class="nb-workspace" aria-label="大单元位置确认">
          <div class="nb-hero">
            <div>
              <div class="nb-kicker">备课室 · 单元位置确认</div>
              <div class="nb-title">${html(title)}</div>
            </div>
            <div class="nb-hero-actions">
              <button class="node-action primary" data-pending="小教已把这次确认放入预览层，教师确认前不生效。">${iconButtonLabel("确认到预览", "check")}</button>
              <button class="node-action secondary" data-clear-big-unit="true">${iconButtonLabel("回到当前课时", "arrow")}</button>
            </div>
          </div>

          <div class="nb-state-bar">
            <div class="nb-state-main">
              <span class="state-tag">大单元位置确认</span>
              <span class="quiet-tag">教师确认前不生效</span>
              <span class="quiet-tag">仅预览建议</span>
            </div>
          </div>

          <div class="nb-bigunit-guidance" data-r6l-teacher-guidance-surface="true">
            <section class="nb-bigunit-guidance-hero">
              <div>
                <h2>先确认这节课站在哪</h2>
                <p>小教发现这节课可能需要先放回单元里看。确认清楚后，再生成单课备课预览会更稳。</p>
                <div class="nb-bigunit-action-row" aria-label="大单元确认快捷动作">
                  <button class="node-action primary" type="button" data-pending="请补充教材目录或单元页，小教只放进预览依据。">${iconButtonLabel("补充教材目录 / 单元页", "upload")}</button>
                  <button class="node-action secondary" type="button" data-pending="请选择这节课在单元中的任务，教师确认前不生效。">${iconButtonLabel("选择本课位置", "check")}</button>
                  <button class="node-action secondary" type="button" data-pending="已进入临时预览判断，不会写入正式备课本。">${iconButtonLabel("先按临时判断预览", "arrow")}</button>
                </div>
              </div>
              <div>${r6kRenderBadge("仅预览确认")}</div>
            </section>

            <section class="nb-doc-section">
              <div class="nb-doc-section-head">
                <div class="nb-doc-title">你现在只需要确认三件事</div>
                <span class="quiet-tag">下一步动作</span>
              </div>
              <ul class="nb-bigunit-teacher-tasks">${r6lTeacherTasks()}</ul>
            </section>

            <section class="nb-bigunit-reading-grid" aria-label="小教临时判断和需要补充资料">
              <article class="nb-bigunit-reading-card">
                <div class="section-caption">小教的临时判断</div>
                <h3>这节课更像是“建立色彩感受”的课</h3>
                <p>它不急着让学生完成复杂作品，而是先让学生能说出：颜色为什么会让人感觉温暖、安静、强烈或轻快。</p>
                <div class="nb-bigunit-soft-note">依据：教材单元候选、课题名称、已有课堂目标。教师确认前不生效。</div>
              </article>
              <article class="nb-bigunit-reading-card">
                <div class="section-caption">这节课可能承担的任务</div>
                <h3>先把“颜色带来的感觉”说清楚</h3>
                <p>建议先确认本课是感受与表达的铺垫课，还是马上进入创作表现。确认后，小教再生成单课备课预览会更贴近你的课堂。</p>
                <div class="nb-bigunit-position-list">${r6lPositionOptions()}</div>
              </article>
            </section>

            <section class="nb-doc-section">
              <div class="nb-doc-section-head">
                <div class="nb-doc-title">建议你先确认</div>
                <span class="quiet-tag">轻时间线</span>
              </div>
              <ol class="nb-bigunit-timeline">${r6lLightTimeline()}</ol>
            </section>

            <section class="nb-bigunit-material-card">
              <div class="section-caption">需要你补充的资料</div>
              <h3>为了判断更准，可以补充这些材料</h3>
              <p>教材目录照片、本单元页截图、教参里的单元目标，或者你已有的教学安排，都可以先作为只读依据进入预览。</p>
              <div class="nb-bigunit-material-actions">${r6lMaterialActions()}</div>
              <div class="nb-bigunit-soft-note">确认前，小教不会把这些判断写进正式备课本，只先生成预览建议。</div>
            </section>

            <section class="nb-doc-section">
              <div class="nb-doc-section-head">
                <div class="nb-doc-title">确认后会发生什么</div>
                <span class="quiet-tag">预览层</span>
              </div>
              <p class="muted-copy">确认到预览后，小教会把“教材位置、本课任务、单元前后关系”作为下一步单课备课建议的依据。你仍然可以撤回、再改一版或暂不处理。</p>
              <div class="nb-bigunit-actions">
                <button class="nb-bigunit-action" type="button" data-pending="已确认到预览，教师确认前不生效。"><span>确认到预览</span>${r6kRenderBadge("仅预览确认")}</button>
                <button class="nb-bigunit-action" type="button" data-pending="已进入临时判断预览，后面仍需教师确认。"><span>先按临时判断预览</span>${r6kRenderBadge("临时预览", "danger")}</button>
                <button class="nb-bigunit-action" type="button" data-pending="请补充资料，小教只放入预览依据。"><span>补充资料</span>${r6kRenderBadge("只读依据")}</button>
                <button class="nb-bigunit-action" type="button" data-pending="本次暂不处理，已回到当前课时备课本。"><span>暂不处理</span>${r6kRenderBadge("不生效")}</button>
              </div>
            </section>
          </div>
        </section>
      `;
    }
'''


def r6l_right_panel() -> str:
    return r'''    function renderBigUnitPrepRightPanel(view) {
      const textbookSection = R6K_BIG_UNIT_FIXTURE.sections.find((item) => item.section_id === "textbook_anchor_candidates");
      const candidate = textbookSection?.candidate || {};
      const lesson = candidate.source_request_lesson || {};
      const anchor = candidate.candidate_anchor || {};
      return `
        <aside class="nb-right-rail" aria-label="大单元只读依据">
          <section class="nb-drawer nb-bigunit-side-note r6l-low-weight">
            <div class="nb-drawer-title"><span>只读依据</span><span class="quiet-tag">默认折叠</span></div>
            <p><strong>${html(lesson.grade || "三年级")} ${html(lesson.subject || "美术")}《${html(lesson.lesson_title || "色彩的感觉")}》</strong></p>
            <p>候选单元：${html((anchor.unit_title_candidates || ["多变的色彩"]).join(" / "))}</p>
            <details>
              <summary>查看来源字段和边界</summary>
              <p>这些字段只用于审阅和追溯，不作为老师主阅读区的表达。</p>
              <p><code>textbook_anchor_candidate</code>：教材锚点候选，等待教师确认。</p>
              <p><code>big_unit_chain_candidate</code>：单元推进链候选，只做轻时间线。</p>
              <p><code>lesson_position_candidate</code>：本课位置候选，用教师可读标签呈现。</p>
              <p><code>teacher_confirmation_required</code>：确认前不生效。</p>
              <p>边界：只进入预览层；不创建正式单元包，不写正式备课正文，不执行正式应用。</p>
            </details>
          </section>
        </aside>
      `;
    }'''


def build_html(output_root: Path) -> str:
    r6k_html = output_root / R6K_DIR_NAME / "prep_room_render_canvas_deepen_v1_R6K_integrated_static.html"
    source = r6k_html.read_text(encoding="utf-8")
    source = source.replace("师维 · 备课室 | R6K 大单元静态接入", "师维 · 备课室 | R6L 教师动作引导")
    source = source.replace("\n  </style>", r6l_css() + "\n  </style>", 1)
    source = replace_block(
        source,
        "    function r6kConfirmationItems() {",
        "    function renderBigUnitPrepRightPanel(view) {",
        r6l_helpers_and_surface(),
    )
    source = replace_block(
        source,
        "    function renderBigUnitPrepRightPanel(view) {",
        "    function renderPrepNotebookBigUnitCanvas(view) {",
        r6l_right_panel(),
    )
    source = source.replace('data-r6k-integrated-static="true"', 'data-r6k-integrated-static="true" data-r6l-teacher-guidance-patch="true"')
    source = source.replace(
        "<!-- 1013I_R6K: original-page static integration copy, no runtime/provider/formal apply. -->",
        "<!-- 1013I_R6L: teacher action guidance copy patch; static preview only, no runtime/provider/formal apply. -->",
    )
    return source


def extract_function_body(source: str, name: str, next_name: str) -> str:
    start = source.index(f"    function {name}")
    end = source.index(f"    function {next_name}", start)
    return source[start:end]


def forbidden_primary_hits(html_text: str) -> list[str]:
    primary = extract_function_body(html_text, "renderBigUnitPrepSurface(view)", "renderBigUnitPrepRightPanel(view)")
    return [key for key in PRIMARY_FORBIDDEN_RAW_KEYS if key in primary]


def raw_keys_in_collapsed_reference(html_text: str) -> bool:
    right = extract_function_body(html_text, "renderBigUnitPrepRightPanel(view)", "renderPrepNotebookBigUnitCanvas(view)")
    if "<details>" not in right or "</details>" not in right:
        return False
    return all(key in right for key in [
        "textbook_anchor_candidate",
        "big_unit_chain_candidate",
        "lesson_position_candidate",
        "teacher_confirmation_required",
    ])


def scan_secrets(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore") if path.suffix.lower() != ".png" else ""
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append(str(path))
                break
    return hits


def create_screenshots(stage_dir: Path, html_path: Path) -> dict[str, Any]:
    browser = find_browser()
    screenshots: list[dict[str, Any]] = []
    if browser is None:
        return {"screenshot_smoke_pass": False, "screenshot_error": "browser_not_found", "screenshots": screenshots}
    for viewport in [
        {"id": "desktop", "width": 1440, "height": 1100},
        {"id": "mobile", "width": 390, "height": 1100},
    ]:
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6L_{viewport['id']}.png"
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


def build_result(html_path: Path, visual_smoke: dict[str, Any]) -> dict[str, Any]:
    html_text = html_path.read_text(encoding="utf-8")
    primary_hits = forbidden_primary_hits(html_text)
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "teacher_action_guidance_surface_created": 'data-r6l-teacher-guidance-surface="true"' in html_text,
        "engineering_field_primary_surface_hits": primary_hits,
        "raw_field_keys_only_in_collapsed_reference": raw_keys_in_collapsed_reference(html_text) and not primary_hits,
        "missing_data_expressed_as_teacher_actions": all(text in html_text for text in [
            "请补充教材目录或单元页",
            "选择本课位置",
            "你现在只需要确认三件事",
        ]),
        "upload_material_entry_present": "上传教材目录" in html_text and "上传单元页 / 教参截图" in html_text,
        "paste_unit_goal_entry_present": "粘贴单元目标" in html_text,
        "temporary_preview_entry_present": "暂时跳过，先按临时判断预览" in html_text and "先按临时判断预览" in html_text,
        "existing_lesson_notebook_tone_reused": "备课室 · 单元位置确认" in html_text and "小教的临时判断" in html_text,
        "big_unit_entry_position_kept": "data-big-unit-entry" in html_text and "nb-unit-entry-badge" in html_text,
        "single_lesson_entries_kept": "data-node^='nb-lesson'" in html_text and "已回到单课备课本" in html_text,
        "top_level_nav_not_modified": "大单元</a>" not in html_text and all(label in html_text for label in ["教室", "备课室", "课堂观察", "作品馆", "知识馆", "档案室"]),
        "preview_only_badges_visible": "教师确认前不生效" in html_text and "仅预览确认" in html_text,
        "button_copy_preview_only": all(text in html_text for text in ["确认到预览", "先按临时判断预览", "补充资料", "暂不处理"]) and "正式生成" not in html_text and "应用到备课本" not in html_text,
        "screenshot_smoke_pass": visual_smoke.get("screenshot_smoke_pass") is True,
        "screenshot_count": len(visual_smoke.get("screenshots", [])),
        "secret_scan_hits": [],
        **boundary(),
    }
    required_true = [
        "teacher_action_guidance_surface_created",
        "raw_field_keys_only_in_collapsed_reference",
        "missing_data_expressed_as_teacher_actions",
        "upload_material_entry_present",
        "paste_unit_goal_entry_present",
        "temporary_preview_entry_present",
        "existing_lesson_notebook_tone_reused",
        "big_unit_entry_position_kept",
        "single_lesson_entries_kept",
        "top_level_nav_not_modified",
        "preview_only_badges_visible",
        "button_copy_preview_only",
        "screenshot_smoke_pass",
    ]
    failures = [key for key in required_true if result.get(key) is not True]
    if result["engineering_field_primary_surface_hits"]:
        failures.append("engineering_field_primary_surface_hits")
    result["failed_checks"] = failures
    result["final_status"] = FINAL_STATUS if not failures else "FAIL_1013I_R6L_TEACHER_ACTION_GUIDANCE_COPY_PATCH_FOR_BIG_UNIT_STATIC_INTEGRATION"
    return result


def write_docs(output_root: Path, stage_dir: Path, result: dict[str, Any]) -> None:
    latest = f"""# Latest Review Entry

```text
REVIEW_STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
LATEST_COMPLETED_ORIGINAL_PAGE_STATIC_INTEGRATION=1013I_R6K_BIG_UNIT_PREP_ORIGINAL_PAGE_STATIC_INTEGRATION_RUN
LATEST_COMPLETED_TEACHER_GUIDANCE_COPY_PATCH={STAGE_ID}
USER_REVIEW_DECISION=REQUEST_TEACHER_ACTION_GUIDANCE_COPY_PATCH
INHERITS_FROM={INHERITS_FROM}
NEXT_RECOMMENDED_STAGE={NEXT_STAGE}
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
TEACHER_ACTION_GUIDANCE_SURFACE_CREATED={str(result["teacher_action_guidance_surface_created"]).lower()}
ENGINEERING_FIELD_PRIMARY_SURFACE_HITS={json.dumps(result["engineering_field_primary_surface_hits"], ensure_ascii=False)}
RAW_FIELD_KEYS_ONLY_IN_COLLAPSED_REFERENCE={str(result["raw_field_keys_only_in_collapsed_reference"]).lower()}
MISSING_DATA_EXPRESSED_AS_TEACHER_ACTIONS={str(result["missing_data_expressed_as_teacher_actions"]).lower()}
UPLOAD_MATERIAL_ENTRY_PRESENT={str(result["upload_material_entry_present"]).lower()}
PASTE_UNIT_GOAL_ENTRY_PRESENT={str(result["paste_unit_goal_entry_present"]).lower()}
TEMPORARY_PREVIEW_ENTRY_PRESENT={str(result["temporary_preview_entry_present"]).lower()}
BIG_UNIT_ENTRY_POSITION_KEPT={str(result["big_unit_entry_position_kept"]).lower()}
SINGLE_LESSON_ENTRIES_KEPT={str(result["single_lesson_entries_kept"]).lower()}
RUNTIME_CONNECTED=false
UI_IMPLEMENTATION_STARTED=false
HTML_UI_IMPLEMENTATION_ALLOWED=false
MAIN_HTML_BODY_MODIFIED=false
```

## Summary

R6L patches the R6K original-page static integration copy. The insertion position stays the same: unit titles in the prep notebook directory, such as `第一单元 多变的色彩`, remain the big-unit entry, and `1-1 / 1-2 / 1-3` remain single-lesson entries.

The patch changes the teacher-visible main surface from engineering diagnostics into action guidance:

```text
先确认这节课站在哪
小教的临时判断
你现在只需要确认三件事
需要你补充的资料
确认后会发生什么
```

The main reading area no longer exposes raw field keys such as `textbook_anchor_candidate`, `big_unit_chain_candidate`, `lesson_position_candidate`, or `teacher_confirmation_required`. Those keys are retained only in the right-side collapsed readonly reference area for audit traceability.

R6L remains static preview only. It does not connect runtime, call a provider/model, generate a formal big-unit design, write a lesson body, write database/memory/Feishu, export/archive officially, or push the main project tree.

## Start Here

```text
README.md
REVIEW_PACKAGE_MANIFEST.md
{STAGE_DIR_NAME}/1013I_R6L_report.md
{STAGE_DIR_NAME}/1013I_R6L_result.json
{STAGE_DIR_NAME}/{HTML_NAME}
{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6L_desktop.png
{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6L_mobile.png
scripts/{VALIDATOR_NAME}
```
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)

    readme = f"""# PREP_ROOM_RENDER_CANVAS_DEEPEN_V1

This review package tracks the prep-room render-canvas line.

## Current Entry

- Current stage: `{STAGE_ID}`
- Final status: `{result["final_status"]}`
- Inherits from: `{INHERITS_FROM}`
- Next recommended stage: `{NEXT_STAGE}`
- Boundary: static preview only; no runtime, provider/model, formal apply, database, memory, Feishu, export, archive, or main-project push.

## What R6L Changes

R6K placed the big-unit confirmation surface in the right location. R6L keeps that structure and fixes the teacher-visible wording.

The main surface now reads as a teacher action flow:

```text
先确认这节课站在哪
你现在只需要确认三件事
小教的临时判断
这节课可能承担的任务
需要你补充的资料
确认后会发生什么
```

Raw engineering fields are not used as the primary teacher copy. They remain only in the collapsed right-side reference area.

## Files

```text
LATEST_REVIEW_ENTRY.md
REVIEW_PACKAGE_MANIFEST.md
{STAGE_DIR_NAME}/{HTML_NAME}
{STAGE_DIR_NAME}/1013I_R6L_result.json
{STAGE_DIR_NAME}/1013I_R6L_report.md
{STAGE_DIR_NAME}/teacher_guidance_patch_manifest_1013I_R6L.json
{STAGE_DIR_NAME}/visual_smoke_1013I_R6L.json
scripts/{VALIDATOR_NAME}
```
"""
    write_text(output_root / "README.md", readme)

    manifest = f"""# Review Package Manifest

```text
package_line=PREP_ROOM_RENDER_CANVAS_DEEPEN_V1
current_review_entry=LATEST_REVIEW_ENTRY.md
current_stage={STAGE_ID}
final_status={result["final_status"]}
main_project_committed=false
main_project_pushed=false
```

## Current Product Baseline

R6L is a teacher-visible copy patch on top of R6K. It does not change the R6K insertion position or page structure. It keeps the big-unit entry inside the prep-room notebook directory and keeps lesson rows as single-lesson entries.

Recommended next product stage:

```text
{NEXT_STAGE}
```

## Included Stage Directories

```text
{R6K_DIR_NAME}/
{STAGE_DIR_NAME}/
```

## Included Source Delta Directories

```text
source_delta_1013I_R6K/
source_delta_1013I_R6L/
```

## Key Files

```text
README.md
LATEST_REVIEW_ENTRY.md
REVIEW_PACKAGE_MANIFEST.md
{STAGE_DIR_NAME}/{HTML_NAME}
{STAGE_DIR_NAME}/1013I_R6L_result.json
{STAGE_DIR_NAME}/1013I_R6L_report.md
{STAGE_DIR_NAME}/teacher_guidance_patch_manifest_1013I_R6L.json
{STAGE_DIR_NAME}/visual_smoke_1013I_R6L.json
scripts/{VALIDATOR_NAME}
source_delta_1013I_R6L/scripts/{VALIDATOR_NAME}
```

## Boundary

```text
runtime_connected=false
provider_called=false
model_called=false
formal_apply_performed=false
database_written=false
memory_written=false
feishu_written=false
main_project_pushed=false
```
"""
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)

    report = f"""# 1013I_R6L Report

`{STAGE_ID}` patches the R6K static integration copy so the big-unit surface reads as teacher action guidance instead of engineering diagnostics.

## Passed Checks

- Teacher action guidance surface created: `{result["teacher_action_guidance_surface_created"]}`
- Engineering field hits in primary surface: `{result["engineering_field_primary_surface_hits"]}`
- Raw keys only in collapsed reference: `{result["raw_field_keys_only_in_collapsed_reference"]}`
- Upload material entry present: `{result["upload_material_entry_present"]}`
- Paste unit goal entry present: `{result["paste_unit_goal_entry_present"]}`
- Temporary preview entry present: `{result["temporary_preview_entry_present"]}`
- Big-unit entry position kept: `{result["big_unit_entry_position_kept"]}`
- Single-lesson entries kept: `{result["single_lesson_entries_kept"]}`
- Screenshot smoke pass: `{result["screenshot_smoke_pass"]}`

## Boundary

No runtime, provider/model, formal apply, database, memory, Feishu, export, archive, or main-project push was performed.
"""
    write_text(stage_dir / "1013I_R6L_report.md", report)


def validate_result(result: dict[str, Any]) -> None:
    if result.get("failed_checks"):
        raise SystemExit("R6L validation failed: " + ", ".join(result["failed_checks"]))


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
    write_json(stage_dir / "visual_smoke_1013I_R6L.json", visual_smoke)

    result = build_result(html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([html_path, stage_dir / "1013I_R6L_report.md"])
    write_json(stage_dir / "1013I_R6L_result.json", result)
    write_json(
        stage_dir / "teacher_guidance_patch_manifest_1013I_R6L.json",
        {
            "stage": STAGE_ID,
            "html": HTML_NAME,
            "inherits_from": INHERITS_FROM,
            "keeps_big_unit_entry_position": True,
            "keeps_single_lesson_entries": True,
            "primary_surface_copy_mode": "teacher_action_guidance",
            "right_reference_raw_keys_collapsed": True,
            "boundary": boundary(),
        },
    )
    write_docs(output_root, stage_dir, result)

    source_delta = output_root / "source_delta_1013I_R6L" / "scripts"
    source_delta.mkdir(parents=True, exist_ok=True)
    current_script = Path(__file__).resolve()
    target_script = source_delta / VALIDATOR_NAME
    if current_script != target_script:
        shutil.copy2(current_script, target_script)

    # Re-write result after docs exist; this keeps validation fully reproducible from fresh clones.
    result = build_result(html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([
        html_path,
        stage_dir / "1013I_R6L_report.md",
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "README.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ])
    write_json(stage_dir / "1013I_R6L_result.json", result)
    write_docs(output_root, stage_dir, result)
    validate_result(result)
    print(json.dumps({"stage": STAGE_ID, "status": result["final_status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
