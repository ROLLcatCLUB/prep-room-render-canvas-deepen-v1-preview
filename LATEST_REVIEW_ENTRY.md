# Latest Review Entry

```text
REVIEW_STAGE=1013I_R6L_TEACHER_ACTION_GUIDANCE_COPY_PATCH_FOR_BIG_UNIT_STATIC_INTEGRATION
FINAL_STATUS=PASS_1013I_R6L_TEACHER_ACTION_GUIDANCE_COPY_PATCH_FOR_BIG_UNIT_STATIC_INTEGRATION
LATEST_COMPLETED_ORIGINAL_PAGE_STATIC_INTEGRATION=1013I_R6K_BIG_UNIT_PREP_ORIGINAL_PAGE_STATIC_INTEGRATION_RUN
LATEST_COMPLETED_TEACHER_GUIDANCE_COPY_PATCH=1013I_R6L_TEACHER_ACTION_GUIDANCE_COPY_PATCH_FOR_BIG_UNIT_STATIC_INTEGRATION
USER_REVIEW_DECISION=REQUEST_TEACHER_ACTION_GUIDANCE_COPY_PATCH
INHERITS_FROM=1013I_R6K_BIG_UNIT_PREP_ORIGINAL_PAGE_STATIC_INTEGRATION_RUN
NEXT_RECOMMENDED_STAGE=1013I_R6M_BIG_UNIT_STATIC_INTEGRATION_USER_REVIEW_OR_RUNTIME_HOLD
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
TEACHER_ACTION_GUIDANCE_SURFACE_CREATED=true
ENGINEERING_FIELD_PRIMARY_SURFACE_HITS=[]
RAW_FIELD_KEYS_ONLY_IN_COLLAPSED_REFERENCE=true
MISSING_DATA_EXPRESSED_AS_TEACHER_ACTIONS=true
UPLOAD_MATERIAL_ENTRY_PRESENT=true
PASTE_UNIT_GOAL_ENTRY_PRESENT=true
TEMPORARY_PREVIEW_ENTRY_PRESENT=true
BIG_UNIT_ENTRY_POSITION_KEPT=true
SINGLE_LESSON_ENTRIES_KEPT=true
RUNTIME_CONNECTED=false
UI_IMPLEMENTATION_STARTED=false
HTML_UI_IMPLEMENTATION_ALLOWED=false
MAIN_HTML_BODY_MODIFIED=false
```

## Summary

R6L patches the R6K original-page static integration copy. The insertion position stays the same: unit titles in the prep notebook directory, such as `第一单元 多变的色彩`, remain the big-unit entry, and `1-1 / 1-2 / 1-3` remain single-lesson entries.

The patch changes the teacher-visible main surface from engineering diagnostics into action guidance:

```text
先确认这节课站在哪
小教的临时判断
你现在只需要确认三件事
需要你补充的资料
确认后会发生什么
```

The main reading area no longer exposes raw field keys such as `textbook_anchor_candidate`, `big_unit_chain_candidate`, `lesson_position_candidate`, or `teacher_confirmation_required`. Those keys are retained only in the right-side collapsed readonly reference area for audit traceability.

R6L remains static preview only. It does not connect runtime, call a provider/model, generate a formal big-unit design, write a lesson body, write database/memory/Feishu, export/archive officially, or push the main project tree.

## Start Here

```text
README.md
REVIEW_PACKAGE_MANIFEST.md
1013I_R6L_teacher_action_guidance_copy_patch_for_big_unit_static_integration/1013I_R6L_report.md
1013I_R6L_teacher_action_guidance_copy_patch_for_big_unit_static_integration/1013I_R6L_result.json
1013I_R6L_teacher_action_guidance_copy_patch_for_big_unit_static_integration/prep_room_render_canvas_deepen_v1_R6L_teacher_guidance_patch.html
1013I_R6L_teacher_action_guidance_copy_patch_for_big_unit_static_integration/ui_smoke_screenshot_1013I_R6L_desktop.png
1013I_R6L_teacher_action_guidance_copy_patch_for_big_unit_static_integration/ui_smoke_screenshot_1013I_R6L_mobile.png
scripts/validate_1013I_R6L_teacher_action_guidance_copy_patch_for_big_unit_static_integration.py
```
