from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.xiaobei_ai.prep_room_art_demonstration_binding_1013M_R1_R3 import (
    STAGE_ID,
    build_art_demonstration_backend_binding_package,
    validate_art_demonstration_backend_binding_package,
)


BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE_DIR = BASE / "1013M_R1_R3_art_demonstration_backend_binding_package"


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.write_text(value, encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def main() -> None:
    STAGE_DIR.mkdir(parents=True, exist_ok=True)
    package = build_art_demonstration_backend_binding_package(ROOT)
    errors = validate_art_demonstration_backend_binding_package(package)

    envelope = package["request_envelope"]
    prompt_binding = package["prompt_binding"]
    normalized = package["normalized_output"]
    courseware = package["courseware_screen_seed_bundle"]

    write_json(STAGE_DIR / "art_demonstration_request_envelope_1013M_R1.json", envelope)
    write_json(STAGE_DIR / "art_demonstration_prompt_binding_1013M_R2.json", prompt_binding)
    write_json(STAGE_DIR / "art_demonstration_normalized_output_1013M_R3.json", normalized)
    write_json(STAGE_DIR / "art_demonstration_courseware_screen_seeds_1013M_R3.json", courseware)
    write_json(STAGE_DIR / "art_demonstration_backend_binding_package_1013M_R1_R3.json", package)

    result = {
        "stage": STAGE_ID,
        "final_status": "PASS_1013M_R1_R3_ART_DEMONSTRATION_BACKEND_BINDING_PACKAGE" if not errors else "FAIL_1013M_R1_R3_ART_DEMONSTRATION_BACKEND_BINDING_PACKAGE",
        "request_envelope_created": True,
        "prompt_binding_created": True,
        "normalized_output_created": True,
        "courseware_screen_seeds_created": True,
        "art_demonstration_required": envelope["art_demonstration_and_visual_scaffold_required"],
        "required_field_count": len(envelope["required_fields"]),
        "normalized_step_id": normalized["process_step_insert"]["id"],
        "courseware_screen_seed_count": courseware["screen_seed_count"],
        "reuse_1013E_lesson_reasoning_contract": package["reuse_policy"]["reuse_1013E_lesson_reasoning_contract"],
        "reuse_1013K_courseware_screen_seed_shape": package["reuse_policy"]["reuse_1013K_courseware_screen_seed_shape"],
        "runtime_contract_patch_applied": False,
        "new_disconnected_page_created": False,
        "provider_called": False,
        "model_called": False,
        "runtime_connected": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "main_project_pushed": False,
        "validator_pass": not errors,
        "failed_checks": errors,
        "outputs": {
            "request_envelope": rel(STAGE_DIR / "art_demonstration_request_envelope_1013M_R1.json"),
            "prompt_binding": rel(STAGE_DIR / "art_demonstration_prompt_binding_1013M_R2.json"),
            "normalized_output": rel(STAGE_DIR / "art_demonstration_normalized_output_1013M_R3.json"),
            "courseware_screen_seeds": rel(STAGE_DIR / "art_demonstration_courseware_screen_seeds_1013M_R3.json"),
            "package": rel(STAGE_DIR / "art_demonstration_backend_binding_package_1013M_R1_R3.json"),
        },
        "next_recommended_stage": "1013M_R4_ART_DEMONSTRATION_TO_EXISTING_PAGE_VIEWMODEL_BINDING",
    }
    write_json(STAGE_DIR / "1013M_R1_R3_result.json", result)

    report = f"""# 1013M_R1_R3 Art Demonstration Backend Binding Package

## Status

```text
{result["final_status"]}
```

## What This Stage Does

This stage connects the R0 `art_demonstration_and_visual_scaffold` contract to a backend-static generation path:

```text
R1 request envelope
-> R2 prompt binding
-> R3 normalized process step
-> R3 courseware screen seeds
```

It does not call a provider/model and does not write the formal lesson body.

## Key Outputs

- `art_demonstration_request_envelope_1013M_R1.json`
- `art_demonstration_prompt_binding_1013M_R2.json`
- `art_demonstration_normalized_output_1013M_R3.json`
- `art_demonstration_courseware_screen_seeds_1013M_R3.json`
- `art_demonstration_backend_binding_package_1013M_R1_R3.json`

## Backend Reuse

This package deliberately reuses existing shapes:

```text
1013E lesson reasoning request / field patch shape
1013E staged derivation process step shape
1013K courseware screen seed shape
1013L render-shell state direction
```

It does not patch the 1013E runtime `ALLOWED_IDS` yet. Instead it records a safe extension candidate:

```text
new_candidate_step_id=demo
runtime_contract_patch_applied=false
```

## Teaching Semantics

The normalized teaching process step is:

```text
id=demo
name=示范与支架
```

The step is intended to sit between:

```text
探究
-> 示范与支架
-> 表现
```

## Boundaries

```text
provider_called=false
model_called=false
runtime_connected=false
database_written=false
memory_written=false
feishu_written=false
formal_apply_performed=false
lesson_body_modified=false
main_project_pushed=false
```

## Next

Recommended next stage:

```text
1013M_R4_ART_DEMONSTRATION_TO_EXISTING_PAGE_VIEWMODEL_BINDING
```

That stage should make the R1-R3 backend-static output visible through the existing page/viewmodel line, not by creating a disconnected page.
"""
    write_text(STAGE_DIR / "1013M_R1_R3_report.md", report)

    if errors:
        raise SystemExit("FAIL: " + ", ".join(errors))
    print(f"PASS: {STAGE_ID}")


if __name__ == "__main__":
    main()
