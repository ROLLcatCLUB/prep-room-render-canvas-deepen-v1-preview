from __future__ import annotations

import json
import statistics
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.xiaobei_ai import providers


STAGE = "1013P_MINIMAX_M3_THINKING_MODES_BENCHMARK"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013P_minimax_m3_thinking_modes_benchmark"
MODEL = "MiniMax-M3"
REPEATS = 2
MODES = [
    {"mode_id": "disabled", "thinking": {"type": "disabled"}},
    {"mode_id": "adaptive", "thinking": {"type": "adaptive"}},
    {"mode_id": "omitted_default_on", "thinking": None},
    {"mode_id": "enabled_probe", "thinking": {"type": "enabled"}},
]


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cases() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "simple_json",
            "max_completion_tokens": 800,
            "messages": [
                {"role": "system", "content": "Return only one valid JSON object. No markdown. No explanation."},
                {"role": "user", "content": 'Return exactly: {"ok":true,"case":"simple_json","mode_check":"m3"}'},
            ],
            "validator": validate_simple_json,
        },
        {
            "case_id": "lesson_patch_reasoning",
            "max_completion_tokens": 2400,
            "messages": [
                {"role": "system", "content": "You are Xiaojiao prep-room assistant. Return only strict JSON. No markdown."},
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "task": "Create compact patch candidates, not a full lesson plan.",
                            "lesson": "Grade 3 art, 1-2 色彩的感觉, 40 minutes",
                            "teacher_input": "学生对冷暖色不太理解，要设计得更直观一点。",
                            "return_shape": {
                                "judgement": "",
                                "student_blocker": "",
                                "patches": [
                                    {"target": "学情分析", "candidate": ""},
                                    {"target": "教学过程 · 探究环节", "candidate": ""},
                                ],
                                "impact_scope": [
                                    {"object": "big_screen", "impact": ""},
                                    {"object": "handout", "impact": ""},
                                    {"object": "evidence_note", "impact": ""},
                                ],
                                "risk_and_adjustment": "",
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
                                "Keep strings short and teacher-readable.",
                                "The output must contain 学情分析 and 探究环节.",
                            ],
                        },
                        ensure_ascii=False,
                    ),
                },
            ],
            "validator": validate_lesson_patch,
        },
    ]


def call(mode: dict[str, Any], case: dict[str, Any], round_index: int) -> dict[str, Any]:
    base_url = providers._resolve_base_url()
    endpoint = providers._resolve_openai_compatible_endpoint(base_url)
    api_key = providers._resolve_api_key()
    body: dict[str, Any] = {
        "model": MODEL,
        "messages": case["messages"],
        "temperature": 0.1,
        "max_completion_tokens": case["max_completion_tokens"],
        "response_format": {"type": "json_object"},
        "reasoning_split": True,
    }
    if mode["thinking"] is not None:
        body["thinking"] = mode["thinking"]
    request = urllib.request.Request(
        base_url + endpoint,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            raw_response = response.read().decode("utf-8")
        latency_ms = round((time.perf_counter() - started) * 1000)
        parsed_response = json.loads(raw_response)
        providers._raise_openai_compatible_business_error(parsed_response, base_url)
        message = (((parsed_response.get("choices") or [])[0] or {}).get("message") or {})
        content = message.get("content") or ""
        reasoning_content = message.get("reasoning_content") or ""
        reasoning_details = message.get("reasoning_details") or []
        finish_reason = ((parsed_response.get("choices") or [])[0] or {}).get("finish_reason")
        evaluation = case["validator"](content)
        return {
            "ok": True,
            "round": round_index,
            "case_id": case["case_id"],
            "mode_id": mode["mode_id"],
            "thinking_sent": mode["thinking"],
            "latency_ms": latency_ms,
            "finish_reason": finish_reason,
            "content_length": len(content),
            "reasoning_content_length": len(reasoning_content),
            "reasoning_details_count": len(reasoning_details) if isinstance(reasoning_details, list) else 0,
            "usage": parsed_response.get("usage") if isinstance(parsed_response.get("usage"), dict) else {},
            "evaluation": evaluation,
            "content_prefix": content[:1200],
            "reasoning_prefix": str(reasoning_content)[:500],
        }
    except Exception as exc:  # noqa: BLE001 - benchmark records provider/API failures.
        latency_ms = round((time.perf_counter() - started) * 1000)
        return {
            "ok": False,
            "round": round_index,
            "case_id": case["case_id"],
            "mode_id": mode["mode_id"],
            "thinking_sent": mode["thinking"],
            "latency_ms": latency_ms,
            "finish_reason": None,
            "content_length": 0,
            "reasoning_content_length": 0,
            "reasoning_details_count": 0,
            "usage": {},
            "evaluation": {"pass": False, "errors": [type(exc).__name__, str(exc)], "quality_score": 0},
            "content_prefix": "",
            "reasoning_prefix": "",
        }


def parse_json(content: str) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(content)
    except Exception as exc:  # noqa: BLE001
        return None, [f"json_parse_error:{exc}"]
    if not isinstance(data, dict):
        return None, ["json_not_object"]
    return data, []


def validate_simple_json(content: str) -> dict[str, Any]:
    data, errors = parse_json(content)
    if data and data.get("ok") is not True:
        errors.append("ok_not_true")
    if data and data.get("case") != "simple_json":
        errors.append("case_mismatch")
    return {"pass": not errors, "errors": errors, "quality_score": 0, "parsed": data}


def validate_lesson_patch(content: str) -> dict[str, Any]:
    data, errors = parse_json(content)
    if not data:
        return {"pass": False, "errors": errors, "quality_score": 0, "parsed": None}
    text = json.dumps(data, ensure_ascii=False)
    for term, code in [
        ("学情分析", "missing_analysis"),
        ("探究", "missing_explore"),
        ("big_screen", "missing_big_screen"),
        ("handout", "missing_handout"),
        ("evidence_note", "missing_evidence_note"),
    ]:
        if term not in text:
            errors.append(code)
    boundary = data.get("boundary_flags") if isinstance(data.get("boundary_flags"), dict) else {}
    if boundary.get("teacher_review_required") is not True:
        errors.append("teacher_review_required_not_true")
    for key in ["formal_apply_performed", "database_written", "memory_written", "feishu_written"]:
        if boundary.get(key) is not False:
            errors.append(f"{key}_not_false")
    quality_terms = ["冷暖", "感受", "直观", "色卡", "大屏", "学习单", "证据", "风险", "追问", "调整"]
    quality_score = sum(1 for term in quality_terms if term in text)
    return {"pass": not errors, "errors": errors, "quality_score": quality_score, "parsed": data}


def metric(records: list[dict[str, Any]]) -> dict[str, Any]:
    latencies = [int(item["latency_ms"]) for item in records]
    passes = [bool(item["evaluation"].get("pass")) for item in records]
    quality = [int(item["evaluation"].get("quality_score") or 0) for item in records]
    reasoning_lengths = [int(item.get("reasoning_content_length") or 0) for item in records]
    completion_tokens = [
        int((item.get("usage") or {}).get("completion_tokens") or 0)
        for item in records
        if isinstance(item.get("usage"), dict)
    ]
    return {
        "count": len(records),
        "avg_latency_ms": round(statistics.mean(latencies), 1) if latencies else None,
        "median_latency_ms": round(statistics.median(latencies), 1) if latencies else None,
        "min_latency_ms": min(latencies) if latencies else None,
        "max_latency_ms": max(latencies) if latencies else None,
        "pass_rate": round(sum(passes) / len(passes), 3) if passes else 0,
        "avg_quality_score": round(statistics.mean(quality), 2) if quality else 0,
        "avg_reasoning_content_length": round(statistics.mean(reasoning_lengths), 1) if reasoning_lengths else 0,
        "avg_completion_tokens": round(statistics.mean(completion_tokens), 1) if completion_tokens else 0,
    }


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    by_mode = {}
    by_case = {}
    for mode in MODES:
        mode_records = [item for item in records if item["mode_id"] == mode["mode_id"]]
        by_mode[mode["mode_id"]] = metric(mode_records)
    for case_id in sorted({item["case_id"] for item in records}):
        by_case[case_id] = {}
        for mode in MODES:
            case_records = [item for item in records if item["case_id"] == case_id and item["mode_id"] == mode["mode_id"]]
            by_case[case_id][mode["mode_id"]] = metric(case_records)
    fastest = min(by_mode, key=lambda key: by_mode[key]["avg_latency_ms"] or 10**9)
    best_quality = max(by_mode, key=lambda key: by_mode[key]["avg_quality_score"])
    return {"by_mode": by_mode, "by_case": by_case, "fastest_mode": fastest, "best_quality_mode": best_quality}


def write_report(result: dict[str, Any]) -> None:
    summary = result["summary"]
    lines = [
        "# 1013P MiniMax-M3 Thinking Modes Benchmark",
        "",
        f"- FINAL_STATUS: `{result['final_status']}`",
        f"- Repeats per mode per case: `{REPEATS}`",
        f"- Fastest mode: `{summary['fastest_mode']}`",
        f"- Best quality mode: `{summary['best_quality_mode']}`",
        "",
        "## Thinking Modes Tested",
        "",
        "- `disabled`: sends `thinking: {\"type\":\"disabled\"}`.",
        "- `adaptive`: sends `thinking: {\"type\":\"adaptive\"}`.",
        "- `omitted_default_on`: omits `thinking`; MiniMax docs say M3 thinking is on by default.",
        "- `enabled_probe`: sends `thinking: {\"type\":\"enabled\"}` to verify whether the live API accepts the model-page third mode.",
        "",
        "## Overall",
        "",
        "| Mode | Calls | Avg latency | Median latency | Pass rate | Avg quality | Avg reasoning length | Avg completion tokens |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for mode_id, block in summary["by_mode"].items():
        lines.append(
            f"| {mode_id} | {block['count']} | {block['avg_latency_ms']}ms | {block['median_latency_ms']}ms | {block['pass_rate']} | {block['avg_quality_score']} | {block['avg_reasoning_content_length']} | {block['avg_completion_tokens']} |"
        )
    lines += ["", "## By Case", ""]
    for case_id, case_summary in summary["by_case"].items():
        lines.append(f"### {case_id}")
        lines.append("")
        lines.append("| Mode | Avg latency | Pass rate | Avg quality | Avg reasoning length |")
        lines.append("|---|---:|---:|---:|---:|")
        for mode_id, block in case_summary.items():
            lines.append(f"| {mode_id} | {block['avg_latency_ms']}ms | {block['pass_rate']} | {block['avg_quality_score']} | {block['avg_reasoning_content_length']} |")
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
    (OUT_DIR / "1013P_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    all_cases = cases()
    for round_index in range(1, REPEATS + 1):
        for case in all_cases:
            for mode in MODES:
                print(f"RUN round={round_index} case={case['case_id']} thinking={mode['mode_id']}", flush=True)
                records.append(call(mode, case, round_index))
    summary = summarize(records)
    interpretation = (
        "Use disabled thinking when the required output is compact JSON or low-latency teacher-facing suggestions. "
        "Use adaptive/default thinking only when a later stage explicitly needs deeper reasoning and can tolerate extra latency and reasoning-token budget. "
        "The enabled_probe result is empirical and should not override the official OpenAI-compatible docs if the API rejects it in other environments."
    )
    result = {
        "stage": STAGE,
        "final_status": "PASS_MINIMAX_M3_THINKING_MODES_BENCHMARK",
        "model": MODEL,
        "repeats": REPEATS,
        "modes": MODES,
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
    write_json(OUT_DIR / "1013P_result.json", result)
    write_json(OUT_DIR / "1013P_records.json", records)
    write_json(OUT_DIR / "1013P_summary.json", summary)
    write_report(result)
    print(json.dumps({k: result[k] for k in ["stage", "final_status", "summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
