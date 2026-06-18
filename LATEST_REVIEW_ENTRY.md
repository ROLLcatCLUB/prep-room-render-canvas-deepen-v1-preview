# Latest Review Entry

```text
REVIEW_STAGE=1013P_MINIMAX_M3_THINKING_MODES_BENCHMARK
FINAL_STATUS=PASS_MINIMAX_M3_THINKING_MODES_BENCHMARK
DEFAULT_RECOMMENDATION=MiniMax-M3_WITH_THINKING_DISABLED
DEEP_REASONING_OPTION=MiniMax-M3_WITH_THINKING_ADAPTIVE
FORMAL_APPLY_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Summary

This stage compares `MiniMax-M3` with different `thinking` settings.

MiniMax OpenAI-compatible API behavior observed in this environment:

```text
thinking.type=disabled -> accepted
thinking.type=adaptive -> accepted
thinking omitted -> thinking is on by default
thinking.type=enabled -> rejected by live API
```

The live API rejection for `enabled` returned:

```text
invalid params, invalid thinking.type: "enabled" (allowed: adaptive, disabled)
```

So for the current OpenAI-compatible path, the usable explicit modes are:

```text
disabled
adaptive
```

## Lesson Patch Case

The most relevant case is `lesson_patch_reasoning`.

```text
disabled:
  avg_latency = 18110.5ms
  pass_rate = 1.0
  avg_quality_score = 3
  reasoning_content = none

adaptive:
  avg_latency = 18661.5ms
  pass_rate = 1.0
  avg_quality_score = 4
  avg_reasoning_content_length = 735.5

omitted_default_on:
  avg_latency = 24569.5ms
  pass_rate = 1.0
  avg_quality_score = 4
  avg_reasoning_content_length = 1235
```

Speed difference on the lesson-patch case:

```text
adaptive vs disabled = +551.0ms / +3.0%
omitted default-on vs disabled = +6459.0ms / +35.7%
```

## Recommendation

Use `MiniMax-M3` with:

```json
{"thinking":{"type":"disabled"}}
```

for current prep-room structured JSON, field patches, UI candidates, and teacher-facing suggestions.

Use:

```json
{"thinking":{"type":"adaptive"}}
```

only when a stage explicitly needs deeper reasoning and can tolerate extra reasoning tokens and latency.

Do not send `thinking.type=enabled` on the current OpenAI-compatible API path. Do not omit the `thinking` field accidentally, because omission turns thinking on by default and was slower in this sample.

## Boundary

Provider/model calls were made only for benchmark comparison. No lesson text was formally applied. No database, memory, or Feishu write was performed. The main project was not committed or pushed.
