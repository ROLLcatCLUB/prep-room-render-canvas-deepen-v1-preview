# 师维「周课表」设计 V0

```text
WEEK_CALENDAR_BOARD_V0_DESIGN
STATUS=INTEGRATED_AS_FIRST_RENDER_STAGE_VIEW
REPLACES_FORMER_WEEK_PACKAGE_VIEW
BOUNDARY=STATIC_FIXTURE_ONLY
```

## 1. 模块定位

`周课表` 是课前执行视图，不替代 `班级进度与排课`。

```text
学期规划：这学期大致教什么、单元顺序是什么
班级进度与排课：各班进度是否一致，课时如何顺延、调课
周课表：本周每天每节课具体上什么，课前包是否完成
```

当前已接入 `prep_room_render_canvas_deepen_v1.html` 的第一个 RenderStage 视图：

```text
view_id = weekCalendar
view_label = 周课表
teacher_title = 本周课表
```

## 2. 主舞台结构

```text
横向 = 周一到周日
纵向 = 第1节到第8节
格子 = 课时卡 / 活动卡 / 调课卡 / 停课卡 / 补课卡
```

周六、周日必须保留，用于调休上课、补课或活动占用场景。

## 3. 数据投影关系

周课表不另起业务对象，而是从排课对象投影：

```text
class_lesson_instance
-> week_calendar_event
-> lesson_package_status
-> week_calendar_view
```

关键对象：

```text
class_lesson_instance：某班某周应上哪一节课
week_calendar_event：落到具体星期与节次后的事件
lesson_package_status：课前包是否备齐
calendar_event：活动、节假日、校务占用
schedule_adjustment_candidate：调课、顺延、补课候选
content_push_task：下节课材料推送任务
```

## 4. 课时卡字段

每张卡只显示：

```text
班级
课时编号 + 课题
课前包状态
```

详情抽屉字段：

```text
班级
时间
课题
已准备材料
待处理材料
上次轻记录
操作：打开课时设计 / 确认学习单 / 生成量规 / 顺手记一笔
```

## 5. 颜色规则

```text
正常上课：系统绿色
今日课时：绿色加深
未来课时：灰色弱化但可读
课前包未齐：橙色
调课：蓝色
活动占用：橙色
节假日停课：红灰色
顺延 / 补课：紫色
已完成：淡绿色
```

## 6. 右侧信息区

右侧不做大聊天，只放轻信息：

```text
今日课前准备
小教提醒
本周课前包完成度
```

## 7. 当前边界

```text
不接真实 API
不写数据库
不接 provider
不接真实学生数据
不包含 API key / token
不做正式应用
只作为静态 fixture 与页面结构预览
```

## 8. 下一阶段

```text
WEEK_CALENDAR_BOARD_V0_STATIC_PREVIEW_COMPLETE
NEXT_STAGE=USER_REVIEW_WEEK_CALENDAR_BOARD
```
