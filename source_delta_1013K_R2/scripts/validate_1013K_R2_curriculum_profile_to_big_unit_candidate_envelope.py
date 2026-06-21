from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R2_CURRICULUM_PROFILE_TO_BIG_UNIT_CANDIDATE_ENVELOPE"
FINAL_STATUS = "PASS_1013K_R2_CURRICULUM_PROFILE_TO_BIG_UNIT_CANDIDATE_ENVELOPE"
INHERITS_FROM = "1013K_R1_CURRICULUM_DERIVATION_PROFILE_RUNTIME_DRY_RUN"
NEXT_STAGE = "1013K_R3_BIG_UNIT_CANDIDATE_ENVELOPE_TO_STATIC_SECTION_PREVIEW"
STAGE_DIR_NAME = "1013K_R2_curriculum_profile_to_big_unit_candidate_envelope"
VALIDATOR_NAME = "validate_1013K_R2_curriculum_profile_to_big_unit_candidate_envelope.py"
BACKEND_ADAPTER_RELATIVE_PATH = "backend/xiaobei_ai/prep_room_curriculum_profile_candidate_envelope_1013K_R2.py"
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
    from backend.xiaobei_ai.prep_room_curriculum_profile_candidate_envelope_1013K_R2 import (  # noqa: PLC0415
        build_curriculum_profile_to_big_unit_candidate_envelope,
    )

    return build_curriculum_profile_to_big_unit_candidate_envelope


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
    write_json(stage_dir / "candidate_generation_policy_1013K_R2.json", payload["candidate_generation_policy"])
    write_json(stage_dir / "prompt_context_pack_1013K_R2.json", payload["prompt_context_pack"])
    write_json(stage_dir / "big_unit_candidate_envelope_bundle_1013K_R2.json", payload["candidate_envelope_bundle"])
    write_json(stage_dir / "candidate_envelope_trace_1013K_R2.json", payload["candidate_envelope_trace"])
    return payload


def copy_source_delta(root: Path, output_root: Path) -> list[Path]:
    delta_root = output_root / "source_delta_1013K_R2"
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
    r1_result = read_json(output_root / "1013K_R1_curriculum_derivation_profile_runtime_dry_run" / "1013K_R1_result.json")
    policy = payload["candidate_generation_policy"]
    context = payload["prompt_context_pack"]
    bundle = payload["candidate_envelope_bundle"]
    trace = payload["candidate_envelope_trace"]
    boundary = payload["boundary"]
    teacher_visible_scan_files = [path for path in stage_files if "source_delta" not in path.as_posix()]
    envelopes = bundle.get("envelopes", [])

    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "github_upload_deferred_until_milestone": True,
        "r1_pass": r1_result.get("final_status") == "PASS_1013K_R1_CURRICULUM_DERIVATION_PROFILE_RUNTIME_DRY_RUN",
        "backend_adapter_created": (root / BACKEND_ADAPTER_RELATIVE_PATH).exists(),
        "candidate_generation_policy_created": (stage_dir / "candidate_generation_policy_1013K_R2.json").exists(),
        "prompt_context_pack_created": (stage_dir / "prompt_context_pack_1013K_R2.json").exists(),
        "candidate_envelope_bundle_created": (stage_dir / "big_unit_candidate_envelope_bundle_1013K_R2.json").exists(),
        "candidate_envelope_trace_created": (stage_dir / "candidate_envelope_trace_1013K_R2.json").exists(),
        "envelope_count": bundle.get("envelope_count"),
        "all_envelopes_teacher_review_required": all(
            envelope.get("teacher_review_required") is True for envelope in envelopes
        ),
        "all_envelopes_degraded_preview_label_required": all(
            envelope.get("degraded_preview_label_required") is True for envelope in envelopes
        ),
        "all_envelopes_candidate_text_not_generated": all(
            envelope.get("candidate_text_generated") is False for envelope in envelopes
        ),
        "all_envelopes_write_nothing": all(
            envelope.get("writes_unit_package") is False and envelope.get("writes_lesson_body") is False
            for envelope in envelopes
        ),
        "normal_candidate_generation_allowed": policy.get("normal_candidate_generation_allowed"),
        "degraded_preview_allowed": policy.get("degraded_preview_allowed"),
        "provider_model_call_allowed": policy.get("provider_model_call_allowed"),
        "prompt_excludes_full_standard_text": "full_curriculum_standard_text" in context.get("prompt_must_not_include", []),
        "future_model_call_allowed": context.get("future_model_call_allowed"),
        "trace_event_count": len(trace.get("events", [])),
        "trace_side_effects_performed": trace.get("side_effects_performed"),
        "trace_candidate_text_generated": trace.get("candidate_text_generated"),
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(teacher_visible_scan_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **boundary,
    }
    required_true = [
        "github_upload_deferred_until_milestone",
        "r1_pass",
        "backend_adapter_created",
        "candidate_generation_policy_created",
        "prompt_context_pack_created",
        "candidate_envelope_bundle_created",
        "candidate_envelope_trace_created",
        "all_envelopes_teacher_review_required",
        "all_envelopes_degraded_preview_label_required",
        "all_envelopes_candidate_text_not_generated",
        "all_envelopes_write_nothing",
        "degraded_preview_allowed",
        "prompt_excludes_full_standard_text",
        "candidate_envelope_only",
        "prompt_envelope_only",
        "degraded_preview_only",
        "preview_only",
    ]
    required_false = [
        "normal_candidate_generation_allowed",
        "provider_model_call_allowed",
        "future_model_call_allowed",
        "trace_side_effects_performed",
        "trace_candidate_text_generated",
        "provider_called",
        "model_called",
        "candidate_text_generated",
        "unit_package_written",
        "lesson_body_modified",
        "html_body_modified",
        "database_written",
        "memory_written",
        "feishu_written",
        "formal_apply_performed",
        "runtime_schema_applied",
        "full_standard_text_dumped_to_prompt",
        "official_curriculum_claim_created",
        "main_project_pushed",
    ]
    failures = [key for key in required_true if result.get(key) is not True]
    failures.extend([key for key in required_false if result.get(key) is not False])
    if result["envelope_count"] != 10:
        failures.append("envelope_count")
    if result["trace_event_count"] < 3:
        failures.append("trace_event_count")
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    result["validator_pass"] = not failures
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013K_R2 Curriculum Profile To Big Unit Candidate Envelope Report

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={result["next_stage"]}
GITHUB_UPLOAD_DEFERRED_UNTIL_MILESTONE=true

## Scope

R2 converts the R1 curriculum control profile and target map into big-unit candidate generation envelopes. It does not generate candidate text, does not call a provider/model, and does not write unit_package, lesson body, database, memory, or Feishu.

## Key Checks

```text
envelope_count={result["envelope_count"]}
normal_candidate_generation_allowed={str(result["normal_candidate_generation_allowed"]).lower()}
degraded_preview_allowed={str(result["degraded_preview_allowed"]).lower()}
all_envelopes_teacher_review_required={str(result["all_envelopes_teacher_review_required"]).lower()}
all_envelopes_candidate_text_not_generated={str(result["all_envelopes_candidate_text_not_generated"]).lower()}
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


def update_local_review_root(output_root: Path) -> None:
    latest = f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
NEXT_STAGE={NEXT_STAGE}
LOCAL_ONLY_SMALL_PACKAGE=true
GITHUB_UPLOAD_DEFERRED_UNTIL_MILESTONE=true
PROVIDER_MODEL_CALL_ALLOWED=false
FORMAL_APPLY_ALLOWED=false
DATABASE_WRITE_ALLOWED=false
MEMORY_WRITE_ALLOWED=false

1013K_R2 converts the R1 curriculum control profile and target map into big-unit candidate generation envelopes. It is a local-only small package; GitHub upload is deferred until a milestone bundle.
"""
    manifest = f"""# Review Package Manifest

Latest local stage: `{STAGE_ID}`

Includes:

- `{STAGE_DIR_NAME}/candidate_generation_policy_1013K_R2.json`
- `{STAGE_DIR_NAME}/prompt_context_pack_1013K_R2.json`
- `{STAGE_DIR_NAME}/big_unit_candidate_envelope_bundle_1013K_R2.json`
- `{STAGE_DIR_NAME}/candidate_envelope_trace_1013K_R2.json`
- `{STAGE_DIR_NAME}/1013K_R2_result.json`
- `{STAGE_DIR_NAME}/1013K_R2_report.md`
- `backend/xiaobei_ai/prep_room_curriculum_profile_candidate_envelope_1013K_R2.py`
- `scripts/{VALIDATOR_NAME}`

Boundary: local-only small package. No GitHub upload until milestone; no provider/model call, no candidate text generation, no database/memory/Feishu write, no formal apply.

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
    update_local_review_root(output_root)
    source_delta_files = copy_source_delta(root, output_root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_files = [
        stage_dir / "candidate_generation_policy_1013K_R2.json",
        stage_dir / "prompt_context_pack_1013K_R2.json",
        stage_dir / "big_unit_candidate_envelope_bundle_1013K_R2.json",
        stage_dir / "candidate_envelope_trace_1013K_R2.json",
        *source_delta_files,
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ]
    result = build_result(root, output_root, payload, stage_files)
    write_json(stage_dir / "1013K_R2_result.json", result)
    write_text(stage_dir / "1013K_R2_report.md", build_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["validator_pass"]:
        print("ALL_1013K_R2_CURRICULUM_PROFILE_TO_BIG_UNIT_CANDIDATE_ENVELOPE_CHECKS_OK")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
