# 1013J_R1G_R2 Courseware Route Isolation Patch

FINAL_STATUS=PASS_1013J_R1G_R2_COURSEWARE_ROUTE_ISOLATION_PATCH
INHERITS_FROM=1013J_R1G_R1_COURSEWARE_RESPONSIVE_FULL_WIDTH_PATCH
NEXT_STAGE=USER_REVIEW_COURSEWARE_ROUTE_ISOLATION

R1G_R2 fixes route pollution where top-level navigation such as week calendar could render the courseware workspace after the courseware expanded state was set.

Fixes:
- courseware workspace renders only when active view is prep notebook
- non-prep views clear courseware expanded state
- non-courseware hash routes clear courseware expanded state
- week calendar and prep notebook routes remain independent

No runtime, provider/model, upload, search, whiteboard library, PPT export, drag edit, database, memory, Feishu, or formal apply is connected.

Failed checks: []
