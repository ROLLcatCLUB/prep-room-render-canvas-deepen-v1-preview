from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
INPUT_STAGE_DIR = OUTPUT_ROOT / "1013I_teacher_self_prep_input_minimal_flow"
OUT_DIR = OUTPUT_ROOT / "1013I_R0_unified_teacher_agent_and_capability_boundary_contract"
SOURCE_DELTA_DIR = OUTPUT_ROOT / "source_delta_1013I_R0" / "scripts"

STAGE_ID = "1013I_R0_UNIFIED_TEACHER_AGENT_AND_CAPABILITY_BOUNDARY_CONTRACT"
NEXT_STAGE = "1013I_R0A_VISIBLE_NAMING_HOTFIX"
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]
CURRENT_DISPLAY_NAME = "小教"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def scan_current_1013i_visible_names() -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for path in sorted(INPUT_STAGE_DIR.glob("*")):
        if path.suffix.lower() not in {".json", ".md"}:
            continue
        text = read_text(path)
        for line_no, line in enumerate(text.splitlines(), start=1):
            for name in DEPRECATED_VISIBLE_NAMES:
                if name in line:
                    hits.append(
                        {
                            "path": rel(path),
                            "line": line_no,
                            "deprecated_name": name,
                            "line_excerpt": line.strip(),
                            "classification": "current_1013I_visible_copy_deferred_to_R0A",
                            "must_fix_in_stage": NEXT_STAGE,
                        }
                    )
    return hits


def build_contract() -> dict[str, Any]:
    return {
        "contract_id": "unified_teacher_agent_and_capability_boundary_contract_1013I_R0",
        "stage": STAGE_ID,
        "generated_at": now(),
        "purpose": "Freeze teacher-visible agent naming and backend capability boundaries before candidate-card seeding continues.",
        "canonical_agent_role": "unified_teacher_agent",
        "current_display_name": CURRENT_DISPLAY_NAME,
        "display_name_status": "current_product_name",
        "rename_allowed_before_public_beta": True,
        "teacher_visible_agent_names_allowed": [CURRENT_DISPLAY_NAME],
        "deprecated_teacher_visible_agent_names": DEPRECATED_VISIBLE_NAMES,
        "legacy_alias_policy": {
            "xiaobei_legacy_status": "deprecated_internal_only",
            "xiaoping_legacy_status": "deprecated_internal_only",
            "legacy_alias_allowed_only_in_migration_map": True,
            "repo_path_rename_required_now": False,
            "global_search_replace_allowed": False,
            "historical_review_package_names_preserved": True,
        },
        "capability_boundary": {
            "front_stage_agent": "unified_teacher_agent",
            "front_stage_current_display_name": CURRENT_DISPLAY_NAME,
            "backend_capability_keys": [
                "lesson_prep",
                "classroom_companion",
                "learning_evidence",
                "assessment_review",
                "assessment_summary",
                "resource_retrieval",
                "archive",
                "export_draft",
            ],
            "lesson_prep_capability_key": "lesson_prep",
            "specialist_agent_front_stage_allowed": False,
            "specialist_capabilities_backend_only": True,
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


def build_deprecation_policy() -> dict[str, Any]:
    return {
        "policy_id": "legacy_agent_deprecation_policy_1013I_R0",
        "stage": STAGE_ID,
        "deprecated_teacher_visible_agent_names": DEPRECATED_VISIBLE_NAMES,
        "replacement": {
            "canonical_agent_role": "unified_teacher_agent",
            "current_display_name": CURRENT_DISPLAY_NAME,
        },
        "rules": [
            {
                "rule_id": "teacher_visible_copy",
                "policy": "New teacher-visible surfaces must use the current unified teacher agent display name only.",
                "allowed_names": [CURRENT_DISPLAY_NAME],
                "blocked_names": DEPRECATED_VISIBLE_NAMES,
            },
            {
                "rule_id": "historical_audit_artifacts",
                "policy": "Historical paths, review packages, stage names, and code module paths may preserve legacy names and must be marked as legacy rather than rewritten globally.",
            },
            {
                "rule_id": "backend_capability_boundary",
                "policy": "Specialist roles move behind capability keys instead of appearing as separate teacher-facing agents.",
            },
            {
                "rule_id": "hotfix_scope",
                "policy": "Current 1013I visible copy hits are acknowledged here and must be fixed in R0A, not by global replacement in R0.",
            },
        ],
    }


def build_migration_map() -> dict[str, Any]:
    return {
        "map_id": "engineering_name_migration_map_1013I_R0",
        "stage": STAGE_ID,
        "canonical_agent_role": "unified_teacher_agent",
        "current_display_name": CURRENT_DISPLAY_NAME,
        "legacy_aliases": [
            {
                "legacy_name": "小备",
                "legacy_engineering_aliases": ["xiaobei", "xiaobei_prep_assistant"],
                "new_front_stage": CURRENT_DISPLAY_NAME,
                "new_backend_capability": "lesson_prep",
                "status": "deprecated_internal_only",
                "global_search_replace_allowed": False,
            },
            {
                "legacy_name": "小评",
                "legacy_engineering_aliases": ["xiaoping"],
                "new_front_stage": CURRENT_DISPLAY_NAME,
                "new_backend_capability": "assessment_review",
                "status": "deprecated_internal_only",
                "global_search_replace_allowed": False,
            },
            {
                "legacy_name": "小管",
                "legacy_engineering_aliases": ["operations_agent"],
                "new_front_stage": CURRENT_DISPLAY_NAME,
                "new_backend_capability": "archive",
                "status": "deprecated_internal_only",
                "global_search_replace_allowed": False,
            },
            {
                "legacy_name": "小美",
                "legacy_engineering_aliases": ["art_agent"],
                "new_front_stage": CURRENT_DISPLAY_NAME,
                "new_backend_capability": "resource_retrieval",
                "status": "deprecated_internal_only",
                "global_search_replace_allowed": False,
            },
        ],
        "capability_keys": {
            "lesson_prep": "备课能力",
            "classroom_companion": "课堂伴随能力",
            "learning_evidence": "学习证据能力",
            "assessment_review": "评价能力",
            "assessment_summary": "评价汇总能力",
            "resource_retrieval": "资源检索能力",
            "archive": "归档能力",
            "export_draft": "导出草稿能力",
        },
    }


def build_scan(hits: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "scan_id": "visible_copy_naming_scan_1013I_R0",
        "stage": STAGE_ID,
        "scan_scope": [
            rel(INPUT_STAGE_DIR),
        ],
        "deprecated_names_scanned": DEPRECATED_VISIBLE_NAMES,
        "current_1013I_visible_xiaobei_hits_found": any(hit["deprecated_name"] == "小备" for hit in hits),
        "current_1013I_visible_deprecated_agent_hits_found": bool(hits),
        "current_1013I_visible_xiaobei_hits_deferred_to_R0A": any(hit["deprecated_name"] == "小备" for hit in hits),
        "current_1013I_visible_deprecated_agent_hits_deferred_to_R0A": bool(hits),
        "teacher_visible_deprecated_agent_hits_deferred": hits,
        "blocking_hits_for_R0": [],
        "teacher_visible_xiaobei_hits": [],
        "teacher_visible_deprecated_agent_hits": [],
        "notes": [
            "R0 records and contracts the naming boundary.",
            "Known current 1013I visible-copy hits are not fixed here; R0A is the visible naming hotfix stage.",
        ],
    }


def build_result(contract: dict[str, Any], scan: dict[str, Any]) -> dict[str, Any]:
    boundary = {
        "canonical_agent_role": contract["canonical_agent_role"],
        "current_display_name": contract["current_display_name"],
        "teacher_visible_agent_names_allowed": contract["teacher_visible_agent_names_allowed"],
        "deprecated_teacher_visible_agent_names": contract["deprecated_teacher_visible_agent_names"],
        "lesson_prep_capability_key": contract["capability_boundary"]["lesson_prep_capability_key"],
        "xiaobei_legacy_status": contract["legacy_alias_policy"]["xiaobei_legacy_status"],
        "xiaoping_legacy_status": contract["legacy_alias_policy"]["xiaoping_legacy_status"],
        "teacher_visible_xiaobei_hits": scan["teacher_visible_xiaobei_hits"],
        "teacher_visible_deprecated_agent_hits": scan["teacher_visible_deprecated_agent_hits"],
        "current_1013I_visible_xiaobei_hits_found": scan["current_1013I_visible_xiaobei_hits_found"],
        "current_1013I_visible_xiaobei_hits_deferred_to_R0A": scan["current_1013I_visible_xiaobei_hits_deferred_to_R0A"],
        "legacy_xiaobei_entries_marked": True,
        "legacy_alias_allowed_only_in_migration_map": True,
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
    final_pass = (
        boundary["canonical_agent_role"] == "unified_teacher_agent"
        and boundary["current_display_name"] == CURRENT_DISPLAY_NAME
        and boundary["teacher_visible_agent_names_allowed"] == [CURRENT_DISPLAY_NAME]
        and boundary["lesson_prep_capability_key"] == "lesson_prep"
        and boundary["xiaobei_legacy_status"] == "deprecated_internal_only"
        and boundary["current_1013I_visible_xiaobei_hits_found"]
        and boundary["current_1013I_visible_xiaobei_hits_deferred_to_R0A"]
        and boundary["legacy_xiaobei_entries_marked"]
        and boundary["legacy_alias_allowed_only_in_migration_map"]
        and not boundary["repo_path_rename_required_now"]
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
        "inherits_from": "1013I_TEACHER_SELF_PREP_INPUT_MINIMAL_FLOW",
        "final_status": "PASS_UNIFIED_TEACHER_AGENT_AND_CAPABILITY_BOUNDARY_CONTRACT" if final_pass else "FAIL_UNIFIED_TEACHER_AGENT_AND_CAPABILITY_BOUNDARY_CONTRACT",
        "next_stage": NEXT_STAGE,
        **boundary,
    }


def build_contract_markdown(contract: dict[str, Any], migration_map: dict[str, Any]) -> str:
    capabilities = migration_map["capability_keys"]
    lines = [
        "# Unified Teacher Agent and Capability Boundary Contract",
        "",
        f"- STAGE: `{STAGE_ID}`",
        "- Contract type: naming and capability boundary only.",
        "- Runtime/apply status: no provider/model call, no formal apply, no lesson body/html write.",
        "",
        "## Canonical Role",
        "",
        "```json",
        json.dumps(
            {
                "canonical_agent_role": contract["canonical_agent_role"],
                "current_display_name": contract["current_display_name"],
                "display_name_status": contract["display_name_status"],
                "rename_allowed_before_public_beta": contract["rename_allowed_before_public_beta"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        "```",
        "",
        "## Teacher-Visible Rule",
        "",
        f"- Allowed teacher-visible agent name now: `{CURRENT_DISPLAY_NAME}`",
        "- Deprecated teacher-visible names: `小备`, `小评`, `小管`, `小美`",
        "- Legacy engineering aliases may remain only in migration maps, historical package names, paths, and review evidence.",
        "- Do not perform global search/replace across repo paths, historical audit packages, validators, or stage names.",
        "",
        "## Capability Boundary",
        "",
    ]
    for key, label in capabilities.items():
        lines.append(f"- `{key}`: {label}")
    lines.extend(
        [
            "",
            "## Next Stage",
            "",
            f"`{NEXT_STAGE}` should repair current teacher-visible copy only. It must not rename historical paths or perform a broad replacement.",
            "",
        ]
    )
    return "\n".join(lines)


def build_report(result: dict[str, Any], scan: dict[str, Any]) -> str:
    lines = [
        "# 1013I R0 Unified Teacher Agent and Capability Boundary Contract",
        "",
        f"- FINAL_STATUS: `{result['final_status']}`",
        f"- NEXT_STAGE: `{result['next_stage']}`",
        "- Boundary: contract/rules/scan/mapping only; no visible-copy hotfix yet, no provider/model, no formal apply.",
        "",
        "## Decision",
        "",
        f"- canonical_agent_role={result['canonical_agent_role']}",
        f"- current_display_name={result['current_display_name']}",
        "- teacher_visible_agent_names_allowed=小教",
        "- deprecated_teacher_visible_agent_names=小备, 小评, 小管, 小美",
        f"- lesson_prep_capability_key={result['lesson_prep_capability_key']}",
        "",
        "## Current 1013I Scan",
        "",
        f"- current_1013I_visible_xiaobei_hits_found={str(result['current_1013I_visible_xiaobei_hits_found']).lower()}",
        f"- current_1013I_visible_xiaobei_hits_deferred_to_R0A={str(result['current_1013I_visible_xiaobei_hits_deferred_to_R0A']).lower()}",
        f"- deferred_hit_count={len(scan['teacher_visible_deprecated_agent_hits_deferred'])}",
        "- blocking_hits_for_R0=0",
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
    ]
    return "\n".join(lines) + "\n"


def copy_source_delta() -> None:
    SOURCE_DELTA_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA_DIR / Path(__file__).name)


def main() -> int:
    hits = scan_current_1013i_visible_names()
    contract = build_contract()
    deprecation_policy = build_deprecation_policy()
    migration_map = build_migration_map()
    scan = build_scan(hits)
    result = build_result(contract, scan)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "unified_teacher_agent_and_capability_boundary_contract.json", contract)
    write_text(OUT_DIR / "unified_teacher_agent_and_capability_boundary_contract.md", build_contract_markdown(contract, migration_map))
    write_json(OUT_DIR / "legacy_agent_deprecation_policy.json", deprecation_policy)
    write_json(OUT_DIR / "visible_copy_naming_scan_1013I_R0.json", scan)
    write_json(OUT_DIR / "engineering_name_migration_map_1013I_R0.json", migration_map)
    write_json(OUT_DIR / "1013I_R0_result.json", result)
    write_text(OUT_DIR / "1013I_R0_report.md", build_report(result, scan))
    copy_source_delta()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
