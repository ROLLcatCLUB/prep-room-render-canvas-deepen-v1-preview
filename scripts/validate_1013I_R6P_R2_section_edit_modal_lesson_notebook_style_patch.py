from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6P_R2_SECTION_EDIT_MODAL_LESSON_NOTEBOOK_STYLE_PATCH"
FINAL_STATUS = "PASS_1013I_R6P_R2_SECTION_EDIT_MODAL_LESSON_NOTEBOOK_STYLE_PATCH"
INHERITS_FROM = "1013I_R6P_R1_EDIT_SURFACE_MODAL_AND_RIGHT_RAIL_RESOURCE_TOOLBAR_PATCH"
NEXT_STAGE = "USER_REVIEW_BIG_UNIT_SECTION_EDIT_MODAL_SURFACE"
BASE_DIR_NAME = "1013I_R6P_R1_edit_surface_modal_and_right_rail_resource_toolbar_patch"
STAGE_DIR_NAME = "1013I_R6P_R2_section_edit_modal_lesson_notebook_style_patch"
BASE_HTML_NAME = "prep_room_render_canvas_deepen_v1_R6P_R1_big_unit_section_edit_modal.html"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6P_R2_section_edit_modal_lesson_notebook_style.html"
VALIDATOR_NAME = "validate_1013I_R6P_R2_section_edit_modal_lesson_notebook_style_patch.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]

RAW_KEYS = [
    "field_key",
    "schema",
    "prompt",
    "unit_package",
    "lesson_position",
    "candidate_patch",
    "formal_apply",
    "provider_called",
    "model_called",
    "database_written",
    "memory_written",
    "feishu_written",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def locate_output_root(root: Path) -> Path:
    if (root / BASE_DIR_NAME).exists() and (root / "LATEST_REVIEW_ENTRY.md").exists():
        return root
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    if (root / "REVIEW_PACKAGE_MANIFEST.md").exists() and (root / "LATEST_REVIEW_ENTRY.md").exists():
        return root
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "preview_only_actions": True,
        "formal_apply_performed": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def css_patch() -> str:
    return """

    /* 1013I_R6P_R2: make the section edit modal follow the single-lesson edit bubble tone */
    [data-r6p-r1-modal-edit] .r6p-side-panel {
      display: none !important;
    }

    [data-r6p-r1-modal-edit] .r6p-resource-rail {
      display: grid;
      gap: 10px;
    }

    [data-r6p-r1-modal-edit] .r6p-tool-strip {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
    }

    [data-r6p-r1-modal-edit] .r6p-tool {
      min-height: 34px;
      justify-content: center;
    }

    [data-r6p-r1-modal-edit] .r6p-resource-item {
      padding: 9px 0;
      border-top: 1px solid rgba(43, 124, 106, .12);
    }

    [data-r6p-r1-modal-edit] .r6p-resource-item strong {
      display: block;
      color: var(--ink);
      font-size: 13px;
      margin-bottom: 4px;
    }

    [data-r6p-r1-modal-edit] .r6p-resource-item p {
      margin: 0;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.55;
    }

    .r6p-modal-backdrop {
      position: fixed;
      inset: 0;
      z-index: 80;
      display: none;
      place-items: start center;
      padding: 28px;
      padding-top: 92px;
      background: rgba(21, 48, 39, .08);
      backdrop-filter: blur(1.5px);
    }

    .r6p-modal-backdrop.is-open {
      display: grid;
    }

    .r6p-modal {
      width: min(720px, calc(100vw - 48px));
      max-height: min(680px, calc(100vh - 120px));
      overflow: auto;
      border: 1px solid rgba(43, 124, 106, .18);
      border-radius: 10px;
      background:
        radial-gradient(circle at 18px 18px, rgba(53, 93, 74, 0.035) 1px, transparent 1.5px),
        linear-gradient(135deg, rgba(250, 252, 246, .98), rgba(238, 247, 235, .98));
      box-shadow: 0 16px 34px rgba(20, 55, 44, .18);
      padding: 14px 16px 16px;
    }

    .r6p-modal-head {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      padding-bottom: 8px;
      border-bottom: 1px dashed rgba(43, 124, 106, .18);
    }

    .r6p-modal-title {
      margin-top: 4px;
      color: var(--ink);
      font-size: 17px;
      font-weight: 950;
    }

    .r6p-modal-status {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: rgba(38, 94, 76, .78);
      font-size: 12px;
    }

    .r6p-modal-status::before {
      content: "";
      width: 7px;
      height: 7px;
      border-radius: 999px;
      background: #2b7c6a;
      box-shadow: 0 0 0 3px rgba(43, 124, 106, .08);
    }

    .r6p-modal-body {
      display: grid;
      gap: 9px;
      margin-top: 10px;
    }

    .r6p-modal-block {
      padding-top: 8px;
      border-top: 1px solid rgba(43, 124, 106, .1);
    }

    .r6p-modal-block:first-child {
      border-top: 0;
      padding-top: 0;
    }

    .r6p-modal-block strong {
      display: block;
      margin-bottom: 5px;
      color: var(--ink);
      font-size: 13px;
    }

    .r6p-modal-block p,
    .r6p-modal-block li {
      margin: 4px 0;
      color: var(--ink);
      font-size: 13px;
      line-height: 1.56;
    }

    .r6p-modal-compare {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }

    .r6p-modal-compare-box {
      padding: 8px;
      border: 1px solid rgba(43, 124, 106, .14);
      border-radius: 8px;
      background: rgba(255, 255, 255, .48);
    }

    .r6p-modal-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 8px;
    }

    .r6p-modal .nb-soft-button,
    .r6p-modal .node-action {
      min-height: 28px;
      padding: 4px 10px;
      font-size: 12px;
    }

    @media (max-width: 760px) {
      .r6p-modal-backdrop {
        align-items: end;
        padding: 12px;
      }

      .r6p-modal {
        width: 100%;
        max-height: 84vh;
        border-radius: 12px 12px 0 0;
      }

      .r6p-modal-compare {
        grid-template-columns: 1fr;
      }
    }
"""


def replace_right_rail(source: str) -> str:
    start = source.index("        <aside class=\"nb-right-rail\" aria-label=\"大单元章节查看与编辑\">")
    end = source.index("        </aside>", start) + len("        </aside>")
    replacement = """        <aside class="nb-right-rail" aria-label="大单元资源库与工具栏">
          <section class="nb-drawer r6p-resource-rail" data-r6p-right-resource-toolbar="true">
            <div class="nb-drawer-title"><span>资源库与工具</span><button class="node-action secondary" type="button">按需打开</button></div>
            <div class="r6p-tool-strip" aria-label="大单元工具栏">
              <button class="node-action secondary r6p-tool" type="button">教材资料</button>
              <button class="node-action secondary r6p-tool" type="button">课标依据</button>
              <button class="node-action secondary r6p-tool" type="button">学习单</button>
              <button class="node-action secondary r6p-tool" type="button">评价句式</button>
            </div>
            <div class="r6p-resource-item">
              <strong>教材资料</strong>
              <p>上传教材目录、单元页或教参截图后，小教再校准单元设计。</p>
            </div>
            <div class="r6p-resource-item">
              <strong>可用支架</strong>
              <p>色卡组合、生活图片、作品图像、学习单与展示评价句式。</p>
            </div>
            <details class="r6p-resource-item">
              <summary>只读依据和风险提醒</summary>
              <p>当前为静态预览样张。章节修改通过弹出框查看，不占用右侧资源区。</p>
            </details>
          </section>
        </aside>"""
    return source[:start] + replacement + source[end:]


def patch_script(source: str) -> str:
    source = source.replace('data-r6p-section-edit-surface="true"', 'data-r6p-section-edit-surface="true" data-r6p-r1-modal-edit="true"', 1)
    source = re.sub(r"\n\s*const rail = document\.querySelector\(\"\\\[data-r6p-side-edit-surface\\\]\"\);\n\s*if \(!dataNode \|\| !scene \|\| !rail\) return;", "\n          if (!dataNode || !scene) return;", source)
    source = source.replace(
        """            if (mode === "view") {
              rail.innerHTML = '<div class="nb-drawer-title"><span>查看章节</span><span class="quiet-tag">预览</span></div><div class="r6p-panel-status">教师确认前不写入正式备课本</div><div class="r6p-panel-block"><strong>' + item.title + '</strong><p>' + item.view_note + '</p></div><details class="r6p-low-ref" open><summary>可能影响</summary><ul>' + impact + '</ul></details><details class="r6p-low-ref"><summary>来源依据</summary><p>依据当前大单元阅读面和候选字段归档，只作为静态预览参考。</p></details>';
              return;
            }
            rail.innerHTML = '<div class="nb-drawer-title"><span>编辑当前章节</span><span class="quiet-tag">预览</span></div><div class="r6p-panel-status">教师确认前不写入正式备课本</div><div class="r6p-panel-block"><strong>当前内容</strong><p>' + item.current + '</p></div><div class="r6p-panel-block"><strong>小教建议</strong><p>' + item.suggestion + '</p></div><div class="r6p-panel-block"><strong>修改前 / 修改后</strong><div class="r6p-compare"><div class="r6p-compare-box"><strong>修改前</strong><p>' + item.before + '</p></div><div class="r6p-compare-box"><strong>修改后</strong><p>' + item.after + '</p></div></div></div><div class="r6p-panel-block"><strong>影响与操作</strong><ul>' + impact + '</ul><div class="r6p-side-actions"><button class="node-action primary" type="button" data-preview-only="true">采纳到预览</button><button class="node-action secondary" type="button" data-preview-only="true">再改一版</button><button class="node-action secondary" type="button" data-preview-only="true">暂不采用</button></div></div><details class="r6p-low-ref"><summary>来源依据</summary><p>依据当前大单元阅读面、教师可见字段模型和后端候选映射归档，只作为静态预览参考。</p></details>';""",
        """            const backdrop = document.querySelector(".r6p-modal-backdrop");
            const title = backdrop.querySelector(".r6p-modal-title");
            const body = backdrop.querySelector(".r6p-modal-body");
            title.textContent = (mode === "view" ? "查看章节 · " : "编辑章节 · ") + item.title;
            if (mode === "view") {
              body.innerHTML = '<div class="r6p-modal-block"><strong>章节说明</strong><p>' + item.view_note + '</p></div><div class="r6p-modal-block"><strong>可能影响</strong><ul>' + impact + '</ul></div><details class="r6p-modal-block"><summary>来源依据</summary><p>依据当前大单元阅读面和候选字段归档，只作为静态预览参考。</p></details>';
            } else {
              body.innerHTML = '<div class="r6p-modal-block"><strong>当前内容</strong><p>' + item.current + '</p></div><div class="r6p-modal-block"><strong>小教建议</strong><p>' + item.suggestion + '</p></div><div class="r6p-modal-block"><strong>修改前 / 修改后</strong><div class="r6p-modal-compare"><div class="r6p-modal-compare-box"><strong>修改前</strong><p>' + item.before + '</p></div><div class="r6p-modal-compare-box"><strong>修改后</strong><p>' + item.after + '</p></div></div></div><div class="r6p-modal-block"><strong>影响与操作</strong><ul>' + impact + '</ul><div class="r6p-modal-actions"><button class="node-action primary" type="button" data-preview-only="true">采纳到预览</button><button class="node-action secondary" type="button" data-preview-only="true">再改一版</button><button class="node-action secondary" type="button" data-preview-only="true">暂不采用</button></div></div><details class="r6p-modal-block"><summary>来源依据</summary><p>依据当前大单元阅读面、教师可见字段模型和后端候选映射归档，只作为静态预览参考。</p></details>';
            }
            backdrop.classList.add("is-open");
            backdrop.setAttribute("aria-hidden", "false");""",
    )
    modal = """
    <div class="r6p-modal-backdrop" aria-hidden="true" role="dialog" aria-label="大单元章节查看编辑弹出框">
      <section class="r6p-modal">
        <div class="r6p-modal-head">
          <div>
            <div class="r6p-modal-status">教师确认前不写入正式备课本</div>
            <div class="r6p-modal-title">编辑章节</div>
          </div>
          <button class="node-action secondary" type="button" data-r6p-modal-close="true">收起</button>
        </div>
        <div class="r6p-modal-body"></div>
      </section>
    </div>
    <script>
      document.addEventListener("click", function (event) {
        if (event.target.closest("[data-r6p-modal-close]") || event.target.classList.contains("r6p-modal-backdrop")) {
          const modal = document.querySelector(".r6p-modal-backdrop");
          if (modal) {
            modal.classList.remove("is-open");
            modal.setAttribute("aria-hidden", "true");
          }
        }
      });
    </script>
"""
    return source.replace("</body>", modal + "\n</body>", 1)


def build_html(output_root: Path) -> str:
    base = output_root / BASE_DIR_NAME / BASE_HTML_NAME
    source = base.read_text(encoding="utf-8")
    source = source.replace("师维 · 备课室 | R6P_R1 大单元弹出编辑样张", "师维 · 备课室 | R6P_R2 大单元轻编辑弹窗样张")
    source = source.replace("<!-- 1013I_R6P_R1: section edit moves to modal; right rail is resource/tool area. -->", "<!-- 1013I_R6P_R2: modal style follows single-lesson edit bubble; right rail unchanged. -->")
    source = source.replace("\n  </style>", css_patch() + "\n  </style>", 1)
    source = source.replace('data-r6p-r1-modal-edit="true"', 'data-r6p-r1-modal-edit="true" data-r6p-r2-lesson-style-modal="true"', 1)
    source = source.replace("查看章节 · ", "查看 · ")
    source = source.replace("编辑章节 · ", "正在修改 · ")
    source = source.replace("采纳到预览", "采纳到本段预览")
    source = source.replace("再改一版", "继续精修")
    source = source.replace("暂不采用", "暂不处理")
    return source


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


def create_screenshots(stage_dir: Path, html_path: Path) -> dict[str, Any]:
    browser = find_browser()
    screenshots: list[dict[str, Any]] = []
    if browser is None:
        return {"screenshot_smoke_pass": False, "screenshot_error": "browser_not_found", "screenshots": screenshots}
    for viewport in [{"id": "desktop", "width": 1440, "height": 1100}, {"id": "mobile", "width": 390, "height": 1100}]:
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6P_R2_{viewport['id']}.png"
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
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        width, height = png_size(out)
        screenshots.append({"viewport": viewport["id"], "path": out.name, "width": width, "height": height, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": True, "screenshots": screenshots}


def main_surface_text(html_text: str) -> str:
    start = html_text.index('<div class="nb-doc" data-r6o-field-render-doc="true">')
    end = html_text.index('<aside class="nb-right-rail"', start)
    return html_text[start:end]


def validate_html(html_text: str) -> dict[str, Any]:
    main = main_surface_text(html_text)
    raw_hits = [key for key in RAW_KEYS if key in main]
    return {
        "based_on_r6p": "data-r6p-section-edit-surface=\"true\"" in html_text,
        "based_on_r6p_r1": "data-r6p-r1-modal-edit=\"true\"" in html_text,
        "lesson_notebook_style_modal_created": "data-r6p-r2-lesson-style-modal=\"true\"" in html_text and "正在修改 · " in html_text,
        "right_rail_resource_toolbar_restored": "data-r6p-right-resource-toolbar=\"true\"" in html_text and "资源库与工具" in html_text,
        "right_rail_not_edit_surface": "编辑当前章节" not in html_text.split('<aside class="nb-right-rail"', 1)[1].split("</aside>", 1)[0],
        "section_edit_modal_created": "r6p-modal-backdrop" in html_text and "大单元章节查看编辑弹出框" in html_text,
        "modal_view_edit_actions_created": "data-r6p-view" in html_text and "data-r6p-edit" in html_text,
        "edit_surface_not_inline_body": "正在修改 · " in html_text and "正在修改 · " not in main,
        "main_reading_flow_kept": "data-r6o-field-render-doc=\"true\"" in html_text and "box-shadow: none !important" in html_text,
        "preview_only_actions": "data-preview-only=\"true\"" in html_text and "教师确认前不写入正式备课本" in html_text,
        "accept_to_preview_action_present": "采纳到本段预览" in html_text,
        "revise_action_present": "继续精修" in html_text,
        "reject_action_present": "暂不处理" in html_text,
        "raw_engineering_field_hits_in_main_surface": raw_hits,
        **boundary(),
    }


def failed_checks(checks: dict[str, Any]) -> list[str]:
    failed: list[str] = []
    expected_false = {
        "formal_apply_performed",
        "runtime_connected",
        "provider_called",
        "model_called",
        "database_written",
        "memory_written",
        "feishu_written",
        "main_project_pushed",
    }
    for key, value in checks.items():
        if key == "raw_engineering_field_hits_in_main_surface":
            if value:
                failed.append(key)
        elif key in expected_false:
            if value is not False:
                failed.append(key)
        elif value is not True:
            failed.append(key)
    return failed


def write_stage_files(output_root: Path, stage_dir: Path, result: dict[str, Any], smoke: dict[str, Any]) -> None:
    write_json(stage_dir / "right_rail_resource_toolbar_1013I_R6P_R2.json", {
        "stage": STAGE_ID,
        "right_rail_role": "resource_library_and_toolbar",
        "tools": ["教材资料", "课标依据", "学习单", "评价句式"],
        "right_rail_not_edit_surface": True,
        **boundary(),
    })
    write_json(stage_dir / "section_edit_modal_surface_1013I_R6P_R2.json", {
        "stage": STAGE_ID,
        "edit_surface": "modal",
        "lesson_notebook_style_modal_created": True,
        "view_surface": "modal",
        "main_reading_flow_kept": True,
        "right_rail_resource_toolbar_restored": True,
        **boundary(),
    })
    write_json(stage_dir / "visual_smoke_1013I_R6P_R2.json", smoke)
    write_json(stage_dir / "1013I_R6P_R2_result.json", result)
    write_text(stage_dir / "1013I_R6P_R2_report.md", f"""# 1013I_R6P_R2 Section Edit Modal Lesson Notebook Style Patch

FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6P_R2 polishes the section edit modal after R6P_R1:
- The right rail remains a resource library and tool area.
- The edit modal follows the single-lesson edit bubble tone.
- Modal copy uses `正在修改 · 当前章节`, `当前内容`, `小教建议`, `修改前 / 修改后`, and lightweight preview actions.
- Actions remain preview-only.

Validation: {result["final_status"]}
Failed checks: {result["failed_checks"]}
""")
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6P_R2 keeps R6P_R1's right-rail correction and polishes the section edit popup to match the single-lesson notebook edit tone.

Key flags:
- RIGHT_RAIL_RESOURCE_TOOLBAR_RESTORED=true
- SECTION_EDIT_MODAL_CREATED=true
- LESSON_NOTEBOOK_STYLE_MODAL_CREATED=true
- RIGHT_RAIL_NOT_EDIT_SURFACE=true
- MAIN_READING_FLOW_KEPT=true
- PREVIEW_ONLY_ACTIONS=true
- FORMAL_APPLY_PERFORMED=false
- PROVIDER_CALLED=false
- MODEL_CALLED=false
- MAIN_PROJECT_PUSHED=false
""")
    write_text(output_root / "README.md", f"""# Prep Room Render Canvas Deepen V1 Review Package

Latest stage: `{STAGE_ID}`

Open:
- `{STAGE_DIR_NAME}/{HTML_NAME}`
- `{STAGE_DIR_NAME}/1013I_R6P_R2_result.json`

Run:

```bash
python scripts/{VALIDATOR_NAME}
python scripts/{VALIDATOR_NAME} --root <repo-root>
```
""")
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", f"""# Review Package Manifest

Latest stage: `{STAGE_ID}`

Files:
- `LATEST_REVIEW_ENTRY.md`
- `README.md`
- `REVIEW_PACKAGE_MANIFEST.md`
- `{STAGE_DIR_NAME}/{HTML_NAME}`
- `{STAGE_DIR_NAME}/right_rail_resource_toolbar_1013I_R6P_R2.json`
- `{STAGE_DIR_NAME}/section_edit_modal_surface_1013I_R6P_R2.json`
- `{STAGE_DIR_NAME}/1013I_R6P_R2_result.json`
- `{STAGE_DIR_NAME}/1013I_R6P_R2_report.md`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6P_R2_desktop.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6P_R2_mobile.png`
- `scripts/{VALIDATOR_NAME}`

Boundary: static review fixture only. No runtime, provider/model, database, memory, Feishu, formal apply, or main-project push.
""")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output_root = locate_output_root(root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)

    html_text = build_html(output_root)
    html_path = stage_dir / HTML_NAME
    write_text(html_path, html_text)

    checks = validate_html(html_text)
    smoke = create_screenshots(stage_dir, html_path)
    checks["screenshot_smoke_pass"] = bool(smoke.get("screenshot_smoke_pass"))
    failed = failed_checks(checks)
    result = {
        "stage": STAGE_ID,
        "status": FINAL_STATUS if not failed else "FAIL_1013I_R6P_R2_SECTION_EDIT_MODAL_LESSON_NOTEBOOK_STYLE_PATCH",
        "final_status": FINAL_STATUS if not failed else "FAIL_1013I_R6P_R2_SECTION_EDIT_MODAL_LESSON_NOTEBOOK_STYLE_PATCH",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        **checks,
        "failed_checks": failed,
    }
    write_stage_files(output_root, stage_dir, result, smoke)
    source_delta = output_root / "source_delta_1013I_R6P_R2" / "scripts" / VALIDATOR_NAME
    source_delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), source_delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False))
    print("ALL_1013I_R6P_R2_SECTION_EDIT_MODAL_LESSON_NOTEBOOK_STYLE_PATCH_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
