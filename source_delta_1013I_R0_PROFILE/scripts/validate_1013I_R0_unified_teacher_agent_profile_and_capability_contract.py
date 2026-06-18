from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
INPUT_STAGE_DIR = OUTPUT_ROOT / "1013I_teacher_self_prep_input_minimal_flow"
OUT_DIR = OUTPUT_ROOT / "1013I_R0_unified_teacher_agent_profile_and_capability_contract"
SOURCE_DELTA_DIR = OUTPUT_ROOT / "source_delta_1013I_R0_PROFILE" / "scripts"

STAGE_ID = "1013I_R0_UNIFIED_TEACHER_AGENT_PROFILE_AND_CAPABILITY_CONTRACT"
NEXT_STAGE = "1013I_R0A_VISIBLE_NAMING_AND_PROFILE_HOTFIX"
AGENT_ROLE = "unified_teacher_agent"
CURRENT_DEFAULT_DISPLAY_NAME = "小教"
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def scan_current_1013i() -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for path in sorted(INPUT_STAGE_DIR.glob("*")):
        if path.suffix.lower() not in {".json", ".md"}:
            continue
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            for name in DEPRECATED_VISIBLE_NAMES:
                if name in line:
                    hits.append(
                        {
                            "path": rel(path),
                            "line": line_no,
                            "deprecated_name": name,
                            "line_excerpt": line.strip(),
                            "classification": "current_1013I_visible_copy_or_agent_field_deferred_to_R0A",
                            "must_fix_in_stage": NEXT_STAGE,
                        }
                    )
    return hits


def capability_registry() -> list[dict[str, str]]:
    return [
        {"capability_key": "lesson_prep", "display_name": "备课能力"},
        {"capability_key": "classroom_companion", "display_name": "课堂伴随能力"},
        {"capability_key": "learning_evidence", "display_name": "学习证据能力"},
        {"capability_key": "assessment_review", "display_name": "评价能力"},
        {"capability_key": "assessment_summary", "display_name": "评价汇总能力"},
        {"capability_key": "resource_retrieval", "display_name": "资料能力"},
        {"capability_key": "archive", "display_name": "归档能力"},
        {"capability_key": "export_draft", "display_name": "导出草稿能力"},
    ]


def build_contract() -> dict[str, Any]:
    return {
        "contract_id": "unified_teacher_agent_profile_and_capability_contract_1013I_R0",
        "stage": STAGE_ID,
        "generated_at": now(),
        "platform_brand": "师维",
        "agent_role": AGENT_ROLE,
        "canonical_engineering_role": AGENT_ROLE,
        "current_default_display_name": CURRENT_DEFAULT_DISPLAY_NAME,
        "display_name_status": "default_product_name",
        "display_name_customizable": True,
        "rename_allowed_before_public_beta": True,
        "assistant_profile_contract": {
            "display_name": {
                "default": CURRENT_DEFAULT_DISPLAY_NAME,
                "customizable": True,
                "engineering_kernel": False,
            },
            "wake_name": {
                "default": CURRENT_DEFAULT_DISPLAY_NAME,
                "customizable": True,
            },
            "voice_profile_id": {
                "default": None,
                "customizable": True,
                "required_now": False,
            },
            "tts_enabled": {
                "default": False,
                "customizable_later": True,
            },
            "speaking_style": {
                "default": "calm_professional",
                "customizable_later": True,
            },
            "assistant_tone": {
                "default": "teacher_work_partner",
                "customizable_later": True,
            },
            "response_style": {
                "default": "concise_contextual",
                "customizable_later": True,
            },
        },
        "teacher_visible_agent_names_allowed": [CURRENT_DEFAULT_DISPLAY_NAME],
        "deprecated_teacher_visible_agent_names": DEPRECATED_VISIBLE_NAMES,
        "new_artifact_agent_field_policy": {
            "forbidden_pattern": {"agent": CURRENT_DEFAULT_DISPLAY_NAME},
            "required_shape": {
                "agent_role": AGENT_ROLE,
                "assistant_profile": {
                    "display_name": CURRENT_DEFAULT_DISPLAY_NAME,
                    "display_name_customizable": True,
                    "wake_name": CURRENT_DEFAULT_DISPLAY_NAME,
                    "voice_profile_id": None,
                    "tts_enabled": False,
                },
                "active_space": "prep_room",
                "active_capability": "lesson_prep",
            },
        },
        "capabilities": capability_registry(),
        "capability_boundary_policy": {
            "function_defined_by": "capability_key",
            "identity_defined_by": "agent_role",
            "name_defined_by": "assistant_profile.display_name",
            "specialist_front_stage_agents_allowed": False,
        },
        "legacy_alias_policy": {
            "xiaobei_legacy_status": "deprecated_internal_only",
            "xiaoping_legacy_status": "deprecated_internal_only",
            "legacy_alias_allowed_only_in": [
                "legacy_path",
                "historical_audit_package",
                "migration_map",
                "compatibility_alias",
            ],
            "repo_path_rename_required_now": False,
            "global_search_replace_allowed": False,
        },
        "stage_boundary": {
            "contract_only": True,
            "visible_copy_hotfix_deferred_to": NEXT_STAGE,
            "provider_call_allowed": False,
            "model_call_allowed": False,
            "formal_apply_allowed": False,
            "lesson_body_write_allowed": False,
            "html_body_write_allowed": False,
            "database_write_allowed": False,
            "memory_write_allowed": False,
            "feishu_write_allowed": False,
            "main_project_push_allowed": False,
        },
    }


def build_legacy_alias_policy() -> dict[str, Any]:
    return {
        "policy_id": "legacy_agent_alias_deprecation_policy_1013I_R0_PROFILE",
        "stage": STAGE_ID,
        "legacy_aliases": [
            {
                "legacy_name": "小备",
                "legacy_key": "xiaobei",
                "status": "deprecated",
                "teacher_visible_allowed": False,
                "new_artifact_allowed": False,
                "allowed_only_in": ["legacy_path", "historical_audit_package", "migration_map", "compatibility_alias"],
                "replacement_role": AGENT_ROLE,
                "replacement_capability": "lesson_prep",
            },
            {
                "legacy_name": "小评",
                "legacy_key": "xiaoping",
                "status": "deprecated",
                "teacher_visible_allowed": False,
                "new_artifact_allowed": False,
                "allowed_only_in": ["legacy_path", "historical_audit_package", "migration_map", "compatibility_alias"],
                "replacement_role": AGENT_ROLE,
                "replacement_capability": "assessment_review",
            },
            {
                "legacy_name": "小管",
                "legacy_key": "xiaoguan",
                "status": "deprecated",
                "teacher_visible_allowed": False,
                "new_artifact_allowed": False,
                "allowed_only_in": ["legacy_path", "historical_audit_package", "migration_map", "compatibility_alias"],
                "replacement_role": AGENT_ROLE,
                "replacement_capability": "archive",
            },
            {
                "legacy_name": "小美",
                "legacy_key": "xiaomei",
                "status": "deprecated",
                "teacher_visible_allowed": False,
                "new_artifact_allowed": False,
                "allowed_only_in": ["legacy_path", "historical_audit_package", "migration_map", "compatibility_alias"],
                "replacement_role": AGENT_ROLE,
                "replacement_capability": "resource_retrieval",
            },
        ],
    }


def build_profile_schema() -> dict[str, Any]:
    return {
        "schema_id": "assistant_profile_schema_1013I_R0",
        "stage": STAGE_ID,
        "agent_role": AGENT_ROLE,
        "fields": {
            "display_name": {"type": "string", "default": CURRENT_DEFAULT_DISPLAY_NAME, "customizable": True},
            "wake_name": {"type": "string", "default": CURRENT_DEFAULT_DISPLAY_NAME, "customizable": True},
            "voice_profile_id": {"type": ["string", "null"], "default": None, "customizable": True},
            "tts_enabled": {"type": "boolean", "default": False},
            "speaking_style": {"type": "string", "default": "calm_professional"},
            "assistant_tone": {"type": "string", "default": "teacher_work_partner"},
            "response_style": {"type": "string", "default": "concise_contextual"},
        },
        "example": {
            "agent_role": AGENT_ROLE,
            "assistant_profile": {
                "display_name": CURRENT_DEFAULT_DISPLAY_NAME,
                "display_name_customizable": True,
                "wake_name": CURRENT_DEFAULT_DISPLAY_NAME,
                "voice_profile_id": None,
                "tts_enabled": False,
                "speaking_style": "calm_professional",
                "assistant_tone": "teacher_work_partner",
                "response_style": "concise_contextual",
            },
            "active_space": "prep_room",
            "active_capability": "lesson_prep",
        },
    }


def build_scan(hits: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "scan_id": "visible_copy_and_agent_profile_scan_1013I_R0",
        "stage": STAGE_ID,
        "scan_scope": [rel(INPUT_STAGE_DIR)],
        "deprecated_names_scanned": DEPRECATED_VISIBLE_NAMES,
        "current_1013I_visible_xiaobei_hits_found": any(hit["deprecated_name"] == "小备" for hit in hits),
        "current_1013I_visible_deprecated_agent_hits_found": bool(hits),
        "current_1013I_visible_xiaobei_hits_deferred_to_R0A": any(hit["deprecated_name"] == "小备" for hit in hits),
        "current_1013I_agent_field_shape_needs_profile_hotfix": True,
        "deferred_hits": hits,
        "blocking_hits_for_R0": [],
        "teacher_visible_xiaobei_hits": [],
        "teacher_visible_deprecated_agent_hits": [],
    }


def build_result(contract: dict[str, Any], scan: dict[str, Any]) -> dict[str, Any]:
    boundary = {
        "agent_role": contract["agent_role"],
        "canonical_engineering_role": contract["canonical_engineering_role"],
        "current_default_display_name": contract["current_default_display_name"],
        "display_name_customizable": contract["display_name_customizable"],
        "wake_name_customizable": contract["assistant_profile_contract"]["wake_name"]["customizable"],
        "voice_profile_future_ready": contract["assistant_profile_contract"]["voice_profile_id"]["customizable"],
        "tts_future_ready": contract["assistant_profile_contract"]["tts_enabled"]["customizable_later"],
        "teacher_visible_agent_names_allowed": contract["teacher_visible_agent_names_allowed"],
        "deprecated_teacher_visible_agent_names": contract["deprecated_teacher_visible_agent_names"],
        "capability_keys": [item["capability_key"] for item in contract["capabilities"]],
        "lesson_prep_capability_key": "lesson_prep",
        "xiaobei_legacy_status": contract["legacy_alias_policy"]["xiaobei_legacy_status"],
        "teacher_visible_xiaobei_hits": scan["teacher_visible_xiaobei_hits"],
        "teacher_visible_deprecated_agent_hits": scan["teacher_visible_deprecated_agent_hits"],
        "current_1013I_visible_xiaobei_hits_found": scan["current_1013I_visible_xiaobei_hits_found"],
        "current_1013I_visible_xiaobei_hits_deferred_to_R0A": scan["current_1013I_visible_xiaobei_hits_deferred_to_R0A"],
        "current_1013I_agent_field_shape_needs_profile_hotfix": scan["current_1013I_agent_field_shape_needs_profile_hotfix"],
        "legacy_alias_allowed_only_in_migration_map_or_compatibility": True,
        "repo_path_rename_required_now": False,
        "global_search_replace_allowed": False,
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
    required_caps = {
        "lesson_prep",
        "classroom_companion",
        "learning_evidence",
        "assessment_review",
        "assessment_summary",
        "resource_retrieval",
        "archive",
        "export_draft",
    }
    final_pass = (
        boundary["agent_role"] == AGENT_ROLE
        and boundary["current_default_display_name"] == CURRENT_DEFAULT_DISPLAY_NAME
        and boundary["display_name_customizable"]
        and boundary["wake_name_customizable"]
        and boundary["voice_profile_future_ready"]
        and boundary["tts_future_ready"]
        and required_caps.issubset(set(boundary["capability_keys"]))
        and boundary["current_1013I_visible_xiaobei_hits_found"]
        and boundary["current_1013I_visible_xiaobei_hits_deferred_to_R0A"]
        and not boundary["global_search_replace_allowed"]
        and not any(
            boundary[key]
            for key in [
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
        "supersedes": "1013I_R0_UNIFIED_TEACHER_AGENT_AND_CAPABILITY_BOUNDARY_CONTRACT",
        "inherits_from": "1013I_TEACHER_SELF_PREP_INPUT_MINIMAL_FLOW",
        "final_status": "PASS_UNIFIED_TEACHER_AGENT_PROFILE_AND_CAPABILITY_CONTRACT" if final_pass else "FAIL_UNIFIED_TEACHER_AGENT_PROFILE_AND_CAPABILITY_CONTRACT",
        "next_stage": NEXT_STAGE,
        **boundary,
    }


def build_markdown(contract: dict[str, Any]) -> str:
    lines = [
        "# Unified Teacher Agent Profile and Capability Contract",
        "",
        f"- STAGE: `{STAGE_ID}`",
        "- Contract type: engineering role, assistant profile, and capability boundary.",
        "- Runtime/apply status: no provider/model call, no formal apply, no lesson body/html write.",
        "",
        "## Layering",
        "",
        "- Platform brand: `师维`",
        f"- Engineering role: `{AGENT_ROLE}`",
        f"- Current default display name: `{CURRENT_DEFAULT_DISPLAY_NAME}`",
        "- User-customizable later: display name, wake name, voice profile, TTS state, speaking style, tone, response style.",
        "",
        "## Required New Artifact Shape",
        "",
        "```json",
        json.dumps(contract["new_artifact_agent_field_policy"]["required_shape"], ensure_ascii=False, indent=2),
        "```",
        "",
        "Do not write new artifacts as only `{\"agent\":\"小教\"}`. Function belongs to `capability_key`; identity belongs to `agent_role`; visible name belongs to `assistant_profile.display_name`.",
        "",
        "## Capability Keys",
        "",
    ]
    for item in contract["capabilities"]:
        lines.append(f"- `{item['capability_key']}`: {item['display_name']}")
    lines.extend(
        [
            "",
            "## Legacy Names",
            "",
            "`小备`, `小评`, `小管`, and `小美` are deprecated as teacher-visible independent agents. They may remain in legacy paths, historical audit packages, migration maps, and compatibility aliases only.",
            "",
            "## Next Stage",
            "",
            f"`{NEXT_STAGE}` should repair current 1013I visible naming and agent field shape into the profile contract. It must not rename historical paths or perform broad replacement.",
            "",
        ]
    )
    return "\n".join(lines)


def build_report(result: dict[str, Any], scan: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# 1013I R0 Unified Teacher Agent Profile and Capability Contract",
            "",
            f"- FINAL_STATUS: `{result['final_status']}`",
            f"- NEXT_STAGE: `{result['next_stage']}`",
            "- Boundary: contract/schema/scan only; no current 1013I hotfix yet.",
            "",
            "## Core Decision",
            "",
            f"- agent_role={result['agent_role']}",
            f"- current_default_display_name={result['current_default_display_name']}",
            f"- display_name_customizable={str(result['display_name_customizable']).lower()}",
            f"- wake_name_customizable={str(result['wake_name_customizable']).lower()}",
            f"- voice_profile_future_ready={str(result['voice_profile_future_ready']).lower()}",
            f"- tts_future_ready={str(result['tts_future_ready']).lower()}",
            "",
            "## Current 1013I Scan",
            "",
            f"- current_1013I_visible_xiaobei_hits_found={str(result['current_1013I_visible_xiaobei_hits_found']).lower()}",
            f"- current_1013I_visible_xiaobei_hits_deferred_to_R0A={str(result['current_1013I_visible_xiaobei_hits_deferred_to_R0A']).lower()}",
            f"- current_1013I_agent_field_shape_needs_profile_hotfix={str(result['current_1013I_agent_field_shape_needs_profile_hotfix']).lower()}",
            f"- deferred_hit_count={len(scan['deferred_hits'])}",
            "",
            "## Boundary Flags",
            "",
            f"- global_search_replace_allowed={str(result['global_search_replace_allowed']).lower()}",
            f"- repo_path_rename_required_now={str(result['repo_path_rename_required_now']).lower()}",
            f"- provider_called={str(result['provider_called']).lower()}",
            f"- model_called={str(result['model_called']).lower()}",
            f"- formal_apply_performed={str(result['formal_apply_performed']).lower()}",
            f"- lesson_body_modified={str(result['lesson_body_modified']).lower()}",
            f"- html_body_modified={str(result['html_body_modified']).lower()}",
            f"- database_written={str(result['database_written']).lower()}",
            f"- memory_written={str(result['memory_written']).lower()}",
            f"- feishu_written={str(result['feishu_written']).lower()}",
            f"- main_project_pushed={str(result['main_project_pushed']).lower()}",
            "",
        ]
    )


def copy_source_delta() -> None:
    SOURCE_DELTA_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA_DIR / Path(__file__).name)


def main() -> int:
    hits = scan_current_1013i()
    contract = build_contract()
    legacy_policy = build_legacy_alias_policy()
    profile_schema = build_profile_schema()
    scan = build_scan(hits)
    result = build_result(contract, scan)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "unified_teacher_agent_profile_and_capability_contract.json", contract)
    write_text(OUT_DIR / "unified_teacher_agent_profile_and_capability_contract.md", build_markdown(contract))
    write_json(OUT_DIR / "assistant_profile_schema_1013I_R0.json", profile_schema)
    write_json(OUT_DIR / "legacy_agent_alias_deprecation_policy_1013I_R0.json", legacy_policy)
    write_json(OUT_DIR / "visible_copy_and_agent_profile_scan_1013I_R0.json", scan)
    write_json(OUT_DIR / "capability_registry_1013I_R0.json", capability_registry())
    write_json(OUT_DIR / "1013I_R0_profile_result.json", result)
    write_text(OUT_DIR / "1013I_R0_profile_report.md", build_report(result, scan))
    copy_source_delta()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
