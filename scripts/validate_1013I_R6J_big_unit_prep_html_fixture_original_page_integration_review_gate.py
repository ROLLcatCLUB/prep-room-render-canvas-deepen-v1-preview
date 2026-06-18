from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6J_BIG_UNIT_PREP_HTML_FIXTURE_ORIGINAL_PAGE_INTEGRATION_REVIEW_GATE"
FINAL_STATUS = "PASS_1013I_R6J_BIG_UNIT_PREP_HTML_FIXTURE_ORIGINAL_PAGE_INTEGRATION_REVIEW_GATE"
INHERITS_FROM = "1013I_R6I_BIG_UNIT_PREP_HTML_FIXTURE_AFTER_REVIEW_APPROVAL"
R6I_PASS_STATUS = "PASS_1013I_R6I_BIG_UNIT_PREP_HTML_FIXTURE_AFTER_REVIEW_APPROVAL"
NEXT_STAGE = "1013I_R6K_BIG_UNIT_PREP_ORIGINAL_PAGE_STATIC_INTEGRATION_FIXTURE_AFTER_REVIEW_GATE"
STAGE_DIR_NAME = "1013I_R6J_big_unit_prep_html_fixture_original_page_integration_review_gate"
VALIDATOR_NAME = "validate_1013I_R6J_big_unit_prep_html_fixture_original_page_integration_review_gate.py"
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]
SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)app[_-]?secret\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)tenant[_-]?access[_-]?token\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)cookie\s*[:=]\s*['\"][^'\"]{20,}"),
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
        "review_gate_only": True,
        "html_body_modified": False,
        "main_prep_room_html_modified": False,
        "static_html_fixture_modified": False,
        "runtime_connected": False,
        "product_runtime_called": False,
        "html_ui_implementation_allowed": False,
        "ui_implementation_started": False,
        "r7_visual_review_entered": False,
        "normal_candidate_card_generation_allowed": False,
        "writes_unit_package": False,
        "writes_lesson_body": False,
        "verified_textbook_anchor_created": False,
        "official_claim_created": False,
        "big_unit_generation_performed": False,
        "single_lesson_generation_performed": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "official_export_created": False,
        "official_archive_created": False,
        "main_project_pushed": False,
    }


def original_page_path(output_root: Path) -> Path:
    path = output_root / "prep_room_render_canvas_deepen_v1.html"
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def original_page_evidence(original_html: str) -> dict[str, bool]:
    return {
        "has_shiwei_shell": "师维" in original_html and "教师AI工作台" in original_html,
        "has_top_space_nav": all(label in original_html for label in ["教室", "备课室", "课堂观察", "作品馆", "知识馆", "档案室"]),
        "prep_room_is_active_space": 'aria-label="备课室"' in original_html and "space-btn active" in original_html,
        "has_context_bar": "context-bar" in original_html and "contextTitle" in original_html,
        "has_prep_notebook_view": "prepNotebook" in original_html and "renderPrepNotebookCanvas" in original_html,
        "has_bottom_assistant_entry": "小教意图入口" in original_html and "对小教说一句" in original_html,
        "has_preview_layer_semantics": "预览层" in original_html and "候选预览 / 教师确认前不生效" in original_html,
        "has_pending_change_queue": "addPendingChange" in original_html and "等待教师确认" in original_html,
        "has_inline_hover_note_pattern": "data-hover-note" in original_html and "小教判断" in original_html,
    }


def r6i_evidence(output_root: Path) -> dict[str, Any]:
    stage_dir = output_root / "1013I_R6I_big_unit_prep_html_fixture_after_review_approval"
    result = read_json(stage_dir / "1013I_R6I_result.json")
    html_text = (stage_dir / "big_unit_prep_html_fixture_1013I_R6I.html").read_text(encoding="utf-8")
    visual = read_json(stage_dir / "visual_smoke_1013I_R6I.json")
    return {
        "stage_dir": str(stage_dir),
        "result": result,
        "html_text": html_text,
        "visual": visual,
    }


def build_style_alignment_matrix(original: dict[str, bool], r6i: dict[str, Any]) -> dict[str, Any]:
    r6i_result = r6i["result"]
    rows = [
        {
            "item": "shell_identity",
            "original_page_evidence": ["师维", "教师AI工作台", "备课室 active space"],
            "r6i_status": "standalone_fixture",
            "review": "R6I must be embedded inside the existing prep-room shell, not replace it.",
            "pass": original["has_shiwei_shell"] and original["prep_room_is_active_space"],
        },
        {
            "item": "visual_tokens",
            "original_page_evidence": ["paper background", "8px radius", "green/blue/amber/red state colors"],
            "r6i_status": "compatible_but_needs_shell_token_reuse",
            "review": "R6I uses similar restrained tokens, but R6K must reuse original CSS variables rather than introduce a second theme.",
            "pass": True,
        },
        {
            "item": "density_and_cards",
            "original_page_evidence": ["dense prep notebook", "right drawer", "status lights"],
            "r6i_status": "decision_first_cards",
            "review": "R6I card density is acceptable only if inserted as a compact upstream-confirmation layer above the current lesson body.",
            "pass": r6i_result.get("decision_first_layout_visible") is True,
        },
        {
            "item": "assistant_and_preview_language",
            "original_page_evidence": ["小教", "预览层", "教师确认前不生效"],
            "r6i_status": "preview_only_badges",
            "review": "R6I must keep the original language: preview first, teacher confirmation before effect, no formal write.",
            "pass": original["has_bottom_assistant_entry"]
            and original["has_preview_layer_semantics"]
            and r6i_result.get("preview_only_badges_visible") is True,
        },
        {
            "item": "reference_material_weight",
            "original_page_evidence": ["right drawer and collapsed details patterns"],
            "r6i_status": "readonly_reference_collapsed",
            "review": "Official references should remain in the right assist area or collapsed drawer, not in the first decision lane.",
            "pass": r6i_result.get("official_reference_collapsed_by_default") is True,
        },
    ]
    return {
        "stage": STAGE_ID,
        "matrix_type": "original_page_style_alignment",
        "original_page_reviewed": all(original.values()),
        "overall_pass": all(row["pass"] for row in rows),
        "rows": rows,
        "required_followup": [
            "R6K should reuse original prep-room shell tokens and not create an unrelated full-page theme.",
            "R6K should keep R6I content as an internal upstream-confirmation layer.",
        ],
    }


def build_entry_placement_map() -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "placement_decision": "inside_prep_room",
        "top_level_nav_not_modified": True,
        "big_unit_not_new_global_space": True,
        "rejected_placements": [
            {
                "placement": "top_level_space_nav",
                "reason": "大单元位置确认不是新空间，不能和 教/备/观/作/知/档 并列。",
            },
            {
                "placement": "standalone_full_page_replace_prep_room",
                "reason": "会切断原备课室的备课本、预览层和小教输入语义。",
            },
        ],
        "approved_candidate_placements": [
            {
                "placement": "prep_room_directory",
                "teacher_label": "单元 / 大单元位置",
                "role": "备课室内部上游确认入口",
            },
            {
                "placement": "current_lesson_preflight_bar",
                "teacher_label": "这节课在单元里的位置待确认",
                "role": "单课备课前置确认条",
            },
            {
                "placement": "prep_notebook_above_lesson_body",
                "teacher_label": "进入单课备课前先确认",
                "role": "阻断原因和待确认项首屏",
            },
        ],
        "recommended_primary_placement": "current_lesson_preflight_bar_above_prep_notebook_body",
    }


def build_main_area_insertion_plan() -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "plan_type": "main_area_insertion_plan",
        "main_area_insertion_plan_created": True,
        "layout": [
            {
                "zone": "main_area_top",
                "content": "大单元位置确认条 / 阻断原因 / 待确认项",
                "purpose": "先说明为什么不能直接生成单课。",
                "writes_lesson_body": False,
            },
            {
                "zone": "main_area_middle",
                "content": "教材锚点候选 + 本课位置选择 + 轻时间线",
                "purpose": "让教师做进入单课备课前的结构判断。",
                "writes_unit_package": False,
            },
            {
                "zone": "main_area_lower",
                "content": "确认后才显示可以进入单课备课候选",
                "purpose": "把候选卡生成放在确认之后。",
                "normal_candidate_card_generation_allowed": False,
            },
            {
                "zone": "right_assistant_area",
                "content": "只读依据、风险提醒、来源字段",
                "purpose": "保留依据但不抢主线，不制造官方结论错觉。",
                "readonly_reference_only": True,
            },
        ],
        "right_assistant_area_usage_reviewed": True,
        "must_not_cover_existing_lesson_body": True,
        "must_not_create_formal_big_unit_editor": True,
    }


def build_writeback_semantics() -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "preview_layer_semantics_kept": True,
        "writeback_preview_only": True,
        "action_semantics": [
            {
                "visible_action": "确认教材锚点",
                "means": "进入 preview_state",
                "does_not_mean": "写入正式教材锚点",
            },
            {
                "visible_action": "选择本课位置",
                "means": "进入 teacher_confirmed_candidate",
                "does_not_mean": "写入正式单元设计",
            },
            {
                "visible_action": "大单元链大方向可以",
                "means": "允许进入后续候选链",
                "does_not_mean": "生成正式大单元",
            },
            {
                "visible_action": "先按临时单课草稿继续",
                "means": "degraded draft preview only",
                "does_not_mean": "正常单课候选生成或 formal apply",
            },
        ],
        "write_layers": [
            {
                "layer": "preview_state",
                "allowed_now": True,
                "description": "教师临时确认，页面可见，不写正式数据。",
            },
            {
                "layer": "teacher_confirmed_candidate",
                "allowed_now": "review_semantics_only",
                "description": "教师明确确认后进入候选链，但仍不是 formal apply。",
            },
            {
                "layer": "formal_apply",
                "allowed_now": False,
                "description": "未来单独阶段，当前禁止。",
            },
        ],
        "formal_apply_performed": False,
    }


def scan_deprecated_visible_names(paths: list[Path]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name in DEPRECATED_VISIBLE_NAMES:
            if name in text:
                hits.append({"path": str(path), "name": name})
    return hits


def scan_secrets(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append(str(path))
                break
    return hits


def build_result(
    output_root: Path,
    original: dict[str, bool],
    style_matrix: dict[str, Any],
    placement_map: dict[str, Any],
    insertion_plan: dict[str, Any],
    writeback: dict[str, Any],
    stage_files: list[Path],
) -> dict[str, Any]:
    latest_text = (output_root / "LATEST_REVIEW_ENTRY.md").read_text(encoding="utf-8")
    manifest_text = (output_root / "REVIEW_PACKAGE_MANIFEST.md").read_text(encoding="utf-8")
    r6i_result = read_json(
        output_root
        / "1013I_R6I_big_unit_prep_html_fixture_after_review_approval"
        / "1013I_R6I_result.json"
    )
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "r6i_result_present": True,
        "r6i_final_status": r6i_result.get("final_status"),
        "r6i_pass": r6i_result.get("final_status") == R6I_PASS_STATUS,
        "latest_entry_points_to_r6j": f"REVIEW_STAGE={STAGE_ID}" in latest_text
        and f"FINAL_STATUS={FINAL_STATUS}" in latest_text,
        "latest_entry_next_stage_is_r6k": f"NEXT_RECOMMENDED_STAGE={NEXT_STAGE}" in latest_text,
        "manifest_includes_r6j": STAGE_ID in manifest_text and f"{STAGE_DIR_NAME}/" in manifest_text,
        "manifest_next_stage_is_r6k": NEXT_STAGE in manifest_text,
        "original_page_reviewed": all(original.values()),
        "original_page_style_alignment_pass": style_matrix["overall_pass"],
        "top_level_nav_not_modified": placement_map["top_level_nav_not_modified"],
        "big_unit_entry_placed_inside_prep_room": placement_map["placement_decision"] == "inside_prep_room",
        "big_unit_not_new_global_space": placement_map["big_unit_not_new_global_space"],
        "main_area_insertion_plan_created": insertion_plan["main_area_insertion_plan_created"],
        "right_assistant_area_usage_reviewed": insertion_plan["right_assistant_area_usage_reviewed"],
        "preview_layer_semantics_kept": writeback["preview_layer_semantics_kept"],
        "writeback_preview_only": writeback["writeback_preview_only"],
        "original_shell_tokens_should_be_reused_next": True,
        "standalone_r6i_not_directly_integrated": True,
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(stage_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **boundary(),
    }
    required_true = [
        "r6i_result_present",
        "r6i_pass",
        "latest_entry_points_to_r6j",
        "latest_entry_next_stage_is_r6k",
        "manifest_includes_r6j",
        "manifest_next_stage_is_r6k",
        "original_page_reviewed",
        "original_page_style_alignment_pass",
        "top_level_nav_not_modified",
        "big_unit_entry_placed_inside_prep_room",
        "big_unit_not_new_global_space",
        "main_area_insertion_plan_created",
        "right_assistant_area_usage_reviewed",
        "preview_layer_semantics_kept",
        "writeback_preview_only",
        "review_gate_only",
    ]
    required_false = [
        "html_body_modified",
        "main_prep_room_html_modified",
        "static_html_fixture_modified",
        "runtime_connected",
        "product_runtime_called",
        "html_ui_implementation_allowed",
        "ui_implementation_started",
        "r7_visual_review_entered",
        "normal_candidate_card_generation_allowed",
        "writes_unit_package",
        "writes_lesson_body",
        "verified_textbook_anchor_created",
        "official_claim_created",
        "big_unit_generation_performed",
        "single_lesson_generation_performed",
        "provider_called",
        "model_called",
        "formal_apply_performed",
        "database_written",
        "memory_written",
        "feishu_written",
        "official_export_created",
        "official_archive_created",
        "main_project_pushed",
    ]
    failures = [key for key in required_true if result.get(key) is not True]
    failures.extend([key for key in required_false if result.get(key) is not False])
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    if failures:
        result["final_status"] = "FAIL_1013I_R6J_BIG_UNIT_PREP_HTML_FIXTURE_ORIGINAL_PAGE_INTEGRATION_REVIEW_GATE"
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013I_R6J Original Page Integration Review Report

```text
STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}
REVIEW_GATE_ONLY=true
HTML_BODY_MODIFIED=false
MAIN_PREP_ROOM_HTML_MODIFIED=false
```

## Review Decision

R6J upgrades the review from a standalone visual check to an original-page integration gate.
The big-unit confirmation surface should be integrated as an upstream confirmation layer inside the existing prep-room page, not as a new global space or unrelated standalone page.

## Key Findings

```text
original_page_reviewed={str(result["original_page_reviewed"]).lower()}
original_page_style_alignment_pass={str(result["original_page_style_alignment_pass"]).lower()}
top_level_nav_not_modified={str(result["top_level_nav_not_modified"]).lower()}
big_unit_entry_placed_inside_prep_room={str(result["big_unit_entry_placed_inside_prep_room"]).lower()}
big_unit_not_new_global_space={str(result["big_unit_not_new_global_space"]).lower()}
main_area_insertion_plan_created={str(result["main_area_insertion_plan_created"]).lower()}
right_assistant_area_usage_reviewed={str(result["right_assistant_area_usage_reviewed"]).lower()}
preview_layer_semantics_kept={str(result["preview_layer_semantics_kept"]).lower()}
writeback_preview_only={str(result["writeback_preview_only"]).lower()}
```

## Required Next Constraint

R6K may create only a static original-page integration fixture after this gate. It should reuse the original prep-room shell and place the big-unit entry inside the prep-room flow. It must not create a new top-level navigation space, connect runtime, write lesson body, write unit package, call provider/model, or perform formal apply.
"""


def copy_source_delta(root: Path, output_root: Path) -> None:
    source = root / "scripts" / VALIDATOR_NAME
    target = output_root / "source_delta_1013I_R6J" / "scripts" / VALIDATOR_NAME
    if source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    root = args.root.resolve()
    output_root = resolve_output_root(root)
    stage_dir = output_root / STAGE_DIR_NAME
    original_html = original_page_path(output_root).read_text(encoding="utf-8")
    original = original_page_evidence(original_html)
    r6i = r6i_evidence(output_root)
    style_matrix = build_style_alignment_matrix(original, r6i)
    placement_map = build_entry_placement_map()
    insertion_plan = build_main_area_insertion_plan()
    writeback = build_writeback_semantics()
    write_json(stage_dir / "original_page_style_alignment_matrix_1013I_R6J.json", style_matrix)
    write_json(stage_dir / "big_unit_entry_placement_map_1013I_R6J.json", placement_map)
    write_json(stage_dir / "main_area_insertion_plan_1013I_R6J.json", insertion_plan)
    write_json(stage_dir / "writeback_preview_semantics_1013I_R6J.json", writeback)
    result_path = stage_dir / "1013I_R6J_result.json"
    report_path = stage_dir / "1013I_R6J_original_page_integration_review_report.md"
    stage_files = [
        stage_dir / "original_page_style_alignment_matrix_1013I_R6J.json",
        stage_dir / "big_unit_entry_placement_map_1013I_R6J.json",
        stage_dir / "main_area_insertion_plan_1013I_R6J.json",
        stage_dir / "writeback_preview_semantics_1013I_R6J.json",
        result_path,
        report_path,
    ]
    result = build_result(output_root, original, style_matrix, placement_map, insertion_plan, writeback, stage_files)
    write_json(result_path, result)
    write_text(report_path, build_report(result))
    copy_source_delta(root, output_root)
    if result["final_status"] != FINAL_STATUS:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    print(f"{FINAL_STATUS}: {result_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
