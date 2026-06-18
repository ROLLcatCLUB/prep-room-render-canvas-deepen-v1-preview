# 1013N Speed Note: MiniMax-M3 vs MiniMax-M2.7-highspeed

| Case | MiniMax-M3 | MiniMax-M2.7-highspeed | M3 faster by | M3 latency reduction vs M2.7 | M2.7 / M3 ratio |
|---|---:|---:|---:|---:|---:|
| json_probe | 1012ms | 3893ms | 2881ms | 74.0% | 3.85x |
| lesson_reasoning_standard_daily | 34776ms | 62293ms | 27517ms | 44.2% | 1.79x |

Conclusion: In this measured sample, M3 is faster on both simple JSON and prep-room reasoning. It also passed the compact contract in the prep-room reasoning case, so M3 remains the recommended default.

