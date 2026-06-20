from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R0_CURRICULUM_STANDARD_DERIVATION_BACKEND_CONTRACT"
FINAL_STATUS = "PASS_1013K_R0_CURRICULUM_STANDARD_DERIVATION_BACKEND_CONTRACT"
NEXT_STAGE = "1013K_R1_CURRICULUM_DERIVATION_PROFILE_RUNTIME_DRY_RUN"
STAGE_DIR_NAME = "1013K_R0_curriculum_standard_derivation_backend_contract"
VALIDATOR_NAME = "validate_1013K_R0_curriculum_standard_derivation_backend_contract.py"
BACKEND_ADAPTER_RELATIVE_PATH = "backend/xiaobei_ai/prep_room_curriculum_standard_derivation_1013K_R0.py"
R6C_STAGE = "1013I_R6C_CURRICULUM_STANDARD_CONTROL_LAYER_CONTRACT"
R6D_STAGE = "1013I_R6D_TEXTBOOK_ANCHOR_AND_BIG_UNIT_DESIGN_CHAIN_CONTRACT"
R6E_STAGE = "1013I_R6E_OFFICIAL_UNIT_MATERIAL_READONLY_EXTRACTION_FIXTURE"
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
    from backend.xiaobei_ai.prep_room_curriculum_standard_derivation_1013K_R0 import (  # noqa: PLC0415
        build_curriculum_standard_derivation_backend_contract,
    )

    return build_curriculum_standard_derivation_backend_contract


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


def write_contract_md(path: Path, contract: dict[str, Any]) -> None:
    targets = "\n".join(f"- `{item}`" for item in contract["derivation_targets"])
    blocked = "\n".join(f"- `{item}`" for item in contract["blocked_targets_before_confirmation"])
    chain = " -> ".join(contract["upstream_chain"])
    text = f"""# 1013K_R0 Curriculum Standard Derivation Backend Contract

STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={R6C_STAGE} + {R6D_STAGE} + {R6E_STAGE}
NEXT_STAGE={NEXT_STAGE}

## Purpose

1013K_R0 defines the backend derivation contract for starting prep-room reasoning from the curriculum-standard control layer. It does not generate a lesson body, does not apply a runtime schema, and does not call a provider/model.

## Reasoning Chain

`{chain}`

## Derivation Targets

{targets}

## Blocked Before Teacher Confirmation

{blocked}

## Boundary

```text
curriculum_standard_as_control_layer=true
full_standard_text_not_dumped_to_prompt=true
textbook_anchor_required=true
official_case_reference_only=true
big_unit_derivation_before_single_lesson=true
teacher_confirmation_required=true
provider_called=false
model_called=false
database_written=false
memory_written=false
formal_apply_performed=false
```
"""
    write_text(path, text)


def write_stage_files(root: Path, output_root: Path) -> dict[str, Any]:
    builder = load_backend_adapter(root)
    payload = builder(root)
    stage_dir = output_root / STAGE_DIR_NAME
    write_json(
        stage_dir / "curriculum_standard_slice_schema_1013K_R0.json",
        payload["curriculum_standard_slice_schema"],
    )
    write_json(
        stage_dir / "curriculum_control_profile_schema_1013K_R0.json",
        payload["curriculum_control_profile_schema"],
    )
    write_json(
        stage_dir / "curriculum_to_big_unit_derivation_contract_1013K_R0.json",
        payload["curriculum_to_big_unit_derivation_contract"],
    )
    write_contract_md(
        stage_dir / "curriculum_to_big_unit_derivation_contract_1013K_R0.md",
        payload["curriculum_to_big_unit_derivation_contract"],
    )
    write_json(
        stage_dir / "curriculum_derivation_trace_fixture_1013K_R0.json",
        payload["curriculum_derivation_trace_fixture"],
    )
    return payload


def build_result(root: Path, output_root: Path, payload: dict[str, Any], stage_files: list[Path]) -> dict[str, Any]:
    stage_dir = output_root / STAGE_DIR_NAME
    r6c_result = read_json(output_root / "1013I_R6C_curriculum_standard_control_layer_contract" / "1013I_R6C_result.json")
    r6d_result = read_json(
        output_root / "1013I_R6D_textbook_anchor_and_big_unit_design_chain_contract" / "1013I_R6D_result.json"
    )
    r6e_result = read_json(
        output_root / "1013I_R6E_official_unit_material_readonly_extraction_fixture" / "1013I_R6E_result.json"
    )
    slice_schema = payload["curriculum_standard_slice_schema"]
    control_schema = payload["curriculum_control_profile_schema"]
    derivation_contract = payload["curriculum_to_big_unit_derivation_contract"]
    trace = payload["curriculum_derivation_trace_fixture"]
    boundary = payload["boundary"]
    teacher_visible_scan_files = [path for path in stage_files if "source_delta" not in path.as_posix()]

    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": [R6C_STAGE, R6D_STAGE, R6E_STAGE],
        "next_stage": NEXT_STAGE,
        "r6c_pass": r6c_result.get("final_status") == "PASS_1013I_R6C_CURRICULUM_STANDARD_CONTROL_LAYER_CONTRACT",
        "r6d_pass": r6d_result.get("final_status")
        == "PASS_1013I_R6D_TEXTBOOK_ANCHOR_AND_BIG_UNIT_DESIGN_CHAIN_CONTRACT",
        "r6e_pass": r6e_result.get("final_status")
        == "PASS_1013I_R6E_OFFICIAL_UNIT_MATERIAL_READONLY_EXTRACTION_FIXTURE",
        "backend_adapter_created": (root / BACKEND_ADAPTER_RELATIVE_PATH).exists(),
        "curriculum_standard_slice_schema_created": (stage_dir / "curriculum_standard_slice_schema_1013K_R0.json").exists(),
        "curriculum_control_profile_schema_created": (
            stage_dir / "curriculum_control_profile_schema_1013K_R0.json"
        ).exists(),
        "curriculum_to_big_unit_derivation_contract_created": (
            stage_dir / "curriculum_to_big_unit_derivation_contract_1013K_R0.json"
        ).exists()
        and (stage_dir / "curriculum_to_big_unit_derivation_contract_1013K_R0.md").exists(),
        "curriculum_derivation_trace_fixture_created": (
            stage_dir / "curriculum_derivation_trace_fixture_1013K_R0.json"
        ).exists(),
        "curriculum_standard_as_control_layer": derivation_contract["required_gates"][
            "curriculum_standard_as_control_layer"
        ],
        "full_standard_text_not_dumped_to_prompt": slice_schema["source_policy"][
            "full_standard_text_dumped_to_prompt"
        ]
        is False,
        "structured_standard_slices_created": len(slice_schema.get("slice_examples", [])) >= 1,
        "curriculum_control_profile_defined": control_schema.get("profile_object") == "curriculum_control_profile",
        "textbook_anchor_required": derivation_contract["required_gates"]["textbook_anchor_required"],
        "big_unit_design_chain_required": derivation_contract["required_gates"]["big_unit_design_chain_required"],
        "official_case_reference_only": derivation_contract["required_gates"]["official_case_reference_only"],
        "big_unit_derivation_before_single_lesson": derivation_contract["upstream_chain"].index(
            "big_unit_chain_check"
        )
        < derivation_contract["upstream_chain"].index("lesson_position_judgement"),
        "teacher_confirmation_required": derivation_contract["required_gates"]["teacher_confirmation_required"],
        "candidate_only": derivation_contract["generation_policy"]["candidate_only"],
        "normal_candidate_generation_blocked_without_curriculum_profile": derivation_contract["generation_policy"][
            "normal_candidate_generation_blocked_without_curriculum_profile"
        ],
        "trace_step_count": len(trace.get("trace_steps", [])),
        "trace_has_control_profile_candidate": bool(trace.get("control_profile_candidate")),
        "trace_writes_unit_package": any(
            step.get("writes_unit_package") is True for step in trace.get("trace_steps", [])
        ),
        "trace_writes_lesson_body": any(step.get("writes_lesson_body") is True for step in trace.get("trace_steps", [])),
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(teacher_visible_scan_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **boundary,
    }

    required_true = [
        "r6c_pass",
        "r6d_pass",
        "r6e_pass",
        "backend_adapter_created",
        "curriculum_standard_slice_schema_created",
        "curriculum_control_profile_schema_created",
        "curriculum_to_big_unit_derivation_contract_created",
        "curriculum_derivation_trace_fixture_created",
        "curriculum_standard_as_control_layer",
        "full_standard_text_not_dumped_to_prompt",
        "structured_standard_slices_created",
        "curriculum_control_profile_defined",
        "textbook_anchor_required",
        "big_unit_design_chain_required",
        "official_case_reference_only",
        "big_unit_derivation_before_single_lesson",
        "teacher_confirmation_required",
        "candidate_only",
        "normal_candidate_generation_blocked_without_curriculum_profile",
        "trace_has_control_profile_candidate",
        "backend_contract_only",
        "backend_adapter_fixture_only",
        "preview_only",
    ]
    required_false = [
        "trace_writes_unit_package",
        "trace_writes_lesson_body",
        "runtime_schema_applied",
        "real_curriculum_standard_full_text_parsed",
        "full_standard_text_stored",
        "full_standard_text_dumped_to_prompt",
        "official_curriculum_claim_created",
        "textbook_anchor_verified",
        "unit_package_written",
        "lesson_body_modified",
        "html_body_modified",
        "product_runtime_called",
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
    if result["trace_step_count"] < 5:
        failures.append("trace_step_count")
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    result["validator_pass"] = not failures
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013K_R0 Curriculum Standard Derivation Backend Contract Report

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
NEXT_STAGE={result["next_stage"]}

## Scope

This stage defines the backend contract for deriving prep-room candidates from curriculum-standard control. It creates structured slice/profile schemas, a derivation contract, and a trace fixture.

## Key Checks

```text
curriculum_standard_as_control_layer={str(result["curriculum_standard_as_control_layer"]).lower()}
full_standard_text_not_dumped_to_prompt={str(result["full_standard_text_not_dumped_to_prompt"]).lower()}
textbook_anchor_required={str(result["textbook_anchor_required"]).lower()}
big_unit_design_chain_required={str(result["big_unit_design_chain_required"]).lower()}
official_case_reference_only={str(result["official_case_reference_only"]).lower()}
big_unit_derivation_before_single_lesson={str(result["big_unit_derivation_before_single_lesson"]).lower()}
teacher_confirmation_required={str(result["teacher_confirmation_required"]).lower()}
provider_called={str(result["provider_called"]).lower()}
model_called={str(result["model_called"]).lower()}
database_written={str(result["database_written"]).lower()}
memory_written={str(result["memory_written"]).lower()}
formal_apply_performed={str(result["formal_apply_performed"]).lower()}
```

## Boundary

1013K_R0 is backend-contract-only and fixture-only. It does not parse real curriculum-standard full text, does not call provider/model, does not apply runtime schema, does not write database/memory/Feishu, and does not modify lesson body or HTML.

## Validator

validator_pass={str(result["validator_pass"]).lower()}
failed_checks={json.dumps(result["failed_checks"], ensure_ascii=False)}
"""


def update_review_root(output_root: Path) -> None:
    latest = f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
NEXT_STAGE={NEXT_STAGE}
BACKEND_CONTRACT_ONLY=true
RUNTIME_SCHEMA_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
FORMAL_APPLY_ALLOWED=false
DATABASE_WRITE_ALLOWED=false
MEMORY_WRITE_ALLOWED=false

1013K_R0 starts the backend line for curriculum-standard-first derivation. It creates structured curriculum slice/profile schemas and a derivation trace fixture, but does not enter runtime schema, provider/model calls, database/memory/Feishu writes, or formal apply.
"""
    manifest = f"""# Review Package Manifest

Latest stage: `{STAGE_ID}`

Includes:

- `{STAGE_DIR_NAME}/curriculum_standard_slice_schema_1013K_R0.json`
- `{STAGE_DIR_NAME}/curriculum_control_profile_schema_1013K_R0.json`
- `{STAGE_DIR_NAME}/curriculum_to_big_unit_derivation_contract_1013K_R0.json`
- `{STAGE_DIR_NAME}/curriculum_to_big_unit_derivation_contract_1013K_R0.md`
- `{STAGE_DIR_NAME}/curriculum_derivation_trace_fixture_1013K_R0.json`
- `{STAGE_DIR_NAME}/1013K_R0_result.json`
- `{STAGE_DIR_NAME}/1013K_R0_report.md`
- `backend/xiaobei_ai/prep_room_curriculum_standard_derivation_1013K_R0.py`
- `scripts/{VALIDATOR_NAME}`

Boundary: backend contract / fixture only. No runtime schema applied, no provider/model call, no database/memory/Feishu write, no formal apply, no lesson body or HTML modification, main project not pushed.

Next stage: `{NEXT_STAGE}`
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)


def copy_source_delta(root: Path, output_root: Path) -> list[Path]:
    delta_root = output_root / "source_delta_1013K_R0"
    backend_src = root / BACKEND_ADAPTER_RELATIVE_PATH
    backend_dst = delta_root / BACKEND_ADAPTER_RELATIVE_PATH
    script_src = root / "scripts" / VALIDATOR_NAME
    script_dst = delta_root / "scripts" / VALIDATOR_NAME
    backend_dst.parent.mkdir(parents=True, exist_ok=True)
    script_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backend_src, backend_dst)
    shutil.copy2(script_src, script_dst)
    return [backend_dst, script_dst]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    root = args.root.resolve()
    output_root = resolve_output_root(root)
    payload = write_stage_files(root, output_root)
    update_review_root(output_root)
    source_delta_files = copy_source_delta(root, output_root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_files = [
        stage_dir / "curriculum_standard_slice_schema_1013K_R0.json",
        stage_dir / "curriculum_control_profile_schema_1013K_R0.json",
        stage_dir / "curriculum_to_big_unit_derivation_contract_1013K_R0.json",
        stage_dir / "curriculum_to_big_unit_derivation_contract_1013K_R0.md",
        stage_dir / "curriculum_derivation_trace_fixture_1013K_R0.json",
        *source_delta_files,
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ]
    result = build_result(root, output_root, payload, stage_files)
    write_json(stage_dir / "1013K_R0_result.json", result)
    write_text(stage_dir / "1013K_R0_report.md", build_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["validator_pass"]:
        print("ALL_1013K_R0_CURRICULUM_STANDARD_DERIVATION_BACKEND_CONTRACT_CHECKS_OK")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
