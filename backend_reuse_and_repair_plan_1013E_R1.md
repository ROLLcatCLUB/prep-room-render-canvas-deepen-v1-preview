# 1013E_R1 Backend Reuse And Repair Plan

```text
decision=REUSE_WITH_REPAIR
status=1013E_R1_BACKEND_FOUNDATION_REVIEW_READY
next_stage=1013E_R1_PROMPT_REPAIR_AND_READONLY_REASONING_PIPELINE
```

## Current Goal

备课本后端不是为了“生成一整篇教案”，而是把老师一句话转成：

```text
教学判断
-> 修改位置
-> 依据与学生状态
-> 环节设计意图
-> 候选补丁
-> 影响范围
-> 教师确认
-> 查看态 / 编辑态绑定
```

因此旧后端可以复用，但不能为了复用而降级成通用聊天、通用填字段或排课规则引擎。

## Reuse Directly

### Provider Transport

文件：

- `backend/xiaobei_ai/providers.py`

用途：

- 继续作为低层模型调用适配器。
- 继续使用已有 provider status、凭据来源判断、超时和脱敏元数据。

不能让它承担：

- 备课本 schema。
- 教学环节推理。
- 质量门判断。
- 查看态 / 编辑态绑定。

判断：

```text
reuse_level=direct_low_level
repair_needed=wrap_by_lesson_reasoning_contract
```

### Strict Output Parser

文件：

- `backend/xiaobei_ai/output_parser.py`
- `backend/xiaobei_ai/controlled_json_extractor.py`

用途：

- 复用严格 JSON 解析。
- MiniMax `<think>` 前缀只能走已有受控抽取，不再用脚本里宽松截取首尾花括号的方式。

本次已改：

- 新增 `backend/xiaobei_ai/prep_room_lesson_reasoning_contract_1013E.py`。
- `scripts/run_prep_room_1013e_model_prompt_to_reasoning_field_patch_poc.py` 已改为调用 `parse_lesson_reasoning_output()` 和 `validate_lesson_reasoning_payload()`。
- 删除了脚本内部临时 `extract_json()` 和重复 `validate_result()`。

判断：

```text
reuse_level=direct
repair_done=1013E_contract_and_parser_binding
```

### Feishu Schedule Adapter

文件：

- `backend/xiaobei_ai/prep_room_feishu_schedule_1013A.py`

用途：

- 只读读取正式课表或本地快照。
- 给备课本提供教师、年级、班级、课位和当前课题入口。

不能让它承担：

- 教学设计依据。
- 学生学情推理。
- 教案生成。
- 飞书写回。

判断：

```text
reuse_level=direct_context_source
boundary=readonly_only
```

## Reuse With Adaptation

### Visible Reasoning Trace

文件：

- `backend/xiaobei_ai/teaching_planning_run_trace_0998G.py`

可吸收：

- 面向老师的可见动作流。
- 等待过程中的步骤状态。
- “正在读上下文 / 查缺口 / 定动作 / 同步预览”这类轻量进度表达。
- 不展示原始模型推理、不展示系统提示词、不展示 provider payload。

必须改造：

- 从“教学规划产物”改成“课时教学设计推理”。
- 步骤应变成：

```text
判断备课程度
读取当前课题与资料
定位学生理解卡点
定位要改的段落或环节
检查依据与影响范围
整理候选修改
等待老师确认
```

判断：

```text
reuse_level=pattern_only
new_module_needed=prep_room_lesson_reasoning_trace_1013E_R1
```

### Semantic Orchestrator

文件：

- `backend/xiaobei_ai/system_semantic_interaction_runtime/orchestrator.py`
- `backend/xiaobei_ai/system_semantic_interaction_runtime/side_effect_gate.py`
- `backend/xiaobei_ai/system_semantic_interaction_runtime/renderer_patch_contract.py`

可吸收：

- domain adapter 思路。
- 副作用闸门。
- renderer patch plan。
- 候选同步到前端前先归一化。

不能直接复用：

- 当前 orchestrator 的动作粒度偏通用，不能表达备课本里的环节意图、学习单、大屏、评价证据、学情依据。
- 当前 renderer patch contract 只有 `patches`，不够表达查看态 / 编辑态 / 候选卡 / 右侧辅助栏 / 流式进度。

必须改造：

```text
LessonModePolicy
SourceBasisResolver
LessonIntentClassifier
PatchTargetResolver
TeachingStepIntentResolver
ImpactScopeResolver
QualityGateEvaluator
QuestionStrategy
ViewEditBindingHint
VisibleReasoningTrace
```

实现方式：

第一版集中成一个内部 pipeline，不拆成多个服务。

判断：

```text
reuse_level=architecture_pattern
repair_needed=lesson_specific_pipeline
```

### Teaching Planning Candidate Modules

文件：

- `backend/xiaobei_ai/teaching_planning_precision_candidate_0998K.py`
- `backend/xiaobei_ai/teaching_planning_precision_candidate_repair_0998L.py`
- `backend/xiaobei_ai/teaching_planning_resource_adapter_0998J.py`

可吸收：

- 只读候选。
- 现有候选的局部修改。
- 资源缺口提示。
- 不写库、不写记忆、不正式导出。

不能直接复用：

- 它们是排课/周历规则型候选，不理解一堂课里每个环节的教学作用。
- 不能用它们的简单规则替代教学设计判断。

判断：

```text
reuse_level=workflow_pattern
repair_needed=lesson_candidate_shape
```

## Do Not Reuse For This Step

### Generic Workbench Agent Runtime

文件示例：

- `backend/xiaobei_ai/workbench_agent_runtime.py`
- `backend/xiaobei_ai/workbench_intent_router.py`
- `backend/xiaobei_ai/workbench_task_object_memory.py`

原因：

- 当前备课本目标很窄，先要稳定课时设计 pipeline。
- 过早接入通用 agent runtime 会把边界变宽，容易出现多业务串线。

判断：

```text
reuse_now=false
reason=too_broad_for_1013E_R1
```

### Memory Modules

原因：

- 当前还没有真实学生档案、课堂反馈和教师偏好正式接入。
- 1013E_R1 只能显示“小备推测 / 教学预设 / 资料依据”，不能写 memory，也不能声称读取了不存在的学生长期记录。

判断：

```text
reuse_now=false
boundary=memory_write_false
```

## New Backend Contract Added

文件：

- `backend/xiaobei_ai/prep_room_lesson_reasoning_contract_1013E.py`

它现在负责：

- 固定真实课题上下文：三年级美术 1-2《色彩的感觉》。
- 固定输出结构：lesson design brief、teaching step reasoning、field patch candidates、impact scope、quality gate、teacher questions、UI binding hint。
- 固定安全边界：teacher review required，no formal apply，no database，no memory，no Feishu write，no formal export，no archive。
- 复用已有 strict parser。
- 校验模型输出是否真的能映射到备课本。

## Next Engineering Plan

### 1. Prompt Repair

目标：

```text
1013E_R1_PROMPT_REPAIR
```

做法：

- 不再一次塞完整 schema + 过多 source context。
- 每次只测一个 `lesson_design_mode`。
- 输出从“大 JSON”压缩为：

```text
lesson_design_brief_compact
target_resolution
step_reasoning_updates
field_patch_candidates
impact_scope
quality_gate_update
ui_binding_hint
boundary_flags
```

### 2. Lesson Reasoning Pipeline

新增内部函数：

```text
run_prep_room_lesson_reasoning_pipeline(input)
```

第一版仍然只读，返回结构化结果和可见进度，不写任何正式对象。

### 3. Visible Progress Stream

借鉴 `0998G`，但新建备课本专用 trace：

```text
prep_room_lesson_reasoning_trace_1013E_R1
```

老师看到的是：

```text
我在判断这节课要解决的学习卡点
我定位到教学过程 · 探究环节
我在检查会影响大屏、学习单和评价证据
我整理成两处候选，等你确认
```

不是：

```text
schema
provider
field_patch
database
memory
formal_apply
```

### 4. Readonly Route Later

等 prompt repair 稳定后，再接只读路由：

```text
POST /api/xiaobei/prep-room/lesson-reasoning
```

边界：

- 可调用 provider。
- 可返回候选。
- 可返回可见进度。
- 不写库。
- 不写 memory。
- 不写 Feishu。
- 不 formal apply。
- 不正式归档。

## Conclusion

后端不是从零开始，已有底座能用。但本轮不能把教学规划、排课候选或通用 workbench runtime 硬套到备课本。

正确路线是：

```text
复用 provider / parser / readonly boundary / trace 思想
新建备课本 lesson reasoning contract
再做 1013E_R1 prompt repair
最后接只读 pipeline 和前端编辑态绑定
```

