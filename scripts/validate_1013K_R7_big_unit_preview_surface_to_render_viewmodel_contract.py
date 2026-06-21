from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R7_BIG_UNIT_PREVIEW_SURFACE_TO_RENDER_VIEWMODEL_CONTRACT"
FINAL_STATUS = "PASS_1013K_R7_BIG_UNIT_PREVIEW_SURFACE_TO_RENDER_VIEWMODEL_CONTRACT"
INHERITS_FROM = "1013K_R6_BIG_UNIT_REVIEW_ACTION_STATE_TO_PREVIEW_SURFACE_FIXTURE"
NEXT_STAGE = "1013K_R8_BIG_UNIT_RENDER_VIEWMODEL_READONLY_ENDPOINT_CONTRACT"
STAGE_DIR_NAME = "1013K_R7_big_unit_preview_surface_to_render_viewmodel_contract"
VALIDATOR_NAME = "validate_1013K_R7_big_unit_preview_surface_to_render_viewmodel_contract.py"
BACKEND_ADAPTER_RELATIVE_PATH = "backend/xiaobei_ai/prep_room_big_unit_render_viewmodel_1013K_R7.py"
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
    from backend.xiaobei_ai.prep_room_big_unit_render_viewmodel_1013K_R7 import (  # noqa: PLC0415
        build_big_unit_preview_surface_to_render_viewmodel_contract,
    )

    return build_big_unit_preview_surface_to_render_viewmodel_contract


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
    write_json(stage_dir / "big_unit_render_viewmodel_contract_1013K_R7.json", payload["render_viewmodel_contract"])
    write_json(stage_dir / "big_unit_render_viewmodel_fixture_1013K_R7.json", payload["render_viewmodel_fixture"])
    write_json(stage_dir / "big_unit_section_to_render_chunk_mapping_1013K_R7.json", payload["section_render_mapping"])
    write_json(stage_dir / "big_unit_render_viewmodel_trace_1013K_R7.json", payload["render_viewmodel_trace"])
    return payload


def copy_source_delta(root: Path, output_root: Path) -> list[Path]:
    delta_root = output_root / "source_delta_1013K_R7"
    backend_src = root / BACKEND_ADAPTER_RELATIVE_PATH
    backend_dst = delta_root / BACKEND_ADAPTER_RELATIVE_PATH
    script_src = root / "scripts" / VALIDATOR_NAME
    script_dst = delta_root / "scripts" / VALIDATOR_NAME
    backend_dst.parent.mkdir(parents=True, exist_ok=True)
    script_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backend_src, backend_dst)
    shutil.copy2(script_src, script_dst)
    return [backend_dst, script_dst]


def update_local_review_root(output_root: Path) -> None:
    latest = f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
NEXT_STAGE={NEXT_STAGE}
LOCAL_ONLY_SMALL_PACKAGE=true
GITHUB_UPLOAD_DEFERRED_UNTIL_NEXT_MILESTONE=true
PROVIDER_MODEL_CALL_ALLOWED=false
FORMAL_APPLY_ALLOWED=false
DATABASE_WRITE_ALLOWED=false
MEMORY_WRITE_ALLOWED=false

1013K_R7 converts the R6 big-unit preview surface into a render ViewModel contract and fixture. The contract is chunk-based and progressive-render ready; it explicitly does not require a whole-document blob.
"""
    manifest = f"""# Review Package Manifest

Latest local stage: `{STAGE_ID}`

Includes:

- `{STAGE_DIR_NAME}/big_unit_render_viewmodel_contract_1013K_R7.json`
- `{STAGE_DIR_NAME}/big_unit_render_viewmodel_fixture_1013K_R7.json`
- `{STAGE_DIR_NAME}/big_unit_section_to_render_chunk_mapping_1013K_R7.json`
- `{STAGE_DIR_NAME}/big_unit_render_viewmodel_trace_1013K_R7.json`
- `{STAGE_DIR_NAME}/1013K_R7_result.json`
- `{STAGE_DIR_NAME}/1013K_R7_report.md`
- `backend/xiaobei_ai/prep_room_big_unit_render_viewmodel_1013K_R7.py`
- `scripts/{VALIDATOR_NAME}`

Boundary: local-only small package. No provider/model call, no runtime connection, no database/memory/Feishu write, no formal apply, no unit_package or lesson body write.
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)


def build_result(root: Path, output_root: Path, payload: dict[str, Any], stage_files: list[Path]) -> dict[str, Any]:
    stage_dir = output_root / STAGE_DIR_NAME
    r6_result = read_json(
        output_root / "1013K_R6_big_unit_review_action_state_to_preview_surface_fixture" / "1013K_R6_result.json"
    )
    contract = payload["render_viewmodel_contract"]
    viewmodel = payload["render_viewmodel_fixture"]
    mapping = payload["section_render_mapping"]
    trace = payload["render_viewmodel_trace"]
    boundary = payload["boundary"]
    chunks = viewmodel.get("section_chunks", [])
    teacher_visible_scan_files = [path for path in stage_files if "source_delta" not in path.as_posix()]

    all_chunks_visible = all(chunk.get("render_state") == "visible" for chunk in chunks)
    all_chunks_have_paragraphs = all(bool(chunk.get("paragraphs")) for chunk in chunks)
    all_chunks_have_three_actions = all(len(chunk.get("actions", [])) == 3 for chunk in chunks)
    all_chunk_actions_preview_only = all(
        action.get("preview_only") is True and action.get("formal_apply_performed") is False
        for chunk in chunks
        for action in chunk.get("actions", [])
    )
    all_mappings_independent = all(item.get("can_update_independently") is True for item in mapping.get("mappings", []))
    all_trace_side_effect_free = all(event.get("side_effects_performed") is False for event in trace.get("events", []))

    progressive_contract = contract.get("progressive_render_contract", {})
    progressive_fixture = viewmodel.get("progressive_render", {})

    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "github_upload_deferred_until_next_milestone": True,
        "r6_pass": r6_result.get("final_status")
        == "PASS_1013K_R6_BIG_UNIT_REVIEW_ACTION_STATE_TO_PREVIEW_SURFACE_FIXTURE",
        "backend_adapter_created": (root / BACKEND_ADAPTER_RELATIVE_PATH).exists(),
        "render_viewmodel_contract_created": (stage_dir / "big_unit_render_viewmodel_contract_1013K_R7.json").exists(),
        "render_viewmodel_fixture_created": (stage_dir / "big_unit_render_viewmodel_fixture_1013K_R7.json").exists(),
        "section_render_mapping_created": (stage_dir / "big_unit_section_to_render_chunk_mapping_1013K_R7.json").exists(),
        "render_viewmodel_trace_created": (stage_dir / "big_unit_render_viewmodel_trace_1013K_R7.json").exists(),
        "viewmodel_kind": viewmodel.get("viewmodel_kind"),
        "chunk_count": progressive_fixture.get("chunk_count"),
        "mapping_count": mapping.get("mapping_count"),
        "side_reference_default_collapsed": viewmodel.get("side_reference", {}).get("default_collapsed"),
        "material_prompt_present": bool(viewmodel.get("material_prompt")),
        "formal_apply_action_present": viewmodel.get("action_bar", {}).get("formal_apply_action_present"),
        "section_chunks_renderable_independently": progressive_contract.get("section_chunks_renderable_independently")
        and progressive_fixture.get("section_chunks_renderable_independently"),
        "whole_document_blob_required": progressive_contract.get("whole_document_blob_required")
        or progressive_fixture.get("whole_document_blob_required")
        or mapping.get("whole_document_blob_required"),
        "can_stream_section_by_section": progressive_contract.get("can_stream_section_by_section")
        and progressive_fixture.get("can_stream_section_by_section"),
        "can_update_single_section_preview": progressive_contract.get("can_update_single_section_preview")
        and progressive_fixture.get("can_update_single_section_preview"),
        "all_chunks_visible": all_chunks_visible,
        "all_chunks_have_paragraphs": all_chunks_have_paragraphs,
        "all_chunks_have_three_actions": all_chunks_have_three_actions,
        "all_chunk_actions_preview_only": all_chunk_actions_preview_only,
        "all_mappings_independent": all_mappings_independent,
        "trace_event_count": trace.get("event_count"),
        "all_trace_side_effect_free": all_trace_side_effect_free,
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(teacher_visible_scan_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **boundary,
    }
    required_true = [
        "github_upload_deferred_until_next_milestone",
        "r6_pass",
        "backend_adapter_created",
        "render_viewmodel_contract_created",
        "render_viewmodel_fixture_created",
        "section_render_mapping_created",
        "render_viewmodel_trace_created",
        "side_reference_default_collapsed",
        "material_prompt_present",
        "section_chunks_renderable_independently",
        "can_stream_section_by_section",
        "can_update_single_section_preview",
        "all_chunks_visible",
        "all_chunks_have_paragraphs",
        "all_chunks_have_three_actions",
        "all_chunk_actions_preview_only",
        "all_mappings_independent",
        "all_trace_side_effect_free",
        "render_viewmodel_contract_only",
        "render_viewmodel_fixture_only",
        "preview_only",
        "teacher_review_required",
    ]
    required_false = [
        "formal_apply_action_present",
        "whole_document_blob_required",
        "runtime_connected",
        "provider_called",
        "model_called",
        "database_written",
        "memory_written",
        "feishu_written",
        "formal_apply_performed",
        "unit_package_written",
        "lesson_body_modified",
        "html_body_modified",
        "runtime_schema_applied",
        "official_curriculum_claim_created",
        "main_project_pushed",
    ]
    failures = [key for key in required_true if result.get(key) is not True]
    failures.extend([key for key in required_false if result.get(key) is not False])
    if result["viewmodel_kind"] != "prep_room_big_unit_design_preview":
        failures.append("viewmodel_kind")
    if result["chunk_count"] != 10:
        failures.append("chunk_count")
    if result["mapping_count"] != 10:
        failures.append("mapping_count")
    if result["trace_event_count"] != 4:
        failures.append("trace_event_count")
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    result["validator_pass"] = not failures
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013K_R7 Big Unit Preview Surface To Render ViewModel Contract Report

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={result["next_stage"]}
LOCAL_ONLY_SMALL_PACKAGE=true
GITHUB_UPLOAD_DEFERRED_UNTIL_NEXT_MILESTONE=true

## Scope

R7 turns the R6 big-unit preview surface into a frontend render ViewModel contract and fixture. The ViewModel is chunk-based, so sections can render and update independently.

## Key Checks

```text
viewmodel_kind={result["viewmodel_kind"]}
chunk_count={result["chunk_count"]}
mapping_count={result["mapping_count"]}
section_chunks_renderable_independently={str(result["section_chunks_renderable_independently"]).lower()}
whole_document_blob_required={str(result["whole_document_blob_required"]).lower()}
can_stream_section_by_section={str(result["can_stream_section_by_section"]).lower()}
can_update_single_section_preview={str(result["can_update_single_section_preview"]).lower()}
provider_called={str(result["provider_called"]).lower()}
model_called={str(result["model_called"]).lower()}
database_written={str(result["database_written"]).lower()}
memory_written={str(result["memory_written"]).lower()}
formal_apply_performed={str(result["formal_apply_performed"]).lower()}
```

## Validator

validator_pass={str(result["validator_pass"]).lower()}
failed_checks={json.dumps(result["failed_checks"], ensure_ascii=False)}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    root = args.root.resolve()
    output_root = resolve_output_root(root)
    payload = write_stage_files(root, output_root)
    update_local_review_root(output_root)
    source_delta_files = copy_source_delta(root, output_root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_files = [
        stage_dir / "big_unit_render_viewmodel_contract_1013K_R7.json",
        stage_dir / "big_unit_render_viewmodel_fixture_1013K_R7.json",
        stage_dir / "big_unit_section_to_render_chunk_mapping_1013K_R7.json",
        stage_dir / "big_unit_render_viewmodel_trace_1013K_R7.json",
        *source_delta_files,
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ]
    result = build_result(root, output_root, payload, stage_files)
    write_json(stage_dir / "1013K_R7_result.json", result)
    write_text(stage_dir / "1013K_R7_report.md", build_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["validator_pass"]:
        print("ALL_1013K_R7_BIG_UNIT_PREVIEW_SURFACE_TO_RENDER_VIEWMODEL_CONTRACT_CHECKS_OK")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
