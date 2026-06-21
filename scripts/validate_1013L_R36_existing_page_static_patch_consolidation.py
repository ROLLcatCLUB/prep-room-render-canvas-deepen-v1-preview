from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R35_HTML = (
    BASE
    / "1013L_R35_paragraph_level_courseware_cards"
    / "prep_room_render_canvas_deepen_v1_1013L_R35_paragraph_courseware_cards.html"
)
R36_DIR = BASE / "1013L_R36_existing_page_static_patch_consolidation"
R36_HTML = R36_DIR / "prep_room_render_canvas_deepen_v1_1013L_R36_consolidated.html"
R36_RESULT = R36_DIR / "1013L_R36_result.json"
R36_SMOKE = R36_DIR / "static_patch_consolidation_smoke_1013L_R36.json"
R36_REPORT = R36_DIR / "1013L_R36_report.md"

FINAL_STATUS = "PASS_1013L_R36_EXISTING_PAGE_STATIC_PATCH_CONSOLIDATION"

OLD_PATCH_IDS = [
    "style-1013L-R22-courseware-markers",
    "style-1013L-R23-marker-reading-polish",
    "style-1013L-R24-static-closed-loop",
    "style-1013L-R25-courseware-focus-adapter",
    "style-1013L-R26-courseware-screen-switch",
    "style-1013L-R27-courseware-tool-actions",
    "style-1013L-R29-marker-edit-scope-patch",
    "style-1013L-R30-center-hints-edit-bubble-fix",
    "style-1013L-R31-pointed-edit-bubble",
    "style-1013L-R32-right-rail-courseware-cards",
    "style-1013L-R33-process-cards-scroll",
    "style-1013L-R34-process-courseware-cards-visible",
    "style-1013L-R35-paragraph-courseware-cards",
    "script-1013L-R22-courseware-markers",
    "script-1013L-R23-marker-reading-polish",
    "script-1013L-R24-static-closed-loop",
    "script-1013L-R25-courseware-focus-adapter",
    "script-1013L-R26-courseware-screen-switch",
    "script-1013L-R27-courseware-tool-actions",
    "script-1013L-R29-marker-edit-scope-patch",
    "script-1013L-R30-center-hints-edit-bubble-fix",
    "script-1013L-R31-pointed-edit-bubble",
    "script-1013L-R32-right-rail-courseware-cards",
    "script-1013L-R33-process-cards-scroll",
    "script-1013L-R34-process-courseware-cards-visible",
    "script-1013L-R35-paragraph-courseware-cards",
]

BOUNDARY_FALSE_KEYS = [
    "runtime_connected",
    "provider_called",
    "model_called",
    "database_written",
    "memory_written",
    "feishu_written",
    "upload_implemented",
    "search_implemented",
    "material_library_connected",
    "whiteboard_library_connected",
    "formal_apply_performed",
    "formal_frontend_binding_performed",
    "main_project_pushed",
    "github_uploaded",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def fail(name: str, failed: list[str], detail: str | None = None) -> None:
    failed.append(name if detail is None else f"{name}: {detail}")


def main() -> None:
    failed: list[str] = []

    for path in [R35_HTML, R36_HTML, R36_RESULT, R36_SMOKE, R36_REPORT]:
        if not path.exists():
            fail("missing_file", failed, str(path))

    if failed:
        raise SystemExit("FAIL: " + "; ".join(failed))

    html = R36_HTML.read_text(encoding="utf-8")
    result = read_json(R36_RESULT)
    smoke = read_json(R36_SMOKE)

    if result.get("final_status") != FINAL_STATUS:
        fail("final_status", failed, str(result.get("final_status")))
    if result.get("failed_checks") != []:
        fail("result_failed_checks", failed, str(result.get("failed_checks")))
    if not result.get("old_versions_preserved"):
        fail("old_versions_preserved", failed)
    source_r35 = ROOT / result.get("source_r35_preserved", "")
    if source_r35 != R35_HTML:
        fail("source_r35_preserved", failed, str(result.get("source_r35_preserved")))

    old_hits = [patch_id for patch_id in OLD_PATCH_IDS if patch_id in html]
    if old_hits:
        fail("old_patch_ids_absent", failed, ", ".join(old_hits[:5]))

    required_html_markers = [
        "style-1013L-R36-consolidated",
        "script-1013L-R36-consolidated",
        "r36-inline-screen-card",
        "paragraphMap",
        "r36-edit-bubble",
        "r36-right-selected",
        "data-1013l-r36-selected-screen",
        "data-1013l-r36-independent-scroll",
    ]
    missing_markers = [marker for marker in required_html_markers if marker not in html]
    if missing_markers:
        fail("required_html_markers", failed, ", ".join(missing_markers))

    true_smoke_keys = [
        "html_created",
        "r36_style_injected",
        "r36_script_injected",
        "old_patch_styles_removed",
        "old_patch_scripts_removed",
        "paragraph_cards_consolidated",
        "edit_bubble_consolidated",
        "right_draft_selection_consolidated",
        "independent_scroll_consolidated",
        "set_interval_reduced",
        "mutation_observer_reduced_or_equal",
    ]
    for key in true_smoke_keys:
        if smoke.get(key) is not True:
            fail(f"smoke_{key}", failed, str(smoke.get(key)))

    before = smoke.get("before_metrics", {})
    after = smoke.get("after_metrics", {})
    if after.get("script_tags", 9999) >= before.get("script_tags", 0):
        fail("script_tag_count_reduced", failed, f"{before.get('script_tags')} -> {after.get('script_tags')}")
    if after.get("style_tags", 9999) >= before.get("style_tags", 0):
        fail("style_tag_count_reduced", failed, f"{before.get('style_tags')} -> {after.get('style_tags')}")
    if after.get("set_interval_count", 9999) >= before.get("set_interval_count", 0):
        fail(
            "set_interval_count_reduced",
            failed,
            f"{before.get('set_interval_count')} -> {after.get('set_interval_count')}",
        )

    for key in BOUNDARY_FALSE_KEYS:
        if result.get(key) is not False:
            fail(f"result_boundary_{key}", failed, str(result.get(key)))
        if smoke.get(key) is not False:
            fail(f"smoke_boundary_{key}", failed, str(smoke.get(key)))

    if failed:
        raise SystemExit("FAIL: " + "; ".join(failed))

    print("PASS: 1013L R36 existing page static patch consolidation")
    print(f"HTML: {R36_HTML}")
    print(
        "metrics: "
        f"scripts {before.get('script_tags')}->{after.get('script_tags')}, "
        f"styles {before.get('style_tags')}->{after.get('style_tags')}, "
        f"setInterval {before.get('set_interval_count')}->{after.get('set_interval_count')}"
    )


if __name__ == "__main__":
    main()
