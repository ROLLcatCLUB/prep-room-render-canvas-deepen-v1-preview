from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6B_R1_REVIEW_MANIFEST_ALIGNMENT"
R6B_STAGE_ID = "1013I_R6B_OFFICIAL_CASE_READONLY_DECONSTRUCTION_FOR_SCHEMA_CALIBRATION"
R6B_PASS_STATUS = "PASS_1013I_R6B_OFFICIAL_CASE_READONLY_DECONSTRUCTION_FOR_SCHEMA_CALIBRATION"
FINAL_STATUS = "PASS_1013I_R6B_R1_REVIEW_MANIFEST_ALIGNMENT"
NEXT_STAGE = "1013I_R6C_CURRICULUM_STANDARD_CONTROL_LAYER_CONTRACT"
OLD_R6_NEXT_STAGE = "1013I_R6_TEACHER_SELF_PREP_RENDER_SURFACE_ALPHA"
R6A_STAGE_ID = "1013I_R6A_BIG_UNIT_CONTEXT_REQUIRED_GATE"
R6_STAGE_ID = "1013I_R6_TEACHER_SELF_PREP_RENDER_SURFACE_ALPHA"

SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)app[_-]?secret\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)tenant[_-]?access[_-]?token\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)cookie\s*[:=]\s*['\"][^'\"]{20,}"),
]

DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_output_root(root: Path) -> Path:
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    if (root / "REVIEW_PACKAGE_MANIFEST.md").exists() and (root / "LATEST_REVIEW_ENTRY.md").exists():
        return root
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def recommended_next_stage(manifest_text: str) -> str:
    match = re.search(
        r"Recommended next product stage:\s*```text\s*(.*?)\s*```",
        manifest_text,
        flags=re.DOTALL,
    )
    if not match:
        return ""
    return match.group(1).strip()


def scan_secrets(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append(str(path))
                break
    return hits


def scan_deprecated_visible_names(paths: list[Path]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name in DEPRECATED_VISIBLE_NAMES:
            if name in text:
                hits.append({"path": str(path), "name": name})
    return hits


def profile_fields() -> dict[str, Any]:
    return {
        "agent_role": "unified_teacher_agent",
        "assistant_profile_present": True,
        "assistant_profile_display_name": "小教",
        "assistant_profile": {
            "display_name": "小教",
            "display_name_customizable": True,
            "wake_name": "小教",
            "voice_profile_id": None,
            "tts_enabled": False,
        },
        "active_space": "prep_room",
        "active_capability": "lesson_prep",
    }


def false_boundaries() -> dict[str, bool]:
    return {
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "official_export_created": False,
        "official_archive_created": False,
        "main_project_pushed": False,
    }


def build_result(output_root: Path) -> dict[str, Any]:
    manifest_path = output_root / "REVIEW_PACKAGE_MANIFEST.md"
    latest_path = output_root / "LATEST_REVIEW_ENTRY.md"
    r6b_result_path = output_root / "1013I_R6B_official_case_readonly_deconstruction" / "1013I_R6B_result.json"

    manifest_text = manifest_path.read_text(encoding="utf-8")
    latest_text = latest_path.read_text(encoding="utf-8")
    r6b_result = read_json(r6b_result_path)

    next_stage_value = recommended_next_stage(manifest_text)
    manifest_includes_r6 = R6_STAGE_ID in manifest_text
    manifest_includes_r6a = R6A_STAGE_ID in manifest_text
    manifest_includes_r6b = R6B_STAGE_ID in manifest_text
    manifest_next_stage_is_r6c = next_stage_value == NEXT_STAGE
    manifest_no_longer_recommends_r6 = next_stage_value != OLD_R6_NEXT_STAGE
    manifest_says_cases_reference_only = "Official cases are reference-only" in manifest_text
    manifest_says_curriculum_standard_upstream = "Curriculum standard is the upstream constraint layer" in manifest_text
    manifest_says_cases_do_not_override = (
        "Official cases must not override curriculum standards, textbook anchors, or teacher confirmation"
        in manifest_text
    )
    r7_pause_recorded = "R7 visual review remains paused" in manifest_text

    latest_entry_already_correct = (
        R6B_STAGE_ID in latest_text
        and f"NEXT_RECOMMENDED_STAGE={NEXT_STAGE}" in latest_text
        and f"NEXT_RECOMMENDED_STAGE={OLD_R6_NEXT_STAGE}" not in latest_text
    )

    r6b_boundary_ok = all(r6b_result.get(key) is value for key, value in false_boundaries().items())
    r6b_result_pass = r6b_result.get("final_status") == R6B_PASS_STATUS
    official_cases_remain_reference_only = r6b_result.get("cases_treated_as_reference_only") is True
    cases_not_treated_as_curriculum_standard = r6b_result.get("cases_not_treated_as_curriculum_standard") is True

    stage_dir = output_root / "1013I_R6B_R1_review_manifest_alignment"
    candidate_stage_files = [
        stage_dir / "1013I_R6B_R1_result.json",
        stage_dir / "1013I_R6B_R1_report.md",
    ]
    teacher_visible_deprecated_agent_hits = scan_deprecated_visible_names(candidate_stage_files)
    secret_scan_paths = [
        manifest_path,
        latest_path,
        r6b_result_path,
        *candidate_stage_files,
    ]
    secret_scan_hits = scan_secrets(secret_scan_paths)

    review_manifest_aligned = all(
        [
            manifest_includes_r6,
            manifest_includes_r6a,
            manifest_includes_r6b,
            manifest_next_stage_is_r6c,
            manifest_no_longer_recommends_r6,
            manifest_says_cases_reference_only,
            manifest_says_curriculum_standard_upstream,
            manifest_says_cases_do_not_override,
            r7_pause_recorded,
        ]
    )

    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": R6B_STAGE_ID,
        "next_stage": NEXT_STAGE,
        "review_manifest_aligned": review_manifest_aligned,
        "latest_entry_already_correct": latest_entry_already_correct,
        "r6b_result_present": r6b_result_path.exists(),
        "r6b_result_pass": r6b_result_pass,
        "r6b_product_semantics_changed": False,
        "manifest_includes_r6": manifest_includes_r6,
        "manifest_includes_r6a": manifest_includes_r6a,
        "manifest_includes_r6b": manifest_includes_r6b,
        "manifest_next_stage": next_stage_value,
        "manifest_next_stage_is_r6c": manifest_next_stage_is_r6c,
        "manifest_no_longer_recommends_r6": manifest_no_longer_recommends_r6,
        "manifest_says_official_cases_reference_only": manifest_says_cases_reference_only,
        "manifest_says_curriculum_standard_upstream": manifest_says_curriculum_standard_upstream,
        "manifest_says_cases_do_not_override": manifest_says_cases_do_not_override,
        "r7_visual_review_pause_recorded": r7_pause_recorded,
        "official_cases_remain_reference_only": official_cases_remain_reference_only,
        "cases_not_treated_as_curriculum_standard": cases_not_treated_as_curriculum_standard,
        "teacher_visible_deprecated_agent_hits": teacher_visible_deprecated_agent_hits,
        "secret_scan_hits": secret_scan_hits,
        "profile_fields_present": True,
        **profile_fields(),
        "formal_apply_allowed": False,
        "provider_model_call_allowed": False,
        **false_boundaries(),
    }

    required_true = [
        "review_manifest_aligned",
        "latest_entry_already_correct",
        "r6b_result_present",
        "r6b_result_pass",
        "manifest_includes_r6",
        "manifest_includes_r6a",
        "manifest_includes_r6b",
        "manifest_next_stage_is_r6c",
        "manifest_no_longer_recommends_r6",
        "manifest_says_official_cases_reference_only",
        "manifest_says_curriculum_standard_upstream",
        "manifest_says_cases_do_not_override",
        "r7_visual_review_pause_recorded",
        "official_cases_remain_reference_only",
        "cases_not_treated_as_curriculum_standard",
        "profile_fields_present",
    ]
    required_false = [
        "r6b_product_semantics_changed",
        "provider_called",
        "model_called",
        "formal_apply_performed",
        "lesson_body_modified",
        "html_body_modified",
        "database_written",
        "memory_written",
        "feishu_written",
        "official_export_created",
        "official_archive_created",
        "main_project_pushed",
    ]

    failures = [key for key in required_true if result.get(key) is not True]
    failures += [key for key in required_false if result.get(key) is not False]
    if teacher_visible_deprecated_agent_hits:
        failures.append("teacher_visible_deprecated_agent_hits")
    if secret_scan_hits:
        failures.append("secret_scan_hits")
    if not r6b_boundary_ok:
        failures.append("r6b_boundary_ok")
    if failures:
        result["final_status"] = "FAIL_1013I_R6B_R1_REVIEW_MANIFEST_ALIGNMENT"
        result["failed_checks"] = failures
    else:
        result["failed_checks"] = []

    return result


def build_report(result: dict[str, Any]) -> str:
    status = result["final_status"]
    return f"""# 1013I_R6B_R1 Review Manifest Alignment Report

```text
STAGE={STAGE_ID}
FINAL_STATUS={status}
INHERITS_FROM={R6B_STAGE_ID}
NEXT_STAGE={NEXT_STAGE}
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Scope

R6B_R1 only aligns the review package manifest. It does not change R6B product semantics, official-case deconstruction data, runtime behavior, lesson body, HTML body, database, memory, Feishu, export, archive, or provider/model behavior.

## Alignment Checks

```text
review_manifest_aligned={str(result["review_manifest_aligned"]).lower()}
latest_entry_already_correct={str(result["latest_entry_already_correct"]).lower()}
r6b_result_pass={str(result["r6b_result_pass"]).lower()}
manifest_includes_r6={str(result["manifest_includes_r6"]).lower()}
manifest_includes_r6a={str(result["manifest_includes_r6a"]).lower()}
manifest_includes_r6b={str(result["manifest_includes_r6b"]).lower()}
manifest_next_stage={result["manifest_next_stage"]}
manifest_no_longer_recommends_r6={str(result["manifest_no_longer_recommends_r6"]).lower()}
manifest_says_official_cases_reference_only={str(result["manifest_says_official_cases_reference_only"]).lower()}
manifest_says_curriculum_standard_upstream={str(result["manifest_says_curriculum_standard_upstream"]).lower()}
manifest_says_cases_do_not_override={str(result["manifest_says_cases_do_not_override"]).lower()}
r7_visual_review_pause_recorded={str(result["r7_visual_review_pause_recorded"]).lower()}
```

## Boundary

```text
r6b_product_semantics_changed=false
official_cases_remain_reference_only={str(result["official_cases_remain_reference_only"]).lower()}
cases_not_treated_as_curriculum_standard={str(result["cases_not_treated_as_curriculum_standard"]).lower()}
provider_called=false
model_called=false
formal_apply_performed=false
lesson_body_modified=false
html_body_modified=false
database_written=false
memory_written=false
feishu_written=false
official_export_created=false
official_archive_created=false
main_project_pushed=false
```

## Conclusion

The R6B review package manifest now reflects the accepted R6/R6A/R6B baseline and points the next stage to R6C curriculum-standard control. Official cases remain reference-only and cannot override curriculum standards, textbook anchors, or teacher confirmation.
"""


def copy_source_delta(repo_root: Path) -> None:
    source = repo_root / "scripts" / Path(__file__).name
    target = (
        repo_root
        / "outputs"
        / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
        / "source_delta_1013I_R6B_R1"
        / "scripts"
        / Path(__file__).name
    )
    if source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()

    root = args.root.resolve()
    output_root = resolve_output_root(root)
    result = build_result(output_root)

    stage_dir = output_root / "1013I_R6B_R1_review_manifest_alignment"
    result_path = stage_dir / "1013I_R6B_R1_result.json"
    report_path = stage_dir / "1013I_R6B_R1_report.md"
    write_json(result_path, result)
    write_text(report_path, build_report(result))

    local_repo_root = repo_root_from_script()
    if (local_repo_root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1").exists():
        copy_source_delta(local_repo_root)

    if result["final_status"] != FINAL_STATUS:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    print(f"{FINAL_STATUS}: {result_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
