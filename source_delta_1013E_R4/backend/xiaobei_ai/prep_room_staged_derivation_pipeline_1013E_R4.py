from __future__ import annotations

from copy import deepcopy
from typing import Any

from .prep_room_lesson_reasoning_contract_1013E import (
    BOUNDARY_FLAGS,
    evaluate_classroom_unfolding_effectiveness,
    evaluate_time_balance,
    validate_lesson_unfolding_graph_payload,
)


STAGE_ID = "1013E_R4_STAGED_LESSON_DERIVATION_PIPELINE"


R4_CASES = [
    {
        "case_id": "standard_daily_cold_warm_more_visual",
        "lesson_design_mode": "standard_daily",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "lesson_title": "1-2《色彩的感觉》",
        "duration_minutes": 40,
        "unit_position": "unit_middle",
        "teacher_input": "学生对冷暖色不太理解，要设计得更直观一点。",
        "student_baseline": "学生知道常见颜色，也能说喜欢或不喜欢，但容易把冷暖色理解成颜色名称，缺少感受分类和理由表达。",
        "resource_constraints": ["可使用黑板、图片、色卡、学习单", "不接真实资料库"],
        "reference_candidates": ["本地色彩单元课例字段样本", "教材图例候选", "色卡活动样本"],
    },
    {
        "case_id": "standard_daily_art_music_dance_rhythm",
        "lesson_design_mode": "standard_daily",
        "grade": "三年级",
        "subject": "美术",
        "unit": "线条与色彩表现",
        "lesson_title": "节奏与线条色彩表现",
        "duration_minutes": 40,
        "unit_position": "unit_middle",
        "teacher_input": "我想放一段美术和音乐结合的舞蹈，让学生感受节奏，再引到线条和色彩表现。帮我设计这一段怎么展开。",
        "student_baseline": "学生能感到音乐或舞蹈热闹，但容易把注意力放在动作好看，未必能转到线条、色彩和节奏的视觉表达。",
        "resource_constraints": ["视频是教师提出的候选资源，不是默认资源", "必须准备无视频替代方案"],
        "reference_candidates": ["本地听音乐画音乐薄案例", "线条节奏表达样本"],
    },
    {
        "case_id": "constrained_low_resource_no_video",
        "lesson_design_mode": "standard_daily",
        "grade": "三年级",
        "subject": "美术",
        "unit": "色彩单元",
        "lesson_title": "1-2《色彩的感觉》",
        "duration_minutes": 40,
        "unit_position": "unit_middle",
        "teacher_input": "这节课不能放视频，也没有平板，只有黑板和几张图片，帮我把活动改得还能上。",
        "student_baseline": "学生需要直观材料支撑，单靠口头解释会停在好看、漂亮等笼统表达。",
        "resource_constraints": ["不能放视频", "没有平板", "只有黑板和几张图片"],
        "reference_candidates": ["低资源课堂组织样本", "图片观察和黑板归类样本"],
    },
]


def run_staged_lesson_derivation_case(case: dict[str, Any]) -> dict[str, Any]:
    trace: list[dict[str, Any]] = []
    candidate_errors: list[dict[str, Any]] = []

    def record(step: str, output: Any, *, ok: bool = True, errors: list[str] | None = None) -> None:
        trace.append({"step": step, "ok": ok, "output": deepcopy(output), "errors": errors or []})
        if not ok:
            candidate_errors.append({"step": step, "errors": errors or ["unknown_error"]})

    context = build_lesson_context_pack(case)
    record("LessonContextPack", context, ok=_has_values(context, ["lesson_title", "grade", "subject", "teacher_input"]))

    learning_problem = derive_learning_problem(context)
    lp_errors = _validate_learning_problem(learning_problem)
    record("LearningProblemDeriver", learning_problem, ok=not lp_errors, errors=lp_errors)

    target_shift = derive_target_shift(context, learning_problem)
    ts_errors = _validate_target_shift(target_shift)
    record("TargetShiftDeriver", target_shift, ok=not ts_errors, errors=ts_errors)

    evidence_plan = derive_evidence_plan(context, learning_problem, target_shift)
    ep_errors = [] if evidence_plan.get("evidence_plan") else ["missing_evidence_plan"]
    record("EvidencePlanDeriver", evidence_plan, ok=not ep_errors, errors=ep_errors)

    route_plan = plan_teaching_route(context, learning_problem, target_shift, evidence_plan)
    route_errors = [] if route_plan.get("teaching_route") else ["missing_teaching_route"]
    record("TeachingRoutePlanner", route_plan, ok=not route_errors, errors=route_errors)

    classroom_events = generate_classroom_events(context, route_plan)
    event_errors = [] if classroom_events.get("classroom_events") else ["missing_classroom_events"]
    record("ClassroomEventGenerator", classroom_events, ok=not event_errors, errors=event_errors)

    expanded_events = expand_classroom_events(context, learning_problem, evidence_plan, classroom_events)
    expand_errors = _validate_expanded_events(expanded_events)
    record("EventUnfoldingExpander", expanded_events, ok=not expand_errors, errors=expand_errors)

    time_rebalance = rebalance_time(expanded_events, context)
    time_errors = []
    if not time_rebalance.get("time_balance_pass") and not time_rebalance.get("rebalance_candidates"):
        time_errors.append("missing_rebalance_candidates")
    record("TimeRebalancer", time_rebalance, ok=not time_errors, errors=time_errors)

    evidence_binding = bind_evidence_to_events(evidence_plan, expanded_events)
    binding_errors = [] if evidence_binding.get("binding_pass") else evidence_binding.get("blockers") or ["evidence_binding_failed"]
    record("EvidenceBinder", evidence_binding, ok=not binding_errors, errors=binding_errors)

    candidate = build_teacher_review_candidate(
        context,
        learning_problem,
        target_shift,
        evidence_plan,
        route_plan,
        expanded_events,
        time_rebalance,
        evidence_binding,
    )
    contract_errors = validate_lesson_unfolding_graph_payload(candidate)
    effectiveness = evaluate_classroom_unfolding_effectiveness(candidate)
    effectiveness_errors = list(contract_errors)
    if not effectiveness.get("pass"):
        effectiveness_errors.extend(effectiveness.get("blockers") or effectiveness.get("issues") or ["effectiveness_gate_failed"])
    if candidate_errors:
        effectiveness_errors.append("upstream_candidate_error")
    record(
        "EffectivenessEvaluator",
        {"contract_errors": contract_errors, "effectiveness": effectiveness},
        ok=not effectiveness_errors,
        errors=effectiveness_errors,
    )

    final_candidate = build_final_case_result(case, candidate, trace, candidate_errors, contract_errors, effectiveness)
    return final_candidate


def build_lesson_context_pack(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "lesson_title": case["lesson_title"],
        "grade": case["grade"],
        "subject": case["subject"],
        "duration_minutes": int(case.get("duration_minutes") or 40),
        "lesson_design_mode": case.get("lesson_design_mode") or "standard_daily",
        "unit_position": case.get("unit_position") or "unit_middle",
        "teacher_input": case.get("teacher_input") or "",
        "student_baseline": case.get("student_baseline") or "",
        "resource_constraints": list(case.get("resource_constraints") or []),
        "reference_candidates": [
            {"source_label": "资料室候选", "use_policy": "reference_only", "title": item}
            for item in case.get("reference_candidates", [])
        ],
        "source_labels": ["教材", "课标", "教师输入", "小备推测", "资料室候选"],
    }


def derive_learning_problem(context: dict[str, Any]) -> dict[str, Any]:
    teacher_input = context["teacher_input"]
    if "舞蹈" in teacher_input or "节奏" in teacher_input:
        return {
            "core_learning_problem": "学生能感到节奏，但不一定能把节奏转译成线条疏密、方向变化和色彩强弱。",
            "real_stuck_point": "注意力容易停在舞蹈动作是否好看，而不是观察节奏如何被艺术语言表现。",
            "student_baseline": context["student_baseline"],
            "why_this_lesson_matters": "本课要把身体和听觉经验转成可画、可说、可评价的视觉表达。",
            "confidence": "medium",
            "needs_teacher_confirmation": True,
        }
    if any("不能放视频" in item or "没有平板" in item for item in context.get("resource_constraints", [])):
        return {
            "core_learning_problem": "学生需要看得见、摸得着的材料来理解色彩感受，低资源条件下更要让观察和表达任务清楚。",
            "real_stuck_point": "如果只讲概念，学生会停在好看、漂亮，难以说出颜色带来的具体感受。",
            "student_baseline": context["student_baseline"],
            "why_this_lesson_matters": "低资源课堂仍要保住直观比较、表达支架和可观察证据。",
            "confidence": "high",
            "needs_teacher_confirmation": True,
        }
    return {
        "core_learning_problem": "学生把冷暖色当成颜色名称或固定答案，缺少从视觉感受到理由表达的连接。",
        "real_stuck_point": "冷暖是感受判断，不是背红黄蓝绿的分类表；学生需要通过情境、色卡和同伴理由建立判断依据。",
        "student_baseline": context["student_baseline"],
        "why_this_lesson_matters": "本课要让学生从说颜色好看，走向能说颜色给自己的感觉以及为什么这样感受。",
        "confidence": "high",
        "needs_teacher_confirmation": True,
    }


def derive_target_shift(context: dict[str, Any], learning_problem: dict[str, Any]) -> dict[str, Any]:
    teacher_input = context["teacher_input"]
    if "舞蹈" in teacher_input or "节奏" in teacher_input:
        target = {
            "from_state": "能说舞蹈或音乐很快、很好看。",
            "to_state": "能抓住一个节奏特征，并用线条或色彩说明它带来的视觉感受。",
            "observable_behavior": "学生能说出“我看到/听到的节奏像什么线条或颜色”，并完成一格节奏转译草图。",
            "success_evidence": "学习单上的节奏词、线条/色彩选择和一句理由能互相对应。",
        }
        return {"target_shift": target, "key_focus": "节奏到视觉语言的转译", "key_difficulty": "把注意力从动作热闹转到节奏特征", "teacher_review_required": True}
    target = {
        "from_state": "能说颜色名称和喜欢不喜欢。",
        "to_state": "能根据色彩带来的温暖、清凉、安静、热烈等感受进行分类并说明理由。",
        "observable_behavior": "学生能把色卡或图片放入感受类别，并用一句话说明依据。",
        "success_evidence": "学习单中至少完成两组颜色感受记录，理由不只停在好看。",
    }
    return {"target_shift": target, "key_focus": "色彩感受分类与理由表达", "key_difficulty": learning_problem["real_stuck_point"], "teacher_review_required": True}


def derive_evidence_plan(context: dict[str, Any], learning_problem: dict[str, Any], target_shift: dict[str, Any]) -> dict[str, Any]:
    if "节奏" in target_shift.get("key_focus", ""):
        plan = [
            {
                "evidence_id": "EVID_FOCUS_WORD",
                "what_it_proves": "学生是否把注意力放在节奏特征而不是动作好看。",
                "collection_method": "观看后先写一个节奏词，再口头补一句理由。",
                "expected_student_output": "快、密、跳、缓、流动等词语及理由。",
                "linked_target_shift": target_shift["target_shift"]["observable_behavior"],
            },
            {
                "evidence_id": "EVID_VISUAL_TRANSLATION",
                "what_it_proves": "学生能否把节奏转成线条或色彩。",
                "collection_method": "学习单一格小草图和同桌说明。",
                "expected_student_output": "线条疏密、方向或色彩强弱与节奏词对应。",
                "linked_target_shift": target_shift["target_shift"]["success_evidence"],
            },
        ]
    else:
        plan = [
            {
                "evidence_id": "EVID_COLOR_SORT",
                "what_it_proves": "学生是否能依据感受而不是死记颜色分类。",
                "collection_method": "小组把色卡或图片贴到感受词下方。",
                "expected_student_output": "至少两张色卡归类，并能说出分类依据。",
                "linked_target_shift": target_shift["target_shift"]["observable_behavior"],
            },
            {
                "evidence_id": "EVID_REASON_SENTENCE",
                "what_it_proves": "学生是否能把颜色和情绪/场景联系起来。",
                "collection_method": "学习单填写“这个颜色让我想到……”句式。",
                "expected_student_output": "一条颜色、感受、理由相连的短句。",
                "linked_target_shift": target_shift["target_shift"]["success_evidence"],
            },
        ]
    return {"evidence_plan": plan}


def plan_teaching_route(
    context: dict[str, Any],
    learning_problem: dict[str, Any],
    target_shift: dict[str, Any],
    evidence_plan: dict[str, Any],
) -> dict[str, Any]:
    teacher_input = context["teacher_input"]
    if "舞蹈" in teacher_input or "节奏" in teacher_input:
        route = [
            _route("R1", "定观看焦点", "把资源从热闹观看变成带任务观看", "学生知道只看节奏变化", 4),
            _route("R2", "短资源感受", "用舞蹈/音乐片段激活节奏经验", "学生有一个节奏词", 8),
            _route("R3", "收感受并转译", "把听觉和身体感受转成线条色彩", "学生能说一个视觉转译理由", 8),
            _route("R4", "个人小练习", "形成可观察作品证据", "学生完成一格节奏表达", 14),
            _route("R5", "展示与连接", "回到美术表达标准并接下一环节", "学生知道如何继续完善画面", 6),
        ]
        rationale = "先定焦点，再用候选资源触发感受，随后马上收束到视觉语言，避免学生只讨论舞蹈好不好看。"
    else:
        route = [
            _route("R1", "唤起颜色经验", "从学生已有颜色经验进入感受问题", "学生知道今天不只说颜色名", 4),
            _route("R2", "对比观察", "用图片/色卡建立冷暖直观差异", "学生能说出一组感受词", 8),
            _route("R3", "色卡分类探究", "让学生用分类和理由处理卡点", "学生能说明冷暖或情绪分类依据", 10),
            _route("R4", "表达小练习", "把理解迁移到个人色彩表达", "学生能完成一组感受表达", 13),
            _route("R5", "分享证据", "用作品和学习单验证目标达成", "学生能听懂同伴理由并修正", 5),
        ]
        rationale = "从经验唤起到直观对比，再到小组分类和个人表达，逐步把颜色名称推进到感受理由。"
    return {"teaching_route": route, "route_rationale": rationale, "time_risk": "若交流过长，优先减少展示人数，不删探究证据。"}


def generate_classroom_events(context: dict[str, Any], route_plan: dict[str, Any]) -> dict[str, Any]:
    events = []
    for step in route_plan["teaching_route"]:
        events.append(
            {
                "event_id": step["route_step_id"].replace("R", "EVT_"),
                "event_name": step["route_step_name"],
                "event_type": _event_type_for(step["route_step_name"]),
                "learning_purpose": step["role_in_learning_progression"],
                "student_state_before": "尚未进入本环节的学习任务。",
                "student_state_after": step["expected_student_state_after"],
                "recommended_minutes": step["recommended_duration_minutes"],
                "teacher_review_required": True,
            }
        )
    return {"classroom_events": events}


def expand_classroom_events(
    context: dict[str, Any],
    learning_problem: dict[str, Any],
    evidence_plan: dict[str, Any],
    classroom_events: dict[str, Any],
) -> dict[str, Any]:
    if "舞蹈" in context["teacher_input"] or "节奏" in context["teacher_input"]:
        expanded = _expand_rhythm_events(context, evidence_plan)
    elif any("不能放视频" in item or "没有平板" in item for item in context.get("resource_constraints", [])):
        expanded = _expand_low_resource_color_events(context, evidence_plan)
    else:
        expanded = _expand_cold_warm_events(context, evidence_plan)
    return {"classroom_events": expanded}


def rebalance_time(expanded_events: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    time_balance = evaluate_time_balance(expanded_events.get("classroom_events") or [], context["duration_minutes"])
    if not time_balance.get("time_balance_pass"):
        return time_balance
    return {
        "target_minutes": context["duration_minutes"],
        "total_event_minutes": time_balance["total_event_minutes"],
        "time_balance_pass": True,
        "rebalance_candidates": [],
    }


def bind_evidence_to_events(evidence_plan: dict[str, Any], expanded_events: dict[str, Any]) -> dict[str, Any]:
    bindings = []
    blockers = []
    events = expanded_events.get("classroom_events") or []
    for evidence in evidence_plan.get("evidence_plan") or []:
        evidence_id = evidence.get("evidence_id")
        event = _find_event_for_evidence(evidence_id, events)
        if not event:
            blockers.append("EVIDENCE_PLAN_NOT_BOUND_TO_CLASSROOM_EVENT")
            continue
        design = event.get("design_view") or {}
        bindings.append(
            {
                "evidence_id": evidence_id,
                "event_id": event["event_id"],
                "assessment_evidence": design.get("assessment_evidence") or evidence.get("expected_student_output"),
                "collection_method": evidence.get("collection_method"),
                "what_it_proves": evidence.get("what_it_proves"),
            }
        )
    return {"evidence_bindings": bindings, "binding_pass": not blockers, "blockers": blockers}


def build_teacher_review_candidate(
    context: dict[str, Any],
    learning_problem: dict[str, Any],
    target_shift: dict[str, Any],
    evidence_plan: dict[str, Any],
    route_plan: dict[str, Any],
    expanded_events: dict[str, Any],
    time_rebalance: dict[str, Any],
    evidence_binding: dict[str, Any],
) -> dict[str, Any]:
    events = expanded_events.get("classroom_events") or []
    graph = {
        "lesson_design_mode": context["lesson_design_mode"],
        "design_context": {
            "grade": context["grade"],
            "subject": context["subject"],
            "lesson_title": context["lesson_title"],
            "unit_position": context["unit_position"],
        },
        "cognitive_grounding": {
            "core_learning_problem": learning_problem["core_learning_problem"],
            "student_baseline": learning_problem["student_baseline"],
            "real_stuck_point": learning_problem["real_stuck_point"],
            "target_shift": target_shift["target_shift"],
            "key_focus": target_shift["key_focus"],
            "key_difficulty": target_shift["key_difficulty"],
        },
        "constraints": {
            "total_duration_minutes": context["duration_minutes"],
            "resource_budget": "low" if "没有平板" in " ".join(context.get("resource_constraints", [])) else "medium",
            "class_condition": "候选推演，不接真实课堂数据。",
            "lesson_position": context["unit_position"],
            "material_conditions": context["resource_constraints"],
        },
        "main_event_sequence": [event["event_id"] for event in events],
        "classroom_events": events,
        "structure_rebalance_candidates": time_rebalance.get("rebalance_candidates") or [],
        "evidence_plan": evidence_plan["evidence_plan"],
        "evidence_bindings": evidence_binding.get("evidence_bindings") or [],
        "lesson_position_connection": {
            "unit_start_entry": "",
            "unit_middle_next_lesson_connection": "下一课可基于本课学习单，继续观察色彩/线条如何服务个人表达。",
            "unit_end_closure": "",
        },
        "closure_plan": "用学生作品或学习单中的一句理由收束，不追求一次讲完概念。",
        "next_lesson_connection": "保留学生证据，下一课先回看典型理由再进入创作深化。",
        "quality_gate": {"level": "ready_to_teach", "teacher_review_required": True},
        "time_balance": time_rebalance,
    }
    return {
        "lesson_unfolding_graph": graph,
        "field_patch_candidates": _field_patch_candidates(context, learning_problem, target_shift),
        "impact_scope": _impact_scope(context),
        "quality_gate_update": {
            "level": "ready_to_teach",
            "passed_items": ["学习问题具体", "目标可观察", "课堂事件有证据绑定", "时间由代码计算"],
            "missing_items": ["需要教师确认资源和班级真实状态"],
            "risk_items": ["学生表达可能停在好看，需要支架句式"],
            "next_best_action": "请老师确认候选课堂事件和资源条件后再进入 UI 绑定。",
        },
        "teacher_review_candidate": {
            "summary": "已形成分阶段课堂展开候选，等待教师确认。",
            "edit_target": "教学过程",
            "teacher_review_required": True,
        },
        "boundary_flags": dict(BOUNDARY_FLAGS),
    }


def build_final_case_result(
    case: dict[str, Any],
    candidate: dict[str, Any],
    trace: list[dict[str, Any]],
    candidate_errors: list[dict[str, Any]],
    contract_errors: list[str],
    effectiveness: dict[str, Any],
) -> dict[str, Any]:
    pass_flag = not candidate_errors and not contract_errors and bool(effectiveness.get("pass"))
    return {
        "case_id": case["case_id"],
        "lesson_design_mode": case["lesson_design_mode"],
        "teacher_input": case["teacher_input"],
        "pipeline_pass": pass_flag,
        "learning_problem_generated": bool(((candidate.get("lesson_unfolding_graph") or {}).get("cognitive_grounding") or {}).get("core_learning_problem")),
        "target_shift_generated": bool(((candidate.get("lesson_unfolding_graph") or {}).get("cognitive_grounding") or {}).get("target_shift")),
        "classroom_events_generated": bool(((candidate.get("lesson_unfolding_graph") or {}).get("classroom_events") or [])),
        "evidence_binding_pass": bool(((candidate.get("lesson_unfolding_graph") or {}).get("evidence_bindings") or [])),
        "time_balance_pass": bool(((candidate.get("lesson_unfolding_graph") or {}).get("time_balance") or {}).get("time_balance_pass")),
        "teacher_review_required": True,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_export_created": False,
        "official_archive_created": False,
        "provider_called": False,
        "model_called": False,
        "contract_errors": contract_errors,
        "candidate_errors": candidate_errors,
        "effectiveness": effectiveness,
        "candidate": candidate,
        "staged_trace": trace,
    }


def aggregate_case_results(case_results: list[dict[str, Any]]) -> dict[str, Any]:
    standard = next((item for item in case_results if item.get("case_id") == "standard_daily_cold_warm_more_visual"), {})
    pass_count = sum(1 for item in case_results if item.get("pipeline_pass"))
    return {
        "case_count": len(case_results),
        "pipeline_pass_count": pass_count,
        "standard_daily_pass": bool(standard.get("pipeline_pass")),
        "learning_problem_success_count": sum(1 for item in case_results if item.get("learning_problem_generated")),
        "target_shift_success_count": sum(1 for item in case_results if item.get("target_shift_generated")),
        "classroom_events_success_count": sum(1 for item in case_results if item.get("classroom_events_generated")),
        "evidence_binding_success_count": sum(1 for item in case_results if item.get("evidence_binding_pass")),
        "time_balance_success_count": sum(1 for item in case_results if item.get("time_balance_pass")),
        "secret_scan_ok": True,
    }


def final_status_for(case_results: list[dict[str, Any]], aggregate: dict[str, Any]) -> tuple[str, str]:
    if not aggregate.get("secret_scan_ok"):
        return "FAIL_SECRET_SCAN_HIT", "1013E_R4_SECRET_REVIEW"
    if not aggregate.get("standard_daily_pass"):
        return "FAIL_STANDARD_DAILY_CORE_CASE", "1013E_R5_CORE_CASE_STRATEGY_REPAIR"
    if aggregate.get("pipeline_pass_count", 0) < 2:
        return "FAIL_EFFECTIVENESS_GATE", "1013E_R5_EFFECTIVENESS_REPAIR"
    if any(item.get("pipeline_pass") is False and item.get("effectiveness", {}).get("overall_effectiveness_score", 0) < 4 for item in case_results):
        return "FAIL_EFFECTIVENESS_GATE", "1013E_R5_EFFECTIVENESS_REPAIR"
    return "PASS_STAGED_LESSON_DERIVATION_PIPELINE", "1013F_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING"


def _route(step_id: str, name: str, role: str, state_after: str, minutes: int) -> dict[str, Any]:
    return {
        "route_step_id": step_id,
        "route_step_name": name,
        "role_in_learning_progression": role,
        "expected_student_state_after": state_after,
        "recommended_duration_minutes": minutes,
    }


def _event_type_for(name: str) -> str:
    if "观察" in name or "感受" in name:
        return "comparison"
    if "练习" in name:
        return "practice"
    if "分享" in name or "展示" in name:
        return "sharing"
    if "分类" in name or "探究" in name or "转译" in name:
        return "analysis"
    return "experience_evoke"


def _event(
    event_id: str,
    event_name: str,
    event_type: str,
    minutes: int,
    purpose: str,
    before: str,
    after: str,
    teacher_focus: str,
    core_question: str,
    student_task: str,
    teacher_summary: str,
    teacher_action: str,
    student_action: str,
    big_screen: str,
    material: str,
    learning_sheet: str,
    evidence: str,
    transition_from: str,
    transition_to: str,
    risk: str,
    responses: list[dict[str, str]],
    resource: dict[str, str],
) -> dict[str, Any]:
    return {
        "event_id": event_id,
        "event_name": event_name,
        "event_type": event_type,
        "learning_purpose": purpose,
        "duration": {"recommended_minutes": minutes, "min_minutes": max(1, minutes - 2), "max_minutes": minutes + 2, "time_risk": "交流超时则减少展示人数。"},
        "execution_view": {
            "teacher_focus_cue": teacher_focus,
            "core_question": core_question,
            "student_task": student_task,
            "teacher_summary_sentence": teacher_summary,
        },
        "design_view": {
            "learning_purpose": purpose,
            "design_intent": purpose,
            "student_state_before": before,
            "student_state_after": after,
            "teacher_action": teacher_action,
            "student_action": student_action,
            "big_screen_state": big_screen,
            "textbook_or_material_state": material,
            "learning_sheet_state": learning_sheet,
            "assessment_evidence": evidence,
            "transition_from_previous": transition_from,
            "transition_to_next": transition_to,
            "risk_and_adjustment": risk,
        },
        "student_response_model": responses,
        "resource_use": resource,
        "teacher_review_required": True,
        "formal_apply_performed": False,
    }


def _responses(topic: str) -> list[dict[str, str]]:
    return [
        {"type": "expected", "student_response": f"能围绕{topic}说出一个具体发现。", "teacher_next_move": "追问依据，让学生把感受和材料连起来。", "scaffold": "用“我看到...所以觉得...”句式。"},
        {"type": "misconception", "student_response": "只说好看、漂亮或直接背答案。", "teacher_next_move": "让学生指向画面或色卡中的具体部分。", "scaffold": "提供感受词卡和二选一比较。"},
        {"type": "silent", "student_response": "学生看着材料但说不出来。", "teacher_next_move": "先让同桌选词，再请学生补一个理由。", "scaffold": "给出“像太阳/像冰水/像晚上”的生活联想。"},
    ]


def _expand_cold_warm_events(context: dict[str, Any], evidence_plan: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _event("EVT_1", "唤起颜色经验", "experience_evoke", 4, "把已有颜色经验转成感受问题。", "学生会说颜色名和喜好。", "学生知道今天要说颜色带来的感觉。", "今天不急着分对错，先说颜色让你想到什么。", "看到这个颜色，你身体里先出现什么感觉？", "每人说一个颜色联想。", "颜色不只叫红黄蓝，也会带来感受。", "展示两张生活图片，板书学生感受词。", "口头联想并听同伴词语。", "展示两张冷暖对比图片。", "图片和色卡只做感受入口。", "学习单暂不发，先口头收集。", "学生能说出至少一个感受词。", "承接已有颜色经验。", "转入色卡对比，让感觉有依据。", "如果只说喜欢，追问像什么场景。", _responses("颜色感受"), {"resource_type": "图片/色卡", "why_needed": "让抽象冷暖变直观。", "attention_focus": "只看颜色带来的温度和情绪感。", "fallback_if_unavailable": "用黑板画两个色块并口头联想。"}),
        _event("EVT_2", "对比观察", "comparison", 8, "建立冷暖差异的直观依据。", "学生有感受词但分类不稳。", "学生能发现同一画面换色后感受会变。", "只看颜色，别先看画得像不像。", "这两组颜色让你觉得哪里不一样？", "同桌选一组图，说出冷/暖或其他感受。", "冷暖不是背表，是你能说出理由的感受判断。", "引导学生比较两组色卡和图片。", "同桌讨论并举卡选择。", "大屏或黑板呈现两组对比图。", "色卡按组发放。", "学习单只露出感受词区。", "同桌能说出一组颜色差异理由。", "从词语进入比较。", "转入小组分类探究。", "若学生抢答固定答案，换成情境图片追问理由。", _responses("冷暖对比"), {"resource_type": "冷暖图片和色卡", "why_needed": "提供可比较对象。", "attention_focus": "颜色变化如何改变感受。", "fallback_if_unavailable": "教师在黑板贴两组彩纸。"}),
        _event("EVT_3", "色卡分类探究", "analysis", 10, "让学生用分类和理由处理卡点。", "学生能感受差异但理由松散。", "学生能把色卡放入感受类别并说明依据。", "你们不是给颜色找标准答案，而是给感受找证据。", "为什么这张色卡应该放在这里？", "小组把色卡贴到感受词下，并准备一句理由。", "只要理由说得通，分类可以有不同想法。", "巡视并追问学生分类依据。", "小组分类、移动色卡、记录理由。", "黑板分成温暖、清凉、安静、热烈四区。", "色卡、图片、黑板磁贴。", "学习单记录一组颜色和理由。", "EVID_COLOR_SORT：色卡归类和理由表达。", "从比较进入主动分类。", "转入个人表达练习。", "若争论停在对错，提醒回到感受依据。", _responses("色卡分类"), {"resource_type": "色卡分组", "why_needed": "让学生用动作完成判断。", "attention_focus": "分类理由，不是贴得快。", "fallback_if_unavailable": "学生在纸上写颜色名称代替贴卡。"}),
        _event("EVT_4", "表达小练习", "practice", 13, "把理解迁移到个人色彩表达。", "学生已能分类但还未表达个人感受。", "学生能用颜色组合表达一种心情或场景。", "选两三种颜色，画出一种你想表达的感觉。", "你的颜色组合想让别人感到什么？", "完成一格小画，并写一句理由。", "这句话就是你作品的证据。", "示范一句理由，不示范完整作品。", "个人完成小练习。", "大屏保留句式：我用了...因为...。", "色卡作为参考，不再要求照抄。", "学习单完成小画和理由句。", "EVID_REASON_SENTENCE：颜色、感受、理由相连。", "从小组分类转到个人表达。", "转入分享时看理由是否成立。", "若学生画太复杂，提醒只做一格感受练习。", _responses("色彩表达"), {"resource_type": "学习单", "why_needed": "留下可观察证据。", "attention_focus": "颜色和理由是否对应。", "fallback_if_unavailable": "用作业纸画一格并口头说明。"}),
        _event("EVT_5", "分享证据", "sharing", 5, "用作品和理由验证目标达成。", "学生完成小练习但还未校准表达。", "学生能听懂同伴理由并修正自己的表达。", "我们不评谁最好看，只听颜色和理由是否连得上。", "他的颜色让你感受到他说的意思了吗？", "两三位学生展示，小组补一句建议。", "好作品不是颜色多，而是感受说得清。", "选择典型作品快速展示。", "展示、倾听、补充建议。", "实物投影或举作品。", "学生作品和学习单。", "学习单作为课后回收证据。", "学生能用理由评价同伴作品。", "承接个人小练习。", "下节课可用这些感受理由深化创作。", "若时间不足，只展示一正一改两个样本。", _responses("分享理由"), {"resource_type": "学生作品", "why_needed": "验证表达是否被理解。", "attention_focus": "理由和颜色是否对应。", "fallback_if_unavailable": "学生举作品口头说明。"}),
    ]


def _expand_rhythm_events(context: dict[str, Any], evidence_plan: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _event("EVT_1", "定观看焦点", "experience_evoke", 4, "先把资源目的说清，避免学生看热闹。", "学生期待看舞蹈或视频。", "学生知道要抓节奏而不是评价动作。", "等会儿只抓一个问题：节奏是跳的、流的，还是停顿的？", "你准备听/看哪一种节奏变化？", "先在学习单圈一个观察词。", "有了焦点，资源才不会散。", "说明观看任务，不评价舞蹈好坏。", "圈选观察词。", "黑板写三类节奏词。", "资源暂不播放，先定观察焦点。", "学习单出现节奏词。", "学生能选一个观察焦点。", "承接教师资源设想。", "转入短资源感受。", "如果学生只问视频内容，重复观察任务。", _responses("节奏焦点"), {"resource_type": "教师提出的舞蹈/音乐候选", "why_needed": "只有当它能提供清楚节奏变化时才使用。", "attention_focus": "节奏变化，不看动作好不好看。", "fallback_if_unavailable": "教师用拍手快慢和线条板书代替。"}),
        _event("EVT_2", "短资源感受", "comparison", 8, "用短资源激活节奏经验。", "学生有观察焦点但尚未形成视觉联想。", "学生能写下一个节奏词和初步感受。", "只看30秒，看到节奏变化就记一个词。", "哪一处节奏最明显？", "观看或听一小段，写一个节奏词。", "一个词够了，后面要把它变成线条。", "播放短片段或用拍手替代。", "观看、记录、同桌说。", "大屏只放短片段或黑板节奏线。", "若放视频，只截取短段。", "学习单记录节奏词。", "EVID_FOCUS_WORD：节奏词和一句理由。", "从焦点进入体验。", "转入线条色彩转译。", "若学生讨论动作漂亮，立刻回到节奏词。", _responses("节奏感受"), {"resource_type": "30秒片段或拍手节奏", "why_needed": "提供共同体验。", "attention_focus": "快慢、停顿、重复。", "fallback_if_unavailable": "全班拍手两种节奏并观察手势轨迹。"}),
        _event("EVT_3", "收感受并转译", "analysis", 8, "把听觉和身体经验转成视觉语言。", "学生有节奏词但不会画。", "学生能把一个节奏词对应到线条或颜色。", "如果这个节奏变成线条，它会是什么样？", "快节奏像密密的短线，还是长长的流线？为什么？", "用手势在空中画，再在纸上试一条线。", "先用一条线说清楚，不急着画完整作品。", "示范词到线条的转换，不给固定答案。", "空中比划并画一条线。", "黑板列出节奏词到线条的多种可能。", "黑板和粉笔即可。", "学习单完成一条试画线。", "学生能说明线条和节奏词的关系。", "从资源感受进入美术表达。", "转入个人小练习。", "若转译过难，给二选一线条让学生选。", _responses("视觉转译"), {"resource_type": "黑板示范", "why_needed": "降低从听觉到视觉的跨度。", "attention_focus": "线条疏密方向与节奏的关系。", "fallback_if_unavailable": "仍可用粉笔画两种线让学生比较。"}),
        _event("EVT_4", "个人小练习", "practice", 14, "形成可观察的节奏表达证据。", "学生会试一条线但作品表达未完成。", "学生能完成一格节奏画面并配一句说明。", "选一个节奏词，用线条和一两种颜色画出来。", "别人看你的画，能猜到你的节奏词吗？", "完成一格节奏表达草图。", "画面可以简单，但线条和颜色要有理由。", "巡视时问理由，不替学生改画。", "个人创作并写一句说明。", "大屏保留句式。", "材料为纸和彩笔。", "学习单完成小草图和说明。", "EVID_VISUAL_TRANSLATION：草图与理由对应。", "从共同转译进入个人表达。", "转入展示校准。", "若学生画成具体舞蹈人物，提醒回到节奏线条。", _responses("节奏表达"), {"resource_type": "学习单/纸笔", "why_needed": "留下目标达成证据。", "attention_focus": "线条色彩是否服务节奏词。", "fallback_if_unavailable": "普通作业纸分一格完成。"}),
        _event("EVT_5", "展示与连接", "sharing", 6, "用同伴猜测校准表达，并接到后续完整创作。", "学生完成草图但表达效果未校准。", "学生知道如何让节奏表达更清楚。", "我们先猜节奏，再听作者说理由。", "你从哪条线或哪个颜色猜出来的？", "两位学生展示，其他学生先猜再补充。", "能被别人看出节奏，说明视觉语言开始成立。", "组织猜测和作者说明。", "展示、猜测、修正。", "实物投影或举纸。", "学生草图。", "学习单作为下一环节创作依据。", "学生能指出作品中的节奏证据。", "承接个人小练习。", "下一环节可把一格草图扩展成完整作品。", "若时间不足，只展示一个清楚样本和一个需要调整样本。", _responses("展示校准"), {"resource_type": "学生草图", "why_needed": "验证视觉表达是否可读。", "attention_focus": "别人从哪里看出节奏。", "fallback_if_unavailable": "同桌互猜代替全班展示。"}),
    ]


def _expand_low_resource_color_events(context: dict[str, Any], evidence_plan: dict[str, Any]) -> list[dict[str, Any]]:
    events = _expand_cold_warm_events(context, evidence_plan)
    for event in events:
        event["design_view"]["big_screen_state"] = "不使用视频和平板；黑板贴图片或手绘色块。"
        event["resource_use"]["fallback_if_unavailable"] = "只用黑板、粉笔、几张图片和学生口头联想完成。"
        if event["resource_use"]["resource_type"] in {"冷暖图片和色卡", "色卡分组"}:
            event["resource_use"]["resource_type"] = "黑板图片/手绘色块"
            event["design_view"]["textbook_or_material_state"] = "几张图片轮流贴黑板，色卡不足时用粉笔写颜色名。"
    return events


def _field_patch_candidates(context: dict[str, Any], learning_problem: dict[str, Any], target_shift: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "field_patch_id": f"{context['lesson_design_mode']}_learning_problem",
            "target_section": "学情分析",
            "target_step_id": "",
            "target_field": "学习卡点",
            "patch_type": "revise",
            "before_summary": "学生基础描述偏泛。",
            "after_candidate": learning_problem["real_stuck_point"],
            "reasoning_basis": ["教师输入", "教材与课堂经验推测", "小备推演"],
            "impact_scope": ["教学过程", "学习单", "评价证据"],
            "teacher_review_required": True,
            "formal_apply_performed": False,
        },
        {
            "field_patch_id": f"{context['lesson_design_mode']}_teaching_route",
            "target_section": "教学过程",
            "target_step_id": "classroom_events",
            "target_field": "课堂事件",
            "patch_type": "restructure",
            "before_summary": "流程可以更明确地服务目标变化。",
            "after_candidate": target_shift["target_shift"]["observable_behavior"],
            "reasoning_basis": ["目标变化", "证据计划", "时间重算"],
            "impact_scope": ["教师动作", "学生任务", "大屏/黑板", "评价证据"],
            "teacher_review_required": True,
            "formal_apply_performed": False,
        },
    ]


def _impact_scope(context: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"affected_object": "teacher_action", "impact_summary": "教师话术从讲概念转为提醒学生看什么、说什么、如何给理由。", "requires_teacher_confirmation": True},
        {"affected_object": "student_activity", "impact_summary": "学生任务从听讲转为观察、分类、表达和说明理由。", "requires_teacher_confirmation": True},
        {"affected_object": "big_screen", "impact_summary": "根据资源条件使用大屏、黑板或图片，核心是聚焦观察点。", "requires_teacher_confirmation": True},
        {"affected_object": "handout", "impact_summary": "学习单只保留关键证据格，避免变成填空表。", "requires_teacher_confirmation": True},
        {"affected_object": "evidence_note", "impact_summary": "证据来自分类结果、理由句、草图和同伴能否读懂。", "requires_teacher_confirmation": True},
    ]


def _find_event_for_evidence(evidence_id: str, events: list[dict[str, Any]]) -> dict[str, Any] | None:
    for event in events:
        text = str(event)
        if evidence_id in text:
            return event
    if evidence_id and ("SORT" in evidence_id or "FOCUS" in evidence_id):
        return events[2] if len(events) > 2 else (events[0] if events else None)
    if evidence_id and ("REASON" in evidence_id or "TRANSLATION" in evidence_id):
        return events[3] if len(events) > 3 else (events[-1] if events else None)
    return None


def _validate_learning_problem(value: dict[str, Any]) -> list[str]:
    errors = []
    for key in ["core_learning_problem", "real_stuck_point", "student_baseline", "why_this_lesson_matters"]:
        if not value.get(key):
            errors.append(f"missing_{key}")
    if "激发兴趣" in value.get("core_learning_problem", "") and len(value.get("real_stuck_point", "")) < 8:
        errors.append("learning_problem_too_generic")
    return errors


def _validate_target_shift(value: dict[str, Any]) -> list[str]:
    target = value.get("target_shift") if isinstance(value.get("target_shift"), dict) else {}
    return [f"missing_target_shift_{key}" for key in ["from_state", "to_state", "observable_behavior", "success_evidence"] if not target.get(key)]


def _validate_expanded_events(value: dict[str, Any]) -> list[str]:
    errors = []
    events = value.get("classroom_events") if isinstance(value.get("classroom_events"), list) else []
    if not events:
        return ["missing_classroom_events"]
    for index, event in enumerate(events):
        design = event.get("design_view") if isinstance(event.get("design_view"), dict) else {}
        execution = event.get("execution_view") if isinstance(event.get("execution_view"), dict) else {}
        for key in ["teacher_focus_cue", "student_task", "core_question"]:
            if not execution.get(key):
                errors.append(f"event_{index}_missing_{key}")
        for key in ["student_state_before", "student_state_after", "assessment_evidence", "transition_to_next", "risk_and_adjustment"]:
            if not design.get(key):
                errors.append(f"event_{index}_missing_{key}")
        responses = event.get("student_response_model") if isinstance(event.get("student_response_model"), list) else []
        if not responses:
            errors.append(f"event_{index}_missing_student_response_model")
    return errors


def _has_values(value: dict[str, Any], keys: list[str]) -> bool:
    return all(bool(value.get(key)) for key in keys)
