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
