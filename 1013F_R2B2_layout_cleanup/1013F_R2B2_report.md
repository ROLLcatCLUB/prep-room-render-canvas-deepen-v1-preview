# 1013F_R2B2 Layout Cleanup

```text
final_status=PASS_LAYOUT_CLEANUP
next_stage=1013F_R2C_CLASSROOM_EVENT_DETAIL_POLISH
edit_button_toggle_pass=true
inline_status_lights_pass=true
right_panel_brief_pass=true
main_body_direct_pass=true
```

## Summary

- Edit buttons now toggle the annotation bubble open and closed.
- Lesson status moved into the view/edit state row as colored lights plus text.
- The removed lesson-brief sentence is not rendered in the main body.
- Design judgement and read-lesson hint moved to the right auxiliary panel as collapsible content.
- The main reading area now enters the lesson body directly with a light text background.
- The edit bubble now starts near the right edge of the selected paragraph and expands over the right-side area.

## Boundary

- No provider/model call.
- No database write.
- No memory write.
- No Feishu write.
- No formal apply.
- No default entry change.
- Did not enter 1013G.
