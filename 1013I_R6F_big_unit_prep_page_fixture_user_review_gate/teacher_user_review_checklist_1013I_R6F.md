# 1013I_R6F Teacher User Review Checklist

```text
STAGE=1013I_R6F_BIG_UNIT_PREP_PAGE_FIXTURE_USER_REVIEW_GATE
STATUS=pending_user_review
PAGE_WORK_STARTED=false
UI_IMPLEMENTATION_STARTED=false
NEXT_STAGE_AFTER_APPROVAL=1013I_R6G_BIG_UNIT_PREP_PAGE_FIXTURE_AFTER_USER_APPROVAL
```

## 请先看这些问题

1. 第一屏是否应该先让老师看到“为什么不能直接生成单课”？
2. 教材锚点候选、单元链候选、本课位置候选，三者的优先顺序是否合理？
3. 大单元推进链是否应该放左侧，还是放在主区域上方？
4. 教师确认项是否太多，是否需要分成“必须确认 / 可以稍后补”？
5. 只读官方字段依据是否默认折叠，避免压过教师自己的判断？
6. 是否允许老师选择“先临时按单课草稿继续”，并明确标记为降级模式？

## 当前不做

- 不写 HTML 页面。
- 不做视觉实现。
- 不生成大单元正文。
- 不生成单课教案。
- 不调用 provider/model。
- 不写 database/memory/Feishu。
