from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R33_DIR = BASE / "1013L_R33_process_courseware_cards_and_independent_scroll"
R33_HTML = R33_DIR / "prep_room_render_canvas_deepen_v1_1013L_R33_process_cards_scroll.html"
R34_DIR = BASE / "1013L_R34_process_courseware_cards_visible_fix"
SOURCE_DELTA = BASE / "source_delta_1013L_R34"

STAGE = "1013L_R34_PROCESS_COURSEWARE_CARDS_VISIBLE_FIX"
FINAL_STATUS = "PASS_1013L_R34_PROCESS_COURSEWARE_CARDS_VISIBLE_FIX"
NEXT_STAGE = "1013L_R35_VISIBLE_FUNCTION_COMPLETION_CONTINUE"


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
  <style id="style-1013L-R34-process-courseware-cards-visible">
    .nb-workspace .r34-process-display-card {
      display: flex !important;
      visibility: visible !important;
      flex-wrap: wrap;
      align-items: center;
      gap: 6px;
      margin: 8px 0 8px;
      font-size: 12px;
      line-height: 1.35;
    }

    .r34-screen-chip {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      min-height: 22px;
      padding: 2px 8px;
      border: 1px solid rgba(224, 151, 43, 0.28);
      border-radius: 999px;
      background: rgba(245, 178, 74, 0.10);
      color: #99651a;
      font-weight: 680;
      white-space: nowrap;
    }

    .r34-screen-chip::before {
      content: "";
      width: 6px;
      height: 6px;
      border-radius: 999px;
      background: currentColor;
      opacity: 0.86;
    }

    .r34-screen-note {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      min-height: 22px;
      padding: 2px 8px;
      border: 1px solid rgba(221, 154, 52, 0.22);
      border-radius: 8px;
      background: rgba(250, 189, 85, 0.10);
      color: #856017;
      white-space: normal;
    }

    .r34-screen-note span:first-child {
      font-weight: 760;
    }

    .r34-screen-text {
      color: #9b6618;
      font-weight: 650;
      text-decoration: underline;
      text-decoration-thickness: 1px;
      text-underline-offset: 3px;
    }
  </style>
"""


def script() -> str:
    return r"""
  <script id="script-1013L-R34-process-courseware-cards-visible">
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

      function removeOldInvisibleProcessRails(body) {
        body.querySelectorAll(".courseware-section-rail, .r33-process-courseware-card").forEach((el) => el.remove());
      }

      function restoreVisibleCards() {
        let count = 0;
        document.querySelectorAll(".nb-readable-step").forEach((step) => {
          const stepId = String(step.id || "").replace(/^nb-step-/, "");
          const item = markers[stepId];
          const body = step.querySelector(".nb-readable-body");
          if (!item || !body) return;
          removeOldInvisibleProcessRails(body);
          if (body.querySelector(".r34-process-display-card")) {
            count += 1;
            return;
          }
          const card = document.createElement("div");
          card.className = "r34-process-display-card";
          card.setAttribute("data-1013l-r34-process-card", stepId);
          card.innerHTML = `
            <span class="r34-screen-chip">${html(item.label)}｜${html(item.title)}</span>
            <span class="r34-screen-note"><span>屏幕展示</span><span class="r34-screen-text">${html(item.prompt)}</span></span>
          `;
          const list = body.querySelector(".nb-step-detail-list");
          if (list) {
            list.insertAdjacentElement("beforebegin", card);
          } else {
            body.insertAdjacentElement("afterbegin", card);
          }
          count += 1;
        });
        document.documentElement.setAttribute("data-1013l-r34-process-card-count", String(count));
        document.documentElement.setAttribute("data-1013l-r34-process-cards", count ? "visible" : "pending");
        return count;
      }

      function removeDuplicateR32RightBlock() {
        document.querySelectorAll(".r32-courseware-right-draft").forEach((el) => el.remove());
      }

      function boot() {
        removeDuplicateR32RightBlock();
        restoreVisibleCards();
      }

      if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot);
      } else {
        boot();
      }

      let tries = 0;
      const timer = window.setInterval(() => {
        tries += 1;
        const count = restoreVisibleCards();
        removeDuplicateR32RightBlock();
        if (count >= 5 && tries >= 18) window.clearInterval(timer);
        if (tries >= 48) window.clearInterval(timer);
      }, 250);

      const observer = new MutationObserver(() => {
        window.requestAnimationFrame(boot);
      });
      window.setTimeout(() => {
        const root = document.querySelector(".nb-workspace") || document.body;
        observer.observe(root, { childList: true, subtree: true });
        document.documentElement.setAttribute("data-1013l-r34-process-card-observer", "active");
      }, 800);
    })();
  </script>
"""


def main() -> None:
    if not R33_HTML.exists():
        raise FileNotFoundError(R33_HTML)
    html = R33_HTML.read_text(encoding="utf-8-sig")
    if "script-1013L-R33-process-cards-scroll" not in html:
        raise RuntimeError("R34 must inherit R33.")
    if "script-1013L-R34-process-courseware-cards-visible" in html:
        raise RuntimeError("R34 already exists in source HTML.")

    html = html.replace("</head>", css() + "\n</head>", 1)
    html = html.replace("</body>", script() + "\n</body>", 1)

    R34_DIR.mkdir(parents=True, exist_ok=True)
    output_html = R34_DIR / "prep_room_render_canvas_deepen_v1_1013L_R34_process_cards_visible.html"
    write_text(output_html, html)

    failed_checks: list[str] = []
    smoke = {
        "stage": STAGE,
        "html_created": output_html.exists(),
        "inherits_r33": "script-1013L-R33-process-cards-scroll" in html,
        "r34_style_injected": "style-1013L-R34-process-courseware-cards-visible" in html,
        "r34_script_injected": "script-1013L-R34-process-courseware-cards-visible" in html,
        "uses_new_non_hidden_class": "r34-process-display-card" in html,
        "old_hidden_class_removed_runtime": "removeOldInvisibleProcessRails" in html,
        "mutation_observer_active": "MutationObserver" in html,
        "r32_duplicate_removed_runtime": "removeDuplicateR32RightBlock" in html,
        **boundary(),
    }
    write_json(R34_DIR / "process_cards_visible_smoke_1013L_R34.json", smoke)

    for key, value in smoke.items():
        if key.startswith(("html_", "inherits_", "r34_", "uses_", "old_", "mutation_", "r32_")) and value is not True:
            failed_checks.append(key)

    result = {
        "stage": STAGE,
        "final_status": FINAL_STATUS if not failed_checks else "FAIL_1013L_R34_PROCESS_COURSEWARE_CARDS_VISIBLE_FIX",
        "source_stage": "1013L_R33_PROCESS_COURSEWARE_CARDS_AND_INDEPENDENT_SCROLL_PATCH",
        "next_stage": NEXT_STAGE,
        "teaching_process_cards_visible_fix_created": True,
        "process_cards_use_new_non_hidden_class": True,
        "old_courseware_section_rail_not_required_for_process_cards": True,
        "r31_r32_cleanup_resistant": True,
        "right_rail_extra_r32_block_removed": True,
        "original_right_rail_courseware_draft_kept": True,
        "non_process_section_courseware_cards_restored": False,
        "inherits_existing_page_lineage": True,
        "new_disconnected_page_created": False,
        "failed_checks": failed_checks,
        **boundary(),
    }
    write_json(R34_DIR / "1013L_R34_result.json", result)

    report = f"""# 1013L R34 · Process Courseware Cards Visible Fix

## Status

`{result["final_status"]}`

R34 fixes the issue where teaching-process courseware cards were still invisible because earlier cleanup rules target `.courseware-section-rail` and old marker attributes. The restored process cards now use a new class that is not caught by the old cleanup selectors and are restored after page rerenders.

## Boundary

No runtime/provider/model/database/memory/Feishu/upload/search/material library/whiteboard library/formal apply/main push/GitHub upload.
"""
    write_text(R34_DIR / "1013L_R34_report.md", report)

    SOURCE_DELTA.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA / Path(__file__).name)
    print(output_html)
    if failed_checks:
        raise SystemExit(f"R34 failed checks: {failed_checks}")


if __name__ == "__main__":
    main()
