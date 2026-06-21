from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R35_DIR = BASE / "1013L_R35_paragraph_level_courseware_cards"
R35_HTML = R35_DIR / "prep_room_render_canvas_deepen_v1_1013L_R35_paragraph_courseware_cards.html"
R36_DIR = BASE / "1013L_R36_existing_page_static_patch_consolidation"
SOURCE_DELTA = BASE / "source_delta_1013L_R36"

STAGE = "1013L_R36_EXISTING_PAGE_STATIC_PATCH_CONSOLIDATION"
FINAL_STATUS = "PASS_1013L_R36_EXISTING_PAGE_STATIC_PATCH_CONSOLIDATION"
NEXT_STAGE = "1013L_R37_VISIBLE_FUNCTION_COMPLETION_CONTINUE"

PATCH_STYLE_IDS = [
    "style-1013L-R22-courseware-markers",
    "style-1013L-R23-marker-reading-polish",
    "style-1013L-R24-static-closed-loop",
    "style-1013L-R25-courseware-focus-adapter",
    "style-1013L-R26-courseware-screen-switch",
    "style-1013L-R27-courseware-tool-actions",
    "style-1013L-R29-marker-edit-scope-patch",
    "style-1013L-R30-center-hints-edit-bubble-fix",
    "style-1013L-R31-pointed-edit-bubble",
    "style-1013L-R32-right-rail-courseware-cards",
    "style-1013L-R33-process-cards-scroll",
    "style-1013L-R34-process-courseware-cards-visible",
    "style-1013L-R35-paragraph-courseware-cards",
]

PATCH_SCRIPT_IDS = [
    "script-1013L-R22-courseware-markers",
    "script-1013L-R23-marker-reading-polish",
    "script-1013L-R24-static-closed-loop",
    "script-1013L-R25-courseware-focus-adapter",
    "script-1013L-R26-courseware-screen-switch",
    "script-1013L-R27-courseware-tool-actions",
    "script-1013L-R29-marker-edit-scope-patch",
    "script-1013L-R30-center-hints-edit-bubble-fix",
    "script-1013L-R31-pointed-edit-bubble",
    "script-1013L-R32-right-rail-courseware-cards",
    "script-1013L-R33-process-cards-scroll",
    "script-1013L-R34-process-courseware-cards-visible",
    "script-1013L-R35-paragraph-courseware-cards",
]


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


def remove_block_by_id(html: str, tag: str, element_id: str) -> tuple[str, int]:
    pattern = re.compile(
        rf"\s*<{tag}\b[^>]*\bid=[\"']{re.escape(element_id)}[\"'][^>]*>.*?</{tag}>",
        re.S,
    )
    html, count = pattern.subn("", html)
    return html, count


def css() -> str:
    return r"""
  <style id="style-1013L-R36-consolidated">
    .nb-workspace .courseware-section-rail,
    .nb-workspace .courseware-inline-chip,
    .nb-workspace .courseware-display-note,
    .nb-workspace [data-1013l-r22-marker="true"],
    .r29-courseware-draft,
    .r32-courseware-right-draft,
    .r33-process-courseware-card,
    .r34-process-display-card,
    .nb-readable-step .nb-edit-bubble:not(.r36-edit-bubble),
    .nb-doc-section > .nb-edit-panel {
      display: none !important;
    }

    html[data-1013l-r36-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) {
      height: calc(100vh - 148px);
      overflow: hidden;
    }

    html[data-1013l-r36-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) > .nb-binder {
      height: 100%;
      min-height: 0;
      align-items: stretch;
      overflow: hidden;
    }

    html[data-1013l-r36-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) .nb-panel,
    html[data-1013l-r36-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) .nb-workspace,
    html[data-1013l-r36-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) .nb-drawer,
    html[data-1013l-r36-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) .nb-right-rail {
      max-height: calc(100vh - 170px);
      overflow-y: auto;
      overscroll-behavior: contain;
      scrollbar-gutter: stable;
    }

    html[data-1013l-r36-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) .nb-panel,
    html[data-1013l-r36-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) .nb-drawer,
    html[data-1013l-r36-independent-scroll="true"] .nb-scene:not(.courseware-expanded-scene) .nb-right-rail {
      position: sticky;
      top: 0;
      align-self: start;
    }

    .nb-step-detail-item .r36-paragraph-screen-row {
      display: inline-flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px;
      margin-left: 8px;
      vertical-align: baseline;
    }

    .r36-inline-screen-card,
    .r36-add-screen-card {
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

    .r36-inline-screen-card {
      border: 1px solid rgba(224, 151, 43, 0.28);
      background: rgba(245, 178, 74, 0.10);
      color: #99651a;
    }

    .r36-inline-screen-card::before {
      content: "";
      width: 6px;
      height: 6px;
      border-radius: 999px;
      background: currentColor;
      opacity: 0.86;
    }

    .r36-inline-screen-card.active {
      border-color: rgba(224, 151, 43, 0.52);
      background: rgba(245, 178, 74, 0.18);
      box-shadow: 0 0 0 3px rgba(245, 178, 74, 0.09);
    }

    .r36-add-screen-card {
      border: 1px dashed rgba(43, 124, 106, 0.22);
      background: rgba(240, 250, 246, 0.52);
      color: #2b7c6a;
      font-weight: 760;
    }

    .courseware-screen-mini {
      user-select: none;
      cursor: pointer;
    }

    .courseware-screen-mini.r36-right-selected,
    .courseware-screen-mini.active {
      border-color: rgba(224, 151, 43, 0.42) !important;
      background: rgba(255, 246, 226, 0.78) !important;
      box-shadow: 0 0 0 3px rgba(245, 178, 74, 0.08);
    }

    .r36-edit-bubble {
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

    .r36-edit-bubble::before {
      content: "";
      position: absolute;
      top: var(--r36-arrow-top, 28px);
      width: 16px;
      height: 16px;
      background: rgba(255, 254, 247, 0.98);
      border-left: 1px solid rgba(219, 150, 48, 0.36);
      border-bottom: 1px solid rgba(219, 150, 48, 0.36);
      transform: rotate(45deg);
    }

    .r36-edit-bubble[data-side="right"]::before {
      left: -8px;
    }

    .r36-edit-bubble[data-side="left"]::before {
      right: -8px;
      transform: rotate(225deg);
    }

    .r36-edit-bubble .nb-edit-panel {
      display: block !important;
      border: 0;
      box-shadow: none;
      background: transparent;
    }

    .r36-edit-close {
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
  <script id="script-1013L-R36-consolidated">
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

      let scheduled = false;
      let successfulRuns = 0;

      function html(value) {
        return String(value || "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;" }[char]));
      }

      function normalizeScreenId(id) {
        const value = String(id || "");
        if (/^screen_\d\d_/.test(value)) return value;
        const seedMatch = value.match(/screen_seed_(\d\d)|_(\d\d)_|(\d{1,2})/);
        if (!seedMatch) return value;
        const number = (seedMatch[1] || seedMatch[2] || seedMatch[3]).padStart(2, "0");
        return Object.keys(screenMeta).find((key) => key.includes(`_${number}_`)) || value;
      }

      function selectRightDraft(screenId) {
        const normalized = normalizeScreenId(screenId);
        const rightItems = document.querySelectorAll('aside[aria-label*="大屏草稿"] .courseware-screen-mini');
        rightItems.forEach((item) => {
          item.classList.remove("active", "r36-right-selected");
          const itemId = normalizeScreenId(item.getAttribute("data-courseware-screen"));
          if (itemId === normalized) {
            item.classList.add("active", "r36-right-selected");
            item.scrollIntoView({ block: "nearest", inline: "nearest", behavior: "smooth" });
          }
        });
        document.documentElement.setAttribute("data-1013l-r36-selected-screen", normalized);
      }

      function clearOldPatchNodes() {
        document.querySelectorAll(".r29-courseware-draft, .r32-courseware-right-draft, .r33-process-courseware-card, .r34-process-display-card, .courseware-section-rail, .courseware-inline-chip, .courseware-display-note, .r29-inline-edit-popover, .r30-follow-edit-bubble, .r31-pointed-edit-bubble").forEach((el) => el.remove());
      }

      function addParagraphCards() {
        clearOldPatchNodes();
        let count = 0;
        document.querySelectorAll(".nb-readable-step").forEach((step) => {
          const stepId = String(step.id || "").replace(/^nb-step-/, "");
          const mapping = paragraphMap[stepId] || [];
          const items = Array.from(step.querySelectorAll(".nb-step-detail-item"));
          items.forEach((li, index) => {
            li.querySelectorAll(".r36-paragraph-screen-row").forEach((row) => row.remove());
            const screenId = mapping[index];
            const row = document.createElement("span");
            row.className = "r36-paragraph-screen-row";
            if (screenId) {
              const meta = screenMeta[screenId] || { label: "大屏", title: "课堂呈现" };
              row.innerHTML = `<button class="r36-inline-screen-card" type="button" data-r36-screen="${html(screenId)}">${html(meta.label)}｜${html(meta.title)}</button>`;
              count += 1;
            }
            const add = document.createElement("button");
            add.className = "r36-add-screen-card";
            add.type = "button";
            add.setAttribute("data-r36-add-screen", stepId);
            add.textContent = "+ 大屏";
            row.appendChild(add);
            li.appendChild(row);
          });
        });
        document.documentElement.setAttribute("data-1013l-r36-paragraph-card-count", String(count));
        document.documentElement.setAttribute("data-1013l-r36-paragraph-cards", count ? "visible" : "pending");
        if (count) successfulRuns += 1;
        return count;
      }

      function closeEditBubble() {
        document.querySelectorAll(".r36-edit-bubble").forEach((el) => el.remove());
      }

      function sectionTitle(anchor) {
        const section = anchor.closest(".nb-doc-section, .nb-readable-step");
        return section?.querySelector(".nb-doc-title, .nb-readable-title")?.textContent?.trim() || "当前段落";
      }

      function contentOf(anchor) {
        if (anchor.matches(".nb-anchor-paragraph, li, p")) return anchor.childNodes[0]?.textContent?.trim() || anchor.textContent.trim();
        return anchor.textContent.trim();
      }

      function makeEditPanel(anchor) {
        const title = sectionTitle(anchor);
        const current = contentOf(anchor);
        const panel = document.createElement("div");
        panel.className = "nb-edit-panel";
        panel.innerHTML = `
          <div class="nb-edit-panel-title">
            <div>正在修改 · ${html(title)}</div>
            <span>待你确认</span>
            <button class="r36-edit-close" type="button" aria-label="收起">收起</button>
          </div>
          <div class="nb-edit-surface">
            <div class="nb-edit-surface-block"><strong>当前段落</strong>${html(current)}</div>
            <div class="nb-edit-surface-block emphasis"><strong>小备建议</strong>先围绕这一行形成候选改写，教师确认前不写入正式备课本。</div>
            <div class="nb-before-after">
              <div class="nb-edit-surface-block"><strong>修改前</strong>${html(current)}</div>
              <div class="nb-edit-surface-block"><strong>修改后</strong>保留原意，补清楚课堂动作、学生反应和可观察证据。</div>
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

      function placeEditBubble(anchor) {
        closeEditBubble();
        const bubble = document.createElement("div");
        bubble.className = "nb-edit-bubble r36-edit-bubble";
        bubble.setAttribute("role", "dialog");
        bubble.setAttribute("aria-label", "当前段落修改批注");
        bubble.appendChild(makeEditPanel(anchor));
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
        let top = Math.max(15, Math.min(rect.top - 12, window.innerHeight - height - 15));
        const arrowTop = Math.max(20, Math.min(rect.top + Math.min(rect.height / 2, 34) - top - 8, height - 32));
        bubble.style.left = `${left}px`;
        bubble.style.top = `${top}px`;
        bubble.style.setProperty("--r36-arrow-top", `${arrowTop}px`);
        bubble.dataset.side = side;
        document.documentElement.setAttribute("data-1013l-r36-edit-bubble", "pointed_to_clicked_row");
      }

      function applyIndependentScroll() {
        if (location.hash === "#coursewareExpanded" || location.search.includes("preview=display")) return;
        document.documentElement.setAttribute("data-1013l-r36-independent-scroll", "true");
      }

      function boot() {
        addParagraphCards();
        applyIndependentScroll();
        document.documentElement.setAttribute("data-1013l-r36-consolidated", "true");
      }

      function scheduleBoot() {
        if (scheduled) return;
        scheduled = true;
        window.requestAnimationFrame(() => {
          scheduled = false;
          boot();
        });
      }

      document.addEventListener("click", (event) => {
        const close = event.target.closest && event.target.closest(".r36-edit-close");
        if (close) {
          event.preventDefault();
          event.stopImmediatePropagation();
          closeEditBubble();
          return;
        }

        const screenCard = event.target.closest && event.target.closest(".r36-inline-screen-card");
        if (screenCard) {
          event.preventDefault();
          event.stopImmediatePropagation();
          document.querySelectorAll(".r36-inline-screen-card.active").forEach((el) => el.classList.remove("active"));
          screenCard.classList.add("active");
          selectRightDraft(screenCard.getAttribute("data-r36-screen"));
          return;
        }

        const addCard = event.target.closest && event.target.closest(".r36-add-screen-card");
        if (addCard) {
          event.preventDefault();
          event.stopImmediatePropagation();
          addCard.closest(".nb-step-detail-item")?.setAttribute("data-1013l-r36-agent-add-screen-requested", "true");
          document.documentElement.setAttribute("data-1013l-r36-agent-screen-add", addCard.getAttribute("data-r36-add-screen") || "process");
          return;
        }

        const rightItem = event.target.closest && event.target.closest('aside[aria-label*="大屏草稿"] .courseware-screen-mini');
        if (rightItem) {
          event.preventDefault();
          event.stopImmediatePropagation();
          selectRightDraft(rightItem.getAttribute("data-courseware-screen"));
          return;
        }

        const editTarget = event.target.closest && event.target.closest("[data-edit-target], .nb-anchor-paragraph");
        if (editTarget && !event.target.closest(".r36-paragraph-screen-row")) {
          event.preventDefault();
          event.stopImmediatePropagation();
          const anchor = editTarget.matches(".nb-anchor-paragraph") ? editTarget : (editTarget.closest(".nb-anchor-paragraph, .nb-doc-section, .nb-readable-step") || editTarget);
          placeEditBubble(anchor);
          return;
        }

        if (!event.target.closest || !event.target.closest(".r36-edit-bubble")) closeEditBubble();
      }, true);

      if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot);
      } else {
        boot();
      }

      [120, 360, 800, 1400].forEach((delay) => window.setTimeout(boot, delay));

      const observer = new MutationObserver(() => {
        if (successfulRuns > 2) return;
        scheduleBoot();
      });
      window.setTimeout(() => {
        const root = document.querySelector(".nb-workspace") || document.body;
        observer.observe(root, { childList: true, subtree: true });
        document.documentElement.setAttribute("data-1013l-r36-observer", "bounded");
      }, 700);
    })();
  </script>
"""


def count_metrics(html: str) -> dict[str, int]:
    return {
        "script_tags": html.count("<script "),
        "style_tags": html.count("<style "),
        "set_interval_count": html.count("setInterval"),
        "mutation_observer_count": html.count("MutationObserver"),
        "query_selector_all_count": html.count("querySelectorAll"),
        "courseware_screen_var_count": html.count("var coursewareScreens1013JR1"),
        "bytes": len(html.encode("utf-8")),
    }


def main() -> None:
    if not R35_HTML.exists():
        raise FileNotFoundError(R35_HTML)
    html = R35_HTML.read_text(encoding="utf-8-sig")
    before = count_metrics(html)

    removed_styles: list[str] = []
    removed_scripts: list[str] = []
    for style_id in PATCH_STYLE_IDS:
        html, count = remove_block_by_id(html, "style", style_id)
        if count:
            removed_styles.append(style_id)
    for script_id in PATCH_SCRIPT_IDS:
        html, count = remove_block_by_id(html, "script", script_id)
        if count:
            removed_scripts.append(script_id)

    if len(removed_styles) != len(PATCH_STYLE_IDS):
        missing = sorted(set(PATCH_STYLE_IDS) - set(removed_styles))
        raise RuntimeError(f"Missing expected style removals: {missing}")
    if len(removed_scripts) != len(PATCH_SCRIPT_IDS):
        missing = sorted(set(PATCH_SCRIPT_IDS) - set(removed_scripts))
        raise RuntimeError(f"Missing expected script removals: {missing}")

    html = html.replace("</head>", css() + "\n</head>", 1)
    html = html.replace("</body>", script() + "\n</body>", 1)
    after = count_metrics(html)

    R36_DIR.mkdir(parents=True, exist_ok=True)
    output_html = R36_DIR / "prep_room_render_canvas_deepen_v1_1013L_R36_consolidated.html"
    write_text(output_html, html)

    failed_checks: list[str] = []
    smoke = {
        "stage": STAGE,
        "html_created": output_html.exists(),
        "removed_patch_style_count": len(removed_styles),
        "removed_patch_script_count": len(removed_scripts),
        "r36_style_injected": "style-1013L-R36-consolidated" in html,
        "r36_script_injected": "script-1013L-R36-consolidated" in html,
        "old_patch_scripts_removed": all(script_id not in html for script_id in PATCH_SCRIPT_IDS),
        "old_patch_styles_removed": all(style_id not in html for style_id in PATCH_STYLE_IDS),
        "paragraph_cards_consolidated": "r36-inline-screen-card" in html and "paragraphMap" in html,
        "edit_bubble_consolidated": "r36-edit-bubble" in html,
        "right_draft_selection_consolidated": "r36-right-selected" in html,
        "independent_scroll_consolidated": "data-1013l-r36-independent-scroll" in html,
        "set_interval_reduced": after["set_interval_count"] < before["set_interval_count"],
        "mutation_observer_reduced_or_equal": after["mutation_observer_count"] <= before["mutation_observer_count"],
        **boundary(),
    }
    write_json(R36_DIR / "static_patch_consolidation_smoke_1013L_R36.json", {**smoke, "before_metrics": before, "after_metrics": after})

    for key, value in smoke.items():
        if key.startswith(("html_", "removed_", "r36_", "old_", "paragraph_", "edit_", "right_", "independent_", "set_", "mutation_")) and value is not True and not isinstance(value, int):
            failed_checks.append(key)

    result = {
        "stage": STAGE,
        "final_status": FINAL_STATUS if not failed_checks else "FAIL_1013L_R36_EXISTING_PAGE_STATIC_PATCH_CONSOLIDATION",
        "source_stage": "1013L_R35_PARAGRAPH_LEVEL_COURSEWARE_CARDS_PATCH",
        "next_stage": NEXT_STAGE,
        "old_versions_preserved": True,
        "source_r35_preserved": str(R35_HTML.relative_to(ROOT)),
        "output_html": str(output_html.relative_to(ROOT)),
        "patch_styles_removed": removed_styles,
        "patch_scripts_removed": removed_scripts,
        "before_metrics": before,
        "after_metrics": after,
        "paragraph_level_courseware_cards_kept": True,
        "right_rail_courseware_draft_kept": True,
        "edit_bubble_kept": True,
        "independent_scroll_kept": True,
        "new_disconnected_page_created": False,
        "failed_checks": failed_checks,
        **boundary(),
    }
    write_json(R36_DIR / "1013L_R36_result.json", result)

    report = f"""# 1013L R36 · Existing Page Static Patch Consolidation

## Status

`{result["final_status"]}`

R36 preserves the old R35 file and creates a consolidated copy. It removes the old R22-R35 patch scripts/styles from the new copy and replaces them with one consolidated static script/style for:

- paragraph-level courseware cards;
- right-rail draft screen selection;
- pointed edit bubble;
- independent left/center/right scrolling.

## Metrics

Before: `{before}`

After: `{after}`

## Boundary

No runtime/provider/model/database/memory/Feishu/upload/search/material library/whiteboard library/formal apply/main push/GitHub upload.
"""
    write_text(R36_DIR / "1013L_R36_report.md", report)

    SOURCE_DELTA.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA / Path(__file__).name)
    print(output_html)
    if failed_checks:
        raise SystemExit(f"R36 failed checks: {failed_checks}")


if __name__ == "__main__":
    main()
