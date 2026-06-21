# 1013M_R1_R3 Art Demonstration Backend Binding Package

## Status

```text
PASS_1013M_R1_R3_ART_DEMONSTRATION_BACKEND_BINDING_PACKAGE
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
