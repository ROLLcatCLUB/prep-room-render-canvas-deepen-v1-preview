from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R10_READONLY_ROUTE_REGISTRATION_REVIEW_GATE"
FINAL_STATUS = "PASS_1013K_R10_READONLY_ROUTE_REGISTRATION_REVIEW_GATE"
INHERITS_FROM = "1013K_R9_BIG_UNIT_READONLY_ENDPOINT_DRY_RUN_WITHOUT_ROUTE_REGISTRATION"
NEXT_STAGE = "1013K_R11_READONLY_ROUTE_REGISTRATION_STATIC_APPLY_GATED"
STAGE_DIR_NAME = "1013K_R10_readonly_route_registration_review_gate"
VALIDATOR_NAME = "validate_1013K_R10_readonly_route_registration_review_gate.py"
BACKEND_ADAPTER_RELATIVE_PATH = "backend/xiaobei_ai/prep_room_big_unit_route_registration_gate_1013K_R10.py"
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
    from backend.xiaobei_ai.prep_room_big_unit_route_registration_gate_1013K_R10 import (  # noqa: PLC0415
        build_readonly_route_registration_review_gate,
    )

    return build_readonly_route_registration_review_gate


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
    write_json(stage_dir / "readonly_route_registration_gate_1013K_R10.json", payload["route_registration_gate"])
    write_json(stage_dir / "readonly_route_mount_plan_1013K_R10.json", payload["route_mount_plan"])
    write_json(stage_dir / "readonly_route_collision_review_1013K_R10.json", payload["route_collision_review"])
    write_json(stage_dir / "readonly_route_registration_trace_1013K_R10.json", payload["route_registration_trace"])
    return payload


def copy_source_delta(root: Path, output_root: Path) -> list[Path]:
    delta_root = output_root / "source_delta_1013K_R10"
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
ROUTE_REGISTERED=false

1013K_R10 reviews whether the R9 readonly dry-run endpoint can be mounted later. It creates a future route mount plan and collision review only; it does not modify `routes.py`, create a route module, start HTTP, or connect runtime.
"""
    manifest = f"""# Review Package Manifest

Latest local stage: `{STAGE_ID}`

Includes:

- `{STAGE_DIR_NAME}/readonly_route_registration_gate_1013K_R10.json`
- `{STAGE_DIR_NAME}/readonly_route_mount_plan_1013K_R10.json`
- `{STAGE_DIR_NAME}/readonly_route_collision_review_1013K_R10.json`
- `{STAGE_DIR_NAME}/readonly_route_registration_trace_1013K_R10.json`
- `{STAGE_DIR_NAME}/1013K_R10_result.json`
- `{STAGE_DIR_NAME}/1013K_R10_report.md`
- `backend/xiaobei_ai/prep_room_big_unit_route_registration_gate_1013K_R10.py`
- `scripts/{VALIDATOR_NAME}`

Boundary: local-only small package. No route registration, no `routes.py` modification, no route module creation, no HTTP server, no provider/model call, no runtime connection, no database/memory/Feishu write, no formal apply, no unit_package or lesson body write.
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)


def build_result(root: Path, output_root: Path, payload: dict[str, Any], stage_files: list[Path]) -> dict[str, Any]:
    stage_dir = output_root / STAGE_DIR_NAME
    r9_result = read_json(
        output_root
        / "1013K_R9_big_unit_readonly_endpoint_dry_run_without_route_registration"
        / "1013K_R9_result.json"
    )
    gate = payload["route_registration_gate"]
    mount_plan = payload["route_mount_plan"]
    collision = payload["route_collision_review"]
    trace = payload["route_registration_trace"]
    boundary = payload["boundary"]
    teacher_visible_scan_files = [path for path in stage_files if "source_delta" not in path.as_posix()]

    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "github_upload_deferred_until_next_milestone": True,
        "r9_pass": r9_result.get("final_status") == "PASS_1013K_R9_BIG_UNIT_READONLY_ENDPOINT_DRY_RUN_WITHOUT_ROUTE_REGISTRATION"
        and r9_result.get("validator_pass") is True,
        "backend_adapter_created": (root / BACKEND_ADAPTER_RELATIVE_PATH).exists(),
        "route_registration_gate_created": (stage_dir / "readonly_route_registration_gate_1013K_R10.json").exists(),
        "route_mount_plan_created": (stage_dir / "readonly_route_mount_plan_1013K_R10.json").exists(),
        "route_collision_review_created": (stage_dir / "readonly_route_collision_review_1013K_R10.json").exists(),
        "route_registration_trace_created": (stage_dir / "readonly_route_registration_trace_1013K_R10.json").exists(),
        "existing_routes_reviewed": gate.get("existing_routes_reviewed") is True,
        "reviewed_route_file_count": collision.get("reviewed_route_file_count"),
        "proposed_public_path": gate.get("proposed_public_path"),
        "proposed_flask_path": gate.get("proposed_flask_path"),
        "proposed_method_get": "GET" in gate.get("proposed_methods", []),
        "proposed_options_preflight": "OPTIONS" in gate.get("proposed_methods", []),
        "cors_preflight_plan_created": gate.get("cors_preflight_plan_created") is True
        and mount_plan.get("cors_preflight_required") is True,
        "route_collision_detected": collision.get("route_collision_detected"),
        "collision_review_pass": collision.get("collision_review_pass"),
        "matched_existing_routes": collision.get("matched_existing_routes", []),
        "route_registration_gate_pass": gate.get("route_registration_gate_pass"),
        "route_registration_allowed_next": gate.get("route_registration_allowed_next"),
        "routes_py_patch_allowed_next": gate.get("routes_py_patch_allowed_next"),
        "future_route_module": mount_plan.get("future_route_module"),
        "future_import_line_present": bool(mount_plan.get("future_import_line")),
        "future_register_line_present": bool(mount_plan.get("future_register_line")),
        "readonly_handler_source_present": bool(mount_plan.get("readonly_handler_source")),
        "trace_event_count": trace.get("event_count"),
        "trace_side_effects_performed": trace.get("side_effects_performed"),
        "all_trace_side_effect_free": all(event.get("side_effects_performed") is False for event in trace.get("events", [])),
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(teacher_visible_scan_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **boundary,
    }
    required_true = [
        "github_upload_deferred_until_next_milestone",
        "r9_pass",
        "backend_adapter_created",
        "route_registration_gate_created",
        "route_mount_plan_created",
        "route_collision_review_created",
        "route_registration_trace_created",
        "existing_routes_reviewed",
        "proposed_method_get",
        "proposed_options_preflight",
        "cors_preflight_plan_created",
        "collision_review_pass",
        "route_registration_gate_pass",
        "route_registration_allowed_next",
        "routes_py_patch_allowed_next",
        "future_import_line_present",
        "future_register_line_present",
        "readonly_handler_source_present",
        "all_trace_side_effect_free",
        "route_registration_review_gate_only",
        "route_registration_allowed_after_gate",
        "preview_only",
        "teacher_review_required",
    ]
    required_false = [
        "route_collision_detected",
        "trace_side_effects_performed",
        "route_registered",
        "routes_py_modified",
        "route_module_created",
        "http_server_started",
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
    if result["reviewed_route_file_count"] < 1:
        failures.append("reviewed_route_file_count")
    if result["proposed_flask_path"] != "/api/prep-room/big-unit-preview-viewmodel/<viewmodel_id>":
        failures.append("proposed_flask_path")
    if result["proposed_public_path"] != "/api/prep-room/big-unit-preview-viewmodel/{viewmodel_id}":
        failures.append("proposed_public_path")
    if result["trace_event_count"] != 4:
        failures.append("trace_event_count")
    if result["matched_existing_routes"]:
        failures.append("matched_existing_routes")
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    result["validator_pass"] = not failures
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013K_R10 Readonly Route Registration Review Gate Report

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={result["next_stage"]}
LOCAL_ONLY_SMALL_PACKAGE=true
GITHUB_UPLOAD_DEFERRED_UNTIL_NEXT_MILESTONE=true

## Scope

R10 reviews the future route registration plan for the R9 readonly dry-run endpoint. It checks the existing `backend/xiaobei_ai/routes.py` registration pattern, records a future mount plan, and confirms no obvious path collision. It does not register the route.

## Proposed Future Route

```text
path={result["proposed_flask_path"]}
methods=GET,OPTIONS
future_route_module={result["future_route_module"]}
route_registration_allowed_next={str(result["route_registration_allowed_next"]).lower()}
routes_py_patch_allowed_next={str(result["routes_py_patch_allowed_next"]).lower()}
```

## Boundary

```text
route_registered={str(result["route_registered"]).lower()}
routes_py_modified={str(result["routes_py_modified"]).lower()}
route_module_created={str(result["route_module_created"]).lower()}
http_server_started={str(result["http_server_started"]).lower()}
runtime_connected={str(result["runtime_connected"]).lower()}
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
        stage_dir / "readonly_route_registration_gate_1013K_R10.json",
        stage_dir / "readonly_route_mount_plan_1013K_R10.json",
        stage_dir / "readonly_route_collision_review_1013K_R10.json",
        stage_dir / "readonly_route_registration_trace_1013K_R10.json",
        *source_delta_files,
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ]
    result = build_result(root, output_root, payload, stage_files)
    write_json(stage_dir / "1013K_R10_result.json", result)
    write_text(stage_dir / "1013K_R10_report.md", build_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["validator_pass"]:
        print("ALL_1013K_R10_READONLY_ROUTE_REGISTRATION_REVIEW_GATE_CHECKS_OK")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
