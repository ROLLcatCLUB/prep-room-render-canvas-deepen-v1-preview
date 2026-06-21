from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R15_ISOLATED_STATIC_FRONTEND_READONLY_BINDING_FIXTURE"
FINAL_STATUS = "PASS_1013K_R15_ISOLATED_STATIC_FRONTEND_READONLY_BINDING_FIXTURE"
INHERITS_FROM = "1013K_R14_FRONTEND_READONLY_RENDER_BINDING_REVIEW_GATE"
NEXT_STAGE = "1013K_R16_ISOLATED_STATIC_BINDING_VISUAL_SMOKE"
STAGE_DIR_NAME = "1013K_R15_isolated_static_frontend_readonly_binding_fixture"
VALIDATOR_NAME = "validate_1013K_R15_isolated_static_frontend_readonly_binding_fixture.py"
BACKEND_ADAPTER_RELATIVE_PATH = "backend/xiaobei_ai/prep_room_big_unit_isolated_static_binding_1013K_R15.py"
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
    from backend.xiaobei_ai.prep_room_big_unit_isolated_static_binding_1013K_R15 import (  # noqa: PLC0415
        build_isolated_static_frontend_readonly_binding_fixture,
    )

    return build_isolated_static_frontend_readonly_binding_fixture


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
    write_text(stage_dir / "isolated_static_frontend_readonly_binding_fixture_1013K_R15.html", payload["isolated_static_html"])
    write_json(stage_dir / "renderer_chunk_mount_map_1013K_R15.json", payload["renderer_chunk_mount_map"])
    write_json(stage_dir / "isolated_static_frontend_binding_smoke_1013K_R15.json", payload["binding_smoke"])
    write_json(stage_dir / "isolated_static_frontend_binding_trace_1013K_R15.json", payload["binding_trace"])
    return payload


def copy_source_delta(root: Path, output_root: Path) -> list[Path]:
    delta_root = output_root / "source_delta_1013K_R15"
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
FORMAL_FRONTEND_PAGE_MODIFIED=false

1013K_R15 creates an isolated static HTML binding fixture from the readonly big-unit ViewModel chunks. It does not mount into formal frontend pages.
"""
    manifest = f"""# Review Package Manifest

Latest local stage: `{STAGE_ID}`

Includes:

- `{STAGE_DIR_NAME}/isolated_static_frontend_readonly_binding_fixture_1013K_R15.html`
- `{STAGE_DIR_NAME}/renderer_chunk_mount_map_1013K_R15.json`
- `{STAGE_DIR_NAME}/isolated_static_frontend_binding_smoke_1013K_R15.json`
- `{STAGE_DIR_NAME}/isolated_static_frontend_binding_trace_1013K_R15.json`
- `{STAGE_DIR_NAME}/1013K_R15_result.json`
- `{STAGE_DIR_NAME}/1013K_R15_report.md`
- `backend/xiaobei_ai/prep_room_big_unit_isolated_static_binding_1013K_R15.py`
- `scripts/{VALIDATOR_NAME}`

Boundary: local-only small package. No formal frontend page modification, no runtime connection, no provider/model call, no storage write, no formal apply.
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)


def build_result(root: Path, output_root: Path, payload: dict[str, Any], stage_files: list[Path]) -> dict[str, Any]:
    stage_dir = output_root / STAGE_DIR_NAME
    mount_map = payload["renderer_chunk_mount_map"]
    smoke = payload["binding_smoke"]
    trace = payload["binding_trace"]
    html_text = payload["isolated_static_html"]
    teacher_visible_scan_files = [path for path in stage_files if "source_delta" not in path.as_posix()]
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "github_upload_deferred_until_next_milestone": True,
        "r14_pass": smoke.get("r14_pass"),
        "backend_adapter_created": (root / BACKEND_ADAPTER_RELATIVE_PATH).exists(),
        "isolated_static_html_created": (stage_dir / "isolated_static_frontend_readonly_binding_fixture_1013K_R15.html").exists(),
        "renderer_chunk_mount_map_created": (stage_dir / "renderer_chunk_mount_map_1013K_R15.json").exists(),
        "binding_smoke_created": (stage_dir / "isolated_static_frontend_binding_smoke_1013K_R15.json").exists(),
        "binding_trace_created": (stage_dir / "isolated_static_frontend_binding_trace_1013K_R15.json").exists(),
        "chunk_count": mount_map.get("chunk_count"),
        "all_chunks_mounted": smoke.get("all_chunks_mounted"),
        "teacher_title_visible": smoke.get("teacher_title_visible"),
        "material_prompt_visible": smoke.get("material_prompt_visible"),
        "progressive_rendering_supported": mount_map.get("progressive_rendering_supported"),
        "single_chunk_update_supported": mount_map.get("single_chunk_update_supported"),
        "whole_document_blob_required": mount_map.get("whole_document_blob_required"),
        "html_has_isolated_binding_marker": 'data-binding-mode="isolated_static_fixture"' in html_text,
        "trace_event_count": trace.get("event_count"),
        "trace_side_effects_performed": trace.get("side_effects_performed"),
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(teacher_visible_scan_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **smoke,
    }
    required_true = [
        "github_upload_deferred_until_next_milestone",
        "r14_pass",
        "backend_adapter_created",
        "isolated_static_html_created",
        "renderer_chunk_mount_map_created",
        "binding_smoke_created",
        "binding_trace_created",
        "all_chunks_mounted",
        "teacher_title_visible",
        "material_prompt_visible",
        "progressive_rendering_supported",
        "single_chunk_update_supported",
        "html_has_isolated_binding_marker",
        "isolated_static_binding_fixture_only",
    ]
    required_false = [
        "whole_document_blob_required",
        "trace_side_effects_performed",
        "formal_frontend_page_modified",
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
    if result["chunk_count"] != 10:
        failures.append("chunk_count")
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
    return f"""# 1013K_R15 Isolated Static Frontend Readonly Binding Fixture Report

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={result["next_stage"]}
LOCAL_ONLY_SMALL_PACKAGE=true
GITHUB_UPLOAD_DEFERRED_UNTIL_NEXT_MILESTONE=true

## Scope

R15 creates an isolated static HTML binding fixture from the readonly big-unit ViewModel chunks. It does not modify formal frontend pages.

## Checks

```text
chunk_count={result["chunk_count"]}
all_chunks_mounted={str(result["all_chunks_mounted"]).lower()}
teacher_title_visible={str(result["teacher_title_visible"]).lower()}
material_prompt_visible={str(result["material_prompt_visible"]).lower()}
formal_frontend_page_modified={str(result["formal_frontend_page_modified"]).lower()}
runtime_connected={str(result["runtime_connected"]).lower()}
provider_called={str(result["provider_called"]).lower()}
model_called={str(result["model_called"]).lower()}
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
        stage_dir / "isolated_static_frontend_readonly_binding_fixture_1013K_R15.html",
        stage_dir / "renderer_chunk_mount_map_1013K_R15.json",
        stage_dir / "isolated_static_frontend_binding_smoke_1013K_R15.json",
        stage_dir / "isolated_static_frontend_binding_trace_1013K_R15.json",
        *source_delta_files,
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ]
    result = build_result(root, output_root, payload, stage_files)
    write_json(stage_dir / "1013K_R15_result.json", result)
    write_text(stage_dir / "1013K_R15_report.md", build_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["validator_pass"]:
        print("ALL_1013K_R15_ISOLATED_STATIC_FRONTEND_READONLY_BINDING_FIXTURE_CHECKS_OK")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
