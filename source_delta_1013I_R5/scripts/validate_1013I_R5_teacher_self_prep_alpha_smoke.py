from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R5_TEACHER_SELF_PREP_ALPHA_SMOKE"
NEXT_STAGE = "1013I_R6_TEACHER_SELF_PREP_RENDER_SURFACE_ALPHA"
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_inputs(output_root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    r4_dir = output_root / "1013I_R4_minimal_self_prep_page_fixture"
    fixture = read_json(r4_dir / "minimal_self_prep_page_fixture_1013I_R4.json")
    actions = read_json(r4_dir / "minimal_self_prep_page_actions_1013I_R4.json")
    result = read_json(r4_dir / "1013I_R4_result.json")
    return fixture, actions, result


def count_actions(actions: dict[str, Any], action_name: str) -> int:
    return sum(1 for action in actions.get("actions", []) if action.get("action") == action_name)


def build_smoke_trace(fixture: dict[str, Any], actions: dict[str, Any]) -> dict[str, Any]:
    sections = fixture["sections"]
    preview_items = sections["preview_diff_section"]["accepted_preview_items"]
    review_cards = sections["review_cards_section"]["cards"]
    revision_items = sections["revision_queue_section"]["items"]
    rejected_items = sections["rejected_items_section"]["items"]
    action_policy = actions["action_state_policy"]
    return {
        "trace_id": "self_prep_alpha_smoke_trace_1013I_R5",
        "stage": STAGE_ID,
        "source_page_fixture": "minimal_self_prep_page_fixture_1013I_R4.json",
        "source_actions": "minimal_self_prep_page_actions_1013I_R4.json",
        "steps": [
            {
                "step_id": "read_teacher_input_summary",
                "passed": bool(sections.get("teacher_input_summary")),
                "detail": "Teacher input summary is readable from fixture.",
            },
            {
                "step_id": "read_review_cards",
                "passed": len(review_cards) == 3,
                "count": len(review_cards),
            },
            {
                "step_id": "read_current_preview_items",
                "passed": len(preview_items) == 3,
                "count": len(preview_items),
                "current_primary_state": action_policy["current_primary_state"],
            },
            {
                "step_id": "read_preview_diff_cards",
                "passed": len(sections["preview_diff_section"]["preview_diff_cards"]) == 3,
                "count": len(sections["preview_diff_section"]["preview_diff_cards"]),
            },
            {
                "step_id": "read_revision_queue_as_alternate_path",
                "passed": len(revision_items) == 3 and sections["revision_queue_section"]["audit_simulated_path"],
                "count": len(revision_items),
                "alternate_path": True,
            },
            {
                "step_id": "read_rejected_items_as_alternate_path",
                "passed": len(rejected_items) == 3 and sections["rejected_items_section"]["audit_simulated_path"],
                "count": len(rejected_items),
                "alternate_path": True,
            },
            {
                "step_id": "read_revert_actions",
                "passed": count_actions(actions, "revert_preview_item") == 3,
                "count": count_actions(actions, "revert_preview_item"),
            },
            {
                "step_id": "read_revise_actions_without_provider",
                "passed": count_actions(actions, "revise_preview_item") == 3
                and all(
                    not action.get("provider_called", False) and not action.get("model_called", False)
                    for action in actions["actions"]
                    if action.get("action") == "revise_preview_item"
                ),
                "count": count_actions(actions, "revise_preview_item"),
            },
            {
                "step_id": "read_reject_actions_without_formal_apply",
                "passed": count_actions(actions, "reject_preview_item") == 3
                and all(
                    not action.get("formal_apply_performed", False)
                    for action in actions["actions"]
                    if action.get("action") == "reject_preview_item"
                ),
                "count": count_actions(actions, "reject_preview_item"),
            },
            {
                "step_id": "verify_single_current_primary_state",
                "passed": action_policy["current_primary_state"] == "accepted_to_preview_only"
                and action_policy["revision_and_reject_are_alternate_paths"]
                and action_policy["action_state_not_confusing"],
                "current_primary_state": action_policy["current_primary_state"],
            },
        ],
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "official_export_created": False,
        "official_archive_created": False,
    }


def build_state_snapshot(fixture: dict[str, Any], actions: dict[str, Any]) -> dict[str, Any]:
    sections = fixture["sections"]
    return {
        "snapshot_id": "self_prep_alpha_smoke_state_snapshot_1013I_R5",
        "stage": STAGE_ID,
        "source_page_fixture_id": fixture["page_fixture_id"],
        "teacher_input_summary_present": bool(sections.get("teacher_input_summary")),
        "review_card_count": len(sections["review_cards_section"]["cards"]),
        "preview_diff_card_count": len(sections["preview_diff_section"]["preview_diff_cards"]),
        "revision_queue_count": len(sections["revision_queue_section"]["items"]),
        "rejected_items_count": len(sections["rejected_items_section"]["items"]),
        "revert_action_count": count_actions(actions, "revert_preview_item"),
        "revise_action_count": count_actions(actions, "revise_preview_item"),
        "reject_action_count": count_actions(actions, "reject_preview_item"),
        "current_primary_state": actions["action_state_policy"]["current_primary_state"],
        "revision_and_reject_are_alternate_paths": actions["action_state_policy"]["revision_and_reject_are_alternate_paths"],
        "action_state_not_confusing": actions["action_state_policy"]["action_state_not_confusing"],
        "agent_role": fixture["agent_role"],
        "assistant_profile": fixture["assistant_profile"],
        "active_space": fixture["active_space"],
        "active_capability": fixture["active_capability"],
        "preview_only": fixture["boundary_flags"]["preview_only"],
        "fixture_only": fixture["boundary_flags"]["fixture_only"],
        "formal_apply_allowed": actions["formal_apply_allowed"],
        "provider_call_allowed": actions["provider_call_allowed"],
        "model_call_allowed": actions["model_call_allowed"],
    }


def scan_deprecated(payload: Any) -> list[str]:
    text = json.dumps(payload, ensure_ascii=False)
    return [name for name in DEPRECATED_VISIBLE_NAMES if name in text]


def has_legacy_agent_field(payload: Any) -> bool:
    if isinstance(payload, dict):
        return "agent" in payload or any(has_legacy_agent_field(value) for value in payload.values())
    if isinstance(payload, list):
        return any(has_legacy_agent_field(item) for item in payload)
    return False


def build_result(
    fixture: dict[str, Any],
    r4_result: dict[str, Any],
    trace: dict[str, Any],
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    hits = sorted(set(scan_deprecated(trace) + scan_deprecated(snapshot)))
    legacy_agent = has_legacy_agent_field(trace) or has_legacy_agent_field(snapshot)
    steps_passed = all(step.get("passed") for step in trace["steps"])
    boundary = {
        "alpha_smoke_trace_created": True,
        "alpha_smoke_state_snapshot_created": True,
        "alpha_smoke_steps_passed": steps_passed,
        "teacher_input_summary_present": snapshot["teacher_input_summary_present"],
        "review_card_count": snapshot["review_card_count"],
        "preview_diff_card_count": snapshot["preview_diff_card_count"],
        "revision_queue_count": snapshot["revision_queue_count"],
        "rejected_items_count": snapshot["rejected_items_count"],
        "revert_action_count": snapshot["revert_action_count"],
        "revise_action_count": snapshot["revise_action_count"],
        "reject_action_count": snapshot["reject_action_count"],
        "current_primary_state": snapshot["current_primary_state"],
        "revision_and_reject_are_alternate_paths": snapshot["revision_and_reject_are_alternate_paths"],
        "action_state_not_confusing": snapshot["action_state_not_confusing"],
        "agent_role": snapshot["agent_role"],
        "assistant_profile_present": bool(snapshot["assistant_profile"]),
        "assistant_profile_display_name": snapshot["assistant_profile"].get("display_name"),
        "active_space": snapshot["active_space"],
        "active_capability": snapshot["active_capability"],
        "teacher_visible_deprecated_agent_hits": hits,
        "legacy_agent_field_present": legacy_agent,
        "preview_only": snapshot["preview_only"],
        "fixture_only": snapshot["fixture_only"],
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "official_export_created": False,
        "official_archive_created": False,
        "main_project_pushed": False,
    }
    final_pass = (
        boundary["alpha_smoke_trace_created"]
        and boundary["alpha_smoke_state_snapshot_created"]
        and boundary["alpha_smoke_steps_passed"]
        and r4_result["final_status"] == "PASS_1013I_R4_MINIMAL_SELF_PREP_PAGE_FIXTURE"
        and boundary["teacher_input_summary_present"]
        and boundary["review_card_count"] == 3
        and boundary["preview_diff_card_count"] == 3
        and boundary["revision_queue_count"] == 3
        and boundary["rejected_items_count"] == 3
        and boundary["revert_action_count"] == 3
        and boundary["revise_action_count"] == 3
        and boundary["reject_action_count"] == 3
        and boundary["current_primary_state"] == "accepted_to_preview_only"
        and boundary["revision_and_reject_are_alternate_paths"]
        and boundary["action_state_not_confusing"]
        and boundary["agent_role"] == "unified_teacher_agent"
        and boundary["assistant_profile_present"]
        and boundary["assistant_profile_display_name"] == "小教"
        and boundary["active_space"] == "prep_room"
        and boundary["active_capability"] == "lesson_prep"
        and not boundary["teacher_visible_deprecated_agent_hits"]
        and not boundary["legacy_agent_field_present"]
        and boundary["preview_only"]
        and boundary["fixture_only"]
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
                "official_export_created",
                "official_archive_created",
                "main_project_pushed",
            ]
        )
    )
    return {
        "stage": STAGE_ID,
        "generated_at": now(),
        "inherits_from": "1013I_R4_MINIMAL_SELF_PREP_PAGE_FIXTURE",
        "final_status": "PASS_1013I_R5_TEACHER_SELF_PREP_ALPHA_SMOKE" if final_pass else "FAIL_1013I_R5_TEACHER_SELF_PREP_ALPHA_SMOKE",
        "next_stage": NEXT_STAGE,
        **boundary,
    }


def build_report(result: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# 1013I R5 Teacher Self Prep Alpha Smoke",
            "",
            f"- FINAL_STATUS: `{result['final_status']}`",
            f"- NEXT_STAGE: `{result['next_stage']}`",
            "- Boundary: fixture-only alpha smoke; no provider/model, no formal apply, no writes.",
            "",
            "## Smoke Path",
            "",
            f"- teacher_input_summary_present={str(result['teacher_input_summary_present']).lower()}",
            f"- review_card_count={result['review_card_count']}",
            f"- preview_diff_card_count={result['preview_diff_card_count']}",
            f"- revision_queue_count={result['revision_queue_count']}",
            f"- rejected_items_count={result['rejected_items_count']}",
            f"- revert_action_count={result['revert_action_count']}",
            f"- revise_action_count={result['revise_action_count']}",
            f"- reject_action_count={result['reject_action_count']}",
            "",
            "## State Clarity",
            "",
            f"- current_primary_state={result['current_primary_state']}",
            f"- revision_and_reject_are_alternate_paths={str(result['revision_and_reject_are_alternate_paths']).lower()}",
            f"- action_state_not_confusing={str(result['action_state_not_confusing']).lower()}",
            "",
            "## Boundary Flags",
            "",
            f"- preview_only={str(result['preview_only']).lower()}",
            f"- fixture_only={str(result['fixture_only']).lower()}",
            f"- provider_called={str(result['provider_called']).lower()}",
            f"- model_called={str(result['model_called']).lower()}",
            f"- formal_apply_performed={str(result['formal_apply_performed']).lower()}",
            f"- lesson_body_modified={str(result['lesson_body_modified']).lower()}",
            f"- html_body_modified={str(result['html_body_modified']).lower()}",
            f"- database_written={str(result['database_written']).lower()}",
            f"- memory_written={str(result['memory_written']).lower()}",
            f"- feishu_written={str(result['feishu_written']).lower()}",
            f"- official_export_created={str(result['official_export_created']).lower()}",
            f"- official_archive_created={str(result['official_archive_created']).lower()}",
            "",
        ]
    )


def copy_source_delta(root: Path, output_root: Path) -> None:
    source_delta_dir = output_root / "source_delta_1013I_R5" / "scripts"
    source_delta_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "scripts" / Path(__file__).name, source_delta_dir / Path(__file__).name)


def run(root: Path) -> int:
    output_root = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    out_dir = output_root / "1013I_R5_teacher_self_prep_alpha_smoke"
    fixture, actions, r4_result = load_inputs(output_root)
    trace = build_smoke_trace(fixture, actions)
    snapshot = build_state_snapshot(fixture, actions)
    result = build_result(fixture, r4_result, trace, snapshot)

    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "self_prep_alpha_smoke_trace_1013I_R5.json", trace)
    write_json(out_dir / "self_prep_alpha_smoke_state_snapshot_1013I_R5.json", snapshot)
    write_json(out_dir / "1013I_R5_result.json", result)
    write_text(out_dir / "1013I_R5_report.md", build_report(result))
    copy_source_delta(root, output_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=None)
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else repo_root_from_script()
    return run(root)


if __name__ == "__main__":
    raise SystemExit(main())
