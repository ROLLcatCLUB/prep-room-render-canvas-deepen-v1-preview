# GPT Review Prompt · 1013L R18

Please review the 1013L R18 teacher-test milestone package.

Check:

1. R16 mobile polish still reuses the existing page and does not create a new shell.
2. R16A closes the older R5 guards or records them as runtime guards.
3. R17 desktop teacher entries are usable: big-unit reading, courseware edit, classroom display preview.
4. Visible teacher copy uses 小教 for the current assistant surface; legacy 小备 only appears as customizable/hidden legacy profile data.
5. No runtime/provider/model/database/memory/Feishu/formal apply/main project push.

Recommended decision format:

```text
REVIEW_DECISION=ACCEPT / ACCEPT_WITH_FIX / HOLD
ACCEPTED_STAGE=1013L_R18_TEACHER_TEST_ENTRY_MILESTONE_PACKAGE
NEXT_STAGE=1013L_R19_TEACHER_MANUAL_TEST_FEEDBACK_INTAKE
FORMAL_FRONTEND_BINDING_ALLOWED=false
RUNTIME_CONNECTED=false
```
