# 1013K_R2 Curriculum Profile To Big Unit Candidate Envelope Report

STAGE=1013K_R2_CURRICULUM_PROFILE_TO_BIG_UNIT_CANDIDATE_ENVELOPE
FINAL_STATUS=PASS_1013K_R2_CURRICULUM_PROFILE_TO_BIG_UNIT_CANDIDATE_ENVELOPE
INHERITS_FROM=1013K_R1_CURRICULUM_DERIVATION_PROFILE_RUNTIME_DRY_RUN
NEXT_STAGE=1013K_R3_BIG_UNIT_CANDIDATE_ENVELOPE_TO_STATIC_SECTION_PREVIEW
GITHUB_UPLOAD_DEFERRED_UNTIL_MILESTONE=true

## Scope

R2 converts the R1 curriculum control profile and target map into big-unit candidate generation envelopes. It does not generate candidate text, does not call a provider/model, and does not write unit_package, lesson body, database, memory, or Feishu.

## Key Checks

```text
envelope_count=10
normal_candidate_generation_allowed=false
degraded_preview_allowed=true
all_envelopes_teacher_review_required=true
all_envelopes_candidate_text_not_generated=true
provider_called=false
model_called=false
database_written=false
memory_written=false
formal_apply_performed=false
```

## Validator

validator_pass=true
failed_checks=[]
