# 1013K_R0 Curriculum Standard Derivation Backend Contract

STAGE=1013K_R0_CURRICULUM_STANDARD_DERIVATION_BACKEND_CONTRACT
FINAL_STATUS=PASS_1013K_R0_CURRICULUM_STANDARD_DERIVATION_BACKEND_CONTRACT
INHERITS_FROM=1013I_R6C_CURRICULUM_STANDARD_CONTROL_LAYER_CONTRACT + 1013I_R6D_TEXTBOOK_ANCHOR_AND_BIG_UNIT_DESIGN_CHAIN_CONTRACT + 1013I_R6E_OFFICIAL_UNIT_MATERIAL_READONLY_EXTRACTION_FIXTURE
NEXT_STAGE=1013K_R1_CURRICULUM_DERIVATION_PROFILE_RUNTIME_DRY_RUN

## Purpose

1013K_R0 defines the backend derivation contract for starting prep-room reasoning from the curriculum-standard control layer. It does not generate a lesson body, does not apply a runtime schema, and does not call a provider/model.

## Reasoning Chain

`teacher_input -> curriculum_standard_slice_selection -> curriculum_control_profile -> textbook_anchor_check -> big_unit_chain_check -> lesson_position_judgement -> teacher_confirmation -> candidate_generation_preview_only`

## Derivation Targets

- `curriculum_basis`
- `core_literacy_goals`
- `student_starting_point`
- `unit_questions`
- `knowledge_and_skills`
- `performance_task`
- `learning_progression`
- `lesson_task_chain`
- `assessment_evidence`
- `materials_and_scaffolds`

## Blocked Before Teacher Confirmation

- `formal_unit_package`
- `formal_single_lesson_body`
- `database_record`
- `memory_record`
- `feishu_writeback`
- `official_export`

## Boundary

```text
curriculum_standard_as_control_layer=true
full_standard_text_not_dumped_to_prompt=true
textbook_anchor_required=true
official_case_reference_only=true
big_unit_derivation_before_single_lesson=true
teacher_confirmation_required=true
provider_called=false
model_called=false
database_written=false
memory_written=false
formal_apply_performed=false
```
