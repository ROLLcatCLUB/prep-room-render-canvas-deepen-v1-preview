# 1013F R2D 内容审查与案例参考吸收闸门

- FINAL_STATUS: `PASS_CONTENT_REVIEW_WITH_CASE_REFERENCE_STRUCTURE_ONLY`
- NEXT_STAGE: `1013F_R2D2_CASE_REFERENCE_STRUCTURE_ASSIMILATION`
- Boundary: no provider/model call, no Feishu/database/memory write, no formal apply, no 1013G.

## 结论

当前 R2C 的课堂展开已经像一节可上、可读、可改的三年级美术常态课。R2D 不建议继续堆字数；建议只做轻修：压缩探究材料复杂度、降低表现任务起步门槛、把展示评价收束到可观察证据。

## 内容审查

- 年段适配: `PASS_WITH_MINOR_REPAIR` - 任务围绕看色、分色、说理由和小练习，三年级能做；但教师话术仍要避免一次给太多抽象词。
- 美术学科真实性: `PASS` - 课堂主线围绕色彩感受、作品观察、色卡分类和色彩表达，没有偏离到泛泛讨论。
- 课堂节奏: `NEEDS_LIGHT_REPAIR` - 5个环节总时长合理，但探究、表现、展示都承载了较多任务，真实课堂需要给材料分发、收束和展示留机动时间。
- 教师话术自然度: `PASS_WITH_MINOR_REPAIR` - 已有可说出口的话术；个别总结句仍偏完整书面化，可再压成短句和追问。
- 学生反应真实性: `PASS_WITH_MINOR_REPAIR` - 已经写到学生可能只说好看、按颜色名称分类、说不清理由；还可以补一个低水平回答样例和教师即时追问。
- 评价证据可观察性: `PASS` - 证据落在口头理由、色卡分类、学习单三格、作品和一句话说明，教师能在课堂中看见或收集。
- 过渡自然度: `PASS` - 导入到感知、感知到探究、探究到表现、表现到展示均有承接语和学习任务变化。

## 本地参考结论

本地知识库没有找到完全同题 1-2《色彩的感觉》的高质量完整课例；但找到若干可用于 R2D 校准的同年段/相近色彩课例。它们只用于结构、节奏、材料和评价证据参考，不直接吸收文本。

- `kb_art_g3_lesson_case_1_fd1b5bdf60.txt`: 三年级色彩课的课堂节奏、工具选择、展示评价与可观察成功标准；吸收级别 `grade_calibration_and_teaching_moves_only`。
- `kb_art_g3_lesson_case_1_08f3e01f0b.txt`: 三年级色彩感受课的观察、表达、轻学习单和材料准备；吸收级别 `grade_calibration_and_material_flow_only`。
- `kb_art_g3_upper_official_lesson_design_unit_02_afb83c9f5c.txt`: 官方三年级色彩单元的学情、基本问题和目标校准；吸收级别 `official_goal_calibration_only`。
- `kb_art_g3_lesson_case_lesson_8974535734.txt`: 三年级色彩单元的大概念、分层任务和单元承接风险；吸收级别 `unit_structure_and_risk_check_only`。
- `kb_art_g4_lesson_case_2_688deacf81.txt`: 色彩感受与自然图片对比的课堂组织，上限参照，需降阶；吸收级别 `upper_bound_reference_only`。
- `kb_art_g4_lesson_case_1_dc37d1bb1e.txt`: 色彩对比课中的直观实验、学生兴奋点和概念风险，上限参照，需降阶；吸收级别 `upper_bound_reference_only`。

## 问题清单

- 教学过程 · 探究 / time_and_material_flow: 色卡、生活物品、记录单同时进入，10分钟内如果分发和收束不清楚，容易挤压理由表达。 建议：把生活物品降为可选，主材料先用色卡；记录单只写一行理由。
- 教学过程 · 表现 / task_load: 基础、进阶、挑战三层是对的，但教师如果同时讲三层标准，学生可能先听复杂了。 建议：默认先说基础任务，再给提前完成的学生打开进阶和挑战。
- 教学过程 · 交流展示 / time_risk: 5分钟展示两三件作品可行，但如果还要同伴反馈和教师归纳，可能超时。 建议：固定展示一件清楚、一件待调整；同伴只回答一个问题。
- 全课话术 / ai_like_complete_sentence: 个别总结句完整但略像教案书面语，课堂上可拆成短句和追问。 建议：保留教师可执行短句，把理论判断放到旁注而不是口头全说。

## 候选修正

- 教学过程 · 探究: 探究时先只发色卡。每组把色卡放到“温暖、清凉、安静、热烈”四个词旁边，再选一张最有把握的色卡说理由。生活物品作为加料材料，只给已经能说出理由的小组使用。
- 教学过程 · 表现: 先让全班完成基础任务：用2-3种颜色表现一种感受。提前完成的学生再选择进阶：加一个小场景；挑战：补一句“我这样配色是因为……”。
- 教学过程 · 交流展示: 展示一件“颜色和感受关系清楚”的作品，再展示一件“还可以调整”的作品。每次只问一个问题：“你从哪一种颜色读到了这种感觉？”

## 边界

- 候选修正不写回 HTML 正文。
- 案例参考不复制原文。
- 保持 R2B2/R2C 的阅读布局、右侧辅助区和编辑气泡机制。
