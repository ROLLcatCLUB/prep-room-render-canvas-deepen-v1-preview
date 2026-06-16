# GPT Review Prompt

You are reviewing a static preview package for Shiwei prep room.

## Review Goal

Please review whether the current preview can serve as the next reference package for:

- `师维 = 学校里的 AI 工作社区`
- `备课室 = current working space`
- `备课本 = 本学期过程性工作本`
- `周课表 = 本周课前执行视图`
- `班级排课 = week-by-class progress and schedule board`
- `学期规划 = semester unit and week planning view`

## Entry Files

Start from:

- `README.md`
- `prep_room_render_canvas_deepen_v1.html`
- `teaching_plan_source_2025_second_term_g3_art_v0.md`
- `feishu_api_connection_inventory_v0.md`
- `feishu_business_data_relevance_inventory_v0.md`
- `prep_notebook_design_v0.md`
- `prep_notebook_right_drawer_source_inventory_v0.md`

Then review the supporting board docs:

- `week_calendar_board_design_v0.md`
- `class_progress_schedule_board_design_v0.md`
- `class_progress_schedule_board_v1.html`
- `shiwei_concept_archive_v0.md`
- `prep_notebook_topic_source_alignment_v0.md`

## Review Questions

1. Is the space-shell principle clear enough?
   - Top and bottom are persistent shell.
   - Center is RenderStage.
   - `备课室 · 当前看板` tells the teacher where they are.
   - Bottom intent bar defaults to `小备`.

2. Is `备课本` correctly separated from `资料室` and `档案室`?
   - `资料室 = 备用资源`
   - `备课本 = 正在用`
   - `档案室 = 用完留下`

3. Does the prep notebook feel like a binder/workbook instead of a normal dashboard?
   - Deep green cover only wraps left notebook directory and center lesson page.
   - Right resource drawer is outside the notebook.
   - Binder rings/pins are intentionally not rendered.

4. Are the teaching topics grounded in the local teaching work plan?
   - Source: `2025学年第二学期三年级美术教学工作计划.docx`
   - Extracted into `teaching_plan_source_2025_second_term_g3_art_v0.md`
   - Avoid temporary GPT-made topic names.

5. Is the Feishu boundary safe and useful?
   - Frontend never reads Feishu secrets.
   - Backend direct connection only.
   - Current review package uses local full-dump findings, not live API calls.
   - Do not request or expose `APP_SECRET`.

6. Is the next integration route reasonable?
   - Use Feishu schedule snapshot to populate `周课表`.
   - Use teaching work plan as first-priority planning source.
   - Later add backend readonly Feishu adapter before real live sync.

## Please Output

Return a concise review with:

- `decision`
- `status`
- `what_passes`
- `blocking_issues`
- `recommended_next_stage`
- `do_not_do_yet`

