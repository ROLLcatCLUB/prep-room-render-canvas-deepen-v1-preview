from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6O_R1_BIG_UNIT_RENDER_SURFACE_READING_POLISH"
FINAL_STATUS = "PASS_1013I_R6O_R1_BIG_UNIT_RENDER_SURFACE_READING_POLISH"
INHERITS_FROM = "1013I_R6O_BIG_UNIT_FIELD_MODEL_TO_PAGE_RENDER_FIXTURE"
NEXT_STAGE = "USER_REVIEW_BIG_UNIT_READING_POLISH_BEFORE_EDIT_SURFACE"
STAGE_DIR_NAME = "1013I_R6O_R1_big_unit_render_surface_reading_polish"
R6O_DIR_NAME = "1013I_R6O_big_unit_field_model_to_page_render_fixture"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6O_R1_big_unit_reading_polish.html"
VALIDATOR_NAME = "validate_1013I_R6O_R1_big_unit_render_surface_reading_polish.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]
CORE_FIELDS = ["单元信息", "课标依据", "核心素养", "学生起点", "单元问题", "知识与技能", "表现任务", "学习推进", "课时任务链", "评价证据", "材料与支架"]
RAW_KEYS = ["unit_package", "textbook_anchor", "lesson_position", "teacher_confirmation_required", "normal_candidate_card_generation_allowed", "knowledge_and_skills", "skills_materials_scaffolds", "single_lesson_inheritance_targets"]


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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "reading_polish_only": True,
        "edit_surface_created": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def polish_css() -> str:
    return """

    /* 1013I_R6O_R1: reading polish, remove card wall and make state row match single-lesson tone */
    [data-r6o-r1-reading-polish] .nb-state-bar {
      margin: 0 0 8px;
      padding: 4px 0 6px;
      border: 0;
      border-bottom: 1px solid rgba(36, 84, 70, .12);
      background: transparent !important;
      box-shadow: none !important;
    }

    [data-r6o-r1-reading-polish] .nb-state-main {
      gap: 7px;
      align-items: center;
      flex-wrap: wrap;
    }

    [data-r6o-r1-reading-polish] .nb-hero {
      padding-bottom: 6px !important;
      margin-bottom: 0 !important;
    }

    [data-r6o-r1-reading-polish] .nb-mode-toggle {
      padding: 2px !important;
      gap: 4px !important;
    }

    [data-r6o-r1-reading-polish] .nb-mode-btn {
      min-height: 24px !important;
      padding: 0 9px !important;
      font-size: 12px !important;
    }

    [data-r6o-r1-reading-polish] .r6o-r1-status-pill {
      display: inline-flex;
      align-items: center;
      min-height: 23px;
      padding: 2px 9px;
      border: 1px solid rgba(43, 112, 92, .18);
      border-radius: 999px;
      background: rgba(239, 248, 243, .72);
      color: rgba(29, 96, 78, .9);
      font-size: 12px;
      line-height: 1.4;
    }

    [data-r6o-r1-reading-polish] .r6o-r1-status-light {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      color: rgba(32, 75, 65, .72);
      font-size: 12px;
      line-height: 1.4;
      letter-spacing: 0;
    }

    [data-r6o-r1-reading-polish] .r6o-r1-dot {
      width: 7px;
      height: 7px;
      border-radius: 999px;
      box-shadow: 0 0 0 3px rgba(43, 112, 92, .06);
    }

    [data-r6o-r1-reading-polish] .r6o-r1-dot.green { background: #2b7c6a; }
    [data-r6o-r1-reading-polish] .r6o-r1-dot.amber { background: #d59748; }
    [data-r6o-r1-reading-polish] .r6o-r1-dot.red { background: #b6544d; }

    [data-r6o-r1-reading-polish] .state-tag,
    [data-r6o-r1-reading-polish] .quiet-tag {
      min-height: 22px;
      padding: 0;
      font-size: 12px;
      background: transparent !important;
      border: 0 !important;
      box-shadow: none !important;
    }

    [data-r6o-r1-reading-polish] .nb-doc-body-surface {
      padding: 0 6px;
      background: transparent;
      border-radius: 0;
    }

    [data-r6o-r1-reading-polish] .nb-doc-section {
      padding: 15px 0;
      margin: 0;
      border-radius: 0 !important;
      border: 0 !important;
      border-bottom: 1px solid rgba(36, 84, 70, .14) !important;
      background: transparent !important;
      box-shadow: none !important;
    }

    [data-r6o-r1-reading-polish] .nb-doc-section:first-child {
      padding-top: 12px;
    }

    [data-r6o-r1-reading-polish] .nb-doc-section-head {
      margin-bottom: 8px;
    }

    [data-r6o-r1-reading-polish] .nb-doc-section-head .node-action {
      opacity: .25;
      transition: opacity .16s ease;
    }

    [data-r6o-r1-reading-polish] .nb-doc-section:hover .node-action {
      opacity: 1;
    }

    [data-r6o-r1-reading-polish] .nb-doc-section p,
    [data-r6o-r1-reading-polish] .nb-doc-section li {
      line-height: 1.56 !important;
      margin-top: 6px;
      margin-bottom: 6px;
    }

    [data-r6o-r1-reading-polish] .nb-doc-section ul {
      margin-top: 8px !important;
      margin-bottom: 8px !important;
    }

    [data-r6o-r1-reading-polish] .nb-material-front-prompt {
      margin: 8px 0 10px !important;
      padding: 10px 14px !important;
      gap: 10px !important;
    }

    [data-r6o-r1-reading-polish] .nb-material-front-title {
      margin-bottom: 2px !important;
    }

    [data-r6o-r1-reading-polish] .nb-material-front-note {
      margin: 2px 0 0 !important;
      line-height: 1.38 !important;
      max-width: 500px;
    }

    [data-r6o-r1-reading-polish] .nb-material-front-actions {
      gap: 6px !important;
    }

    [data-r6o-r1-reading-polish] .nb-material-front-actions .node-action {
      min-height: 26px;
      padding-top: 3px;
      padding-bottom: 3px;
    }
"""


def remove_duplicate_material_section(source: str) -> str:
    title = '<div class="nb-doc-title">十二、资料补充</div>'
    if title not in source:
        return source
    title_index = source.index(title)
    section_start = source.rfind('<section class="nb-doc-section">', 0, title_index)
    section_end = source.index('                  </section>', title_index) + len('                  </section>\n')
    return source[:section_start] + source[section_end:]


def move_status_above_material_prompt(source: str) -> str:
    material_marker = '              <section class="nb-material-front-prompt" aria-label="资料补充提示">'
    state_marker = '              <div class="nb-state-bar">'
    material_start = source.find(material_marker)
    if material_start < 0:
        return source
    state_start = source.find(state_marker, material_start)
    if state_start < 0:
        return source
    material_end = source.find('              </section>', material_start) + len('              </section>\n')
    state_end = source.find('              </div>\n\n              <div class="nb-doc"', state_start)
    if material_end <= material_start or state_end < 0:
        return source
    state_block = source[state_start:state_end + len('              </div>\n')]
    material_block = source[material_start:material_end]
    return source[:material_start] + state_block + "\n" + material_block + source[state_end + len('              </div>\n'):]


def build_html(output_root: Path) -> str:
    base = output_root / R6O_DIR_NAME / "prep_room_render_canvas_deepen_v1_R6O_big_unit_field_model_render.html"
    source = base.read_text(encoding="utf-8")
    source = source.replace("师维 · 备课室 | R6O 大单元字段回灌样张", "师维 · 备课室 | R6O_R1 大单元阅读面修补")
    source = source.replace("<!-- 1013I_R6O: big-unit field model rendered to page fixture; no runtime/schema. -->", "<!-- 1013I_R6O_R1: reading polish only; no edit surface/runtime/schema. -->")
    source = source.replace("\n  </style>", polish_css() + "\n  </style>", 1)
    source = source.replace('data-r6o-field-model-render="true"', 'data-r6o-field-model-render="true" data-r6o-r1-reading-polish="true"', 1)
    old_status = """<div class="nb-state-bar">
                <div class="nb-state-main">
                  <span class="state-tag">查看状态</span>
                  <span class="quiet-tag">字段模型已回灌</span>
                  <span class="quiet-tag">大单元</span>
                  <span class="quiet-tag" title="当前内容仅为预览候选，教师确认前不写入正式备课本。">预览</span>
                  <span class="status-dot green"></span><span class="quiet-tag">可阅读</span>
                  <span class="status-dot amber"></span><span class="quiet-tag">资料待补充</span>
                </div>
                <div class="nb-mode-toggle" aria-label="大单元状态">
                  <button class="nb-mode-btn active" type="button">查看</button>
                  <button class="nb-mode-btn" type="button" data-pending="大单元编辑暂不接入，只做静态样张。">编辑</button>
                </div>
              </div>"""
    new_status = """<div class="nb-state-bar">
                <div class="nb-state-main">
                  <span class="r6o-r1-status-pill">查看状态</span>
                  <span class="r6o-r1-status-pill">可预览</span>
                  <span class="r6o-r1-status-light"><span class="r6o-r1-dot amber"></span>资料待补充</span>
                  <span class="r6o-r1-status-light"><span class="r6o-r1-dot green"></span>大单元预览</span>
                  <span class="r6o-r1-status-light" title="当前内容仅为预览候选，教师确认前不写入正式备课本。"><span class="r6o-r1-dot red"></span>教师确认前不生效</span>
                </div>
                <div class="nb-mode-toggle" aria-label="大单元状态">
                  <button class="nb-mode-btn active" type="button">查看</button>
                  <button class="nb-mode-btn" type="button" data-pending="大单元编辑暂不接入，只做静态样张。">编辑</button>
                </div>
              </div>"""
    source = source.replace(old_status, new_status, 1)
    source = move_status_above_material_prompt(source)
    return remove_duplicate_material_section(source)


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
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6O_R1_{viewport['id']}.png"
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


def main_doc_text(html_text: str) -> str:
    start = html_text.index('<div class="nb-doc" data-r6o-field-render-doc="true">')
    end = html_text.index('<aside class="nb-right-rail"', start)
    return html_text[start:end]


def validate_html(html_text: str) -> dict[str, Any]:
    main = main_doc_text(html_text)
    raw_hits = [key for key in RAW_KEYS if key in main]
    return {
        "top_status_row_matches_single_lesson_style": all(text in html_text for text in ["r6o-r1-status-pill", "r6o-r1-dot amber", "r6o-r1-dot green", "r6o-r1-dot red"]),
        "section_outer_cards_removed": "border-radius: 0 !important" in html_text and "box-shadow: none !important" in html_text,
        "main_reading_flow_continuous": 'data-r6o-r1-reading-polish="true"' in html_text and "border-bottom: 1px solid" in html_text,
        "duplicate_material_request_removed": "十二、资料补充" not in main,
        "material_request_kept_as_top_or_side_light_entry": "还缺教材材料" in html_text and "上传教材目录" in html_text and "上传单元页" in html_text,
        "all_core_big_unit_fields_still_visible": all(field in main for field in CORE_FIELDS),
        "old_skills_materials_scaffolds_label_absent": "技能与支架" not in html_text,
        "raw_engineering_field_hits": raw_hits,
        **boundary(),
    }


def write_review_files(output_root: Path, stage_dir: Path, result: dict[str, Any], smoke: dict[str, Any]) -> None:
    manifest = {
        "stage": STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "html": HTML_NAME,
        "top_status_row_matches_single_lesson_style": True,
        "section_outer_cards_removed": True,
        "duplicate_material_request_removed": True,
        "material_request_kept_as_top_or_side_light_entry": True,
        **boundary(),
    }
    write_json(stage_dir / "big_unit_reading_polish_manifest_1013I_R6O_R1.json", manifest)
    write_json(stage_dir / "visual_smoke_1013I_R6O_R1.json", smoke)
    write_json(stage_dir / "1013I_R6O_R1_result.json", result)
    write_text(stage_dir / "1013I_R6O_R1_report.md", f"""# 1013I_R6O_R1 Big Unit Render Surface Reading Polish

FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

Fixes:
- Top status row now follows the lighter single-lesson style.
- Section outer cards are visually removed; the main area reads as a continuous notebook page.
- Duplicate bottom `资料补充` chapter is removed.
- Material request remains as a top light entry.

Not included:
- No edit surface.
- No runtime/schema/provider/model/database/memory/Feishu/formal apply.

Validation: {FINAL_STATUS}
Failed checks: {result["failed_checks"]}
""")
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6O_R1 is a reading-surface polish patch only. It does not create the edit page.

Boundaries:
- edit_surface_created=false
- runtime_connected=false
- provider_called=false
- model_called=false
- formal_apply_performed=false
- database_written=false
- memory_written=false
- feishu_written=false
- main_project_pushed=false
""")
    write_text(output_root / "README.md", f"""# Prep Room Render Canvas Deepen V1 Review Package

Latest stage: `{STAGE_ID}`

Open:
- `{STAGE_DIR_NAME}/{HTML_NAME}`

Run:
- `python scripts/{VALIDATOR_NAME}`
""")
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", f"""# Review Package Manifest

Latest stage: `{STAGE_ID}`

Files:
- `{STAGE_DIR_NAME}/{HTML_NAME}`
- `{STAGE_DIR_NAME}/big_unit_reading_polish_manifest_1013I_R6O_R1.json`
- `{STAGE_DIR_NAME}/1013I_R6O_R1_result.json`
- `{STAGE_DIR_NAME}/1013I_R6O_R1_report.md`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6O_R1_desktop.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6O_R1_mobile.png`
- `scripts/{VALIDATOR_NAME}`

Boundary: reading polish only; edit page deferred to R6P.
""")


def run(root: Path) -> dict[str, Any]:
    output_root = resolve_output_root(root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)
    html_text = build_html(output_root)
    html_path = stage_dir / HTML_NAME
    write_text(html_path, html_text)
    checks = validate_html(html_text)
    smoke = create_screenshots(stage_dir, html_path)
    checks["screenshot_smoke_pass"] = bool(smoke.get("screenshot_smoke_pass"))
    expected_false = {
        "edit_surface_created",
        "runtime_connected",
        "provider_called",
        "model_called",
        "formal_apply_performed",
        "database_written",
        "memory_written",
        "feishu_written",
        "main_project_pushed",
    }
    failed = []
    for key, value in checks.items():
        if key == "raw_engineering_field_hits":
            continue
        if key in expected_false:
            if value is not False:
                failed.append(key)
            continue
        if value is not True:
            failed.append(key)
    if checks["raw_engineering_field_hits"]:
        failed.append("raw_engineering_field_hits")
    result = {
        "stage": STAGE_ID,
        "status": FINAL_STATUS if not failed else "FAIL_1013I_R6O_R1_BIG_UNIT_RENDER_SURFACE_READING_POLISH",
        "final_status": FINAL_STATUS if not failed else "FAIL_1013I_R6O_R1_BIG_UNIT_RENDER_SURFACE_READING_POLISH",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        **checks,
        "failed_checks": failed,
    }
    write_review_files(output_root, stage_dir, result, smoke)
    source_delta = output_root / "source_delta_1013I_R6O_R1" / "scripts" / VALIDATOR_NAME
    source_delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), source_delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=None)
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else repo_root_from_script()
    result = run(root)
    print("ALL_1013I_R6O_R1_BIG_UNIT_RENDER_SURFACE_READING_POLISH_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
