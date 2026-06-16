# Session Handoff: Prep Room Render Canvas V1

```text
handoff_id=PREP_ROOM_RENDER_CANVAS_V1_SESSION_HANDOFF_20260616
workspace=D:\Documents\SmartEdu\xiaobei-core
package=outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1
review_repo=https://github.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview
latest_review_commit=efbd26fc4ca5bd4a700a75cd4919c45f6a2d27b4
status=STATIC_PREVIEW_AND_DOCUMENTATION_FOR_GPT_REVIEW
```

## 1. Current State

This session turned the prep-room preview into a shell-and-render-stage prototype.

Current main file:

```text
outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/prep_room_render_canvas_deepen_v1.html
```

Current GitHub review entry:

```text
https://github.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview
```

Current raw review prompt:

```text
https://raw.githubusercontent.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview/main/GPT_REVIEW_PROMPT.md
```

Current raw main preview:

```text
https://raw.githubusercontent.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview/main/prep_room_render_canvas_deepen_v1.html
```

## 2. System Logic Locked In This Session

The system principle is:

```text
师维 = 学校里的 AI 工作社区
```

The architecture principle is:

```text
身份决定空间，空间决定 Agent，Agent 承办对应事务。
```

The shell principle is:

```text
顶部和底部常驻。
中间动态渲染。
空间不是页面，空间是 RenderStage 里的当前状态。
Agent 不是页面组件，Agent 是底部意图栏里的当前承办角色。
```

Current shell structure:

```text
ShiweiShell
├─ TopSpaceNav
├─ RenderStage
└─ BottomIntentBar
```

Current prep-room route shape:

```text
当前空间 = 备课室
顶部标题 = 备课室 · 当前看板
底部默认 Agent = 小备
中间 RenderStage = 周课表 / 备课本 / 班级排课 / 学期规划
```

Important ownership rule:

```text
备课室不是小教管辖。
备课室主助理是小备。
小教可以出现在周课表、班级排课、课前执行提醒里。
小管可以出现在排课、校历、调课建议里。
```

## 3. View Decisions

### 3.1 Removed Or Replaced

Removed from the prep-room RenderStage:

```text
旧周课包视图
旧月进度视图
月进度压力卡
大单元阵列式月进度
```

Do not restore these as primary prep-room boards.

### 3.2 Current Boards

The prep-room boards are now:

```text
周课表
备课本
班级排课
学期规划
```

Top center title must show:

```text
备课室 · 周课表
备课室 · 备课本
备课室 · 班级排课
备课室 · 学期规划
```

### 3.3 周课表

Purpose:

```text
本周课前执行视图。
回答：今天/本周哪天哪节、哪个班、上什么、课前包准备好了没有。
```

Structure:

```text
横向 = 周一到周日
纵向 = 节次
格子 = 班级 + 课题 + 课前包状态 / 活动 / 调课 / 节假日 / 补课
```

Reason for Saturday and Sunday:

```text
调休时可能有课，所以周六周日也要保留。
```

### 3.4 备课本

Purpose:

```text
备课本 = 本学期的过程性工作本。
```

It is not a normal document, not a resource library, and not an archive.

Visual direction:

```text
活页夹 / 工作本感觉。
绿色系深色书皮。
书皮只包左侧目录和中间工作页。
右侧资源栏在本子外面。
中间可有灰绿展开隔层。
暂不做装订线和钉子。
```

Current structure:

```text
左侧：学期 / 单元 / 课时目录
中间：当前课时工作页
右侧：小备建议 / 可调用资料 / 待沉淀内容
底部：对小备说一句
```

Important content direction for the right drawer:

```text
右侧备课栏里的内容需要继续做。
不要凭空拟题。
要查找原系统中和备课有关的资料、字段、素材、教材、学期规划，再整理成可用内容。
```

### 3.5 班级排课

Purpose:

```text
跨周、跨班级，看不同班级进度差异。
```

Structure:

```text
横向 = 班级
纵向 = 周次
格子 = 每班每周两个课时槽位
```

Slot rule:

```text
weekly_period_capacity = 2
每个 week × class 单元格默认两个课时槽。
可显示正常课时、未来课、活动占用、节假日、调课、顺延、补课、风险。
```

Recent visual decisions:

```text
课时居中对齐。
不要显示第1课时/第2课时卡片芯片。
中间横向展开，不要被固定尺寸压扁。
授课班级等指标只留图标和数字，不要标题小字。
指标移动到班级切换后面。
颜色说明跟在指标后面。
```

### 3.6 学期规划

Purpose:

```text
这学期大致教什么、单元顺序是什么、每周怎么推进。
```

Current source priority:

```text
本地 Word 教学工作计划 > 飞书课表快照 > 临时静态 fixture > GPT 临时拟题
```

Do not use GPT-made fake topic chains when the local teaching plan exists.

## 4. Concept Index

### 4.1 Role And Space Model

Current first role sample:

```text
role = art_teacher
spaces = 备课室 / 教室 / 作品馆 / 资料室 / 档案室 / 教研室
agents = 小备 / 小教 / 小评 / 小美 / 小管 / 小研
```

Future role expansion must remain possible:

```text
role = principal
role = logistics_staff
role = science_teacher
role = homeroom_teacher
```

Do not name the system as `art_teacher_only`.

### 4.2 备课本 / 资料室 / 档案室 Boundary

Stable boundary:

```text
资料室 = 备用资源
备课本 = 正在用
档案室 = 用完留下
```

Flow:

```text
资料室
↓ 被选用
备课本
↓ 上课 / 修改 / 评价 / 记录
档案室
↓ 提炼成可复用经验
资料室
```

Teacher-facing name:

```text
知识库不要直接显示给教师。
教师端建议叫 资料室。
沉淀区叫 档案室。
```

### 4.3 Sample Room Notes

Earlier pasted sample-room references were recorded as:

```text
首页样板间
教室样板间
备课室样板间
```

These are reference-only unless the user explicitly asks to implement.

## 5. Source Materials And Local Evidence

### 5.1 Teaching Work Plan

Local Word source:

```text
E:\学校工作\教学\教学资料\2025第二学期三年级\2025学年第二学期三年级美术教学工作计划.docx
```

Extracted document:

```text
outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/teaching_plan_source_2025_second_term_g3_art_v0.md
```

Current extracted planning source includes:

```text
7 textbook units
4 Creative Arts Festival lessons
6 flexible/review lessons
16-week progress table
```

Use this source first when populating:

```text
学期规划
备课本目录
周课表课题
班级排课课题
```

### 5.2 Feishu Connection Findings

Feishu connection is backend-direct only:

```text
frontend -> backend -> Feishu OpenAPI
```

Do not put Feishu secrets into frontend or GitHub.

Server-side real connection code path noted by the user:

```text
/home/admin/feishu_login_ocr.py
```

Important functions:

```text
get_tenant_access_token()
_list_bitable_records()
_post_bitable_record()
_put_bitable_record()
```

Current local evidence source:

```text
D:\Documents\New project\feishu_full_dump\main\tbl7OxfE4YPSE6GU.json
```

Current Feishu docs:

```text
outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/feishu_api_connection_inventory_v0.md
outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/feishu_business_data_relevance_inventory_v0.md
```

Current Xu Tao Grade 3 art schedule rows recorded in the inventory:

```text
周一 第6节 三(5)班 美术 美术一室
周一 第7节 三(1)班 美术 美术一室
周二 第6节 三(3)班 美术 美术一室
周三 第3节 三(4)班 美术 美术一室
周三 第7节 三(3)班 美术 美术一室
周四 第7节 三(2)班 美术 美术一室
周五 第5节 三(2)班 美术 美术一室
周五 第7节 三(1)班 美术 美术一室
```

Current boundary:

```text
not_live_api=true
local_dump_snapshot=true
no_token_in_docs=true
no_feishu_write=true
```

## 6. GitHub Review Upload Method

Do not push the dirty main repo.

Main repo state is dirty and contains many unrelated changes. Review upload must use a small dedicated package.

Current local review root:

```text
D:\Documents\SmartEdu\xiaobei-github-review\prep-room-render-canvas-deepen-v1-preview
```

Current review repo:

```text
https://github.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview
```

Current review commit:

```text
efbd26fc4ca5bd4a700a75cd4919c45f6a2d27b4
```

Upload method used:

```text
gh api / GitHub Git Data API
```

Reason:

```text
This Windows environment may not safely use plain git push for review packages,
and the main working tree is too dirty to publish directly.
```

Review package files:

```text
GPT_REVIEW_PROMPT.md
REVIEW_PACKAGE_MANIFEST.md
README.md
prep_room_render_canvas_deepen_v1.html
class_progress_schedule_board_v1.html
teaching_plan_source_2025_second_term_g3_art_v0.md
feishu_api_connection_inventory_v0.md
feishu_business_data_relevance_inventory_v0.md
shiwei_concept_archive_v0.md
prep_notebook_design_v0.md
prep_notebook_right_drawer_source_inventory_v0.md
prep_notebook_topic_source_alignment_v0.md
week_calendar_board_design_v0.md
class_progress_schedule_board_design_v0.md
smoke screenshots
ZIP archive
SHA256SUMS.txt
```

Raw links to give GPT:

```text
https://raw.githubusercontent.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview/main/GPT_REVIEW_PROMPT.md
https://raw.githubusercontent.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview/main/REVIEW_PACKAGE_MANIFEST.md
https://raw.githubusercontent.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview/main/README.md
https://raw.githubusercontent.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview/main/prep_room_render_canvas_deepen_v1.html
https://raw.githubusercontent.com/ROLLcatCLUB/prep-room-render-canvas-deepen-v1-preview/main/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1_REVIEW_20260616.zip
```

Before upload, run a secret scan. The last package passed strict scan:

```text
SECRET_SCAN_STRICT=PASS
```

## 7. Do Not Do Yet

Do not do these in the next session unless the user explicitly widens scope:

```text
Do not connect live Feishu from frontend.
Do not paste APP_SECRET or tenant_access_token into chat, docs, HTML, or GitHub.
Do not write Feishu records.
Do not connect real model/provider calls.
Do not switch default route of the real app.
Do not formal-apply this static preview into main runtime.
Do not restore old month-progress view.
Do not use GPT-made topic names when local teaching plan exists.
Do not treat 资料室 and 档案室 as the same thing.
Do not make 小教 the owner of the whole 备课室.
```

## 8. Recommended Next Session Route

Suggested next route:

```text
1. Read this handoff.
2. Read README.md.
3. Read GPT_REVIEW_PROMPT.md.
4. Open prep_room_render_canvas_deepen_v1.html locally.
5. Wait for or paste GPT review result.
6. If review passes, choose one narrow next stage.
```

Likely next stages:

```text
PREP_NOTEBOOK_RIGHT_DRAWER_CONTENT_V1
FEISHU_SNAPSHOT_SCHEDULE_TO_WEEK_CALENDAR_V1
BACKEND_FEISHU_READONLY_SCHEDULE_ADAPTER_V0
TEACHING_PLAN_TO_RENDER_STAGE_VIEWMODEL_V1
PREP_ROOM_RENDER_STAGE_STATE_SCHEMA_V1
```

Preferred immediate stage:

```text
PREP_NOTEBOOK_RIGHT_DRAWER_CONTENT_V1
```

Reason:

```text
The user specifically said the right prep drawer content should start to be built
from original system prep-related materials and source inventory,
not from temporary GPT-generated content.
```

## 9. One-Sentence Handoff

```text
This line is a static, review-only Shiwei prep-room RenderStage prototype:
the shell logic and board taxonomy are now clear, the teaching topics are grounded
in the local Grade 3 art teaching work plan, Feishu has only been inventoried from
safe snapshots, and the next session should continue by deepening the prep notebook
right drawer or wiring a readonly schedule adapter without exposing secrets or
formally applying the preview into runtime.
```

