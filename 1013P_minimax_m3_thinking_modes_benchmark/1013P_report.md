# 1013P MiniMax-M3 Thinking Modes Benchmark

- FINAL_STATUS: `PASS_MINIMAX_M3_THINKING_MODES_BENCHMARK`
- Repeats per mode per case: `2`
- Fastest mode: `enabled_probe`
- Best quality mode: `adaptive`

## Thinking Modes Tested

- `disabled`: sends `thinking: {"type":"disabled"}`.
- `adaptive`: sends `thinking: {"type":"adaptive"}`.
- `omitted_default_on`: omits `thinking`; MiniMax docs say M3 thinking is on by default.
- `enabled_probe`: sends `thinking: {"type":"enabled"}` to verify whether the live API accepts the model-page third mode.

## Overall

| Mode | Calls | Avg latency | Median latency | Pass rate | Avg quality | Avg reasoning length | Avg completion tokens |
|---|---:|---:|---:|---:|---:|---:|---:|
| disabled | 4 | 10151.2ms | 10198.0ms | 0.75 | 1.5 | 0 | 245.2 |
| adaptive | 4 | 9899ms | 8559.0ms | 0.75 | 2 | 389.8 | 285.2 |
| omitted_default_on | 4 | 42446.2ms | 24569.5ms | 0.5 | 2 | 617.5 | 381.8 |
| enabled_probe | 4 | 1286.5ms | 473.5ms | 0.0 | 0 | 0 | 0 |

## By Case

### lesson_patch_reasoning

| Mode | Avg latency | Pass rate | Avg quality | Avg reasoning length |
|---|---:|---:|---:|---:|
| disabled | 18110.5ms | 1.0 | 3 | 0 |
| adaptive | 18661.5ms | 1.0 | 4 | 735.5 |
| omitted_default_on | 24569.5ms | 1.0 | 4 | 1235 |
| enabled_probe | 2099.5ms | 0.0 | 0 | 0 |

### simple_json

| Mode | Avg latency | Pass rate | Avg quality | Avg reasoning length |
|---|---:|---:|---:|---:|
| disabled | 2192ms | 0.5 | 0 | 0 |
| adaptive | 1136.5ms | 0.5 | 0 | 44 |
| omitted_default_on | 60323ms | 0.0 | 0 | 0 |
| enabled_probe | 473.5ms | 0.0 | 0 | 0 |

## Interpretation

Use disabled thinking when the required output is compact JSON or low-latency teacher-facing suggestions. Use adaptive/default thinking only when a later stage explicitly needs deeper reasoning and can tolerate extra latency and reasoning-token budget. The enabled_probe result is empirical and should not override the official OpenAI-compatible docs if the API rejects it in other environments.

## Boundary

- Provider/model calls were made for benchmark only.
- No lesson text was formally applied.
- No database, memory, or Feishu write was performed.
