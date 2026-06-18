from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6E_OFFICIAL_UNIT_MATERIAL_READONLY_EXTRACTION_FIXTURE"
FINAL_STATUS = "PASS_1013I_R6E_OFFICIAL_UNIT_MATERIAL_READONLY_EXTRACTION_FIXTURE"
INHERITS_FROM = "1013I_R6D_TEXTBOOK_ANCHOR_AND_BIG_UNIT_DESIGN_CHAIN_CONTRACT"
R6D_PASS_STATUS = "PASS_1013I_R6D_TEXTBOOK_ANCHOR_AND_BIG_UNIT_DESIGN_CHAIN_CONTRACT"
NEXT_STAGE = "1013I_R6F_BIG_UNIT_PREP_PAGE_FIXTURE_USER_REVIEW_GATE"
STAGE_DIR_NAME = "1013I_R6E_official_unit_material_readonly_extraction_fixture"
VALIDATOR_NAME = "validate_1013I_R6E_official_unit_material_readonly_extraction_fixture.py"
BACKEND_ADAPTER_RELATIVE_PATH = (
    "backend/xiaobei_ai/prep_room_official_unit_material_extraction_1013I_R6E.py"
)
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


def load_backend_adapter(root: Path):
    sys.path.insert(0, str(root))
    from backend.xiaobei_ai.prep_room_official_unit_material_extraction_1013I_R6E import (  # noqa: PLC0415
        build_official_unit_material_readonly_extraction,
    )

    return build_official_unit_material_readonly_extraction


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


def write_stage_files(root: Path, output_root: Path) -> dict[str, Any]:
    builder = load_backend_adapter(root)
    payload = builder(root)
    stage_dir = output_root / STAGE_DIR_NAME
    write_json(stage_dir / "official_unit_material_source_index_1013I_R6E.json", payload["source_index"])
    write_json(
        stage_dir / "official_unit_material_extraction_fixture_1013I_R6E.json",
        payload["extraction_fixture"],
    )
    write_json(
        stage_dir / "textbook_anchor_candidates_1013I_R6E.json",
        payload["textbook_anchor_candidates"],
    )
    write_json(stage_dir / "big_unit_chain_candidates_1013I_R6E.json", payload["big_unit_chain_candidates"])
    write_json(
        stage_dir / "teacher_confirmation_required_items_1013I_R6E.json",
        payload["teacher_confirmation_required_items"],
    )
    return payload


def build_result(root: Path, output_root: Path, payload: dict[str, Any], stage_files: list[Path]) -> dict[str, Any]:
    stage_dir = output_root / STAGE_DIR_NAME
    r6d_path = output_root / "1013I_R6D_textbook_anchor_and_big_unit_design_chain_contract" / "1013I_R6D_result.json"
    latest_path = output_root / "LATEST_REVIEW_ENTRY.md"
    manifest_path = output_root / "REVIEW_PACKAGE_MANIFEST.md"
    r6d = read_json(r6d_path)
    latest_text = latest_path.read_text(encoding="utf-8")
    manifest_text = manifest_path.read_text(encoding="utf-8")
    fixture = payload["extraction_fixture"]
    textbook_candidates = payload["textbook_anchor_candidates"]
    big_unit_candidates = payload["big_unit_chain_candidates"]
    confirmation_items = payload["teacher_confirmation_required_items"]

    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "r6d_result_present": r6d_path.exists(),
        "r6d_final_status": r6d.get("final_status"),
        "r6d_pass": r6d.get("final_status") == R6D_PASS_STATUS,
        "latest_entry_points_to_r6e": f"REVIEW_STAGE={STAGE_ID}" in latest_text
        and f"FINAL_STATUS={FINAL_STATUS}" in latest_text,
        "latest_entry_next_stage_is_r6f_gate": f"NEXT_RECOMMENDED_STAGE={NEXT_STAGE}" in latest_text,
        "manifest_includes_r6e": STAGE_ID in manifest_text and f"{STAGE_DIR_NAME}/" in manifest_text,
        "manifest_next_stage_is_r6f_gate": NEXT_STAGE in manifest_text,
        "backend_adapter_created": (root / BACKEND_ADAPTER_RELATIVE_PATH).exists(),
        "source_index_created": (stage_dir / "official_unit_material_source_index_1013I_R6E.json").exists(),
        "extraction_fixture_created": (
            stage_dir / "official_unit_material_extraction_fixture_1013I_R6E.json"
        ).exists(),
        "textbook_anchor_candidates_created": (
            stage_dir / "textbook_anchor_candidates_1013I_R6E.json"
        ).exists()
        and fixture.get("textbook_anchor_candidates_created") is True,
        "big_unit_chain_candidates_created": (
            stage_dir / "big_unit_chain_candidates_1013I_R6E.json"
        ).exists()
        and fixture.get("big_unit_chain_candidates_created") is True,
        "teacher_confirmation_required_items_created": (
            stage_dir / "teacher_confirmation_required_items_1013I_R6E.json"
        ).exists()
        and fixture.get("teacher_confirmation_required_items_created") is True,
        "source_contracts_loaded": fixture.get("source_contracts_loaded") is True,
        "source_contract_count": fixture.get("source_contract_count"),
        "official_dictionary_field_count": fixture.get("official_dictionary_field_count"),
        "question_flow_stage_count": fixture.get("question_flow_stage_count"),
        "textbook_anchor_candidate_count": len(textbook_candidates.get("candidates", [])),
        "big_unit_chain_stage_count": fixture.get("big_unit_chain_stage_count"),
        "lesson_position_candidate_created": fixture.get("lesson_position_candidate_created") is True,
        "teacher_confirmation_required_item_count": len(confirmation_items.get("items", [])),
        "normal_candidate_card_generation_allowed": fixture.get("normal_candidate_card_generation_allowed"),
        "teacher_confirmation_required": confirmation_items.get("teacher_confirmation_required") is True,
        "verified_textbook_anchor_created": textbook_candidates.get("verified_textbook_anchor_created"),
        "unit_package_created": big_unit_candidates.get("unit_package_created"),
        "big_unit_body_generated": big_unit_candidates.get("big_unit_body_generated"),
        "page_work_started": fixture.get("page_work_started"),
        "page_user_gate_required_before_r6f": fixture.get("page_user_gate_required_before_r6f") is True,
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(stage_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **payload["boundary"],
    }
    required_true = [
        "r6d_result_present",
        "r6d_pass",
        "latest_entry_points_to_r6e",
        "latest_entry_next_stage_is_r6f_gate",
        "manifest_includes_r6e",
        "manifest_next_stage_is_r6f_gate",
        "backend_adapter_created",
        "source_index_created",
        "extraction_fixture_created",
        "textbook_anchor_candidates_created",
        "big_unit_chain_candidates_created",
        "teacher_confirmation_required_items_created",
        "source_contracts_loaded",
        "lesson_position_candidate_created",
        "teacher_confirmation_required",
        "page_user_gate_required_before_r6f",
        "backend_adapter_only",
        "readonly_extraction_only",
        "fixture_only",
        "preview_only",
    ]
    required_false = [
        "normal_candidate_card_generation_allowed",
        "verified_textbook_anchor_created",
        "unit_package_created",
        "big_unit_body_generated",
        "page_work_started",
        "actual_textbook_parsing_performed",
        "actual_big_unit_material_parsing_performed",
        "official_claim_created",
        "big_unit_generation_performed",
        "single_lesson_generation_performed",
        "r7_visual_review_entered",
        "product_runtime_called",
        "provider_called",
        "model_called",
        "formal_apply_performed",
        "lesson_body_modified",
        "html_body_modified",
        "database_written",
        "memory_written",
        "feishu_written",
        "official_export_created",
        "official_archive_created",
        "main_project_pushed",
    ]
    failures = [key for key in required_true if result.get(key) is not True]
    failures.extend([key for key in required_false if result.get(key) is not False])
    numeric_minimums = {
        "source_contract_count": 4,
        "official_dictionary_field_count": 20,
        "question_flow_stage_count": 4,
        "textbook_anchor_candidate_count": 1,
        "big_unit_chain_stage_count": 4,
        "teacher_confirmation_required_item_count": 5,
    }
    for key, minimum in numeric_minimums.items():
        if not isinstance(result.get(key), int) or result[key] < minimum:
            failures.append(key)
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    if failures:
        result["final_status"] = "FAIL_1013I_R6E_OFFICIAL_UNIT_MATERIAL_READONLY_EXTRACTION_FIXTURE"
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013I_R6E Official Unit Material Readonly Extraction Fixture Report

```text
STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
PAGE_WORK_STARTED=false
PAGE_USER_GATE_REQUIRED_BEFORE_R6F=true
```

## Result

```text
backend_adapter_created={str(result["backend_adapter_created"]).lower()}
source_contracts_loaded={str(result["source_contracts_loaded"]).lower()}
source_contract_count={result["source_contract_count"]}
official_dictionary_field_count={result["official_dictionary_field_count"]}
question_flow_stage_count={result["question_flow_stage_count"]}
textbook_anchor_candidates_created={str(result["textbook_anchor_candidates_created"]).lower()}
textbook_anchor_candidate_count={result["textbook_anchor_candidate_count"]}
big_unit_chain_candidates_created={str(result["big_unit_chain_candidates_created"]).lower()}
big_unit_chain_stage_count={result["big_unit_chain_stage_count"]}
lesson_position_candidate_created={str(result["lesson_position_candidate_created"]).lower()}
teacher_confirmation_required_items_created={str(result["teacher_confirmation_required_items_created"]).lower()}
teacher_confirmation_required_item_count={result["teacher_confirmation_required_item_count"]}
normal_candidate_card_generation_allowed={str(result["normal_candidate_card_generation_allowed"]).lower()}
page_work_started={str(result["page_work_started"]).lower()}
```

## Boundary

R6E is backend-adapter-only and readonly-extraction-only. It reads local official unit field contracts and R6D control fixtures, then produces candidate extraction fixtures for teacher review. It does not verify a textbook anchor, does not create a formal `unit_package`, does not generate a big-unit body, does not generate a single-lesson plan, does not enter page work, and does not write lesson body, HTML, database, memory, Feishu, export, or archive.

## Next Gate

The next stage is a page user-review gate, not automatic page implementation. Before any big-unit prep page fixture is created, the user must review and approve the page structure.
"""


def copy_source_delta(root: Path, output_root: Path) -> None:
    files = [
        (
            root / "scripts" / VALIDATOR_NAME,
            output_root / "source_delta_1013I_R6E" / "scripts" / VALIDATOR_NAME,
        ),
        (
            root / BACKEND_ADAPTER_RELATIVE_PATH,
            output_root / "source_delta_1013I_R6E" / BACKEND_ADAPTER_RELATIVE_PATH,
        ),
    ]
    for source, target in files:
        if source.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    root = args.root.resolve()
    output_root = resolve_output_root(root)
    payload = write_stage_files(root, output_root)
    stage_dir = output_root / STAGE_DIR_NAME
    result_path = stage_dir / "1013I_R6E_result.json"
    report_path = stage_dir / "1013I_R6E_report.md"
    stage_files = [
        stage_dir / "official_unit_material_source_index_1013I_R6E.json",
        stage_dir / "official_unit_material_extraction_fixture_1013I_R6E.json",
        stage_dir / "textbook_anchor_candidates_1013I_R6E.json",
        stage_dir / "big_unit_chain_candidates_1013I_R6E.json",
        stage_dir / "teacher_confirmation_required_items_1013I_R6E.json",
        result_path,
        report_path,
    ]
    result = build_result(root, output_root, payload, stage_files)
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
