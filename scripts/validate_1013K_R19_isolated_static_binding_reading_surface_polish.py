from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = OUT / "1013K_R19_isolated_static_binding_reading_surface_polish"
HTML = STAGE / "isolated_static_binding_reading_surface_polish_1013K_R19.html"
RESULT = STAGE / "1013K_R19_result.json"
MOUNT_MAP = STAGE / "renderer_chunk_mount_map_1013K_R19.json"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main() -> None:
    if not HTML.exists():
        fail(f"missing html: {HTML}")
    if not RESULT.exists():
        fail(f"missing result: {RESULT}")
    if not MOUNT_MAP.exists():
        fail(f"missing mount map: {MOUNT_MAP}")

    html = HTML.read_text(encoding="utf-8")
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    mount_map = json.loads(MOUNT_MAP.read_text(encoding="utf-8"))

    checks: list[tuple[str, bool]] = [
        ("final_status", result.get("final_status") == "PASS_1013K_R19_ISOLATED_STATIC_BINDING_READING_SURFACE_POLISH"),
        ("binding_mode", 'data-binding-mode="isolated_static_fixture"' in html),
        ("stage_marker", "1013K_R19_ISOLATED_STATIC_BINDING_READING_SURFACE_POLISH" in html),
        ("material_prompt_lightweight", result.get("material_prompt_lightweight") is True and "还缺教材材料" in html),
        ("continuous_reading_flow", result.get("continuous_reading_flow") is True and ".unit-section { border-top:" in html),
        ("frontend_not_modified", result.get("formal_frontend_page_modified") is False),
        ("runtime_not_connected", result.get("runtime_connected") is False),
        ("provider_not_called", result.get("provider_called") is False),
        ("model_not_called", result.get("model_called") is False),
        ("formal_apply_not_performed", result.get("formal_apply_performed") is False),
        ("storage_not_written", all(result.get(k) is False for k in ("database_written", "memory_written", "feishu_written"))),
    ]

    expected_chunks = mount_map.get("chunks", [])
    actual_chunks = re.findall(r'data-chunk-id="([^"]+)"', html)
    checks.append(("chunk_count", len(actual_chunks) == 10 and result.get("chunk_count") == 10))
    checks.append(("chunk_ids_preserved", actual_chunks == expected_chunks))

    failed = [name for name, ok in checks if not ok]
    if failed:
        fail(", ".join(failed))

    print("PASS: 1013K_R19 isolated static binding reading surface polish")


if __name__ == "__main__":
    main()
