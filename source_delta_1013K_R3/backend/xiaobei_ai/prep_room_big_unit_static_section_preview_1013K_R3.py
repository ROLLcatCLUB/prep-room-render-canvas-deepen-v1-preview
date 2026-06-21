from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R3_BIG_UNIT_CANDIDATE_ENVELOPE_TO_STATIC_SECTION_PREVIEW"


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
        "r2_result": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R2_curriculum_profile_to_big_unit_candidate_envelope/1013K_R2_result.json",
        ),
        "r2_policy": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R2_curriculum_profile_to_big_unit_candidate_envelope/"
            "candidate_generation_policy_1013K_R2.json",
        ),
        "r2_context": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R2_curriculum_profile_to_big_unit_candidate_envelope/"
            "prompt_context_pack_1013K_R2.json",
        ),
        "r2_bundle": _source_path(
            root,
            "outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/"
            "1013K_R2_curriculum_profile_to_big_unit_candidate_envelope/"
            "big_unit_candidate_envelope_bundle_1013K_R2.json",
        ),
    }
    missing = [str(path) for path in sources.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing static section preview sources: {missing}")
    return {key: _read_json(path) for key, path in sources.items()}


def boundary_flags() -> dict[str, bool]:
    return {
        "static_preview_fixture_only": True,
        "degraded_preview_only": True,
        "teacher_review_required": True,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "model_candidate_text_generated": False,
        "unit_package_written": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "runtime_schema_applied": False,
        "official_curriculum_claim_created": False,
        "full_standard_text_dumped_to_prompt": False,
        "main_project_pushed": False,
        "github_upload_deferred_until_milestone": True,
    }


def profile() -> dict[str, Any]:
    return {
        "agent_role": "unified_teacher_agent",
        "assistant_profile": {
            "display_name": "小教",
            "display_name_customizable": True,
            "wake_name": "小教",
            "voice_profile_id": None,
            "tts_enabled": False,
        },
        "active_space": "prep_room",
        "active_capability": "lesson_prep",
    }


STATIC_PREVIEW_TEXT = {
    "curriculum_basis": [
        "本单元先按艺术课程方向生成预览：通过观察、比较、尝试和表达，让学生理解色彩组合会改变画面感觉，并尝试用色彩表达一种较明确的情绪或氛围。",
        "具体课标来源和教材锚点仍需教师补充或确认；确认前，这一段只作为大单元预览内容。",
    ],
    "core_literacy_goals": [
        "审美感知：能感受不同色彩组合带来的冷暖、轻重、热烈、安静等视觉意味。",
        "艺术表现：能选择一组颜色表达明确感觉，并说明自己的选色理由。",
        "创意实践：能在比较、试验和反馈中调整色彩搭配。",
        "文化理解：能发现色彩感受与生活场景、作品情境有关。",
    ],
    "student_starting_point": [
        "三年级学生通常能说出“红色热闹、蓝色安静”这样的直观感受，但容易停留在“好看、鲜艳、漂亮”等笼统判断。",
        "本单元重点帮助学生从“我觉得”走向“我能说明为什么”。",
    ],
    "unit_questions": [
        "颜色为什么会让人产生不同感觉？",
        "我们怎样用颜色把一种感觉表达出来？",
        "改动一处颜色，画面的意味为什么会变化？",
    ],
    "knowledge_and_skills": [
        "认识色彩组合带来的视觉差异，能用冷暖、强弱、明暗、轻重等词语描述色彩感觉。",
        "能在观察和比较中发现颜色搭配的变化，并用 3 到 4 种颜色完成一次小型色彩表达。",
    ],
    "performance_task": [
        "学生完成一件“色彩感觉”小作品，并用一句到几句话说明：我用了哪些颜色、想表达什么感觉、为什么这样搭配。",
        "如果时间允许，再根据同伴或教师反馈调整一处颜色，并说明为什么改。",
    ],
    "learning_progression": [
        "感受：看生活图片、作品、色卡或真实物件，先说直观感受。",
        "比较：比较不同色彩组合，发现搭配变化会改变画面感觉。",
        "表现：围绕一种感觉完成色彩实验或小作品。",
        "修订：展示作品，说出理由，根据反馈调整一处颜色。",
    ],
    "lesson_task_chain": [
        "1-1 色彩初体验：打开经验，建立感受语言，让学生说出颜色带来的直观感觉。",
        "1-2 色彩的感觉：比较变化，发现色彩组合会改变画面意味。",
        "1-3 色彩表达：完成表达，展示并修订，用色彩表达一种明确感受。",
    ],
    "assessment_evidence": [
        "能说出色彩带来的感觉；能说明自己的选色理由；学习单留下观察和选择记录。",
        "作品呈现较明确的视觉意味；学生能根据反馈做出一次可见调整。",
    ],
    "materials_and_scaffolds": [
        "建议准备生活色彩图片、艺术作品图像、不同色卡组合、学生作品正反例、简短学习单和展示评价句式。",
        "学习单可以很轻：我看到的颜色；我感受到的画面；我为什么这样选；我还想改哪里。",
    ],
}


RISK_NOTES = {
    "curriculum_basis": "课标依据仍需教师补充来源或确认，当前不得视为正式课标引用。",
    "core_literacy_goals": "核心素养表述要保持可观察，避免写成口号。",
    "student_starting_point": "学情为常见三年级判断，真实班级差异需教师补充。",
    "unit_questions": "单元问题应带动连续学习，不应退回知识问答。",
    "knowledge_and_skills": "避免越级进入复杂色彩理论。",
    "performance_task": "任务要适合常态课时长，不能变成过重公开课项目。",
    "learning_progression": "学习推进仍需结合真实课时数量调整。",
    "lesson_task_chain": "课时安排未确认前，只能作为 3 课时临时预览。",
    "assessment_evidence": "评价证据应服务观察和修改，不是正式评分表。",
    "materials_and_scaffolds": "材料清单需随教材页、教参和课堂条件修正。",
}


def build_static_section_preview_bundle(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    sources = _load_sources(root)
    context = sources["r2_context"]["teacher_visible_context"]
    bundle = sources["r2_bundle"]
    sections = []
    for envelope in bundle.get("envelopes", []):
        target_key = envelope["target_key"]
        body = STATIC_PREVIEW_TEXT.get(target_key, [envelope["source_intent"]])
        sections.append(
            {
                "section_preview_id": f"static_section_preview_{target_key}_1013K_R3",
                "source_envelope_id": envelope["envelope_id"],
                "order": envelope["order"],
                "target_key": target_key,
                "teacher_label": envelope["teacher_label"],
                "display_mode": "main_reading_surface_preview",
                "status_label": "临时预览",
                "degraded_preview_label_required": True,
                "teacher_review_required": True,
                "static_preview_fixture_text_created": True,
                "model_candidate_text_generated": False,
                "summary": body[0],
                "body_paragraphs": body,
                "risk_note": RISK_NOTES.get(target_key, "教师确认前不写入正式备课本。"),
                "source_context": {
                    "unit_theme": context["unit_theme"],
                    "lesson_title": context["lesson_title"],
                    "core_literacy_focus": context["core_literacy_focus"],
                    "learning_task_direction": context["learning_task_direction"],
                },
                "teacher_action_options": ["采纳到预览", "再改一版", "暂不采用"],
                "writes_unit_package": False,
                "writes_lesson_body": False,
            }
        )
    return {
        "bundle_id": "big_unit_static_section_preview_bundle_1013K_R3",
        "stage": STAGE_ID,
        "source_bundle_id": bundle["bundle_id"],
        "section_count": len(sections),
        "sections": sections,
        "main_reading_surface_ready": True,
        "normal_candidate_generation_allowed": False,
        "degraded_preview_only": True,
        **boundary_flags(),
        **profile(),
    }


def build_preview_review_actions(root: Path | None = None) -> dict[str, Any]:
    preview_bundle = build_static_section_preview_bundle(root)
    actions = []
    for section in preview_bundle["sections"]:
        actions.append(
            {
                "section_preview_id": section["section_preview_id"],
                "actions": [
                    {
                        "action": "accept_to_preview",
                        "teacher_label": "采纳到预览",
                        "allowed_now": True,
                        "formal_apply_performed": False,
                        "writes_unit_package": False,
                        "writes_lesson_body": False,
                    },
                    {
                        "action": "revise",
                        "teacher_label": "再改一版",
                        "allowed_now": True,
                        "formal_apply_performed": False,
                        "writes_unit_package": False,
                        "writes_lesson_body": False,
                    },
                    {
                        "action": "reject",
                        "teacher_label": "暂不采用",
                        "allowed_now": True,
                        "formal_apply_performed": False,
                        "writes_unit_package": False,
                        "writes_lesson_body": False,
                    },
                ],
            }
        )
    return {
        "action_surface_id": "big_unit_static_section_preview_actions_1013K_R3",
        "stage": STAGE_ID,
        "source_bundle_id": preview_bundle["bundle_id"],
        "section_action_count": len(actions),
        "actions": actions,
        "preview_only_actions": True,
        **boundary_flags(),
        **profile(),
    }


def build_static_preview_trace(root: Path | None = None) -> dict[str, Any]:
    preview_bundle = build_static_section_preview_bundle(root)
    actions = build_preview_review_actions(root)
    return {
        "trace_id": "big_unit_static_section_preview_trace_1013K_R3",
        "stage": STAGE_ID,
        "events": [
            {
                "event_id": "r3_event_01_envelopes_loaded",
                "event_type": "read_r2_candidate_envelopes",
                "section_count": preview_bundle["section_count"],
                "side_effects_performed": False,
            },
            {
                "event_id": "r3_event_02_static_preview_text_created",
                "event_type": "deterministic_static_fixture_preview",
                "model_candidate_text_generated": False,
                "section_count": preview_bundle["section_count"],
                "side_effects_performed": False,
            },
            {
                "event_id": "r3_event_03_review_actions_created",
                "event_type": "preview_only_review_actions",
                "section_action_count": actions["section_action_count"],
                "side_effects_performed": False,
            },
        ],
        "side_effects_performed": False,
        "model_candidate_text_generated": False,
        "provider_called": False,
        "model_called": False,
        **boundary_flags(),
        **profile(),
    }


def build_big_unit_candidate_envelope_to_static_section_preview(root: Path | None = None) -> dict[str, Any]:
    root = (root or _repo_root_from_module()).resolve()
    return {
        "stage": STAGE_ID,
        "static_section_preview_bundle": build_static_section_preview_bundle(root),
        "preview_review_actions": build_preview_review_actions(root),
        "static_preview_trace": build_static_preview_trace(root),
        "boundary": boundary_flags(),
    }
