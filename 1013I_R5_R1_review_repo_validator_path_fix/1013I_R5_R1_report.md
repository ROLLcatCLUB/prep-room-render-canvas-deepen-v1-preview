# 1013I R5 R1 Review Repo Validator Path Fix

```text
FINAL_STATUS=PASS_1013I_R5_R1_REVIEW_REPO_VALIDATOR_PATH_FIX
INHERITS_FROM=1013I_R5_TEACHER_SELF_PREP_ALPHA_SMOKE
NEXT_STAGE=1013I_R6_TEACHER_SELF_PREP_RENDER_SURFACE_ALPHA
```

## Scope

R5 product evidence and state boundaries remain accepted. This R5_R1 hotfix only repairs the GitHub review package reproducibility entrypoint.

The validator is now available at the review repo top-level path:

```text
scripts/validate_1013I_R5_teacher_self_prep_alpha_smoke.py
```

The source-delta copy is still preserved at:

```text
source_delta_1013I_R5/scripts/validate_1013I_R5_teacher_self_prep_alpha_smoke.py
```

This hotfix also records the updated validator source at:

```text
source_delta_1013I_R5_R1/scripts/validate_1013I_R5_teacher_self_prep_alpha_smoke.py
```

## Reproducibility Fix

The validator now supports both layouts:

```text
xiaobei-core root -> outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/
GitHub review repo root -> repo root
```

Fresh clone review commands:

```text
python -m py_compile scripts/validate_1013I_R5_teacher_self_prep_alpha_smoke.py
python scripts/validate_1013I_R5_teacher_self_prep_alpha_smoke.py
python scripts/validate_1013I_R5_teacher_self_prep_alpha_smoke.py --root <repo-root>
```

## Boundary

```text
business_semantics_changed=false
r5_core_result_changed=false
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
main_project_committed=false
main_project_pushed=false
```
