# 1013N MiniMax M3 vs M2.7-highspeed Comparison

- FINAL_STATUS: `PASS_MINIMAX_M3_VS_M27_HIGHSPEED_COMPARISON`
- Winner: `MiniMax-M3`
- Scope: two live read-only model calls per model, no DB/memory/Feishu write, no formal apply.

## Scores

- `MiniMax-M3`: 12
- `MiniMax-M2.7-highspeed`: 9

## Case Summary

- `MiniMax-M3` / `json_probe`: latency `1012ms`, strict_json `True`, contract `n/a`, quality `n/a`
- `MiniMax-M2.7-highspeed` / `json_probe`: latency `3893ms`, strict_json `True`, contract `n/a`, quality `n/a`
- `MiniMax-M3` / `lesson_reasoning_standard_daily`: latency `34776ms`, strict_json `True`, contract `True`, quality `4`
  - issues: missing_resource_timing, missing_risk_adjustment, forbidden_terms:formal_apply
- `MiniMax-M2.7-highspeed` / `lesson_reasoning_standard_daily`: latency `62293ms`, strict_json `True`, contract `False`, quality `5`
  - issues: missing_explore_patch, missing_explore_step_update

## Interpretation

For this prep-room structured reasoning sample, compare strict JSON first, then contract coverage, then teacher-readable quality. M3 contract_pass=True and quality=4; M2.7-highspeed contract_pass=False and quality=5.

## Boundary

- Provider/model calls were made for comparison only.
- No formal lesson text was applied.
- No database, memory, or Feishu write was performed.
