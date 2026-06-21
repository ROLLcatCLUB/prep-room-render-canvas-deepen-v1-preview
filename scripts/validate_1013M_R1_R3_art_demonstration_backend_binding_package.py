from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.xiaobei_ai.prep_room_art_demonstration_binding_1013M_R1_R3 import (
    validate_art_demonstration_backend_binding_package,
)


BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE_DIR = BASE / "1013M_R1_R3_art_demonstration_backend_binding_package"


REQUIRED_FILES = [
    "art_demonstration_request_envelope_1013M_R1.json",
    "art_demonstration_prompt_binding_1013M_R2.json",
    "art_demonstration_normalized_output_1013M_R3.json",
    "art_demonstration_courseware_screen_seeds_1013M_R3.json",
    "art_demonstration_backend_binding_package_1013M_R1_R3.json",
    "1013M_R1_R3_result.json",
    "1013M_R1_R3_report.md",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    if not STAGE_DIR.exists():
        fail(f"missing stage dir: {STAGE_DIR}")
    for name in REQUIRED_FILES:
        if not (STAGE_DIR / name).exists():
            fail(f"missing file: {name}")

    package = read_json(STAGE_DIR / "art_demonstration_backend_binding_package_1013M_R1_R3.json")
    result = read_json(STAGE_DIR / "1013M_R1_R3_result.json")
    errors = validate_art_demonstration_backend_binding_package(package)
    if errors:
        fail(f"package validation errors: {errors}")

    envelope = read_json(STAGE_DIR / "art_demonstration_request_envelope_1013M_R1.json")
    prompt = read_json(STAGE_DIR / "art_demonstration_prompt_binding_1013M_R2.json")
    normalized = read_json(STAGE_DIR / "art_demonstration_normalized_output_1013M_R3.json")
    seeds = read_json(STAGE_DIR / "art_demonstration_courseware_screen_seeds_1013M_R3.json")

    if envelope.get("art_demonstration_and_visual_scaffold_required") is not True:
        fail("request envelope did not require art demonstration")
    if envelope.get("runtime_contract_patch_applied") is True:
        fail("request envelope should not apply runtime contract patch")
    if "不要只写“教师示范”" not in json.dumps(prompt, ensure_ascii=False):
        fail("prompt binding missing generic-demo guard")
    if normalized.get("process_step_insert", {}).get("id") != "demo":
        fail("normalized output missing demo process step")
    if normalized.get("field_patch_candidate", {}).get("target_section") != "teaching_process":
        fail("normalized field patch must target teaching_process")
    if seeds.get("screen_seed_count") != 5:
        fail("courseware seed count must be 5")
    if not all(seed.get("preview_only") is True for seed in seeds.get("screen_seeds", [])):
        fail("all courseware seeds must be preview_only")

    for false_field in [
        "provider_called",
        "model_called",
        "runtime_connected",
        "database_written",
        "memory_written",
        "feishu_written",
        "formal_apply_performed",
        "lesson_body_modified",
        "main_project_pushed",
    ]:
        if result.get(false_field) is not False:
            fail(f"{false_field} must be false")
    if result.get("validator_pass") is not True:
        fail("result validator_pass must be true")
    if result.get("failed_checks") != []:
        fail("result failed_checks must be []")

    print("PASS: 1013M_R1_R3 art demonstration backend binding package")


if __name__ == "__main__":
    main()
