# GPT Review Prompt - 1013L R10

Please review the 1013L R10 milestone package.

Focus:

1. Confirm the visible shell remains the existing 1013J_R1M polished prep-room page.
2. Confirm R7 maps original page interactions to readonly viewmodel states without replacing UI.
3. Confirm R8 creates only a hidden static readonly fetch hook.
4. Confirm R9 browser smoke resolves:
   - default -> single_lesson_design
   - week calendar -> week_calendar
   - prep notebook -> single_lesson_design
   - courseware expanded -> courseware_workspace
   - display preview -> classroom_display_preview
5. Confirm no runtime/provider/model/database/memory/Feishu/formal apply/main-project-push happened.

Required boundary fields:

```text
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

Expected decision if clean:

```text
REVIEW_DECISION=ACCEPT
ACCEPTED_STAGE=1013L_R10_EXISTING_PAGE_READONLY_VIEWMODEL_BINDING_MILESTONE_PACKAGE
FINAL_STATUS=PASS_1013L_R10_EXISTING_PAGE_READONLY_VIEWMODEL_BINDING_MILESTONE_PACKAGE
NEXT_STAGE=1013L_R11_EXISTING_PAGE_READONLY_VIEWMODEL_STATIC_HYDRATION_APPLY
FORMAL_FRONTEND_BINDING_ALLOWED=false
```
