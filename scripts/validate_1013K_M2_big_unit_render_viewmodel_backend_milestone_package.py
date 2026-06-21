from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_M2_BIG_UNIT_RENDER_VIEWMODEL_BACKEND_MILESTONE_PACKAGE"
FINAL_STATUS = "PASS_1013K_M2_BIG_UNIT_RENDER_VIEWMODEL_BACKEND_MILESTONE_PACKAGE"
INHERITS_FROM = "1013K_R8_BIG_UNIT_RENDER_VIEWMODEL_READONLY_ENDPOINT_CONTRACT"
NEXT_STAGE = "1013K_R9_BIG_UNIT_READONLY_ENDPOINT_DRY_RUN_WITHOUT_ROUTE_REGISTRATION"
STAGE_DIR_NAME = "1013K_M2_big_unit_render_viewmodel_backend_milestone_package"

STAGE_CHAIN = [
    {
        "stage": "1013K_R5_BIG_UNIT_REVIEW_ACTION_STATE_DRY_RUN",
        "dir": "1013K_R5_big_unit_review_action_state_dry_run",
        "result": "1013K_R5_result.json",
        "role": "simulate teacher review actions as preview-only state",
    },
    {
        "stage": "1013K_R6_BIG_UNIT_REVIEW_ACTION_STATE_TO_PREVIEW_SURFACE_FIXTURE",
        "dir": "1013K_R6_big_unit_review_action_state_to_preview_surface_fixture",
        "result": "1013K_R6_result.json",
        "role": "turn accepted preview state into renderable preview surface",
    },
    {
        "stage": "1013K_R7_BIG_UNIT_PREVIEW_SURFACE_TO_RENDER_VIEWMODEL_CONTRACT",
        "dir": "1013K_R7_big_unit_preview_surface_to_render_viewmodel_contract",
        "result": "1013K_R7_result.json",
        "role": "define chunked render ViewModel contract and fixture",
    },
    {
        "stage": "1013K_R8_BIG_UNIT_RENDER_VIEWMODEL_READONLY_ENDPOINT_CONTRACT",
        "dir": "1013K_R8_big_unit_render_viewmodel_readonly_endpoint_contract",
        "result": "1013K_R8_result.json",
        "role": "define future readonly endpoint contract without registering route",
    },
]

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


def scan_secret_hits(paths: list[Path]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append({"path": str(path), "pattern": pattern.pattern})
    return hits


def load_stage_results(output_root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    stage_results: list[dict[str, Any]] = []
    missing: list[str] = []
    for item in STAGE_CHAIN:
        result_path = output_root / item["dir"] / item["result"]
        if not result_path.exists():
            missing.append(str(result_path))
            continue
        result = read_json(result_path)
        stage_results.append(
            {
                **item,
                "path": str(result_path.relative_to(output_root)),
                "final_status": result.get("final_status"),
                "validator_pass": result.get("validator_pass"),
                "next_stage": result.get("next_stage"),
                "failed_checks": result.get("failed_checks", []),
                "provider_called": result.get("provider_called", False),
                "model_called": result.get("model_called", False),
                "database_written": result.get("database_written", False),
                "memory_written": result.get("memory_written", False),
                "feishu_written": result.get("feishu_written", False),
                "formal_apply_performed": result.get("formal_apply_performed", False),
                "route_registered": result.get("route_registered", False),
                "main_project_pushed": result.get("main_project_pushed", False),
            }
        )
    return stage_results, missing


def build_index(output_root: Path, stage_results: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "milestone_id": "big_unit_render_viewmodel_backend_milestone_1013K_M2",
        "stage": STAGE_ID,
        "created_at": now(),
        "purpose": (
            "Archive the local R5-R8 backend chain from teacher review action state to "
            "chunked render ViewModel and future readonly endpoint contract."
        ),
        "stage_chain": stage_results,
        "review_entrypoints": {
            "latest_review_entry": "LATEST_REVIEW_ENTRY.md",
            "manifest": "REVIEW_PACKAGE_MANIFEST.md",
            "milestone_report": f"{STAGE_DIR_NAME}/1013K_M2_report.md",
            "milestone_result": f"{STAGE_DIR_NAME}/1013K_M2_result.json",
            "boundary_summary": f"{STAGE_DIR_NAME}/big_unit_render_viewmodel_boundary_summary_1013K_M2.json",
            "replay_commands": f"{STAGE_DIR_NAME}/big_unit_render_viewmodel_replay_commands_1013K_M2.md",
        },
        "key_outputs": [
            "1013K_R7_big_unit_preview_surface_to_render_viewmodel_contract/big_unit_render_viewmodel_fixture_1013K_R7.json",
            "1013K_R8_big_unit_render_viewmodel_readonly_endpoint_contract/big_unit_render_viewmodel_readonly_response_fixture_1013K_R8.json",
        ],
        "github_upload_ready": True,
        "github_uploaded": False,
        "output_root": str(output_root),
    }


def build_boundary_summary(stage_results: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "boundary_type": "local_milestone_review_package_only",
        "small_package_policy": "R5-R8 remained local-only; M2 is upload-ready but not uploaded.",
        "route_registered": False,
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
        "main_project_pushed": False,
        "section_chunks_renderable_independently": True,
        "whole_document_blob_required": False,
        "stage_boundary_snapshot": [
            {
                "stage": item["stage"],
                "validator_pass": item["validator_pass"],
                "provider_called": item["provider_called"],
                "model_called": item["model_called"],
                "database_written": item["database_written"],
                "memory_written": item["memory_written"],
                "formal_apply_performed": item["formal_apply_performed"],
                "route_registered": item["route_registered"],
            }
            for item in stage_results
        ],
    }


def build_replay_commands() -> str:
    commands = [
        "python -m py_compile backend\\xiaobei_ai\\prep_room_big_unit_review_action_state_1013K_R5.py scripts\\validate_1013K_R5_big_unit_review_action_state_dry_run.py",
        "python scripts\\validate_1013K_R5_big_unit_review_action_state_dry_run.py",
        "python -m py_compile backend\\xiaobei_ai\\prep_room_big_unit_preview_surface_1013K_R6.py scripts\\validate_1013K_R6_big_unit_review_action_state_to_preview_surface_fixture.py",
        "python scripts\\validate_1013K_R6_big_unit_review_action_state_to_preview_surface_fixture.py",
        "python -m py_compile backend\\xiaobei_ai\\prep_room_big_unit_render_viewmodel_1013K_R7.py scripts\\validate_1013K_R7_big_unit_preview_surface_to_render_viewmodel_contract.py",
        "python scripts\\validate_1013K_R7_big_unit_preview_surface_to_render_viewmodel_contract.py",
        "python -m py_compile backend\\xiaobei_ai\\prep_room_big_unit_viewmodel_endpoint_contract_1013K_R8.py scripts\\validate_1013K_R8_big_unit_render_viewmodel_readonly_endpoint_contract.py",
        "python scripts\\validate_1013K_R8_big_unit_render_viewmodel_readonly_endpoint_contract.py",
        "python -m py_compile scripts\\validate_1013K_M2_big_unit_render_viewmodel_backend_milestone_package.py",
        "python scripts\\validate_1013K_M2_big_unit_render_viewmodel_backend_milestone_package.py",
    ]
    body = "\n".join(f"{index + 1}. `{command}`" for index, command in enumerate(commands))
    return (
        "# 1013K M2 Replay Commands\n\n"
        "Run from `D:\\Documents\\SmartEdu\\xiaobei-core`.\n\n"
        f"{body}\n\n"
        "Expected: every validator prints `ALL_..._CHECKS_OK` and M2 final status is PASS.\n"
    )


def build_report(stage_results: list[dict[str, Any]], result: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| {item['stage']} | {item['final_status']} | {item['validator_pass']} |"
        for item in stage_results
    )
    return (
        "# 1013K M2 Big Unit Render ViewModel Backend Milestone Package\n\n"
        "This milestone packages the local R5-R8 chain from preview action state to chunked render "
        "ViewModel and future readonly endpoint contract.\n\n"
        "## Stage Chain\n\n"
        "| Stage | Final Status | Validator |\n"
        "| --- | --- | --- |\n"
        f"{rows}\n\n"
        "## Boundary\n\n"
        "- Route registered: false\n"
        "- Runtime connected: false\n"
        "- Provider/model called: false\n"
        "- Database/memory/Feishu written: false\n"
        "- Formal apply performed: false\n"
        "- GitHub upload: ready but not performed in this validator\n\n"
        "## Result\n\n"
        f"`validator_pass={str(result['validator_pass']).lower()}`\n"
    )


def write_latest_and_manifest(output_root: Path) -> None:
    latest = (
        "# Latest Review Entry\n\n"
        f"STAGE={STAGE_ID}\n"
        f"FINAL_STATUS={FINAL_STATUS}\n"
        f"NEXT_STAGE={NEXT_STAGE}\n"
        "MILESTONE_PACKAGE_CREATED=true\n"
        "GITHUB_UPLOAD_READY=true\n"
        "GITHUB_UPLOADED=false\n"
        "PROVIDER_MODEL_CALL_ALLOWED=false\n"
        "FORMAL_APPLY_ALLOWED=false\n"
        "DATABASE_WRITE_ALLOWED=false\n"
        "MEMORY_WRITE_ALLOWED=false\n\n"
        "1013K_M2 archives R5-R8 from teacher action state to chunked render ViewModel and future "
        "readonly endpoint contract. It is upload-ready as a milestone package, but this validator "
        "does not push GitHub.\n"
    )
    manifest = (
        "# Review Package Manifest\n\n"
        f"Latest local milestone: `{STAGE_ID}`\n\n"
        "Includes:\n\n"
        f"- `{STAGE_DIR_NAME}/big_unit_render_viewmodel_milestone_index_1013K_M2.json`\n"
        f"- `{STAGE_DIR_NAME}/big_unit_render_viewmodel_boundary_summary_1013K_M2.json`\n"
        f"- `{STAGE_DIR_NAME}/big_unit_render_viewmodel_replay_commands_1013K_M2.md`\n"
        f"- `{STAGE_DIR_NAME}/1013K_M2_result.json`\n"
        f"- `{STAGE_DIR_NAME}/1013K_M2_report.md`\n"
        "- `1013K_R5_big_unit_review_action_state_dry_run/`\n"
        "- `1013K_R6_big_unit_review_action_state_to_preview_surface_fixture/`\n"
        "- `1013K_R7_big_unit_preview_surface_to_render_viewmodel_contract/`\n"
        "- `1013K_R8_big_unit_render_viewmodel_readonly_endpoint_contract/`\n\n"
        "Boundary: milestone review package only. No route registration, provider/model call, "
        "runtime connection, database/memory/Feishu write, formal apply, unit_package write, or "
        "lesson body write.\n"
    )
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)


def validate(root: Path) -> dict[str, Any]:
    output_root = resolve_output_root(root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)

    stage_results, missing_results = load_stage_results(output_root)
    all_stage_results_present = not missing_results and len(stage_results) == len(STAGE_CHAIN)
    all_validators_pass = all(item.get("validator_pass") is True for item in stage_results)
    all_failed_checks_empty = all(item.get("failed_checks", []) == [] for item in stage_results)
    any_provider_model_called = any(item.get("provider_called") or item.get("model_called") for item in stage_results)
    any_write_or_route_performed = any(
        item.get("database_written")
        or item.get("memory_written")
        or item.get("feishu_written")
        or item.get("formal_apply_performed")
        or item.get("route_registered")
        or item.get("main_project_pushed")
        for item in stage_results
    )
    source_files = [
        root / item
        for item in [
            "backend/xiaobei_ai/prep_room_big_unit_review_action_state_1013K_R5.py",
            "backend/xiaobei_ai/prep_room_big_unit_preview_surface_1013K_R6.py",
            "backend/xiaobei_ai/prep_room_big_unit_render_viewmodel_1013K_R7.py",
            "backend/xiaobei_ai/prep_room_big_unit_viewmodel_endpoint_contract_1013K_R8.py",
            "scripts/validate_1013K_M2_big_unit_render_viewmodel_backend_milestone_package.py",
        ]
    ]
    secret_scan_hits = scan_secret_hits(source_files)

    index = build_index(output_root, stage_results)
    boundary_summary = build_boundary_summary(stage_results)
    write_json(stage_dir / "big_unit_render_viewmodel_milestone_index_1013K_M2.json", index)
    write_json(stage_dir / "big_unit_render_viewmodel_boundary_summary_1013K_M2.json", boundary_summary)
    write_text(stage_dir / "big_unit_render_viewmodel_replay_commands_1013K_M2.md", build_replay_commands())

    failed_checks = []
    if not all_stage_results_present:
        failed_checks.append("all_stage_results_present")
    if not all_validators_pass:
        failed_checks.append("all_validators_pass")
    if not all_failed_checks_empty:
        failed_checks.append("all_failed_checks_empty")
    if any_provider_model_called:
        failed_checks.append("no_provider_or_model_call")
    if any_write_or_route_performed:
        failed_checks.append("no_write_route_or_formal_apply")
    if secret_scan_hits:
        failed_checks.append("secret_scan_clean")

    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS if not failed_checks else f"FAIL_{STAGE_ID}",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "milestone_package_created": True,
        "github_upload_ready": True,
        "github_uploaded": False,
        "all_stage_results_present": all_stage_results_present,
        "stage_count": len(stage_results),
        "all_validators_pass": all_validators_pass,
        "all_failed_checks_empty": all_failed_checks_empty,
        "secret_scan_hits": secret_scan_hits,
        "route_registered": False,
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
        "main_project_pushed": False,
        "failed_checks": failed_checks,
        "validator_pass": not failed_checks,
    }
    write_json(stage_dir / "1013K_M2_result.json", result)
    write_text(stage_dir / "1013K_M2_report.md", build_report(stage_results, result))
    write_latest_and_manifest(output_root)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    result = validate(args.root.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["validator_pass"]:
        return 1
    print("ALL_1013K_M2_BIG_UNIT_RENDER_VIEWMODEL_BACKEND_MILESTONE_PACKAGE_CHECKS_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
