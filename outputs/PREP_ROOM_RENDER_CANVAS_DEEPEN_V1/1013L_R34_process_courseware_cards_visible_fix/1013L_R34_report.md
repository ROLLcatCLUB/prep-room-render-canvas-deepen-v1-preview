# 1013L R34 · Process Courseware Cards Visible Fix

## Status

`PASS_1013L_R34_PROCESS_COURSEWARE_CARDS_VISIBLE_FIX`

R34 fixes the issue where teaching-process courseware cards were still invisible because earlier cleanup rules target `.courseware-section-rail` and old marker attributes. The restored process cards now use a new class that is not caught by the old cleanup selectors and are restored after page rerenders.

## Boundary

No runtime/provider/model/database/memory/Feishu/upload/search/material library/whiteboard library/formal apply/main push/GitHub upload.
