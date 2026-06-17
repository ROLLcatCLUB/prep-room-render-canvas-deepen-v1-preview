from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.xiaobei_ai.prep_room_lesson_reasoning_contract_1013E import BOUNDARY_FLAGS  # noqa: E402
from backend.xiaobei_ai.prep_room_staged_derivation_pipeline_1013E_R4 import (  # noqa: E402
    R4_CASES,
    STAGE_ID,
    aggregate_case_results,
    final_status_for,
    run_staged_lesson_derivation_case,
)


OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "live_poc_1013E_R4"

SECRET_PATTERNS = [
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]{12,}", re.I),
    re.compile(r"sk-[A-Za-z0-9_\-]{12,}", re.I),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{12,}", re.I),
    re.compile(r"(?i)(api[_-]?key|authorization|secret|tenant_access_token)\s*[:=]\s*['\"][^'\"]{8,}"),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(name: str, payload: Any) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_text(name: str, text: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    path.write_text(text, encoding="utf-8")
    return path


def secret_scan_payload(payload: Any) -> list[str]:
    text = json.dumps(payload, ensure_ascii=False)
    return [pattern.pattern for pattern in SECRET_PATTERNS if pattern.search(text)]


def public_case_result(case_result: dict[str, Any]) -> dict[str, Any]:
    return case_result


def collect_step_trace(case_results: list[dict[str, Any]], step: str) -> list[dict[str, Any]]:
    rows = []
    for item in case_results:
        for trace in item.get("staged_trace") or []:
            if trace.get("step") == step:
                rows.append({"case_id": item["case_id"], **trace})
    return rows


def write_report(result: dict[str, Any], case_results: list[dict[str, Any]]) -> None:
    lines = [
        "# 1013E_R4 Staged Lesson Derivation Pipeline",
        "",
        "```text",
        f"final_status={result['final_status']}",
        f"next_stage={result['next_stage']}",
        f"pipeline_pass_count={result['aggregate']['pipeline_pass_count']}/3",
        f"standard_daily_pass={str(result['aggregate']['standard_daily_pass']).lower()}",
        f"secret_scan_ok={str(result['aggregate']['secret_scan_ok']).lower()}",
        "```",
        "",
        "## Case Results",
        "",
        "| case_id | pipeline | learning_problem | target_shift | events | evidence | time |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in case_results:
        lines.append(
            f"| `{item['case_id']}` | {str(item['pipeline_pass']).lower()} | "
            f"{str(item['learning_problem_generated']).lower()} | {str(item['target_shift_generated']).lower()} | "
            f"{str(item['classroom_events_generated']).lower()} | {str(item['evidence_binding_pass']).lower()} | "
            f"{str(item['time_balance_pass']).lower()} |"
        )
    lines.extend(
        [
            "",
            "## Strategy",
            "",
            "- R4 stops one-call full lesson graph generation.",
            "- R4 uses staged derivation: context, learning problem, target shift, evidence, route, classroom events, event unfolding, time rebalance, evidence binding, effectiveness evaluation.",
            "- This implementation is local rule-based staged derivation first, so provider/model are not called in R4.",
            "- Local cases are treated as reference candidates only, not authoritative templates.",
            "",
            "## Boundary",
            "",
            "- No UI binding.",
            "- No database write.",
            "- No memory write.",
            "- No Feishu write.",
            "- No formal apply.",
            "- No official export.",
            "- No official archive.",
            "- No real knowledge-base retrieval.",
            "- No raw model output is sent to frontend.",
        ]
    )
    write_text("1013E_R4_report.md", "\n".join(lines) + "\n")


def write_outputs(result: dict[str, Any], case_results: list[dict[str, Any]]) -> None:
    step_names = [
        "LessonContextPack",
        "LearningProblemDeriver",
        "TargetShiftDeriver",
        "EvidencePlanDeriver",
        "TeachingRoutePlanner",
        "ClassroomEventGenerator",
        "EventUnfoldingExpander",
        "TimeRebalancer",
        "EvidenceBinder",
        "EffectivenessEvaluator",
    ]
    trace = [{step: collect_step_trace(case_results, step)} for step in step_names]
    candidate_errors = [
        {"case_id": item["case_id"], "candidate_errors": item.get("candidate_errors") or [], "contract_errors": item.get("contract_errors") or []}
        for item in case_results
    ]
    metrics = {
        "provider_called": False,
        "model_called": False,
        "strategy": "local_staged_rule_derivation",
        "case_count": len(case_results),
        "aggregate": result["aggregate"],
    }
    redacted_trace = [
        {
            "case_id": item["case_id"],
            "teacher_input": item["teacher_input"],
            "provider_called": False,
            "model_called": False,
            "trace_step_count": len(item.get("staged_trace") or []),
        }
        for item in case_results
    ]
    write_json("1013E_R4_result.json", result)
    write_json("case_results_1013E_R4.json", case_results)
    write_json("staged_pipeline_trace_1013E_R4.json", trace)
    write_json("learning_problem_derivation_1013E_R4.json", collect_step_trace(case_results, "LearningProblemDeriver"))
    write_json("target_shift_derivation_1013E_R4.json", collect_step_trace(case_results, "TargetShiftDeriver"))
    write_json("evidence_plan_1013E_R4.json", collect_step_trace(case_results, "EvidencePlanDeriver"))
    write_json("teaching_route_plan_1013E_R4.json", collect_step_trace(case_results, "TeachingRoutePlanner"))
    write_json("classroom_event_generation_1013E_R4.json", collect_step_trace(case_results, "ClassroomEventGenerator"))
    write_json("event_unfolding_expansion_1013E_R4.json", collect_step_trace(case_results, "EventUnfoldingExpander"))
    write_json("time_rebalance_trace_1013E_R4.json", collect_step_trace(case_results, "TimeRebalancer"))
    write_json("evidence_binding_trace_1013E_R4.json", collect_step_trace(case_results, "EvidenceBinder"))
    write_json("effectiveness_eval_1013E_R4.json", collect_step_trace(case_results, "EffectivenessEvaluator"))
    write_json("candidate_error_trace_1013E_R4.json", candidate_errors)
    write_json("provider_metrics_1013E_R4.json", metrics)
    write_json("redacted_provider_trace_1013E_R4.json", redacted_trace)
    write_report(result, case_results)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    case_results = [public_case_result(run_staged_lesson_derivation_case(case)) for case in R4_CASES]
    secret_hits = secret_scan_payload(case_results)
    aggregate = aggregate_case_results(case_results)
    aggregate["secret_scan_ok"] = not secret_hits
    final_status, next_stage = final_status_for(case_results, aggregate)
    result = {
        "stage_id": STAGE_ID,
        "created_at": now(),
        "final_status": final_status,
        "next_stage": next_stage,
        "provider_called": False,
        "model_called": False,
        "aggregate": aggregate,
        "secret_scan_hits": sorted(set(secret_hits)),
        "boundary_flags": dict(BOUNDARY_FLAGS),
    }
    write_outputs(result, case_results)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if final_status == "PASS_STAGED_LESSON_DERIVATION_PIPELINE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
