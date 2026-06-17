# 1013F Reasoning Field Patch To View/Edit UI Binding

```text
final_status=PASS_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING
next_stage=1013G_TEACHER_REVIEW_ACTIONS_PREVIEW_SANDBOX
view_mode_binding_pass=true
edit_mode_binding_pass=true
patch_candidate_card_pass=true
impact_scope_mapping_pass=true
screenshot_smoke_pass=true
edit_screenshot_smoke_pass=true
```

## Summary

- R4 staged lesson derivation is bound to teacher-readable view mode and edit mode samples.
- The binding shows judgement, suggested target, impact scope, and teacher review actions.
- The HTML preview uses a preview-only `#prepNotebook1013F` / `#prepNotebook1013FEdit` state and does not change the default entry.

## Boundary

- No provider/model call.
- No database write.
- No memory write.
- No Feishu write.
- No formal apply.
- No official export/archive.
- No raw model output is sent to frontend.
