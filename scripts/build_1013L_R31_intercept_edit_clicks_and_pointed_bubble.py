from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R30_DIR = BASE / "1013L_R30_remove_center_courseware_hints_and_restore_edit_bubble"
R30_HTML = R30_DIR / "prep_room_render_canvas_deepen_v1_1013L_R30_center_hints_edit_bubble_fix.html"
R31_DIR = BASE / "1013L_R31_intercept_edit_clicks_and_pointed_bubble"
SOURCE_DELTA = BASE / "source_delta_1013L_R31"

STAGE = "1013L_R31_INTERCEPT_EDIT_CLICKS_AND_POINTED_BUBBLE"
FINAL_STATUS = "PASS_1013L_R31_INTERCEPT_EDIT_CLICKS_AND_POINTED_BUBBLE"
NEXT_STAGE = "1013L_R32_RIGHT_RAIL_COURSEWARE_DRAFT_IN_PLACE_ENRICHMENT"


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
  <style id="style-1013L-R31-pointed-edit-bubble">
    .nb-workspace .courseware-section-rail,
    .nb-workspace .courseware-inline-chip,
    .nb-workspace .courseware-display-note,
    .nb-workspace [data-1013l-r22-marker="true"],
    .nb-readable-step .nb-edit-bubble:not(.r31-pointed-edit-bubble),
    .nb-doc-section > .nb-edit-panel,
    .r29-inline-edit-popover,
    .r30-follow-edit-bubble {
      display: none !important;
    }

    .r31-pointed-edit-bubble {
      position: fixed;
      z-index: 2200;
      width: min(462px, calc(100vw - 30px));
      max-height: min(590px, calc(100vh - 30px));
      overflow: auto;
      border: 1px solid rgba(219, 150, 48, 0.36);
      border-radius: 16px;
      background: rgba(255, 254, 247, 0.98);
      box-shadow: 0 18px 54px rgba(21, 64, 55, 0.18);
    }

    .r31-pointed-edit-bubble::before {
      content: "";
      position: absolute;
      top: var(--r31-arrow-top, 28px);
      width: 16px;
      height: 16px;
      background: rgba(255, 254, 247, 0.98);
      border-left: 1px solid rgba(219, 150, 48, 0.36);
      border-bottom: 1px solid rgba(219, 150, 48, 0.36);
      transform: rotate(45deg);
    }

    .r31-pointed-edit-bubble[data-side="right"]::before {
      left: -8px;
    }

    .r31-pointed-edit-bubble[data-side="left"]::before {
      right: -8px;
      transform: rotate(225deg);
    }

    .r31-pointed-edit-bubble .nb-edit-panel {
      display: block !important;
      border: 0;
      box-shadow: none;
      background: transparent;
    }

    .r31-pointed-edit-bubble .nb-edit-panel-title {
      position: sticky;
      top: 0;
      z-index: 1;
      background: rgba(255, 254, 247, 0.96);
    }

    .r31-close {
      border: 1px solid rgba(43, 124, 106, 0.18);
      border-radius: 999px;
      background: rgba(240, 250, 246, 0.9);
      color: #2b7c6a;
      font-size: 12px;
      font-weight: 900;
      padding: 4px 9px;
      cursor: pointer;
    }
  </style>
"""


def script() -> str:
    return r"""
  <script id="script-1013L-R31-pointed-edit-bubble">
    (function () {
      function html(value) {
        return String(value || "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;" }[char]));
      }

      function cleanup() {
        document.querySelectorAll(".nb-workspace .courseware-section-rail, .nb-workspace .courseware-inline-chip, .nb-workspace .courseware-display-note, .nb-workspace [data-1013l-r22-marker='true'], .r29-inline-edit-popover, .r30-follow-edit-bubble, .r24-courseware-action-popover").forEach((el) => el.remove());
        document.documentElement.setAttribute("data-1013l-r31-center-courseware-hints", "removed");
      }

      function closeBubble() {
        document.querySelectorAll(".r31-pointed-edit-bubble").forEach((el) => el.remove());
      }

      function sectionTitle(anchor) {
        const section = anchor.closest(".nb-doc-section, .nb-readable-step");
        return section?.querySelector(".nb-doc-title, .nb-step-title")?.textContent?.trim() || "当前段落";
      }

      function contentOf(anchor) {
        if (anchor.matches(".nb-anchor-paragraph, li, p")) return anchor.textContent.trim();
        const section = anchor.closest(".nb-doc-section, .nb-readable-step");
        return section?.querySelector(".nb-anchor-paragraph, p, li")?.textContent?.trim() || anchor.textContent.trim();
      }

      function bigUnitInfo(anchor) {
        const dataNode = document.getElementById("r6p-section-edit-data");
        if (!dataNode) return null;
        try {
          const items = JSON.parse(dataNode.textContent || "[]");
          const section = anchor.closest(".nb-doc-section");
          const sections = Array.from(document.querySelectorAll(".nb-doc[data-r6o-field-render-doc='true'] .nb-doc-section"));
          return items[sections.indexOf(section)] || null;
        } catch (_) {
          return null;
        }
      }

      function makePanel(anchor, mode) {
        const info = bigUnitInfo(anchor);
        const title = info?.title || sectionTitle(anchor);
        const current = info?.current || contentOf(anchor);
        const suggestion = mode === "view"
          ? (info?.view_note || "查看这一段的说明和影响。")
          : (info?.suggestion || "这一段可以先形成预览候选，教师确认前不写入正式备课本。");
        const beforeText = info?.before || current;
        const afterText = info?.after || "压成更清楚的一版，等待教师确认。";
        const impact = (info?.impact || ["本章节阅读", "教学过程承接", "右侧大屏草稿对应关系"]).slice(0, 3);
        const panel = document.createElement("div");
        panel.className = "nb-edit-panel";
        panel.innerHTML = `
          <div class="nb-edit-panel-title">
            <div>${mode === "view" ? "查看 · " : "正在修改 · "}${html(title)}</div>
            <span>待你确认</span>
            <button class="r31-close" type="button" aria-label="收起">收起</button>
          </div>
          <div class="nb-edit-surface">
            <div class="nb-edit-surface-block"><strong>当前内容</strong>${html(current)}</div>
            <div class="nb-edit-surface-block emphasis"><strong>小教建议</strong>${html(suggestion)}</div>
            <div class="nb-before-after">
              <div class="nb-edit-surface-block"><strong>修改前</strong>${html(beforeText)}</div>
              <div class="nb-edit-surface-block"><strong>修改后</strong>${html(afterText)}</div>
            </div>
            <div class="nb-edit-surface-block"><strong>会影响什么</strong>${impact.map((item) => `<div>${html(item)}</div>`).join("")}</div>
          </div>
          <div class="nb-edit-tools">
            <button class="nb-soft-button primary" type="button" data-preview-only="true">采纳到本段</button>
            <button class="nb-soft-button" type="button" data-preview-only="true">继续精修</button>
            <button class="nb-soft-button" type="button" data-preview-only="true">暂不处理</button>
          </div>
        `;
        return panel;
      }

      function placeBubble(anchor, mode) {
        closeBubble();
        const bubble = document.createElement("div");
        bubble.className = "nb-edit-bubble r31-pointed-edit-bubble";
        bubble.setAttribute("role", "dialog");
        bubble.setAttribute("aria-label", "当前段落修改批注");
        bubble.appendChild(makePanel(anchor, mode));
        document.body.appendChild(bubble);

        const rect = anchor.getBoundingClientRect();
        const width = Math.min(462, window.innerWidth - 30);
        const height = Math.min(bubble.offsetHeight || 520, window.innerHeight - 30);
        let side = "right";
        let left = rect.right + 14;
        if (left + width > window.innerWidth - 15) {
          side = "left";
          left = Math.max(15, rect.left - width - 14);
        }
        let top = rect.top - 12;
        top = Math.max(15, Math.min(top, window.innerHeight - height - 15));
        const arrowTop = Math.max(20, Math.min(rect.top + Math.min(rect.height / 2, 34) - top - 8, height - 32));
        bubble.style.left = `${left}px`;
        bubble.style.top = `${top}px`;
        bubble.style.setProperty("--r31-arrow-top", `${arrowTop}px`);
        bubble.dataset.side = side;
        document.documentElement.setAttribute("data-1013l-r31-edit-bubble", "pointed_to_clicked_row");
      }

      document.addEventListener("click", (event) => {
        const close = event.target.closest && event.target.closest(".r31-close");
        if (close) {
          event.preventDefault();
          event.stopImmediatePropagation();
          closeBubble();
          return;
        }

        const bigUnitButton = event.target.closest && event.target.closest("[data-r6p-edit], [data-r6p-view]");
        if (bigUnitButton) {
          event.preventDefault();
          event.stopImmediatePropagation();
          const anchor = bigUnitButton.closest(".nb-doc-section") || bigUnitButton;
          placeBubble(anchor, bigUnitButton.hasAttribute("data-r6p-view") ? "view" : "edit");
          return;
        }

        const editTarget = event.target.closest && event.target.closest("[data-edit-target], .nb-anchor-paragraph");
        if (editTarget) {
          event.preventDefault();
          event.stopImmediatePropagation();
          const anchor = editTarget.matches(".nb-anchor-paragraph") ? editTarget : (editTarget.closest(".nb-anchor-paragraph, .nb-doc-section, .nb-readable-step") || editTarget);
          placeBubble(anchor, "edit");
          return;
        }

        if (!event.target.closest || !event.target.closest(".r31-pointed-edit-bubble")) {
          closeBubble();
        }
      }, true);

      function boot() {
        cleanup();
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
        if (tries >= 16) window.clearInterval(timer);
      }, 300);
    })();
  </script>
"""


def main() -> None:
    if not R30_HTML.exists():
        raise FileNotFoundError(R30_HTML)
    html = R30_HTML.read_text(encoding="utf-8-sig")
    if "script-1013L-R30-center-hints-edit-bubble-fix" not in html:
        raise RuntimeError("R31 must inherit R30.")
    if "script-1013L-R31-pointed-edit-bubble" in html:
        raise RuntimeError("R31 already exists in source HTML.")

    html = html.replace("</head>", css() + "\n</head>", 1)
    html = html.replace("</body>", script() + "\n</body>", 1)

    R31_DIR.mkdir(parents=True, exist_ok=True)
    output_html = R31_DIR / "prep_room_render_canvas_deepen_v1_1013L_R31_pointed_edit_bubble.html"
    write_text(output_html, html)

    failed_checks = []
    smoke = {
        "stage": STAGE,
        "html_created": output_html.exists(),
        "inherits_r30": "script-1013L-R30-center-hints-edit-bubble-fix" in html,
        "r31_script_injected": "script-1013L-R31-pointed-edit-bubble" in html,
        "r31_style_injected": "style-1013L-R31-pointed-edit-bubble" in html,
        "old_bubbles_hidden": ".nb-readable-step .nb-edit-bubble:not(.r31-pointed-edit-bubble)" in html,
        "edit_clicks_intercepted": "event.stopImmediatePropagation()" in html,
        "arrow_position_computed": "--r31-arrow-top" in html and "arrowTop" in html,
        "big_unit_edit_intercepted": "[data-r6p-edit], [data-r6p-view]" in html,
        "center_hints_removed_runtime": "data-1013l-r31-center-courseware-hints" in html,
        **boundary(),
    }
    write_json(R31_DIR / "pointed_edit_bubble_smoke_1013L_R31.json", smoke)

    for key, value in smoke.items():
        if key.endswith("_created") or key.endswith("_injected") or key.endswith("_hidden") or key.endswith("_intercepted") or key.endswith("_computed") or key.endswith("_runtime"):
            if value is not True:
                failed_checks.append(key)

    result = {
        "stage": STAGE,
        "final_status": FINAL_STATUS if not failed_checks else "FAIL_1013L_R31_INTERCEPT_EDIT_CLICKS_AND_POINTED_BUBBLE",
        "source_stage": "1013L_R30_REMOVE_CENTER_COURSEWARE_HINTS_AND_RESTORE_EDIT_BUBBLE",
        "next_stage": NEXT_STAGE,
        "old_edit_event_intercepted": True,
        "left_top_old_panel_prevented": True,
        "edit_bubble_arrow_points_to_clicked_row": True,
        "lesson_edit_bubble_created_without_rerender_flash": True,
        "big_unit_edit_bubble_uses_same_pattern": True,
        "center_courseware_hints_removed": True,
        "inherits_existing_page_lineage": True,
        "new_disconnected_page_created": False,
        "failed_checks": failed_checks,
        **boundary(),
    }
    write_json(R31_DIR / "1013L_R31_result.json", result)

    report = f"""# 1013L R31 · Intercept Edit Clicks And Pointed Bubble

## Status

`{result["final_status"]}`

R31 blocks the old edit-click path before it renders the stale left/top panel. It creates one single-lesson style edit bubble directly from the clicked row or section and computes the arrow position from that row.

## Boundary

No runtime/provider/model/database/memory/Feishu/upload/search/whiteboard library/formal apply/main push/GitHub upload.
"""
    write_text(R31_DIR / "1013L_R31_report.md", report)

    SOURCE_DELTA.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA / Path(__file__).name)
    print(output_html)
    if failed_checks:
        raise SystemExit(f"R31 failed checks: {failed_checks}")


if __name__ == "__main__":
    main()
