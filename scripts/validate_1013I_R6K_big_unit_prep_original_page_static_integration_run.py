from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6K_BIG_UNIT_PREP_ORIGINAL_PAGE_STATIC_INTEGRATION_RUN"
FINAL_STATUS = "PASS_1013I_R6K_BIG_UNIT_PREP_ORIGINAL_PAGE_STATIC_INTEGRATION_RUN"
INHERITS_FROM = "1013I_R6J_BIG_UNIT_PREP_HTML_FIXTURE_ORIGINAL_PAGE_INTEGRATION_REVIEW_GATE"
R6J_PASS_STATUS = "PASS_1013I_R6J_BIG_UNIT_PREP_HTML_FIXTURE_ORIGINAL_PAGE_INTEGRATION_REVIEW_GATE"
NEXT_STAGE = "1013I_R6L_BIG_UNIT_PREP_STATIC_INTEGRATION_PATCH_IF_NEEDED"
STAGE_DIR_NAME = "1013I_R6K_big_unit_prep_original_page_static_integration_run"
VALIDATOR_NAME = "validate_1013I_R6K_big_unit_prep_original_page_static_integration_run.py"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6K_integrated_static.html"
CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]
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
        "verified_textbook_anchor_created": False,
        "official_claim_created": False,
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


def load_inputs(output_root: Path) -> dict[str, Any]:
    r6g = output_root / "1013I_R6G_big_unit_prep_page_fixture_after_user_approval"
    r6j = output_root / "1013I_R6J_big_unit_prep_html_fixture_original_page_integration_review_gate"
    return {
        "source_html": (output_root / "prep_room_render_canvas_deepen_v1.html").read_text(encoding="utf-8"),
        "page_fixture": read_json(r6g / "big_unit_prep_page_fixture_1013I_R6G.json"),
        "action_state": read_json(r6g / "big_unit_prep_page_action_state_1013I_R6G.json"),
        "r6j_result": read_json(r6j / "1013I_R6J_result.json"),
        "placement": read_json(r6j / "big_unit_entry_placement_map_1013I_R6J.json"),
        "insertion": read_json(r6j / "main_area_insertion_plan_1013I_R6J.json"),
        "writeback": read_json(r6j / "writeback_preview_semantics_1013I_R6J.json"),
    }


def js_string(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def r6k_css() -> str:
    return """

    /* 1013I_R6K static integration: big-unit confirmation inside prep-room notebook */
    .nb-tree-title.unit-entry {
      width: 100%;
      min-height: 34px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      border: 0;
      border-radius: 8px;
      padding: 6px 8px;
      background: transparent;
      color: var(--ink);
      text-align: left;
      font: inherit;
      cursor: pointer;
    }

    .nb-tree-title.unit-entry:hover,
    .nb-tree-title.unit-entry.active {
      background: var(--green-soft);
      box-shadow: inset 0 0 0 1px #b9d9cf;
    }

    .nb-unit-entry-badge {
      flex: 0 0 auto;
      min-height: 22px;
      display: inline-flex;
      align-items: center;
      padding: 0 8px;
      border: 1px solid #cfe0d9;
      border-radius: 999px;
      color: var(--green);
      background: #fff;
      font-size: 11px;
      font-weight: 800;
    }

    .nb-bigunit-preflight {
      display: grid;
      gap: 14px;
    }

    .nb-bigunit-hero {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 14px;
      align-items: start;
      padding: 16px;
      border: 1px solid #ecd6ad;
      border-left: 5px solid var(--amber);
      border-radius: var(--radius);
      background: linear-gradient(135deg, #fff6df, #fffdf8);
    }

    .nb-bigunit-hero h2 {
      margin: 0 0 6px;
      font-size: 20px;
      line-height: 1.25;
    }

    .nb-bigunit-hero p,
    .nb-bigunit-card p,
    .nb-bigunit-timeline p {
      margin: 0;
      color: var(--muted);
      line-height: 1.7;
    }

    .nb-bigunit-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }

    .nb-bigunit-card {
      padding: 13px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: rgba(255, 255, 255, 0.92);
    }

    .nb-bigunit-card strong {
      display: block;
      margin-bottom: 5px;
      font-size: 15px;
    }

    .nb-bigunit-confirm-list {
      display: grid;
      gap: 8px;
      margin: 0;
      padding: 0;
      list-style: none;
    }

    .nb-bigunit-confirm-list li {
      display: grid;
      grid-template-columns: 24px minmax(0, 1fr);
      gap: 9px;
      align-items: start;
      padding: 9px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #fff;
    }

    .nb-bigunit-alert-dot {
      width: 22px;
      height: 22px;
      display: grid;
      place-items: center;
      border-radius: 999px;
      background: var(--amber);
      color: #fff;
      font-size: 12px;
      font-weight: 900;
    }

    .nb-bigunit-timeline {
      display: grid;
      gap: 8px;
      margin: 0;
      padding: 0;
      list-style: none;
    }

    .nb-bigunit-timeline li {
      display: grid;
      grid-template-columns: 28px minmax(0, 1fr);
      gap: 10px;
      padding: 10px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #fff;
    }

    .nb-bigunit-index {
      width: 26px;
      height: 26px;
      display: grid;
      place-items: center;
      border-radius: 999px;
      background: var(--green);
      color: #fff;
      font-size: 12px;
      font-weight: 900;
    }

    .nb-bigunit-position-list,
    .nb-bigunit-actions {
      display: grid;
      gap: 8px;
    }

    .nb-bigunit-option,
    .nb-bigunit-action {
      width: 100%;
      min-height: 40px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 8px 10px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #fff;
      color: var(--ink);
      text-align: left;
      font: inherit;
    }

    .nb-bigunit-side-note {
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #fff;
      line-height: 1.7;
    }

    .nb-bigunit-side-note details {
      margin-top: 10px;
      padding: 9px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--panel-soft);
    }

    .nb-bigunit-side-note summary {
      cursor: pointer;
      font-weight: 850;
    }

    @media (max-width: 900px) {
      .nb-bigunit-hero,
      .nb-bigunit-grid {
        grid-template-columns: 1fr;
      }
    }
"""


def r6k_script_fixture(inputs: dict[str, Any]) -> str:
    fixture = inputs["page_fixture"]
    action_state = inputs["action_state"]
    placement = inputs["placement"]
    writeback = inputs["writeback"]
    return f"""

    const R6K_BIG_UNIT_FIXTURE = {js_string(fixture)};
    const R6K_BIG_UNIT_ACTION_STATE = {js_string(action_state)};
    const R6K_BIG_UNIT_PLACEMENT = {js_string(placement)};
    const R6K_BIG_UNIT_WRITEBACK = {js_string(writeback)};

    function r6kBigUnitTitleFromId(unitId) {{
      const prepView = model.views.find((view) => view.id === "prepNotebook");
      const unit = prepView?.tree?.find((group) => group.id === unitId);
      return unit?.title || R6K_BIG_UNIT_FIXTURE.first_screen.lower.columns[2].summary || "大单元位置确认";
    }}

    function r6kRenderBadge(text, tone = "warn") {{
      return `<span class="quiet-tag ${{tone === "danger" ? "danger" : ""}}">${{html(text)}}</span>`;
    }}

    function r6kConfirmationItems() {{
      return R6K_BIG_UNIT_FIXTURE.first_screen.middle.items.map((item) => `
        <li>
          <span class="nb-bigunit-alert-dot">!</span>
          <div>
            <strong>${{html(item.label)}}</strong>
            <p>${{html(item.why_required)}}</p>
          </div>
        </li>
      `).join("");
    }}

    function r6kSummaryCards() {{
      return R6K_BIG_UNIT_FIXTURE.first_screen.lower.columns.map((column) => `
        <article class="nb-bigunit-card">
          <span class="section-caption">${{html(column.teacher_label)}}</span>
          <strong>${{html(column.summary)}}</strong>
          ${{r6kRenderBadge("待教师确认")}}
        </article>
      `).join("");
    }}

    function r6kTimeline() {{
      const section = R6K_BIG_UNIT_FIXTURE.sections.find((item) => item.section_id === "big_unit_chain_light_timeline");
      const timeline = section?.timeline || [];
      return timeline.map((node, index) => `
        <li>
          <span class="nb-bigunit-index">${{index + 1}}</span>
          <div>
            <strong>${{html(node.teacher_title)}}</strong>
            <p>${{html(node.one_sentence_purpose)}}</p>
          </div>
        </li>
      `).join("");
    }}

    function r6kPositionOptions() {{
      const section = R6K_BIG_UNIT_FIXTURE.sections.find((item) => item.section_id === "lesson_position_candidate");
      return (section?.options || []).map((option) => `
        <button class="nb-bigunit-option" type="button" data-pending="小教已把「${{html(option.teacher_label)}}」放入大单元位置预览确认，教师确认前不生效。">
          <span>${{html(option.teacher_label)}}</span>
          ${{r6kRenderBadge("待选")}}
        </button>
      `).join("");
    }}

    function r6kTeacherActions() {{
      return (R6K_BIG_UNIT_ACTION_STATE.teacher_actions || []).map((action) => {{
        const degraded = action.action_id === "continue_degraded_single_lesson_draft";
        return `
          <button class="nb-bigunit-action" type="button" data-pending="小教已生成「${{html(action.teacher_label)}}」的${{degraded ? "降级草稿" : "预览确认"}}，不会写入正式备课本。">
            <span>${{html(action.teacher_label)}}</span>
            ${{r6kRenderBadge(degraded ? "降级草稿" : "仅预览确认", degraded ? "danger" : "warn")}}
          </button>
        `;
      }}).join("");
    }}

    function renderBigUnitPrepSurface(view) {{
      const title = r6kBigUnitTitleFromId(view.active_big_unit_id || "nb-unit-color");
      const first = R6K_BIG_UNIT_FIXTURE.first_screen;
      return `
        <section class="nb-workspace" aria-label="大单元位置确认">
          <div class="nb-hero">
            <div>
              <div class="nb-kicker">备课室 · 单元级前置确认</div>
              <div class="nb-title">${{html(title)}}</div>
            </div>
            <div class="nb-hero-actions">
              <button class="node-action primary" data-pending="小教已记录大单元确认为预览状态，教师确认前不生效。">${{iconButtonLabel("仅预览确认", "check")}}</button>
              <button class="node-action secondary" data-clear-big-unit="true">${{iconButtonLabel("回到当前课时", "arrow")}}</button>
            </div>
          </div>

          <div class="nb-state-bar">
            <div class="nb-state-main">
              <span class="state-tag">大单元位置确认</span>
              <span class="quiet-tag">教师确认前不生效</span>
              <span class="quiet-tag">不生成正式大单元</span>
            </div>
          </div>

          <div class="nb-bigunit-preflight">
            <section class="nb-bigunit-hero" data-r6k-blocking-reason="true">
              <div>
                <h2>为什么现在还不能直接生成单课</h2>
                <p>${{html(first.top.teacher_copy)}}</p>
              </div>
              <div>${{r6kRenderBadge("仅预览确认")}}</div>
            </section>

            <section class="nb-doc-section" data-r6k-missing-confirmations="true">
              <div class="nb-doc-section-head">
                <div class="nb-doc-title">还差这些教师确认</div>
                <span class="quiet-tag">阻断正常候选生成</span>
              </div>
              <ul class="nb-bigunit-confirm-list">${{r6kConfirmationItems()}}</ul>
            </section>

            <section class="nb-bigunit-grid" aria-label="教材锚点、本课位置和大单元链摘要">
              ${{r6kSummaryCards()}}
            </section>

            <section class="nb-doc-section" data-r6k-light-timeline="true">
              <div class="nb-doc-section-head">
                <div class="nb-doc-title">大单元推进链</div>
                <span class="quiet-tag">轻时间线，不是正式大单元正文</span>
              </div>
              <ol class="nb-bigunit-timeline">${{r6kTimeline()}}</ol>
            </section>

            <section class="nb-doc-section" data-r6k-lesson-position="true">
              <div class="nb-doc-section-head">
                <div class="nb-doc-title">这节课承担什么任务</div>
                <span class="quiet-tag">教师选择后进入候选链</span>
              </div>
              <div class="nb-bigunit-position-list">${{r6kPositionOptions()}}</div>
            </section>

            <section class="nb-doc-section">
              <div class="nb-doc-section-head">
                <div class="nb-doc-title">教师动作</div>
                <span class="quiet-tag">preview_state / teacher_confirmed_candidate / formal_apply 禁止</span>
              </div>
              <div class="nb-bigunit-actions">${{r6kTeacherActions()}}</div>
            </section>
          </div>
        </section>
      `;
    }}

    function renderBigUnitPrepRightPanel(view) {{
      const textbookSection = R6K_BIG_UNIT_FIXTURE.sections.find((item) => item.section_id === "textbook_anchor_candidates");
      const candidate = textbookSection?.candidate || {{}};
      const lesson = candidate.source_request_lesson || {{}};
      const anchor = candidate.candidate_anchor || {{}};
      return `
        <aside class="nb-right-rail" aria-label="大单元只读依据">
          <section class="nb-drawer nb-bigunit-side-note">
            <div class="nb-drawer-title"><span>只读依据和风险提醒</span><span class="quiet-tag">默认折叠</span></div>
            <p><strong>${{html(lesson.grade || "三年级")}} ${{html(lesson.subject || "美术")}}《${{html(lesson.lesson_title || "色彩的感觉")}}》</strong></p>
            <p>候选单元：${{html((anchor.unit_title_candidates || ["多变的色彩"]).join(" / "))}}</p>
            <details>
              <summary>查看来源字段和写入边界</summary>
              <p>${{html(candidate.risk_note || "候选链只来自字段抽取，不等于已确认的大单元设计。")}}</p>
              <p>确认教材锚点、选择本课位置、大单元链通过，都只进入预览或候选语义，不写正式教材锚点、unit_package 或 lesson_body。</p>
            </details>
          </section>
        </aside>
      `;
    }}

    function renderPrepNotebookBigUnitCanvas(view) {{
      return `
        <div class="nb-scene" data-r6k-integrated-static="true">
          <div class="nb-binder" aria-label="备课本活页夹">
            <aside class="nb-panel" aria-label="备课本目录">
              <div class="nb-cover">
                <div class="nb-cover-title">${{html(view.cover.title)}}</div>
                <div class="nb-cover-sub">${{html(view.cover.subtitle)}}</div>
                <div class="nb-metrics">
                  ${{view.cover.metrics.map(([label, value]) => `
                    <div class="nb-metric ${{nbMetricTone(label)}}">
                      <span class="nb-metric-light" aria-hidden="true"></span>
                      <strong>${{html(value)}}</strong>
                      <span>${{html(label)}}</span>
                    </div>
                  `).join("")}}
                </div>
              </div>
              <div class="nb-tree">${{renderPrepNotebookTree(view)}}</div>
            </aside>

            <div class="nb-gutter" aria-hidden="true"></div>
            ${{renderBigUnitPrepSurface(view)}}
          </div>
          ${{renderBigUnitPrepRightPanel(view)}}
        </div>
      `;
    }}

    function openBigUnitPrepSurface(unitId, options = {{}}) {{
      const prepView = model.views.find((view) => view.id === "prepNotebook");
      if (!prepView) return;
      if (!options.skipRemember) rememberActiveScroll();
      model.active_view = "prepNotebook";
      prepView.prep_notebook_mode = "view";
      prepView.active_big_unit_id = unitId || "nb-unit-color";
      prepView.active_edit_target = null;
      prepView.selected_paragraph_id = "";
      if (!options.skipRender) {{
        renderPrepRoomCanvas();
        showToast("已打开大单元位置确认");
      }}
    }}

    function closeBigUnitPrepSurface(options = {{}}) {{
      const prepView = model.views.find((view) => view.id === "prepNotebook");
      if (!prepView) return;
      prepView.active_big_unit_id = "";
      if (!options.skipRender) {{
        renderPrepRoomCanvas();
        showToast("已回到当前课时备课本");
      }}
    }}

    function applyR6KInitialState() {{
      if (window.location.hash) return;
      openBigUnitPrepSurface("nb-unit-color", {{ skipRemember: true, skipRender: true }});
    }}
"""


def replace_function(source: str, name: str, replacement: str, next_name: str) -> str:
    start = source.index(f"    function {name}")
    end = source.index(f"    function {next_name}", start)
    return source[:start] + replacement + "\n\n" + source[end:]


def build_tree_function() -> str:
    return """    function renderPrepNotebookTree(view) {
      return view.tree.map((group) => {
        const isUnitGroup = String(group.id || "").startsWith("nb-unit-");
        const isActiveUnit = view.active_big_unit_id === group.id;
        const groupTitle = isUnitGroup
          ? `<button class="nb-tree-title unit-entry ${isActiveUnit ? "active" : ""}" type="button" data-big-unit-entry="${html(group.id)}" title="打开${html(group.title)}的大单元备课">
              <span><span class="nb-tree-mark ${html(group.tone)}"></span>${html(group.title)}</span>
              <span class="nb-unit-entry-badge">大单元</span>
            </button>`
          : `<div class="nb-tree-title"><span class="nb-tree-mark ${html(group.tone)}"></span>${html(group.title)}</div>`;
        return `
          <section class="nb-tree-group">
            ${groupTitle}
            <div class="nb-tree-items">
              ${group.items.map((item) => {
                const detail = {
                  type: "备课本节点",
                  group: group.title,
                  code: item.code,
                  title: item.title,
                  status: nbStatusLabel(item.status)
                };
                return `
                  <button class="nb-tree-button ${!view.active_big_unit_id && item.id === view.active_node ? "active" : ""}" type="button" data-node="${html(item.id)}" data-nb-detail="${html(JSON.stringify(detail))}" title="${html(item.title)}">
                    <span class="nb-node-code">${html(item.code)}</span>
                    <span class="nb-node-title">${html(item.title)}</span>
                    <span class="nb-status-dot ${html(item.status)}" aria-label="${html(nbStatusLabel(item.status))}"></span>
                  </button>
                `;
              }).join("")}
            </div>
          </section>
        `;
      }).join("");
    }"""


def integrate_html(inputs: dict[str, Any]) -> str:
    source = inputs["source_html"]
    source = source.replace("师维 · 备课室 | 渲染画布深化 V1", "师维 · 备课室 | R6K 大单元静态接入")
    source = source.replace("\n  </style>", r6k_css() + "\n  </style>", 1)
    source = source.replace("    function renderPrepNotebookTree(view) {", r6k_script_fixture(inputs) + "\n\n    function renderPrepNotebookTree(view) {", 1)
    source = replace_function(source, "renderPrepNotebookTree(view) {", build_tree_function(), "prepNotebookMode(view) {")
    marker = "      const afterProcess = sections.slice(5);\n"
    source = source.replace(marker, marker + "      if (view.active_big_unit_id) return renderPrepNotebookBigUnitCanvas(view);\n", 1)
    click_marker = '      document.body.addEventListener("click", (event) => {\n'
    click_insert = """      document.body.addEventListener("click", (event) => {
        const bigUnitEntry = event.target.closest("[data-big-unit-entry]");
        if (bigUnitEntry) {
          openBigUnitPrepSurface(bigUnitEntry.dataset.bigUnitEntry);
          return;
        }

        const clearBigUnit = event.target.closest("[data-clear-big-unit]");
        if (clearBigUnit) {
          closeBigUnitPrepSurface();
          return;
        }

        const prepLessonButton = event.target.closest("[data-node^='nb-lesson']");
        if (prepLessonButton && model.active_view === "prepNotebook") {
          closeBigUnitPrepSurface({ skipRender: true });
          renderPrepRoomCanvas();
          showToast("已回到单课备课本");
          return;
        }

"""
    source = source.replace(click_marker, click_insert, 1)
    init_marker = "      applyInitialViewFromHash();\n"
    source = source.replace(init_marker, init_marker + "      applyR6KInitialState();\n", 1)
    source = source.replace("</body>", "<!-- 1013I_R6K: original-page static integration copy, no runtime/provider/formal apply. -->\n</body>", 1)
    return source


def create_screenshots(stage_dir: Path, html_path: Path) -> dict[str, Any]:
    browser = find_browser()
    screenshots: list[dict[str, Any]] = []
    if browser is None:
        return {"screenshot_smoke_pass": False, "screenshot_error": "browser_not_found", "screenshots": screenshots}
    viewports = [
        {"id": "desktop", "width": 1440, "height": 1100},
        {"id": "mobile", "width": 390, "height": 1100},
    ]
    for viewport in viewports:
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6K_{viewport['id']}.png"
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


def scan_deprecated_visible_names(paths: list[Path]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name in DEPRECATED_VISIBLE_NAMES:
            if name in text:
                hits.append({"path": str(path), "name": name})
    return hits


def scan_secrets(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append(str(path))
                break
    return hits


def build_result(output_root: Path, html_path: Path, visual_smoke: dict[str, Any], stage_files: list[Path]) -> dict[str, Any]:
    html_text = html_path.read_text(encoding="utf-8")
    latest_text = (output_root / "LATEST_REVIEW_ENTRY.md").read_text(encoding="utf-8")
    manifest_text = (output_root / "REVIEW_PACKAGE_MANIFEST.md").read_text(encoding="utf-8")
    r6j_result = read_json(
        output_root
        / "1013I_R6J_big_unit_prep_html_fixture_original_page_integration_review_gate"
        / "1013I_R6J_result.json"
    )
    r6g_fixture = read_json(
        output_root
        / "1013I_R6G_big_unit_prep_page_fixture_after_user_approval"
        / "big_unit_prep_page_fixture_1013I_R6G.json"
    )
    timeline_section = next(
        section for section in r6g_fixture["sections"] if section["section_id"] == "big_unit_chain_light_timeline"
    )
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "r6j_result_present": True,
        "r6j_final_status": r6j_result.get("final_status"),
        "r6j_pass": r6j_result.get("final_status") == R6J_PASS_STATUS,
        "latest_entry_points_to_r6k": f"REVIEW_STAGE={STAGE_ID}" in latest_text and f"FINAL_STATUS={FINAL_STATUS}" in latest_text,
        "latest_entry_next_stage_is_r6l": f"NEXT_RECOMMENDED_STAGE={NEXT_STAGE}" in latest_text,
        "manifest_includes_r6k": STAGE_ID in manifest_text and f"{STAGE_DIR_NAME}/" in manifest_text,
        "manifest_next_stage_is_r6l": NEXT_STAGE in manifest_text,
        "original_page_static_copy_created": html_path.exists(),
        "big_unit_surface_integrated_inside_prep_room": 'data-r6k-integrated-static="true"' in html_text,
        "unit_title_click_entry_created": 'data-big-unit-entry="${html(group.id)}"' in html_text or "data-big-unit-entry" in html_text,
        "lesson_buttons_return_to_single_lesson": "data-node^='nb-lesson'" in html_text and "已回到单课备课本" in html_text,
        "top_level_nav_not_modified": all(label in html_text for label in ["教室", "备课室", "课堂观察", "作品馆", "知识馆", "档案室"]) and "大单元</a>" not in html_text,
        "decision_first_layout_visible": "为什么现在还不能直接生成单课" in html_text,
        "blocking_reason_visible": "需要先确认教材锚点、大单元推进链和这节课承担的任务" in html_text,
        "missing_confirmations_visible": "还差这些教师确认" in html_text and "确认教材版本" in html_text,
        "preview_only_badges_visible": "仅预览确认" in html_text and "教师确认前不生效" in html_text,
        "degraded_draft_label_visible": "降级草稿" in html_text,
        "big_unit_chain_rendered_as_light_timeline": "大单元推进链" in html_text and "轻时间线，不是正式大单元正文" in html_text,
        "light_timeline_node_count": len(timeline_section.get("timeline", [])),
        "lesson_position_teacher_labels_visible": "单元开头：先激发兴趣、建立问题" in html_text and "暂不确定：需要老师补充单元材料" in html_text,
        "right_reference_area_collapsed_or_low_weight": "<summary>查看来源字段和写入边界</summary>" in html_text,
        "screenshot_smoke_pass": visual_smoke.get("screenshot_smoke_pass") is True,
        "screenshot_count": len(visual_smoke.get("screenshots", [])),
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(
            [
                path
                for path in stage_files
                if path != html_path and path.name not in {"1013I_R6K_result.json", "visual_smoke_1013I_R6K.json"}
            ]
        ),
        "secret_scan_hits": scan_secrets(stage_files),
        **boundary(),
    }
    required_true = [
        "r6j_result_present",
        "r6j_pass",
        "latest_entry_points_to_r6k",
        "latest_entry_next_stage_is_r6l",
        "manifest_includes_r6k",
        "manifest_next_stage_is_r6l",
        "original_page_static_copy_created",
        "big_unit_surface_integrated_inside_prep_room",
        "unit_title_click_entry_created",
        "lesson_buttons_return_to_single_lesson",
        "top_level_nav_not_modified",
        "decision_first_layout_visible",
        "blocking_reason_visible",
        "missing_confirmations_visible",
        "preview_only_badges_visible",
        "degraded_draft_label_visible",
        "big_unit_chain_rendered_as_light_timeline",
        "lesson_position_teacher_labels_visible",
        "right_reference_area_collapsed_or_low_weight",
        "screenshot_smoke_pass",
    ]
    required_false = [
        "runtime_connected",
        "product_runtime_called",
        "html_ui_implementation_allowed",
        "ui_implementation_started",
        "r7_visual_review_entered",
        "normal_candidate_card_generation_allowed",
        "writes_unit_package",
        "writes_lesson_body",
        "verified_textbook_anchor_created",
        "official_claim_created",
        "big_unit_generation_performed",
        "single_lesson_generation_performed",
        "provider_called",
        "model_called",
        "formal_apply_performed",
        "database_written",
        "memory_written",
        "feishu_written",
        "official_export_created",
        "official_archive_created",
        "main_project_pushed",
    ]
    failures = [key for key in required_true if result.get(key) is not True]
    failures.extend([key for key in required_false if result.get(key) is not False])
    if result.get("light_timeline_node_count") != 4:
        failures.append("light_timeline_node_count")
    if result.get("screenshot_count") != 2:
        failures.append("screenshot_count")
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    if failures:
        result["final_status"] = "FAIL_1013I_R6K_BIG_UNIT_PREP_ORIGINAL_PAGE_STATIC_INTEGRATION_RUN"
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013I_R6K Big Unit Prep Original Page Static Integration Report

```text
STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}
ORIGINAL_PAGE_STATIC_COPY_CREATED=true
RUNTIME_CONNECTED=false
FORMAL_APPLY_PERFORMED=false
```

## What Changed

R6K creates a static copy of the original prep-room page and integrates the big-unit confirmation surface into the prep notebook directory flow. Unit titles such as `第一单元 多变的色彩` become internal big-unit entry buttons; lesson rows such as `1-2 色彩的感觉` still return to the single-lesson prep notebook.

## Result

```text
big_unit_surface_integrated_inside_prep_room={str(result["big_unit_surface_integrated_inside_prep_room"]).lower()}
top_level_nav_not_modified={str(result["top_level_nav_not_modified"]).lower()}
decision_first_layout_visible={str(result["decision_first_layout_visible"]).lower()}
blocking_reason_visible={str(result["blocking_reason_visible"]).lower()}
missing_confirmations_visible={str(result["missing_confirmations_visible"]).lower()}
preview_only_badges_visible={str(result["preview_only_badges_visible"]).lower()}
degraded_draft_label_visible={str(result["degraded_draft_label_visible"]).lower()}
big_unit_chain_rendered_as_light_timeline={str(result["big_unit_chain_rendered_as_light_timeline"]).lower()}
lesson_position_teacher_labels_visible={str(result["lesson_position_teacher_labels_visible"]).lower()}
right_reference_area_collapsed_or_low_weight={str(result["right_reference_area_collapsed_or_low_weight"]).lower()}
screenshot_smoke_pass={str(result["screenshot_smoke_pass"]).lower()}
```

## Boundary

This is a static integrated copy only. It does not modify the formal original page, connect runtime, call provider/model, write database/memory/Feishu, write unit package or lesson body, generate a formal big-unit design, or perform formal apply.
"""


def copy_source_delta(root: Path, output_root: Path) -> None:
    source = root / "scripts" / VALIDATOR_NAME
    target = output_root / "source_delta_1013I_R6K" / "scripts" / VALIDATOR_NAME
    if source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    root = args.root.resolve()
    output_root = resolve_output_root(root)
    inputs = load_inputs(output_root)
    stage_dir = output_root / STAGE_DIR_NAME
    html_path = stage_dir / HTML_NAME
    integrated = integrate_html(inputs)
    write_text(html_path, integrated)
    visual_smoke = create_screenshots(stage_dir, html_path)
    write_json(stage_dir / "visual_smoke_1013I_R6K.json", visual_smoke)
    write_json(
        stage_dir / "integration_manifest_1013I_R6K.json",
        {
            "stage": STAGE_ID,
            "html": HTML_NAME,
            "source_page": "prep_room_render_canvas_deepen_v1.html",
            "static_copy_only": True,
            "entry": "unit_title_click_inside_prep_notebook_tree",
            "recommended_default_open_unit": "nb-unit-color",
            "visual_smoke": visual_smoke,
        },
    )
    result_path = stage_dir / "1013I_R6K_result.json"
    report_path = stage_dir / "1013I_R6K_report.md"
    stage_files = [
        html_path,
        stage_dir / "visual_smoke_1013I_R6K.json",
        stage_dir / "integration_manifest_1013I_R6K.json",
        result_path,
        report_path,
    ]
    result = build_result(output_root, html_path, visual_smoke, stage_files)
    write_json(result_path, result)
    write_text(report_path, build_report(result))
    copy_source_delta(root, output_root)
    if result["final_status"] != FINAL_STATUS:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    print(f"{FINAL_STATUS}: {result_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
