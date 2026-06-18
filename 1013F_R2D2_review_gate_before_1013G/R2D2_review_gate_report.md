# 1013F R2D2 Review Gate Before 1013G

- FINAL_STATUS: `PASS_R2D2_REVIEW_GATE_BEFORE_1013G`
- NEXT_STAGE: `1013G_PREP_CANDIDATE_REVIEW_SANDBOX`
- Boundary: review only; no HTML write, no formal apply, no 1013G execution, no database/memory/Feishu write.

## Gate Decision

R2D2 candidate outputs are acceptable for a later `1013G_PREP` candidate-review sandbox, but this gate does not enter 1013G and does not apply any lesson text.

`approved` in this report means approved for sandbox preview only. It is not approval for formal apply, not teacher confirmation, and not permission to merge candidate text into the lesson body.

## Approved Candidates

- `r2d2_patch_explore` -> 教学过程 · 探究
  - reasons: keeps_explore_material_light_and_reason_visible
- `r2d2_patch_make` -> 教学过程 · 表现
  - reasons: keeps_default_entry_before_extension
- `r2d2_patch_share` -> 教学过程 · 交流展示
  - reasons: keeps_assessment_observable_and_time_bounded

## Rejected Candidates

- None.

## Required Checks

- patch_candidate_only_schema_pass=true
- registry_schema_pass=true
- teaching_moves_trace_schema_pass=true
- case_reference_direct_copy_hits_clear=true
- html_body_modified=false
- r2b2_layout_baseline_kept=true
- r2c_process_focus_kept=true
- formal_apply_performed=false
- entered_1013G=false
- database_written=false
- memory_written=false
- feishu_written=false
- main_project_pushed=false

## Boundary

- Approved here means approved for a later candidate-review sandbox only.
- It does not mean teacher confirmation has happened.
- It does not mean formal apply is allowed.
