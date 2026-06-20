# 1013K_R0 Curriculum Standard Derivation Backend Contract Report

STAGE=1013K_R0_CURRICULUM_STANDARD_DERIVATION_BACKEND_CONTRACT
FINAL_STATUS=PASS_1013K_R0_CURRICULUM_STANDARD_DERIVATION_BACKEND_CONTRACT
NEXT_STAGE=1013K_R1_CURRICULUM_DERIVATION_PROFILE_RUNTIME_DRY_RUN

## Scope

This stage defines the backend contract for deriving prep-room candidates from curriculum-standard control. It creates structured slice/profile schemas, a derivation contract, and a trace fixture.

## Key Checks

```text
curriculum_standard_as_control_layer=true
full_standard_text_not_dumped_to_prompt=true
textbook_anchor_required=true
big_unit_design_chain_required=true
official_case_reference_only=true
big_unit_derivation_before_single_lesson=true
teacher_confirmation_required=true
provider_called=false
model_called=false
database_written=false
memory_written=false
formal_apply_performed=false
```

## Boundary

1013K_R0 is backend-contract-only and fixture-only. It does not parse real curriculum-standard full text, does not call provider/model, does not apply runtime schema, does not write database/memory/Feishu, and does not modify lesson body or HTML.

## Validator

validator_pass=true
failed_checks=[]
