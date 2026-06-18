# 1013I R6A Big Unit Context Required Gate

- FINAL_STATUS: `PASS_1013I_R6A_BIG_UNIT_CONTEXT_REQUIRED_GATE`
- NEXT_STAGE: `1013I_R6B_OFFICIAL_BIG_UNIT_MATERIAL_READONLY_EXTRACTION_FIXTURE`
- Scope: contract-only / fixture-only required gate; no real material parsing.

## Decision

Single-lesson prep is paused as a normal path until the system has a big-unit context gate and lesson-position judgement.

Revised chain:

```text
teacher_input -> big_unit_context_gate -> lesson_position_judgement -> teacher_confirm_unit_position -> self_prep_review_cards -> preview_only
```

## Gate Behavior

- Missing big-unit context blocks normal single-lesson prep.
- A degraded single-lesson draft is allowed only as a clearly labeled temporary mode.
- Official big-unit materials enter later through read-only extraction, then teacher confirmation.

## Boundary

- r7_visual_review_paused=true
- r6_product_semantics_changed=false
- actual_material_parsing_performed=false
- provider_called=false
- model_called=false
- formal_apply_performed=false
- lesson_body_modified=false
- html_body_modified=false
- database_written=false
- memory_written=false
- feishu_written=false
