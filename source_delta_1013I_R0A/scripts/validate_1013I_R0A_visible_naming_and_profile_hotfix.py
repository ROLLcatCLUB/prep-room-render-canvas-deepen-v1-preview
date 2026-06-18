from __future__ import annotations

import copy
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
INPUT_DIR = OUTPUT_ROOT / "1013I_teacher_self_prep_input_minimal_flow"
CONTRACT_DIR = OUTPUT_ROOT / "1013I_R0_unified_teacher_agent_profile_and_capability_contract"
OUT_DIR = OUTPUT_ROOT / "1013I_R0A_visible_naming_and_profile_hotfix"
SOURCE_DELTA_DIR = OUTPUT_ROOT / "source_delta_1013I_R0A" / "scripts"

STAGE_ID = "1013I_R0A_VISIBLE_NAMING_AND_PROFILE_HOTFIX"
NEXT_STAGE = "1013I_R1_CANDIDATE_CARD_SEED_FROM_SELF_PREP_REQUEST"
AGENT_ROLE = "unified_teacher_agent"
DISPLAY_NAME = "小教"
ACTIVE_SPACE = "prep_room"
ACTIVE_CAPABILITY = "lesson_prep"
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


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def assistant_profile() -> dict[str, Any]:
    return {
        "display_name": DISPLAY_NAME,
        "display_name_customizable": True,
        "wake_name": DISPLAY_NAME,
        "voice_profile_id": None,
        "tts_enabled": False,
        "speaking_style": "calm_professional",
        "assistant_tone": "teacher_work_partner",
        "response_style": "concise_contextual",
    }


def apply_profile_shape(payload: dict[str, Any]) -> dict[str, Any]:
    fixed = copy.deepcopy(payload)
    fixed.pop("agent", None)
    fixed["agent_role"] = AGENT_ROLE
    fixed["assistant_profile"] = assistant_profile()
    fixed["active_space"] = ACTIVE_SPACE
    fixed["active_capability"] = ACTIVE_CAPABILITY
    return fixed


def replace_deprecated_text(value: Any) -> Any:
    if isinstance(value, str):
        result = value
        for name in DEPRECATED_VISIBLE_NAMES:
            result = result.replace(name, DISPLAY_NAME)
        return result
    if isinstance(value, list):
        return [replace_deprecated_text(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_deprecated_text(item) for key, item in value.items()}
    return value


def scan_payload(name: str, payload: Any) -> list[dict[str, Any]]:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    hits: list[dict[str, Any]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for deprecated in DEPRECATED_VISIBLE_NAMES:
            if deprecated in line:
                hits.append(
                    {
                        "artifact": name,
                        "line": line_no,
                        "deprecated_name": deprecated,
                        "line_excerpt": line.strip(),
                    }
                )
    return hits


def has_legacy_agent_field(payload: Any) -> bool:
    if isinstance(payload, dict):
        return "agent" in payload or any(has_legacy_agent_field(value) for value in payload.values())
    if isinstance(payload, list):
        return any(has_legacy_agent_field(item) for item in payload)
    return False


def build_hotfix() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    original_input = read_json(INPUT_DIR / "teacher_self_prep_input_fixture_1013I.json")
    original_request = read_json(INPUT_DIR / "teacher_self_prep_request_1013I.json")
    original_preview = read_json(INPUT_DIR / "self_prep_preview_fixture_1013I.json")

    fixed_input = apply_profile_shape(replace_deprecated_text(original_input))

    fixed_request = replace_deprecated_text(original_request)
    fixed_request["teacher_input"] = apply_profile_shape(fixed_request["teacher_input"])
    fixed_request["profile_contract"] = {
        "stage": "1013I_R0_UNIFIED_TEACHER_AGENT_PROFILE_AND_CAPABILITY_CONTRACT",
        "agent_role": AGENT_ROLE,
        "current_default_display_name": DISPLAY_NAME,
        "active_space": ACTIVE_SPACE,
        "active_capability": ACTIVE_CAPABILITY,
    }

    fixed_preview = replace_deprecated_text(original_preview)
    fixed_preview["agent_role"] = AGENT_ROLE
    fixed_preview["assistant_profile"] = assistant_profile()
    fixed_preview["active_space"] = ACTIVE_SPACE
    fixed_preview["active_capability"] = ACTIVE_CAPABILITY
    fixed_preview["source_request_id"] = "teacher_self_prep_request_1013I_R0A"

    scan = {
        "scan_id": "visible_naming_and_profile_hotfix_scan_1013I_R0A",
        "stage": STAGE_ID,
        "original_scan": {
            "teacher_self_prep_input_fixture_1013I.json": scan_payload("teacher_self_prep_input_fixture_1013I.json", original_input),
            "teacher_self_prep_request_1013I.json": scan_payload("teacher_self_prep_request_1013I.json", original_request),
            "self_prep_preview_fixture_1013I.json": scan_payload("self_prep_preview_fixture_1013I.json", original_preview),
            "legacy_agent_field_found": any(
                [
                    has_legacy_agent_field(original_input),
                    has_legacy_agent_field(original_request),
                    has_legacy_agent_field(original_preview),
                ]
            ),
        },
        "fixed_scan": {
            "teacher_self_prep_input_fixture_1013I_R0A.json": scan_payload("teacher_self_prep_input_fixture_1013I_R0A.json", fixed_input),
            "teacher_self_prep_request_1013I_R0A.json": scan_payload("teacher_self_prep_request_1013I_R0A.json", fixed_request),
            "self_prep_preview_fixture_1013I_R0A.json": scan_payload("self_prep_preview_fixture_1013I_R0A.json", fixed_preview),
            "legacy_agent_field_found": any(
                [
                    has_legacy_agent_field(fixed_input),
                    has_legacy_agent_field(fixed_request),
                    has_legacy_agent_field(fixed_preview),
                ]
            ),
        },
    }
    return fixed_input, fixed_request, fixed_preview, scan


def build_patch_manifest(scan: dict[str, Any]) -> dict[str, Any]:
    original_hit_count = sum(len(hits) for key, hits in scan["original_scan"].items() if isinstance(hits, list))
    fixed_hit_count = sum(len(hits) for key, hits in scan["fixed_scan"].items() if isinstance(hits, list))
    return {
        "manifest_id": "visible_naming_and_profile_hotfix_manifest_1013I_R0A",
        "stage": STAGE_ID,
        "source_stage": "1013I_TEACHER_SELF_PREP_INPUT_MINIMAL_FLOW",
        "profile_contract_stage": "1013I_R0_UNIFIED_TEACHER_AGENT_PROFILE_AND_CAPABILITY_CONTRACT",
        "hotfix_scope": [
            "teacher-visible deprecated agent names in current 1013I artifacts",
            "legacy agent field shape in current 1013I artifacts",
        ],
        "generated_successor_artifacts": [
            "teacher_self_prep_input_fixture_1013I_R0A.json",
            "teacher_self_prep_request_1013I_R0A.json",
            "self_prep_preview_fixture_1013I_R0A.json",
        ],
        "original_1013I_artifacts_modified": False,
        "original_deprecated_visible_hit_count": original_hit_count,
        "fixed_deprecated_visible_hit_count": fixed_hit_count,
        "global_search_replace_performed": False,
        "repo_path_rename_performed": False,
        "historical_review_package_modified": False,
        "old_validator_renamed": False,
    }


def build_result(scan: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    fixed_hit_count = manifest["fixed_deprecated_visible_hit_count"]
    fixed_legacy_agent = scan["fixed_scan"]["legacy_agent_field_found"]
    boundary = {
        "visible_naming_hotfix_created": True,
        "profile_shape_hotfix_created": True,
        "successor_artifacts_created": True,
        "original_1013I_artifacts_modified": False,
        "teacher_visible_xiaobei_hits_after_hotfix": [],
        "teacher_visible_deprecated_agent_hits_after_hotfix": [],
        "deprecated_visible_hit_count_after_hotfix": fixed_hit_count,
        "legacy_agent_field_after_hotfix": fixed_legacy_agent,
        "agent_role": AGENT_ROLE,
        "assistant_profile_present": True,
        "current_default_display_name": DISPLAY_NAME,
        "active_space": ACTIVE_SPACE,
        "active_capability": ACTIVE_CAPABILITY,
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
        boundary["visible_naming_hotfix_created"]
        and boundary["profile_shape_hotfix_created"]
        and boundary["successor_artifacts_created"]
        and not boundary["original_1013I_artifacts_modified"]
        and fixed_hit_count == 0
        and not fixed_legacy_agent
        and boundary["agent_role"] == AGENT_ROLE
        and boundary["assistant_profile_present"]
        and boundary["active_capability"] == ACTIVE_CAPABILITY
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
        "inherits_from": "1013I_R0_UNIFIED_TEACHER_AGENT_PROFILE_AND_CAPABILITY_CONTRACT",
        "final_status": "PASS_1013I_R0A_VISIBLE_NAMING_AND_PROFILE_HOTFIX" if final_pass else "FAIL_1013I_R0A_VISIBLE_NAMING_AND_PROFILE_HOTFIX",
        "next_stage": NEXT_STAGE,
        **boundary,
    }


def build_report(result: dict[str, Any], manifest: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# 1013I R0A Visible Naming And Profile Hotfix",
            "",
            f"- FINAL_STATUS: `{result['final_status']}`",
            f"- NEXT_STAGE: `{result['next_stage']}`",
            "- Boundary: current 1013I successor artifacts only; no global replacement, no runtime/provider/model, no formal apply.",
            "",
            "## Hotfix Scope",
            "",
            "- Replace teacher-visible deprecated assistant name in current 1013I successor artifacts.",
            "- Upgrade old `agent` field shape to `agent_role + assistant_profile + active_space + active_capability`.",
            "- Preserve original 1013I artifacts as historical input; R1 should read the R0A successor artifacts.",
            "",
            "## Result",
            "",
            f"- original_deprecated_visible_hit_count={manifest['original_deprecated_visible_hit_count']}",
            f"- deprecated_visible_hit_count_after_hotfix={result['deprecated_visible_hit_count_after_hotfix']}",
            f"- legacy_agent_field_after_hotfix={str(result['legacy_agent_field_after_hotfix']).lower()}",
            f"- agent_role={result['agent_role']}",
            f"- current_default_display_name={result['current_default_display_name']}",
            f"- active_capability={result['active_capability']}",
            "",
            "## Boundary Flags",
            "",
            f"- original_1013I_artifacts_modified={str(result['original_1013I_artifacts_modified']).lower()}",
            f"- global_search_replace_performed={str(result['global_search_replace_performed']).lower()}",
            f"- repo_path_rename_performed={str(result['repo_path_rename_performed']).lower()}",
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
    contract = read_json(CONTRACT_DIR / "unified_teacher_agent_profile_and_capability_contract.json")
    if contract["agent_role"] != AGENT_ROLE:
        raise ValueError("Profile contract agent_role mismatch")
    fixed_input, fixed_request, fixed_preview, scan = build_hotfix()
    manifest = build_patch_manifest(scan)
    result = build_result(scan, manifest)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "teacher_self_prep_input_fixture_1013I_R0A.json", fixed_input)
    write_json(OUT_DIR / "teacher_self_prep_request_1013I_R0A.json", fixed_request)
    write_json(OUT_DIR / "self_prep_preview_fixture_1013I_R0A.json", fixed_preview)
    write_json(OUT_DIR / "visible_naming_and_profile_hotfix_scan_1013I_R0A.json", scan)
    write_json(OUT_DIR / "visible_naming_and_profile_hotfix_manifest_1013I_R0A.json", manifest)
    write_json(OUT_DIR / "1013I_R0A_result.json", result)
    write_text(OUT_DIR / "1013I_R0A_report.md", build_report(result, manifest))
    copy_source_delta()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
