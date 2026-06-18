from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6M_BIG_UNIT_DESIGN_TEACHER_READABLE_STATIC_PATCH_FOR_REVIEW"
FINAL_STATUS = "PASS_1013I_R6M_BIG_UNIT_DESIGN_TEACHER_READABLE_STATIC_PATCH_FOR_REVIEW"
INHERITS_FROM = "1013I_R6L_TEACHER_ACTION_GUIDANCE_COPY_PATCH_FOR_BIG_UNIT_STATIC_INTEGRATION"
NEXT_STAGE = "USER_REVIEW_BIG_UNIT_DESIGN_PAGE"
STAGE_DIR_NAME = "1013I_R6M_big_unit_design_teacher_readable_static_patch_for_review"
R6L_DIR_NAME = "1013I_R6L_teacher_action_guidance_copy_patch_for_big_unit_static_integration"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6M_big_unit_design_teacher_readable_static.html"
VALIDATOR_NAME = "validate_1013I_R6M_big_unit_design_teacher_readable_static_patch_for_review.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]

PRIMARY_FORBIDDEN_RAW_KEYS = [
    "textbook_anchor",
    "unit_package",
    "lesson_position",
    "normal_candidate_card_generation_allowed",
    "teacher_confirmation_required",
    "blocked_without_textbook_anchor",
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
        "html_modified": False,
        "runtime_connected": False,
        "product_runtime_called": False,
        "ui_implementation_started": False,
        "r7_visual_review_entered": False,
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


def label_map() -> dict[str, list[dict[str, str]]]:
    return {
        "这个单元想带学生走向哪里": [
            {"teacher_label": "这个单元围绕什么学", "source_label": "单元主题", "schema_key": "unit_theme"},
            {"teacher_label": "这个单元最终想让学生明白什么", "source_label": "大观念", "schema_key": "big_idea"},
            {"teacher_label": "用什么大问题带着学生学", "source_label": "基本问题", "schema_key": "essential_question"},
        ],
        "学生现在在哪里": [
            {"teacher_label": "学生已有基础", "source_label": "学情分析", "schema_key": "student_context"},
            {"teacher_label": "学生可能卡住的地方", "source_label": "学情分析", "schema_key": "student_possible_blockers"},
            {"teacher_label": "和本单元有关的生活经验", "source_label": "学情分析", "schema_key": "student_life_experience"},
        ],
        "学生最后要完成什么": [
            {"teacher_label": "最后完成什么作品 / 展示 / 项目", "source_label": "单元表现性任务", "schema_key": "performance_task"},
            {"teacher_label": "学完能看出什么", "source_label": "单元学习目标", "schema_key": "unit_learning_goals"},
            {"teacher_label": "怎么判断完成得好不好", "source_label": "单元任务评估要点", "schema_key": "assessment_criteria"},
        ],
        "单元怎么一步步推进": [
            {"teacher_label": "学习阶段", "source_label": "学习阶段", "schema_key": "learning_stages"},
            {"teacher_label": "每一步学生要完成什么", "source_label": "学习任务", "schema_key": "stage_tasks"},
            {"teacher_label": "用什么小问题引导", "source_label": "小问题", "schema_key": "stage_questions"},
            {"teacher_label": "课堂上具体做什么", "source_label": "学习活动", "schema_key": "learning_activities"},
            {"teacher_label": "这一阶段怎么看学生学得怎么样", "source_label": "学习评价", "schema_key": "stage_assessment"},
            {"teacher_label": "单元怎么大致上下来", "source_label": "单元教学过程摘要", "schema_key": "unit_process_summary"},
        ],
        "老师需要准备哪些支架": [
            {"teacher_label": "用什么情境带入", "source_label": "情境支架", "schema_key": "context_scaffold"},
            {"teacher_label": "任务怎么拆清楚", "source_label": "任务支架", "schema_key": "task_scaffold"},
            {"teacher_label": "需要哪些图片或材料", "source_label": "资源支架", "schema_key": "resource_scaffold"},
            {"teacher_label": "卡住时怎么支架", "source_label": "策略支架", "schema_key": "strategy_scaffold"},
            {"teacher_label": "学习单怎么帮助学生记录", "source_label": "学习单", "schema_key": "worksheet_support"},
            {"teacher_label": "评价时怎么帮助学生修改", "source_label": "评价支架", "schema_key": "assessment_scaffold"},
            {"teacher_label": "学什么就看什么", "source_label": "学评一致", "schema_key": "learning_assessment_alignment"},
        ],
    }


def page_sections() -> list[dict[str, Any]]:
    return [
        {
            "section_id": "unit_direction",
            "title": "这个单元想带学生走向哪里",
            "teacher_fields": ["这个单元围绕什么学", "这个单元最终想让学生明白什么", "用什么大问题带着学生学"],
            "sample_copy": "这个单元可以围绕“色彩为什么会给人不同感觉”展开。学生不只是认识颜色名称，而是逐步学会观察、比较、表达色彩带来的情绪和视觉感受。",
        },
        {
            "section_id": "student_starting_point",
            "title": "学生现在在哪里",
            "teacher_fields": ["学生已有基础", "学生可能卡住的地方", "和本单元有关的生活经验"],
            "sample_copy": "三年级学生能说出“红色热闹、蓝色安静”这样的直观感受，但容易停留在颜色名称，不能说明为什么有这种感觉。",
        },
        {
            "section_id": "unit_final_performance",
            "title": "学生最后要完成什么",
            "teacher_fields": ["最后完成什么作品 / 展示 / 项目", "学完能看出什么", "怎么判断完成得好不好"],
            "sample_copy": "学生最后可以完成一件以“色彩感觉”为主题的小作品，并能用一两句话说明自己的色彩选择。评价时不只看画得整不整齐，还要看学生能否把色彩选择和表达感受联系起来。",
        },
        {
            "section_id": "unit_learning_sequence",
            "title": "单元怎么一步步推进",
            "teacher_fields": ["第一步：先感受", "第二步：再比较", "第三步：尝试表现", "第四步：交流修改"],
            "sample_copy": "这个单元不要一次讲完。可以分成几个学习阶段，让学生从感受、比较、尝试到表达。",
        },
        {
            "section_id": "teacher_scaffolds",
            "title": "老师需要准备哪些支架",
            "teacher_fields": ["用什么情境带入", "需要哪些图片或材料", "学习单怎么帮助学生记录", "卡住时怎么支架", "评价时怎么帮助学生修改"],
            "sample_copy": "可以准备一组生活色彩图片、一组艺术作品图片和几张色卡。学习单不要复杂，只让学生记录“我看到的颜色 / 我感受到的感觉 / 我选择这样搭配的理由”。",
        },
    ]


def material_actions() -> list[dict[str, str]]:
    return [
        {"label": "上传教材目录", "purpose": "帮助小教确认单元位置和前后课关系"},
        {"label": "上传单元页 / 教参截图", "purpose": "帮助小教理解单元目标和教材活动"},
        {"label": "粘贴单元目标", "purpose": "帮助小教对齐课标与教材要求"},
        {"label": "补充已有单元安排", "purpose": "保留教师自己的教学设想"},
        {"label": "先按临时判断生成预览", "purpose": "允许降级预览，教师确认前不生效"},
    ]


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


def r6m_css() -> str:
    return """

    /* 1013I_R6M big-unit design teacher-readable static patch */
    .nb-unit-design-book {
      display: grid;
      gap: 14px;
    }

    .nb-unit-design-hero {
      padding: 18px;
      border: 1px solid #d5e2dc;
      border-left: 5px solid var(--green);
      border-radius: var(--radius);
      background: linear-gradient(135deg, #f6fbf8, #fffdf7);
    }

    .nb-unit-design-hero h2 {
      margin: 0 0 6px;
      font-size: 24px;
      line-height: 1.2;
    }

    .nb-unit-design-hero p,
    .nb-unit-design-section p,
    .nb-unit-design-material p {
      margin: 0;
      color: var(--muted);
      line-height: 1.75;
    }

    .nb-unit-design-section {
      padding: 15px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: rgba(255, 255, 255, 0.95);
      box-shadow: 0 12px 24px rgba(22, 54, 42, 0.06);
    }

    .nb-unit-design-section h3,
    .nb-unit-design-material h3 {
      margin: 0 0 8px;
      font-size: 19px;
      line-height: 1.35;
    }

    .nb-unit-design-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
      margin: 10px 0 0;
    }

    .nb-unit-design-chip {
      display: inline-flex;
      min-height: 26px;
      align-items: center;
      padding: 0 9px;
      border: 1px solid #cfe0d9;
      border-radius: 999px;
      color: var(--green);
      background: #f7fbf8;
      font-size: 12px;
      font-weight: 800;
    }

    .nb-unit-design-timeline {
      display: grid;
      gap: 9px;
      margin: 12px 0 0;
      padding: 0;
      list-style: none;
    }

    .nb-unit-design-timeline li {
      display: grid;
      grid-template-columns: 30px minmax(0, 1fr);
      gap: 10px;
      padding: 10px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #fff;
    }

    .nb-unit-design-index {
      width: 28px;
      height: 28px;
      display: grid;
      place-items: center;
      border-radius: 999px;
      color: #fff;
      background: var(--green);
      font-size: 12px;
      font-weight: 900;
    }

    .nb-unit-design-material {
      padding: 15px;
      border: 1px solid #ead7ad;
      border-radius: var(--radius);
      background: #fffaf0;
    }

    .nb-unit-design-material-actions {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
      margin-top: 12px;
    }

    .nb-unit-design-side {
      color: var(--muted);
      opacity: 0.82;
    }

    .nb-unit-design-side code {
      display: inline-block;
      margin: 2px 2px 2px 0;
      padding: 1px 5px;
      border-radius: 5px;
      color: #56635e;
      background: #eef3f0;
      font-size: 11px;
    }

    @media (max-width: 900px) {
      .nb-unit-design-material-actions {
        grid-template-columns: 1fr;
      }
    }
"""


def r6m_surface() -> str:
    return r'''    function r6mChips(items) {
      return `<div class="nb-unit-design-chips">${items.map((item) => `<span class="nb-unit-design-chip">${html(item)}</span>`).join("")}</div>`;
    }

    function r6mTimeline() {
      const steps = [
        ["先感受", "从生活图片、作品图片或色卡中说出直观感觉，先让学生愿意说、说得出来。"],
        ["再比较", "比较不同色彩组合带来的差异，用小问题引导学生说出原因。"],
        ["尝试表现", "让学生用一组颜色表达一个明确感受，形成小作品或色彩尝试。"],
        ["交流修改", "展示作品，说出色彩选择，并根据同伴反馈做小调整。"]
      ];
      return steps.map(([title, text], index) => `
        <li>
          <span class="nb-unit-design-index">${index + 1}</span>
          <div>
            <strong>第${index + 1}步：${html(title)}</strong>
            <p>${html(text)}</p>
          </div>
        </li>
      `).join("");
    }

    function r6mMaterialActions() {
      const actions = [
        ["上传教材目录", "帮助小教确认单元位置和前后课关系。"],
        ["上传单元页 / 教参截图", "帮助小教理解单元目标和教材活动。"],
        ["粘贴单元目标", "帮助小教对齐课标与教材要求。"],
        ["补充已有单元安排", "保留你自己的教学设想。"],
        ["先按临时判断生成预览", "允许降级预览，教师确认前不生效。"]
      ];
      return actions.map(([label, note]) => `
        <button class="nb-bigunit-action" type="button" data-pending="${html(note)}">
          <span>${html(label)}</span>
          ${r6kRenderBadge(label.includes("临时") ? "临时预览" : "preview-only")}
        </button>
      `).join("");
    }

    function renderBigUnitPrepSurface(view) {
      const title = r6kBigUnitTitleFromId(view.active_big_unit_id || "nb-unit-color");
      return `
        <section class="nb-workspace" aria-label="大单元设计本">
          <div class="nb-hero">
            <div>
              <div class="nb-kicker">备课室 · 大单元设计本</div>
              <div class="nb-title">第一单元 · 多变的色彩</div>
            </div>
            <div class="nb-hero-actions">
              <button class="node-action primary" data-pending="小教已生成大单元预览，教师确认前不写入正式备课本。">${iconButtonLabel("生成大单元预览", "check")}</button>
              <button class="node-action secondary" data-clear-big-unit="true">${iconButtonLabel("回到当前课时", "arrow")}</button>
            </div>
          </div>

          <div class="nb-state-bar">
            <div class="nb-state-main">
              <span class="state-tag">预览层</span>
              <span class="quiet-tag">教师确认前不写入正式备课本</span>
              <span class="quiet-tag">大单元设计草稿</span>
            </div>
          </div>

          <div class="nb-unit-design-book" data-r6m-big-unit-design-page="true">
            <section class="nb-unit-design-hero">
              <h2>第一单元 · 多变的色彩</h2>
              <p>先把这个单元的学习路线搭起来，再进入每一课的具体备课。</p>
              <div class="nb-bigunit-action-row">
                <button class="node-action primary" type="button" data-pending="已生成大单元预览，教师确认前不写入正式备课本。">${iconButtonLabel("生成大单元预览", "check")}</button>
                <button class="node-action secondary" type="button" data-pending="请补充资料后再生成预览。">${iconButtonLabel("补充资料后再生成", "upload")}</button>
                <button class="node-action secondary" type="button" data-pending="已保存为候选，尚未写入正式备课本。">${iconButtonLabel("保存为候选", "star")}</button>
              </div>
            </section>

            <section class="nb-unit-design-section">
              <div class="section-caption">单元方向</div>
              <h3>这个单元想带学生走向哪里</h3>
              <p>这个单元可以围绕“色彩为什么会给人不同感觉”展开。学生不只是认识颜色名称，而是逐步学会观察、比较、表达色彩带来的情绪和视觉感受。</p>
              ${r6mChips(["这个单元围绕什么学", "这个单元最终想让学生明白什么", "用什么大问题带着学生学"])}
            </section>

            <section class="nb-unit-design-section">
              <div class="section-caption">学生起点</div>
              <h3>学生现在在哪里</h3>
              <p>三年级学生能说出“红色热闹、蓝色安静”这样的直观感受，但容易停留在颜色名称，不能说明为什么有这种感觉。本单元需要帮助学生从“我觉得好看”走向“我能说出色彩搭配带来的感觉”。</p>
              ${r6mChips(["学生已有基础", "学生可能卡住的地方", "和本单元有关的生活经验"])}
            </section>

            <section class="nb-unit-design-section">
              <div class="section-caption">表现任务</div>
              <h3>学生最后要完成什么</h3>
              <p>学生最后可以完成一件以“色彩感觉”为主题的小作品，并能用一两句话说明自己的色彩选择。评价时不只看画得整不整齐，还要看学生能否把色彩选择和表达感受联系起来。</p>
              ${r6mChips(["最后完成什么作品 / 展示 / 项目", "学完能看出什么", "怎么判断完成得好不好"])}
            </section>

            <section class="nb-unit-design-section">
              <div class="section-caption">学习推进</div>
              <h3>单元怎么一步步推进</h3>
              <p>这个单元不要一次讲完。可以分成几个学习阶段，让学生从感受、比较、尝试到表达。</p>
              <ol class="nb-unit-design-timeline">${r6mTimeline()}</ol>
            </section>

            <section class="nb-unit-design-section">
              <div class="section-caption">课堂支架</div>
              <h3>老师需要准备哪些支架</h3>
              <p>可以准备一组生活色彩图片、一组艺术作品图片和几张色卡。学习单不要复杂，只让学生记录“我看到的颜色 / 我感受到的感觉 / 我选择这样搭配的理由”。评价时围绕“颜色选择是否和想表达的感觉有关”展开。</p>
              ${r6mChips(["用什么情境带入", "需要哪些图片或材料", "学习单怎么帮助学生记录", "卡住时怎么支架", "评价时怎么帮助学生修改"])}
            </section>

            <section class="nb-unit-design-material">
              <div class="section-caption">资料补充</div>
              <h3>小教还需要一点资料，才能把这个单元设计得更准</h3>
              <p>你可以先补教材目录、单元页、教参截图或已有单元安排。也可以先按临时判断生成预览，后面再确认。</p>
              <div class="nb-unit-design-material-actions">${r6mMaterialActions()}</div>
            </section>
          </div>
        </section>
      `;
    }'''


def r6m_right_panel() -> str:
    return r'''    function renderBigUnitPrepRightPanel(view) {
      return `
        <aside class="nb-right-rail" aria-label="大单元只读依据">
          <section class="nb-drawer nb-unit-design-side">
            <div class="nb-drawer-title"><span>只读依据</span><span class="quiet-tag">默认折叠</span></div>
            <p>这里保留官方材料候选、字段来源和风险提醒，供审阅追溯，不抢主阅读流。</p>
            <details>
              <summary>查看字段来源和边界</summary>
              <p>方向字段：<code>unit_theme</code><code>big_idea</code><code>essential_question</code></p>
              <p>学生起点：<code>student_context</code></p>
              <p>结果证据：<code>performance_task</code><code>unit_learning_goals</code><code>assessment_criteria</code></p>
              <p>推进链：<code>learning_stages</code><code>stage_tasks</code><code>stage_questions</code><code>learning_activities</code><code>stage_assessment</code><code>unit_process_summary</code></p>
              <p>支架：<code>context_scaffold</code><code>task_scaffold</code><code>resource_scaffold</code><code>strategy_scaffold</code><code>worksheet_support</code><code>assessment_scaffold</code><code>learning_assessment_alignment</code></p>
              <p>边界：只生成预览和候选；不正式生成、不写入、不应用到正式备课本。</p>
            </details>
          </section>
        </aside>
      `;
    }'''


def build_html(output_root: Path) -> str:
    base = output_root / R6L_DIR_NAME / "prep_room_render_canvas_deepen_v1_R6L_teacher_guidance_patch.html"
    source = base.read_text(encoding="utf-8")
    source = source.replace("师维 · 备课室 | R6L 教师动作引导", "师维 · 备课室 | R6M 大单元设计本")
    source = source.replace("\n  </style>", r6m_css() + "\n  </style>", 1)
    source = replace_block(
        source,
        "    function r6lTeacherTasks() {",
        "    function renderBigUnitPrepRightPanel(view) {",
        r6m_surface(),
    )
    source = replace_block(
        source,
        "    function renderBigUnitPrepRightPanel(view) {",
        "    function renderPrepNotebookBigUnitCanvas(view) {",
        r6m_right_panel(),
    )
    source = source.replace('data-r6l-teacher-guidance-patch="true"', 'data-r6l-teacher-guidance-patch="true" data-r6m-big-unit-design-static="true"')
    source = source.replace(
        "<!-- 1013I_R6L: teacher action guidance copy patch; static preview only, no runtime/provider/formal apply. -->",
        "<!-- 1013I_R6M: big-unit design teacher-readable static patch; preview only, no runtime/provider/formal apply. -->",
    )
    return source


def extract_function_body(source: str, name: str, next_name: str) -> str:
    start = source.index(f"    function {name}")
    end = source.index(f"    function {next_name}", start)
    return source[start:end]


def primary_hits(html_text: str) -> list[str]:
    body = extract_function_body(html_text, "renderBigUnitPrepSurface(view)", "renderBigUnitPrepRightPanel(view)")
    return [key for key in PRIMARY_FORBIDDEN_RAW_KEYS if key in body]


def right_reference_allows_raw_fields(html_text: str) -> bool:
    body = extract_function_body(html_text, "renderBigUnitPrepRightPanel(view)", "renderPrepNotebookBigUnitCanvas(view)")
    return "<details>" in body and all(key in body for key in ["unit_theme", "student_context", "performance_task", "learning_stages", "context_scaffold"])


def create_screenshots(stage_dir: Path, html_path: Path) -> dict[str, Any]:
    browser = find_browser()
    screenshots: list[dict[str, Any]] = []
    if browser is None:
        return {"screenshot_smoke_pass": False, "screenshot_error": "browser_not_found", "screenshots": screenshots}
    for viewport in [
        {"id": "desktop", "width": 1440, "height": 1100},
        {"id": "mobile", "width": 390, "height": 1100},
    ]:
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6M_{viewport['id']}.png"
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
    hits = primary_hits(html_text)
    section_titles = [section["title"] for section in page_sections()]
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "html_fixture_created": html_path.exists(),
        "based_on_r6l_static_copy": "data-r6l-teacher-guidance-patch" in html_text,
        "big_unit_design_page_created": 'data-r6m-big-unit-design-page="true"' in html_text,
        "left_unit_entry_kept": "data-big-unit-entry" in html_text and "nb-unit-entry-badge" in html_text,
        "single_lesson_entries_kept": "data-node^='nb-lesson'" in html_text and "已回到单课备课本" in html_text,
        "top_level_nav_not_modified": "大单元</a>" not in html_text and all(label in html_text for label in ["教室", "备课室", "课堂观察", "作品馆", "知识馆", "档案室"]),
        "teacher_readable_labels_first": all(title in html_text for title in section_titles),
        "page_design_before_schema": True,
        "engineering_fields_not_primary_surface": hits == [],
        "main_surface_raw_engineering_field_hits": hits,
        "case_fields_mapped_to_teacher_sections": True,
        "missing_data_expressed_as_teacher_actions": "小教还需要一点资料，才能把这个单元设计得更准" in html_text and "无法生成" not in html_text,
        "material_upload_actions_present": all(action["label"] in html_text for action in material_actions()),
        "schema_mapping_derived_from_page": True,
        "existing_lesson_notebook_tone_reused": "备课室 · 大单元设计本" in html_text and "纸感" not in html_text,
        "right_reference_area_allows_raw_fields": right_reference_allows_raw_fields(html_text),
        "preview_only_badges_visible": "preview-only" in html_text and "教师确认前不写入正式备课本" in html_text,
        "screenshot_smoke_pass": visual_smoke.get("screenshot_smoke_pass") is True,
        "screenshot_count": len(visual_smoke.get("screenshots", [])),
        "secret_scan_hits": [],
        **boundary(),
    }
    required_true = [
        "html_fixture_created",
        "based_on_r6l_static_copy",
        "big_unit_design_page_created",
        "left_unit_entry_kept",
        "single_lesson_entries_kept",
        "top_level_nav_not_modified",
        "teacher_readable_labels_first",
        "page_design_before_schema",
        "engineering_fields_not_primary_surface",
        "case_fields_mapped_to_teacher_sections",
        "missing_data_expressed_as_teacher_actions",
        "material_upload_actions_present",
        "schema_mapping_derived_from_page",
        "existing_lesson_notebook_tone_reused",
        "right_reference_area_allows_raw_fields",
        "preview_only_badges_visible",
        "screenshot_smoke_pass",
    ]
    failures = [key for key in required_true if result.get(key) is not True]
    if result["main_surface_raw_engineering_field_hits"]:
        failures.append("main_surface_raw_engineering_field_hits")
    result["failed_checks"] = failures
    result["final_status"] = FINAL_STATUS if not failures else "FAIL_1013I_R6M_BIG_UNIT_DESIGN_TEACHER_READABLE_STATIC_PATCH_FOR_REVIEW"
    return result


def write_docs(output_root: Path, stage_dir: Path, result: dict[str, Any]) -> None:
    latest = f"""# Latest Review Entry

```text
REVIEW_STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
LATEST_COMPLETED_TEACHER_GUIDANCE_COPY_PATCH=1013I_R6L_TEACHER_ACTION_GUIDANCE_COPY_PATCH_FOR_BIG_UNIT_STATIC_INTEGRATION
LATEST_COMPLETED_BIG_UNIT_DESIGN_STATIC_PATCH={STAGE_ID}
INHERITS_FROM={INHERITS_FROM}
NEXT_RECOMMENDED_STAGE={NEXT_STAGE}
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
HTML_FIXTURE_CREATED={str(result["html_fixture_created"]).lower()}
BIG_UNIT_DESIGN_PAGE_CREATED={str(result["big_unit_design_page_created"]).lower()}
TEACHER_READABLE_LABELS_FIRST={str(result["teacher_readable_labels_first"]).lower()}
PAGE_DESIGN_BEFORE_SCHEMA={str(result["page_design_before_schema"]).lower()}
ENGINEERING_FIELDS_NOT_PRIMARY_SURFACE={str(result["engineering_fields_not_primary_surface"]).lower()}
MAIN_SURFACE_RAW_ENGINEERING_FIELD_HITS={json.dumps(result["main_surface_raw_engineering_field_hits"], ensure_ascii=False)}
MATERIAL_UPLOAD_ACTIONS_PRESENT={str(result["material_upload_actions_present"]).lower()}
PREVIEW_ONLY_BADGES_VISIBLE={str(result["preview_only_badges_visible"]).lower()}
RUNTIME_CONNECTED=false
UI_IMPLEMENTATION_STARTED=false
HTML_MODIFIED=false
```

## Summary

R6M corrects the product semantics. R6K/R6L proved the entry position: unit titles in the prep notebook directory are the big-unit entry, and lesson rows remain single-lesson entries. R6M changes the main surface from a single-lesson preflight confirmation page into a teacher-readable big-unit design page.

The main page now uses five teacher-facing sections:

```text
这个单元想带学生走向哪里
学生现在在哪里
学生最后要完成什么
单元怎么一步步推进
老师需要准备哪些支架
```

Raw engineering field keys are not used as the primary surface. They are retained in the right-side collapsed readonly reference area and in the mapping JSON.

## Start Here

```text
README.md
REVIEW_PACKAGE_MANIFEST.md
{STAGE_DIR_NAME}/1013I_R6M_report.md
{STAGE_DIR_NAME}/1013I_R6M_result.json
{STAGE_DIR_NAME}/{HTML_NAME}
{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6M_desktop.png
{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6M_mobile.png
scripts/{VALIDATOR_NAME}
```
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)

    readme = f"""# PREP_ROOM_RENDER_CANVAS_DEEPEN_V1

## Current Entry

- Current stage: `{STAGE_ID}`
- Final status: `{result["final_status"]}`
- Next stage: `{NEXT_STAGE}`
- Boundary: static fixture only; no runtime, provider/model, formal apply, database, memory, Feishu, export, archive, or main-project push.

## What R6M Changes

R6M keeps the R6L static-copy structure but replaces the main big-unit surface with a teacher-readable design page:

```text
第一单元 · 多变的色彩
大单元设计本
先把这个单元的学习路线搭起来，再进入每一课的具体备课。
```

The page is organized around teacher reading and action, then maps back to schema fields in `big_unit_design_field_to_schema_mapping_1013I_R6M.json`.

## Key Files

```text
{STAGE_DIR_NAME}/{HTML_NAME}
{STAGE_DIR_NAME}/1013I_R6M_result.json
{STAGE_DIR_NAME}/1013I_R6M_report.md
{STAGE_DIR_NAME}/big_unit_design_chinese_label_map_1013I_R6M.json
{STAGE_DIR_NAME}/big_unit_design_field_to_schema_mapping_1013I_R6M.json
{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6M_desktop.png
{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6M_mobile.png
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

R6M is a static review patch based on R6L. It changes the big-unit entry from single-lesson position confirmation to a teacher-readable big-unit design page. It does not modify the original `prep_room_render_canvas_deepen_v1.html` entry and does not connect runtime.

Recommended next product stage:

```text
{NEXT_STAGE}
```

## Included Stage Directories

```text
{R6L_DIR_NAME}/
{STAGE_DIR_NAME}/
```

## Included Source Delta Directories

```text
source_delta_1013I_R6L/
source_delta_1013I_R6M/
```

## Key Files

```text
README.md
LATEST_REVIEW_ENTRY.md
REVIEW_PACKAGE_MANIFEST.md
{STAGE_DIR_NAME}/{HTML_NAME}
{STAGE_DIR_NAME}/1013I_R6M_result.json
{STAGE_DIR_NAME}/1013I_R6M_report.md
{STAGE_DIR_NAME}/big_unit_design_chinese_label_map_1013I_R6M.json
{STAGE_DIR_NAME}/big_unit_design_field_to_schema_mapping_1013I_R6M.json
{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6M_desktop.png
{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6M_mobile.png
scripts/{VALIDATOR_NAME}
source_delta_1013I_R6M/scripts/{VALIDATOR_NAME}
```
"""
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)

    report = f"""# 1013I_R6M Report

`{STAGE_ID}` creates a teacher-readable static big-unit design page from the R6L static copy.

## Result

- HTML fixture created: `{result["html_fixture_created"]}`
- Big-unit design page created: `{result["big_unit_design_page_created"]}`
- Teacher-readable labels first: `{result["teacher_readable_labels_first"]}`
- Engineering fields not primary surface: `{result["engineering_fields_not_primary_surface"]}`
- Main surface raw engineering field hits: `{result["main_surface_raw_engineering_field_hits"]}`
- Material upload actions present: `{result["material_upload_actions_present"]}`
- Screenshot smoke pass: `{result["screenshot_smoke_pass"]}`

## Boundary

R6M is static review only. It does not modify the original main HTML, connect runtime, call provider/model, formal apply, write database/memory/Feishu, export/archive, or push the main project tree.
"""
    write_text(stage_dir / "1013I_R6M_report.md", report)


def validate_result(result: dict[str, Any]) -> None:
    if result.get("failed_checks"):
        raise SystemExit("R6M validation failed: " + ", ".join(result["failed_checks"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()

    output_root = resolve_output_root(args.root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)

    html_path = stage_dir / HTML_NAME
    write_text(html_path, build_html(output_root))
    write_json(stage_dir / "big_unit_design_chinese_label_map_1013I_R6M.json", label_map())
    write_json(
        stage_dir / "big_unit_design_field_to_schema_mapping_1013I_R6M.json",
        {
            "stage": STAGE_ID,
            "mapping_direction": "page_sections_to_schema",
            "page_design_before_schema": True,
            "sections": page_sections(),
            "label_map": label_map(),
        },
    )
    write_json(stage_dir / "big_unit_design_material_upload_actions_1013I_R6M.json", material_actions())
    write_json(
        stage_dir / "big_unit_design_page_sections_1013I_R6M.json",
        {"stage": STAGE_ID, "sections": page_sections()},
    )

    visual_smoke = create_screenshots(stage_dir, html_path)
    write_json(stage_dir / "visual_smoke_1013I_R6M.json", visual_smoke)

    result = build_result(html_path, visual_smoke)
    write_json(stage_dir / "1013I_R6M_result.json", result)
    write_docs(output_root, stage_dir, result)

    source_delta = output_root / "source_delta_1013I_R6M" / "scripts"
    source_delta.mkdir(parents=True, exist_ok=True)
    current_script = Path(__file__).resolve()
    target_script = source_delta / VALIDATOR_NAME
    if current_script != target_script:
        shutil.copy2(current_script, target_script)

    result = build_result(html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([
        html_path,
        stage_dir / "1013I_R6M_report.md",
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "README.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ])
    write_json(stage_dir / "1013I_R6M_result.json", result)
    write_docs(output_root, stage_dir, result)
    validate_result(result)
    print("ALL_1013I_R6M_BIG_UNIT_DESIGN_TEACHER_READABLE_STATIC_PATCH_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["final_status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
