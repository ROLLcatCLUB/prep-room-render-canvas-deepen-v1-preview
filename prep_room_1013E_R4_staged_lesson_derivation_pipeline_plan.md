# 1013E_R4 分阶段课时推演 Pipeline 策略

```text
decision=STOP_COMPETITOR_RESEARCH_FOR_NOW
status=SHIFT_TO_INTERNAL_STRATEGY_AND_SYSTEM_REFINEMENT
next_stage=1013E_R4_STAGED_LESSON_DERIVATION_PIPELINE
```

## 核心判断

调研报告已经回答战略问题：

```text
普通 AI 备课 = 快速生成教案文本
师维 / 小备 = 从依据到课堂行动的推演协作系统
```

因此 1013E_R4 不继续横向竞品分析，也不继续硬压一次性 prompt。R2、R3 的失败说明：一次调用生成完整 `lesson_unfolding_graph` 不稳定。R4 改为分阶段推演：

```text
LessonContextPack
→ LearningProblemDeriver
→ TargetShiftDeriver
→ EvidencePlanDeriver
→ TeachingRoutePlanner
→ ClassroomEventGenerator
→ EventUnfoldingExpander
→ TimeRebalancer
→ EvidenceBinder
→ EffectivenessEvaluator
→ TeacherReviewCandidate / CandidateError
```

## 产品边界

- 先跑稳后端推演链，不接 UI。
- 案例只做校准、教师语言样本、资源使用方式和质量门参考，不做范文套用。
- 每一步都必须有明确输入输出，可以单独失败。
- 失败进入 `candidate_error`，不得用空默认值伪装成功。
- 不得 formal apply，不得写 database / memory / Feishu。

## R4 通过标准

- 3 个核心案例至少 2 个完整 pass。
- `standard_daily_cold_warm_more_visual` 必须 pass。
- 通过案例必须生成 learning problem、target shift、classroom events、evidence binding。
- 通过案例必须通过 time rebalance 或给出明确 rebalance candidates。
- 通过案例必须 `teacher_review_required=true`，`formal_apply_performed=false`。
- 无 key 泄露，无数据库 / memory / Feishu 写入，不接 UI。
