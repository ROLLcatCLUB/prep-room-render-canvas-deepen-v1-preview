# 1013E_R4 Staged Lesson Derivation Pipeline

```text
final_status=PASS_STAGED_LESSON_DERIVATION_PIPELINE
next_stage=1013F_REASONING_FIELD_PATCH_TO_VIEW_EDIT_UI_BINDING
pipeline_pass_count=3/3
standard_daily_pass=true
secret_scan_ok=true
```

## Case Results

| case_id | pipeline | learning_problem | target_shift | events | evidence | time |
| --- | --- | --- | --- | --- | --- | --- |
| `standard_daily_cold_warm_more_visual` | true | true | true | true | true | true |
| `standard_daily_art_music_dance_rhythm` | true | true | true | true | true | true |
| `constrained_low_resource_no_video` | true | true | true | true | true | true |

## Strategy

- R4 stops one-call full lesson graph generation.
- R4 uses staged derivation: context, learning problem, target shift, evidence, route, classroom events, event unfolding, time rebalance, evidence binding, effectiveness evaluation.
- This implementation is local rule-based staged derivation first, so provider/model are not called in R4.
- Local cases are treated as reference candidates only, not authoritative templates.

## Boundary

- No UI binding.
- No database write.
- No memory write.
- No Feishu write.
- No formal apply.
- No official export.
- No official archive.
- No real knowledge-base retrieval.
- No raw model output is sent to frontend.
