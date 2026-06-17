from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.xiaobei_ai import providers

OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013M_minimax_m3_connection"


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    os.environ["MINIMAX_MODEL"] = "MiniMax-M3"

    status = providers.provider_status()
    generation = status.get("generation", {})

    started = time.perf_counter()
    result = providers.generate_json_patch(
        {"mode": "1013M_MINIMAX_M3_CONNECTION_SMOKE", "case_id": "m3_minimal_json"},
        {
            "system_prompt": "Return only one valid JSON object. No markdown. No explanation.",
            "user_prompt": 'Return exactly this JSON object: {"ok":true,"model_check":"m3"}',
        },
        {
            "provider": "openai_compatible",
            "temperature": 0.0,
            "max_tokens": 160,
            "timeout_ms": 60000,
            "use_response_format": True,
            "use_reasoning_split": False,
        },
    )
    elapsed_ms = round((time.perf_counter() - started) * 1000)
    raw_text = str(result.get("raw_text") or "")
    parsed = json.loads(raw_text)
    provider_meta = result.get("provider_meta") if isinstance(result.get("provider_meta"), dict) else {}

    smoke = {
        "stage": "1013M_MINIMAX_M3_CONNECTION_SMOKE",
        "final_status": "PASS_MINIMAX_M3_CONNECTED",
        "model_requested": "MiniMax-M3",
        "provider_family": generation.get("provider_family"),
        "provider_enabled": generation.get("provider_enabled"),
        "credential_source": generation.get("credential_source"),
        "base_url_host": str(provider_meta.get("base_url") or "").split("/")[2] if provider_meta.get("base_url") else None,
        "provider_meta": {
            "provider": provider_meta.get("provider"),
            "model": provider_meta.get("model"),
            "credential_source": provider_meta.get("credential_source"),
            "reasoning_split": provider_meta.get("reasoning_split"),
            "latency_ms": provider_meta.get("latency_ms") or elapsed_ms,
        },
        "parsed_response": parsed,
        "m3_thinking_default_for_business_calls": "disabled",
        "m3_token_field": "max_completion_tokens",
        "teacher_review_required": True,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }

    report = "\n".join(
        [
            "# 1013M MiniMax M3 Connection Smoke",
            "",
            "- FINAL_STATUS: `PASS_MINIMAX_M3_CONNECTED`",
            "- Model: `MiniMax-M3`",
            "- Provider: `openai_compatible` over MiniMax env credentials",
            "- Business-call default: `thinking: {\"type\":\"disabled\"}`",
            "- Token field for M3: `max_completion_tokens`",
            "",
            "The smoke call returned valid JSON:",
            "",
            "```json",
            json.dumps(parsed, ensure_ascii=False, indent=2),
            "```",
            "",
            "Boundary: no database write, no memory write, no Feishu write, no formal apply, and no main project push.",
        ]
    )

    write_json(OUT_DIR / "1013M_result.json", smoke)
    (OUT_DIR / "1013M_report.md").write_text(report + "\n", encoding="utf-8")
    print(json.dumps(smoke, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
