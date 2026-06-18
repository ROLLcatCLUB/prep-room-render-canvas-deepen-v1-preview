from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6E_OFFICIAL_UNIT_MATERIAL_READONLY_EXTRACTION_FIXTURE"


def _repo_root_from_module() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _source_path(root: Path, relative_path: str) -> Path:
    direct = root / relative_path
    if direct.exists():
        return direct
    review_prefix = "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
    if relative_path.startswith(review_prefix):
        review_root_path = root / relative_path.removeprefix(review_prefix)
        if review_root_path.exists():
            return review_root_path
    return direct


def _load_sources(root: Path) -> dict[str, Any]:
    sources = {
        "official_unit_field_dictionary_v1": _source_path(
            root, "docs/contracts/official_unit_field_dictionary_v1.json"
        ),
        "official_unit_field_prompt_standard_v1": _source_path(
            root, "docs/contracts/official_unit_field_prompt_standard_v1.json"
        ),
        "official_unit_field_question_flow_v1": _source_path(
            root, "docs/contracts/official_unit_field_question_flow_v1.json"
        ),
        "r6d_textbook_anchor_and_big_unit_contract": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013I_R6D_textbook_anchor_and_big_unit_design_chain_contract/"
            "textbook_anchor_and_big_unit_design_chain_contract_1013I_R6D.json",
        ),
        "r6d_textbook_anchor_fixture": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013I_R6D_textbook_anchor_and_big_unit_design_chain_contract/"
            "textbook_anchor_fixture_1013I_R6D.json",
        ),
    }
    missing = [str(path) for path in sources.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing readonly unit material sources: {missing}")
    return {key: _read_json(path) for key, path in sources.items()}


def build_source_index(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "source_policy": "readonly_reference_only",
        "official_claim_created": False,
        "sources": [
            {
                "source_id": "official_unit_field_dictionary_v1",
                "relative_path": "docs/contracts/official_unit_field_dictionary_v1.json",
                "source_type": "official_unit_field_contract",
                "readonly": True,
                "may_extract": [
                    "field_names",
                    "teacher_friendly_names",
                    "workbench_layers",
                    "source_basis_labels",
                    "common_mistake_warnings",
                ],
                "may_not_extract": [
                    "authoritative_curriculum_claim",
                    "final_unit_body",
                    "single_lesson_plan_body",
                ],
            },
            {
                "source_id": "official_unit_field_prompt_standard_v1",
                "relative_path": "docs/contracts/official_unit_field_prompt_standard_v1.json",
                "source_type": "prompt_wording_contract",
                "readonly": True,
                "may_extract": ["question_wording_rules", "avoid_rules", "field_prompt_shape"],
                "may_not_extract": ["provider_prompt_runtime_call", "model_generated_content"],
            },
            {
                "source_id": "official_unit_field_question_flow_v1",
                "relative_path": "docs/contracts/official_unit_field_question_flow_v1.json",
                "source_type": "teacher_question_flow_contract",
                "readonly": True,
                "may_extract": ["flow_stages", "required_fields", "teacher_confirmation_states"],
                "may_not_extract": ["teacher_answer", "confirmed_unit_design"],
            },
            {
                "source_id": "r6d_textbook_anchor_and_big_unit_contract",
                "relative_path": (
                    "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
                    "1013I_R6D_textbook_anchor_and_big_unit_design_chain_contract/"
                    "textbook_anchor_and_big_unit_design_chain_contract_1013I_R6D.json"
                ),
                "source_type": "upstream_control_contract",
                "readonly": True,
                "may_extract": [
                    "lesson_textbook_map_required_fields",
                    "unit_package_required_fields",
                    "lesson_position_required_fields",
                ],
                "may_not_extract": ["formal_apply_permission", "runtime_write_permission"],
            },
        ],
    }


def _fields_by_name(dictionary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {field.get("official_field_name", ""): field for field in dictionary.get("fields", [])}


def _field_ref(field: dict[str, Any]) -> dict[str, Any]:
    return {
        "official_field_name": field.get("official_field_name"),
        "teacher_friendly_name": field.get("teacher_friendly_name"),
        "workbench_layer": field.get("workbench_layer"),
        "source_basis": field.get("source_basis", []),
        "common_mistakes": field.get("common_mistakes", []),
    }


def build_textbook_anchor_candidates(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    dictionary_fields = _fields_by_name(sources["official_unit_field_dictionary_v1"])
    r6d_anchor = sources["r6d_textbook_anchor_fixture"]["lesson_textbook_map"]
    unit_theme = dictionary_fields.get("单元主题", {})

    return {
        "stage": STAGE_ID,
        "candidate_type": "textbook_anchor_candidates",
        "readonly_extraction_only": True,
        "verified_textbook_anchor_created": False,
        "teacher_confirmation_required": True,
        "candidates": [
            {
                "candidate_id": "textbook_anchor_candidate_color_unit_1013I_R6E",
                "source_request_lesson": {
                    "subject": r6d_anchor.get("subject"),
                    "grade": r6d_anchor.get("grade"),
                    "semester": r6d_anchor.get("semester"),
                    "lesson_code": r6d_anchor.get("lesson_code"),
                    "lesson_title": r6d_anchor.get("lesson_title"),
                },
                "candidate_anchor": {
                    "textbook_version": r6d_anchor.get("textbook_version"),
                    "unit_title_candidates": [
                        r6d_anchor.get("unit_title"),
                        "色彩的碰撞",
                    ],
                    "lesson_title_candidate": r6d_anchor.get("lesson_title"),
                    "textbook_catalog_ref": r6d_anchor.get("textbook_catalog_ref"),
                    "anchor_status": "candidate_anchor_from_official_material",
                    "teacher_confirmation_status": "pending_teacher_confirm",
                },
                "evidence_refs": [
                    {
                        "source_id": "r6d_textbook_anchor_fixture",
                        "field": "lesson_textbook_map",
                        "usage": "inherit teacher request and missing-anchor status",
                    },
                    {
                        "source_id": "official_unit_field_dictionary_v1",
                        "field_ref": _field_ref(unit_theme),
                        "usage": "extract unit theme field shape only",
                    },
                ],
                "risk_note": "Unit title candidates are not a verified textbook anchor. Teacher must confirm textbook version, unit, lesson code, and activity/page reference.",
            }
        ],
    }


def build_big_unit_chain_candidates(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    dictionary_fields = _fields_by_name(sources["official_unit_field_dictionary_v1"])
    question_flow = sources["official_unit_field_question_flow_v1"]

    stages = []
    for flow_stage in question_flow.get("flow_stages", []):
        field_refs = []
        for field_name in flow_stage.get("fields", []):
            field = dictionary_fields.get(field_name)
            if field:
                field_refs.append(_field_ref(field))
            else:
                field_refs.append(
                    {
                        "official_field_name": field_name,
                        "teacher_friendly_name": None,
                        "workbench_layer": None,
                        "source_basis": [],
                        "common_mistakes": [],
                        "missing_from_dictionary": True,
                    }
                )
        stages.append(
            {
                "stage_id": flow_stage.get("stage_id"),
                "stage_name": flow_stage.get("stage_name"),
                "ask_order": flow_stage.get("ask_order"),
                "stage_goal": flow_stage.get("stage_goal"),
                "field_candidates": field_refs,
                "teacher_confirmation_status": "pending_teacher_confirm",
            }
        )

    return {
        "stage": STAGE_ID,
        "candidate_type": "big_unit_chain_candidates",
        "readonly_extraction_only": True,
        "unit_package_created": False,
        "big_unit_body_generated": False,
        "teacher_confirmation_required": True,
        "unit_package_candidate": {
            "unit_package_id": "unit_package_candidate_1013I_R6E_color_feeling",
            "unit_title_candidates": ["多变的色彩", "色彩的碰撞"],
            "unit_task_chain_candidates": stages,
            "chain_status": "candidate_chain_from_official_material",
            "teacher_confirmation_status": "pending_teacher_confirm",
        },
    }


def build_teacher_confirmation_required_items(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    _load_sources(root)
    return {
        "stage": STAGE_ID,
        "teacher_confirmation_required": True,
        "items": [
            {
                "item_id": "confirm_textbook_version",
                "label": "确认教材版本",
                "why_required": "缺教材版本时不能把候选锚点视为正式教材锚点。",
                "blocks_normal_generation": True,
            },
            {
                "item_id": "confirm_unit_title",
                "label": "确认本课所在单元",
                "why_required": "当前存在单元标题候选，必须由教师确认本课归属。",
                "blocks_normal_generation": True,
            },
            {
                "item_id": "confirm_lesson_code_and_activity_ref",
                "label": "确认课题编号和教材活动落点",
                "why_required": "缺课题编号或活动页/活动任务时，不能进入正常单课候选生成。",
                "blocks_normal_generation": True,
            },
            {
                "item_id": "confirm_unit_task_chain",
                "label": "确认单元任务链",
                "why_required": "候选链只来自字段抽取，不等于已确认的大单元设计。",
                "blocks_normal_generation": True,
            },
            {
                "item_id": "confirm_lesson_position",
                "label": "确认本课在单元中的位置",
                "why_required": "本课是导入、探究、表现、展示评价还是综合推进，会改变候选卡范围。",
                "blocks_normal_generation": True,
            },
        ],
    }


def build_extraction_fixture(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    source_index = build_source_index(root)
    textbook_candidates = build_textbook_anchor_candidates(root)
    big_unit_candidates = build_big_unit_chain_candidates(root)
    confirmation_items = build_teacher_confirmation_required_items(root)

    return {
        "stage": STAGE_ID,
        "fixture_id": "official_unit_material_extraction_fixture_1013I_R6E",
        "source_contracts_loaded": True,
        "source_contract_count": len(source_index["sources"]),
        "official_dictionary_field_count": len(sources["official_unit_field_dictionary_v1"].get("fields", [])),
        "question_flow_stage_count": len(sources["official_unit_field_question_flow_v1"].get("flow_stages", [])),
        "readonly_extraction_only": True,
        "official_claim_created": False,
        "textbook_anchor_candidates_created": True,
        "textbook_anchor_candidate_count": len(textbook_candidates["candidates"]),
        "big_unit_chain_candidates_created": True,
        "big_unit_chain_stage_count": len(
            big_unit_candidates["unit_package_candidate"]["unit_task_chain_candidates"]
        ),
        "lesson_position_candidate_created": True,
        "lesson_position_candidate": {
            "lesson_title": "色彩的感觉",
            "candidate_position_status": "candidate_position_pending_teacher_review",
            "possible_roles": [
                "unit_entry",
                "concept_building",
                "method_learning",
                "creative_production",
                "critique_and_revision",
                "exhibition_or_reflection",
                "unknown_pending_teacher_confirm",
            ],
            "teacher_confirmation_status": "pending_teacher_confirm",
            "candidate_cards_blocked_until_confirmation": True,
        },
        "teacher_confirmation_required_items_created": True,
        "teacher_confirmation_required_item_count": len(confirmation_items["items"]),
        "normal_candidate_card_generation_allowed": False,
        "page_work_started": False,
        "page_user_gate_required_before_r6f": True,
        "boundary": boundary_flags(),
    }


def boundary_flags() -> dict[str, bool]:
    return {
        "backend_adapter_only": True,
        "readonly_extraction_only": True,
        "fixture_only": True,
        "preview_only": True,
        "actual_textbook_parsing_performed": False,
        "actual_big_unit_material_parsing_performed": False,
        "official_claim_created": False,
        "big_unit_generation_performed": False,
        "single_lesson_generation_performed": False,
        "page_work_started": False,
        "r7_visual_review_entered": False,
        "product_runtime_called": False,
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


def build_official_unit_material_readonly_extraction(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "source_index": build_source_index(root),
        "extraction_fixture": build_extraction_fixture(root),
        "textbook_anchor_candidates": build_textbook_anchor_candidates(root),
        "big_unit_chain_candidates": build_big_unit_chain_candidates(root),
        "teacher_confirmation_required_items": build_teacher_confirmation_required_items(root),
        "boundary": boundary_flags(),
    }
