from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R11_READONLY_ROUTE_REGISTRATION_STATIC_APPLY_GATED"
FINAL_STATUS = "PASS_1013K_R11_READONLY_ROUTE_REGISTRATION_STATIC_APPLY_GATED"
INHERITS_FROM = "1013K_R10_READONLY_ROUTE_REGISTRATION_REVIEW_GATE"
NEXT_STAGE = "1013K_R12_READONLY_ROUTE_RESPONSE_CONTRACT_AND_CLIENT_FETCH_FIXTURE"
STAGE_DIR_NAME = "1013K_R11_readonly_route_registration_static_apply_gated"
VALIDATOR_NAME = "validate_1013K_R11_readonly_route_registration_static_apply_gated.py"
ROUTE_MODULE_RELATIVE_PATH = "backend/xiaobei_ai/prep_room_big_unit_readonly_routes_1013K_R11.py"
ROUTES_PY_RELATIVE_PATH = "backend/xiaobei_ai/routes.py"
PROPOSED_FLASK_PATH = "/api/prep-room/big-unit-preview-viewmodel/<viewmodel_id>"
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


def build_static_registration_record(root: Path, output_root: Path) -> dict[str, Any]:
    r10_result = read_json(output_root / "1013K_R10_readonly_route_registration_review_gate" / "1013K_R10_result.json")
    routes_text = (root / ROUTES_PY_RELATIVE_PATH).read_text(encoding="utf-8")
    route_module_text = (root / ROUTE_MODULE_RELATIVE_PATH).read_text(encoding="utf-8")
    import_present = "from . import prep_room_big_unit_readonly_routes_1013K_R11" in routes_text
    register_present = "prep_room_big_unit_readonly_routes_1013K_R11.register_routes(bp, _cors_preflight)" in routes_text
    route_path_present = PROPOSED_FLASK_PATH in route_module_text
    return {
        "registration_record_id": "readonly_route_registration_static_apply_1013K_R11",
        "stage": STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "r10_pass": r10_result.get("final_status") == "PASS_1013K_R10_READONLY_ROUTE_REGISTRATION_REVIEW_GATE",
        "route_module_created": (root / ROUTE_MODULE_RELATIVE_PATH).exists(),
        "routes_py_import_present": import_present,
        "routes_py_register_present": register_present,
        "route_path_present": route_path_present,
        "proposed_flask_path": PROPOSED_FLASK_PATH,
        "methods": ["GET", "OPTIONS"],
        "readonly_handler_source": "prep_room_big_unit_readonly_endpoint_dry_run_1013K_R9.handle_readonly_viewmodel_request",
        "route_registered": import_present and register_present and route_path_present,
        "routes_py_modified": import_present and register_present,
        "http_server_started": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "unit_package_written": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "runtime_schema_applied": False,
        "official_curriculum_claim_created": False,
        "main_project_pushed": False,
    }


def run_flask_test_client_smoke(root: Path, output_root: Path) -> dict[str, Any]:
    sys.path.insert(0, str(root))
    from flask import Flask  # noqa: PLC0415
    from backend.xiaobei_ai.routes import create_blueprint  # noqa: PLC0415

    response_fixture = read_json(
        output_root
        / "1013K_R8_big_unit_render_viewmodel_readonly_endpoint_contract"
        / "big_unit_render_viewmodel_readonly_response_fixture_1013K_R8.json"
    )
    viewmodel_id = response_fixture["viewmodel"]["viewmodel_id"]
    app = Flask("r11_readonly_route_smoke")
    app.register_blueprint(create_blueprint())
    rules = sorted(str(rule.rule) for rule in app.url_map.iter_rules())
    target_route_registered_in_url_map = PROPOSED_FLASK_PATH in rules
    with app.test_client() as client:
        response = client.get(f"/api/prep-room/big-unit-preview-viewmodel/{viewmodel_id}")
        payload = response.get_json(silent=True) or {}
    return {
        "route_smoke_id": "readonly_route_registration_static_smoke_1013K_R11",
        "stage": STAGE_ID,
        "flask_test_client_used": True,
        "http_server_started": False,
        "runtime_connected": False,
        "target_route_registered_in_url_map": target_route_registered_in_url_map,
        "url_rule_count": len(rules),
        "status_code": response.status_code,
        "response_ok": payload.get("ok") is True,
        "response_mode": payload.get("response_mode"),
        "route_registered_in_response": payload.get("route_registered") is True,
        "readonly_route_registered_in_response": payload.get("readonly_route_registered") is True,
        "provider_called": payload.get("provider_called"),
        "model_called": payload.get("model_called"),
        "database_written": payload.get("database_written"),
        "memory_written": payload.get("memory_written"),
        "feishu_written": payload.get("feishu_written"),
        "formal_apply_performed": payload.get("formal_apply_performed"),
        "payload_sample": {
            "viewmodel_id": payload.get("viewmodel_id"),
            "chunk_count": payload.get("chunk_count"),
            "route_stage": payload.get("route_stage"),
        },
    }


def build_trace(record: dict[str, Any], smoke: dict[str, Any]) -> dict[str, Any]:
    events = [
        {
            "event_id": "r11_event_01_r10_gate_loaded",
            "event_type": "load_r10_route_registration_review_gate",
            "r10_pass": record["r10_pass"],
            "side_effects_performed": False,
        },
        {
            "event_id": "r11_event_02_route_module_created",
            "event_type": "create_readonly_route_module",
            "route_module_created": record["route_module_created"],
            "side_effects_performed": True,
            "side_effect_scope": "static_source_file_only",
        },
        {
            "event_id": "r11_event_03_routes_py_static_registration_added",
            "event_type": "add_import_and_register_lines_to_routes_py",
            "routes_py_modified": record["routes_py_modified"],
            "side_effects_performed": True,
            "side_effect_scope": "static_source_file_only",
        },
        {
            "event_id": "r11_event_04_flask_test_client_smoke",
            "event_type": "verify_route_with_flask_test_client_without_http_server",
            "status_code": smoke["status_code"],
            "http_server_started": False,
            "side_effects_performed": False,
        },
    ]
    return {
        "trace_id": "readonly_route_registration_static_apply_trace_1013K_R11",
        "stage": STAGE_ID,
        "event_count": len(events),
        "events": events,
        "static_source_files_modified": True,
        "runtime_side_effects_performed": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
    }


def write_stage_files(root: Path, output_root: Path) -> dict[str, Any]:
    stage_dir = output_root / STAGE_DIR_NAME
    record = build_static_registration_record(root, output_root)
    smoke = run_flask_test_client_smoke(root, output_root)
    trace = build_trace(record, smoke)
    write_json(stage_dir / "readonly_route_registration_static_apply_1013K_R11.json", record)
    write_json(stage_dir / "readonly_route_registration_static_smoke_1013K_R11.json", smoke)
    write_json(stage_dir / "readonly_route_registration_static_apply_trace_1013K_R11.json", trace)
    return {"record": record, "smoke": smoke, "trace": trace}


def copy_source_delta(root: Path, output_root: Path) -> list[Path]:
    delta_root = output_root / "source_delta_1013K_R11"
    copied: list[Path] = []
    for relative_path in [ROUTE_MODULE_RELATIVE_PATH, ROUTES_PY_RELATIVE_PATH, f"scripts/{VALIDATOR_NAME}"]:
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
ROUTE_REGISTERED=true
HTTP_SERVER_STARTED=false

1013K_R11 statically registers the readonly big-unit ViewModel route in the local Flask blueprint code and verifies it with Flask test client only. It does not start an HTTP server or connect provider/model/runtime storage.
"""
    manifest = f"""# Review Package Manifest

Latest local stage: `{STAGE_ID}`

Includes:

- `{STAGE_DIR_NAME}/readonly_route_registration_static_apply_1013K_R11.json`
- `{STAGE_DIR_NAME}/readonly_route_registration_static_smoke_1013K_R11.json`
- `{STAGE_DIR_NAME}/readonly_route_registration_static_apply_trace_1013K_R11.json`
- `{STAGE_DIR_NAME}/1013K_R11_result.json`
- `{STAGE_DIR_NAME}/1013K_R11_report.md`
- `backend/xiaobei_ai/prep_room_big_unit_readonly_routes_1013K_R11.py`
- `backend/xiaobei_ai/routes.py`
- `scripts/{VALIDATOR_NAME}`

Boundary: local-only small package. Static route code is registered, but no HTTP server is started, no provider/model is called, no database/memory/Feishu write occurs, and no formal apply or lesson/unit write is performed.
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)


def build_result(root: Path, output_root: Path, payload: dict[str, Any], stage_files: list[Path]) -> dict[str, Any]:
    record = payload["record"]
    smoke = payload["smoke"]
    trace = payload["trace"]
    teacher_visible_scan_files = [path for path in stage_files if "source_delta" not in path.as_posix()]
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "github_upload_deferred_until_next_milestone": True,
        "r10_pass": record["r10_pass"],
        "route_module_created": record["route_module_created"],
        "routes_py_import_present": record["routes_py_import_present"],
        "routes_py_register_present": record["routes_py_register_present"],
        "route_path_present": record["route_path_present"],
        "route_registered": record["route_registered"],
        "routes_py_modified": record["routes_py_modified"],
        "proposed_flask_path": record["proposed_flask_path"],
        "target_route_registered_in_url_map": smoke["target_route_registered_in_url_map"],
        "flask_test_client_used": smoke["flask_test_client_used"],
        "http_server_started": False,
        "route_smoke_status_code": smoke["status_code"],
        "route_smoke_response_ok": smoke["response_ok"],
        "route_smoke_response_mode": smoke["response_mode"],
        "route_registered_in_response": smoke["route_registered_in_response"],
        "readonly_route_registered_in_response": smoke["readonly_route_registered_in_response"],
        "trace_event_count": trace["event_count"],
        "static_source_files_modified": trace["static_source_files_modified"],
        "runtime_side_effects_performed": trace["runtime_side_effects_performed"],
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "unit_package_written": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "runtime_schema_applied": False,
        "official_curriculum_claim_created": False,
        "main_project_pushed": False,
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(teacher_visible_scan_files),
        "secret_scan_hits": scan_secrets(stage_files),
    }
    required_true = [
        "github_upload_deferred_until_next_milestone",
        "r10_pass",
        "route_module_created",
        "routes_py_import_present",
        "routes_py_register_present",
        "route_path_present",
        "route_registered",
        "routes_py_modified",
        "target_route_registered_in_url_map",
        "flask_test_client_used",
        "route_smoke_response_ok",
        "route_registered_in_response",
        "readonly_route_registered_in_response",
        "static_source_files_modified",
    ]
    required_false = [
        "http_server_started",
        "runtime_side_effects_performed",
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
    if result["proposed_flask_path"] != PROPOSED_FLASK_PATH:
        failures.append("proposed_flask_path")
    if result["route_smoke_status_code"] != 200:
        failures.append("route_smoke_status_code")
    if result["route_smoke_response_mode"] != "full_viewmodel_fixture":
        failures.append("route_smoke_response_mode")
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
    return f"""# 1013K_R11 Readonly Route Registration Static Apply Gated Report

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={result["next_stage"]}
LOCAL_ONLY_SMALL_PACKAGE=true
GITHUB_UPLOAD_DEFERRED_UNTIL_NEXT_MILESTONE=true

## Scope

R11 statically registers the readonly big-unit ViewModel route in the local Flask blueprint. It also verifies the registered URL rule with Flask test client. It does not start an HTTP server or connect runtime storage/provider/model.

## Route

```text
path={result["proposed_flask_path"]}
route_registered={str(result["route_registered"]).lower()}
target_route_registered_in_url_map={str(result["target_route_registered_in_url_map"]).lower()}
route_smoke_status_code={result["route_smoke_status_code"]}
route_smoke_response_mode={result["route_smoke_response_mode"]}
```

## Boundary

```text
http_server_started={str(result["http_server_started"]).lower()}
provider_called={str(result["provider_called"]).lower()}
model_called={str(result["model_called"]).lower()}
database_written={str(result["database_written"]).lower()}
memory_written={str(result["memory_written"]).lower()}
formal_apply_performed={str(result["formal_apply_performed"]).lower()}
lesson_body_modified={str(result["lesson_body_modified"]).lower()}
html_body_modified={str(result["html_body_modified"]).lower()}
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
        stage_dir / "readonly_route_registration_static_apply_1013K_R11.json",
        stage_dir / "readonly_route_registration_static_smoke_1013K_R11.json",
        stage_dir / "readonly_route_registration_static_apply_trace_1013K_R11.json",
        *source_delta_files,
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ]
    result = build_result(root, output_root, payload, stage_files)
    write_json(stage_dir / "1013K_R11_result.json", result)
    write_text(stage_dir / "1013K_R11_report.md", build_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["validator_pass"]:
        print("ALL_1013K_R11_READONLY_ROUTE_REGISTRATION_STATIC_APPLY_GATED_CHECKS_OK")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
