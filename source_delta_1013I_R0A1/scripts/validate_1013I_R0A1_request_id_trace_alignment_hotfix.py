from __future__ import annotations

import copy
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R0A_DIR = OUTPUT_ROOT / "1013I_R0A_visible_naming_and_profile_hotfix"
OUT_DIR = OUTPUT_ROOT / "1013I_R0A1_request_id_trace_alignment_hotfix"
SOURCE_DELTA_DIR = OUTPUT_ROOT / "source_delta_1013I_R0A1" / "scripts"

STAGE_ID = "1013I_R0A1_REQUEST_ID_TRACE_ALIGNMENT_HOTFIX"
NEXT_STAGE = "1013I_R1_CANDIDATE_CARD_SEED_FROM_SELF_PREP_REQUEST"
ALIGNED_REQUEST_ID = "teacher_self_prep_request_1013I_R0A"
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def scan_deprecated(payload: Any) -> list[str]:
    text = json.dumps(payload, ensure_ascii=False)
    return [name for name in DEPRECATED_VISIBLE_NAMES if name in text]


def has_legacy_agent_field(payload: Any) -> bool:
    if isinstance(payload, dict):
        return "agent" in payload or any(has_legacy_agent_field(value) for value in payload.values())
    if isinstance(payload, list):
        return any(has_legacy_agent_field(item) for item in payload)
    return False


def build_aligned_artifacts() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    r0a_request = read_json(R0A_DIR / "teacher_self_prep_request_1013I_R0A.json")
    r0a_preview = read_json(R0A_DIR / "self_prep_preview_fixture_1013I_R0A.json")

    aligned_request = copy.deepcopy(r0a_request)
    original_request_id = aligned_request.get("request_id")
    aligned_request["request_id"] = ALIGNED_REQUEST_ID
    aligned_request["original_request_id"] = original_request_id
    aligned_request["trace_alignment"] = {
        "stage": STAGE_ID,
        "request_id_trace_aligned": True,
        "aligned_request_id": ALIGNED_REQUEST_ID,
        "source_request_id_expected_by_preview": ALIGNED_REQUEST_ID,
    }

    aligned_preview = copy.deepcopy(r0a_preview)
    aligned_preview["source_request_id"] = ALIGNED_REQUEST_ID
    aligned_preview["trace_alignment"] = {
        "stage": STAGE_ID,
        "request_id_trace_aligned": True,
        "aligned_request_id": ALIGNED_REQUEST_ID,
    }

    trace = {
        "trace_id": "request_id_trace_alignment_1013I_R0A1",
        "stage": STAGE_ID,
        "source_stage": "1013I_R0A_VISIBLE_NAMING_AND_PROFILE_HOTFIX",
        "r0a_request_file": "1013I_R0A_visible_naming_and_profile_hotfix/teacher_self_prep_request_1013I_R0A.json",
        "r0a_preview_file": "1013I_R0A_visible_naming_and_profile_hotfix/self_prep_preview_fixture_1013I_R0A.json",
        "original_request_id": original_request_id,
        "aligned_request_id": ALIGNED_REQUEST_ID,
        "preview_source_request_id": aligned_preview["source_request_id"],
        "request_id_trace_aligned": aligned_request["request_id"] == aligned_preview["source_request_id"],
        "original_r0a_artifacts_modified": False,
        "successor_artifacts_created": [
            "teacher_self_prep_request_1013I_R0A1.json",
            "self_prep_preview_fixture_1013I_R0A1.json",
        ],
    }

    manifest = {
        "manifest_id": "request_id_trace_alignment_hotfix_manifest_1013I_R0A1",
        "stage": STAGE_ID,
        "hotfix_scope": [
            "align request.request_id with preview.source_request_id",
            "preserve original_request_id for traceability",
        ],
        "r1_should_read": "1013I_R0A1_request_id_trace_alignment_hotfix/teacher_self_prep_request_1013I_R0A1.json",
        "r1_preview_fixture": "1013I_R0A1_request_id_trace_alignment_hotfix/self_prep_preview_fixture_1013I_R0A1.json",
        "global_search_replace_performed": False,
        "repo_path_rename_performed": False,
        "historical_review_package_modified": False,
    }
    return aligned_request, aligned_preview, trace, manifest


def build_result(
    aligned_request: dict[str, Any],
    aligned_preview: dict[str, Any],
    trace: dict[str, Any],
) -> dict[str, Any]:
    request_id_trace_aligned = aligned_request.get("request_id") == aligned_preview.get("source_request_id")
    deprecated_hits = sorted(set(scan_deprecated(aligned_request) + scan_deprecated(aligned_preview)))
    legacy_agent_field = has_legacy_agent_field(aligned_request) or has_legacy_agent_field(aligned_preview)
    boundary = {
        "request_id_trace_alignment_hotfix_created": True,
        "successor_artifacts_created": True,
        "request_id_trace_aligned": request_id_trace_aligned,
        "request_id": aligned_request.get("request_id"),
        "source_request_id": aligned_preview.get("source_request_id"),
        "original_request_id": aligned_request.get("original_request_id"),
        "original_r0a_artifacts_modified": False,
        "teacher_visible_deprecated_agent_hits_after_hotfix": deprecated_hits,
        "legacy_agent_field_after_hotfix": legacy_agent_field,
        "agent_role": aligned_request.get("teacher_input", {}).get("agent_role"),
        "assistant_profile_present": bool(aligned_request.get("teacher_input", {}).get("assistant_profile")),
        "active_space": aligned_request.get("teacher_input", {}).get("active_space"),
        "active_capability": aligned_request.get("teacher_input", {}).get("active_capability"),
        "global_search_replace_performed": False,
        "repo_path_rename_performed": False,
        "historical_review_package_modified": False,
        "old_validator_renamed": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }
    final_pass = (
        boundary["request_id_trace_alignment_hotfix_created"]
        and boundary["successor_artifacts_created"]
        and boundary["request_id_trace_aligned"]
        and boundary["request_id"] == ALIGNED_REQUEST_ID
        and boundary["source_request_id"] == ALIGNED_REQUEST_ID
        and boundary["original_request_id"] == "teacher_self_prep_request_1013I"
        and not boundary["original_r0a_artifacts_modified"]
        and not boundary["teacher_visible_deprecated_agent_hits_after_hotfix"]
        and not boundary["legacy_agent_field_after_hotfix"]
        and trace["request_id_trace_aligned"]
        and not any(
            boundary[key]
            for key in [
                "global_search_replace_performed",
                "repo_path_rename_performed",
                "historical_review_package_modified",
                "old_validator_renamed",
                "provider_called",
                "model_called",
                "formal_apply_performed",
                "lesson_body_modified",
                "html_body_modified",
                "database_written",
                "memory_written",
                "feishu_written",
                "main_project_pushed",
            ]
        )
    )
    return {
        "stage": STAGE_ID,
        "generated_at": now(),
        "inherits_from": "1013I_R0A_VISIBLE_NAMING_AND_PROFILE_HOTFIX",
        "final_status": "PASS_1013I_R0A1_REQUEST_ID_TRACE_ALIGNMENT_HOTFIX" if final_pass else "FAIL_1013I_R0A1_REQUEST_ID_TRACE_ALIGNMENT_HOTFIX",
        "next_stage": NEXT_STAGE,
        **boundary,
    }


def build_report(result: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# 1013I R0A1 Request ID Trace Alignment Hotfix",
            "",
            f"- FINAL_STATUS: `{result['final_status']}`",
            f"- NEXT_STAGE: `{result['next_stage']}`",
            "- Boundary: trace alignment only; no global replacement, no provider/model, no formal apply.",
            "",
            "## Trace Alignment",
            "",
            f"- request_id={result['request_id']}",
            f"- source_request_id={result['source_request_id']}",
            f"- original_request_id={result['original_request_id']}",
            f"- request_id_trace_aligned={str(result['request_id_trace_aligned']).lower()}",
            "",
            "## Preserved R0A Boundary",
            "",
            f"- original_r0a_artifacts_modified={str(result['original_r0a_artifacts_modified']).lower()}",
            f"- legacy_agent_field_after_hotfix={str(result['legacy_agent_field_after_hotfix']).lower()}",
            f"- teacher_visible_deprecated_agent_hits_after_hotfix={result['teacher_visible_deprecated_agent_hits_after_hotfix']}",
            f"- provider_called={str(result['provider_called']).lower()}",
            f"- model_called={str(result['model_called']).lower()}",
            f"- formal_apply_performed={str(result['formal_apply_performed']).lower()}",
            f"- lesson_body_modified={str(result['lesson_body_modified']).lower()}",
            f"- html_body_modified={str(result['html_body_modified']).lower()}",
            f"- database_written={str(result['database_written']).lower()}",
            f"- memory_written={str(result['memory_written']).lower()}",
            f"- feishu_written={str(result['feishu_written']).lower()}",
            "",
        ]
    )


def copy_source_delta() -> None:
    SOURCE_DELTA_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA_DIR / Path(__file__).name)


def main() -> int:
    aligned_request, aligned_preview, trace, manifest = build_aligned_artifacts()
    result = build_result(aligned_request, aligned_preview, trace)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "teacher_self_prep_request_1013I_R0A1.json", aligned_request)
    write_json(OUT_DIR / "self_prep_preview_fixture_1013I_R0A1.json", aligned_preview)
    write_json(OUT_DIR / "request_id_trace_alignment_1013I_R0A1.json", trace)
    write_json(OUT_DIR / "request_id_trace_alignment_hotfix_manifest_1013I_R0A1.json", manifest)
    write_json(OUT_DIR / "1013I_R0A1_result.json", result)
    write_text(OUT_DIR / "1013I_R0A1_report.md", build_report(result))
    copy_source_delta()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
