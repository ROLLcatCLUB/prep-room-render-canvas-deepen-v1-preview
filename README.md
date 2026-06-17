# PREP_ROOM_RENDER_CANVAS_DEEPEN_V1

This package turns the v5 prep-room static preview into a render-canvas preview.

## Files

- `prep_room_render_canvas_deepen_v1.html`
- `GPT_REVIEW_PROMPT.md`
- `REVIEW_PACKAGE_MANIFEST.md`
- `SESSION_HANDOFF_20260616_PREP_ROOM_RENDER_CANVAS.md`
- `shiwei_concept_archive_v0.md`
- `prep_notebook_design_v0.md`
- `prep_notebook_right_drawer_source_inventory_v0.md`
- `prep_notebook_topic_source_alignment_v0.md`
- `teaching_plan_source_2025_second_term_g3_art_v0.md`
- `feishu_api_connection_inventory_v0.md`
- `feishu_business_data_relevance_inventory_v0.md`
- `week_calendar_board_design_v0.md`
- `class_progress_schedule_board_design_v0.md`
- `class_progress_schedule_board_v1.html`

## Preview Boundary

- Static fixture only.
- No API call.
- No model/provider call.
- No database, memory, Feishu, export, or formal apply.
- Teacher review is required for every pending change.

## Reused Project Patterns

- `frontend/home.html`: scene-level ViewModel plus renderer function split.
- `frontend/xiaojiao-preview.html`: work state to render directive to surface renderer idea.
- `docs/foundation/xiaojiao_dynamic_work_panel_contract_1000C.md`: dynamic panel / inspector contract direction.
- `docs/foundation/xiaojiao_core_pack_to_preview_surface_contract_1012C.md`: render directive safety shape.
- `backend/xiaobei_ai/workbench_preview_viewmodel_builder_071B.py`: preview safety flags and teacher-review boundary.

## Canvas Shape

```text
ShiweiShell
├─ TopSpaceNav
├─ RenderStage
└─ BottomIntentBar

Current space = prep_room
Current bottom agent = xiaobei_prep_assistant

PrepRoomWorkState
-> composePrepRoomRenderDirective()
-> window.PREP_ROOM_RENDER_VIEW_MODEL
-> RenderStage renders PrepRoomCanvas
```

Current V1 keeps the composer implicit inside the static fixture and exposes the renderer functions on `window` for later adapter work.

## Visual Repair Notes

- View switching now uses a lightweight fade transition on the render layer.
- Week package cards show one primary gap plus two priority actions; secondary collaboration actions move to the floating inspector.
- The former month-progress view has been removed from the prep-room RenderStage.
- The AI tool rail is horizontal and icon-only, with tool names kept in hover titles and accessible labels.
- The bottom status area uses a global flow step bar for `备课室 -> 教室 -> 作品馆 -> 档案室 -> 回流`.
- The top area now uses a compact product navigation bar and context row; view switching lives in the context row, while the verbose canvas heading block has been removed.
- The current space name is centered as large gradient text, with a horizontal AI tool strip below it using one icon per tool.
- The centered context title now shows the active board after the space name, for example `备课室 · 周课表`, `备课室 · 班级排课`, or `备课室 · 学期规划`.
- The bottom intent bar belongs to the prep-room space and defaults to `小备`; `小教` and `小管` may still appear as specialist collaborators inside weekly schedule, class progress, and timetable-adjustment panels.
- `shiwei_concept_archive_v0.md` records the current concept boundary: `备课本 = 本学期过程性工作本`, `资料室 = 备用资源`, `档案室 = 用完留下的证据`.
- The first view is now `周课表 / 本周课前看板`, replacing the former week-package card view. It renders a Monday-to-Sunday timetable for class, topic, package status, activities, holidays, reschedules, and makeup lessons.
- `备课本` is now integrated directly after `周课表`, with a link button inside the week-calendar control strip. It renders the V0 structure: left semester/unit/lesson directory, center lesson work page, right drawer for 小备建议 / 可调用资料 / 待沉淀内容.
- The prep notebook visual now uses a binder-cover feel: deep green cover background, paper texture, left notebook directory, a gray-green center expansion layer, and a right drawer stack. Binder rings/pins are intentionally not rendered in this pass.
- The binder cover only wraps the left notebook directory and center lesson page; the right resource drawer sits outside the notebook as a separate resource rail.
- `prep_notebook_right_drawer_source_inventory_v0.md` records source-system prep materials and field ideas for redesigning the right prep drawer around 小备建议, 本课材料夹, 可调用资料, 教师审核门, and 待沉淀入口.
- `teaching_plan_source_2025_second_term_g3_art_v0.md` extracts the local Word teaching work plan into a page-ready planning source: 7 textbook units, 4 Creative Arts Festival lessons, 6 flexible/review lessons, and the 16-week progress table.
- The current page uses that Word teaching work plan as the first-priority planning source. `学期规划`, `备课本`, `周课表`, and `班级排课` now share the same 2025 second-term Grade 3 art unit chain instead of temporary GPT topic names.
- `feishu_api_connection_inventory_v0.md` records local Feishu connection findings: the usable full-dump snapshot, the `教师课表` table, Xu Tao's Grade 3 art schedule rows, the existing OpenAPI request pattern, and the current no-token/no-write boundary.
- `feishu_business_data_relevance_inventory_v0.md` records how Feishu tables map into Shiwei spaces: prep room, classroom, gallery, archive room, resource room, routine records, assignments, evaluations, energy, and term profiles.
- The third view is now `班级排课 / 班级进度与排课`, rendered as a week-by-class board with two default weekly lesson slots per class.
- V1.1 readability polish strengthens the current-week marker, keeps future lessons readable while muted, adds a compact status legend, removes the visible slot-label chips, and lets the dense class-by-week board expand horizontally.
- The class schedule control strip now places compact metric pills directly after the grade switcher; metric labels are kept as hover titles, while the visible surface only shows icon plus value such as `5`, `3`, `4`, or `第8周`.
- The fourth view remains `学期规划`, rendered as a left unit lesson catalog plus a right weekly lesson plan board.
- `class_progress_schedule_board_v1.html` is retained as the accepted standalone reference preview for the integrated `班级进度与排课` scene.
- The page now follows the shell principle: spaces are states rendered in the center stage, and agents are bottom intent-bar roles rather than room-internal page widgets.
- Visual rule update: week indicators should be prominent, while actions use pill or circular button shapes by default.
- Icon rule update: use a Lucide-like line icon style for circular controls; keep action text in `title` / accessible labels instead of visible button copy.
- Inspector rule update: the floating inspector stays hidden on initial render and opens near the pointer after a node/action click.

## 1013A Feishu Schedule And Prep Field POC

- `backend/xiaobei_ai/prep_room_feishu_schedule_1013A.py` adds a read-only prep-room schedule adapter at `/api/xiaobei/prep-room/schedule`.
- The adapter reads live Feishu only when formal env credentials are present; otherwise it falls back to the local full-dump snapshot for `教师课表`.
- The preview page now binds the week calendar to Xu Tao's Grade 3 art schedule rows and opens the prep notebook on 1-2 `色彩的感觉`.
- The prep notebook center area is the main prep canvas: field candidates, teacher confirmation, resource references, and archive candidates stay in preview state.
- `scripts/run_prep_room_1013a_feishu_schedule_and_live_poc.py` runs the limited MiniMax field-patch POC and writes outputs under `outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/live_poc/`.
- Boundary: no Feishu write, no database write, no memory write, no formal apply, no formal export, and no frontend secret exposure.

## 1013C Prep Notebook View/Edit And Teaching Process Plan

- `prep_notebook_1013C_view_edit_teaching_process_design_plan.md` records the next-stage redesign plan for the prep notebook.
- Core direction: default `查看状态` reads like a continuous lesson design; `编辑状态` appears only when the teacher edits a section, step, or candidate.
- The teaching process becomes the key design layer: every lesson step carries its role, intent, transition, student state, teacher action, screen/material state, evidence, and adjustment plan.
- Market scan summary: absorb tool granularity, post-draft revision workflow, teacher-controlled AI, classroom evidence, and platform-chain awareness from current AI lesson-prep products; do not copy their tool-menu shape.
- Boundary: 1013C remains preview/design implementation only; no provider call, Feishu write, database write, memory write, formal apply, or formal export.

## 1013C Local Implementation

- `prep_room_render_canvas_deepen_v1.html#prepNotebook` now opens the prep notebook in `查看状态`: a continuous lesson design for real topic 1-2 `色彩的感觉`.
- `prep_room_render_canvas_deepen_v1.html#prepNotebookEdit` opens `编辑状态`, focused on `教学过程 · 探究环节`.
- `prep_room_render_canvas_deepen_v1.html#prepNotebookIntent` opens the teaching-process intent layer with the `探究` design explanation expanded.
- The visible teacher UI avoids engineering words and keeps edit tools around the current section or lesson step.
- No large review package, ZIP, formal validator, provider call, database write, memory write, Feishu write, formal apply, or formal export was added in this implementation pass.

## 1013D Lesson Design Reasoning Field Model

- `lesson_design_reasoning_model_1013D.md` defines the next model layer: a lesson is a learning-problem solving chain, not a fixed set of process labels.
- `lesson_design_reasoning_model_1013D.json` defines the field model for `lesson_design_mode`, `lesson_design_brief`, teaching-step reasoning, visible-surface rules, and hard no-write boundaries.
- `lesson_design_brief_sample_1013D.json` gives the full sample for Grade 3 art, Unit 1, 1-2 `色彩的感觉`, with `standard_daily` as the sample preparation depth.
- `teaching_step_reasoning_sample_1013D.json` gives five reasoning objects for 导入, 感知, 探究, 表现, and 交流展示.
- `lesson_design_quality_gate_1013D.json` defines the quality gate dimensions: alignment, student baseline, target shift, route coherence, teacher/student actions, big screen, material timing, evidence, risk adjustment, not-too-easy, and not-over-scope.
- `xiaobei_question_strategy_1013D.json` defines how 小备 asks before generating candidates, with question limits by preparation depth.
- The HTML prep notebook now includes a lightweight teacher-facing preparation-depth selector: 快速 / 标准 / 精磨 / 公开课, plus a design-judgment summary for the current real topic.
- Boundary: 1013D is a local model and light preview pass only. It does not call a provider, write a database, write memory, write Feishu, export officially, archive officially, or generate a large ZIP.

## 1013E Lesson Reasoning Trace Module

- `lesson_reasoning_trace_module_1013E.md` defines the teacher-facing reasoning progress stream for the prep notebook.
- `lesson_reasoning_trace_module_1013E.json` records the trace-step structure and its internal pipeline mapping.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook` now shows a lightweight streamed thinking process after the teacher sends an instruction to 小备.
- `prep_room_render_canvas_deepen_v1.html#prepNotebookReasoning` opens a review-ready state with the reasoning trace completed and the edit candidate located at `教学过程 · 探究环节`.
- `prep_notebook_1013E_reasoning_trace_smoke.png` captures the completed reasoning-trace state.
- The visible trace uses teacher language: judging preparation depth, checking student blocker, locating the section, checking basis and impact, and organizing candidates.
- Boundary: this is a local static trace preview. It does not expose raw model reasoning, call a provider, write a database, write memory, write Feishu, formal apply, export officially, or archive officially.
