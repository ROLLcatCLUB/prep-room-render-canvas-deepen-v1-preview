# GPT Review Prompt - 1013L R15

Please review the 1013L R15 milestone package.

Focus:

1. Confirm the visible shell remains the existing polished prep-room page, not a newly invented shell.
2. Confirm courseware ViewModel hydration uses the existing courseware list/workspace/display preview surfaces.
3. Confirm big-unit ViewModel hydration uses the existing big-unit entry and reading surface.
4. Confirm desktop screenshots are valid review evidence.
5. Confirm mobile layout remains a hold item and does not allow formal frontend binding.
6. Confirm boundary flags remain clean.

Expected decision if clean:

```text
REVIEW_DECISION=ACCEPT_AS_EXISTING_PAGE_HYDRATION_MILESTONE
ACCEPTED_STAGE=1013L_R15_EXISTING_PAGE_HYDRATION_MILESTONE_PACKAGE
FINAL_STATUS=PASS_1013L_R15_EXISTING_PAGE_HYDRATION_MILESTONE_PACKAGE
NEXT_STAGE=1013L_R16_EXISTING_PAGE_MOBILE_LAYOUT_POLISH_AND_TEACHER_TEST_ENTRY
FORMAL_FRONTEND_BINDING_ALLOWED=false
MOBILE_LAYOUT_POLISH_REQUIRED=true
```

Machine flags to preserve:

```text
formal_frontend_binding_allowed=false
mobile_layout_polish_required=true
runtime_connected=false
real_fetch_performed=false
provider_called=false
model_called=false
database_written=false
memory_written=false
feishu_written=false
formal_apply_performed=false
main_project_pushed=false
```
