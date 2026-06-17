from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.xiaobei_ai import providers
from backend.xiaobei_ai.prep_room_lesson_reasoning_contract_1013E import (
    BOUNDARY_FLAGS,
    LESSON_CONTEXT,
    R1_COMPACT_OUTPUT_SHAPE,
    R1_HARD_RULES,
    parse_lesson_reasoning_output,
    validate_compact_lesson_reasoning_payload,
)


STAGE = "1013N_MINIMAX_M3_VS_M27_HIGHSPEED_COMPARISON"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013N_minimax_m3_vs_m27_highspeed_comparison"
MODELS = ["MiniMax-M3", "MiniMax-M2.7-highspeed"]


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_json_probe_prompt() -> dict[str, str]:
    return {
        "system_prompt": "Return only one valid JSON object. No markdown. No explanation.",
        "user_prompt": 'Return exactly this JSON object: {"ok":true,"task":"json_probe","lesson":"color_feeling"}',
    }


def build_lesson_reasoning_prompt() -> dict[str, str]:
    request = {
        "stage_id": STAGE,
        "task": "Compare model ability to convert a teacher intent into compact lesson reasoning field patches.",
        "fixed_lesson_context": LESSON_CONTEXT,
        "lesson_design_mode": "standard_daily",
        "teacher_input": "学生对冷暖色不太理解，要设计得更直观一点。",
        "must_return_shape": R1_COMPACT_OUTPUT_SHAPE,
        "hard_rules": R1_HARD_RULES,
        "extra_requirements": [
            "step_reasoning_updates 至少包含探究环节。",
            "impact_scope 必须覆盖 big_screen, handout, evidence_note。",
            "field_patch_candidates 必须定位到 学情分析 和 教学过程 · 探究环节。",
            "最多输出 2 个 field_patch_candidates。",
            "只输出 1 个 step_reasoning_updates，聚焦探究环节。",
            "impact_scope 只输出 big_screen, handout, evidence_note 三项。",
            "每个字符串尽量短，不写完整段落。",
            "不要写完整教案，只写候选补丁、影响范围和页面绑定。",
        ],
        "boundary_flags": BOUNDARY_FLAGS,
    }
    return {
        "system_prompt": "You are Xiaojiao prep-room assistant. Return only one strict JSON object. No markdown.",
        "user_prompt": json.dumps(request, ensure_ascii=False, separators=(",", ":")),
    }


def call_model(model: str, case_id: str, prompt: dict[str, str], max_tokens: int) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        result = providers.generate_json_patch(
            {"mode": STAGE, "case_id": case_id, "model": model},
            prompt,
            {
                "provider": "openai_compatible",
                "model": model,
                "temperature": 0.1,
                "max_tokens": max_tokens,
                "timeout_ms": 120000,
                "use_response_format": True,
                "use_reasoning_split": False,
            },
        )
        elapsed_ms = round((time.perf_counter() - started) * 1000)
        provider_meta = result.get("provider_meta") if isinstance(result.get("provider_meta"), dict) else {}
        return {
            "ok": True,
            "model": model,
            "case_id": case_id,
            "latency_ms": provider_meta.get("latency_ms") or elapsed_ms,
            "raw_text": str(result.get("raw_text") or ""),
            "provider_meta": {
                "provider": provider_meta.get("provider"),
                "model": provider_meta.get("model"),
                "credential_source": provider_meta.get("credential_source"),
                "reasoning_split": provider_meta.get("reasoning_split"),
            },
        }
    except Exception as exc:  # noqa: BLE001 - comparison report needs provider errors.
        elapsed_ms = round((time.perf_counter() - started) * 1000)
        return {
            "ok": False,
            "model": model,
            "case_id": case_id,
            "latency_ms": elapsed_ms,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "raw_text": "",
            "provider_meta": {},
        }


def evaluate_json_probe(record: dict[str, Any]) -> dict[str, Any]:
    raw = record.get("raw_text") or ""
    try:
        parsed = json.loads(raw)
        strict_json_success = isinstance(parsed, dict) and parsed.get("ok") is True and parsed.get("task") == "json_probe"
    except Exception as exc:  # noqa: BLE001
        parsed = None
        strict_json_success = False
        record["parse_error"] = str(exc)
    return {
        "strict_json_success": strict_json_success,
        "parsed": parsed,
        "raw_length": len(raw),
    }


def coverage_errors(parsed: dict[str, Any] | None) -> list[str]:
    if not isinstance(parsed, dict):
        return ["parsed_not_object"]
    errors: list[str] = []
    patches = parsed.get("field_patch_candidates")
    patch_text = json.dumps(patches, ensure_ascii=False) if patches is not None else ""
    if "学情" not in patch_text and "analysis" not in patch_text:
        errors.append("missing_analysis_patch")
    if "探究" not in patch_text and "explore" not in patch_text:
        errors.append("missing_explore_patch")
    impact_text = json.dumps(parsed.get("impact_scope"), ensure_ascii=False)
    for key in ["big_screen", "handout", "evidence_note"]:
        if key not in impact_text:
            errors.append(f"missing_impact_{key}")
    step_text = json.dumps(parsed.get("step_reasoning_updates"), ensure_ascii=False)
    if "探究" not in step_text and "explore" not in step_text:
        errors.append("missing_explore_step_update")
    return errors


def teacher_quality_score(parsed: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(parsed, dict):
        return {"score": 0, "signals": [], "issues": ["no_parsed_payload"]}
    visible_payload = {
        key: value
        for key, value in parsed.items()
        if key
        not in {
            "boundary_flags",
            "must_return_shape",
            "hard_rules",
            "fixed_lesson_context",
            "extra_requirements",
            "task",
            "stage_id",
        }
    }
    text = json.dumps(visible_payload, ensure_ascii=False)
    signals = []
    issues = []
    signal_terms = {
        "student_blocker": ["好看", "说不清", "理由", "冷暖"],
        "teacher_action": ["追问", "示范", "巡视", "引导"],
        "student_action": ["分类", "观察", "说出", "记录"],
        "resource_timing": ["大屏", "学习单", "色卡", "词卡"],
        "assessment": ["证据", "能否", "评价", "说明"],
        "risk_adjustment": ["如果", "卡住", "调整", "减少"],
    }
    for key, terms in signal_terms.items():
        if any(term in text for term in terms):
            signals.append(key)
        else:
            issues.append(f"missing_{key}")
    forbidden = ["schema", "provider", "database", "memory", "Feishu", "formal_apply"]
    forbidden_hits = [term for term in forbidden if term in text]
    if forbidden_hits:
        issues.append("forbidden_terms:" + ",".join(forbidden_hits))
    return {"score": len(signals), "signals": signals, "issues": issues}


def evaluate_lesson_reasoning(record: dict[str, Any]) -> dict[str, Any]:
    raw = record.get("raw_text") or ""
    parsed, parser_meta = parse_lesson_reasoning_output(raw, record.get("provider_meta") or {})
    contract_errors = validate_compact_lesson_reasoning_payload(parsed)
    contract_errors.extend(coverage_errors(parsed))
    quality = teacher_quality_score(parsed)
    return {
        "strict_json_success": parser_meta.get("parser_mode") == "strict_json_parser" and not parser_meta.get("parse_error_code"),
        "contract_pass": not contract_errors,
        "contract_errors": contract_errors,
        "parser_meta": parser_meta,
        "teacher_quality": quality,
        "raw_length": len(raw),
        "parsed": parsed,
    }


def rank_models(case_results: list[dict[str, Any]]) -> dict[str, Any]:
    scores: dict[str, int] = {model: 0 for model in MODELS}
    details: dict[str, list[str]] = {model: [] for model in MODELS}
    for item in case_results:
        model = item["model"]
        evaluation = item["evaluation"]
        if evaluation.get("strict_json_success"):
            scores[model] += 2
            details[model].append(f"{item['case_id']}: strict_json +2")
        if evaluation.get("contract_pass"):
            scores[model] += 3
            details[model].append(f"{item['case_id']}: contract +3")
        quality = evaluation.get("teacher_quality") or {}
        scores[model] += int(quality.get("score") or 0)
        if quality:
            details[model].append(f"{item['case_id']}: teacher_quality +{quality.get('score')}")
        latency = int(item.get("latency_ms") or 0)
        if latency and latency < 3000:
            scores[model] += 1
            details[model].append(f"{item['case_id']}: latency_under_3s +1")
    winner = max(scores, key=lambda model: scores[model])
    return {
        "scores": scores,
        "details": details,
        "winner": winner,
        "recommendation": (
            "Use the winner for structured prep-room reasoning by default, then keep the other model as fallback."
            if scores[MODELS[0]] != scores[MODELS[1]]
            else "Scores tied; prefer MiniMax-M3 for future long-context/agentic tasks and keep M2.7-highspeed for speed fallback."
        ),
    }


def write_report(result: dict[str, Any]) -> None:
    lines = [
        "# 1013N MiniMax M3 vs M2.7-highspeed Comparison",
        "",
        f"- FINAL_STATUS: `{result['final_status']}`",
        f"- Winner: `{result['model_ranking']['winner']}`",
        "- Scope: two live read-only model calls per model, no DB/memory/Feishu write, no formal apply.",
        "",
        "## Scores",
        "",
    ]
    for model, score in result["model_ranking"]["scores"].items():
        lines.append(f"- `{model}`: {score}")
    lines += ["", "## Case Summary", ""]
    for item in result["case_results"]:
        ev = item["evaluation"]
        lines.append(
            f"- `{item['model']}` / `{item['case_id']}`: latency `{item['latency_ms']}ms`, "
            f"strict_json `{ev.get('strict_json_success')}`, contract `{ev.get('contract_pass', 'n/a')}`, "
            f"quality `{(ev.get('teacher_quality') or {}).get('score', 'n/a')}`"
        )
        errors = ev.get("contract_errors") or ev.get("teacher_quality", {}).get("issues") or []
        if errors:
            lines.append(f"  - issues: {', '.join(str(e) for e in errors[:8])}")
    lines += [
        "",
        "## Interpretation",
        "",
        result["interpretation"],
        "",
        "## Boundary",
        "",
        "- Provider/model calls were made for comparison only.",
        "- No formal lesson text was applied.",
        "- No database, memory, or Feishu write was performed.",
    ]
    (OUT_DIR / "1013N_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cases = [
        ("json_probe", build_json_probe_prompt(), 400, evaluate_json_probe),
        ("lesson_reasoning_standard_daily", build_lesson_reasoning_prompt(), 5000, evaluate_lesson_reasoning),
    ]
    case_results = []
    for case_id, prompt, max_tokens, evaluator in cases:
        for model in MODELS:
            record = call_model(model, case_id, prompt, max_tokens)
            evaluation = evaluator(record) if record.get("ok") else {"strict_json_success": False, "contract_pass": False, "provider_error": record.get("error")}
            case_results.append(
                {
                    "case_id": case_id,
                    "model": model,
                    "ok": record.get("ok"),
                    "latency_ms": record.get("latency_ms"),
                    "provider_meta": record.get("provider_meta"),
                    "evaluation": evaluation,
                    "raw_text_redacted_prefix": (record.get("raw_text") or "")[:1200],
                    "error": record.get("error"),
                }
            )

    ranking = rank_models(case_results)
    m3 = next(item for item in case_results if item["case_id"] == "lesson_reasoning_standard_daily" and item["model"] == "MiniMax-M3")
    m27 = next(item for item in case_results if item["case_id"] == "lesson_reasoning_standard_daily" and item["model"] == "MiniMax-M2.7-highspeed")
    interpretation = (
        "For this prep-room structured reasoning sample, compare strict JSON first, then contract coverage, then teacher-readable quality. "
        f"M3 contract_pass={m3['evaluation'].get('contract_pass')} and quality={m3['evaluation'].get('teacher_quality', {}).get('score')}; "
        f"M2.7-highspeed contract_pass={m27['evaluation'].get('contract_pass')} and quality={m27['evaluation'].get('teacher_quality', {}).get('score')}."
    )
    result = {
        "stage": STAGE,
        "final_status": "PASS_MINIMAX_M3_VS_M27_HIGHSPEED_COMPARISON",
        "models": MODELS,
        "model_ranking": ranking,
        "interpretation": interpretation,
        "case_results": case_results,
        "provider_called": True,
        "model_called": True,
        "teacher_review_required": True,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }
    write_json(OUT_DIR / "1013N_result.json", result)
    write_json(OUT_DIR / "1013N_case_results.json", case_results)
    write_json(OUT_DIR / "1013N_model_ranking.json", ranking)
    write_report(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
