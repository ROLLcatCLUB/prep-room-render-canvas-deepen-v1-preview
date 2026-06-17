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

## 1013E Model Prompt To Reasoning Field Patch POC

- `scripts/run_prep_room_1013e_model_prompt_to_reasoning_field_patch_poc.py` runs the live model POC for four fixed lesson-design modes.
- Output directory: `live_poc_1013E/`.
- Required files were generated: `1013E_result.json`, `1013E_report.md`, four test result JSON files, `provider_metrics_1013E.json`, `redacted_provider_trace_1013E.json`, and `prompt_used_1013E.md`.
- Final status: `FAIL_MODEL_OUTPUT_NOT_STABLE`.
- What worked: `quick_daily` produced strict JSON and usable lesson-design field patch structure.
- What failed: `standard_daily` started producing the expected structure but did not return parseable complete JSON; `open_class` and `research_lesson` timed out.
- Conclusion: the model path is plausible, but the prompt is too heavy for stable four-case output. Next stage should be `1013E_R1_PROMPT_REPAIR`, with shorter schema, smaller source context, and mode-specific prompt compression.
- Boundary: no database write, memory write, Feishu write, formal apply, official export, or official archive was performed.

## 1013E_R1 Backend Reuse And Repair Review

- `backend_reuse_and_repair_plan_1013E_R1.md` records which existing backend foundations can be reused for the prep notebook reasoning layer.
- Direct reuse: provider transport, strict output parser, controlled MiniMax JSON extraction, and the read-only Feishu schedule adapter as schedule context.
- Pattern-only reuse: visible action trace, semantic orchestration, side-effect gate, renderer patch plan, and read-only candidate repair patterns.
- Not reused in this step: broad workbench agent runtime, memory modules, and teaching-planning candidate rules that would flatten lesson design into generic field filling.
- `backend/xiaobei_ai/prep_room_lesson_reasoning_contract_1013E.py` now centralizes the real lesson context, required output shape, boundary flags, strict parser binding, and lesson-reasoning payload validation.
- `scripts/run_prep_room_1013e_model_prompt_to_reasoning_field_patch_poc.py` now uses that contract instead of local loose JSON extraction and duplicate validation.
- Next stage: `1013E_R1_PROMPT_REPAIR_AND_READONLY_REASONING_PIPELINE`.

## 1013E_R1 Prompt Repair And Readonly Reasoning Pipeline

- `backend/xiaobei_ai/prep_room_lesson_reasoning_pipeline_1013E_R1.py` adds the internal read-only lesson reasoning pipeline.
- `scripts/run_prep_room_1013e_r1_prompt_repair_readonly_pipeline.py` runs the repaired compact-prompt live POC for four lesson-design modes.
- Output directory: `live_poc_1013E_R1/`.
- Required files were generated: `1013E_R1_result.json`, `1013E_R1_report.md`, four mode result JSON files, `provider_metrics_1013E_R1.json`, `redacted_provider_trace_1013E_R1.json`, `visible_reasoning_trace_samples_1013E_R1.json`, and `prompt_repair_1013E_R1.md`.
- Final status: `PASS_STRICT_JSON_WITH_ONE_FAILURE`.
- What passed: `quick_daily`, `open_class`, and `research_lesson` produced strict JSON and passed the compact lesson-reasoning contract.
- What failed: `standard_daily` still returned non-parseable JSON.
- Boundary: provider was called; no database write, memory write, Feishu write, formal apply, official export, or official archive was performed.
- Next stage: `1013F_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING`.

## 1013E_R2 Standard Daily Repair

- `scripts/run_prep_room_1013e_r2_standard_daily_repair.py` runs the targeted repair for the failed `standard_daily` case only.
- Output directory: `live_poc_1013E_R2/`.
- Required files were generated: `1013E_R2_result.json`, `1013E_R2_report.md`, `test_standard_daily_repair_result.json`, `prompt_repair_standard_daily_1013E_R2.md`, `redacted_provider_trace_1013E_R2.json`, and `provider_metrics_1013E_R2.json`.
- Final status: `STANDARD_DAILY_REPAIR_FAILED`.
- What improved: the final R2 attempt produced strict JSON.
- What still failed: the JSON did not satisfy the compact contract; key arrays were returned in looser shapes, so the validator correctly blocked UI binding readiness.
- Conclusion: do not enter full `1013F` with `standard_daily` yet. Next stage should be `1013E_R3_PROMPT_REPAIR_OR_MODEL_STRATEGY_ADJUSTMENT`, likely adding a normalization step before UI binding.
- Boundary: provider was called; no database write, memory write, Feishu write, formal apply, official export, or official archive was performed.

## 1013E_R2 Multi-Case Lesson Reasoning Benchmark

- `scripts/run_prep_room_1013e_r2_multi_case_benchmark.py` runs the 12-case benchmark requested for lesson reasoning stability.
- Output directory: `live_poc_1013E_R2/`.
- Required files were generated: `1013E_R2_result.json`, `1013E_R2_report.md`, `lesson_reasoning_case_bank_1013E_R2.json`, `case_results_1013E_R2.json`, `benchmark_scores_1013E_R2.json`, `standard_daily_repair_result_1013E_R2.json`, `prompt_repair_1013E_R2.md`, `provider_metrics_1013E_R2.json`, and `redacted_provider_trace_1013E_R2.json`.
- Final status: `FAIL_STANDARD_DAILY_REPAIR`.
- Benchmark summary: 12 cases, 4 strict JSON successes, 2 raw contract successes, 4 normalized contract successes, 3 overall passes, 8 empty/failed content cases.
- The targeted standard-daily probe can pass in isolation, but the final full benchmark still failed the main `standard_daily_cold_warm_more_visual` case, showing provider/prompt instability under multi-case conditions.
- Conclusion: do not enter `1013F` UI binding yet. Next stage should be `1013E_R3_PROMPT_REPAIR`, focused on stabilizing the standard daily case and reducing empty provider responses before UI binding.
- Boundary: provider was called; no database write, memory write, Feishu write, formal apply, official export, official archive, real knowledge-base retrieval, large ZIP, or main-project commit/push was performed.

## 1013E_R3 Lesson Unfolding Graph Normalizer And Effectiveness Eval

- `backend/xiaobei_ai/prep_room_lesson_reasoning_contract_1013E.py` now includes the R3 lesson-unfolding extensions: `lesson_unfolding_graph`, `classroom_event`, wide-output normalization, contract validation, time balance evaluation, and classroom-unfolding effectiveness scoring.
- `scripts/run_prep_room_1013e_r3_unfolding_graph_eval.py` runs the 6-case R3 live POC.
- Output directory: `live_poc_1013E_R3/`.
- Required files were generated: `1013E_R3_result.json`, `1013E_R3_report.md`, `case_results_1013E_R3.json`, `standard_daily_repair_result_1013E_R3.json`, `dance_rhythm_case_result_1013E_R3.json`, `wide_to_unfolding_normalization_trace_1013E_R3.json`, `classroom_unfolding_effectiveness_eval_1013E_R3.json`, `time_rebalance_trace_1013E_R3.json`, `provider_metrics_1013E_R3.json`, `redacted_provider_trace_1013E_R3.json`, and `prompt_repair_1013E_R3.md`.
- Final status: `FAIL_STANDARD_DAILY_REPAIR`.
- Benchmark summary: 6 cases, 3 strict-or-wide parse successes, 3 normalization successes, 2 contract validation successes, 2 classroom effectiveness passes.
- What worked: the schema, normalizer, evaluator, and time rebalancer ran end to end; `quick_daily_basic_design` and `constrained_low_resource_no_video` produced usable unfolding graph candidates.
- What failed: the standard-daily main case and the teacher-provided dance/rhythm case did not produce parseable unfolding graph payloads in the final live POC.
- Conclusion: do not enter `1013F` UI binding yet. Next stage should be `1013E_R4_MODEL_STRATEGY_ADJUSTMENT`, likely using a staged multi-call strategy instead of asking one call to generate the full unfolding graph.
- Boundary: provider was called; no database write, memory write, Feishu write, formal apply, official export, official archive, UI binding, real knowledge-base retrieval, large ZIP, or main-project commit/push was performed.

## 1013E_R4 Staged Lesson Derivation Pipeline

- `high_quality_prep_system_market_research_and_classroom_reasoning_report_20260617.md` records the market and pedagogy research conclusion: Shiwei/Xiaobei should become a classroom reasoning collaboration system, not a faster lesson-plan generator.
- `prep_room_1013E_R4_staged_lesson_derivation_pipeline_plan.md` records the R4 strategy shift: stop competitor research for now, stop one-call full lesson graph generation, and move to staged derivation.
- `backend/xiaobei_ai/prep_room_staged_derivation_pipeline_1013E_R4.py` adds a local staged derivation pipeline: context pack, learning problem, target shift, evidence plan, teaching route, classroom events, event unfolding, time rebalance, evidence binding, effectiveness evaluation, and teacher review candidate.
- `scripts/run_prep_room_1013e_r4_staged_derivation_pipeline.py` runs the 3-case R4 POC.
- Output directory: `live_poc_1013E_R4/`.
- Required files were generated: `1013E_R4_result.json`, `1013E_R4_report.md`, `case_results_1013E_R4.json`, `staged_pipeline_trace_1013E_R4.json`, `learning_problem_derivation_1013E_R4.json`, `target_shift_derivation_1013E_R4.json`, `evidence_plan_1013E_R4.json`, `teaching_route_plan_1013E_R4.json`, `classroom_event_generation_1013E_R4.json`, `event_unfolding_expansion_1013E_R4.json`, `time_rebalance_trace_1013E_R4.json`, `evidence_binding_trace_1013E_R4.json`, `effectiveness_eval_1013E_R4.json`, `candidate_error_trace_1013E_R4.json`, `provider_metrics_1013E_R4.json`, and `redacted_provider_trace_1013E_R4.json`.
- Final status: `PASS_STAGED_LESSON_DERIVATION_PIPELINE`.
- Benchmark summary: 3 cases, 3 pipeline passes; the main `standard_daily_cold_warm_more_visual` case passed.
- Strategy note: R4 is local rule-based staged derivation first, so provider/model were not called in this pass. This proves the staged reasoning shape before reintroducing model calls or UI binding.
- Boundary: no UI binding, no database write, no memory write, no Feishu write, no formal apply, no official export, no official archive, no real knowledge-base retrieval, and no raw model output was sent to frontend.

## 1013F Reasoning Field Patch To View/Edit UI Binding

- `scripts/run_prep_room_1013f_view_edit_ui_binding.py` maps the R4 staged derivation output into teacher-readable view/edit binding samples.
- Output directory: `1013F_view_edit_ui_binding/`.
- Required files were generated: `1013F_result.json`, `1013F_report.md`, `view_mode_binding_sample_1013F.json`, `edit_mode_binding_sample_1013F.json`, `patch_candidate_cards_1013F.json`, `impact_scope_mapping_1013F.json`, `teacher_review_action_contract_1013F.json`, `candidate_error_display_1013F.json`, and `ui_smoke_screenshot_1013F.png`.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013F` opens the preview-only view binding state.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013FEdit` opens the preview-only edit binding state focused on `教学过程 · 色卡分类探究`.
- Final status: `PASS_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING`.
- Next stage: `1013G_TEACHER_REVIEW_ACTIONS_PREVIEW_SANDBOX`.
- Boundary: no provider/model call, database write, memory write, Feishu write, formal apply, official export, official archive, real knowledge-base retrieval, raw model output to frontend, default entry change, or main-project commit/push.

## 1013F_R1 Teacher Readable Inline Reasoning Surface

- `scripts/run_prep_room_1013f_r1_teacher_readable_quality_check.py` runs the multi-pass teacher-reading quality check.
- Output directory: `1013F_R1_teacher_readable_inline_reasoning_surface/`.
- Required files were generated: `1013F_R1_result.json`, `1013F_R1_report.md`, `teacher_readable_paragraph_render_rules_1013F_R1.json`, `paragraph_anchor_mapping_1013F_R1.json`, `hover_reasoning_note_sample_1013F_R1.json`, `selected_paragraph_design_note_sample_1013F_R1.json`, `edit_mode_selected_paragraph_sample_1013F_R1.json`, `impact_scope_teacher_language_mapping_1013F_R1.json`, `candidate_error_inline_display_1013F_R1.json`, `ui_smoke_screenshot_1013F_R1_view.png`, and `ui_smoke_screenshot_1013F_R1_hover_or_selected.png`.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013FR1` opens the denoised reading surface.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013FR1Selected` opens the selected-paragraph note state.
- The teaching process now reads as continuous classroom paragraphs. Hover notes follow the pointer; clicking a paragraph opens one local note panel; clicking blank space closes it; scroll position is preserved during note toggles.
- Final status: `PASS_TEACHER_READABLE_INLINE_REASONING_SURFACE`.
- Next stage: `1013F_R2_CLASSROOM_EVENT_DETAIL_POLISH`.
- Boundary: no provider/model call, database write, memory write, Feishu write, formal apply, official export, official archive, real knowledge-base retrieval, raw model output to frontend, default entry change, 1013G action entry, or main-project commit/push.

## 1013F_R2A Information Hierarchy And Edit Surface Repair

- `scripts/run_prep_room_1013f_r2a_information_hierarchy_repair.py` runs the information-hierarchy and edit-surface repair check.
- Output directory: `1013F_R2A_information_hierarchy_edit_surface_repair/`.
- Required files were generated: `1013F_R2A_result.json`, `1013F_R2A_report.md`, `information_hierarchy_rules_1013F_R2A.json`, `selected_paragraph_side_note_sample_1013F_R2A.json`, `edit_surface_sample_1013F_R2A.json`, `forbidden_table_check_1013F_R2A.json`, `ui_smoke_screenshot_1013F_R2A_view.png`, `ui_smoke_screenshot_1013F_R2A_selected_note.png`, and `ui_smoke_screenshot_1013F_R2A_edit.png`.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013FR2A` opens the repaired reading surface.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013FR2ASelected` opens the selected paragraph floating-note state.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013FR2AEdit` opens the focused four-block edit surface.
- R2A does not remove backend fields. It lowers their teacher-facing weight: source details are available in collapsed, muted, low-weight blocks, while the main page keeps classroom reading first.
- Final status: `PASS_INFORMATION_HIERARCHY_AND_EDIT_SURFACE_REPAIR`.
- Next stage: `1013F_R2_CLASSROOM_EVENT_DETAIL_POLISH`.
- Boundary: no provider/model call, database write, memory write, Feishu write, formal apply, official export, official archive, real knowledge-base retrieval, raw model output to frontend, default entry change, 1013G action entry, or main-project commit/push.

## 1013F_R2B Teacher Readable Copy And Visual Tone Repair

- `scripts/run_prep_room_1013f_r2b_teacher_readable_copy_visual_tone.py` runs the teacher-readable copy and visual-tone repair check.
- Output directory: `1013F_R2B_teacher_readable_copy_and_visual_tone_repair/`.
- Required files were generated: `1013F_R2B_result.json`, `1013F_R2B_report.md`, `teacher_display_label_map_1013F_R2B.json`, `visual_tone_rules_1013F_R2B.json`, `low_weight_source_sample_1013F_R2B.json`, `teacher_readable_copy_sample_1013F_R2B.json`, `ui_smoke_screenshot_1013F_R2B_view.png`, `ui_smoke_screenshot_1013F_R2B_selected_note.png`, and `ui_smoke_screenshot_1013F_R2B_edit.png`.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013FR2B` opens the repaired reading tone state.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013FR2BSelected` opens the softened selected-note state.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013FR2BEdit` opens the softened edit surface.
- Added `teacher_display_label_map` so raw backend field keys can map to teacher-readable labels. Raw field keys remain only in collapsed low-weight source details for debugging and error observation.
- Visible assistant copy now uses `小教`; visible legacy assistant-name hits are zero.
- Final status: `PASS_TEACHER_READABLE_COPY_AND_VISUAL_TONE_REPAIR`.
- Next stage: `1013F_R2C_CLASSROOM_EVENT_DETAIL_POLISH`.
- Boundary: no provider/model call, database write, memory write, Feishu write, formal apply, official export, official archive, real knowledge-base retrieval, raw model output to frontend, default entry change, 1013G action entry, or main-project commit/push.

## 1013F_R2B1 Edit Bubble Annotation Surface

- `scripts/run_prep_room_1013f_r2b1_edit_bubble_annotation_surface.py` verifies that edit candidates no longer appear inside the lesson body.
- Output directory: `1013F_R2B1_edit_bubble_annotation_surface/`.
- Required files were generated: `1013F_R2B1_result.json`, `1013F_R2B1_report.md`, `edit_bubble_rules_1013F_R2B1.json`, `edit_bubble_sample_1013F_R2B1.json`, and `ui_smoke_screenshot_1013F_R2B1_edit_bubble.png`.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013FR2B1EditBubble` opens the edit bubble state.
- Edit mode now keeps the lesson body clean: the current paragraph is highlighted, while all current-section changes live in a floating annotation bubble with an arrow pointing to the body.
- Low-weight source details remain available inside the bubble for debugging and error observation.
- Final status: `PASS_EDIT_BUBBLE_ANNOTATION_SURFACE`.
- Next stage: `1013F_R2C_CLASSROOM_EVENT_DETAIL_POLISH`.
- Boundary: no provider/model call, database write, memory write, Feishu write, formal apply, official export, official archive, real knowledge-base retrieval, raw model output to frontend, default entry change, 1013G action entry, or main-project commit/push.

## 1013F_R2B2 Layout Cleanup

- `scripts/run_prep_room_1013f_r2b2_layout_cleanup.py` verifies the latest layout cleanup requested after R2B1.
- Output directory: `1013F_R2B2_layout_cleanup/`.
- Required files were generated: `1013F_R2B2_result.json`, `1013F_R2B2_report.md`, `layout_cleanup_rules_1013F_R2B2.json`, `ui_smoke_screenshot_1013F_R2B2_view.png`, and `ui_smoke_screenshot_1013F_R2B2_edit_toggle_bubble.png`.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013FR2B2` opens the cleaned reading state.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013FR2B2Edit` opens the edit bubble state focused on `教学过程 · 探究环节`.
- Edit buttons now toggle open/closed for the current target; the focused edit button reads `收起`.
- The edit bubble now starts near the right edge of the selected paragraph and expands over the right-side area.
- Lesson status is reduced into colored lights plus short text in the view/edit state row.
- The visible lesson-brief sentence was removed from the main body.
- `本课设计判断` and `小教读课提示` moved to the right reading-assist area above the edit auxiliary panels and are collapsible.
- The main reading area now enters the lesson body directly with a light text background.
- Final status: `PASS_LAYOUT_CLEANUP`.
- Next stage: `1013F_R2C_CLASSROOM_EVENT_DETAIL_POLISH`.
- Boundary: no provider/model call, database write, memory write, Feishu write, formal apply, official export, official archive, real knowledge-base retrieval, raw model output to frontend, default entry change, 1013G action entry, or main-project commit/push.
