from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAGE_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013M_R0_art_demonstration_and_visual_scaffold_contract"


REQUIRED_FILES = [
    "art_demonstration_visual_scaffold_contract_1013M_R0.md",
    "art_demonstration_visual_scaffold_schema_1013M_R0.json",
    "art_demonstration_prompt_policy_1013M_R0.md",
    "courseware_mapping_for_demonstration_1013M_R0.json",
    "sample_fixture_color_contrast_harmony_1013M_R0.json",
    "prep_room_render_canvas_deepen_v1_1013M_R0_art_demo_visual_scaffold.html",
    "1013M_R0_report.md",
    "1013M_R0_result.json",
]

REQUIRED_SCHEMA_FIELDS = [
    "demo_purpose",
    "visual_attention_points",
    "tools_and_techniques",
    "drawing_process_steps",
    "memory_phrase",
    "common_mistakes_and_repairs",
    "peer_example_scaffold",
    "anti_copy_guidance",
    "pre_creation_check",
    "assessment_link",
]

REQUIRED_PAGE_TEXT = [
    'id: "demo"',
    'name: "示范与支架"',
    "色彩三部曲",
    "先定主色，再找伙伴，最后一点亮",
    "借鉴不照抄",
    'demo: ["明确看点", "示范技法", "记住口令", "辨析错例", "借鉴不照抄"]',
]

BOUNDARY_FALSE_FIELDS = [
    "runtime_connected",
    "provider_called",
    "model_called",
    "database_written",
    "memory_written",
    "feishu_written",
    "formal_apply_performed",
    "main_project_pushed",
    "github_uploaded",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict:
    return json.loads(read_text(path))


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    if not STAGE_DIR.exists():
        fail(f"missing stage dir: {STAGE_DIR}")

    for name in REQUIRED_FILES:
        if not (STAGE_DIR / name).exists():
            fail(f"missing required file: {name}")

    schema = read_json(STAGE_DIR / "art_demonstration_visual_scaffold_schema_1013M_R0.json")
    block = schema.get("demonstration_block") or {}
    missing_schema_fields = [field for field in REQUIRED_SCHEMA_FIELDS if field not in block]
    if missing_schema_fields:
        fail(f"missing schema fields: {missing_schema_fields}")

    prompt_policy = read_text(STAGE_DIR / "art_demonstration_prompt_policy_1013M_R0.md")
    for phrase in ["教师示范", "三步口令", "同龄作品", "不照抄"]:
        if phrase not in prompt_policy:
            fail(f"prompt policy missing phrase: {phrase}")

    mapping = read_json(STAGE_DIR / "courseware_mapping_for_demonstration_1013M_R0.json")
    screen_types = {item.get("screen_type") for item in mapping.get("screen_mappings", [])}
    for required in [
        "teacher_demo_screen",
        "step_mantra_screen",
        "mistake_comparison_screen",
        "peer_example_screen",
        "pre_creation_check_screen",
    ]:
        if required not in screen_types:
            fail(f"missing courseware screen type: {required}")

    fixture = read_json(STAGE_DIR / "sample_fixture_color_contrast_harmony_1013M_R0.json")
    demo = fixture.get("art_demonstration_and_visual_scaffold") or {}
    for field in [
        "memory_phrase",
        "drawing_process_steps",
        "peer_example_scaffold",
        "anti_copy_guidance",
        "pre_creation_check",
    ]:
        if not demo.get(field):
            fail(f"sample fixture missing field: {field}")

    html = read_text(STAGE_DIR / "prep_room_render_canvas_deepen_v1_1013M_R0_art_demo_visual_scaffold.html")
    for phrase in REQUIRED_PAGE_TEXT:
        if phrase not in html:
            fail(f"page missing required text: {phrase}")

    result = read_json(STAGE_DIR / "1013M_R0_result.json")
    if result.get("r36_baseline_overwritten") is not False:
        fail("r36_baseline_overwritten must be false")
    if result.get("new_disconnected_page_created") is not False:
        fail("new_disconnected_page_created must be false")
    if result.get("inserted_step_id") != "demo":
        fail("inserted_step_id must be demo")
    if result.get("preview_only") is not True:
        fail("preview_only must be true")
    for field in BOUNDARY_FALSE_FIELDS:
        if result.get(field) is not False:
            fail(f"{field} must be false")

    print("PASS: 1013M_R0 art demonstration and visual scaffold contract")


if __name__ == "__main__":
    main()
