from __future__ import annotations

import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.xiaobei_ai import providers


STAGE = "1013O_MINIMAX_M3_VS_M27_HIGHSPEED_MULTI_ROUND_BENCHMARK"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013O_minimax_m3_vs_m27_highspeed_multi_round"
MODELS = ["MiniMax-M3", "MiniMax-M2.7-highspeed"]
REPEATS = 3


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_cases() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "simple_json_exact",
            "max_tokens": 400,
            "prompt": {
                "system_prompt": "Return only one valid JSON object. No markdown. No explanation.",
                "user_prompt": 'Return exactly this JSON object: {"ok":true,"case":"simple_json_exact","value":3}',
            },
            "validator": validate_simple_json,
        },
        {
            "case_id": "teacher_note_micro",
            "max_tokens": 900,
            "prompt": {
                "system_prompt": "You are a primary school art lesson assistant. Return only strict JSON.",
                "user_prompt": json.dumps(
                    {
                        "task": "Turn teacher intent into a short teacher-readable suggestion.",
                        "lesson": "Grade 3 art, 1-2 色彩的感觉",
                        "teacher_input": "学生对冷暖色不太理解，要更直观。",
                        "return_shape": {
                            "judgement": "",
                            "suggested_change": "",
                            "student_blocker": "",
                            "teacher_move": "",
                            "impact_scope": ["big_screen", "handout", "evidence_note"],
                            "boundary_flags": {
                                "teacher_review_required": True,
                                "formal_apply_performed": False,
                                "database_written": False,
                                "memory_written": False,
                                "feishu_written": False,
                            },
                        },
                    },
                    ensure_ascii=False,
                ),
            },
            "validator": validate_teacher_note,
        },
        {
            "case_id": "lesson_patch_micro",
            "max_tokens": 1600,
            "prompt": {
                "system_prompt": "You are Xiaojiao prep-room assistant. Return only one strict JSON object.",
                "user_prompt": json.dumps(
                    {
                        "task": "Create compact patch candidates, not a full lesson plan.",
                        "lesson": {
                            "subject": "美术",
                            "grade": "三年级",
                            "title": "1-2 色彩的感觉",
                            "duration_minutes": 40,
                        },
                        "teacher_input": "学生对冷暖色不太理解，要设计得更直观一点。",
                        "return_shape": {
                            "intent_summary": "",
                            "patches": [
                                {
                                    "target": "学情分析",
                                    "candidate": "",
                                    "reason": "",
                                },
                                {
                                    "target": "教学过程 · 探究环节",
                                    "candidate": "",
                                    "reason": "",
                                },
                            ],
                            "impact_scope": [
                                {"object": "big_screen", "impact": ""},
                                {"object": "handout", "impact": ""},
                                {"object": "evidence_note", "impact": ""},
                            ],
                            "quality_gate": {"pass": True, "risk": ""},
                            "boundary_flags": {
                                "teacher_review_required": True,
                                "formal_apply_performed": False,
                                "database_written": False,
                                "memory_written": False,
                                "feishu_written": False,
                            },
                        },
                        "rules": [
                            "Do not echo return_shape.",
                            "Do not mention schema, provider, database, memory, Feishu, formal_apply in teacher text.",
                            "Keep every string short.",
                        ],
                    },
                    ensure_ascii=False,
                ),
            },
            "validator": validate_lesson_patch,
        },
    ]


def call_model(model: str, case: dict[str, Any], round_index: int) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        result = providers.generate_json_patch(
            {"mode": STAGE, "case_id": case["case_id"], "round": round_index, "model": model},
            case["prompt"],
            {
                "provider": "openai_compatible",
                "model": model,
                "temperature": 0.1,
                "max_tokens": case["max_tokens"],
                "timeout_ms": 120000,
                "use_response_format": True,
                "use_reasoning_split": False,
            },
        )
        elapsed_ms = round((time.perf_counter() - started) * 1000)
        provider_meta = result.get("provider_meta") if isinstance(result.get("provider_meta"), dict) else {}
        raw_text = str(result.get("raw_text") or "")
        evaluation = case["validator"](raw_text)
        return {
            "ok": True,
            "case_id": case["case_id"],
            "round": round_index,
            "model": model,
            "latency_ms": provider_meta.get("latency_ms") or elapsed_ms,
            "raw_length": len(raw_text),
            "evaluation": evaluation,
            "raw_text_redacted_prefix": raw_text[:1000],
            "provider_meta": {
                "provider": provider_meta.get("provider"),
                "model": provider_meta.get("model"),
                "credential_source": provider_meta.get("credential_source"),
                "reasoning_split": provider_meta.get("reasoning_split"),
            },
        }
    except Exception as exc:  # noqa: BLE001 - benchmark should record provider failure.
        elapsed_ms = round((time.perf_counter() - started) * 1000)
        return {
            "ok": False,
            "case_id": case["case_id"],
            "round": round_index,
            "model": model,
            "latency_ms": elapsed_ms,
            "raw_length": 0,
            "evaluation": {"pass": False, "errors": [type(exc).__name__, str(exc)]},
            "raw_text_redacted_prefix": "",
            "provider_meta": {},
        }


def parse_json(raw_text: str) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        parsed = json.loads(raw_text)
    except Exception as exc:  # noqa: BLE001
        return None, [f"json_parse_error:{exc}"]
    if not isinstance(parsed, dict):
        return None, ["json_not_object"]
    return parsed, []


def validate_simple_json(raw_text: str) -> dict[str, Any]:
    parsed, errors = parse_json(raw_text)
    if parsed and parsed.get("ok") is not True:
        errors.append("ok_not_true")
    if parsed and parsed.get("case") != "simple_json_exact":
        errors.append("case_mismatch")
    if parsed and parsed.get("value") != 3:
        errors.append("value_mismatch")
    return {"pass": not errors, "errors": errors, "parsed": parsed}


def validate_teacher_note(raw_text: str) -> dict[str, Any]:
    parsed, errors = parse_json(raw_text)
    if not parsed:
        return {"pass": False, "errors": errors, "parsed": None, "quality_score": 0}
    for key in ["judgement", "suggested_change", "student_blocker", "teacher_move", "impact_scope", "boundary_flags"]:
        if key not in parsed:
            errors.append(f"missing_{key}")
    text = json.dumps(parsed, ensure_ascii=False)
    quality_terms = ["冷暖", "感受", "色卡", "大屏", "学习单", "证据", "追问"]
    quality_score = sum(1 for term in quality_terms if term in text)
    boundary = parsed.get("boundary_flags") if isinstance(parsed.get("boundary_flags"), dict) else {}
    if boundary.get("teacher_review_required") is not True:
        errors.append("teacher_review_required_not_true")
    for key in ["formal_apply_performed", "database_written", "memory_written", "feishu_written"]:
        if boundary.get(key) is not False:
            errors.append(f"{key}_not_false")
    return {"pass": not errors, "errors": errors, "parsed": parsed, "quality_score": quality_score}


def validate_lesson_patch(raw_text: str) -> dict[str, Any]:
    parsed, errors = parse_json(raw_text)
    if not parsed:
        return {"pass": False, "errors": errors, "parsed": None, "quality_score": 0}
    for key in ["intent_summary", "patches", "impact_scope", "quality_gate", "boundary_flags"]:
        if key not in parsed:
            errors.append(f"missing_{key}")
    text = json.dumps(parsed, ensure_ascii=False)
    for term, code in [
        ("学情", "missing_analysis"),
        ("探究", "missing_explore"),
        ("big_screen", "missing_big_screen"),
        ("handout", "missing_handout"),
        ("evidence_note", "missing_evidence_note"),
    ]:
        if term not in text:
            errors.append(code)
    quality_terms = ["冷暖", "感受", "直观", "色卡", "大屏", "学习单", "证据", "风险", "追问"]
    quality_score = sum(1 for term in quality_terms if term in text)
    boundary = parsed.get("boundary_flags") if isinstance(parsed.get("boundary_flags"), dict) else {}
    if boundary.get("teacher_review_required") is not True:
        errors.append("teacher_review_required_not_true")
    for key in ["formal_apply_performed", "database_written", "memory_written", "feishu_written"]:
        if boundary.get(key) is not False:
            errors.append(f"{key}_not_false")
    return {"pass": not errors, "errors": errors, "parsed": parsed, "quality_score": quality_score}


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    by_model: dict[str, dict[str, Any]] = {}
    by_case: dict[str, dict[str, Any]] = {}
    for model in MODELS:
        model_records = [r for r in records if r["model"] == model]
        latencies = [int(r["latency_ms"]) for r in model_records]
        passes = [bool(r.get("evaluation", {}).get("pass")) for r in model_records]
        quality = [int(r.get("evaluation", {}).get("quality_score") or 0) for r in model_records]
        by_model[model] = metric_block(latencies, passes, quality)
    for case in sorted({r["case_id"] for r in records}):
        by_case[case] = {}
        for model in MODELS:
            case_records = [r for r in records if r["case_id"] == case and r["model"] == model]
            latencies = [int(r["latency_ms"]) for r in case_records]
            passes = [bool(r.get("evaluation", {}).get("pass")) for r in case_records]
            quality = [int(r.get("evaluation", {}).get("quality_score") or 0) for r in case_records]
            by_case[case][model] = metric_block(latencies, passes, quality)
        m3_avg = by_case[case]["MiniMax-M3"]["avg_latency_ms"]
        m27_avg = by_case[case]["MiniMax-M2.7-highspeed"]["avg_latency_ms"]
        by_case[case]["speed_delta"] = speed_delta(m3_avg, m27_avg)
    overall_delta = speed_delta(by_model["MiniMax-M3"]["avg_latency_ms"], by_model["MiniMax-M2.7-highspeed"]["avg_latency_ms"])
    return {
        "by_model": by_model,
        "by_case": by_case,
        "overall_speed_delta": overall_delta,
        "winner_by_average_latency": "MiniMax-M3" if overall_delta["m3_faster_by_ms"] > 0 else "MiniMax-M2.7-highspeed",
        "winner_by_pass_rate": max(MODELS, key=lambda model: by_model[model]["pass_rate"]),
    }


def metric_block(latencies: list[int], passes: list[bool], quality: list[int]) -> dict[str, Any]:
    return {
        "count": len(latencies),
        "avg_latency_ms": round(statistics.mean(latencies), 1) if latencies else None,
        "median_latency_ms": round(statistics.median(latencies), 1) if latencies else None,
        "min_latency_ms": min(latencies) if latencies else None,
        "max_latency_ms": max(latencies) if latencies else None,
        "pass_count": sum(1 for item in passes if item),
        "pass_rate": round(sum(1 for item in passes if item) / len(passes), 3) if passes else 0,
        "avg_quality_score": round(statistics.mean(quality), 2) if quality else 0,
    }


def speed_delta(m3_latency: float | None, m27_latency: float | None) -> dict[str, Any]:
    if not m3_latency or not m27_latency:
        return {}
    return {
        "m3_latency_ms": m3_latency,
        "m27_highspeed_latency_ms": m27_latency,
        "m3_faster_by_ms": round(m27_latency - m3_latency, 1),
        "m27_highspeed_is_x_of_m3": round(m27_latency / m3_latency, 2),
        "m3_latency_reduction_vs_m27_percent": round((m27_latency - m3_latency) / m27_latency * 100, 1),
    }


def write_report(result: dict[str, Any]) -> None:
    summary = result["summary"]
    lines = [
        "# 1013O Multi-Round Benchmark: MiniMax-M3 vs MiniMax-M2.7-highspeed",
        "",
        f"- FINAL_STATUS: `{result['final_status']}`",
        f"- Repeats per model per case: `{REPEATS}`",
        f"- Winner by average latency: `{summary['winner_by_average_latency']}`",
        f"- Winner by pass rate: `{summary['winner_by_pass_rate']}`",
        "",
        "## Overall",
        "",
        "| Model | Calls | Avg latency | Median latency | Pass rate | Avg quality |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for model, block in summary["by_model"].items():
        lines.append(
            f"| {model} | {block['count']} | {block['avg_latency_ms']}ms | {block['median_latency_ms']}ms | {block['pass_rate']} | {block['avg_quality_score']} |"
        )
    delta = summary["overall_speed_delta"]
    lines += [
        "",
        f"Overall speed delta: M3 faster by `{delta.get('m3_faster_by_ms')}ms` on average; M2.7-highspeed is `{delta.get('m27_highspeed_is_x_of_m3')}x` of M3 average latency.",
        "",
        "## By Case",
        "",
    ]
    for case_id, case_summary in summary["by_case"].items():
        lines.append(f"### {case_id}")
        lines.append("")
        lines.append("| Model | Avg latency | Median latency | Pass rate | Avg quality |")
        lines.append("|---|---:|---:|---:|---:|")
        for model in MODELS:
            block = case_summary[model]
            lines.append(f"| {model} | {block['avg_latency_ms']}ms | {block['median_latency_ms']}ms | {block['pass_rate']} | {block['avg_quality_score']} |")
        d = case_summary["speed_delta"]
        lines.append("")
        lines.append(f"Speed delta: M3 faster by `{d.get('m3_faster_by_ms')}ms`; M2.7-highspeed is `{d.get('m27_highspeed_is_x_of_m3')}x` of M3.")
        lines.append("")
    lines += [
        "## Interpretation",
        "",
        result["interpretation"],
        "",
        "## Boundary",
        "",
        "- Provider/model calls were made for benchmark only.",
        "- No lesson text was formally applied.",
        "- No database, memory, or Feishu write was performed.",
    ]
    (OUT_DIR / "1013O_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cases = make_cases()
    records = []
    for round_index in range(1, REPEATS + 1):
        for case in cases:
            for model in MODELS:
                print(f"RUN round={round_index} case={case['case_id']} model={model}", flush=True)
                records.append(call_model(model, case, round_index))
    summary = summarize(records)
    interpretation = (
        "Across this multi-round sample, M3 should be judged on both latency and usable structured output. "
        "If the pass rate stays close while M3 latency is lower, use M3 by default; if a later larger benchmark reverses this, keep model routing configurable."
    )
    result = {
        "stage": STAGE,
        "final_status": "PASS_MINIMAX_M3_VS_M27_HIGHSPEED_MULTI_ROUND_BENCHMARK",
        "models": MODELS,
        "repeats": REPEATS,
        "case_ids": [case["case_id"] for case in cases],
        "summary": summary,
        "interpretation": interpretation,
        "records": records,
        "provider_called": True,
        "model_called": True,
        "teacher_review_required": True,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }
    write_json(OUT_DIR / "1013O_result.json", result)
    write_json(OUT_DIR / "1013O_records.json", records)
    write_json(OUT_DIR / "1013O_summary.json", summary)
    write_report(result)
    print(json.dumps({k: result[k] for k in ["stage", "final_status", "summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
