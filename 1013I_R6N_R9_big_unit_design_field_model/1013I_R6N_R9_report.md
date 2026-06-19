# 1013I_R6N_R9 Big Unit Design Field Model

FINAL_STATUS=PASS_1013I_R6N_R9_BIG_UNIT_DESIGN_FIELD_MODEL
INHERITS_FROM=1013I_R6N_R8_BIG_UNIT_DESIGN_RESTYLED_AS_LESSON_NOTEBOOK_UI
NEXT_STAGE=USER_REVIEW_BIG_UNIT_FIELD_MODEL_BEFORE_RUNTIME_SCHEMA

This stage archives the teacher-visible big-unit field model, backend mapping candidates, and reuse/integration matrix.

Key decisions:
- Reuse R6D `unit_package` as the candidate backend container.
- Reuse R6E official field dictionary and extraction fixtures as readonly source candidates.
- Reuse R6C curriculum-standard control layer as upstream constraint.
- Keep the `1-2 色彩的感觉` single-lesson page paused for UI changes, but use it as the inheritance target reference.
- Do not apply runtime schema, database writes, memory writes, Feishu writes, provider/model calls, or formal apply.

Validation: PASS_1013I_R6N_R9_BIG_UNIT_DESIGN_FIELD_MODEL
Failed checks: []
