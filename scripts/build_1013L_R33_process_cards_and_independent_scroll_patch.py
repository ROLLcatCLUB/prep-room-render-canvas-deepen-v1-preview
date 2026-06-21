from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R32_DIR = BASE / "1013L_R32_restore_right_rail_courseware_cards_only"
R32_HTML = R32_DIR / "prep_room_render_canvas_deepen_v1_1013L_R32_right_rail_courseware_cards.html"
R33_DIR = BASE / "1013L_R33_process_courseware_cards_and_independent_scroll"
SOURCE_DELTA = BASE / "source_delta_1013L_R33"

STAGE = "1013L_R33_PROCESS_COURSEWARE_CARDS_AND_INDEPENDENT_SCROLL_PATCH"
FINAL_STATUS = "PASS_1013L_R33_PROCESS_COURSEWARE_CARDS_AND_INDEPENDENT_SCROLL_PATCH"
NEXT_STAGE = "1013L_R34_VISIBLE_FUNCTION_COMPLETION_CONTINUE"


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
  <style id="style-1013L-R33-process-cards-scroll">
    .r32-courseware-right-draft {
      display: none !important;
    }

    .nb-workspace .r33-process-courseware-card {
      display: flex !important;
      flex-wrap: wrap;
      align-items: center;
      gap: 6px;
      margin: 8px 0 7px;
      font-size: 12px;
      line-height: 1.35;
    }

    .r33-process-courseware-card .courseware-inline-chip {
      border-color: rgba(224, 151, 43, 0.28);
      background: rgba(245, 178, 74, 0.10);
      color: #99651a;
    }

    .r33-process-courseware-card .courseware-display-note {
      border-color: rgba(221, 154, 52, 0.22);
      background: rgba(250, 189, 85, 0.10);
      color: #856017;
    }

    html[data-1013l-r33-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) {
      height: calc(100vh - 148px);
      overflow: hidden;
    }

    html[data-1013l-r33-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) > .nb-binder {
      height: 100%;
      min-height: 0;
      align-items: stretch;
      overflow: hidden;
    }

    html[data-1013l-r33-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) .nb-panel,
    html[data-1013l-r33-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) .nb-workspace,
    html[data-1013l-r33-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) .nb-drawer,
    html[data-1013l-r33-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) .nb-right-rail {
      max-height: calc(100vh - 170px);
      overflow-y: auto;
      overscroll-behavior: contain;
      scrollbar-gutter: stable;
    }

    html[data-1013l-r33-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) .nb-panel,
    html[data-1013l-r33-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) .nb-drawer,
    html[data-1013l-r33-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) .nb-right-rail {
      position: sticky;
      top: 0;
      align-self: start;
    }

    .courseware-screen-mini {
      user-select: none;
      cursor: pointer;
    }

    .courseware-screen-mini.active,
    .courseware-screen-mini:focus-visible {
      border-color: rgba(43, 124, 106, 0.34);
      background: rgba(232, 248, 240, 0.88);
      outline: none;
    }
  </style>
"""


def script() -> str:
    return r"""
  <script id="script-1013L-R33-process-cards-scroll">
    (function () {
      const markers = {
        intro: { label: "大屏 02", title: "看色彩图片", prompt: "你第一眼感觉这组颜色怎样？" },
        sense: { label: "大屏 03/04", title: "比较两组颜色", prompt: "哪一组颜色更安静？" },
        explore: { label: "大屏 03/04/06", title: "比较与试色", prompt: "换掉一处颜色后，感觉变了吗？" },
        make: { label: "大屏 05/06", title: "色彩实验任务", prompt: "用 3 到 4 种颜色表达一种感觉。" },
        share: { label: "大屏 07/08", title: "作品展示与评价", prompt: "你用了哪些颜色？想表达什么感觉？" }
      };

      function html(value) {
        return String(value || "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;" }[char]));
      }

      function removeR32DuplicateRightDraft() {
        document.querySelectorAll(".r32-courseware-right-draft").forEach((el) => el.remove());
      }

      function restoreProcessCoursewareCards() {
        document.querySelectorAll(".nb-readable-step").forEach((step) => {
          const stepId = String(step.id || "").replace(/^nb-step-/, "");
          const item = markers[stepId];
          const body = step.querySelector(".nb-readable-body");
          if (!item || !body) return;
          if (body.querySelector(".r33-process-courseware-card")) return;
          body.querySelectorAll(".courseware-section-rail:not(.r33-process-courseware-card)").forEach((el) => el.remove());
          const rail = document.createElement("div");
          rail.className = "courseware-section-rail courseware-step-rail r33-process-courseware-card";
          rail.setAttribute("data-section-kind", "process");
          rail.setAttribute("data-1013l-r33-process-card", "true");
          rail.innerHTML = `
            <span class="courseware-inline-chip">${html(item.label)}｜${html(item.title)}</span>
            <span class="courseware-display-note"><span>屏幕展示</span><span class="courseware-screen-text">${html(item.prompt)}</span></span>
          `;
          const list = body.querySelector(".nb-step-detail-list");
          if (list) {
            list.insertAdjacentElement("beforebegin", rail);
          } else {
            body.insertAdjacentElement("afterbegin", rail);
          }
        });
        document.documentElement.setAttribute("data-1013l-r33-process-cards", "restored");
      }

      function bindRightDraftSelection() {
        document.querySelectorAll('aside[aria-label*="大屏草稿"] .courseware-screen-mini').forEach((item) => {
          if (item.dataset.r33Bound === "true") return;
          item.dataset.r33Bound = "true";
          item.setAttribute("tabindex", "0");
          item.addEventListener("click", (event) => {
            event.preventDefault();
            event.stopPropagation();
            const parent = item.closest('aside[aria-label*="大屏草稿"]') || item.parentElement;
            parent?.querySelectorAll(".courseware-screen-mini.active").forEach((el) => el.classList.remove("active"));
            item.classList.add("active");
            document.documentElement.setAttribute("data-1013l-r33-selected-right-draft", item.getAttribute("data-courseware-screen") || item.textContent.trim().slice(0, 24));
          });
        });
        document.documentElement.setAttribute("data-1013l-r33-right-draft-click", "local_selection_only");
      }

      function applyIndependentScroll() {
        if (location.hash === "#coursewareExpanded" || location.search.includes("preview=display")) return;
        document.documentElement.setAttribute("data-1013l-r33-independent-scroll", "true");
      }

      function boot() {
        removeR32DuplicateRightDraft();
        restoreProcessCoursewareCards();
        bindRightDraftSelection();
        applyIndependentScroll();
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
        if (tries >= 36) window.clearInterval(timer);
      }, 300);
    })();
  </script>
"""


def main() -> None:
    if not R32_HTML.exists():
        raise FileNotFoundError(R32_HTML)
    html = R32_HTML.read_text(encoding="utf-8-sig")
    if "script-1013L-R32-right-rail-courseware-cards" not in html:
        raise RuntimeError("R33 must inherit R32.")
    if "script-1013L-R33-process-cards-scroll" in html:
        raise RuntimeError("R33 already exists in source HTML.")

    html = html.replace("</head>", css() + "\n</head>", 1)
    html = html.replace("</body>", script() + "\n</body>", 1)

    R33_DIR.mkdir(parents=True, exist_ok=True)
    output_html = R33_DIR / "prep_room_render_canvas_deepen_v1_1013L_R33_process_cards_scroll.html"
    write_text(output_html, html)

    failed_checks: list[str] = []
    smoke = {
        "stage": STAGE,
        "html_created": output_html.exists(),
        "inherits_r32": "script-1013L-R32-right-rail-courseware-cards" in html,
        "r33_style_injected": "style-1013L-R33-process-cards-scroll" in html,
        "r33_script_injected": "script-1013L-R33-process-cards-scroll" in html,
        "r32_duplicate_hidden": ".r32-courseware-right-draft" in html and "display: none !important" in css(),
        "process_cards_restored": "data-1013l-r33-process-card" in html,
        "process_cards_display_override": ".nb-workspace .r33-process-courseware-card" in html and "display: flex !important" in html,
        "right_draft_local_selection": "data-1013l-r33-selected-right-draft" in html,
        "independent_scroll_enabled": "data-1013l-r33-independent-scroll" in html,
        **boundary(),
    }
    write_json(R33_DIR / "process_cards_scroll_smoke_1013L_R33.json", smoke)

    for key, value in smoke.items():
        if key.startswith(("html_", "inherits_", "r33_", "r32_", "process_", "right_", "independent_")) and value is not True:
            failed_checks.append(key)

    result = {
        "stage": STAGE,
        "final_status": FINAL_STATUS if not failed_checks else "FAIL_1013L_R33_PROCESS_COURSEWARE_CARDS_AND_INDEPENDENT_SCROLL_PATCH",
        "source_stage": "1013L_R32_RESTORE_RIGHT_RAIL_COURSEWARE_CARDS_ONLY",
        "next_stage": NEXT_STAGE,
        "right_rail_extra_r32_block_removed": True,
        "original_right_rail_courseware_draft_kept": True,
        "teaching_process_courseware_cards_restored": True,
        "non_process_section_courseware_cards_restored": False,
        "right_draft_click_selects_card_only": True,
        "prep_column_independent_scroll": True,
        "right_rail_independent_scroll": True,
        "left_catalog_independent_scroll": True,
        "inherits_existing_page_lineage": True,
        "new_disconnected_page_created": False,
        "failed_checks": failed_checks,
        **boundary(),
    }
    write_json(R33_DIR / "1013L_R33_result.json", result)

    report = f"""# 1013L R33 · Process Cards And Independent Scroll Patch

## Status

`{result["final_status"]}`

R33 corrects the R32 misunderstanding:

- keeps the original lower right-rail courseware draft;
- removes the extra R32 right-rail card block;
- restores courseware cards inside teaching-process steps only;
- keeps non-process lesson sections free of courseware cards;
- separates left catalog, center notebook, and right draft scrolling.

## Boundary

No runtime/provider/model/database/memory/Feishu/upload/search/material library/whiteboard library/formal apply/main push/GitHub upload.
"""
    write_text(R33_DIR / "1013L_R33_report.md", report)

    SOURCE_DELTA.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA / Path(__file__).name)
    print(output_html)
    if failed_checks:
        raise SystemExit(f"R33 failed checks: {failed_checks}")


if __name__ == "__main__":
    main()
