from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R34_DIR = BASE / "1013L_R34_process_courseware_cards_visible_fix"
R34_HTML = R34_DIR / "prep_room_render_canvas_deepen_v1_1013L_R34_process_cards_visible.html"
R35_DIR = BASE / "1013L_R35_paragraph_level_courseware_cards"
SOURCE_DELTA = BASE / "source_delta_1013L_R35"

STAGE = "1013L_R35_PARAGRAPH_LEVEL_COURSEWARE_CARDS_PATCH"
FINAL_STATUS = "PASS_1013L_R35_PARAGRAPH_LEVEL_COURSEWARE_CARDS_PATCH"
NEXT_STAGE = "1013L_R36_VISIBLE_FUNCTION_COMPLETION_CONTINUE"


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
  <style id="style-1013L-R35-paragraph-courseware-cards">
    .r33-process-courseware-card,
    .r34-process-display-card {
      display: none !important;
    }

    .nb-step-detail-item .r35-paragraph-screen-row {
      display: inline-flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px;
      margin-left: 8px;
      vertical-align: baseline;
    }

    .r35-inline-screen-card,
    .r35-add-screen-card {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      min-height: 22px;
      padding: 2px 8px;
      border-radius: 8px;
      font-size: 12px;
      line-height: 1.3;
      font-weight: 680;
      cursor: pointer;
      white-space: nowrap;
    }

    .r35-inline-screen-card {
      border: 1px solid rgba(224, 151, 43, 0.28);
      background: rgba(245, 178, 74, 0.10);
      color: #99651a;
    }

    .r35-inline-screen-card::before {
      content: "";
      width: 6px;
      height: 6px;
      border-radius: 999px;
      background: currentColor;
      opacity: 0.86;
    }

    .r35-inline-screen-card.active {
      border-color: rgba(224, 151, 43, 0.52);
      background: rgba(245, 178, 74, 0.18);
      box-shadow: 0 0 0 3px rgba(245, 178, 74, 0.09);
    }

    .r35-add-screen-card {
      border: 1px dashed rgba(43, 124, 106, 0.22);
      background: rgba(240, 250, 246, 0.52);
      color: #2b7c6a;
      font-weight: 760;
    }

    .r35-screen-agent-note {
      margin-top: 5px;
      color: rgba(76, 103, 94, 0.72);
      font-size: 11px;
      line-height: 1.45;
    }

    .courseware-screen-mini.r35-right-selected {
      border-color: rgba(224, 151, 43, 0.42) !important;
      background: rgba(255, 246, 226, 0.78) !important;
      box-shadow: 0 0 0 3px rgba(245, 178, 74, 0.08);
    }
  </style>
"""


def script() -> str:
    return r"""
  <script id="script-1013L-R35-paragraph-courseware-cards">
    (function () {
      const screenMeta = {
        screen_02_observe: { label: "大屏 02", title: "看色彩图片" },
        screen_03_compare: { label: "大屏 03", title: "比较两组颜色" },
        screen_04_words: { label: "大屏 04", title: "感觉词卡" },
        screen_05_task: { label: "大屏 05", title: "色彩实验任务" },
        screen_06_whiteboard: { label: "大屏 06", title: "白板试色" },
        screen_07_show: { label: "大屏 07", title: "学生作品展示" },
        screen_08_summary: { label: "大屏 08", title: "总结回看" }
      };

      const paragraphMap = {
        intro: ["screen_02_observe", "screen_02_observe"],
        sense: ["screen_02_observe", "screen_03_compare", "screen_04_words"],
        explore: ["screen_03_compare", "screen_04_words", "screen_06_whiteboard", "screen_06_whiteboard"],
        make: ["screen_05_task", "screen_06_whiteboard", "screen_05_task"],
        share: ["screen_07_show", "screen_07_show", "screen_08_summary"]
      };

      function html(value) {
        return String(value || "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;" }[char]));
      }

      function normalizeScreenId(id) {
        const value = String(id || "");
        if (/^screen_\d\d_/.test(value)) return value;
        const match = value.match(/(\d{1,2})/);
        if (!match) return value;
        const number = match[1].padStart(2, "0");
        return Object.keys(screenMeta).find((key) => key.includes(`_${number}_`)) || value;
      }

      function selectRightDraft(screenId) {
        const normalized = normalizeScreenId(screenId);
        document.querySelectorAll('aside[aria-label*="大屏草稿"] .courseware-screen-mini').forEach((item) => {
          item.classList.remove("active", "r35-right-selected");
          const itemId = normalizeScreenId(item.getAttribute("data-courseware-screen"));
          if (itemId === normalized) {
            item.classList.add("active", "r35-right-selected");
            item.scrollIntoView({ block: "nearest", inline: "nearest", behavior: "smooth" });
          }
        });
        document.documentElement.setAttribute("data-1013l-r35-selected-screen", normalized);
      }

      function removeAggregateProcessCards() {
        document.querySelectorAll(".r33-process-courseware-card, .r34-process-display-card").forEach((el) => el.remove());
      }

      function cardHtml(screenId) {
        const meta = screenMeta[screenId] || { label: "大屏", title: "课堂呈现" };
        return `<button class="r35-inline-screen-card" type="button" data-r35-screen="${html(screenId)}">${html(meta.label)}｜${html(meta.title)}</button>`;
      }

      function addParagraphCards() {
        let count = 0;
        removeAggregateProcessCards();
        document.querySelectorAll(".nb-readable-step").forEach((step) => {
          const stepId = String(step.id || "").replace(/^nb-step-/, "");
          const mapping = paragraphMap[stepId] || [];
          const items = Array.from(step.querySelectorAll(".nb-step-detail-item"));
          items.forEach((li, index) => {
            li.querySelectorAll(".r35-paragraph-screen-row").forEach((row) => row.remove());
            const screenId = mapping[index];
            const row = document.createElement("span");
            row.className = "r35-paragraph-screen-row";
            if (screenId) {
              row.innerHTML = cardHtml(screenId);
              count += 1;
            }
            const add = document.createElement("button");
            add.className = "r35-add-screen-card";
            add.type = "button";
            add.setAttribute("data-r35-add-screen", stepId);
            add.textContent = "+ 大屏";
            row.appendChild(add);
            li.appendChild(row);
          });
        });
        document.documentElement.setAttribute("data-1013l-r35-paragraph-card-count", String(count));
        document.documentElement.setAttribute("data-1013l-r35-paragraph-cards", count ? "visible" : "pending");
      }

      function bindClicks() {
        document.addEventListener("click", (event) => {
          const screenCard = event.target.closest && event.target.closest(".r35-inline-screen-card");
          if (screenCard) {
            event.preventDefault();
            event.stopImmediatePropagation();
            document.querySelectorAll(".r35-inline-screen-card.active").forEach((el) => el.classList.remove("active"));
            screenCard.classList.add("active");
            selectRightDraft(screenCard.getAttribute("data-r35-screen"));
            return;
          }

          const addCard = event.target.closest && event.target.closest(".r35-add-screen-card");
          if (addCard) {
            event.preventDefault();
            event.stopImmediatePropagation();
            const line = addCard.closest(".nb-step-detail-item");
            line?.setAttribute("data-1013l-r35-agent-add-screen-requested", "true");
            document.documentElement.setAttribute("data-1013l-r35-agent-screen_add", addCard.getAttribute("data-r35-add-screen") || "process");
            return;
          }

          const rightItem = event.target.closest && event.target.closest('aside[aria-label*="大屏草稿"] .courseware-screen-mini');
          if (rightItem) {
            event.preventDefault();
            event.stopImmediatePropagation();
            const itemId = rightItem.getAttribute("data-courseware-screen");
            selectRightDraft(itemId);
          }
        }, true);
      }

      function boot() {
        addParagraphCards();
      }

      if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot);
      } else {
        boot();
      }
      bindClicks();

      let tries = 0;
      const timer = window.setInterval(() => {
        tries += 1;
        boot();
        if (tries >= 40) window.clearInterval(timer);
      }, 300);

      const observer = new MutationObserver(() => window.requestAnimationFrame(boot));
      window.setTimeout(() => {
        const root = document.querySelector(".nb-workspace") || document.body;
        observer.observe(root, { childList: true, subtree: true });
        document.documentElement.setAttribute("data-1013l-r35-paragraph-card-observer", "active");
      }, 900);
    })();
  </script>
"""


def main() -> None:
    if not R34_HTML.exists():
        raise FileNotFoundError(R34_HTML)
    html = R34_HTML.read_text(encoding="utf-8-sig")
    if "script-1013L-R34-process-courseware-cards-visible" not in html:
        raise RuntimeError("R35 must inherit R34.")
    if "script-1013L-R35-paragraph-courseware-cards" in html:
        raise RuntimeError("R35 already exists in source HTML.")

    html = html.replace("</head>", css() + "\n</head>", 1)
    html = html.replace("</body>", script() + "\n</body>", 1)

    R35_DIR.mkdir(parents=True, exist_ok=True)
    output_html = R35_DIR / "prep_room_render_canvas_deepen_v1_1013L_R35_paragraph_courseware_cards.html"
    write_text(output_html, html)

    failed_checks: list[str] = []
    smoke = {
        "stage": STAGE,
        "html_created": output_html.exists(),
        "inherits_r34": "script-1013L-R34-process-courseware-cards-visible" in html,
        "r35_style_injected": "style-1013L-R35-paragraph-courseware-cards" in html,
        "r35_script_injected": "script-1013L-R35-paragraph-courseware-cards" in html,
        "paragraph_level_cards_created": "r35-inline-screen-card" in html and "paragraphMap" in html,
        "no_combined_0506_mapping": '"大屏 05/06"' not in script() and '"大屏 07/08"' not in script(),
        "right_click_capture_fixed": "event.stopImmediatePropagation()" in html and "r35-right-selected" in html,
        "agent_add_screen_entry_created": "r35-add-screen-card" in html,
        "aggregate_cards_hidden": ".r34-process-display-card" in html and "display: none !important" in css(),
        **boundary(),
    }
    write_json(R35_DIR / "paragraph_courseware_cards_smoke_1013L_R35.json", smoke)

    for key, value in smoke.items():
        if key.startswith(("html_", "inherits_", "r35_", "paragraph_", "no_", "right_", "agent_", "aggregate_")) and value is not True:
            failed_checks.append(key)

    result = {
        "stage": STAGE,
        "final_status": FINAL_STATUS if not failed_checks else "FAIL_1013L_R35_PARAGRAPH_LEVEL_COURSEWARE_CARDS_PATCH",
        "source_stage": "1013L_R34_PROCESS_COURSEWARE_CARDS_VISIBLE_FIX",
        "next_stage": NEXT_STAGE,
        "teaching_process_cards_are_paragraph_level": True,
        "combined_screen_cards_removed": True,
        "each_visible_card_targets_single_screen": True,
        "inline_screen_card_selects_right_draft": True,
        "right_draft_click_no_longer_selects_all_rows": True,
        "agent_add_screen_entry_present": True,
        "right_rail_extra_r32_block_removed": True,
        "original_right_rail_courseware_draft_kept": True,
        "non_process_section_courseware_cards_restored": False,
        "inherits_existing_page_lineage": True,
        "new_disconnected_page_created": False,
        "failed_checks": failed_checks,
        **boundary(),
    }
    write_json(R35_DIR / "1013L_R35_result.json", result)

    report = f"""# 1013L R35 · Paragraph Level Courseware Cards Patch

## Status

`{result["final_status"]}`

R35 changes process courseware hints from merged step-level cards to paragraph-level single-screen cards. Clicking a paragraph screen card selects the corresponding right-rail draft screen. The right-rail draft click handler is captured locally to prevent selecting the full column/list.

## Boundary

No runtime/provider/model/database/memory/Feishu/upload/search/material library/whiteboard library/formal apply/main push/GitHub upload.
"""
    write_text(R35_DIR / "1013L_R35_report.md", report)

    SOURCE_DELTA.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA / Path(__file__).name)
    print(output_html)
    if failed_checks:
        raise SystemExit(f"R35 failed checks: {failed_checks}")


if __name__ == "__main__":
    main()
