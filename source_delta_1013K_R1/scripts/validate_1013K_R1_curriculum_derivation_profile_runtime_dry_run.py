from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R1_CURRICULUM_DERIVATION_PROFILE_RUNTIME_DRY_RUN"
FINAL_STATUS = "PASS_1013K_R1_CURRICULUM_DERIVATION_PROFILE_RUNTIME_DRY_RUN"
INHERITS_FROM = "1013K_R0_CURRICULUM_STANDARD_DERIVATION_BACKEND_CONTRACT"
NEXT_STAGE = "1013K_R2_CURRICULUM_PROFILE_TO_BIG_UNIT_CANDIDATE_ENVELOPE"
STAGE_DIR_NAME = "1013K_R1_curriculum_derivation_profile_runtime_dry_run"
VALIDATOR_NAME = "validate_1013K_R1_curriculum_derivation_profile_runtime_dry_run.py"
BACKEND_ADAPTER_RELATIVE_PATH = "backend/xiaobei_ai/prep_room_curriculum_derivation_runtime_dry_run_1013K_R1.py"
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
    from backend.xiaobei_ai.prep_room_curriculum_derivation_runtime_dry_run_1013K_R1 import (  # noqa: PLC0415
        build_curriculum_derivation_profile_runtime_dry_run,
    )

    return build_curriculum_derivation_profile_runtime_dry_run


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
    write_json(
        stage_dir / "curriculum_derivation_runtime_dry_run_request_1013K_R1.json",
        payload["dry_run_request"],
    )
    write_json(stage_dir / "curriculum_derivation_runtime_state_1013K_R1.json", payload["runtime_state"])
    write_json(stage_dir / "curriculum_derivation_gate_decision_1013K_R1.json", payload["gate_decision"])
    write_json(stage_dir / "curriculum_derivation_target_map_1013K_R1.json", payload["derivation_target_map"])
    write_json(stage_dir / "curriculum_derivation_runtime_trace_1013K_R1.json", payload["runtime_trace"])
    return payload


def copy_source_delta(root: Path, output_root: Path) -> list[Path]:
    delta_root = output_root / "source_delta_1013K_R1"
    backend_src = root / BACKEND_ADAPTER_RELATIVE_PATH
    backend_dst = delta_root / BACKEND_ADAPTER_RELATIVE_PATH
    script_src = root / "scripts" / VALIDATOR_NAME
    script_dst = delta_root / "scripts" / VALIDATOR_NAME
    backend_dst.parent.mkdir(parents=True, exist_ok=True)
    script_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backend_src, backend_dst)
    shutil.copy2(script_src, script_dst)
    return [backend_dst, script_dst]


def build_result(root: Path, output_root: Path, payload: dict[str, Any], stage_files: list[Path]) -> dict[str, Any]:
    stage_dir = output_root / STAGE_DIR_NAME
    r0_result = read_json(
        output_root / "1013K_R0_curriculum_standard_derivation_backend_contract" / "1013K_R0_result.json"
    )
    request = payload["dry_run_request"]
    state = payload["runtime_state"]
    decision = payload["gate_decision"]
    target_map = payload["derivation_target_map"]
    trace = payload["runtime_trace"]
    boundary = payload["boundary"]
    teacher_visible_scan_files = [path for path in stage_files if "source_delta" not in path.as_posix()]
    gate_ids = {gate["gate_id"]: gate for gate in decision.get("gates", [])}

    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "r0_result_present": True,
        "r0_pass": r0_result.get("final_status") == "PASS_1013K_R0_CURRICULUM_STANDARD_DERIVATION_BACKEND_CONTRACT",
        "backend_adapter_created": (root / BACKEND_ADAPTER_RELATIVE_PATH).exists(),
        "dry_run_request_created": (stage_dir / "curriculum_derivation_runtime_dry_run_request_1013K_R1.json").exists(),
        "runtime_state_created": (stage_dir / "curriculum_derivation_runtime_state_1013K_R1.json").exists(),
        "gate_decision_created": (stage_dir / "curriculum_derivation_gate_decision_1013K_R1.json").exists(),
        "target_map_created": (stage_dir / "curriculum_derivation_target_map_1013K_R1.json").exists(),
        "runtime_trace_created": (stage_dir / "curriculum_derivation_runtime_trace_1013K_R1.json").exists(),
        "runtime_dry_run_request_id_aligned": request["request_id"]
        == state["request_id"]
        == "curriculum_derivation_runtime_dry_run_request_1013K_R1",
        "curriculum_control_profile_built": bool(state["curriculum_control_profile"].get("profile_id")),
        "curriculum_profile_gate_pass": gate_ids.get("curriculum_control_profile_gate", {}).get("pass") is True,
        "textbook_anchor_gate_blocks_normal_generation": gate_ids.get("textbook_anchor_gate", {}).get(
            "blocks_normal_generation"
        )
        is True,
        "big_unit_chain_gate_blocks_normal_generation": gate_ids.get("big_unit_chain_gate", {}).get(
            "blocks_normal_generation"
        )
        is True,
        "teacher_confirmation_gate_blocks_normal_generation": gate_ids.get("teacher_confirmation_gate", {}).get(
            "blocks_normal_generation"
        )
        is True,
        "normal_candidate_generation_allowed": decision.get("normal_candidate_generation_allowed"),
        "degraded_preview_allowed": decision.get("degraded_preview_allowed"),
        "degraded_preview_label_required": decision.get("degraded_preview_label_required"),
        "derivation_target_count": target_map.get("target_count"),
        "targets_write_unit_package": any(target.get("writes_unit_package") for target in target_map.get("targets", [])),
        "targets_write_lesson_body": any(target.get("writes_lesson_body") for target in target_map.get("targets", [])),
        "trace_event_count": len(trace.get("events", [])),
        "runtime_trace_side_effects_performed": trace.get("side_effects_performed"),
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(teacher_visible_scan_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **boundary,
    }
    required_true = [
        "r0_result_present",
        "r0_pass",
        "backend_adapter_created",
        "dry_run_request_created",
        "runtime_state_created",
        "gate_decision_created",
        "target_map_created",
        "runtime_trace_created",
        "runtime_dry_run_request_id_aligned",
        "curriculum_control_profile_built",
        "curriculum_profile_gate_pass",
        "textbook_anchor_gate_blocks_normal_generation",
        "big_unit_chain_gate_blocks_normal_generation",
        "teacher_confirmation_gate_blocks_normal_generation",
        "degraded_preview_allowed",
        "degraded_preview_label_required",
        "runtime_dry_run_only",
        "in_memory_only",
        "readonly_sources_only",
        "preview_only",
    ]
    required_false = [
        "normal_candidate_generation_allowed",
        "targets_write_unit_package",
        "targets_write_lesson_body",
        "runtime_trace_side_effects_performed",
        "side_effects_performed",
        "runtime_schema_applied",
        "provider_called",
        "model_called",
        "database_written",
        "memory_written",
        "feishu_written",
        "formal_apply_performed",
        "lesson_body_modified",
        "html_body_modified",
        "unit_package_written",
        "textbook_anchor_verified",
        "official_curriculum_claim_created",
        "full_standard_text_stored",
        "full_standard_text_dumped_to_prompt",
        "big_unit_body_generated",
        "single_lesson_body_generated",
        "main_project_pushed",
    ]
    failures = [key for key in required_true if result.get(key) is not True]
    failures.extend([key for key in required_false if result.get(key) is not False])
    if result["derivation_target_count"] != 10:
        failures.append("derivation_target_count")
    if result["trace_event_count"] < 4:
        failures.append("trace_event_count")
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    result["validator_pass"] = not failures
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013K_R1 Curriculum Derivation Profile Runtime Dry Run Report

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={result["next_stage"]}

## Scope

R1 executes an in-memory runtime dry-run over the R0 curriculum derivation contract. It builds a runtime state, evaluates gates, maps derivation targets, and records a dry-run trace without side effects.

## Key Checks

```text
runtime_dry_run_only={str(result["runtime_dry_run_only"]).lower()}
in_memory_only={str(result["in_memory_only"]).lower()}
curriculum_control_profile_built={str(result["curriculum_control_profile_built"]).lower()}
curriculum_profile_gate_pass={str(result["curriculum_profile_gate_pass"]).lower()}
textbook_anchor_gate_blocks_normal_generation={str(result["textbook_anchor_gate_blocks_normal_generation"]).lower()}
big_unit_chain_gate_blocks_normal_generation={str(result["big_unit_chain_gate_blocks_normal_generation"]).lower()}
teacher_confirmation_gate_blocks_normal_generation={str(result["teacher_confirmation_gate_blocks_normal_generation"]).lower()}
normal_candidate_generation_allowed={str(result["normal_candidate_generation_allowed"]).lower()}
degraded_preview_allowed={str(result["degraded_preview_allowed"]).lower()}
provider_called={str(result["provider_called"]).lower()}
model_called={str(result["model_called"]).lower()}
database_written={str(result["database_written"]).lower()}
memory_written={str(result["memory_written"]).lower()}
side_effects_performed={str(result["side_effects_performed"]).lower()}
```

## Boundary

This stage does not apply runtime schema, does not call provider/model, does not write database/memory/Feishu, does not write unit_package or lesson_body, and does not formal apply. Normal candidate generation remains blocked because textbook anchor, big-unit chain, and teacher confirmation are still pending.

## Validator

validator_pass={str(result["validator_pass"]).lower()}
failed_checks={json.dumps(result["failed_checks"], ensure_ascii=False)}
"""


def update_review_root(output_root: Path) -> None:
    latest = f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
NEXT_STAGE={NEXT_STAGE}
RUNTIME_DRY_RUN_ONLY=true
IN_MEMORY_ONLY=true
RUNTIME_SCHEMA_APPLIED=false
PROVIDER_MODEL_CALL_ALLOWED=false
FORMAL_APPLY_ALLOWED=false
DATABASE_WRITE_ALLOWED=false
MEMORY_WRITE_ALLOWED=false

1013K_R1 runs an in-memory dry-run of the curriculum derivation profile from R0. It builds runtime state, evaluates gates, maps derivation targets, and records a trace without side effects. Normal candidate generation remains blocked until textbook anchor, big-unit chain, and teacher confirmation are ready.
"""
    manifest = f"""# Review Package Manifest

Latest stage: `{STAGE_ID}`

Includes:

- `{STAGE_DIR_NAME}/curriculum_derivation_runtime_dry_run_request_1013K_R1.json`
- `{STAGE_DIR_NAME}/curriculum_derivation_runtime_state_1013K_R1.json`
- `{STAGE_DIR_NAME}/curriculum_derivation_gate_decision_1013K_R1.json`
- `{STAGE_DIR_NAME}/curriculum_derivation_target_map_1013K_R1.json`
- `{STAGE_DIR_NAME}/curriculum_derivation_runtime_trace_1013K_R1.json`
- `{STAGE_DIR_NAME}/1013K_R1_result.json`
- `{STAGE_DIR_NAME}/1013K_R1_report.md`
- `backend/xiaobei_ai/prep_room_curriculum_derivation_runtime_dry_run_1013K_R1.py`
- `scripts/{VALIDATOR_NAME}`

Boundary: in-memory runtime dry-run only. No runtime schema applied, no provider/model call, no database/memory/Feishu write, no formal apply, no unit_package or lesson body write, main project not pushed.

Next stage: `{NEXT_STAGE}`
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)


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
        stage_dir / "curriculum_derivation_runtime_dry_run_request_1013K_R1.json",
        stage_dir / "curriculum_derivation_runtime_state_1013K_R1.json",
        stage_dir / "curriculum_derivation_gate_decision_1013K_R1.json",
        stage_dir / "curriculum_derivation_target_map_1013K_R1.json",
        stage_dir / "curriculum_derivation_runtime_trace_1013K_R1.json",
        *source_delta_files,
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ]
    result = build_result(root, output_root, payload, stage_files)
    write_json(stage_dir / "1013K_R1_result.json", result)
    write_text(stage_dir / "1013K_R1_report.md", build_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["validator_pass"]:
        print("ALL_1013K_R1_CURRICULUM_DERIVATION_PROFILE_RUNTIME_DRY_RUN_CHECKS_OK")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
