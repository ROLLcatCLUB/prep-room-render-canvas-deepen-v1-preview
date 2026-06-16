# 备课本右侧备课栏资料整理 V0

生成日期：2026-06-16  
适用页面：`prep_room_render_canvas_deepen_v1.html` / `备课室 · 备课本`  
用途：给后续 GPT 继续设计右侧备课栏内容，不直接接 API、不写数据库、不改正式系统。

## 1. 一句话结论

右侧备课栏不应只是“资源列表”，也不应变成大聊天框。

它更适合定义为：

```text
本课备课辅助栏 =
小备建议
+ 本课材料夹
+ 可调用资料
+ 教师审核门
+ 待沉淀入口
```

当前备课本中间主区域负责“本课正在做什么”，右侧栏负责“这节课还能调用什么、缺什么、下一步让小备做什么、哪些内容需要教师确认”。

## 2. 已查阅的原系统资料

| 来源 | 路径 | 可复用点 |
| --- | --- | --- |
| 小备角色边界 | `docs/agent_profiles/sanitized_xiaobei_role_profile_068A.json` | 小备是“备课与教学设计协作助手”，必须 preview/candidate、教师确认优先、信息不足先追问 |
| 小备完整落地计划 | `docs/roadmap/小备系统完整落地总计划_v1_2026-04-21.md` | `prep_package` 是单课最终交付对象，承接基础、执行、资源、反思 |
| 备课底座 Schema | `docs/roadmap/备课底座_schema_v1_2026-04-21.md` | L1/L2/L3/L4 四层备课包字段，可直接映射右侧栏 |
| 旧 prep-workbench-v2 发现报告 | `docs/audit/xiaobei_prep_workbench_v2_base_discovery_20260518.md` | 旧系统的强项是“语义编排、会追问、整合上传资料/右侧字段/知识库上下文” |
| 小备基础底座审计 | `docs/audit/xiaobei_foundation_alignment_audit_20260518.md` | 明确指出缺少 `material_tray` 是短板，不能继续只做长文生成 |
| 课时设计业务模块 | `docs/foundation/lesson_design_business_module_schema_0948C.json` | 课时设计输入槽、缺失追问、输出字段、质量门 |
| 课时设计 ViewModel 映射 | `docs/foundation/lesson_design_viewmodel_mapping_candidate_0948C.md` | 可渲染区块：input_summary、missing_slots、lesson_design_candidate、quality_gate_results、risk_flags、next_actions |
| 资源收集业务模块 | `docs/foundation/resource_collection_business_module_schema_0948J.json` | 资源候选、来源类别、版权风险、知识库候选边界 |
| 资源收集 ViewModel 映射 | `docs/foundation/resource_collection_viewmodel_mapping_candidate_0948J.md` | header、resource_types、roles、keywords、source_categories、risks、risk_flags |
| 美术课时模板 | `subject_packs/art/lesson_templates/art_lesson_design_template_0954E.json` | 美术课时结构：topic_context、student_baseline、learning_objectives、classroom_flow 等 |
| 美术评价量规 | `subject_packs/art/rubrics/art_rubric_schema_0954E.json` | 构图、色彩、材料、技法、创意、过程性评价 |
| 字段资源注册 | `backend/xiaobei_ai/business_field_resource_registry_0998H.py` | 字段依赖资源、缺口提示、推荐追问、只读边界 |
| 资源适配器 | `backend/xiaobei_ai/teaching_planning_resource_adapter_0998J.py` | 接收老师粘贴/右侧上传/运行字段；缺资源时生成教师可见下一步 |
| 预览工作对象 | `backend/xiaobei_ai/xiaojiao_preview_sandbox_store_1009H.py` | 已有 `lesson_design_L003` 和 `handout_L003` 工作对象示例 |
| 美术备课核心包 | `samples/xiaojiao_teacher_business_object_model_1012B/art_teacher_prep_core_pack_v1_1012B.json` | work objects：lesson_design、lesson_section、handout、rubric、resource_reference、evidence_note、teacher_review_gate |
| 真实/解析资料 | `knowledge-base/_parsed/`、`knowledge-base/lesson-cases/` | 三、四年级美术课例、青绿内容、教材图片等，可作为资料室候选 |

## 3. 右侧栏应继承的核心对象

### 3.1 `prep_package`

原系统把 `prep_package` 定为单课真相源。右侧栏应围绕它，而不是另起一套“备课栏字段”。

建议右侧栏读取或展示这些层：

```text
prep_package
├─ l1_basic              基础小备：作业要求、核心活动、评价维度
├─ l2_lesson_execution   课堂执行：目标、重难点、流程、操作规范、成功标准
├─ l3_resource_collab    资源协作：PPT、学习单、素材、材料、给小美说明
└─ l4_reflection         课后反思：课堂记录、作品反馈、下次调整
```

### 3.2 备课本右栏应优先承载的工作对象

来自 `art_teacher_prep_core_pack_v1_1012B`：

```text
lesson_design        课时设计
lesson_section       课堂环节
handout              学习单
rubric               评价量规
resource_reference   资源参考
evidence_note        证据记录
teacher_review_gate  教师审核门
```

这些对象与当前页面里的状态可以对应：

| 当前页面状态 | 后续对象 |
| --- | --- |
| 课时设计待确认 | `lesson_design` + `teacher_review_gate` |
| 学习单已有候选 | `handout` |
| 评价量规未生成 | `rubric` |
| 资源参考待选择 | `resource_reference` |
| 课堂记录暂无 | `evidence_note` / `l4_reflection` |

## 4. 右侧栏内容结构建议

### 4.1 模块一：小备建议

用途：告诉老师“这节课现在最应该处理什么”。

建议字段：

```json
{
  "assistant": "xiaobei",
  "suggestion_type": "next_best_action",
  "current_task": "lesson_design",
  "blocking_gap": "学习单候选待确认",
  "reason": "课前包需要学习单和评价量规才能进入课前确认",
  "actions": ["确认学习单", "生成量规", "稍后处理"],
  "requires_teacher_confirmation": true
}
```

显示方式：

```text
小备建议
- 先确认学习单候选
- 再生成评价量规
- 课前包确认后，可推送到周课表
```

注意：小备建议不应显示成“已替你完成”，只能显示“候选 / 待确认 / 可处理”。

### 4.2 模块二：本课材料夹

用途：本节课真正要用的材料状态，不等同于资料室。

建议项目：

```text
课时设计
学习单
评价量规
资源参考
材料工具
板书 / PPT
课堂活动卡
课堂记录
```

建议状态字典：

```text
missing       未生成
candidate     已有候选
pending       待确认
confirmed     已确认
needs_update   需更新
archived      已沉淀
```

建议 UI：小圆点状态 + 名称 + 一个圆形操作按钮。不要长段文字。

### 4.3 模块三：可调用资料

用途：从资料室/知识库候选里给当前课调用，但不正式入库。

来源类别可来自 0948J：

```text
课标依据
教材资料
优秀课例
图片素材
视频 / 作品样例
材料工具说明
评价语 / 量规模板
校本资料
```

建议展示：

```text
可调用资料
- 苏少版三年级色彩单元课标摘要
- 冷暖色图片素材 12 张
- 优秀课例《色彩的感觉》2 个
```

必须保留边界：

```text
internet_search_allowed=false
resource_download_allowed=false
formal_kb_ingest_allowed=false
retrieval_enabled=false
generation_context_enabled=false
official_claim_allowed=false
```

### 4.4 模块四：缺口与追问

旧 `prep-workbench-v2` 的优势是会先理解语义、再追问缺项。右栏可以承担轻量缺口提示。

来自 0948C 的关键缺口：

```text
subject
grade
lesson_title
unit_or_topic
class_period_minutes
teacher_goal
student_prior_knowledge
assessment_evidence
unit_context
```

右栏不需要显示完整表单，只显示最关键的一个缺口：

```text
还差一个关键确认：
这节课希望用什么证据判断学生学会了？
[作品] [过程观察] [学习单]
```

### 4.5 模块五：教师审核门

所有生成/整理结果都要停在候选态。

建议字段：

```json
{
  "review_gate_id": "rg_lesson_1_2_handout",
  "target_object_type": "handout",
  "target_object_id": "handout_1_2",
  "status": "pending_teacher_review",
  "allowed_actions": ["accept", "accept_after_edit", "save_pending", "discard", "request_revision"],
  "formal_apply_performed": false
}
```

建议 UI 文案：

```text
教师确认后进入课前包
```

不要写：

```text
已发布
已写入
已同步
已正式生成
```

### 4.6 模块六：待沉淀内容

这块连接档案室，但不属于当前资料室。

建议展示：

```text
待沉淀
- 最终课时设计
- 课堂轻记录
- 学生作品证据
- 本课作品证据和课后反思
```

状态：

```text
not_started
pending_after_class
ready_to_archive
archived
```

## 5. 美术学科可复用内容

### 5.1 美术课时模板

来自 `subject_packs/art/lesson_templates/art_lesson_design_template_0954E.json`。

可用结构：

```text
topic_context
student_baseline
learning_objectives
key_difficult_points
materials_and_tools
classroom_flow
teacher_questions
student_activities
process_evaluation
display_and_reflection
```

这些适合放入中间主区的“课时设计”和右栏的“生成/补齐建议”。

### 5.2 美术评价量规维度

来自 `subject_packs/art/rubrics/art_rubric_schema_0954E.json`。

可用维度：

```text
构图
色彩
材料
技法
创意
过程性评价
```

右侧栏可以显示：

```text
评价量规：未生成
推荐维度：色彩 / 过程性评价 / 创意
```

不要直接进入正式评分。

### 5.3 可复用资料目录

本地已有解析资料：

```text
knowledge-base/_parsed/kb_art_g3_*.txt
knowledge-base/_parsed/kb_art_g4_*.txt
knowledge-base/_parsed/kb_art_g3_qinglv_content_export_001.txt
knowledge-base/_parsed/kb_art_g3_textbook_images_20260427.txt
knowledge-base/lesson-cases/
```

用途建议：

```text
资料室候选
课例参考
图片素材候选
教材图例候选
课题上下文候选
```

注意：当前只作为候选资料，不作为正式知识库检索结果。

## 6. 右侧栏建议 ViewModel

可以给 GPT 参考下面这个结构：

```json
{
  "right_prep_drawer": {
    "space": "prep_room",
    "view": "prep_notebook",
    "agent": "xiaobei",
    "lesson_ref": {
      "semester": "2026春学期",
      "grade": "三年级",
      "subject": "美术",
      "unit": "色彩单元",
      "lesson_code": "1-2",
      "lesson_title": "色彩的感觉"
    },
    "prep_package_ref": {
      "prep_package_id": "prep_2026_g3_art_1_2",
      "status": "draft_basic",
      "release_level": "none"
    },
    "suggestions": [
      {
        "type": "next_best_action",
        "title": "先确认学习单候选",
        "target_object": "handout",
        "reason": "学习单确认后才能进入课前包确认",
        "actions": ["open", "confirm", "revise"]
      }
    ],
    "material_folder": [
      {
        "object_type": "lesson_design",
        "title": "课时设计",
        "status": "pending",
        "source_layer": "l2_lesson_execution"
      },
      {
        "object_type": "handout",
        "title": "学习单",
        "status": "candidate",
        "source_layer": "l3_resource_collab"
      },
      {
        "object_type": "rubric",
        "title": "评价量规",
        "status": "missing",
        "source_layer": "l1_basic"
      },
      {
        "object_type": "resource_reference",
        "title": "资源参考",
        "status": "pending",
        "source_layer": "l3_resource_collab"
      }
    ],
    "available_resources": [
      {
        "resource_type": "textbook_context",
        "title": "苏少版三年级色彩单元课标摘要",
        "status": "candidate_only"
      },
      {
        "resource_type": "lesson_case",
        "title": "优秀课例《色彩的感觉》",
        "status": "candidate_only"
      }
    ],
    "missing_slots": [
      {
        "slot": "assessment_evidence",
        "question": "这节课你希望通过什么证据判断学生学会了？"
      }
    ],
    "review_gates": [
      {
        "target_object_type": "handout",
        "status": "pending_teacher_review",
        "formal_apply_performed": false
      }
    ],
    "archive_candidates": [
      "最终课时设计",
      "课堂轻记录",
      "学生作品证据",
      "本课课后反思"
    ],
    "boundary_flags": {
      "preview_only": true,
      "provider_called": false,
      "database_written": false,
      "feishu_written": false,
      "formal_export_created": false,
      "formal_scoring_enabled": false
    }
  }
}
```

## 7. 右侧栏视觉与交互建议

### 推荐分区

```text
本课建议
本课材料夹
可调用资料
待确认
待沉淀
```

### 推荐交互

```text
点击材料项 -> 中间主区高亮对应工作卡
点击生成按钮 -> 只生成候选，不正式写入
点击确认按钮 -> 进入 teacher_review_gate，显示待确认
点击资料项 -> 打开资料摘要/来源候选，不直接下载
点击沉淀项 -> 标记为档案室候选，不直接归档
```

### 不建议

```text
不做大段解释文案
不显示工程词：ViewModel / schema / dry-run
不把右栏做成聊天记录
不把资料室、备课本、档案室混成一个列表
不把小教写成备课室主助理
```

## 8. 推荐给 GPT 的设计问题

可以把这份资料交给 GPT 后，让它重点回答：

```text
1. 右侧备课栏如何围绕 prep_package 的 L1-L4 展开？
2. 本课材料夹应该显示哪些对象和状态？
3. 小备建议如何做到短、准、可操作？
4. 可调用资料如何区分资料室候选和本课已选材料？
5. 教师审核门如何嵌入右侧栏，避免系统自动正式写入？
6. 右侧栏和中间主工作区如何联动？
```

## 9. 当前建议结论

右侧栏第一版不要做复杂内容生成。

建议先做成：

```text
一张“本课备课状态与资料托盘”
```

它要让老师一眼知道：

```text
这节课还差什么
哪些材料已有候选
哪些资料可调用
哪些内容等我确认
上完课后哪些东西要沉淀到档案室
```

这比直接放“资料室 / 小备建议 / 待沉淀内容”三块粗列表更接近原系统底座。
