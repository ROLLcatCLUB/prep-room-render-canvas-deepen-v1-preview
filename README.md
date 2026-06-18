# PREP_ROOM_RENDER_CANVAS_DEEPEN_V1

This package turns the v5 prep-room static preview into a render-canvas preview.

## 2026-06-18 New Session Entry

- Start with `SESSION_HANDOFF_20260618_PREP_ROOM_M3_AND_R2D_NEXT.md`.
- Current review entry: `LATEST_REVIEW_ENTRY.md`.
- Current completed product stage: `1013I_R3_SELF_PREP_PREVIEW_CHAIN_FROM_REVIEW_CARDS`.
- Current product next stage: `1013I_R4_MINIMAL_SELF_PREP_PAGE_FIXTURE`.
- Current model default: `MiniMax-M3` with `thinking: {"type":"disabled"}`.
- Deep reasoning option: `MiniMax-M3` with `thinking: {"type":"adaptive"}`.
- Current boundary: no formal apply, no database write, no memory write, no Feishu write, no official archive/export, no formal 1013G. `accept_to_preview_only` remains sandbox-only.

## Files

- `prep_room_render_canvas_deepen_v1.html`
- `GPT_REVIEW_PROMPT.md`
- `REVIEW_PACKAGE_MANIFEST.md`
- `SESSION_HANDOFF_20260616_PREP_ROOM_RENDER_CANVAS.md`
- `SESSION_HANDOFF_20260618_PREP_ROOM_M3_AND_R2D_NEXT.md`
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
- R2D2 / 1013G PREP outputs are review-package data only; they do not write candidate text into the HTML body.
- 1013G teacher-review prep exposes `accept_to_preview_only`, `reject`, and `revise` options, but none of them perform formal apply.
- 1013H creates sandbox preview-state items and preview diff cards only; it remains reversible and does not write the formal lesson body.
- 1013I creates a teacher self-prep input schema, request envelope, sufficiency assessment, and fixture preview only; it does not call a provider/model.

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

## 1013F R2D Content Review Then Case Reference Assimilation

- `scripts/run_prep_room_1013f_r2d_content_review.py` performs the R2D content-quality gate for the R2C classroom-event polish baseline.
- Output directory: `1013F_R2D_content_review_then_case_reference_assimilation/`.
- Local knowledge-base cases were checked first. No same-topic mature case for 1-2 `色彩的感觉` was found, but six local art cases are usable for structure-only calibration.
- Best local references: Grade 3 `渐变的魅力`, Grade 3 `走进青绿山水`, official Grade 3 `色彩的碰撞`, Grade 3 `多变的色彩`, plus Grade 4 `色彩的和谐/对比` as upper-bound references.
- Final status: `PASS_CONTENT_REVIEW_WITH_CASE_REFERENCE_STRUCTURE_ONLY`.
- Next stage: `1013F_R2D2_CASE_REFERENCE_STRUCTURE_ASSIMILATION`.
- Boundary: no provider/model call, no Feishu/database/memory write, no formal apply, no 1013G, and no copied case text was inserted into the lesson.

## 1013F_R2D2 Case Reference Structure Assimilation

- `scripts/validate_1013F_R2D2_case_reference_structure_assimilation.py` converts R2D case references into structure-only candidate teaching moves.
- Output directory: `1013F_R2D2_case_reference_structure_assimilation/`.
- Required files were generated: `1013F_R2D2_result.json`, `1013F_R2D2_report.md`, `case_reference_registry_1013F_R2D2.json`, `teaching_moves_extraction_1013F_R2D2.json`, and `assimilation_candidate_patch_1013F_R2D2.json`.
- Final status: `PASS_CASE_REFERENCE_STRUCTURE_ASSIMILATION`.
- Boundary: no HTML body write, no direct case text copy, no formal apply, no database/memory/Feishu write, no formal 1013G, and no main-project push.

## 1013F_R2D2 Review Gate Before 1013G

- `scripts/validate_1013F_R2D2_review_gate_before_1013G.py` reviews R2D2 candidates before any teacher-review stage.
- Output directory: `1013F_R2D2_review_gate_before_1013G/`.
- Required files were generated: `R2D2_review_gate_result.json`, `R2D2_review_gate_report.md`, `approved_candidate_moves.json`, and `rejected_candidate_moves.json`.
- Final status: `PASS_R2D2_REVIEW_GATE_BEFORE_1013G`.
- Approved candidates: 3. Rejected candidates: 0.
- Boundary: approved means approved for sandbox preview only, not formal apply or teacher confirmation.

## 1013G_PREP Candidate Review Sandbox

- `scripts/validate_1013G_prep_candidate_review_sandbox.py` loads the approved R2D2 candidates into sandbox preview cards.
- Output directory: `1013G_PREP_candidate_review_sandbox/`.
- Required files were generated: `1013G_PREP_result.json`, `1013G_PREP_report.md`, and `candidate_review_surface_1013G_PREP.json`.
- Final status: `PASS_1013G_PREP_CANDIDATE_REVIEW_SANDBOX`.
- Boundary: preview data only; no lesson body write, no formal apply, no database/memory/Feishu write, and no formal 1013G.

## 1013G Teacher Review Prep Only

- `scripts/validate_1013G_teacher_review_prep_only.py` turns sandbox preview cards into teacher-review preparation cards.
- Output directory: `1013G_teacher_review_prep_only/`.
- Required files were generated: `1013G_teacher_review_prep_result.json`, `1013G_teacher_review_prep_report.md`, and `teacher_review_prep_surface_1013G.json`.
- Final status: `PASS_1013G_TEACHER_REVIEW_PREP_ONLY`.
- Teacher actions prepared: `accept_to_preview_only`, `reject`, and `revise`.
- Next stage: `1013H_SANDBOX_APPLY_TO_PREVIEW_ONLY`.
- Boundary: `accept_to_preview_only` remains sandbox-only; no formal apply, no formal 1013G, and no lesson body write.

## 1013H Sandbox Apply To Preview Only

- `scripts/validate_1013H_sandbox_apply_to_preview_only.py` simulates teacher actions from `1013G_TEACHER_REVIEW_PREP_ONLY` into sandbox preview state.
- Output directory: `1013H_sandbox_apply_to_preview_only/`.
- Required files were generated: `1013H_result.json`, `1013H_report.md`, `sandbox_preview_state_1013H.json`, `preview_diff_cards_1013H.json`, and `teacher_action_trace_1013H.json`.
- Final status: `PASS_1013H_SANDBOX_APPLY_TO_PREVIEW_ONLY`.
- Simulated actions: `accept_to_preview_only`, `reject`, and `revise`.
- Next stage: `1013I_TEACHER_SELF_PREP_INPUT_MINIMAL_FLOW`.
- Boundary: preview-state only; no formal apply, no formal 1013G, no lesson body write, no database/memory/Feishu write.

## 1013I Teacher Self Prep Input Minimal Flow

- `scripts/validate_1013I_teacher_self_prep_input_minimal_flow.py` creates the minimum teacher self-prep input workflow.
- Output directory: `1013I_teacher_self_prep_input_minimal_flow/`.
- Required files were generated: `1013I_result.json`, `1013I_report.md`, `teacher_self_prep_input_schema_1013I.json`, `teacher_self_prep_input_fixture_1013I.json`, `input_sufficiency_assessment_1013I.json`, `teacher_self_prep_request_1013I.json`, `self_prep_preview_fixture_1013I.json`, and `preview_chain_bridge_1013I.json`.
- Final status: `PASS_1013I_TEACHER_SELF_PREP_INPUT_MINIMAL_FLOW`.
- Required input fields are present; the fixture can generate a self-prep preview without provider/model calls.
- Next stage: `1013I_R0_UNIFIED_TEACHER_AGENT_PROFILE_AND_CAPABILITY_CONTRACT` first, then `1013I_R0A_VISIBLE_NAMING_AND_PROFILE_HOTFIX` before candidate-card seeding.
- Boundary: input envelope and fixture preview only; no provider/model call, no formal apply, no lesson body write, no database/memory/Feishu write.

## 1013M MiniMax M3 Connection

- `backend/xiaobei_ai/providers.py` now defaults MiniMax generation and vision fallback models to `MiniMax-M3`.
- M3 OpenAI-compatible calls use `max_completion_tokens` and default to `thinking: {"type":"disabled"}` for business JSON calls. `MINIMAX_M3_THINKING=adaptive` can be used when a stage explicitly needs M3 thinking output.
- `MINIMAX_MODEL=MiniMax-M3` is documented in `.env.example`, and the local user environment has been set to `MiniMax-M3`.
- Prep-room reasoning POC scripts that previously hardcoded `MiniMax-M2.7-highspeed` now request `MiniMax-M3`.
- `scripts/run_minimax_m3_connection_smoke.py` performs a minimal live JSON smoke.
- Output directory: `1013M_minimax_m3_connection/`.
- Final status: `PASS_MINIMAX_M3_CONNECTED`.

## 1013N MiniMax M3 Vs M2.7-highspeed Comparison

- `scripts/run_minimax_m3_vs_m27_highspeed_comparison.py` compares `MiniMax-M3` and `MiniMax-M2.7-highspeed` on two read-only cases.
- Case 1: minimal strict JSON probe. Both models passed; M3 was faster in the measured run.
- Case 2: standard daily prep-room reasoning for Grade 3 art 1-2 `色彩的感觉`.
- M3 produced strict JSON and passed the compact lesson-reasoning contract.
- M2.7-highspeed produced strict JSON but missed the required `探究环节` coverage in contract validation.
- Output directory: `1013N_minimax_m3_vs_m27_highspeed_comparison/`.
- Final status: `PASS_MINIMAX_M3_VS_M27_HIGHSPEED_COMPARISON`.
- Recommendation: use `MiniMax-M3` as default for structured prep-room reasoning; keep `MiniMax-M2.7-highspeed` only as fallback for simpler/shorter calls.

## 1013O MiniMax M3 Vs M2.7-highspeed Multi-Round Benchmark

- `scripts/run_minimax_m3_vs_m27_highspeed_multi_round_benchmark.py` repeats the comparison across 3 cases and 3 rounds per model.
- Total live calls: 18.
- Cases: exact JSON, short teacher suggestion, compact lesson patch.
- Both models passed all cases in this benchmark.
- Overall average latency: `MiniMax-M3=7544.4ms`, `MiniMax-M2.7-highspeed=16669.4ms`.
- Overall speed delta: M3 was faster by `9125.0ms` on average; M2.7-highspeed took `2.21x` the M3 latency.
- Final status: `PASS_MINIMAX_M3_VS_M27_HIGHSPEED_MULTI_ROUND_BENCHMARK`.
- Recommendation remains: use `MiniMax-M3` as the default prep-room reasoning model; keep M2.7-highspeed as configurable fallback only.

## 1013P MiniMax M3 Thinking Modes Benchmark

- `scripts/run_minimax_m3_thinking_modes_benchmark.py` compares M3 `thinking` modes on simple JSON and compact lesson-patch calls.
- Tested modes: `disabled`, `adaptive`, omitted default-on, and `enabled_probe`.
- Current MiniMax OpenAI-compatible API accepted `disabled` and `adaptive`; it rejected `enabled_probe` with invalid params and allowed values `adaptive, disabled`.
- On the lesson-patch case: `disabled=18110.5ms`, `adaptive=18661.5ms`, omitted default-on `24569.5ms`.
- Adaptive added about `551ms` / `3.0%` latency versus disabled on the lesson-patch case, and produced more reasoning content with slightly higher heuristic quality.
- Omitted default-on was slower and less explicit, so the system should not rely on omission.
- Recommendation: default `thinking: {"type":"disabled"}` for structured JSON and teacher-facing suggestions; use `adaptive` only for explicit deep reasoning stages.
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

## 1013F_R2C Classroom Event Detail Polish

- `scripts/run_prep_room_1013f_r2c_classroom_event_detail_polish.py` verifies the classroom-event content polish while inheriting the R2B2 layout baseline.
- Output directory: `1013F_R2C_classroom_event_detail_polish/`.
- Required files were generated: `1013F_R2C_result.json`, `1013F_R2C_report.md`, `classroom_event_detail_rules_1013F_R2C.json`, `ui_smoke_screenshot_1013F_R2C_view_numbered_sections.png`, `ui_smoke_screenshot_1013F_R2C_process_focus.png`, and `ui_smoke_screenshot_1013F_R2C_edit_bubble_kept.png`.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013FR2C` opens the numbered-section reading state.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013FR2CProcess` opens the teaching-process focus state.
- `prep_room_render_canvas_deepen_v1.html#prepNotebook1013FR2CEdit` opens the edit-bubble state after content polish.
- Normal lesson sections now use visible numbered lines such as `1.` and `2.`.
- Clicking normal sections no longer frames the main reading text; only the edit panel below keeps a container.
- Teaching process now has a distinct warm focus background and a teacher-facing cue.
- Teaching-process paragraphs now use visible process sequence numbers.
- Classroom events were expanded with teacher language, likely student responses, scaffolds, resources, evidence, and transitions.
- Final status: `PASS_CLASSROOM_EVENT_DETAIL_POLISH`.
- Next stage: `1013F_R2D_CASE_REFERENCE_ASSIMILATION_OR_CONTENT_REVIEW`.
- Boundary: no provider/model call, database write, memory write, Feishu write, formal apply, official export, official archive, real knowledge-base retrieval, raw model output to frontend, default entry change, 1013G action entry, or main-project commit/push.

## 1013S Feishu Schedule Real Time Binding

- `backend/xiaobei_ai/prep_room_feishu_schedule_1013A.py` now attaches local school-day time ranges to Feishu schedule slots.
- `scripts/run_prep_room_1013s_feishu_schedule_real_time_binding.py` verifies Feishu schedule probing and real-time calendar rendering.
- Output directory: `1013S_feishu_schedule_real_time_binding/`.
- Required files were generated: `1013S_result.json`, `1013S_report.md`, `feishu_schedule_probe_1013S.json`, `period_time_map_1013S.json`, and `ui_smoke_screenshot_1013S_week_calendar_real_time.png`.
- Feishu live read was checked first. It is not configured in this local environment, so auto mode falls back to the Feishu full-dump schedule snapshot.
- Snapshot mode reads 8 Xu Tao grade-three art schedule slots from `tbl7OxfE4YPSE6GU`.
- Week calendar cards now carry Feishu record id, room, period, and visible time range.
- Week dates are generated from the current natural week, anchored to `2026-06-17` for this preview.
- The left period column now shows the local school-day time configuration.
- Final status: `PASS_FEISHU_SNAPSHOT_SCHEDULE_REAL_TIME_BINDING_WITH_LIVE_CONFIG_CAVEAT`.
- Next stage: `1013S_R1_FEISHU_LIVE_CREDENTIAL_BINDING_OR_1013F_R2D_CONTENT_REVIEW`.
- Boundary: no provider/model call, database write, memory write, Feishu write, formal apply, official export, official archive, real knowledge-base retrieval, raw model output to frontend, default entry change, 1013G action entry, or main-project commit/push.

## 1013I_R0 Unified Teacher Agent And Capability Boundary Contract

- `scripts/validate_1013I_R0_unified_teacher_agent_and_capability_boundary_contract.py` generates the naming and capability-boundary contract before candidate-card seeding.
- Output directory: `1013I_R0_unified_teacher_agent_and_capability_boundary_contract/`.
- Required files were generated: `unified_teacher_agent_and_capability_boundary_contract.md`, `unified_teacher_agent_and_capability_boundary_contract.json`, `legacy_agent_deprecation_policy.json`, `visible_copy_naming_scan_1013I_R0.json`, `engineering_name_migration_map_1013I_R0.json`, `1013I_R0_result.json`, and `1013I_R0_report.md`.
- Teacher-visible agent contract: canonical role is `unified_teacher_agent`; current display name is `小教`; public-beta rename remains allowed by contract.
- Deprecated as teacher-visible front-stage agent names: `小备`, `小评`, `小管`, and `小美`.
- Backend distinctions move behind capability keys such as `lesson_prep`, `classroom_companion`, `learning_evidence`, `assessment_review`, `assessment_summary`, `resource_retrieval`, `archive`, and `export_draft`.
- The scan found current 1013I visible `小备` hits and records them as deferred to the profile hotfix stage.
- This stage does not perform global search/replace and does not rename historical paths, review packages, validators, or prior audit evidence.
- Final status: `PASS_UNIFIED_TEACHER_AGENT_AND_CAPABILITY_BOUNDARY_CONTRACT`.
- Superseded by: `1013I_R0_UNIFIED_TEACHER_AGENT_PROFILE_AND_CAPABILITY_CONTRACT`.
- Boundary: no provider/model call, database write, memory write, Feishu write, formal apply, lesson body/html write, repo path rename, global search/replace, or main-project commit/push.

## 1013I_R0 Unified Teacher Agent Profile And Capability Contract

- `scripts/validate_1013I_R0_unified_teacher_agent_profile_and_capability_contract.py` refines the earlier R0 boundary contract into a profile-aware engineering contract.
- Output directory: `1013I_R0_unified_teacher_agent_profile_and_capability_contract/`.
- Required files were generated: `unified_teacher_agent_profile_and_capability_contract.md`, `unified_teacher_agent_profile_and_capability_contract.json`, `assistant_profile_schema_1013I_R0.json`, `legacy_agent_alias_deprecation_policy_1013I_R0.json`, `visible_copy_and_agent_profile_scan_1013I_R0.json`, `capability_registry_1013I_R0.json`, `1013I_R0_profile_result.json`, and `1013I_R0_profile_report.md`.
- Engineering core: `unified_teacher_agent`.
- Current default display name: `小教`.
- `小教` is not the engineering kernel name. It is `assistant_profile.display_name` and remains customizable before public beta.
- Future assistant profile fields are reserved: `display_name`, `wake_name`, `voice_profile_id`, `tts_enabled`, `speaking_style`, `assistant_tone`, and `response_style`.
- Required new artifact shape uses `agent_role`, `assistant_profile`, `active_space`, and `active_capability`; it must not use only `"agent": "小教"`.
- Capability keys remain independent: `lesson_prep`, `classroom_companion`, `learning_evidence`, `assessment_review`, `assessment_summary`, `resource_retrieval`, `archive`, and `export_draft`.
- Deprecated as teacher-visible front-stage agent names: `小备`, `小评`, `小管`, and `小美`.
- The scan found current 1013I visible `小备` hits and an old `agent` field shape; both are deferred to `1013I_R0A_VISIBLE_NAMING_AND_PROFILE_HOTFIX`.
- This stage does not perform global search/replace and does not rename historical paths, review packages, validators, or prior audit evidence.
- Final status: `PASS_UNIFIED_TEACHER_AGENT_PROFILE_AND_CAPABILITY_CONTRACT`.
- Next stage: `1013I_R0A_VISIBLE_NAMING_AND_PROFILE_HOTFIX`.
- Boundary: no provider/model call, database write, memory write, Feishu write, formal apply, lesson body/html write, repo path rename, global search/replace, or main-project commit/push.

## 1013I_R0A Visible Naming And Profile Hotfix

- `scripts/validate_1013I_R0A_visible_naming_and_profile_hotfix.py` creates hotfixed successor artifacts from the current 1013I teacher self-prep request.
- Output directory: `1013I_R0A_visible_naming_and_profile_hotfix/`.
- Required files were generated: `1013I_R0A_result.json`, `1013I_R0A_report.md`, `teacher_self_prep_input_fixture_1013I_R0A.json`, `teacher_self_prep_request_1013I_R0A.json`, `self_prep_preview_fixture_1013I_R0A.json`, `visible_naming_and_profile_hotfix_scan_1013I_R0A.json`, and `visible_naming_and_profile_hotfix_manifest_1013I_R0A.json`.
- Original current 1013I artifacts are preserved as historical input; R0A writes successor artifacts for the next stage.
- Teacher-visible deprecated names after hotfix: zero.
- Legacy `agent` field after hotfix: false.
- Successor artifacts now use `agent_role=unified_teacher_agent`, `assistant_profile.display_name=小教`, `active_space=prep_room`, and `active_capability=lesson_prep`.
- R1 should read `1013I_R0A_visible_naming_and_profile_hotfix/teacher_self_prep_request_1013I_R0A.json`.
- Final status: `PASS_1013I_R0A_VISIBLE_NAMING_AND_PROFILE_HOTFIX`.
- Next stage: `1013I_R0A1_REQUEST_ID_TRACE_ALIGNMENT_HOTFIX`.
- Boundary: no provider/model call, database write, memory write, Feishu write, formal apply, lesson body/html write, repo path rename, global search/replace, historical review-package rewrite, old validator rename, or main-project commit/push.

## 1013I_R0A1 Request ID Trace Alignment Hotfix

- `scripts/validate_1013I_R0A1_request_id_trace_alignment_hotfix.py` aligns the R0A successor request id with the preview fixture source request id.
- Output directory: `1013I_R0A1_request_id_trace_alignment_hotfix/`.
- Required files were generated: `1013I_R0A1_result.json`, `1013I_R0A1_report.md`, `teacher_self_prep_request_1013I_R0A1.json`, `self_prep_preview_fixture_1013I_R0A1.json`, `request_id_trace_alignment_1013I_R0A1.json`, and `request_id_trace_alignment_hotfix_manifest_1013I_R0A1.json`.
- Trace alignment: `request_id=teacher_self_prep_request_1013I_R0A` and `source_request_id=teacher_self_prep_request_1013I_R0A`.
- Original request id is preserved as `original_request_id=teacher_self_prep_request_1013I`.
- Original 1013I and R0A artifacts are preserved; R0A1 writes aligned successor artifacts for the next stage.
- R1 should read `1013I_R0A1_request_id_trace_alignment_hotfix/teacher_self_prep_request_1013I_R0A1.json`.
- Final status: `PASS_1013I_R0A1_REQUEST_ID_TRACE_ALIGNMENT_HOTFIX`.
- Next stage: `1013I_R1_CANDIDATE_CARD_SEED_FROM_SELF_PREP_REQUEST`.
- Boundary: no provider/model call, database write, memory write, Feishu write, formal apply, lesson body/html write, repo path rename, global search/replace, historical review-package rewrite, old validator rename, or main-project commit/push.

## 1013I_R1 Candidate Card Seed From Self Prep Request

- `scripts/validate_1013I_R1_candidate_card_seed_from_self_prep_request.py` creates candidate-card seed data from the aligned R0A1 teacher self-prep request.
- Output directory: `1013I_R1_candidate_card_seed_from_self_prep_request/`.
- Required files were generated: `1013I_R1_result.json`, `1013I_R1_report.md`, `candidate_card_seed_1013I_R1.json`, `candidate_card_seed_bundle_1013I_R1.json`, `candidate_card_seed_trace_1013I_R1.json`, and `candidate_seed_to_teacher_review_surface_bridge_1013I_R1.json`.
- Source request: `1013I_R0A1_request_id_trace_alignment_hotfix/teacher_self_prep_request_1013I_R0A1.json`.
- Source request id: `teacher_self_prep_request_1013I_R0A`.
- Candidate seeds created: learning problem, material scaffold, and review chain.
- Each seed includes source teacher input, a draft seed, seed basis, risk note, and teacher action options.
- This stage is seed-only and teacher-review-required; it does not create lesson body text, preview apply state, or formal apply output.
- Final status: `PASS_1013I_R1_CANDIDATE_CARD_SEED_FROM_SELF_PREP_REQUEST`.
- Next stage: `1013I_R2_TEACHER_REVIEW_CARD_SURFACE_FROM_SEED`.
- Boundary: no provider/model call, database write, memory write, Feishu write, formal apply, lesson body/html write, preview apply, or main-project commit/push.

## 1013I_R2 Teacher Review Card Surface From Seed

- `scripts/validate_1013I_R2_teacher_review_card_surface_from_seed.py` converts the R1 seed bundle into teacher-readable review-card surface data.
- Output directory: `1013I_R2_teacher_review_card_surface_from_seed/`.
- Required files were generated: `1013I_R2_result.json`, `1013I_R2_report.md`, `teacher_review_card_surface_1013I_R2.json`, `review_card_actions_1013I_R2.json`, and `teacher_review_card_surface_trace_1013I_R2.json`.
- Review cards created: 3.
- Each card includes card title, source teacher input, assistant suggestion, why-this-suggestion, risk note, and teacher action options.
- Teacher action options: `accept_to_preview`, `revise_seed`, and `reject_seed`.
- R2 only exposes `accept_to_preview`; it does not execute preview apply. Preview-chain state is deferred to R3.
- Final status: `PASS_1013I_R2_TEACHER_REVIEW_CARD_SURFACE_FROM_SEED`.
- Next stage: `1013I_R3_SELF_PREP_PREVIEW_CHAIN_FROM_REVIEW_CARDS`.
- Boundary: no provider/model call, database write, memory write, Feishu write, formal apply, lesson body/html write, preview-chain execution, or main-project commit/push.

## 1013I_R3 Self Prep Preview Chain From Review Cards

- `scripts/validate_1013I_R3_self_prep_preview_chain_from_review_cards.py` simulates review-card actions into preview-chain state.
- Output directory: `1013I_R3_self_prep_preview_chain_from_review_cards/`.
- Required files were generated: `1013I_R3_result.json`, `1013I_R3_report.md`, `self_prep_preview_chain_state_1013I_R3.json`, `self_prep_preview_diff_cards_1013I_R3.json`, `self_prep_review_card_action_trace_1013I_R3.json`, and `self_prep_preview_chain_to_minimal_page_fixture_bridge_1013I_R3.json`.
- Simulated actions: `accept_to_preview`, `revise_seed`, and `reject_seed`.
- Preview data created: 3 accepted preview items, 3 revision queue items, 3 rejected items, and 3 preview diff cards.
- Action trace count: 9.
- Revert is available; formal apply remains forbidden.
- Final status: `PASS_1013I_R3_SELF_PREP_PREVIEW_CHAIN_FROM_REVIEW_CARDS`.
- Next stage: `1013I_R4_MINIMAL_SELF_PREP_PAGE_FIXTURE`.
- Boundary: preview-chain simulation only; no provider/model call, database write, memory write, Feishu write, formal apply, lesson body/html write, official export/archive, or main-project commit/push.
