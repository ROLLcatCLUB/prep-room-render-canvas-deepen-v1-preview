# 1013G PREP Candidate Review Sandbox

- FINAL_STATUS: `PASS_1013G_PREP_CANDIDATE_REVIEW_SANDBOX`
- NEXT_STAGE: `1013G_TEACHER_REVIEW_PREP_ONLY`
- Boundary: sandbox preview only; no formal 1013G, no apply, no HTML body modification, no database/memory/Feishu write.

## Decision

The approved R2D2 candidates were loaded into a teacher-review sandbox data surface. This stage previews candidate cards only. It does not confirm, apply, merge, or write lesson text.

## Preview Cards

- `1013g_prep_card_01` / 教学过程 · 探究
  - 原段落: 先用生活图片唤起感受，再通过色卡分类帮助学生建立冷暖体验，最后把感受转化为自己的色彩表达。
  - 候选调整: 探究先只发色卡和感受词卡。每组把色卡放到“温暖、清凉、安静、热烈”四个词旁边，再选一张最有把握的色卡说理由。已经能说出理由的小组，再领取一件生活物品做加料比较；记录单只写一行“我这样分是因为……”。
  - 风险提示: 如果生活物品过早进入，会重新挤压理由表达；因此只作为加料材料。
- `1013g_prep_card_02` / 教学过程 · 表现
  - 原段落: 学生围绕“我心中的一种感受”进行色彩小练习，自选基础、进阶或挑战任务，用颜色表达一种心情、天气、场景或小故事。
  - 候选调整: 表现环节先让全班完成同一个基础任务：用2到3种颜色表现一种感受。提前完成的学生再打开加层：可以加一个小场景，或补一句“我这样配色是因为……”。
  - 风险提示: 如果一开始展示三层标准，部分学生会先听复杂，反而晚开始。
- `1013g_prep_card_03` / 教学过程 · 交流展示
  - 原段落: 选择几件作品展示，学生用一句话说明自己的色彩选择，同伴说出自己读到的感受，教师归纳色彩和情绪表达的关系。
  - 候选调整: 交流展示固定两件作品：一件“颜色和感受关系清楚”，一件“还可以调整”。每件只问一个问题：“你从哪一种颜色读到了这种感觉？”教师最后只收束到颜色、感受和理由。
  - 风险提示: 如果时间不足，第二件改为教师指出可调整方向，不展开同伴讨论。

## Required Checks

- sandbox_preview_created=true
- approved_candidates_loaded=3
- candidate_preview_only=true
- lesson_body_modified=false
- html_body_modified=false
- teacher_review_required=true
- formal_apply_performed=false
- entered_1013G=false
- database_written=false
- memory_written=false
- feishu_written=false
- main_project_pushed=false

## Boundary

- Teacher action controls remain placeholders.
- Accept/apply buttons are not enabled in this data surface.
- A later decision stage must decide whether any candidate can enter real 1013G work.
