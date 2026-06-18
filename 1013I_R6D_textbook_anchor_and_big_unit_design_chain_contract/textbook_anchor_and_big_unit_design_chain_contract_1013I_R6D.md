# 1013I_R6D Textbook Anchor And Big Unit Design Chain Contract

```text
STAGE=1013I_R6D_TEXTBOOK_ANCHOR_AND_BIG_UNIT_DESIGN_CHAIN_CONTRACT
FINAL_STATUS=PASS_1013I_R6D_TEXTBOOK_ANCHOR_AND_BIG_UNIT_DESIGN_CHAIN_CONTRACT
INHERITS_FROM=1013I_R6C_CURRICULUM_STANDARD_CONTROL_LAYER_CONTRACT
NEXT_STAGE=1013I_R6E_OFFICIAL_UNIT_MATERIAL_READONLY_EXTRACTION_FIXTURE
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Purpose

R6D defines the contract relationship between `lesson_textbook_map`, `unit_package`, and `lesson_position_judgement`.

It connects R6C's curriculum-standard control layer to the concrete textbook anchor, the larger unit design chain, and the current lesson's role in that chain. It is contract-only and fixture-only: no big-unit body is generated and no single-lesson plan is generated.

## Required Textbook Anchor Fields

- `lesson_textbook_map_id`
- `textbook_version`
- `subject`
- `grade`
- `semester`
- `unit_id`
- `unit_title`
- `lesson_id`
- `lesson_code`
- `lesson_title`
- `lesson_count`
- `textbook_catalog_ref`
- `textbook_page_or_activity_ref`
- `material_or_image_anchor`
- `textbook_activity_hint`
- `source_material_refs`
- `anchor_status`
- `teacher_confirmation_status`

## Required Big Unit Chain Fields

- `unit_package_id`
- `unit_title`
- `unit_big_idea`
- `unit_essential_question`
- `unit_learning_goals`
- `unit_performance_task`
- `unit_task_chain`
- `unit_assessment_focus`
- `unit_learning_evidence_chain`
- `lesson_sequence`
- `source_material_refs`
- `chain_status`
- `teacher_confirmation_status`

## Required Lesson Position Fields

- `lesson_id`
- `lesson_title`
- `lesson_position_in_unit`
- `current_lesson_role`
- `prior_lesson_connection`
- `next_lesson_connection`
- `current_lesson_unit_task`
- `current_lesson_evidence`
- `allowed_candidate_scope`
- `blocked_candidate_scope`
- `teacher_confirmation_status`

## Generation Gate

```text
textbook_anchor_required=true
big_unit_design_chain_defined=true
lesson_position_judgement_required=true
teacher_confirm_unit_position_required=true
single_lesson_generation_blocked_without_textbook_anchor=true
single_lesson_generation_blocked_without_lesson_position=true
```

## Chain

```text
teacher_input
-> curriculum_standard_control_layer
-> textbook_anchor_check
-> big_unit_design_chain_check
-> lesson_position_judgement
-> teacher_confirm_unit_position
-> self_prep_review_cards
-> preview_only
```

## Non-Negotiable Rules

- `lesson_textbook_map` is the textbook semantic anchor, not an image path list.
- `unit_package` is the big-unit middle object, not the generated unit-design body.
- The current lesson must have a lesson-position judgement before normal candidate-card generation.
- Teacher confirmation is required before this lesson position can feed candidate cards.
- Missing textbook anchor or missing lesson position can only enter visible degraded draft mode.
- Official cases remain reference-only and cannot replace textbook anchors, unit chains, or teacher confirmation.
