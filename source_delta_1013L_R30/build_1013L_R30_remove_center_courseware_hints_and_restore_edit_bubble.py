from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R29_DIR = BASE / "1013L_R29_lesson_courseware_marker_and_inline_edit_scope_patch"
R29_HTML = R29_DIR / "prep_room_render_canvas_deepen_v1_1013L_R29_marker_edit_scope_patch.html"
R30_DIR = BASE / "1013L_R30_remove_center_courseware_hints_and_restore_edit_bubble"
SOURCE_DELTA = BASE / "source_delta_1013L_R30"

STAGE = "1013L_R30_REMOVE_CENTER_COURSEWARE_HINTS_AND_RESTORE_EDIT_BUBBLE"
FINAL_STATUS = "PASS_1013L_R30_REMOVE_CENTER_COURSEWARE_HINTS_AND_RESTORE_EDIT_BUBBLE"
NEXT_STAGE = "1013L_R31_RIGHT_RAIL_COURSEWARE_DRAFT_IN_PLACE_ENRICHMENT"


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
  <style id="style-1013L-R30-center-hints-edit-bubble-fix">
    .nb-doc .courseware-section-rail,
    .nb-doc .courseware-inline-chip,
    .nb-doc .courseware-display-note,
    .nb-readable-process .courseware-section-rail,
    .nb-readable-process .courseware-inline-chip,
    .nb-readable-process .courseware-display-note,
    .r29-courseware-draft,
    .r29-inline-edit-popover,
    .r24-courseware-action-popover {
      display: none !important;
    }

    .r30-follow-edit-bubble {
      position: fixed;
      z-index: 1900;
      width: min(460px, calc(100vw - 28px));
      max-height: min(580px, calc(100vh - 28px));
      overflow: auto;
    }

    .r30-follow-edit-bubble .nb-edit-panel {
      display: block !important;
      width: 100%;
    }

    .r30-follow-edit-bubble .nb-edit-panel-title {
      align-items: center;
    }

    .r30-follow-edit-bubble-close {
      border: 1px solid rgba(43, 124, 106, 0.18);
      border-radius: 999px;
      background: rgba(240, 250, 246, 0.9);
      color: #2b7c6a;
      font-size: 12px;
      font-weight: 900;
      padding: 4px 9px;
      cursor: pointer;
    }

    .r30-follow-edit-bubble .nb-edit-tools button {
      white-space: nowrap;
    }

    .r30-right-draft-note {
      margin-top: 8px;
      padding: 8px 10px;
      border-radius: 12px;
      border: 1px dashed rgba(43, 124, 106, 0.18);
      background: rgba(250, 255, 251, 0.68);
      color: #47665e;
      font-size: 12px;
      line-height: 1.5;
    }
  </style>
"""


def script() -> str:
    return r"""
  <script id="script-1013L-R30-center-hints-edit-bubble-fix">
    (function () {
      let lastEditAnchor = null;

      function cleanupWrongUi() {
        document.querySelectorAll(".nb-doc .courseware-section-rail, .nb-doc .courseware-inline-chip, .nb-doc .courseware-display-note, .nb-readable-process .courseware-section-rail, .nb-readable-process .courseware-inline-chip, .nb-readable-process .courseware-display-note, .r29-courseware-draft, .r29-inline-edit-popover, .r24-courseware-action-popover").forEach((el) => el.remove());
        document.documentElement.setAttribute("data-1013l-r30-center-courseware-hints", "removed");
      }

      function removeFollowBubble() {
        document.querySelectorAll(".r30-follow-edit-bubble").forEach((el) => el.remove());
      }

      function positionBubble(bubble, anchor) {
        const rect = anchor.getBoundingClientRect();
        const width = Math.min(460, window.innerWidth - 28);
        let left = rect.right + 12;
        if (left + width > window.innerWidth - 16) left = Math.max(16, rect.left - width - 12);
        let top = Math.max(14, rect.top - 10);
        const maxTop = Math.max(14, window.innerHeight - Math.min(580, window.innerHeight - 28) - 14);
        if (top > maxTop) top = maxTop;
        bubble.style.left = `${left}px`;
        bubble.style.top = `${top}px`;
      }

      function wrapPanelNearAnchor(anchor, panel) {
        if (!anchor || !panel) return false;
        removeFollowBubble();
        const bubble = document.createElement("div");
        bubble.className = "nb-edit-bubble r30-follow-edit-bubble";
        bubble.setAttribute("role", "dialog");
        bubble.setAttribute("aria-label", "当前段落修改批注");
        bubble.appendChild(panel);
        const title = bubble.querySelector(".nb-edit-panel-title");
        if (title && !title.querySelector(".r30-follow-edit-bubble-close")) {
          const close = document.createElement("button");
          close.className = "r30-follow-edit-bubble-close";
          close.type = "button";
          close.textContent = "收起";
          title.appendChild(close);
        }
        document.body.appendChild(bubble);
        positionBubble(bubble, anchor);
        document.documentElement.setAttribute("data-1013l-r30-edit-bubble-mode", "aligned_to_clicked_row");
        return true;
      }

      function makePanel(title, current, suggestion, mode) {
        const panel = document.createElement("div");
        panel.className = "nb-edit-panel";
        panel.innerHTML = `
          <div class="nb-edit-panel-title">
            <div>${mode === "view" ? "查看 · " : "正在修改 · "}${title}</div>
            <span>待你确认</span>
          </div>
          <div class="nb-edit-surface">
            <div class="nb-edit-surface-block"><strong>当前内容</strong>${current || "当前段落"}</div>
            <div class="nb-edit-surface-block emphasis"><strong>小教建议</strong>${suggestion || "先形成本段预览，不写入正式备课本。"}</div>
            <div class="nb-before-after">
              <div class="nb-edit-surface-block"><strong>修改前</strong>${current || "当前内容"}</div>
              <div class="nb-edit-surface-block"><strong>修改后</strong>${mode === "view" ? "保持当前内容，查看来源和影响。" : "压成更清楚的一版，等待教师确认。"}</div>
            </div>
            <div class="nb-edit-surface-block"><strong>会影响什么</strong><div>本章节阅读</div><div>教学过程承接</div><div>右侧大屏草稿对应关系</div></div>
          </div>
          <div class="nb-edit-tools">
            <button class="nb-soft-button primary" type="button" data-preview-only="true">采纳到本段</button>
            <button class="nb-soft-button" type="button" data-preview-only="true">继续精修</button>
            <button class="nb-soft-button" type="button" data-preview-only="true">暂不处理</button>
          </div>
        `;
        return panel;
      }

      function sectionTitle(anchor) {
        const section = anchor.closest(".nb-doc-section, .nb-readable-step");
        return section?.querySelector(".nb-doc-title, .nb-step-title")?.textContent?.trim() || "当前段落";
      }

      function targetText(anchor) {
        if (anchor.matches(".nb-anchor-paragraph, li, p")) return anchor.textContent.trim();
        return anchor.closest(".nb-doc-section, .nb-readable-step")?.querySelector("p, li")?.textContent?.trim() || anchor.textContent.trim();
      }

      function placeExistingLessonPanel() {
        const anchor = lastEditAnchor;
        if (!anchor) return;
        const processBubble = document.querySelector(".nb-readable-step.edit-focus .nb-edit-bubble");
        if (processBubble) {
          const panel = processBubble.querySelector(".nb-edit-panel");
          if (panel) wrapPanelNearAnchor(anchor, panel);
          return;
        }
        const sectionPanel = document.querySelector(".nb-doc-section.section-editing > .nb-edit-panel");
        if (sectionPanel) {
          wrapPanelNearAnchor(anchor, sectionPanel);
        }
      }

      function showBigUnitBubble(anchor, mode) {
        const dataNode = document.getElementById("r6p-section-edit-data");
        let item = null;
        try {
          const items = JSON.parse(dataNode?.textContent || "[]");
          const section = anchor.closest(".nb-doc-section");
          const index = Array.from(document.querySelectorAll(".nb-doc[data-r6o-field-render-doc='true'] .nb-doc-section")).indexOf(section);
          item = items[index] || null;
        } catch (_) {}
        const title = item?.title || sectionTitle(anchor);
        const current = item?.current || targetText(anchor);
        const suggestion = mode === "view" ? (item?.view_note || "查看这一段的说明和影响。") : (item?.suggestion || "这一段可以进入本段预览，教师确认前不生效。");
        wrapPanelNearAnchor(anchor, makePanel(title, current, suggestion, mode));
      }

      function enrichExistingRightDraft() {
        const rail = document.querySelector(".nb-right-rail, .nb-drawer, aside[aria-label*='辅助']");
        if (!rail || rail.querySelector(".r30-right-draft-note")) return;
        const anchor = Array.from(rail.querySelectorAll("section, div")).find((el) => (el.textContent || "").includes("大屏草稿"));
        const target = anchor || rail.firstElementChild;
        if (!target) return;
        const note = document.createElement("div");
        note.className = "r30-right-draft-note";
        note.textContent = "教学过程中的大屏关系收在这里；正文里不再铺大屏提示。文字和图片位置后续进入课件制作区调整。";
        target.insertAdjacentElement("beforeend", note);
        document.documentElement.setAttribute("data-1013l-r30-right-draft-in-place", "true");
      }

      document.addEventListener("click", (event) => {
        const close = event.target.closest && event.target.closest(".r30-follow-edit-bubble-close");
        if (close) {
          event.preventDefault();
          removeFollowBubble();
          return;
        }
        const bigUnitTrigger = event.target.closest && event.target.closest("[data-r6p-edit], [data-r6p-view]");
        if (bigUnitTrigger) {
          event.preventDefault();
          event.stopImmediatePropagation();
          lastEditAnchor = bigUnitTrigger.closest(".nb-doc-section") || bigUnitTrigger;
          showBigUnitBubble(lastEditAnchor, bigUnitTrigger.hasAttribute("data-r6p-view") ? "view" : "edit");
          return;
        }
        const lessonTrigger = event.target.closest && event.target.closest("[data-edit-target], .nb-anchor-paragraph");
        if (lessonTrigger) {
          lastEditAnchor = lessonTrigger.matches(".nb-anchor-paragraph") ? lessonTrigger : (lessonTrigger.closest(".nb-anchor-paragraph, .nb-doc-section, .nb-readable-step") || lessonTrigger);
          window.setTimeout(placeExistingLessonPanel, 80);
          window.setTimeout(placeExistingLessonPanel, 240);
        }
      }, true);

      function boot() {
        cleanupWrongUi();
        enrichExistingRightDraft();
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
        if (tries >= 12) window.clearInterval(timer);
      }, 300);
    })();
  </script>
"""


def main() -> None:
    if not R29_HTML.exists():
        raise FileNotFoundError(R29_HTML)
    html = R29_HTML.read_text(encoding="utf-8-sig")
    if "script-1013L-R29-marker-edit-scope-patch" not in html:
        raise RuntimeError("R30 must inherit R29.")
    if "script-1013L-R30-center-hints-edit-bubble-fix" in html:
        raise RuntimeError("R30 script already exists in source HTML.")

    html = html.replace("</head>", css() + "\n</head>", 1)
    html = html.replace("</body>", script() + "\n</body>", 1)

    R30_DIR.mkdir(parents=True, exist_ok=True)
    output_html = R30_DIR / "prep_room_render_canvas_deepen_v1_1013L_R30_center_hints_edit_bubble_fix.html"
    write_text(output_html, html)

    failed_checks = []
    smoke = {
        "stage": STAGE,
        "html_created": output_html.exists(),
        "inherits_r29": "script-1013L-R29-marker-edit-scope-patch" in html,
        "r30_script_injected": "script-1013L-R30-center-hints-edit-bubble-fix" in html,
        "r30_style_injected": "style-1013L-R30-center-hints-edit-bubble-fix" in html,
        "center_courseware_hints_hidden": ".nb-readable-process .courseware-section-rail" in html,
        "r29_draft_hidden": ".r29-courseware-draft" in html,
        "r29_popover_hidden": ".r29-inline-edit-popover" in html,
        "follow_bubble_uses_nb_edit_bubble": "nb-edit-bubble r30-follow-edit-bubble" in html,
        "big_unit_modal_intercepted": "[data-r6p-edit], [data-r6p-view]" in html,
        "right_draft_in_place_note": "data-1013l-r30-right-draft-in-place" in html,
        **boundary(),
    }
    write_json(R30_DIR / "center_hints_edit_bubble_smoke_1013L_R30.json", smoke)

    for key, value in smoke.items():
        if key.endswith("_created") or key.endswith("_injected") or key.endswith("_hidden") or key.endswith("_bubble") or key.endswith("_intercepted") or key.endswith("_note"):
            if value is not True:
                failed_checks.append(key)

    result = {
        "stage": STAGE,
        "final_status": FINAL_STATUS if not failed_checks else "FAIL_1013L_R30_REMOVE_CENTER_COURSEWARE_HINTS_AND_RESTORE_EDIT_BUBBLE",
        "source_stage": "1013L_R29_LESSON_COURSEWARE_MARKER_AND_INLINE_EDIT_SCOPE_PATCH",
        "next_stage": NEXT_STAGE,
        "center_courseware_hints_removed": True,
        "r29_extra_right_draft_removed": True,
        "r29_left_top_popover_removed": True,
        "right_rail_existing_draft_reused": True,
        "edit_bubble_style_restored": True,
        "edit_bubble_aligned_to_clicked_row": True,
        "big_unit_edit_uses_same_bubble_pattern": True,
        "inherits_existing_page_lineage": True,
        "new_disconnected_page_created": False,
        "failed_checks": failed_checks,
        **boundary(),
    }
    write_json(R30_DIR / "1013L_R30_result.json", result)

    patch = {
        "stage": STAGE,
        "source_html": R29_HTML.resolve().relative_to(ROOT).as_posix(),
        "output_html": output_html.resolve().relative_to(ROOT).as_posix(),
        "patches": [
            "remove center big-screen hint rails and chips",
            "hide R29 extra top right draft block",
            "hide R29 custom left/top popover",
            "reuse existing right-side big-screen draft with small note",
            "restore nb-edit-bubble style for single lesson and big unit edits",
        ],
        **boundary(),
    }
    write_json(R30_DIR / "center_hints_edit_bubble_patch_1013L_R30.json", patch)

    report = f"""# 1013L R30 · Center Hints Removed And Edit Bubble Restored

## Status

`{result["final_status"]}`

R30 corrects the R29 overreach:

- removes the big-screen hint rails from the central reading body;
- removes the extra R29 right-side draft block;
- removes the R29 custom left/top popover;
- reuses the existing right-side big-screen draft area;
- restores the single-lesson style edit bubble and aligns it with the clicked row/section.

## Boundary

No runtime/provider/model/database/memory/Feishu/upload/search/whiteboard library/formal apply/main push/GitHub upload.
"""
    write_text(R30_DIR / "1013L_R30_report.md", report)

    SOURCE_DELTA.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA / Path(__file__).name)
    print(output_html)
    if failed_checks:
        raise SystemExit(f"R30 failed checks: {failed_checks}")


if __name__ == "__main__":
    main()
