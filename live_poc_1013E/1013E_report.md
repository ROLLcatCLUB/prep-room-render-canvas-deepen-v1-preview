# 1013E Model Prompt To Reasoning Field Patch POC

```text
final_status=FAIL_MODEL_OUTPUT_NOT_STABLE
next_stage=1013E_R1_PROMPT_REPAIR
strict_json_success_count=1
safe_success_count=1
cases_with_lesson_design_brief=1
cases_with_field_patch_candidates=1
cases_with_teaching_step_reasoning_updates=1
targetable_patch_count=1
boundary_ok=true
secret_scan_ok=true
```

## Boundary

- No database write.
- No memory write.
- No Feishu write.
- No formal apply.
- No official export.
- No official archive.
- Provider requests and responses are redacted.

## Test Cases

- `test_1_quick_daily` `quick_daily`: PASS; parser=strict_json; errors=0
- `test_2_standard_daily` `standard_daily`: FAIL; parser=json_parse_failed; errors=1
- `test_3_open_class` `open_class`: FAIL; parser=provider_error; errors=1
- `test_4_research_lesson` `research_lesson`: FAIL; parser=provider_error; errors=1

## Impact Objects

big_screen, evidence_note, handout

## Quality Gate Levels

basic_usable
