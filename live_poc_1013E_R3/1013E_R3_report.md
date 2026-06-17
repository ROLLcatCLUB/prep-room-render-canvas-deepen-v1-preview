# 1013E_R3 Lesson Unfolding Graph Normalizer And Effectiveness Eval

```text
final_status=FAIL_STANDARD_DAILY_REPAIR
next_stage=1013E_R4_MODEL_STRATEGY_ADJUSTMENT
strict_or_wide_parse_success_count=3/6
normalization_success_count=3/6
contract_validation_success_count=2/6
effectiveness_pass_count=2/6
boundary_ok_count=3/6
secret_scan_ok=true
```

## Case Results

| case_id | parse | normalized | contract | effectiveness | boundary |
| --- | --- | --- | --- | --- | --- |
| `standard_daily_cold_warm_more_visual` | false | false | false | false | false |
| `standard_daily_art_music_dance_rhythm` | false | false | false | false | false |
| `quick_daily_basic_design` | true | true | true | true | true |
| `open_class_question_expression_evidence` | false | false | false | false | false |
| `research_lesson_color_feeling_transition` | true | true | false | false | true |
| `constrained_low_resource_no_video` | true | true | true | true | true |

## classroom_unfolding_script_result

- Generated through `lesson_unfolding_graph.classroom_events`.
- Each event separates execution view, design view, response model, resource use, duration, and boundary flags.

## classroom_unfolding_effectiveness_eval

- Evaluates resource purpose, attention focus, teacher guidance, student response prediction, scaffold quality, collection/evidence, media/material timing, transition, time feasibility, and age appropriateness.

## dance_rhythm_case_result

- The dance/rhythm case is treated only as a teacher-provided classroom event request, not as a default resource inserted into unrelated lessons.

## Boundary

- Provider may be called for six cases.
- No database write.
- No memory write.
- No Feishu write.
- No formal apply.
- No official export.
- No official archive.
- No UI binding.
- Requests and responses are redacted in trace outputs.
