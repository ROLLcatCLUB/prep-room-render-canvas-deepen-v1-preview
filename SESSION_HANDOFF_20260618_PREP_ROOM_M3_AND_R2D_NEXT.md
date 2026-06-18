# Session Handoff 2026-06-18: Prep Room M3 Provider Line And R2D Next

```text
handoff_status=READY_FOR_NEW_SESSION
current_latest_stage=1013P_MINIMAX_M3_THINKING_MODES_BENCHMARK
latest_review_commit=e4d55628901df41acc90f4c8c4c26fccc689d840
recommended_next_product_stage=1013F_R2D2_CASE_REFERENCE_STRUCTURE_ASSIMILATION
default_model_recommendation=MiniMax-M3_WITH_THINKING_DISABLED
deep_reasoning_option=MiniMax-M3_WITH_THINKING_ADAPTIVE
main_project_committed=false
main_project_pushed=false
```

## 1. Where To Start

Local workspace:

```text
D:\Documents\SmartEdu\xiaobei-core
```

Local review mirror:

```text
D:\Documents\SmartEdu\xiaobei-github-review\prep-room-render-canvas-deepen-v1-preview
```

GitHub review repo:

```text
https://github.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview
```

Latest review entry:

```text
https://raw.githubusercontent.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview/e4d55628901df41acc90f4c8c4c26fccc689d840/LATEST_REVIEW_ENTRY.md
```

## 2. Current Product Thread

The prep notebook has already passed the recent UI/content baseline stages:

```text
1013F_R2B2_LAYOUT_CLEANUP
1013F_R2C_CLASSROOM_EVENT_DETAIL_POLISH
1013F_R2D_CONTENT_REVIEW_THEN_CASE_REFERENCE_ASSIMILATION
```

The accepted content baseline before model testing was:

```text
BASELINE_COMMIT=fa83edcadfee242a86a452bbfac1d8971a933f46
ACCEPTED_STAGE=1013F_R2C_CLASSROOM_EVENT_DETAIL_POLISH
NEXT_STAGE=1013F_R2D_CONTENT_REVIEW_THEN_CASE_REFERENCE_ASSIMILATION
```

R2D content review has been completed:

```text
FINAL_STATUS=PASS_CONTENT_REVIEW_WITH_CASE_REFERENCE_STRUCTURE_ONLY
NEXT_STAGE=1013F_R2D2_CASE_REFERENCE_STRUCTURE_ASSIMILATION
```

R2D conclusion:

- The current R2C classroom unfolding is basically teacher-readable and suitable for Grade 3 art.
- No mature same-topic local case for `1-2《色彩的感觉》` was found.
- Official Grade 3 material can be used for age/goal calibration.
- Local `渐变的魅力` and `走进青绿山水` are useful as structure references but should be treated as AI-generated or AI-assisted samples, not authoritative cases.
- Future IMA-generated cases may be useful as candidate variants, but only as structure/action samples, not as copied text.

Recommended next product stage:

```text
1013F_R2D2_CASE_REFERENCE_STRUCTURE_ASSIMILATION
```

Scope for next product stage:

- Use official Grade 3 sources as calibration.
- Optionally ask IMA to generate 2-3 variant cases:
  - normal daily lesson;
  - student-blocker-focused lesson;
  - resource/learning-sheet-focused lesson.
- Decompose cases into teaching moves, question chains, material timing, evidence design, and risk handling.
- Do not directly paste case text into the lesson.
- Do not enter 1013G teacher-confirmation actions until R2D2 candidates are reviewed.

## 3. Feishu Schedule Line

Stage:

```text
1013S_FEISHU_SCHEDULE_REAL_TIME_BINDING
FINAL_STATUS=PASS_FEISHU_SNAPSHOT_SCHEDULE_REAL_TIME_BINDING_WITH_LIVE_CONFIG_CAVEAT
```

Important caveat:

- Live Feishu was checked first but was not configured in this environment.
- The preview uses the local Feishu full-dump snapshot.
- Source table does not contain real date/time fields.
- Time is currently derived from local school period mapping plus the current week dates.

Do not treat this as formal live Feishu provider integration.

## 4. MiniMax Model Line

### 1013M: M3 Connection

Stage:

```text
1013M_MINIMAX_M3_CONNECTION
FINAL_STATUS=PASS_MINIMAX_M3_CONNECTED
```

Changes:

- `MiniMax-M3` is now the local default MiniMax model.
- `.env.example` documents `MINIMAX_MODEL=MiniMax-M3`.
- Local user environment was set to `MINIMAX_MODEL=MiniMax-M3`.
- Provider M3 calls use `max_completion_tokens`.
- Provider defaults business JSON calls to:

```json
{"thinking":{"type":"disabled"}}
```

Smoke result:

```json
{"ok":true,"model_check":"m3"}
```

### 1013N: M3 vs M2.7-highspeed Initial Comparison

Stage:

```text
1013N_MINIMAX_M3_VS_M27_HIGHSPEED_COMPARISON
FINAL_STATUS=PASS_MINIMAX_M3_VS_M27_HIGHSPEED_COMPARISON
```

Initial result:

```text
MiniMax-M3=12
MiniMax-M2.7-highspeed=9
winner=MiniMax-M3
```

### 1013O: M3 vs M2.7-highspeed Multi-Round Benchmark

Stage:

```text
1013O_MINIMAX_M3_VS_M27_HIGHSPEED_MULTI_ROUND_BENCHMARK
FINAL_STATUS=PASS_MINIMAX_M3_VS_M27_HIGHSPEED_MULTI_ROUND_BENCHMARK
```

Benchmark shape:

```text
3 cases
3 rounds per model per case
18 live provider calls
```

Overall result:

```text
MiniMax-M3 average latency = 7544.4ms
MiniMax-M2.7-highspeed average latency = 16669.4ms
M3 faster by = 9125.0ms average
M2.7-highspeed / M3 latency ratio = 2.21x
M3 latency reduction vs M2.7-highspeed = 54.7%
MiniMax-M3 pass_rate = 1.0
MiniMax-M2.7-highspeed pass_rate = 1.0
```

Recommendation:

```text
Use MiniMax-M3 as default prep-room reasoning model.
Keep MiniMax-M2.7-highspeed as configurable fallback only.
```

### 1013P: M3 Thinking Modes

Stage:

```text
1013P_MINIMAX_M3_THINKING_MODES_BENCHMARK
FINAL_STATUS=PASS_MINIMAX_M3_THINKING_MODES_BENCHMARK
```

Observed OpenAI-compatible API behavior:

```text
thinking.type=disabled -> accepted
thinking.type=adaptive -> accepted
thinking omitted -> thinking is on by default
thinking.type=enabled -> rejected
```

The live API rejection for `enabled`:

```text
invalid params, invalid thinking.type: "enabled" (allowed: adaptive, disabled)
```

Lesson-patch case result:

```text
disabled avg latency = 18110.5ms
adaptive avg latency = 18661.5ms
omitted default-on avg latency = 24569.5ms

adaptive vs disabled = +551.0ms / +3.0%
omitted default-on vs disabled = +6459.0ms / +35.7%
```

Recommendation:

```text
Default: MiniMax-M3 + thinking disabled
Deep reasoning: MiniMax-M3 + thinking adaptive
Do not use thinking.type=enabled on current API path
Do not omit thinking accidentally
```

## 5. Important Implementation Details

Files modified for M3 line:

```text
backend/xiaobei_ai/providers.py
backend/xiaobei_ai/workbench_ai_candidate_dry_run.py
scripts/run_prep_room_1013e_r2_multi_case_benchmark.py
scripts/run_prep_room_1013e_r2_standard_daily_repair.py
scripts/run_prep_room_1013e_r3_unfolding_graph_eval.py
scripts/run_agent_capability_spike_0952B.py
.env.example
```

New benchmark scripts:

```text
scripts/run_minimax_m3_connection_smoke.py
scripts/run_minimax_m3_vs_m27_highspeed_comparison.py
scripts/run_minimax_m3_vs_m27_highspeed_multi_round_benchmark.py
scripts/run_minimax_m3_thinking_modes_benchmark.py
```

Important provider behavior:

- `MiniMax-M3` requires `max_completion_tokens` on the current OpenAI-compatible path.
- For compact JSON, `thinking: {"type":"disabled"}` avoids reasoning consuming output budget.
- `MINIMAX_M3_THINKING=adaptive` can be used later when a stage explicitly asks for deeper reasoning.

## 6. Review Artifacts

Latest commit:

```text
e4d55628901df41acc90f4c8c4c26fccc689d840
```

Latest entry:

```text
https://raw.githubusercontent.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview/e4d55628901df41acc90f4c8c4c26fccc689d840/LATEST_REVIEW_ENTRY.md
```

M3 connection:

```text
https://raw.githubusercontent.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview/895b097dd333097e3d9e63df713d0ef499491f02/1013M_minimax_m3_connection/1013M_result.json
```

M3 vs M2.7 initial:

```text
https://raw.githubusercontent.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview/11eb80ff5d5a2535623c5d97f698d051ff219e74/1013N_minimax_m3_vs_m27_highspeed_comparison/1013N_result.json
```

M3 vs M2.7 multi-round:

```text
https://raw.githubusercontent.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview/e5e36fd2e5f491179933ae17a23b32fae8adae27/1013O_minimax_m3_vs_m27_highspeed_multi_round/1013O_result.json
```

M3 thinking:

```text
https://raw.githubusercontent.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview/e4d55628901df41acc90f4c8c4c26fccc689d840/1013P_minimax_m3_thinking_modes_benchmark/1013P_result.json
https://raw.githubusercontent.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview/e4d55628901df41acc90f4c8c4c26fccc689d840/1013P_minimax_m3_thinking_modes_benchmark/1013P_interpretation_note.md
```

## 7. Boundaries For Next Session

Do not do these unless explicitly asked:

```text
formal_apply
database write
memory write
Feishu write
official archive
official export
enter 1013G
push main project tree
copy external/IMA case text directly into lesson
```

Safe next steps:

```text
1. Review official Grade 3 source material as calibration.
2. Generate or request IMA case variants as reference-only candidates.
3. Start 1013F_R2D2_CASE_REFERENCE_STRUCTURE_ASSIMILATION.
4. Use MiniMax-M3 thinking disabled for compact JSON candidates.
5. Use MiniMax-M3 thinking adaptive only for explicit deep reasoning / comparison traces.
6. Upload every new review package to the independent GitHub review repo.
```

## 8. Suggested First Prompt For Next Session

```text
请先读取：
- outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/SESSION_HANDOFF_20260618_PREP_ROOM_M3_AND_R2D_NEXT.md
- outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/LATEST_REVIEW_ENTRY.md
- outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/1013P_minimax_m3_thinking_modes_benchmark/1013P_interpretation_note.md

然后接 1013F_R2D2_CASE_REFERENCE_STRUCTURE_ASSIMILATION。
只做案例结构吸收和候选修正，不进入 1013G，不 formal apply，不写数据库/memory/Feishu。
模型默认用 MiniMax-M3 + thinking disabled；如需深度推演，显式说明再用 adaptive。
```
