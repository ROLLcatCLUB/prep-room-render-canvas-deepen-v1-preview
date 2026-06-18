# 1013O Multi-Round Benchmark: MiniMax-M3 vs MiniMax-M2.7-highspeed

- FINAL_STATUS: `PASS_MINIMAX_M3_VS_M27_HIGHSPEED_MULTI_ROUND_BENCHMARK`
- Repeats per model per case: `3`
- Winner by average latency: `MiniMax-M3`
- Winner by pass rate: `MiniMax-M3`

## Overall

| Model | Calls | Avg latency | Median latency | Pass rate | Avg quality |
|---|---:|---:|---:|---:|---:|
| MiniMax-M3 | 9 | 7544.4ms | 7451ms | 1.0 | 2.44 |
| MiniMax-M2.7-highspeed | 9 | 16669.4ms | 16356ms | 1.0 | 1.78 |

Overall speed delta: M3 faster by `9125.0ms` on average; M2.7-highspeed is `2.21x` of M3 average latency.

## By Case

### lesson_patch_micro

| Model | Avg latency | Median latency | Pass rate | Avg quality |
|---|---:|---:|---:|---:|
| MiniMax-M3 | 13479ms | 12725ms | 1.0 | 4.33 |
| MiniMax-M2.7-highspeed | 25050.3ms | 23608ms | 1.0 | 2.33 |

Speed delta: M3 faster by `11571.3ms`; M2.7-highspeed is `1.86x` of M3.

### simple_json_exact

| Model | Avg latency | Median latency | Pass rate | Avg quality |
|---|---:|---:|---:|---:|
| MiniMax-M3 | 1216.7ms | 1014ms | 1.0 | 0 |
| MiniMax-M2.7-highspeed | 9647ms | 7291ms | 1.0 | 0 |

Speed delta: M3 faster by `8430.3ms`; M2.7-highspeed is `7.93x` of M3.

### teacher_note_micro

| Model | Avg latency | Median latency | Pass rate | Avg quality |
|---|---:|---:|---:|---:|
| MiniMax-M3 | 7937.7ms | 7451ms | 1.0 | 3 |
| MiniMax-M2.7-highspeed | 15311ms | 14320ms | 1.0 | 3 |

Speed delta: M3 faster by `7373.3ms`; M2.7-highspeed is `1.93x` of M3.

## Interpretation

Across this multi-round sample, M3 should be judged on both latency and usable structured output. If the pass rate stays close while M3 latency is lower, use M3 by default; if a later larger benchmark reverses this, keep model routing configurable.

## Boundary

- Provider/model calls were made for benchmark only.
- No lesson text was formally applied.
- No database, memory, or Feishu write was performed.
