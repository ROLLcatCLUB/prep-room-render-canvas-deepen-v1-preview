# 1013I_R6C Curriculum Standard Control Layer Contract

```text
STAGE=1013I_R6C_CURRICULUM_STANDARD_CONTROL_LAYER_CONTRACT
FINAL_STATUS=PASS_1013I_R6C_CURRICULUM_STANDARD_CONTROL_LAYER_CONTRACT
INHERITS_FROM=1013I_R6B_R1_REVIEW_MANIFEST_ALIGNMENT
NEXT_STAGE=1013I_R6D_TEXTBOOK_ANCHOR_AND_BIG_UNIT_DESIGN_CHAIN_CONTRACT
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Purpose

R6C defines `curriculum_standard_control_layer` as the upstream constraint layer for teacher self-prep, big-unit context judgement, lesson-position judgement, candidate-card generation, and later render surfaces.

This stage is contract-only. It does not parse real curriculum-standard full text, does not create official curriculum claims, does not generate a big-unit design, and does not generate a single-lesson plan.

## Control Fields

- `standard_version_label`: required=true, mode=structured_ref_or_missing
- `subject`: required=true, mode=teacher_input_or_textbook_context
- `school_stage`: required=true, mode=teacher_input_or_structured_ref
- `grade_band`: required=true, mode=teacher_input_or_structured_ref
- `art_domain_or_learning_domain`: required=true, mode=structured_ref_or_teacher_confirm
- `core_literacy_tags`: required=true, mode=structured_ref_or_candidate_with_teacher_confirm
- `learning_task_direction`: required=true, mode=structured_ref_or_missing
- `assessment_requirement`: required=true, mode=structured_ref_or_missing
- `academic_quality_or_performance_evidence`: required=true, mode=structured_ref_or_missing
- `content_scope_boundary`: required=true, mode=structured_ref_or_missing
- `prohibited_overreach`: required=true, mode=structured_ref_or_missing
- `standard_ref_ids`: required=true, mode=source_ref_or_missing
- `interpretation_status`: required=true, mode=enum
- `teacher_confirmation_status`: required=true, mode=enum

## Priority

1. `curriculum_standard_control_layer` - upstream_constraint: Sets learning direction, competency focus, assessment evidence, and scope boundaries.
2. `textbook_anchor` - required_content_landing: Locates the specific lesson content, unit sequence, materials, and textbook position.
3. `big_unit_context_gate_and_lesson_position` - unit_structure_control: Judges what this lesson is supposed to do inside the larger unit.
4. `teacher_confirmation_gate` - classroom_judgement_inside_required_bounds: Confirms or revises mappings and chooses whether to continue, revise, or use degraded draft mode.
5. `official_case_reference` - reference_only: Offers reusable design moves, field patterns, and wording inspiration only.
6. `provider_or_model_candidate` - candidate_only_when_enabled_later: Later model output must become reviewable candidates, not direct lesson body.

## Chain

```text
teacher_input
-> curriculum_standard_control_layer
-> textbook_anchor_check
-> big_unit_context_gate
-> lesson_position_judgement
-> teacher_confirm_unit_position
-> self_prep_review_cards
-> preview_only
```

## Non-Negotiable Rules

- Curriculum standard is the upstream constraint layer.
- Textbook anchor is required before normal lesson generation.
- Official cases are reference-only and cannot override curriculum standards, textbook anchors, or teacher confirmation.
- Teacher confirmation remains required before candidate cards, but it cannot remove the required standard check.
- R7 visual review remains paused until the standard control, interpretation, textbook anchor, and big-unit design chain are filled.
