# 1013D 课时设计推理字段模型

Stage: `1013D_LESSON_DESIGN_REASONING_FIELD_MODEL`

Status: `MODEL_READY_FOR_REVIEW`

Scope: `备课室 · 备课本 · 课时设计推理模型`

本阶段把 1013C 的查看态、编辑态、教学过程意图层继续往下收：一节课不是固定环节填空，而是围绕学生学习问题建立的一条解决链。小备以后不能先自由生成整篇教案，而要先形成一份课时设计判断，再生成可读正文和可确认候选。

## 1. 核心判断

一堂课的设计质量不来自“导入、探究、展示”这些标题，而来自这些问题是否被回答清楚：

```text
学生现在在哪里？
他们卡在哪里？
这节课要把他们带到哪里？
为什么用这个活动？
这一步之后学生应该发生什么变化？
老师此时怎样引导？
大屏、教材、材料、学习单什么时候出现？
怎样判断学生真的理解了？
如果没有发生预期变化，老师怎么调整？
```

因此备课本需要三层：

```text
查看态：老师读一份可上课的连续教学设计。
编辑态：老师围绕某一段或某一环节修改候选。
设计依据层：解释为什么这样设计，以及依据、学生状态、媒介和证据。
```

## 2. lesson_design_mode

`lesson_design_mode` 是备课程度字段。它决定小备生成深度、追问数量、资料调用量、设计说明展开程度和评价证据要求。

| 值 | 教师语言 | 系统处理 |
| --- | --- | --- |
| `quick_daily` | 快速日常课 | 能上即可，最多追问 1 个关键问题，少调用资料。 |
| `standard_daily` | 标准日常课 | 目标、流程、任务、评价基本完整，最多追问 2 个。 |
| `refined_lesson` | 精磨课 | 强化学情、问题串、材料、评价证据。 |
| `open_class` | 公开课 / 展示课 | 强化设计意图、课堂节奏、大屏状态、学生表达和证据沉淀。 |
| `research_lesson` | 研究课 | 强化问题意识、教学假设、证据链和课后分析。 |

教师可见时不要显示字段名，只显示：

```text
这节课按：快速 / 标准 / 精磨 / 公开课 / 研究课
```

## 3. lesson_design_brief

`lesson_design_brief` 是小备生成前的设计判断对象，不直接全部铺给老师。它可以在编辑态或“设计说明”中转成教师语言。

```json
{
  "lesson_design_mode": "",
  "core_learning_problem": "",
  "student_baseline": "",
  "target_shift": "",
  "unit_position": "",
  "curriculum_basis": [],
  "textbook_basis": [],
  "prior_learning_basis": [],
  "teacher_intent": "",
  "classroom_constraints": [],
  "resource_budget": "low | medium | high",
  "teaching_route": [],
  "evidence_plan": [],
  "risk_points": [],
  "next_best_questions": []
}
```

它的作用是防止生成漂移：

```text
先判断学习问题，再决定教学路径；
先判断学生起点，再决定活动难度；
先判断证据，再决定学习单和展示方式；
先判断现实约束，再决定课件、材料和追问深度。
```

## 4. teaching_step_reasoning

每个教学环节都需要一份推理结构：

```json
{
  "step_id": "",
  "step_name": "",
  "duration": "",
  "step_role": "",
  "design_intent": "",
  "student_state_before": "",
  "student_state_after": "",
  "teacher_action": "",
  "student_action": "",
  "big_screen_state": "",
  "textbook_or_material_state": "",
  "learning_sheet_state": "",
  "assessment_evidence": "",
  "transition_from_previous": "",
  "transition_to_next": "",
  "risk_and_adjustment": ""
}
```

本课默认五环节：

```text
导入：唤起经验，不急着讲概念。
感知：通过图片和作品建立色彩与感受的联系。
探究：让学生动手分类并说理由。
表现：把理解转成自己的色彩表达。
交流展示：让作品、说明和同伴反馈成为评价证据。
```

## 5. lesson_design_quality_gate

质量门不是为了卡老师，而是帮助小备知道“这节课是否已经能上”。

检查维度：

```text
curriculum_aligned
textbook_grounded
student_baseline_clear
target_shift_clear
teaching_route_coherent
step_intent_clear
teacher_action_operable
student_action_visible
big_screen_state_defined
material_timing_clear
assessment_evidence_defined
risk_adjustment_ready
not_too_easy
not_over_scope
```

质量等级：

```text
basic_usable：基础可用，能上，但依据和证据较轻。
ready_to_teach：可正常上课，目标、流程、任务、评价基本完整。
refined：学情、材料、问题串、评价证据都较清楚。
open_class_ready：适合公开课或教研展示，需要课堂节奏和证据链更强。
```

## 6. 小备追问策略

字段不足时，小备不能硬生成。追问顺序：

```text
1. 这节课按什么程度备？快速、标准、精磨、公开？
2. 学生现在主要卡在哪里？
3. 这节课更想让学生理解什么，还是表达什么？
4. 有没有必须使用的材料或图片？
5. 是否需要学习单？
6. 你希望用什么证据判断学生达成？
7. 课堂时间是否完整 40 分钟？
8. 是否有班级特殊情况？
```

追问数量：

```text
快速日常课：最多 1 个关键问题。
标准日常课：最多 2 个。
精磨课：最多 3 个。
公开课 / 研究课：可以 3-5 个。
老师始终可以选择“先按默认生成”。
```

## 7. 查看态 / 编辑态 / 设计依据层

查看态：

```text
只显示连续教学设计正文。
设计依据用轻标签和“查看设计说明”呈现。
不显示复杂字段表。
```

编辑态：

```text
可以展开设计简报摘要。
可以展开每个环节的设计说明。
可以修改某一段或某一环节。
可以查看影响范围。
所有候选等待老师确认。
```

设计依据层：

```text
显示教学依据、学生状态、环节作用、教师动作、大屏状态、材料状态、学习单状态、评价证据、风险调整。
不显示工程字段名。
```

## 8. 1-2《色彩的感觉》样例结论

本课的核心学习问题：

```text
学生知道很多颜色，也会说喜欢或不喜欢，但还不能稳定地把颜色、情绪、生活场景和作品表达联系起来。
```

目标变化：

```text
从“看到颜色”
到“说出颜色带来的感受”
再到“有意识地用色彩表达心情或场景”。
```

合理路径：

```text
生活感受 -> 图片与作品观察 -> 色卡/物品分类 -> 分层色彩表达 -> 作品说明与同伴反馈
```

质量边界：

```text
不能太简单：不能只让学生认识冷暖色。
不能超纲：不能变成专业色彩心理学或复杂配色理论。
应该稍有挑战：让学生说出理由，并把理由用到自己的表达里。
```

## 9. 本阶段边界

本阶段只落模型和轻量页面验证：

```text
不接真实 provider
不写数据库
不写 memory
不写 Feishu
不正式导出
不正式归档
不切默认入口
不生成复杂 ZIP
不继续市场检索
```

## 10. 配套文件

- `lesson_design_reasoning_model_1013D.json`
- `lesson_design_brief_sample_1013D.json`
- `teaching_step_reasoning_sample_1013D.json`
- `lesson_design_quality_gate_1013D.json`
- `xiaobei_question_strategy_1013D.json`
