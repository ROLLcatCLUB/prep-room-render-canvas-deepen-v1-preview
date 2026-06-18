# 1013I_R6H Big Unit Prep Page Fixture Review Before HTML

```text
STAGE=1013I_R6H_BIG_UNIT_PREP_PAGE_FIXTURE_REVIEW_BEFORE_HTML
FINAL_STATUS=PASS_1013I_R6H_BIG_UNIT_PREP_PAGE_FIXTURE_REVIEW_BEFORE_HTML
INHERITS_FROM=1013I_R6G_BIG_UNIT_PREP_PAGE_FIXTURE_AFTER_USER_APPROVAL
NEXT_STAGE=1013I_R6I_BIG_UNIT_PREP_HTML_FIXTURE_AFTER_REVIEW_APPROVAL
HTML_FIXTURE_ALLOWED_AFTER_REVIEW=true
HTML_BODY_MODIFIED=false
UI_IMPLEMENTATION_STARTED=false
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
```

## Review Result

```text
decision_first_layout_review_pass=true
teacher_action_semantics_review_pass=true
degraded_draft_label_review_pass=true
official_reference_notes_collapsed_review_pass=true
big_unit_timeline_not_full_unit_body=true
lesson_position_labels_teacher_readable=true
```

## HTML Fixture Constraints

- Confirmation-style actions must be visibly marked as preview-only, not formal confirmation.
- Degraded single-lesson draft must show a visible degraded label.
- Official reference notes remain collapsed by default.
- Big-unit chain remains a light timeline, not full unit-design body.
- HTML fixture may render static JSON state only; it must not introduce runtime writes.
