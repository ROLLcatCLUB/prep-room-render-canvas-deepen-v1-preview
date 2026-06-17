# 1013E 课时推理过程流模块

Stage: `1013E_LESSON_REASONING_TRACE_MODULE`

Status: `LOCAL_TRACE_PREVIEW_READY`

Scope: `备课室 · 备课本 · 小备同步思考过程`

## 1. 目标

本阶段先实现一个轻量的推理过程流，让老师在等待小备处理时看到系统正在做哪一步，而不是盯着空白等待。

它服务于两个体验目标：

```text
减少等待焦虑；
让老师感到小备正在和自己同步思考。
```

但它不展示原始模型思维链，不展示 prompt，不展示工程字段，不展示内部接口名。教师可见的是“工作进度 + 教学判断摘要”。

## 2. 教师可见过程

当前静态预览采用 5 步：

```text
1. 先判断备课程度
2. 再看学生卡在哪里
3. 定位要改的位置
4. 检查依据和影响
5. 整理成候选
```

页面文案保持教师语言：

```text
小备正在同步思考
你刚才说：学生对冷暖色不太理解，要设计得更直观一点。
已定位到：学情分析、教学过程 · 探究环节、学习单与评价。
会影响三处：大屏、学习单、评价证据。
```

## 3. 内部对应关系

教师可见步骤对应内部 pipeline：

| 教师可见步骤 | 内部对应 |
| --- | --- |
| 先判断备课程度 | LessonModePolicy |
| 再看学生卡在哪里 | LessonReasoningRequest + IntentClassifier |
| 定位要改的位置 | PatchTargetResolver |
| 检查依据和影响 | SourceBasisResolver + ImpactScopeResolver |
| 整理成候选 | ReasoningPatchCandidate + ViewEditBindingHint |

这些内部名称不出现在教师界面，只用于工程实现和后续 1013E live model POC 对接。

## 4. 当前实现

当前 HTML 已实现本地静态流式预览：

```text
在备课本中输入一句话
-> 显示“小备正在同步思考”
-> 每约 650ms 推进一步
-> 最后进入编辑态
-> 显示探究环节候选和影响范围
```

新增直达入口：

```text
prep_room_render_canvas_deepen_v1.html#prepNotebookReasoning
```

该入口用于审核截图：直接打开推理过程已完成、候选已定位的状态。

## 5. 后续对接

当 1013E live model POC 跑通后，静态步骤可由真实事件驱动：

```text
request_started
mode_policy_done
basis_resolved
intent_classified
target_resolved
impact_resolved
candidate_ready
ui_binding_ready
```

前端仍只显示教师可读文案，不显示原始模型输出和内部事件名。

## 6. 边界

本阶段明确不做：

```text
不接真实 provider
不展示原始模型思维链
不写数据库
不写 memory
不写 Feishu
不 formal apply
不正式导出
不正式归档
不切默认入口
不做大 ZIP
```

## 7. 完成标记

```text
1013E_LESSON_REASONING_TRACE_MODULE_COMPLETE
NEXT_STAGE=1013E_MODEL_PROMPT_TO_REASONING_FIELD_PATCH_POC
```
