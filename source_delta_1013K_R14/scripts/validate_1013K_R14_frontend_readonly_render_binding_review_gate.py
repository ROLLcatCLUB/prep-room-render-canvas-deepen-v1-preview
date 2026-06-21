from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R14_FRONTEND_READONLY_RENDER_BINDING_REVIEW_GATE"
FINAL_STATUS = "PASS_1013K_R14_FRONTEND_READONLY_RENDER_BINDING_REVIEW_GATE"
INHERITS_FROM = "1013K_M3_READONLY_ROUTE_CLIENT_RENDERER_MILESTONE_PACKAGE"
NEXT_STAGE = "1013K_R15_ISOLATED_STATIC_FRONTEND_READONLY_BINDING_FIXTURE"
STAGE_DIR_NAME = "1013K_R14_frontend_readonly_render_binding_review_gate"
VALIDATOR_NAME = "validate_1013K_R14_frontend_readonly_render_binding_review_gate.py"
BACKEND_ADAPTER_RELATIVE_PATH = "backend/xiaobei_ai/prep_room_big_unit_frontend_binding_gate_1013K_R14.py"
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


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_backend_adapter(root: Path):
    sys.path.insert(0, str(root))
    from backend.xiaobei_ai.prep_room_big_unit_frontend_binding_gate_1013K_R14 import (  # noqa: PLC0415
        build_frontend_readonly_render_binding_review_gate,
    )

    return build_frontend_readonly_render_binding_review_gate


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
    write_json(stage_dir / "frontend_readonly_render_binding_gate_1013K_R14.json", payload["frontend_binding_gate"])
    write_json(stage_dir / "frontend_surface_inventory_1013K_R14.json", payload["frontend_surface_inventory"])
    write_json(stage_dir / "frontend_readonly_binding_plan_1013K_R14.json", payload["binding_plan"])
    write_json(stage_dir / "frontend_readonly_binding_risk_review_1013K_R14.json", payload["binding_risk_review"])
    write_json(stage_dir / "frontend_readonly_binding_trace_1013K_R14.json", payload["binding_trace"])
    return payload


def copy_source_delta(root: Path, output_root: Path) -> list[Path]:
    delta_root = output_root / "source_delta_1013K_R14"
    copied: list[Path] = []
    for relative_path in [BACKEND_ADAPTER_RELATIVE_PATH, f"scripts/{VALIDATOR_NAME}"]:
        src = root / relative_path
        dst = delta_root / relative_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(dst)
    return copied


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
FRONTEND_PAGE_MODIFIED=false
MAIN_FRONTEND_MOUNT_ALLOWED=false

1013K_R14 reviews frontend binding targets for the readonly big-unit renderer. It allows only an isolated static binding fixture next and forbids direct modification of formal frontend pages.
"""
    manifest = f"""# Review Package Manifest

Latest local stage: `{STAGE_ID}`

Includes:

- `{STAGE_DIR_NAME}/frontend_readonly_render_binding_gate_1013K_R14.json`
- `{STAGE_DIR_NAME}/frontend_surface_inventory_1013K_R14.json`
- `{STAGE_DIR_NAME}/frontend_readonly_binding_plan_1013K_R14.json`
- `{STAGE_DIR_NAME}/frontend_readonly_binding_risk_review_1013K_R14.json`
- `{STAGE_DIR_NAME}/frontend_readonly_binding_trace_1013K_R14.json`
- `{STAGE_DIR_NAME}/1013K_R14_result.json`
- `{STAGE_DIR_NAME}/1013K_R14_report.md`
- `backend/xiaobei_ai/prep_room_big_unit_frontend_binding_gate_1013K_R14.py`
- `scripts/{VALIDATOR_NAME}`

Boundary: local-only small package. No formal frontend page modification, no runtime connection, no provider/model call, no storage write, no formal apply.
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)


def build_result(root: Path, output_root: Path, payload: dict[str, Any], stage_files: list[Path]) -> dict[str, Any]:
    stage_dir = output_root / STAGE_DIR_NAME
    gate = payload["frontend_binding_gate"]
    inventory = payload["frontend_surface_inventory"]
    plan = payload["binding_plan"]
    risk = payload["binding_risk_review"]
    trace = payload["binding_trace"]
    teacher_visible_scan_files = [path for path in stage_files if "source_delta" not in path.as_posix()]
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "github_upload_deferred_until_next_milestone": True,
        "m3_pass": gate.get("m3_pass"),
        "r12_fetch_contract_pass": gate.get("r12_fetch_contract_pass"),
        "r13_renderer_adapter_pass": gate.get("r13_renderer_adapter_pass"),
        "backend_adapter_created": (root / BACKEND_ADAPTER_RELATIVE_PATH).exists(),
        "frontend_binding_gate_created": (stage_dir / "frontend_readonly_render_binding_gate_1013K_R14.json").exists(),
        "frontend_surface_inventory_created": (stage_dir / "frontend_surface_inventory_1013K_R14.json").exists(),
        "binding_plan_created": (stage_dir / "frontend_readonly_binding_plan_1013K_R14.json").exists(),
        "binding_risk_review_created": (stage_dir / "frontend_readonly_binding_risk_review_1013K_R14.json").exists(),
        "binding_trace_created": (stage_dir / "frontend_readonly_binding_trace_1013K_R14.json").exists(),
        "formal_frontend_candidate_count": inventory.get("formal_frontend_candidate_count"),
        "static_fixture_candidate_count": inventory.get("static_fixture_candidate_count"),
        "formal_frontend_direct_mount_recommended": inventory.get("formal_frontend_direct_mount_recommended"),
        "isolated_static_fixture_recommended": inventory.get("isolated_static_fixture_recommended"),
        "recommended_binding_mode": plan.get("recommended_binding_mode"),
        "main_frontend_mount_allowed": plan.get("main_frontend_mount_allowed"),
        "isolated_static_binding_allowed_next": plan.get("isolated_static_binding_allowed_next"),
        "frontend_binding_gate_pass": gate.get("frontend_binding_gate_pass"),
        "risk_review_pass": risk.get("risk_review_pass"),
        "trace_event_count": trace.get("event_count"),
        "trace_side_effects_performed": trace.get("side_effects_performed"),
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(teacher_visible_scan_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **gate,
    }
    required_true = [
        "github_upload_deferred_until_next_milestone",
        "m3_pass",
        "r12_fetch_contract_pass",
        "r13_renderer_adapter_pass",
        "backend_adapter_created",
        "frontend_binding_gate_created",
        "frontend_surface_inventory_created",
        "binding_plan_created",
        "binding_risk_review_created",
        "binding_trace_created",
        "isolated_static_fixture_recommended",
        "isolated_static_binding_allowed_next",
        "frontend_binding_gate_pass",
        "risk_review_pass",
        "frontend_binding_review_gate_only",
    ]
    required_false = [
        "formal_frontend_direct_mount_recommended",
        "main_frontend_mount_allowed",
        "trace_side_effects_performed",
        "frontend_page_modified",
        "runtime_connected",
        "http_server_started",
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
    if result["formal_frontend_candidate_count"] < 1:
        failures.append("formal_frontend_candidate_count")
    if result["static_fixture_candidate_count"] < 1:
        failures.append("static_fixture_candidate_count")
    if result["recommended_binding_mode"] != "isolated_static_fixture_first":
        failures.append("recommended_binding_mode")
    if result["trace_event_count"] != 3:
        failures.append("trace_event_count")
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    result["validator_pass"] = not failures
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013K_R14 Frontend Readonly Render Binding Review Gate Report

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={result["next_stage"]}
LOCAL_ONLY_SMALL_PACKAGE=true
GITHUB_UPLOAD_DEFERRED_UNTIL_NEXT_MILESTONE=true

## Decision

R14 does not allow direct formal frontend mounting yet. It allows only an isolated static binding fixture next, using R12 fetch and R13 renderer adapter fixtures.

```text
recommended_binding_mode={result["recommended_binding_mode"]}
formal_frontend_candidate_count={result["formal_frontend_candidate_count"]}
static_fixture_candidate_count={result["static_fixture_candidate_count"]}
main_frontend_mount_allowed={str(result["main_frontend_mount_allowed"]).lower()}
isolated_static_binding_allowed_next={str(result["isolated_static_binding_allowed_next"]).lower()}
frontend_page_modified={str(result["frontend_page_modified"]).lower()}
```

## Boundary

```text
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
        stage_dir / "frontend_readonly_render_binding_gate_1013K_R14.json",
        stage_dir / "frontend_surface_inventory_1013K_R14.json",
        stage_dir / "frontend_readonly_binding_plan_1013K_R14.json",
        stage_dir / "frontend_readonly_binding_risk_review_1013K_R14.json",
        stage_dir / "frontend_readonly_binding_trace_1013K_R14.json",
        *source_delta_files,
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ]
    result = build_result(root, output_root, payload, stage_files)
    write_json(stage_dir / "1013K_R14_result.json", result)
    write_text(stage_dir / "1013K_R14_report.md", build_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["validator_pass"]:
        print("ALL_1013K_R14_FRONTEND_READONLY_RENDER_BINDING_REVIEW_GATE_CHECKS_OK")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
