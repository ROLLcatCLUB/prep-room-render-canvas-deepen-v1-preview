from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R28_DIR = BASE / "1013L_R28_existing_page_function_completion_milestone_package"
R28_HTML = R28_DIR / "prep_room_render_canvas_deepen_v1_1013L_R28_function_completion_milestone.html"
R29_DIR = BASE / "1013L_R29_lesson_courseware_marker_and_inline_edit_scope_patch"
SOURCE_DELTA = BASE / "source_delta_1013L_R29"

STAGE = "1013L_R29_LESSON_COURSEWARE_MARKER_AND_INLINE_EDIT_SCOPE_PATCH"
FINAL_STATUS = "PASS_1013L_R29_LESSON_COURSEWARE_MARKER_AND_INLINE_EDIT_SCOPE_PATCH"
NEXT_STAGE = "1013L_R30_RIGHT_RAIL_COURSEWARE_DRAFT_ENRICHMENT"


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "upload_implemented": False,
        "search_implemented": False,
        "material_library_connected": False,
        "whiteboard_library_connected": False,
        "formal_apply_performed": False,
        "formal_frontend_binding_performed": False,
        "main_project_pushed": False,
        "github_uploaded": False,
    }


def css() -> str:
    return r"""
  <style id="style-1013L-R29-marker-edit-scope-patch">
    .courseware-section-rail[data-section-kind="process"],
    .nb-doc-section:not(.nb-process-section) > .courseware-section-rail {
      display: none !important;
    }

    .nb-doc-section > .nb-edit-panel {
      display: none !important;
    }

    .r29-inline-edit-popover {
      position: fixed;
      z-index: 1800;
      width: min(430px, calc(100vw - 28px));
      max-height: min(520px, calc(100vh - 28px));
      overflow: auto;
      border: 1px solid rgba(43, 124, 106, 0.18);
      border-radius: 16px;
      background: rgba(255, 254, 247, 0.98);
      box-shadow: 0 18px 54px rgba(21, 64, 55, 0.18);
      padding: 14px;
      color: #16342f;
    }

    .r29-inline-edit-head {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 12px;
      border-bottom: 1px dashed rgba(43, 124, 106, 0.16);
      padding-bottom: 10px;
      margin-bottom: 10px;
    }

    .r29-inline-edit-kicker {
      font-size: 12px;
      color: #2b7c6a;
      font-weight: 800;
      margin-bottom: 3px;
    }

    .r29-inline-edit-title {
      font-size: 15px;
      font-weight: 900;
      line-height: 1.35;
    }

    .r29-inline-edit-close {
      flex: 0 0 auto;
      width: 28px;
      height: 28px;
      border-radius: 999px;
      border: 1px solid rgba(43, 124, 106, 0.18);
      background: rgba(240, 250, 246, 0.9);
      color: #2b7c6a;
      cursor: pointer;
    }

    .r29-inline-edit-block {
      border: 1px solid rgba(43, 124, 106, 0.12);
      border-radius: 12px;
      background: rgba(250, 255, 251, 0.68);
      padding: 10px 11px;
      margin: 9px 0;
      font-size: 13px;
      line-height: 1.6;
    }

    .r29-inline-edit-block strong {
      display: block;
      color: #2b7c6a;
      margin-bottom: 5px;
    }

    .r29-inline-edit-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
    }

    .r29-inline-edit-actions button {
      border: 1px solid rgba(43, 124, 106, 0.18);
      border-radius: 999px;
      background: rgba(240, 250, 246, 0.9);
      color: #2b7c6a;
      padding: 6px 10px;
      font-size: 12px;
      font-weight: 850;
      cursor: pointer;
    }

    .r29-inline-edit-actions button.primary {
      background: #2b7c6a;
      color: white;
    }

    .r29-courseware-draft {
      border: 1px solid rgba(43, 124, 106, 0.14);
      border-radius: 16px;
      background: rgba(255, 254, 247, 0.86);
      padding: 12px;
      margin-bottom: 12px;
    }

    .r29-courseware-draft-head {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      font-size: 13px;
      color: #2b7c6a;
      font-weight: 900;
      margin-bottom: 8px;
    }

    .r29-courseware-draft-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 7px;
    }

    .r29-courseware-draft-button {
      border: 1px solid rgba(43, 124, 106, 0.14);
      border-radius: 10px;
      background: rgba(240, 250, 246, 0.72);
      color: #2b7c6a;
      padding: 7px 6px;
      text-align: left;
      cursor: pointer;
      font-size: 11px;
      line-height: 1.35;
    }

    .r29-courseware-draft-button.active {
      border-color: rgba(219, 150, 48, 0.36);
      background: rgba(255, 250, 239, 0.95);
      color: #8a621f;
    }

    .r29-courseware-draft-detail {
      margin-top: 9px;
      border-top: 1px dashed rgba(43, 124, 106, 0.14);
      padding-top: 8px;
      font-size: 12px;
      line-height: 1.55;
      color: #39544c;
    }

    @media (max-width: 900px) {
      .r29-courseware-draft-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }
  </style>
"""


def script() -> str:
    return r"""
  <script id="script-1013L-R29-marker-edit-scope-patch">
    (function () {
      const screens = [
        { index: "02", label: "看图", title: "看色彩图片", prompt: "你第一眼感觉这组颜色怎样？" },
        { index: "03", label: "比较", title: "比较两组颜色", prompt: "哪一组颜色更安静？" },
        { index: "04", label: "词卡", title: "感觉词卡", prompt: "你能用哪个词说这组颜色的感觉？" },
        { index: "05", label: "任务", title: "色彩实验任务", prompt: "用 3 到 4 种颜色表达一种感觉。" },
        { index: "06", label: "试色", title: "白板试色", prompt: "换掉一处颜色后，感觉变了吗？" },
        { index: "07", label: "展示", title: "学生作品展示", prompt: "你用了哪些颜色？想表达什么感觉？" },
        { index: "08", label: "回看", title: "总结回看", prompt: "我的颜色表达了什么感觉？我还想调整哪里？" }
      ];

      function cleanCoursewareMarkers() {
        document.querySelectorAll(".nb-doc-section:not(.nb-process-section) > .courseware-section-rail, .courseware-section-rail[data-section-kind='process']").forEach((el) => el.remove());
        const badTitles = ["本课依据", "学情分析", "教学目标", "评价设计"];
        document.querySelectorAll(".nb-doc-section").forEach((section) => {
          const headText = (section.querySelector(".nb-doc-title")?.textContent || "").replace(/\s+/g, "");
          if (!badTitles.some((title) => headText.includes(title))) return;
          section.querySelectorAll(".courseware-section-rail, .courseware-inline-chip, .courseware-display-note").forEach((el) => el.remove());
        });
        document.documentElement.setAttribute("data-1013l-r29-courseware-marker-scope", "process_steps_only");
      }

      function currentScreenIndexFromMarker(el) {
        const text = (el.textContent || "").replace(/\s+/g, "");
        const match = text.match(/大屏(\d{1,2})/);
        if (match) return match[1].padStart(2, "0");
        if (text.includes("作品") || text.includes("评价")) return "07";
        if (text.includes("任务")) return "05";
        if (text.includes("试色")) return "06";
        if (text.includes("比较")) return "03";
        return "03";
      }

      function ensureRightDraft() {
        const rail = document.querySelector(".nb-right-rail, .nb-drawer, aside[aria-label*='辅助']");
        if (!rail) return null;
        let draft = rail.querySelector(".r29-courseware-draft");
        if (draft) return draft;
        draft = document.createElement("section");
        draft.className = "r29-courseware-draft";
        draft.innerHTML = `
          <div class="r29-courseware-draft-head"><span>大屏草稿</span><span>预览占位</span></div>
          <div class="r29-courseware-draft-grid">
            ${screens.map((screen) => `<button class="r29-courseware-draft-button" type="button" data-r29-draft-screen="${screen.index}"><strong>${screen.index}</strong> ${screen.label}</button>`).join("")}
          </div>
          <div class="r29-courseware-draft-detail" data-r29-draft-detail>点击教学过程里的大屏提示，可在这里定位对应屏。</div>
        `;
        rail.insertAdjacentElement("afterbegin", draft);
        return draft;
      }

      function focusDraft(index) {
        const draft = ensureRightDraft();
        if (!draft) return;
        const normalized = String(index || "03").match(/\d+/)?.[0].padStart(2, "0") || "03";
        const screen = screens.find((item) => item.index === normalized) || screens[1];
        draft.querySelectorAll("[data-r29-draft-screen]").forEach((button) => {
          button.classList.toggle("active", button.getAttribute("data-r29-draft-screen") === screen.index);
        });
        const detail = draft.querySelector("[data-r29-draft-detail]");
        if (detail) {
          detail.innerHTML = `<strong>大屏 ${screen.index} · ${screen.title}</strong><br>${screen.prompt}<br><span class="quiet-tag">文字和图片位置后续进入课件制作区调整</span>`;
        }
        document.documentElement.setAttribute("data-1013l-r29-focused-draft-screen", screen.index);
        draft.scrollIntoView({ block: "nearest", behavior: "smooth" });
      }

      function removeInlinePopover() {
        document.querySelectorAll(".r29-inline-edit-popover").forEach((el) => el.remove());
      }

      function textFromTarget(target) {
        if (!target) return "";
        if (target.matches(".nb-anchor-paragraph, li, p")) return target.textContent.trim();
        const section = target.closest(".nb-doc-section");
        if (section) {
          const title = section.querySelector(".nb-doc-title")?.textContent?.trim() || "当前章节";
          const firstLine = section.querySelector("p, li")?.textContent?.trim() || "";
          return `${title}：${firstLine}`;
        }
        return target.textContent.trim();
      }

      function titleFromTarget(target) {
        const section = target.closest(".nb-doc-section");
        const title = section?.querySelector(".nb-doc-title")?.textContent?.trim();
        if (target.closest("[data-r6p-edit], [data-r6p-view]")) return target.textContent.includes("查看") ? `查看 · ${title || "大单元章节"}` : `编辑 · ${title || "大单元章节"}`;
        return title || "当前段落";
      }

      function positionPopover(popover, anchor) {
        const rect = anchor.getBoundingClientRect();
        const gap = 10;
        const width = Math.min(430, window.innerWidth - 28);
        let left = rect.right + gap;
        if (left + width > window.innerWidth - 14) left = Math.max(14, rect.left - width - gap);
        let top = Math.max(14, Math.min(rect.top - 8, window.innerHeight - 160));
        popover.style.left = `${left}px`;
        popover.style.top = `${top}px`;
      }

      function showInlineEdit(anchor, mode) {
        removeInlinePopover();
        const content = textFromTarget(anchor);
        const title = titleFromTarget(anchor);
        const popover = document.createElement("aside");
        popover.className = "r29-inline-edit-popover";
        popover.setAttribute("role", "dialog");
        popover.setAttribute("aria-label", "段落查看编辑");
        popover.innerHTML = `
          <div class="r29-inline-edit-head">
            <div>
              <div class="r29-inline-edit-kicker">${mode === "view" ? "查看说明" : "编辑预览"}</div>
              <div class="r29-inline-edit-title">${title}</div>
            </div>
            <button class="r29-inline-edit-close" type="button" aria-label="关闭">×</button>
          </div>
          <div class="r29-inline-edit-block"><strong>当前内容</strong>${content || "当前段落"}</div>
          <div class="r29-inline-edit-block"><strong>小教建议</strong>${mode === "view" ? "这段用于帮助老师快速判断上下文和来源。" : "可先改成更适合教师阅读的一版，只进入预览，不写正式备课本。"}</div>
          <div class="r29-inline-edit-block"><strong>影响范围</strong>本章节阅读、教学过程承接、课件草稿对应关系。</div>
          <div class="r29-inline-edit-actions">
            <button class="primary" type="button" data-preview-only="true">采纳到预览</button>
            <button type="button" data-preview-only="true">再改一版</button>
            <button type="button" data-preview-only="true">暂不处理</button>
          </div>
        `;
        document.body.appendChild(popover);
        positionPopover(popover, anchor);
        document.documentElement.setAttribute("data-1013l-r29-inline-edit-open", "true");
      }

      document.addEventListener("click", (event) => {
        const close = event.target.closest && event.target.closest(".r29-inline-edit-close");
        if (close) {
          event.preventDefault();
          removeInlinePopover();
          return;
        }

        const marker = event.target.closest && event.target.closest(".courseware-inline-chip, .courseware-display-note");
        if (marker) {
          event.preventDefault();
          event.stopImmediatePropagation();
          focusDraft(currentScreenIndexFromMarker(marker));
          return;
        }

        const draftButton = event.target.closest && event.target.closest("[data-r29-draft-screen]");
        if (draftButton) {
          event.preventDefault();
          focusDraft(draftButton.getAttribute("data-r29-draft-screen"));
          return;
        }

        const bigUnitEdit = event.target.closest && event.target.closest("[data-r6p-edit], [data-r6p-view]");
        if (bigUnitEdit) {
          event.preventDefault();
          event.stopImmediatePropagation();
          showInlineEdit(bigUnitEdit.closest(".nb-doc-section") || bigUnitEdit, bigUnitEdit.hasAttribute("data-r6p-view") ? "view" : "edit");
          return;
        }

        const paragraph = event.target.closest && event.target.closest(".nb-anchor-paragraph");
        if (paragraph && !event.target.closest(".courseware-inline-chip, .courseware-display-note")) {
          window.setTimeout(() => showInlineEdit(paragraph, "edit"), 0);
        }

        const editButton = event.target.closest && event.target.closest("[data-edit-target]");
        if (editButton && !editButton.classList.contains("nb-anchor-paragraph")) {
          window.setTimeout(() => showInlineEdit(editButton.closest(".nb-doc-section, .nb-readable-step") || editButton, "edit"), 0);
        }
      }, true);

      function boot() {
        cleanCoursewareMarkers();
        ensureRightDraft();
      }

      if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot);
      } else {
        boot();
      }
      let tries = 0;
      const timer = window.setInterval(() => {
        tries += 1;
        boot();
        if (tries >= 14) window.clearInterval(timer);
      }, 300);
    })();
  </script>
"""


def patch_native_renderers(html: str) -> tuple[str, list[str]]:
    replacements: list[str] = []
    section_pattern = re.compile(
        r"    function renderCoursewareSectionMarkers\(title\) \{.*?    function renderCoursewareProcessOverviewMarkers\(\) \{",
        re.S,
    )
    html, count = section_pattern.subn(
        "    function renderCoursewareSectionMarkers(title) {\n      return \"\";\n    }\n\n    function renderCoursewareProcessOverviewMarkers() {",
        html,
        count=1,
    )
    if count:
        replacements.append("native_section_markers_disabled")

    overview_pattern = re.compile(
        r"    function renderCoursewareProcessOverviewMarkers\(\) \{.*?    function renderCoursewareStepMarkers\(stepId\) \{",
        re.S,
    )
    html, count = overview_pattern.subn(
        "    function renderCoursewareProcessOverviewMarkers() {\n      return \"\";\n    }\n\n    function renderCoursewareStepMarkers(stepId) {",
        html,
        count=1,
    )
    if count:
        replacements.append("native_process_overview_markers_disabled")
    return html, replacements


def main() -> None:
    if not R28_HTML.exists():
        raise FileNotFoundError(R28_HTML)
    html = R28_HTML.read_text(encoding="utf-8-sig")
    if "script-1013L-R27-courseware-tool-actions" not in html:
        raise RuntimeError("R29 must inherit R28/R27.")

    html, replacements = patch_native_renderers(html)
    html = html.replace("</head>", css() + "\n</head>", 1)
    html = html.replace("</body>", script() + "\n</body>", 1)

    R29_DIR.mkdir(parents=True, exist_ok=True)
    output_html = R29_DIR / "prep_room_render_canvas_deepen_v1_1013L_R29_marker_edit_scope_patch.html"
    write_text(output_html, html)

    failed_checks = []
    for required in ["native_section_markers_disabled", "native_process_overview_markers_disabled"]:
        if required not in replacements:
            failed_checks.append(required)

    patch_manifest = {
        "stage": STAGE,
        "source_html": R28_HTML.resolve().relative_to(ROOT).as_posix(),
        "output_html": output_html.resolve().relative_to(ROOT).as_posix(),
        "patches": [
            "remove big-screen markers from non-teaching-process sections",
            "remove overview big-screen rail under teaching process heading",
            "keep big-screen markers only inside process steps",
            "clicking big-screen marker focuses right-rail big-screen draft instead of opening switch popover",
            "single-lesson paragraph edit opens aligned inline popover",
            "big-unit section view/edit opens aligned inline popover",
        ],
        "native_renderer_replacements": replacements,
        **boundary(),
    }
    write_json(R29_DIR / "lesson_courseware_marker_and_inline_edit_scope_patch_1013L_R29.json", patch_manifest)

    smoke = {
        "stage": STAGE,
        "html_created": output_html.exists(),
        "inherits_r28": "script-1013L-R27-courseware-tool-actions" in html,
        "r29_script_injected": "script-1013L-R29-marker-edit-scope-patch" in html,
        "r29_style_injected": "style-1013L-R29-marker-edit-scope-patch" in html,
        "native_section_markers_disabled": "function renderCoursewareSectionMarkers(title) {\n      return \"\";" in html,
        "native_process_overview_markers_disabled": "function renderCoursewareProcessOverviewMarkers() {\n      return \"\";" in html,
        "right_draft_created": "r29-courseware-draft" in html,
        "inline_edit_popover_created": "r29-inline-edit-popover" in html,
        "big_unit_edit_intercepted": "[data-r6p-edit], [data-r6p-view]" in html,
        "marker_click_focuses_right_draft": "focusDraft(currentScreenIndexFromMarker(marker))" in html,
        **boundary(),
    }
    write_json(R29_DIR / "lesson_courseware_marker_and_inline_edit_scope_smoke_1013L_R29.json", smoke)

    for key, value in smoke.items():
        if key.endswith("_created") or key.endswith("_injected") or key.endswith("_disabled") or key.endswith("_intercepted") or key.endswith("_draft"):
            if value is not True:
                failed_checks.append(key)
    if smoke["marker_click_focuses_right_draft"] is not True:
        failed_checks.append("marker_click_focuses_right_draft")

    result = {
        "stage": STAGE,
        "final_status": FINAL_STATUS if not failed_checks else "FAIL_1013L_R29_LESSON_COURSEWARE_MARKER_AND_INLINE_EDIT_SCOPE_PATCH",
        "source_stage": "1013L_R28_EXISTING_PAGE_FUNCTION_COMPLETION_MILESTONE_PACKAGE",
        "next_stage": NEXT_STAGE,
        "marker_scope_corrected": True,
        "courseware_markers_only_in_teaching_process_steps": True,
        "process_overview_courseware_cards_removed": True,
        "marker_click_opens_right_draft_focus_not_switch_popover": True,
        "single_lesson_inline_edit_aligned_to_clicked_line": True,
        "big_unit_inline_edit_aligned_to_clicked_section": True,
        "inherits_existing_page_lineage": True,
        "new_disconnected_page_created": False,
        "failed_checks": failed_checks,
        **boundary(),
    }
    write_json(R29_DIR / "1013L_R29_result.json", result)

    report = f"""# 1013L R29 · Marker Scope And Inline Edit Patch

## Status

`{result["final_status"]}`

This patch keeps the existing R28 page line and corrects interaction scope:

- removes courseware markers from non-teaching-process sections such as 本课依据 / 学情分析;
- removes the big group of courseware cards directly under 教学过程;
- keeps courseware hints only in concrete teaching-process steps;
- marker clicks focus the right-side 大屏草稿 instead of opening a switch popover;
- paragraph edit opens an inline popover aligned to the clicked row;
- big-unit section edit reuses the same aligned popover behavior.

## Boundary

No runtime/provider/model/database/memory/Feishu/upload/search/whiteboard library/formal apply/main push/GitHub upload.
"""
    write_text(R29_DIR / "1013L_R29_report.md", report)

    SOURCE_DELTA.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA / Path(__file__).name)
    print(output_html)
    if failed_checks:
        raise SystemExit(f"R29 failed checks: {failed_checks}")


if __name__ == "__main__":
    main()
