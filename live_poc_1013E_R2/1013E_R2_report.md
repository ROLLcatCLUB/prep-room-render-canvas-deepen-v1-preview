# 1013E_R2 Standard Daily Prompt Repair

```text
final_status=STANDARD_DAILY_REPAIR_FAILED
next_stage=1013E_R3_PROMPT_REPAIR_OR_MODEL_STRATEGY_ADJUSTMENT
strict_json_success=false
validation_error_count=26
secret_scan_ok=true
```

## Case

- mode: `standard_daily`
- input: 学生对冷暖色不太理解，要设计得更直观一点。

## Boundary

- Provider called once for this repair run.
- No database write.
- No memory write.
- No Feishu write.
- No formal apply.
- No formal export or archive.
- Request and response are redacted.

## Validation Errors

- `target_0_not_object`
- `target_1_not_object`
- `patch_0_missing_target`
- `patch_0_missing_target_field`
- `patch_0_teacher_review_required_not_true`
- `patch_0_formal_apply_not_false`
- `patch_1_missing_target`
- `patch_1_missing_target_field`
- `patch_1_teacher_review_required_not_true`
- `patch_1_formal_apply_not_false`
- `step_reasoning_updates_missing_student_state_before`
- `step_reasoning_updates_missing_student_state_after`
- `impact_0_affected_object_invalid`
- `impact_0_missing_summary`
- `impact_0_confirmation_not_true`
- `impact_1_affected_object_invalid`
- `impact_1_missing_summary`
- `impact_1_confirmation_not_true`
- `impact_2_affected_object_invalid`
- `impact_2_missing_summary`
- `impact_2_confirmation_not_true`
- `missing_impact_big_screen`
- `missing_impact_handout`
- `missing_impact_evidence_note`
- `missing_analysis_patch`
- `missing_explore_patch`
