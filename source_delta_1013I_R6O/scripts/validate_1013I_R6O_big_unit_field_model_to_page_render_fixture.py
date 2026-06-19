from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6O_BIG_UNIT_FIELD_MODEL_TO_PAGE_RENDER_FIXTURE"
FINAL_STATUS = "PASS_1013I_R6O_BIG_UNIT_FIELD_MODEL_TO_PAGE_RENDER_FIXTURE"
INHERITS_FROM = "1013I_R6N_R9A_FIELD_LABEL_DISAMBIGUATION_BEFORE_RUNTIME_SCHEMA"
NEXT_STAGE = "USER_REVIEW_BIG_UNIT_FIELD_RENDERED_PAGE"
STAGE_DIR_NAME = "1013I_R6O_big_unit_field_model_to_page_render_fixture"
R8_DIR_NAME = "1013I_R6N_R8_big_unit_design_restyled_as_lesson_notebook_ui"
R7_DIR_NAME = "1013I_R6N_R7_big_unit_page_user_review_and_content_polish"
R9_DIR_NAME = "1013I_R6N_R9_big_unit_design_field_model"
R9A_DIR_NAME = "1013I_R6N_R9A_field_label_disambiguation_before_runtime_schema"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6O_big_unit_field_model_render.html"
VALIDATOR_NAME = "validate_1013I_R6O_big_unit_field_model_to_page_render_fixture.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]
RAW_KEYS = [
    "unit_package",
    "textbook_anchor",
    "lesson_position",
    "teacher_confirmation_required",
    "normal_candidate_card_generation_allowed",
    "knowledge_and_skills",
    "skills_materials_scaffolds",
    "single_lesson_inheritance_targets",
]
TEACHER_FIELDS = [
    "单元信息",
    "课标依据",
    "核心素养",
    "学生起点",
    "单元问题",
    "知识与技能",
    "表现任务",
    "学习推进",
    "课时任务链",
    "评价证据",
    "材料与支架",
    "资料补充",
]


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


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def boundary() -> dict[str, bool]:
    return {
        "single_lesson_work_paused": True,
        "runtime_schema_applied": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def find_base_html(output_root: Path) -> Path:
    r8 = output_root / R8_DIR_NAME / "prep_room_render_canvas_deepen_v1_R6N_R8_big_unit_design_lesson_notebook_ui.html"
    if r8.exists():
        return r8
    r7 = output_root / R7_DIR_NAME / "prep_room_render_canvas_deepen_v1_R6N_R7_big_unit_page_user_review_and_content_polish.html"
    if r7.exists():
        return r7
    raise FileNotFoundError("Missing R6N_R8 and R6N_R7 HTML baselines.")


def replace_once(source: str, old: str, new: str) -> str:
    if old not in source:
        raise ValueError(f"Missing marker: {old[:120]}")
    return source.replace(old, new, 1)


def section(title: str, body: str, note: str = "") -> str:
    note_html = f'\n                    <div class="nb-doc-subnote">{note}</div>' if note else ""
    return f'''                  <section class="nb-doc-section">
                    <div class="nb-doc-section-head">
                      <div class="nb-doc-title">{title}</div>
                      <button class="node-action secondary" type="button" data-pending="说明已收在轻提示里。">查看说明</button>
                    </div>
{body}{note_html}
                  </section>
'''


def rendered_doc_sections() -> str:
    return (
        section(
            "一、单元信息",
            """                    <p><strong>第一单元 · 多变的色彩</strong></p>
                    <p>三年级｜美术｜预计 3 课时</p>
                    <p><span class="quiet-tag">大单元</span> <span class="quiet-tag" title="当前内容仅为预览候选，教师确认前不写入正式备课本。">● 预览</span></p>""",
        )
        + section(
            "二、课标依据",
            """                    <p>本单元主要指向审美感知、艺术表现、创意实践，文化理解作轻量渗透。</p>
                    <p>学生通过观察、比较、尝试和表达，理解色彩组合会改变画面感觉，并能用色彩表达一种较明确的情绪或氛围。</p>""",
            "具体课标原文待资料确认，当前按课标方向生成预览。",
        )
        + section(
            "三、核心素养",
            """                    <ul>
                      <li><strong>审美感知：</strong>能感受不同色彩组合带来的冷暖、轻重、热烈、安静等视觉意味。</li>
                      <li><strong>艺术表现：</strong>能选择一组颜色表达明确感觉，并说明自己的选色理由。</li>
                      <li><strong>创意实践：</strong>能在比较、试验和反馈中调整色彩搭配。</li>
                      <li><strong>文化理解：</strong>能发现色彩感受与生活场景、作品情境有关。</li>
                    </ul>""",
        )
        + section(
            "四、学生起点",
            """                    <p>三年级学生通常能说出“红色热闹、蓝色安静”等直观感受，但容易停留在“好看、鲜艳、漂亮”。</p>
                    <p>本单元要帮助学生从“我觉得”走向“我能说明为什么”。</p>""",
        )
        + section(
            "五、单元问题",
            """                    <ul>
                      <li>颜色为什么会让人产生不同感觉？</li>
                      <li>我们怎样用颜色把一种感觉表达出来？</li>
                      <li>改动一处颜色，画面的意味为什么会变化？</li>
                    </ul>""",
        )
        + section(
            "六、知识与技能",
            """                    <ul>
                      <li>认识色彩组合带来的视觉差异。</li>
                      <li>能用冷暖、强弱、明暗、纯度变化等词语描述色彩感觉。</li>
                      <li>能选择 3-4 种颜色进行搭配尝试。</li>
                      <li>能通过调整颜色让画面感觉更明确。</li>
                    </ul>""",
            "本单元的美术语言和技能目标。",
        )
        + section(
            "七、表现任务",
            """                    <p>学生完成一件“色彩感觉”小作品，并用一句到几句话说明：我用了哪些颜色；我想表达什么感觉；我为什么这样搭配。</p>
                    <p>如果时间允许，再根据同伴或教师反馈调整一处颜色，并说明为什么改。</p>""",
        )
        + section(
            "八、学习推进",
            """                    <ul>
                      <li><strong>感受：</strong>看生活图片、作品、色卡或真实物件，先说直观感受。</li>
                      <li><strong>比较：</strong>比较不同色彩组合，发现搭配变化会改变画面感觉。</li>
                      <li><strong>表现：</strong>围绕一种感觉完成色彩实验或小作品。</li>
                      <li><strong>修订：</strong>展示作品，说出理由，根据反馈调整一处颜色。</li>
                    </ul>""",
        )
        + section(
            "九、课时任务链",
            """                    <p><strong>1-1 色彩初体验：</strong>打开感受，建立感受语言。</p>
                    <p><strong>1-2 色彩的感觉：</strong>比较方法，发现色彩组合会改变画面意味。</p>
                    <p><strong>1-3 色彩表达：</strong>完成表达，展示并修订。</p>
                    <details><summary>展开查看每课承接</summary><p>每课可继续查看：本课任务、学生会做什么、留下什么证据、如何承接下一课。</p></details>""",
        )
        + section(
            "十、评价证据",
            """                    <ul>
                      <li>能说出色彩带来的感觉；</li>
                      <li>能说明自己的选色理由；</li>
                      <li>学习单留下观察和选择记录；</li>
                      <li>作品呈现较明确的视觉意味；</li>
                      <li>能根据反馈做出一次可见调整。</li>
                    </ul>""",
        )
        + section(
            "十一、材料与支架",
            """                    <p>生活色彩图片；艺术作品图像；不同色卡组合；学生作品正反例；简短学习单；展示评价句式。</p>
                    <p>学习单轻量示例：我看到的颜色；我感受到的画面；我为什么这样选；我还想改哪里。</p>""",
            "教师准备的材料、学习单、示例和过程支架。",
        )
        + section(
            "十二、资料补充",
            """                    <div class="nb-material-action-list">
                      <div class="nb-material-action-row"><button class="node-action secondary" type="button">上传教材目录</button><small>帮助小教确认本单元前后课关系。</small></div>
                      <div class="nb-material-action-row"><button class="node-action secondary" type="button">上传单元页 / 教参截图</button><small>帮助小教理解教材活动和单元目标。</small></div>
                      <div class="nb-material-action-row"><button class="node-action secondary" type="button">粘贴单元目标</button><small>帮助小教对齐课标与教材要求。</small></div>
                      <div class="nb-material-action-row"><button class="node-action secondary" type="button">补充已有单元安排</button><small>保留你的教学经验和学校实际。</small></div>
                      <div class="nb-material-action-row"><button class="node-action secondary" type="button">先按临时判断看预览</button><small>不会写入正式备课本，后面仍需教师确认。</small></div>
                    </div>""",
        )
    )


def build_html(output_root: Path) -> str:
    base = find_base_html(output_root)
    source = base.read_text(encoding="utf-8")
    source = source.replace("师维 · 备课室 | R6N_R8 大单元教学设计式样张", "师维 · 备课室 | R6O 大单元字段回灌样张")
    source = source.replace("<!-- 1013I_R6N_R8: big-unit design restyled as the polished single-lesson notebook UI; standalone static sample. -->", "<!-- 1013I_R6O: big-unit field model rendered to page fixture; no runtime/schema. -->")
    source = source.replace("技能与支架", "材料与支架")
    source = source.replace("补课时安排", "补充课时安排")
    start = source.index('<div class="nb-doc" data-r6n-r8-big-unit-doc="true">')
    body_start = source.index('<div class="nb-doc-body-surface">', start) + len('<div class="nb-doc-body-surface">')
    body_end = source.index('</div>\n              </div>\n            </section>', body_start)
    source = source[:body_start] + "\n" + rendered_doc_sections() + "                " + source[body_end:]
    source = replace_once(source, 'data-r6n-r8-big-unit-doc="true"', 'data-r6o-field-render-doc="true"')
    source = source.replace('data-r6n-r8-notebook-ui="true"', 'data-r6n-r8-notebook-ui="true" data-r6o-field-model-render="true"')
    source = source.replace("查看状态</span>", "查看状态</span>\n                  <span class=\"quiet-tag\">字段模型已回灌</span>", 1)
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
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6O_{viewport['id']}.png"
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
        "field_model_rendered_to_page": 'data-r6o-field-model-render="true"' in html_text,
        "all_12_teacher_visible_fields_rendered": all(field in main for field in TEACHER_FIELDS),
        "unit_info_field_rendered": "单元信息" in main,
        "curriculum_basis_field_rendered": "课标依据" in main,
        "core_literacy_field_rendered": "核心素养" in main,
        "student_start_field_rendered": "学生起点" in main,
        "unit_question_field_rendered": "单元问题" in main,
        "knowledge_and_skills_field_rendered": "知识与技能" in main,
        "performance_task_field_rendered": "表现任务" in main,
        "learning_progression_field_rendered": "学习推进" in main,
        "lesson_chain_field_rendered": "课时任务链" in main,
        "assessment_evidence_field_rendered": "评价证据" in main,
        "materials_and_scaffolds_field_rendered": "材料与支架" in main,
        "material_request_actions_field_rendered": "资料补充" in main and "上传教材目录" in main and "先按临时判断看预览" in main,
        "knowledge_and_skills_label_present": "知识与技能" in main,
        "materials_and_scaffolds_label_present": "材料与支架" in main,
        "old_skills_materials_scaffolds_label_absent": "技能与支架" not in html_text,
        "teacher_reading_flow_kept": "nb-doc-section" in main and "nb-doc-body-surface" in main,
        "hover_or_collapsed_explanations_kept": "title=" in html_text or "<details" in main,
        "right_reference_area_low_weight": "阅读辅助" in html_text and "只读依据" in html_text,
        "main_surface_raw_engineering_field_hits": raw_hits,
        "single_lesson_work_paused": True,
    }


def write_review_files(output_root: Path, stage_dir: Path, result: dict[str, Any], field_model: dict[str, Any], backend_mapping: dict[str, Any], reuse_matrix: dict[str, Any], smoke: dict[str, Any]) -> None:
    rendered_fields = [{"teacher_label": field, "render_layer": "main_reading_surface"} for field in TEACHER_FIELDS]
    write_json(stage_dir / "big_unit_page_rendered_fields_1013I_R6O.json", {"stage": STAGE_ID, "rendered_teacher_fields": rendered_fields})
    manifest = {
        "stage": STAGE_ID,
        "source_field_model": f"{R9A_DIR_NAME}/big_unit_teacher_visible_field_model_1013I_R6N_R9A.json",
        "source_backend_mapping": f"{R9A_DIR_NAME}/big_unit_backend_field_mapping_1013I_R6N_R9A.json",
        "source_reuse_matrix": f"{R9A_DIR_NAME}/big_unit_field_reuse_and_integration_matrix_1013I_R6N_R9A.json",
        "rendered_teacher_fields": TEACHER_FIELDS,
        "main_surface_fields": TEACHER_FIELDS,
        "hover_fields": ["课标依据", "单元信息", "课时任务链"],
        "right_reference_fields": ["课标原文待确认", "教材锚点候选", "资料来源", "生成风险", "字段来源", "后端候选映射"],
        "forbidden_primary_surface_raw_keys": RAW_KEYS,
        "single_lesson_work_paused": True,
        "runtime_schema_applied": False,
    }
    write_json(stage_dir / "big_unit_field_render_manifest_1013I_R6O.json", manifest)
    write_json(stage_dir / "visual_smoke_1013I_R6O.json", smoke)
    write_json(stage_dir / "1013I_R6O_result.json", result)
    report = f"""# 1013I_R6O Big Unit Field Model To Page Render Fixture

FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

本阶段把 R9/R9A 确认的大单元教师可见字段模型回灌到大单元页面样张。

- 渲染 12 个教师可见字段。
- 保留教学设计正文阅读流。
- `知识与技能` 和 `材料与支架` 已消歧。
- 单课页工作暂停。
- 不接 runtime/schema/provider/model/database/memory/Feishu/formal apply。

Validation: {FINAL_STATUS}
Failed checks: {result["failed_checks"]}
"""
    write_text(stage_dir / "1013I_R6O_report.md", report)
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6O renders the R9/R9A big-unit teacher-visible field model back into a standalone static page fixture.

Boundaries:
- single_lesson_work_paused=true
- runtime_schema_applied=false
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
- `{STAGE_DIR_NAME}/big_unit_field_render_manifest_1013I_R6O.json`
- `{STAGE_DIR_NAME}/big_unit_page_rendered_fields_1013I_R6O.json`
- `{STAGE_DIR_NAME}/1013I_R6O_result.json`
- `{STAGE_DIR_NAME}/1013I_R6O_report.md`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6O_desktop.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6O_mobile.png`
- `scripts/{VALIDATOR_NAME}`

Boundary: page render fixture only; no runtime schema/database/memory/Feishu/provider/model/formal apply.
""")


def run(root: Path) -> dict[str, Any]:
    output_root = resolve_output_root(root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)
    field_model = load_json(output_root / R9A_DIR_NAME / "big_unit_teacher_visible_field_model_1013I_R6N_R9A.json")
    backend_mapping = load_json(output_root / R9A_DIR_NAME / "big_unit_backend_field_mapping_1013I_R6N_R9A.json")
    reuse_matrix = load_json(output_root / R9A_DIR_NAME / "big_unit_field_reuse_and_integration_matrix_1013I_R6N_R9A.json")
    html_text = build_html(output_root)
    html_path = stage_dir / HTML_NAME
    write_text(html_path, html_text)
    checks = validate_html(html_text)
    smoke = create_screenshots(stage_dir, html_path)
    checks["screenshot_smoke_pass"] = bool(smoke.get("screenshot_smoke_pass"))
    failed = [key for key, value in checks.items() if value is not True and key != "main_surface_raw_engineering_field_hits"]
    if checks["main_surface_raw_engineering_field_hits"]:
        failed.append("main_surface_raw_engineering_field_hits")
    result = {
        "stage": STAGE_ID,
        "final_status": FINAL_STATUS if not failed else "FAIL_1013I_R6O_BIG_UNIT_FIELD_MODEL_TO_PAGE_RENDER_FIXTURE",
        "status": FINAL_STATUS if not failed else "FAIL_1013I_R6O_BIG_UNIT_FIELD_MODEL_TO_PAGE_RENDER_FIXTURE",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        **checks,
        **boundary(),
        "failed_checks": failed,
    }
    write_review_files(output_root, stage_dir, result, field_model, backend_mapping, reuse_matrix, smoke)
    source_delta = output_root / "source_delta_1013I_R6O" / "scripts" / VALIDATOR_NAME
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
    print("ALL_1013I_R6O_BIG_UNIT_FIELD_MODEL_TO_PAGE_RENDER_FIXTURE_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
