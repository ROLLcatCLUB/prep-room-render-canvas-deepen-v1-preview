from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
SOURCE_DIR = OUTPUT_ROOT / "1013I_R0A1_request_id_trace_alignment_hotfix"
OUT_DIR = OUTPUT_ROOT / "1013I_R1_candidate_card_seed_from_self_prep_request"
SOURCE_DELTA_DIR = OUTPUT_ROOT / "source_delta_1013I_R1" / "scripts"

STAGE_ID = "1013I_R1_CANDIDATE_CARD_SEED_FROM_SELF_PREP_REQUEST"
NEXT_STAGE = "1013I_R2_TEACHER_REVIEW_CARD_SURFACE_FROM_SEED"
SOURCE_REQUEST_FILE = "teacher_self_prep_request_1013I_R0A1.json"
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


def assistant_context(teacher_input: dict[str, Any]) -> dict[str, Any]:
    return {
        "agent_role": teacher_input["agent_role"],
        "assistant_profile": teacher_input["assistant_profile"],
        "active_space": teacher_input["active_space"],
        "active_capability": teacher_input["active_capability"],
    }


def build_candidate_cards(request: dict[str, Any]) -> list[dict[str, Any]]:
    teacher_input = request["teacher_input"]
    context = assistant_context(teacher_input)
    common = {
        "source_request_id": request["request_id"],
        "source_request_file": SOURCE_REQUEST_FILE,
        "stage": STAGE_ID,
        "seed_only": True,
        "teacher_review_required": True,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        **context,
    }
    return [
        {
            **common,
            "seed_id": "candidate_seed_learning_problem_1013I_R1",
            "card_type": "learning_problem_seed",
            "target_section": "本课先解决什么",
            "seed_title": f"{teacher_input['lesson_title']}：先把颜色感受说成理由",
            "teacher_visible_prompt": "学生这节课最先要解决的学习问题是什么？",
            "seed_basis": [
                {"field": "lesson_title", "value": teacher_input["lesson_title"]},
                {"field": "class_profile_hint", "value": teacher_input["class_profile_hint"]},
                {"field": "teacher_ideas", "value": teacher_input["teacher_ideas"]},
            ],
            "draft_seed": "围绕颜色带来的感受展开，让学生从说颜色名称和喜欢不喜欢，推进到能说出温暖、清凉、安静、热烈等感受，并给出一个理由。",
            "risk_note": "避免把学习问题写成成人化概念解释；保持三年级学生能说、能试、能展示。",
            "next_review_action_options": ["accept_to_review_surface", "revise_seed", "reject_seed"],
        },
        {
            **common,
            "seed_id": "candidate_seed_material_scaffold_1013I_R1",
            "card_type": "material_scaffold_seed",
            "target_section": "材料与支架",
            "seed_title": "先轻材料，再加生活图例",
            "teacher_visible_prompt": "材料和支架怎样既轻又能帮学生说出理由？",
            "seed_basis": [
                {"field": "existing_materials", "value": teacher_input["existing_materials"]},
                {"field": "resource_preferences", "value": teacher_input["resource_preferences"]},
                {"field": "classroom_constraints", "value": teacher_input["classroom_constraints"]},
            ],
            "draft_seed": "先用色卡和感受词卡建立基础表达，再把生活图片作为小组加料材料；学习单只保留感受词、理由句和一个小观察。",
            "risk_note": "避免材料堆叠成公开课式复杂流程；常态课优先保证学生有时间观察、表达和调整。",
            "next_review_action_options": ["accept_to_review_surface", "revise_seed", "reject_seed"],
        },
        {
            **common,
            "seed_id": "candidate_seed_review_chain_1013I_R1",
            "card_type": "review_chain_seed",
            "target_section": "展示与评价",
            "seed_title": "展示评价控制在短链路",
            "teacher_visible_prompt": "展示评价怎样不拖长，同时留下学习证据？",
            "seed_basis": [
                {"field": "classroom_constraints", "value": teacher_input["classroom_constraints"]},
                {"field": "preferred_depth", "value": teacher_input["preferred_depth"]},
                {"field": "active_capability", "value": teacher_input["active_capability"]},
            ],
            "draft_seed": "展示评价控制在 5 分钟内，优先让学生说一种颜色感受和一个理由；教师只收集能证明学生从名称走向感受表达的证据。",
            "risk_note": "避免评价维度过多，导致课堂结尾变成泛泛夸奖或复杂量表。",
            "next_review_action_options": ["accept_to_review_surface", "revise_seed", "reject_seed"],
        },
    ]


def build_seed_bundle(request: dict[str, Any], cards: list[dict[str, Any]]) -> dict[str, Any]:
    teacher_input = request["teacher_input"]
    return {
        "bundle_id": "candidate_card_seed_bundle_1013I_R1",
        "stage": STAGE_ID,
        "source_request_file": SOURCE_REQUEST_FILE,
        "source_request_id": request["request_id"],
        "original_request_id": request.get("original_request_id"),
        "request_id_trace_aligned": bool(request.get("trace_alignment", {}).get("request_id_trace_aligned")),
        "agent_role": teacher_input["agent_role"],
        "assistant_profile": teacher_input["assistant_profile"],
        "active_space": teacher_input["active_space"],
        "active_capability": teacher_input["active_capability"],
        "lesson_context": {
            "grade_level": teacher_input["grade_level"],
            "subject": teacher_input["subject"],
            "lesson_title": teacher_input["lesson_title"],
            "lesson_count": teacher_input["lesson_count"],
            "unit_or_textbook_context": teacher_input["unit_or_textbook_context"],
            "preferred_depth": teacher_input["preferred_depth"],
        },
        "candidate_cards": cards,
        "seed_only": True,
        "teacher_review_required": True,
        "can_enter_review_surface_next": True,
        "formal_apply_allowed": False,
    }


def build_trace(request: dict[str, Any], cards: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "trace_id": "candidate_card_seed_trace_1013I_R1",
        "stage": STAGE_ID,
        "source_request_file": SOURCE_REQUEST_FILE,
        "source_request_id": request["request_id"],
        "original_request_id": request.get("original_request_id"),
        "seed_count": len(cards),
        "seed_ids": [card["seed_id"] for card in cards],
        "field_to_seed_mapping": [
            {"field": "class_profile_hint", "seed_id": "candidate_seed_learning_problem_1013I_R1"},
            {"field": "teacher_ideas", "seed_id": "candidate_seed_learning_problem_1013I_R1"},
            {"field": "existing_materials", "seed_id": "candidate_seed_material_scaffold_1013I_R1"},
            {"field": "resource_preferences", "seed_id": "candidate_seed_material_scaffold_1013I_R1"},
            {"field": "classroom_constraints", "seed_id": "candidate_seed_review_chain_1013I_R1"},
            {"field": "preferred_depth", "seed_id": "candidate_seed_review_chain_1013I_R1"},
        ],
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
    }


def build_review_bridge(bundle: dict[str, Any]) -> dict[str, Any]:
    return {
        "bridge_id": "candidate_seed_to_teacher_review_surface_bridge_1013I_R1",
        "stage": STAGE_ID,
        "source_bundle_id": bundle["bundle_id"],
        "next_stage": NEXT_STAGE,
        "cards_ready_for_review_surface": True,
        "review_surface_should_show": [
            "source teacher input",
            "candidate seed title",
            "draft seed",
            "seed basis",
            "risk note",
            "teacher action options",
        ],
        "teacher_action_options": ["accept_to_review_surface", "revise_seed", "reject_seed"],
        "preview_apply_allowed": False,
        "formal_apply_allowed": False,
    }


def scan_for_deprecated(payload: Any) -> list[str]:
    text = json.dumps(payload, ensure_ascii=False)
    return [name for name in DEPRECATED_VISIBLE_NAMES if name in text]


def has_legacy_agent_field(payload: Any) -> bool:
    if isinstance(payload, dict):
        return "agent" in payload or any(has_legacy_agent_field(value) for value in payload.values())
    if isinstance(payload, list):
        return any(has_legacy_agent_field(item) for item in payload)
    return False


def build_result(
    request: dict[str, Any],
    bundle: dict[str, Any],
    trace: dict[str, Any],
    bridge: dict[str, Any],
) -> dict[str, Any]:
    hits = sorted(set(scan_for_deprecated(bundle) + scan_for_deprecated(trace) + scan_for_deprecated(bridge)))
    legacy_agent = has_legacy_agent_field(bundle) or has_legacy_agent_field(trace) or has_legacy_agent_field(bridge)
    teacher_input = request["teacher_input"]
    boundary = {
        "candidate_card_seed_created": True,
        "candidate_seed_bundle_created": bool(bundle),
        "candidate_seed_trace_created": bool(trace),
        "candidate_seed_review_bridge_created": bool(bridge),
        "candidate_card_seed_count": len(bundle["candidate_cards"]),
        "source_request_file": SOURCE_REQUEST_FILE,
        "source_request_id": request["request_id"],
        "original_request_id": request.get("original_request_id"),
        "request_id_trace_aligned": bool(request.get("trace_alignment", {}).get("request_id_trace_aligned")),
        "agent_role": teacher_input.get("agent_role"),
        "assistant_profile_present": bool(teacher_input.get("assistant_profile")),
        "active_space": teacher_input.get("active_space"),
        "active_capability": teacher_input.get("active_capability"),
        "teacher_visible_deprecated_agent_hits": hits,
        "legacy_agent_field_present": legacy_agent,
        "seed_only": True,
        "teacher_review_required": True,
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
        boundary["candidate_card_seed_created"]
        and boundary["candidate_seed_bundle_created"]
        and boundary["candidate_seed_trace_created"]
        and boundary["candidate_seed_review_bridge_created"]
        and boundary["candidate_card_seed_count"] >= 3
        and boundary["source_request_file"] == SOURCE_REQUEST_FILE
        and boundary["source_request_id"] == "teacher_self_prep_request_1013I_R0A"
        and boundary["request_id_trace_aligned"]
        and boundary["agent_role"] == "unified_teacher_agent"
        and boundary["assistant_profile_present"]
        and boundary["active_space"] == "prep_room"
        and boundary["active_capability"] == "lesson_prep"
        and not boundary["teacher_visible_deprecated_agent_hits"]
        and not boundary["legacy_agent_field_present"]
        and boundary["seed_only"]
        and boundary["teacher_review_required"]
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
        "inherits_from": "1013I_R0A1_REQUEST_ID_TRACE_ALIGNMENT_HOTFIX",
        "final_status": "PASS_1013I_R1_CANDIDATE_CARD_SEED_FROM_SELF_PREP_REQUEST" if final_pass else "FAIL_1013I_R1_CANDIDATE_CARD_SEED_FROM_SELF_PREP_REQUEST",
        "next_stage": NEXT_STAGE,
        **boundary,
    }


def build_report(result: dict[str, Any], bundle: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# 1013I R1 Candidate Card Seed From Self Prep Request",
            "",
            f"- FINAL_STATUS: `{result['final_status']}`",
            f"- NEXT_STAGE: `{result['next_stage']}`",
            "- Boundary: candidate-card seed only; no provider/model call, no formal apply, no lesson body/html write.",
            "",
            "## Source",
            "",
            f"- source_request_file={result['source_request_file']}",
            f"- source_request_id={result['source_request_id']}",
            f"- original_request_id={result['original_request_id']}",
            f"- request_id_trace_aligned={str(result['request_id_trace_aligned']).lower()}",
            "",
            "## Candidate Seeds",
            "",
            f"- candidate_card_seed_count={result['candidate_card_seed_count']}",
            f"- seed_ids={', '.join(card['seed_id'] for card in bundle['candidate_cards'])}",
            "",
            "## Boundary Flags",
            "",
            f"- agent_role={result['agent_role']}",
            f"- assistant_profile_present={str(result['assistant_profile_present']).lower()}",
            f"- active_space={result['active_space']}",
            f"- active_capability={result['active_capability']}",
            f"- teacher_visible_deprecated_agent_hits={result['teacher_visible_deprecated_agent_hits']}",
            f"- legacy_agent_field_present={str(result['legacy_agent_field_present']).lower()}",
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
    request = read_json(SOURCE_DIR / SOURCE_REQUEST_FILE)
    cards = build_candidate_cards(request)
    bundle = build_seed_bundle(request, cards)
    trace = build_trace(request, cards)
    bridge = build_review_bridge(bundle)
    result = build_result(request, bundle, trace, bridge)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "candidate_card_seed_1013I_R1.json", cards)
    write_json(OUT_DIR / "candidate_card_seed_bundle_1013I_R1.json", bundle)
    write_json(OUT_DIR / "candidate_card_seed_trace_1013I_R1.json", trace)
    write_json(OUT_DIR / "candidate_seed_to_teacher_review_surface_bridge_1013I_R1.json", bridge)
    write_json(OUT_DIR / "1013I_R1_result.json", result)
    write_text(OUT_DIR / "1013I_R1_report.md", build_report(result, bundle))
    copy_source_delta()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
