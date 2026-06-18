# 1013G Teacher Review Prep Only

- FINAL_STATUS: `PASS_1013G_TEACHER_REVIEW_PREP_ONLY`
- NEXT_STAGE: `1013H_SANDBOX_APPLY_TO_PREVIEW_ONLY`
- Boundary: teacher-review preparation only; no formal 1013G, no formal apply, no lesson body write.

## Decision

This stage turns sandbox candidate cards into teacher-review preparation cards. The teacher actions are prepared as options only: accept to preview, reject, or revise. Accept to preview still means sandbox/preview state only.

## Review Cards

- `1013g_teacher_review_prep_card_01` / 教学过程 · 探究
  - current: 先用生活图片唤起感受，再通过色卡分类帮助学生建立冷暖体验，最后把感受转化为自己的色彩表达。
  - suggested: 探究先只发色卡和感受词卡。每组把色卡放到“温暖、清凉、安静、热烈”四个词旁边，再选一张最有把握的色卡说理由。已经能说出理由的小组，再领取一件生活物品做加料比较；记录单只写一行“我这样分是因为……”。
  - actions: accept_to_preview_only, reject, revise
- `1013g_teacher_review_prep_card_02` / 教学过程 · 表现
  - current: 学生围绕“我心中的一种感受”进行色彩小练习，自选基础、进阶或挑战任务，用颜色表达一种心情、天气、场景或小故事。
  - suggested: 表现环节先让全班完成同一个基础任务：用2到3种颜色表现一种感受。提前完成的学生再打开加层：可以加一个小场景，或补一句“我这样配色是因为……”。
  - actions: accept_to_preview_only, reject, revise
- `1013g_teacher_review_prep_card_03` / 教学过程 · 交流展示
  - current: 选择几件作品展示，学生用一句话说明自己的色彩选择，同伴说出自己读到的感受，教师归纳色彩和情绪表达的关系。
  - suggested: 交流展示固定两件作品：一件“颜色和感受关系清楚”，一件“还可以调整”。每件只问一个问题：“你从哪一种颜色读到了这种感觉？”教师最后只收束到颜色、感受和理由。
  - actions: accept_to_preview_only, reject, revise

## Required Checks

- teacher_review_prep_surface_created=true
- candidate_cards_loaded=3
- teacher_action_options_present=true
- accept_to_preview_only=true
- reject_option_present=true
- revise_option_present=true
- formal_apply_performed=false
- entered_formal_1013G=false
- lesson_body_modified=false
- html_body_modified=false
- database_written=false
- memory_written=false
- feishu_written=false
- main_project_pushed=false
