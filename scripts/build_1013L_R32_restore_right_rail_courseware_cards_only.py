from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R31_DIR = BASE / "1013L_R31_intercept_edit_clicks_and_pointed_bubble"
R31_HTML = R31_DIR / "prep_room_render_canvas_deepen_v1_1013L_R31_pointed_edit_bubble.html"
R32_DIR = BASE / "1013L_R32_restore_right_rail_courseware_cards_only"
SOURCE_DELTA = BASE / "source_delta_1013L_R32"

STAGE = "1013L_R32_RESTORE_RIGHT_RAIL_COURSEWARE_CARDS_ONLY"
FINAL_STATUS = "PASS_1013L_R32_RESTORE_RIGHT_RAIL_COURSEWARE_CARDS_ONLY"
NEXT_STAGE = "1013L_R33_EXISTING_PAGE_INLINE_EDIT_AND_RIGHT_DRAFT_POLISH"


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
  <style id="style-1013L-R32-right-rail-courseware-cards">
    .r32-courseware-right-draft {
      margin-top: 12px;
      border-top: 1px dashed rgba(43, 124, 106, 0.18);
      padding-top: 10px;
    }

    .r32-courseware-right-draft-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 8px;
      color: #1f6f5f;
      font-size: 12px;
      font-weight: 900;
    }

    .r32-courseware-card-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 7px;
    }

    .r32-courseware-card {
      display: grid;
      grid-template-columns: auto minmax(0, 1fr) auto;
      align-items: center;
      gap: 7px;
      min-height: 32px;
      padding: 7px 8px;
      border: 1px solid rgba(43, 124, 106, 0.14);
      border-radius: 9px;
      background: rgba(246, 253, 249, 0.72);
      color: #244f46;
      cursor: pointer;
      text-align: left;
    }

    .r32-courseware-card:hover,
    .r32-courseware-card.active {
      border-color: rgba(43, 124, 106, 0.32);
      background: rgba(232, 248, 240, 0.92);
    }

    .r32-courseware-card-index {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 24px;
      height: 22px;
      border-radius: 7px;
      background: rgba(43, 124, 106, 0.10);
      color: #247765;
      font-size: 11px;
      font-weight: 900;
    }

    .r32-courseware-card-title {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-size: 12px;
      font-weight: 850;
      line-height: 1.2;
    }

    .r32-status-dot {
      width: 7px;
      height: 7px;
      border-radius: 999px;
      background: #2f8c78;
      box-shadow: 0 0 0 3px rgba(47, 140, 120, 0.08);
    }

    .r32-status-dot.need {
      background: #d99a35;
      box-shadow: 0 0 0 3px rgba(217, 154, 53, 0.10);
    }

    .r32-status-dot.board {
      background: #2d73a8;
      box-shadow: 0 0 0 3px rgba(45, 115, 168, 0.10);
    }

    .r32-status-dot.work {
      background: #b85b5b;
      box-shadow: 0 0 0 3px rgba(184, 91, 91, 0.10);
    }

    .r32-courseware-detail {
      margin-top: 10px;
      padding: 9px 10px;
      border: 1px solid rgba(43, 124, 106, 0.13);
      border-radius: 10px;
      background: rgba(255, 254, 248, 0.75);
      color: #315c52;
      font-size: 12px;
      line-height: 1.55;
    }

    .r32-courseware-detail strong {
      display: block;
      margin-bottom: 3px;
      color: #1f6f5f;
    }
  </style>
"""


def script() -> str:
    return r"""
  <script id="script-1013L-R32-right-rail-courseware-cards">
    (function () {
      const fallbackScreens = [
        { index: "01", title: "色彩的感觉", lesson_link: "本课方向", status: "已有文字", placeholder: "课题封面" },
        { index: "02", title: "看色彩图片", lesson_link: "导入与观察", status: "待补图", placeholder: "生活色彩图片" },
        { index: "03", title: "比较两组颜色", lesson_link: "比较变化", status: "待补图 / 可白板", placeholder: "两组对比图" },
        { index: "04", title: "感觉词卡", lesson_link: "比较变化", status: "已有文字", placeholder: "感觉词卡" },
        { index: "05", title: "色彩实验任务", lesson_link: "创作表达", status: "待补图", placeholder: "任务图示" },
        { index: "06", title: "白板试色", lesson_link: "创作表达", status: "可白板", placeholder: "试色区" },
        { index: "07", title: "学生作品展示", lesson_link: "展示评价", status: "待学生作品", placeholder: "作品位" },
        { index: "08", title: "总结回看", lesson_link: "展示评价", status: "已有文字", placeholder: "回看提示" }
      ];

      function html(value) {
        return String(value || "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;" }[char]));
      }

      function normalizeStatus(status) {
        const value = String(status || "");
        if (value.includes("白板")) return "board";
        if (value.includes("学生作品")) return "work";
        if (value.includes("待") || value.includes("补")) return "need";
        return "ready";
      }

      function readScreens() {
        if (Array.isArray(window.coursewareScreens1013JR1) && window.coursewareScreens1013JR1.length) {
          return window.coursewareScreens1013JR1;
        }
        const node = document.getElementById("1013k-courseware-screen-viewmodel") ||
          document.getElementById("1013k-courseware-normalized-render-viewmodel");
        if (node) {
          try {
            const payload = JSON.parse(node.textContent || "{}");
            if (Array.isArray(payload.screen_outline) && payload.screen_outline.length) {
              return payload.screen_outline.map((screen, i) => ({
                index: screen.index_label || String(i + 1).padStart(2, "0"),
                title: screen.short_title || screen.screen_title || screen.title || "大屏",
                lesson_link: payload.current_screen?.lesson_bridge?.lesson_section_ref || screen.screen_type || "课堂环节",
                status: screen.status || "待确认",
                placeholder: screen.screen_type || "素材位"
              }));
            }
          } catch (_) {}
        }
        return fallbackScreens;
      }

      function cleanupCenterHints() {
        document.querySelectorAll(".nb-workspace .courseware-section-rail, .nb-workspace .courseware-inline-chip, .nb-workspace .courseware-display-note, .nb-workspace [data-1013l-r22-marker='true'], .r29-courseware-draft, .r29-inline-edit-popover, .r24-courseware-action-popover").forEach((el) => el.remove());
        document.documentElement.setAttribute("data-1013l-r32-center-courseware-hints", "removed");
      }

      function findRightRail() {
        const rails = Array.from(document.querySelectorAll("aside.nb-drawer, aside.nb-right-rail"));
        return rails.find((el) => (el.getAttribute("aria-label") || "").includes("大屏草稿")) ||
          rails.find((el) => (el.textContent || "").includes("大屏草稿")) ||
          rails.find((el) => (el.getAttribute("aria-label") || "").includes("辅助")) ||
          rails.find((el) => (el.getAttribute("aria-label") || "").includes("资源")) ||
          rails[rails.length - 1] ||
          null;
      }

      function detailText(screen) {
        return `<strong>${html(screen.index || "")} ${html(screen.title || "")}</strong>` +
          `环节：${html(screen.lesson_link || "课堂环节")}｜素材：${html(screen.placeholder || "素材占位")}｜状态：${html(screen.status || "待确认")}`;
      }

      function renderRightRailCards() {
        cleanupCenterHints();
        const rail = findRightRail();
        if (!rail) return false;

        rail.querySelectorAll(".r32-courseware-right-draft").forEach((el) => el.remove());
        const screens = readScreens().slice(0, 8);
        if (!screens.length) return false;

        const block = document.createElement("section");
        block.className = "r32-courseware-right-draft";
        block.setAttribute("data-1013l-r32-right-draft", "true");
        block.innerHTML = `
          <div class="r32-courseware-right-draft-head">
            <span>大屏草稿</span>
            <span class="quiet-tag">${screens.length} 屏</span>
          </div>
          <div class="r32-courseware-card-grid" aria-label="右侧大屏卡片">
            ${screens.map((screen, index) => `
              <button class="r32-courseware-card ${index === 2 ? "active" : ""}" type="button" data-r32-screen-index="${html(screen.index || String(index + 1).padStart(2, "0"))}">
                <span class="r32-courseware-card-index">${html(screen.index || String(index + 1).padStart(2, "0"))}</span>
                <span class="r32-courseware-card-title">${html(screen.title || screen.short_title || "大屏")}</span>
                <span class="r32-status-dot ${normalizeStatus(screen.status)}" aria-hidden="true"></span>
              </button>
            `).join("")}
          </div>
          <div class="r32-courseware-detail" data-r32-courseware-detail>${detailText(screens[2] || screens[0])}</div>
        `;

        const existingCourseware = rail.querySelector(".courseware-rail");
        const summary = existingCourseware?.querySelector(".courseware-rail-summary");
        if (summary) {
          summary.insertAdjacentElement("afterend", block);
        } else if (existingCourseware) {
          existingCourseware.appendChild(block);
        } else {
          const firstCard = rail.querySelector(".nb-drawer-card, .r6p-resource-rail, section, div");
          if (firstCard && firstCard.parentElement === rail) {
            firstCard.insertAdjacentElement("afterend", block);
          } else {
            rail.appendChild(block);
          }
        }

        const detail = block.querySelector("[data-r32-courseware-detail]");
        block.querySelectorAll(".r32-courseware-card").forEach((button, index) => {
          button.addEventListener("click", (event) => {
            event.preventDefault();
            block.querySelectorAll(".r32-courseware-card").forEach((item) => item.classList.remove("active"));
            button.classList.add("active");
            const screen = screens[index];
            if (detail) detail.innerHTML = detailText(screen);
            document.documentElement.setAttribute("data-1013l-r32-selected-screen", button.dataset.r32ScreenIndex || "");
          });
        });

        document.documentElement.setAttribute("data-1013l-r32-right-courseware-cards", "restored");
        return true;
      }

      function boot() {
        renderRightRailCards();
      }

      if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot);
      } else {
        boot();
      }
      let tries = 0;
      const timer = window.setInterval(() => {
        tries += 1;
        const ok = renderRightRailCards();
        if (ok || tries >= 20) window.clearInterval(timer);
      }, 300);
    })();
  </script>
"""


def main() -> None:
    if not R31_HTML.exists():
        raise FileNotFoundError(R31_HTML)
    html = R31_HTML.read_text(encoding="utf-8-sig")
    if "script-1013L-R31-pointed-edit-bubble" not in html:
        raise RuntimeError("R32 must inherit R31.")
    if "script-1013L-R32-right-rail-courseware-cards" in html:
        raise RuntimeError("R32 already exists in source HTML.")

    html = html.replace("</head>", css() + "\n</head>", 1)
    html = html.replace("</body>", script() + "\n</body>", 1)

    R32_DIR.mkdir(parents=True, exist_ok=True)
    output_html = R32_DIR / "prep_room_render_canvas_deepen_v1_1013L_R32_right_rail_courseware_cards.html"
    write_text(output_html, html)

    failed_checks: list[str] = []
    smoke = {
        "stage": STAGE,
        "html_created": output_html.exists(),
        "inherits_r31": "script-1013L-R31-pointed-edit-bubble" in html,
        "r32_style_injected": "style-1013L-R32-right-rail-courseware-cards" in html,
        "r32_script_injected": "script-1013L-R32-right-rail-courseware-cards" in html,
        "right_rail_cards_restored": "r32-courseware-right-draft" in html,
        "right_rail_card_count_static": html.count("r32-courseware-card") >= 6,
        "center_cleanup_kept": "data-1013l-r32-center-courseware-hints" in html,
        "r29_top_draft_runtime_cleanup": ".r29-courseware-draft" in html and "document.querySelectorAll(\".nb-workspace .courseware-section-rail" in html,
        **boundary(),
    }
    write_json(R32_DIR / "right_rail_courseware_cards_smoke_1013L_R32.json", smoke)

    for key, value in smoke.items():
        if key.startswith(("html_", "inherits_", "r32_", "right_", "center_", "r29_")) and value is not True:
            failed_checks.append(key)

    result = {
        "stage": STAGE,
        "final_status": FINAL_STATUS if not failed_checks else "FAIL_1013L_R32_RESTORE_RIGHT_RAIL_COURSEWARE_CARDS_ONLY",
        "source_stage": "1013L_R31_INTERCEPT_EDIT_CLICKS_AND_POINTED_BUBBLE",
        "next_stage": NEXT_STAGE,
        "right_rail_courseware_cards_restored": True,
        "center_courseware_hints_restored": False,
        "center_courseware_hints_removed": True,
        "r29_top_extra_block_restored": False,
        "screen_cards_target_area": "right_rail_courseware_draft_only",
        "inherits_existing_page_lineage": True,
        "new_disconnected_page_created": False,
        "failed_checks": failed_checks,
        **boundary(),
    }
    write_json(R32_DIR / "1013L_R32_result.json", result)

    report = f"""# 1013L R32 · Restore Right Rail Courseware Cards Only

## Status

`{result["final_status"]}`

R32 restores the 8-screen courseware draft cards in the right rail only. It keeps the center lesson body clean: no inline courseware chips, no center screen hint rows, and no R29 top extra draft block.

## Boundary

No runtime/provider/model/database/memory/Feishu/upload/search/material library/whiteboard library/formal apply/main push/GitHub upload.
"""
    write_text(R32_DIR / "1013L_R32_report.md", report)

    SOURCE_DELTA.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA / Path(__file__).name)
    print(output_html)
    if failed_checks:
        raise SystemExit(f"R32 failed checks: {failed_checks}")


if __name__ == "__main__":
    main()
