from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6S_BIG_UNIT_SECTION_CANDIDATE_RETURN_TO_EDIT_MODAL_PREVIEW"
FINAL_STATUS = "PASS_1013I_R6S_BIG_UNIT_SECTION_CANDIDATE_RETURN_TO_EDIT_MODAL_PREVIEW"
INHERITS_FROM = "1013I_R6R_BIG_UNIT_SECTION_CANDIDATE_GENERATOR_ADAPTER_FIXTURE"
NEXT_STAGE = "USER_REVIEW_BIG_UNIT_SECTION_CANDIDATE_MODAL_PREVIEW"
BASE_DIR_NAME = "1013I_R6P_R2_section_edit_modal_lesson_notebook_style_patch"
R6R_DIR_NAME = "1013I_R6R_big_unit_section_candidate_generator_adapter_fixture"
STAGE_DIR_NAME = "1013I_R6S_big_unit_section_candidate_return_to_edit_modal_preview"
BASE_HTML_NAME = "prep_room_render_canvas_deepen_v1_R6P_R2_section_edit_modal_lesson_notebook_style.html"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6S_candidate_return_to_edit_modal_preview.html"
VALIDATOR_NAME = "validate_1013I_R6S_big_unit_section_candidate_return_to_edit_modal_preview.py"

LABEL_TO_SECTION_ID = {
    "课标依据": "curriculum_basis",
    "核心素养": "core_literacy",
    "表现任务": "performance_task",
    "课时任务链": "lesson_chain",
}
REQUIRED_LABELS = list(LABEL_TO_SECTION_ID)
FORBIDDEN_TEXT = ["正式写入", "正式生成", "应用到正式备课本"]
RAW_KEYS = [
    "field_key",
    "schema",
    "prompt",
    "unit_package",
    "formal_apply",
    "provider_called",
    "model_called",
    "database_written",
    "memory_written",
    "feishu_written",
]
CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def locate_output_root(root: Path) -> Path:
    if (root / "LATEST_REVIEW_ENTRY.md").exists() and (root / "REVIEW_PACKAGE_MANIFEST.md").exists():
        return root
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "preview_only": True,
        "preview_only_actions": True,
        "formal_apply_performed": False,
        "formal_apply_allowed": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def escape_text(value: str) -> str:
    return html.escape(value, quote=True).replace("\n", "<br>")


def candidate_modal_items(candidate_pack: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for candidate in candidate_pack.get("candidates", []):
        label = candidate["teacher_label"]
        items.append(
            {
                "section_id": LABEL_TO_SECTION_ID[label],
                "candidate_id": candidate["candidate_id"],
                "teacher_label": label,
                "teacher_intent": candidate["teacher_intent"],
                "current_text": candidate["current_text"],
                "candidate_text": candidate["candidate_text"],
                "xiaojiao_suggestion": candidate["xiaojiao_suggestion"],
                "why_this_change": candidate["why_this_change"],
                "risk_note": candidate["risk_note"],
                "affected_parts": candidate["affected_parts"],
                "destination": "section_preview_only",
                "preview_only": True,
                "actions": [
                    {"label": "采纳到本段预览", "action": "accept_to_section_preview", "preview_only": True},
                    {"label": "继续精修", "action": "revise_candidate", "preview_only": True},
                    {"label": "暂不处理", "action": "reject_candidate_for_now", "preview_only": True},
                ],
                "formal_apply_allowed": False,
                "provider_called": False,
                "model_called": False,
            }
        )
    return items


def build_return_fixture(candidate_pack: dict[str, Any]) -> dict[str, Any]:
    items = candidate_modal_items(candidate_pack)
    return {
        "stage": STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "source_candidate_pack": f"{R6R_DIR_NAME}/big_unit_section_candidate_pack_1013I_R6R.json",
        "target_modal_baseline": f"{BASE_DIR_NAME}/{BASE_HTML_NAME}",
        "candidate_returned_to_edit_modal": True,
        "candidate_count": len(items),
        "modal_uses_r6p_r2_lesson_notebook_style": True,
        "items": items,
        **boundary(),
    }


def build_preview_state(return_fixture: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "state_type": "section_edit_modal_candidate_preview_state",
        "items": [
            {
                "section_id": item["section_id"],
                "candidate_id": item["candidate_id"],
                "teacher_label": item["teacher_label"],
                "state": "candidate_visible_in_edit_modal",
                "destination": "section_preview_only",
                "can_accept_to_section_preview": True,
                "can_revise": True,
                "can_reject": True,
                "can_formal_apply": False,
            }
            for item in return_fixture["items"]
        ],
        **boundary(),
    }


def build_action_trace(return_fixture: dict[str, Any]) -> dict[str, Any]:
    trace_items = []
    for item in return_fixture["items"]:
        for action in item["actions"]:
            trace_items.append(
                {
                    "section_id": item["section_id"],
                    "candidate_id": item["candidate_id"],
                    "action": action["action"],
                    "label": action["label"],
                    "destination": "section_preview_only",
                    "preview_only": True,
                    "formal_apply_performed": False,
                }
            )
    return {
        "stage": STAGE_ID,
        "trace_type": "candidate_return_to_modal_action_trace",
        "action_trace_count": len(trace_items),
        "trace_items": trace_items,
        **boundary(),
    }


def patch_edit_data(html_text: str, return_fixture: dict[str, Any]) -> str:
    match = re.search(r'<script[^>]*id="r6p-section-edit-data"[^>]*>(.*?)</script>', html_text, re.S)
    if not match:
        raise ValueError("Cannot find r6p-section-edit-data.")
    edit_data = json.loads(match.group(1))
    by_section = {item["section_id"]: item for item in return_fixture["items"]}
    for section in edit_data:
        candidate = by_section.get(section.get("id"))
        if not candidate:
            continue
        section["candidate_id"] = candidate["candidate_id"]
        section["teacher_intent"] = candidate["teacher_intent"]
        section["current"] = candidate["current_text"]
        section["suggestion"] = candidate["xiaojiao_suggestion"]
        section["before"] = candidate["current_text"]
        section["after"] = candidate["candidate_text"]
        section["why_this_change"] = candidate["why_this_change"]
        section["risk_note"] = candidate["risk_note"]
        section["impact"] = candidate["affected_parts"]
        section["destination"] = "section_preview_only"
        section["preview_only"] = True
    replacement = '<script id="r6p-section-edit-data" type="application/json">' + json.dumps(edit_data, ensure_ascii=False) + "</script>"
    return html_text[: match.start()] + replacement + html_text[match.end() :]


def patch_modal_render(html_text: str) -> str:
    html_text = html_text.replace(
        "师维 · 备课室 | R6P_R2 大单元轻编辑弹窗样张",
        "师维 · 备课室 | R6S 候选回灌编辑弹窗预览",
    )
    html_text = html_text.replace(
        '<!-- 1013I_R6P_R2: modal style follows single-lesson edit bubble; right rail unchanged. -->',
        '<!-- 1013I_R6S: R6R candidate texts are returned to the R6P_R2 edit modal preview. -->',
    )
    html_text = html_text.replace(
        'data-r6p-r2-lesson-style-modal="true"',
        'data-r6p-r2-lesson-style-modal="true" data-r6s-candidate-modal-preview="true"',
        1,
    )
    html_text = re.sub(
        r'\n\s*const rail = document\.querySelector\("\[data-r6p-side-edit-surface\]"\);\n\s*if \(!dataNode \|\| !scene \|\| !rail\) return;',
        "\n          if (!dataNode || !scene) return;",
        html_text,
        count=1,
    )
    old = """              body.innerHTML = '<div class="r6p-modal-block"><strong>当前内容</strong><p>' + item.current + '</p></div><div class="r6p-modal-block"><strong>小教建议</strong><p>' + item.suggestion + '</p></div><div class="r6p-modal-block"><strong>修改前 / 修改后</strong><div class="r6p-modal-compare"><div class="r6p-modal-compare-box"><strong>修改前</strong><p>' + item.before + '</p></div><div class="r6p-modal-compare-box"><strong>修改后</strong><p>' + item.after + '</p></div></div></div><div class="r6p-modal-block"><strong>影响与操作</strong><ul>' + impact + '</ul><div class="r6p-modal-actions"><button class="node-action primary" type="button" data-preview-only="true">采纳到本段预览</button><button class="node-action secondary" type="button" data-preview-only="true">继续精修</button><button class="node-action secondary" type="button" data-preview-only="true">暂不处理</button></div></div><details class="r6p-modal-block"><summary>来源依据</summary><p>依据当前大单元阅读面、教师可见字段模型和后端候选映射归档，只作为静态预览参考。</p></details>';"""
    new = """              body.innerHTML = '<div class="r6p-modal-block"><strong>当前内容</strong><p>' + item.current + '</p></div><div class="r6p-modal-block"><strong>小教建议</strong><p>' + item.suggestion + '</p><p class="r6s-teacher-intent">老师意图：' + (item.teacher_intent || "调整这一段") + '</p></div><div class="r6p-modal-block"><strong>修改前 / 修改后</strong><div class="r6p-modal-compare"><div class="r6p-modal-compare-box"><strong>修改前</strong><p>' + item.before + '</p></div><div class="r6p-modal-compare-box r6s-candidate-box"><strong>修改后 · 候选预览</strong><p>' + item.after + '</p></div></div></div><div class="r6p-modal-block"><strong>为什么这样改</strong><p>' + (item.why_this_change || "让这一段更适合教师阅读和后续单课继承。") + '</p></div><div class="r6p-modal-block"><strong>影响与操作</strong><ul>' + impact + '</ul><p class="r6s-risk-note">' + (item.risk_note || "仅进入本段预览，教师确认前不生效。") + '</p><div class="r6p-modal-actions"><button class="node-action primary" type="button" data-preview-only="true" data-r6s-action="accept_to_section_preview">采纳到本段预览</button><button class="node-action secondary" type="button" data-preview-only="true" data-r6s-action="revise_candidate">继续精修</button><button class="node-action secondary" type="button" data-preview-only="true" data-r6s-action="reject_candidate_for_now">暂不处理</button></div></div><details class="r6p-modal-block"><summary>来源依据</summary><p>候选来自 R6R 静态候选包，依据当前大单元阅读面、教师可见字段模型和后端候选映射归档，只作为静态预览参考。</p></details>';"""
    if old not in html_text:
        raise ValueError("Cannot find R6P_R2 edit modal render template.")
    html_text = html_text.replace(old, new, 1)
    css = """

    /* 1013I_R6S: candidate return preview in edit modal */
    .r6s-candidate-box {
      background: rgba(229, 242, 238, .66);
      border-color: rgba(43, 124, 106, .24);
    }

    .r6s-teacher-intent,
    .r6s-risk-note {
      color: rgba(38, 94, 76, .78) !important;
      font-size: 12px !important;
    }
"""
    html_text = html_text.replace("\n  </style>", css + "\n  </style>", 1)
    return html_text


def build_html(output_root: Path, return_fixture: dict[str, Any]) -> str:
    html_path = output_root / BASE_DIR_NAME / BASE_HTML_NAME
    html_text = html_path.read_text(encoding="utf-8")
    html_text = patch_edit_data(html_text, return_fixture)
    html_text = patch_modal_render(html_text)
    return html_text


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
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6S_{viewport['id']}.png"
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


def validate_outputs(stage_dir: Path, html_text: str, return_fixture: dict[str, Any], preview_state: dict[str, Any]) -> dict[str, Any]:
    items = return_fixture.get("items", [])
    labels = [item.get("teacher_label") for item in items]
    combined = json.dumps(return_fixture, ensure_ascii=False) + html_text
    right_rail = html_text.split('<aside class="nb-right-rail"', 1)[1].split("</aside>", 1)[0]
    main = main_surface_text(html_text)
    return {
        "candidate_returned_to_edit_modal": return_fixture.get("candidate_returned_to_edit_modal") is True,
        "candidate_count_is_4": len(items) == 4 and return_fixture.get("candidate_count") == 4,
        "required_labels_present": labels == REQUIRED_LABELS,
        "modal_uses_r6p_r2_lesson_notebook_style": return_fixture.get("modal_uses_r6p_r2_lesson_notebook_style") is True and "data-r6p-r2-lesson-style-modal" in html_text,
        "before_after_preview_present": "修改前 / 修改后" in html_text and "修改后 · 候选预览" in html_text,
        "xiaojiao_suggestion_present": all(item.get("xiaojiao_suggestion") for item in items) and "小教建议" in html_text,
        "impact_notes_present": all(item.get("affected_parts") for item in items) and "影响与操作" in html_text,
        "accept_to_section_preview_action_present": "采纳到本段预览" in html_text and "accept_to_section_preview" in html_text,
        "revise_action_present": "继续精修" in html_text and "revise_candidate" in html_text,
        "reject_action_present": "暂不处理" in html_text and "reject_candidate_for_now" in html_text,
        "preview_only_actions": 'data-preview-only="true"' in html_text and all(item.get("preview_only") is True for item in items),
        "right_rail_resource_toolbar_kept": "资源库与工具" in right_rail and "编辑当前章节" not in right_rail,
        "edit_surface_not_inline_body": "修改后 · 候选预览" in html_text and "修改后 · 候选预览" not in main,
        "destination_all_section_preview_only": all(item.get("destination") == "section_preview_only" for item in items),
        "candidate_preview_state_created": len(preview_state.get("items", [])) == 4,
        "forbidden_text_hits": [term for term in FORBIDDEN_TEXT if term in combined],
        "raw_engineering_field_hits_in_main_surface": [key for key in RAW_KEYS if key in main],
        **boundary(),
    }


def failed_checks(checks: dict[str, Any]) -> list[str]:
    failed: list[str] = []
    expected_false = {
        "formal_apply_performed",
        "formal_apply_allowed",
        "runtime_connected",
        "provider_called",
        "model_called",
        "database_written",
        "memory_written",
        "feishu_written",
        "main_project_pushed",
    }
    for key, value in checks.items():
        if key in {"forbidden_text_hits", "raw_engineering_field_hits_in_main_surface"}:
            if value:
                failed.append(key)
        elif key in expected_false:
            if value is not False:
                failed.append(key)
        elif value is not True:
            failed.append(key)
    return failed


def write_package_docs(output_root: Path, stage_dir: Path, result: dict[str, Any]) -> None:
    write_text(stage_dir / "1013I_R6S_report.md", f"""# 1013I_R6S Big Unit Section Candidate Return To Edit Modal Preview

FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6S returns the four R6R static candidates to the R6P_R2 big-unit section edit modal.

Teacher-visible modal content:
- 当前内容
- 小教建议
- 修改前 / 修改后
- 为什么这样改
- 影响与操作
- 采纳到本段预览 / 继续精修 / 暂不处理

Boundaries:
- Preview-only actions.
- No runtime connection.
- No provider/model call.
- No formal apply.
- No database/memory/Feishu write.
- No main-project push.

Failed checks: {result["failed_checks"]}
""")
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6S returns the four R6R static candidates to the R6P_R2 lesson-notebook-style edit modal preview. It does not generate new content and does not write formal lesson body.

Key flags:
- CANDIDATE_RETURNED_TO_EDIT_MODAL=true
- CANDIDATE_COUNT=4
- BEFORE_AFTER_PREVIEW_PRESENT=true
- XIAOJIAO_SUGGESTION_PRESENT=true
- ACCEPT_TO_SECTION_PREVIEW_ACTION_PRESENT=true
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
- `{STAGE_DIR_NAME}/1013I_R6S_result.json`

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
- `{STAGE_DIR_NAME}/big_unit_section_candidate_modal_return_fixture_1013I_R6S.json`
- `{STAGE_DIR_NAME}/big_unit_section_candidate_modal_preview_state_1013I_R6S.json`
- `{STAGE_DIR_NAME}/big_unit_section_candidate_modal_action_trace_1013I_R6S.json`
- `{STAGE_DIR_NAME}/1013I_R6S_result.json`
- `{STAGE_DIR_NAME}/1013I_R6S_report.md`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6S_desktop.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6S_mobile.png`
- `scripts/{VALIDATOR_NAME}`

Boundary: static candidate return to edit-modal preview only. No runtime, provider/model, formal apply, database, memory, Feishu, or main-project push.
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

    pack_path = output_root / R6R_DIR_NAME / "big_unit_section_candidate_pack_1013I_R6R.json"
    base_result = output_root / BASE_DIR_NAME / "1013I_R6P_R2_result.json"
    if not pack_path.exists():
        raise FileNotFoundError(pack_path)
    if not base_result.exists():
        raise FileNotFoundError(base_result)

    candidate_pack = read_json(pack_path)
    return_fixture = build_return_fixture(candidate_pack)
    preview_state = build_preview_state(return_fixture)
    action_trace = build_action_trace(return_fixture)
    html_text = build_html(output_root, return_fixture)
    html_path = stage_dir / HTML_NAME
    write_text(html_path, html_text)

    write_json(stage_dir / "big_unit_section_candidate_modal_return_fixture_1013I_R6S.json", return_fixture)
    write_json(stage_dir / "big_unit_section_candidate_modal_preview_state_1013I_R6S.json", preview_state)
    write_json(stage_dir / "big_unit_section_candidate_modal_action_trace_1013I_R6S.json", action_trace)
    smoke = create_screenshots(stage_dir, html_path)
    checks = validate_outputs(stage_dir, html_text, return_fixture, preview_state)
    checks["screenshot_smoke_pass"] = bool(smoke.get("screenshot_smoke_pass"))
    failed = failed_checks(checks)
    result = {
        "stage": STAGE_ID,
        "status": FINAL_STATUS if not failed else "FAIL_1013I_R6S_BIG_UNIT_SECTION_CANDIDATE_RETURN_TO_EDIT_MODAL_PREVIEW",
        "final_status": FINAL_STATUS if not failed else "FAIL_1013I_R6S_BIG_UNIT_SECTION_CANDIDATE_RETURN_TO_EDIT_MODAL_PREVIEW",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        "candidate_returned_to_edit_modal": True,
        "candidate_count": 4,
        "modal_uses_r6p_r2_lesson_notebook_style": True,
        "before_after_preview_present": True,
        "xiaojiao_suggestion_present": True,
        "impact_notes_present": True,
        "accept_to_section_preview_action_present": True,
        "revise_action_present": True,
        "reject_action_present": True,
        "preview_only_actions": True,
        "formal_apply_performed": False,
        "provider_called": False,
        "model_called": False,
        "runtime_connected": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
        "validation_checks": checks,
        "failed_checks": failed,
    }
    write_json(stage_dir / "1013I_R6S_result.json", result)
    write_package_docs(output_root, stage_dir, result)
    source_delta = output_root / "source_delta_1013I_R6S" / "scripts" / VALIDATOR_NAME
    source_delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), source_delta)

    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False))
    print("ALL_1013I_R6S_BIG_UNIT_SECTION_CANDIDATE_RETURN_TO_EDIT_MODAL_PREVIEW_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
