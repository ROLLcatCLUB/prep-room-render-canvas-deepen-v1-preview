from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R16A_DIR = BASE / "1013L_R16A_r5_guard_closure_note_for_current_line"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def read_json(path: Path):
    if not path.exists():
        fail(f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def assert_true(payload: dict, key: str) -> None:
    if payload.get(key) is not True:
        fail(f"expected true flag: {key}")


def assert_false(payload: dict, key: str) -> None:
    if payload.get(key) is not False:
        fail(f"expected false flag: {key}")


def main() -> None:
    result = read_json(R16A_DIR / "1013L_R16A_result.json")
    matrix = read_json(R16A_DIR / "r5_guard_closure_matrix_1013L_R16A.json")
    report = R16A_DIR / "1013L_R16A_report.md"
    if not report.exists():
        fail("missing R16A report")

    if result.get("final_status") != "PASS_1013L_R16A_R5_GUARD_CLOSURE_NOTE_FOR_CURRENT_LINE":
        fail("unexpected R16A final status")
    if result.get("failed_checks") != []:
        fail(f"R16A has failed checks: {result.get('failed_checks')}")

    for key in [
        "r5_guard_closure_created",
        "visible_agent_name_guard_closed",
        "legacy_hidden_xiaobei_recorded_as_customizable_profile",
        "state_count_gap_documented",
        "prep_notebook_registry_only_alias_documented",
        "route_evidence_held_for_runtime_smoke",
        "runtime_route_smoke_required_before_real_binding",
        "current_line_teacher_visible_engineering_copy_fixed",
        "guard_closure_note_only",
        "existing_page_reused",
    ]:
        assert_true(result, key)

    for key in [
        "new_visible_page_created",
        "new_shell_standard_created",
        "runtime_connected",
        "real_fetch_performed",
        "provider_called",
        "model_called",
        "database_written",
        "memory_written",
        "feishu_written",
        "formal_apply_performed",
        "main_project_pushed",
        "github_uploaded",
        "formal_frontend_binding_allowed",
    ]:
        assert_false(result, key)

    guards = matrix.get("guards", [])
    if len(guards) != 3:
        fail("R16A guard count mismatch")
    guard_ids = {guard.get("guard_id") for guard in guards}
    expected = {
        "R5_GUARD_A_VISIBLE_AGENT_NAME",
        "R5_GUARD_B_STATE_COUNT_ALIGNMENT",
        "R5_GUARD_C_ROUTE_EVIDENCE",
    }
    if guard_ids != expected:
        fail(f"unexpected guard ids: {guard_ids}")

    name_scan = matrix.get("name_scan", {})
    if name_scan.get("deprecated_visible_phrase_hits") != []:
        fail(f"deprecated visible phrase hits remain: {name_scan.get('deprecated_visible_phrase_hits')}")
    for phrase in [
        "小教草稿",
        "对小教说一句",
        "编辑会在弹窗里处理，教师确认前不写入正式备课本。",
    ]:
        if phrase not in name_scan.get("required_current_phrase_hits", []):
            fail(f"missing current visible phrase evidence: {phrase}")

    state_guard = next(guard for guard in guards if guard.get("guard_id") == "R5_GUARD_B_STATE_COUNT_ALIGNMENT")
    evidence = state_guard.get("evidence", {})
    if evidence.get("registry_state_count") != 8:
        fail("registry_state_count should remain 8 in R5 evidence")
    if evidence.get("adapter_state_count") != 7:
        fail("adapter_state_count should remain 7 in R5 evidence")
    if evidence.get("registry_only_states") != ["prep_notebook"]:
        fail(f"unexpected registry_only_states: {evidence.get('registry_only_states')}")

    route_guard = next(guard for guard in guards if guard.get("guard_id") == "R5_GUARD_C_ROUTE_EVIDENCE")
    if route_guard.get("current_line_status") != "HELD_FOR_REAL_RUNTIME_ROUTE_SMOKE":
        fail("route guard should be held for runtime smoke")
    next_runtime_guard = matrix.get("next_runtime_guard", {})
    if next_runtime_guard.get("required_before_real_runtime_binding") is not True:
        fail("runtime route smoke guard missing")
    if len(next_runtime_guard.get("must_check", [])) < 8:
        fail("runtime route smoke must_check list too short")

    print("PASS: 1013L R16A R5 guard closure note for current line")


if __name__ == "__main__":
    main()
