# 师维「班级进度与排课」设计 V0.1

```text
ACCEPT_AS_V0_STRUCTURE
NEEDS_V0_1_WEEKLY_TWO_SLOT_RULE -> RESOLVED_IN_THIS_DOC
ACCEPT_AS_V1_STATIC_PREVIEW
INTEGRATED_IN_PREP_ROOM_RENDER_STAGE -> REPLACES_FORMER_MONTH_PROGRESS_VIEW
CLASS_PROGRESS_SCHEDULE_BOARD_V1_1_READABILITY_POLISH -> APPLIED_IN_PREVIEW
```

## 0. 集成记录

2026-06-16：`class_progress_schedule_board_v1.html` 的方向已收为静态预览样板，并接入
`prep_room_render_canvas_deepen_v1.html` 的备课室 `RenderStage`。

当前系统页中，原“月进度”视图已删除，第二个中心舞台状态改为：

```text
view_id = classProgressSchedule
view_label = 班级排课
teacher_title = 班级进度与排课
weekly_period_capacity = 2
```

该视图固定采用：

```text
横向 = 班级
纵向 = 周次
单元格 = ClassWeekCell
单元格内部 = WeeklySlotStack
槽位 = ScheduleSlot(slot_index = 1 / 2)
```

后续接真实课表、校历、顺延和推送能力时，应围绕 `class_lesson_instance`
继续扩展，不再恢复旧的“月进度压力卡”结构。

V1.1 只处理可读性和密度，不接真实课表、校历、后端、Agent 调度或正式应用。已落实：

```text
当前周：整行高亮 + 左侧箭头 + 当前周胶囊
两课时槽：第1课时 / 第2课时稳定显示
未来课：灰化但保持文字可读
状态颜色：正常 / 未来 / 活动 / 节假日 / 调课 / 补课顺延保持克制区分
图例：轻量横向图例，不占主舞台
右侧建议：保持轻面板，只承载问题、建议和确认入口
移动端：保留横向滚动，不压碎班级列
```

## 1. 模块定位

`班级进度与排课` 不再按“月进度”理解，也不再是单纯的“学期地图”。

它的核心是：

```text
单元课时目录
-> 班级课表
-> 校历事件
-> 每班每周真实课时实例
-> 自动识别差异
-> 小教给出调整建议
-> 推送下节课准备内容
```

这个模块解决的是教师每天真正会遇到的问题：

- 同一个年级下，不同班级分别上到了哪一课；
- 哪些班因为活动、节假日、调课、考试、请假等原因落后或顺延；
- 未来几周每个班应该上哪一节；
- 调整某一周后，后续课时如何自动顺延、合并、跳过或提醒；
- 下节课应该提前准备哪些课包、学习单、材料、评价量规。

当前版本仍属于静态预览与结构讨论，不接 API、不写数据库、不自动正式应用。

教师可见标题建议固定为：

```text
班级进度与排课
```

教师可见副标题可用：

```text
查看各班上课进度，处理活动、节假日和调课带来的顺延。
```

## 2. 在师维系统中的位置

在 `ShiweiShell` 中，这个板块应作为中间 `RenderStage` 的一种动态渲染状态，而不是新开一套页面壳。

```text
ShiweiShell
├─ TopSpaceNav
├─ RenderStage
│  └─ ClassProgressScheduleBoard
└─ BottomIntentBar
   └─ 当前 Agent 建议切为 小教
```

推荐命名：

```text
space_state = prep_room 或 classroom_bridge
render_scene = class_progress_schedule_board
agent_position = xiaojiao_schedule_assistant
```

它与其他空间的联动关系：

```text
班级进度与排课
-> 小备：生成/补齐对应课包
-> 小教：安排课堂执行与调课建议
-> 小评：生成评价量规与观察点
-> 小美：准备学习单/PPT/视觉材料
-> 小管：课后归档、作品与学生记录回流
```

## 3. 中间主舞台结构

最终主舞台建议采用：

```text
横向 = 班级
纵向 = 周次
格子 = 该周该班的课时卡 / 活动 / 节假日 / 调课 / 顺延 / 风险
```

结构示意：

```text
┌──────────────────────────────────────────────────────────────┐
│ 控制条：学期 / 学科 / 年级切换 / 视图模式 / 筛选               │
├────────┬──────────┬──────────┬──────────┬──────────┬────────┤
│ 周次   │ 三1班     │ 三2班     │ 三3班     │ 三4班     │ 三5班   │
├────────┼──────────┼──────────┼──────────┼──────────┼────────┤
│ 第5周  │ 1-1      │ 1-1      │ 活动占用  │ 1-1      │ 1-1    │
│ 第6周  │ 1-2      │ 1-2      │ 1-1      │ 1-2      │ 1-2    │
│ 第7周  │ 1-3      │ 1-3      │ 1-2      │ 调课      │ 1-3    │
│ 第8周  │ 2-1      │ 2-1      │ 调课至周五 │ 2-1      │ 2-1    │
└────────┴──────────┴──────────┴──────────┴──────────┴────────┘
```

主舞台优先级：

1. `WeekAxis`：左侧固定周次与日期；
2. `ClassHeader`：顶部固定班级列头；
3. `ScheduleCell`：每周每班的格子；
4. `LessonCard / EventCard`：格子里的课时或事件；
5. `TodayLine`：当前周/当前日期线；
6. `FutureMask`：未来未到课时灰化；
7. `SuggestionPanel`：右侧或抽屉式建议，不抢主看板。

## 3.1 WeeklySlotStack 双课时槽位规则

这是 V0.1 必须补上的硬规则。

```text
每个 week × class 单元格，不是一个普通格子；
它是一个 ClassWeekCell。
每个 ClassWeekCell 内部默认包含 WeeklySlotStack。
WeeklySlotStack 默认容量 weekly_period_capacity = 2。
```

默认两个槽位：

```text
第1课时
第2课时
```

每个槽位只能放一种内容：

```text
lesson
activity
holiday
reschedule
delay
makeup
buffer
empty
```

示例：

```text
第8周 × 三3班
├─ 第1课时：调课至周五
└─ 第2课时：2-1 拼贴练习
```

这条规则用于防止页面重新退化成“普通进度表”。真实排课看的是：某一周、某一班、该教师这一周的两个美术课时分别发生了什么。

核心组件层级固定为：

```text
WeekClassScheduleGrid
└─ WeekRow
   └─ ClassWeekCell
      └─ WeeklySlotStack
         ├─ ScheduleSlot(slot_index=1)
         └─ ScheduleSlot(slot_index=2)
```

`ClassWeekCell` 只负责承载本周本班状态；`ScheduleSlot` 才是真正的课时/事件落点。

## 4. 顶部控制区字段

顶部控制只服务于“当前看哪一个排课上下文”，不要堆业务说明。

需要预留字段：

```text
term_id
term_label
subject_id
subject_label
grade_id
grade_label
grade_options
class_group_ids
view_mode
filter_flags
current_week_no
current_date
```

建议控件：

- 学期：`2026春学期`
- 学科：`美术`
- 年级切换：`三年级 / 四年级 / 五年级 / 六年级`
- 视图模式：`全班对照 / 单班详情 / 调整建议`
- 筛选：`只看异常 / 只看未来两周 / 只看已顺延`

年级切换必须显眼，因为这个看板默认按“教师授课年级”看，不建议把所有年级混在一张表里。

## 5. 主看板字段结构

### 5.1 ViewModel 顶层

```json
{
  "scene_id": "class_progress_schedule_board",
  "role": "art_teacher",
  "space": "prep_room",
  "agent_position": "xiaojiao_schedule_assistant",
  "weekly_period_capacity": 2,
  "term": {},
  "subject": {},
  "grade_scope": {},
  "class_headers": [],
  "week_axis": [],
  "class_week_cells": [],
  "lesson_catalog": [],
  "calendar_events": [],
  "adjustment_candidates": [],
  "next_lesson_push_tasks": [],
  "status_summary": {},
  "render_flags": {},
  "safety": {}
}
```

### 5.1.1 ClassWeekCell 与 ScheduleSlot

`class_week_cells` 是页面施工时的主数据，不建议只用松散的 `schedule_cells`。

```json
{
  "weekly_period_capacity": 2,
  "class_week_cells": [
    {
      "cell_id": "cell_w08_g3_c3",
      "week_id": "w08",
      "class_id": "g3_c3",
      "cell_state": "needs_adjustment",
      "slots": [
        {
          "slot_id": "slot_w08_g3_c3_1",
          "slot_index": 1,
          "slot_label": "第1课时",
          "card_type": "reschedule",
          "title": "调课至周五",
          "source_event_id": "event_school_activity_001",
          "status": "rescheduled",
          "is_future": false
        },
        {
          "slot_id": "slot_w08_g3_c3_2",
          "slot_index": 2,
          "slot_label": "第2课时",
          "card_type": "lesson",
          "lesson_code": "2-1",
          "lesson_title": "拼贴练习",
          "lesson_instance_id": "inst_g3_c3_w08_2",
          "status": "current",
          "is_future": false
        }
      ]
    }
  ]
}
```

如果某班每周实际课时量不是 2，可以通过 `weekly_period_capacity` 调整；但 V1 静态预览和默认交互先按 2 个槽位设计。

### 5.2 年级与班级

```json
{
  "grade_scope": {
    "grade_id": "grade_3",
    "grade_label": "三年级",
    "switchable_grades": ["grade_3", "grade_4", "grade_5", "grade_6"]
  },
  "class_headers": [
    {
      "class_id": "g3_c1",
      "class_label": "三1班",
      "current_lesson_code": "2-1",
      "progress_state": "normal",
      "risk_level": "none",
      "next_lesson_instance_id": "inst_g3_c1_w8_1"
    }
  ]
}
```

`progress_state` 建议枚举：

```text
normal
ahead
behind
delayed
conflict
needs_adjustment
```

### 5.3 周次轴

```json
{
  "week_axis": [
    {
      "week_id": "w08",
      "week_no": 8,
      "week_label": "第8周",
      "date_range": "5.18 - 5.24",
      "is_current_week": true,
      "is_future": false,
      "events_summary": ["校活动", "调课"]
    }
  ]
}
```

渲染要求：

- 左侧周次列固定；
- 当前周整行高亮；
- 未来周保持排课但整体灰化；
- 重要事件用轻标签提示。

### 5.4 课时实例

这是本模块最核心的对象。

```json
{
  "instance_id": "inst_g3_c3_w8_slot1",
  "class_id": "g3_c3",
  "week_id": "w08",
  "date": "2026-05-19",
  "weekday": "周二",
  "period": "第1课时",
  "lesson_code": "2-1",
  "lesson_title": "拼贴练习",
  "unit_id": "unit_2",
  "unit_title": "造型表现单元",
  "card_type": "lesson",
  "status": "rescheduled",
  "source": "auto_schedule",
  "is_future": false,
  "is_locked": false,
  "linked_package_id": "pkg_2_1",
  "linked_resources": ["worksheet_2_1", "rubric_2_1"],
  "previous_instance_id": "inst_g3_c3_w7_slot2",
  "next_instance_id": "inst_g3_c3_w8_slot2",
  "adjustment_candidate_ids": ["adj_g3_c3_w8_001"]
}
```

`card_type` 建议枚举：

```text
lesson
activity
holiday
exam
reschedule
delay
makeup
buffer
conflict
```

`status` 建议枚举：

```text
completed
current
planned
future
occupied
cancelled
rescheduled
delayed
makeup_needed
locked
```

### 5.5 单元课时目录

左侧目录不是菜单，而是课程内容主线。

```json
{
  "lesson_catalog": [
    {
      "unit_id": "unit_1",
      "unit_title": "色彩单元",
      "unit_color": "green",
      "total_lessons": 6,
      "arranged_lessons": 6,
      "lessons": [
        {
          "lesson_code": "1-1",
          "lesson_title": "色彩游戏",
          "required": true,
          "mergeable": false,
          "skippable": false,
          "buffer_candidate": false,
          "package_id": "pkg_1_1"
        }
      ]
    }
  ]
}
```

交互：

- 点击课时：高亮主表中所有班级对应课时；
- 点击单元：筛选/聚焦该单元；
- 后续可支持拖动课时到周次格，但第一版先不做拖拽。

## 6. 颜色与状态规则

默认系统色：

```text
正常课时：绿色 / 青绿色
```

其他类别：

```text
未来未到：灰色，文字浅灰
活动占用：橙色
节假日停课：浅红或灰红
调课：蓝色
顺延生成：淡紫或青灰，带箭头感
补课：紫色或蓝紫
风险冲突：红色描边 / 红点
机动课：浅灰绿
```

视觉原则：

- 颜色先表达类别，不要靠长文本解释；
- 每张卡只放课时编号、课时名、节次；
- 详情进点击弹框/抽屉；
- 当前周高亮，未来周灰化；
- 异常班级列头给弱红点或状态符号。

## 7. 中间区域推荐布局

推荐布局：

```text
RenderStage
├─ BoardControlStrip
│  ├─ TermSelect
│  ├─ SubjectSelect
│  ├─ GradeSwitcher
│  ├─ ViewModeTabs
│  └─ FilterChips
│
├─ ProgressSummary
│  ├─ 授课班级
│  ├─ 进度一致班
│  ├─ 待调整课时
│  └─ 当前周
│
├─ MainScheduleBoard
│  ├─ WeekAxis sticky
│  ├─ ClassHeader sticky
│  ├─ WeekClassScheduleGrid
│  │  ├─ WeekRow
│  │  ├─ ClassWeekCell
│  │  ├─ WeeklySlotStack
│  │  └─ ScheduleSlot
│  ├─ TodayLine
│  └─ FutureMask
│
└─ ScheduleInsightLayer
   ├─ LessonDetailDrawer
   ├─ AdjustmentSuggestionPanel
   └─ NextLessonPush
```

如果宽度不足：

- `ClassHeader + ScheduleGrid` 横向滚动；
- `WeekAxis` 保持 sticky；
- `SuggestionPanel` 收成右侧抽屉或底部浮层；
- `UnitLessonCatalog` 可以默认折叠，只在“学期规划/课时目录”模式展开。

## 8. 小教建议联动字段

建议对象：

```json
{
  "candidate_id": "adj_g3_c3_w8_001",
  "class_id": "g3_c3",
  "week_id": "w08",
  "reason_type": "activity_occupied",
  "reason_text": "三3班校活动占用第6周第1课时，已自动顺延。",
  "impact_scope": {
    "affected_instances": ["inst_g3_c3_w6_1", "inst_g3_c3_w7_1"],
    "affected_unit_ids": ["unit_1"],
    "delay_count": 1
  },
  "plans": [
    {
      "plan_id": "A",
      "label": "后续整体顺延",
      "tradeoff": "不跳过核心课时，但单元结束延后一周"
    },
    {
      "plan_id": "B",
      "label": "使用机动课补齐",
      "tradeoff": "保持单元结束时间，但占用1节机动课"
    }
  ],
  "teacher_confirmation_required": true,
  "apply_state": "preview_only"
}
```

注意：小教只能生成调整候选，不能直接正式改课表。

## 9. 下节课推送字段

```json
{
  "push_task_id": "push_g3_c5_next_001",
  "class_id": "g3_c5",
  "next_instance_id": "inst_g3_c5_w9_slot1",
  "lesson_code": "2-3",
  "lesson_title": "纹样设计",
  "prepare_items": [
    {
      "type": "lesson_package",
      "label": "课时设计",
      "state": "ready"
    },
    {
      "type": "worksheet",
      "label": "学习单",
      "state": "missing"
    },
    {
      "type": "rubric",
      "label": "评价量规",
      "state": "draft"
    }
  ],
  "agent_routes": ["xiaobei", "xiaomei", "xiaoping"],
  "teacher_action": "push_to_prep_room"
}
```

联动路径：

```text
点击“推送下节准备”
-> 小教识别各班 next_lesson
-> 小备补齐课包
-> 小美生成视觉材料
-> 小评补评价量规
-> 教师确认
-> 回到课堂执行
```

## 10. 第一版建议范围

第一版先做：

- 年级切换；
- 全班对照；
- 周次 × 班级矩阵；
- 每格支持多张课时/事件卡；
- 当前周高亮；
- 未来课时灰化；
- 活动、节假日、调课、顺延用颜色区分；
- 点击卡片打开详情；
- 右侧小教建议；
- 下节课准备推送入口。

第一版先不做：

- 拖拽排课；
- 真实写入课表；
- 自动正式应用；
- 复杂冲突求解器；
- 跨学科全校排课。

## 11. 当前预览线状态

当前 `PREP_ROOM_RENDER_CANVAS_DEEPEN_V1` 已更新为 `周课包 / 班级排课 / 学期规划` 三个视图。

已完成：

```text
删除“月进度”中心舞台
接入“班级进度与排课”
保留顶部 ShiweiShell
保留底部 IntentBar
中间 RenderStage 的第二视图改成 ClassProgressScheduleBoard
```

也就是说：

```text
班级排课 -> 班级进度与排课
学期规划 -> 保留为单元课时目录与学期周计划
周课包 -> 保留为课包准备入口
```

这样三个视图的职责会更清楚：

```text
周课包：本周要准备什么
班级进度与排课：每个班本周/未来周实际上什么
学期规划：整个学期课程主线怎么排
```
