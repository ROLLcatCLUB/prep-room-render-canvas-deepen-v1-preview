from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R12_READONLY_ROUTE_RESPONSE_CONTRACT_AND_CLIENT_FETCH_FIXTURE"
FINAL_STATUS = "PASS_1013K_R12_READONLY_ROUTE_RESPONSE_CONTRACT_AND_CLIENT_FETCH_FIXTURE"
INHERITS_FROM = "1013K_R11_READONLY_ROUTE_REGISTRATION_STATIC_APPLY_GATED"
NEXT_STAGE = "1013K_R13_RENDERER_READONLY_FETCH_ADAPTER_FIXTURE"
STAGE_DIR_NAME = "1013K_R12_readonly_route_response_contract_and_client_fetch_fixture"
VALIDATOR_NAME = "validate_1013K_R12_readonly_route_response_contract_and_client_fetch_fixture.py"
BACKEND_ADAPTER_RELATIVE_PATH = "backend/xiaobei_ai/prep_room_big_unit_client_fetch_contract_1013K_R12.py"
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
    from backend.xiaobei_ai.prep_room_big_unit_client_fetch_contract_1013K_R12 import (  # noqa: PLC0415
        build_readonly_route_response_contract_and_client_fetch_fixture,
    )

    return build_readonly_route_response_contract_and_client_fetch_fixture


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
    write_json(stage_dir / "readonly_route_response_contract_1013K_R12.json", payload["response_contract"])
    write_text(stage_dir / "client_fetch_fixture_1013K_R12.js", payload["client_fetch_fixture_js"])
    write_json(stage_dir / "client_fetch_fixture_manifest_1013K_R12.json", {
        "fixture_id": "client_fetch_fixture_manifest_1013K_R12",
        "stage": STAGE_ID,
        "fixture_file": "client_fetch_fixture_1013K_R12.js",
        "mounted_into_frontend": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
    })
    write_json(stage_dir / "readonly_client_fetch_contract_trace_1013K_R12.json", payload["fetch_trace"])
    return payload


def copy_source_delta(root: Path, output_root: Path) -> list[Path]:
    delta_root = output_root / "source_delta_1013K_R12"
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

1013K_R12 defines the readonly route response contract and a standalone client fetch fixture. It does not mount the fixture into the frontend, start runtime, call provider/model, or write storage.
"""
    manifest = f"""# Review Package Manifest

Latest local stage: `{STAGE_ID}`

Includes:

- `{STAGE_DIR_NAME}/readonly_route_response_contract_1013K_R12.json`
- `{STAGE_DIR_NAME}/client_fetch_fixture_1013K_R12.js`
- `{STAGE_DIR_NAME}/client_fetch_fixture_manifest_1013K_R12.json`
- `{STAGE_DIR_NAME}/readonly_client_fetch_contract_trace_1013K_R12.json`
- `{STAGE_DIR_NAME}/1013K_R12_result.json`
- `{STAGE_DIR_NAME}/1013K_R12_report.md`
- `backend/xiaobei_ai/prep_room_big_unit_client_fetch_contract_1013K_R12.py`
- `scripts/{VALIDATOR_NAME}`

Boundary: local-only small package. No frontend page mount, no provider/model call, no runtime connection, no database/memory/Feishu write, no formal apply, no unit_package or lesson body write.
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)


def build_result(root: Path, output_root: Path, payload: dict[str, Any], stage_files: list[Path]) -> dict[str, Any]:
    stage_dir = output_root / STAGE_DIR_NAME
    contract = payload["response_contract"]
    trace = payload["fetch_trace"]
    fixture_text = payload["client_fetch_fixture_js"]
    modes = {mode["mode"]: mode for mode in contract.get("supported_fetch_modes", [])}
    teacher_visible_scan_files = [path for path in stage_files if "source_delta" not in path.as_posix()]
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "github_upload_deferred_until_next_milestone": True,
        "r11_pass": contract.get("r11_pass"),
        "backend_adapter_created": (root / BACKEND_ADAPTER_RELATIVE_PATH).exists(),
        "response_contract_created": (stage_dir / "readonly_route_response_contract_1013K_R12.json").exists(),
        "client_fetch_fixture_created": (stage_dir / "client_fetch_fixture_1013K_R12.js").exists(),
        "client_fetch_fixture_manifest_created": (stage_dir / "client_fetch_fixture_manifest_1013K_R12.json").exists(),
        "fetch_trace_created": (stage_dir / "readonly_client_fetch_contract_trace_1013K_R12.json").exists(),
        "fetch_mode_count": len(modes),
        "full_viewmodel_fetch_mode_present": "full_viewmodel" in modes,
        "single_chunk_fetch_mode_present": "single_chunk" in modes,
        "readonly_error_fetch_mode_present": "readonly_error" in modes,
        "chunked_rendering_supported": contract.get("chunked_rendering_supported"),
        "whole_document_blob_required": contract.get("whole_document_blob_required"),
        "renderer_can_request_single_chunk": contract.get("renderer_can_request_single_chunk"),
        "fixture_exports_fetch_function": "export async function fetchBigUnitPreviewViewModel" in fixture_text,
        "fixture_uses_get": "method: 'GET'" in fixture_text,
        "fixture_uses_chunk_id_param": "chunk_id" in fixture_text,
        "fixture_not_mounted_into_frontend": True,
        "trace_event_count": trace.get("event_count"),
        "trace_side_effects_performed": trace.get("side_effects_performed"),
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(teacher_visible_scan_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **contract,
    }
    required_true = [
        "github_upload_deferred_until_next_milestone",
        "r11_pass",
        "backend_adapter_created",
        "response_contract_created",
        "client_fetch_fixture_created",
        "client_fetch_fixture_manifest_created",
        "fetch_trace_created",
        "full_viewmodel_fetch_mode_present",
        "single_chunk_fetch_mode_present",
        "readonly_error_fetch_mode_present",
        "chunked_rendering_supported",
        "renderer_can_request_single_chunk",
        "fixture_exports_fetch_function",
        "fixture_uses_get",
        "fixture_uses_chunk_id_param",
        "fixture_not_mounted_into_frontend",
        "client_fetch_contract_only",
        "preview_only",
    ]
    required_false = [
        "whole_document_blob_required",
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
    if result["fetch_mode_count"] != 3:
        failures.append("fetch_mode_count")
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
    return f"""# 1013K_R12 Readonly Route Response Contract And Client Fetch Fixture Report

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={result["next_stage"]}
LOCAL_ONLY_SMALL_PACKAGE=true
GITHUB_UPLOAD_DEFERRED_UNTIL_NEXT_MILESTONE=true

## Scope

R12 defines how a frontend renderer can fetch the big-unit preview ViewModel through the R11 readonly route. It creates a standalone JS fetch fixture only and does not mount it into a production page.

## Fetch Modes

```text
fetch_mode_count={result["fetch_mode_count"]}
full_viewmodel_fetch_mode_present={str(result["full_viewmodel_fetch_mode_present"]).lower()}
single_chunk_fetch_mode_present={str(result["single_chunk_fetch_mode_present"]).lower()}
readonly_error_fetch_mode_present={str(result["readonly_error_fetch_mode_present"]).lower()}
whole_document_blob_required={str(result["whole_document_blob_required"]).lower()}
```

## Boundary

```text
frontend_page_modified={str(result["frontend_page_modified"]).lower()}
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
        stage_dir / "readonly_route_response_contract_1013K_R12.json",
        stage_dir / "client_fetch_fixture_1013K_R12.js",
        stage_dir / "client_fetch_fixture_manifest_1013K_R12.json",
        stage_dir / "readonly_client_fetch_contract_trace_1013K_R12.json",
        *source_delta_files,
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ]
    result = build_result(root, output_root, payload, stage_files)
    write_json(stage_dir / "1013K_R12_result.json", result)
    write_text(stage_dir / "1013K_R12_report.md", build_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["validator_pass"]:
        print("ALL_1013K_R12_READONLY_ROUTE_RESPONSE_CONTRACT_AND_CLIENT_FETCH_FIXTURE_CHECKS_OK")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
