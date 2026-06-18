# Latest Review Entry

```text
REVIEW_STAGE=1013I_R6M_BIG_UNIT_DESIGN_TEACHER_READABLE_STATIC_PATCH_FOR_REVIEW
FINAL_STATUS=PASS_1013I_R6M_BIG_UNIT_DESIGN_TEACHER_READABLE_STATIC_PATCH_FOR_REVIEW
LATEST_COMPLETED_TEACHER_GUIDANCE_COPY_PATCH=1013I_R6L_TEACHER_ACTION_GUIDANCE_COPY_PATCH_FOR_BIG_UNIT_STATIC_INTEGRATION
LATEST_COMPLETED_BIG_UNIT_DESIGN_STATIC_PATCH=1013I_R6M_BIG_UNIT_DESIGN_TEACHER_READABLE_STATIC_PATCH_FOR_REVIEW
INHERITS_FROM=1013I_R6L_TEACHER_ACTION_GUIDANCE_COPY_PATCH_FOR_BIG_UNIT_STATIC_INTEGRATION
NEXT_RECOMMENDED_STAGE=USER_REVIEW_BIG_UNIT_DESIGN_PAGE
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
HTML_FIXTURE_CREATED=true
BIG_UNIT_DESIGN_PAGE_CREATED=true
TEACHER_READABLE_LABELS_FIRST=true
PAGE_DESIGN_BEFORE_SCHEMA=true
ENGINEERING_FIELDS_NOT_PRIMARY_SURFACE=true
MAIN_SURFACE_RAW_ENGINEERING_FIELD_HITS=[]
MATERIAL_UPLOAD_ACTIONS_PRESENT=true
PREVIEW_ONLY_BADGES_VISIBLE=true
RUNTIME_CONNECTED=false
UI_IMPLEMENTATION_STARTED=false
HTML_MODIFIED=false
```

## Summary

R6M corrects the product semantics. R6K/R6L proved the entry position: unit titles in the prep notebook directory are the big-unit entry, and lesson rows remain single-lesson entries. R6M changes the main surface from a single-lesson preflight confirmation page into a teacher-readable big-unit design page.

The main page now uses five teacher-facing sections:

```text
这个单元想带学生走向哪里
学生现在在哪里
学生最后要完成什么
单元怎么一步步推进
老师需要准备哪些支架
```

Raw engineering field keys are not used as the primary surface. They are retained in the right-side collapsed readonly reference area and in the mapping JSON.

## Start Here

```text
README.md
REVIEW_PACKAGE_MANIFEST.md
1013I_R6M_big_unit_design_teacher_readable_static_patch_for_review/1013I_R6M_report.md
1013I_R6M_big_unit_design_teacher_readable_static_patch_for_review/1013I_R6M_result.json
1013I_R6M_big_unit_design_teacher_readable_static_patch_for_review/prep_room_render_canvas_deepen_v1_R6M_big_unit_design_teacher_readable_static.html
1013I_R6M_big_unit_design_teacher_readable_static_patch_for_review/ui_smoke_screenshot_1013I_R6M_desktop.png
1013I_R6M_big_unit_design_teacher_readable_static_patch_for_review/ui_smoke_screenshot_1013I_R6M_mobile.png
scripts/validate_1013I_R6M_big_unit_design_teacher_readable_static_patch_for_review.py
```
