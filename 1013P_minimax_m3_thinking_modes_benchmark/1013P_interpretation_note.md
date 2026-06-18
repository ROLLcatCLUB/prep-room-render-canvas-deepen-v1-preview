# 1013P Interpretation Note: MiniMax-M3 Thinking Modes

## What modes exist?

On the MiniMax OpenAI-compatible API path used here, the accepted `thinking.type` values are `disabled` and `adaptive`. Omitting `thinking` leaves M3 thinking on by default. The model page mentions `enabled`, but the live API rejected `thinking.type=enabled` with `invalid params` and allowed values `adaptive, disabled`.

## Usable Results On Lesson Patch Case

| Mode | Avg latency | Pass rate | Avg quality | Reasoning content | Best use |
|---|---:|---:|---:|---:|---|
| disabled | 18110.5ms | 1.0 | 3 | 0 | compact JSON, teacher-facing suggestions, low-latency UI response |
| adaptive | 18661.5ms | 1.0 | 4 | 735.5 | harder classroom reasoning where extra reasoning trace is useful and small latency increase is acceptable |
| omitted_default_on | 24569.5ms | 1.0 | 4 | 1235 | slower and one simple-json timeout in this sample; avoid implicit default because behavior is less explicit |

## Speed Difference

- Adaptive vs disabled on lesson patch: +551.0ms, +3.0% latency.
- Omitted default-on vs disabled on lesson patch: +6459.0ms, +35.7% latency.

## Recommendation

Default to disabled for current prep-room structured JSON. Use adaptive only for explicit deep reasoning stages. Do not send enabled on the current OpenAI-compatible API path. Do not omit thinking accidentally.
