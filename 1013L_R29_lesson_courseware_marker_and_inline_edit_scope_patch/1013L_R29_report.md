# 1013L R29 · Marker Scope And Inline Edit Patch

## Status

`PASS_1013L_R29_LESSON_COURSEWARE_MARKER_AND_INLINE_EDIT_SCOPE_PATCH`

This patch keeps the existing R28 page line and corrects interaction scope:

- removes courseware markers from non-teaching-process sections such as 本课依据 / 学情分析;
- removes the big group of courseware cards directly under 教学过程;
- keeps courseware hints only in concrete teaching-process steps;
- marker clicks focus the right-side 大屏草稿 instead of opening a switch popover;
- paragraph edit opens an inline popover aligned to the clicked row;
- big-unit section edit reuses the same aligned popover behavior.

## Boundary

No runtime/provider/model/database/memory/Feishu/upload/search/whiteboard library/formal apply/main push/GitHub upload.
