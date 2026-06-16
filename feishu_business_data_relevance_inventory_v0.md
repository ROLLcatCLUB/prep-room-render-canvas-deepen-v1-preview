# 飞书业务资料与师维系统关系盘点 V0

生成日期：2026-06-16  
范围：本地项目、飞书 full dump 快照、服务器备份代码。  
原则：前端不直接接触飞书密钥；真实飞书连接必须由后端完成。

## 1. 关键判断

飞书在当前项目中不是普通外部表格，而是已经承载了大量真实业务对象：

```text
教师与课表
备课与课时
教学环节
作业发布与提交
作品评价
课堂常规
学期总表
能量 / 等级 / 勋章
```

因此，师维后续不能只把飞书当“导入源”，而应把它视为现有学校业务数据底座的一部分。

推荐系统关系：

```text
飞书现有表 = 真实业务资料来源
师维后端 = 读取 / 适配 / 安全写入网关
师维前端 = 渲染与教师确认界面
```

## 2. 飞书连接方式

用户确认的服务器连接方式：

```text
服务器文件：/home/admin/feishu_login_ocr.py
```

关键函数：

```text
get_tenant_access_token()
_list_bitable_records()
_post_bitable_record()
_put_bitable_record()
```

连接流程：

```text
1. 后端使用 APP_ID + APP_SECRET 换 tenant_access_token
2. 后端带 Authorization: Bearer {tenant_access_token} 访问多维表格
3. 前端只访问后端接口，不接触 APP_SECRET、tenant_access_token 或飞书 app token
```

Token 接口：

```http
POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
```

多维表格接口：

```http
GET  https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records
POST https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records
PUT  https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}
```

本地可参考代码：

```text
backend/xiaobei_ai/submission_transfer_0951I.py
outputs/server_backups/routine_ai_bot_0951N_20260615_152712_work/feishu_login_ocr.py
```

注意：

```text
服务器真实 APP_SECRET 不写入文档，不出现在前端，不贴入聊天。
```

## 3. 本地 full dump 数据源

本地真实快照目录：

```text
D:\Documents\New project\feishu_full_dump\main
```

前端快照入口：

```text
frontend/feishu-real-data-v1.js
```

该快照声明：

```text
teacherName = 徐涛老师
subject = 美术
teachingGrades = 三年级、四年级
preferredGrade = 三年级
scheduleSource = 飞书真实课表
semester = 2025-2026学年第二学期
```

用途：

```text
可作为静态预览、字段映射、数据模型设计的真实样本。
不能当作最新在线数据。
```

## 4. 已发现主表清单

### 4.1 备课与教学设计

| 表名 | table_id | 记录数 | 与师维关系 |
| --- | --- | ---: | --- |
| 大单元主表 | tbl1XHhTVBBcR5Xs | 14 | 学期规划、备课本单元页、资料室素材 |
| 课时子表 | tbl0oOhzN7gwfE1O | 51 | 备课本课时页、课前包、周课表课题来源 |
| 教学环节表 | tblNJTHVrmgq40Ec | 134 | 课时流程、小教课堂流程、PPT/话术生成 |
| 备课总表 | tblXwzZl3tVhoWYh | 19 | 备课本目录、已备/待备状态 |
| 单课备课表(老） | tblb4Yr5JT4I6QQK | 7 | 老版教案资料，可进入资料室或档案室 |

关键字段：

```text
大单元、年级、课时数、核心素养目标、核心表现性任务、教学资源清单
子课时名、所属大单元、课时目标、主要内容、核心活动、教师准备、学生准备
教学步骤、教师话术、学生任务、材料需求、成功标准、PPT页面说明
```

对应师维模块：

```text
备课室 · 备课本
备课室 · 学期规划
备课室 · 周课表
资料室 · 教材课例 / 教学资源
```

### 4.2 教师与课表

| 表名 | table_id | 记录数 | 与师维关系 |
| --- | --- | ---: | --- |
| 教师课表 | tbl7OxfE4YPSE6GU | 52 | 周课表、班级排课、课前提醒 |

关键字段：

```text
课表ID
班级
星期
节次
课程名称
授课教师
教室
学期
```

徐涛老师三年级美术课表快照：

| 星期 | 节次 | 班级 | 教室 |
| --- | --- | --- | --- |
| 周一 | 第6节 | 三(5)班 | 美术一室 |
| 周一 | 第7节 | 三(1)班 | 美术一室 |
| 周二 | 第6节 | 三(3)班 | 美术一室 |
| 周三 | 第3节 | 三(4)班 | 美术一室 |
| 周三 | 第7节 | 三(3)班 | 美术一室 |
| 周四 | 第7节 | 三(2)班 | 美术一室 |
| 周五 | 第5节 | 三(2)班 | 美术一室 |
| 周五 | 第7节 | 三(1)班 | 美术一室 |

对应师维模块：

```text
备课室 · 周课表
备课室 · 班级进度与排课
小教提醒
小管排课建议
```

### 4.3 作业、作品与评价

| 表名 | table_id | 记录数 | 与师维关系 |
| --- | --- | ---: | --- |
| 作业信息表 | tblt9cFmiy6ZQ6yL | 15 | 课前包、作业发布、提交追踪 |
| 作品提交表 | tblBfJPnSXFldxg3 | 3271 | 作品馆、作品评价、档案室证据 |
| 作业统计表 | tbllDblbp0Fxc3YS | 1123 | 班级作业完成度、学情摘要 |
| 作品评价表 | tblnxTSmMteoj6yy | 11 | 小评、评价证据、档案沉淀 |
| 标签管理表 | tblGes5UQLYyQ4si | 4 | 评价话术库、资料室评价语 |
| 技能进阶表 | tbltUBqhTYPrexYM | 3 | 学生能力轨迹、评价维度 |

关键字段：

```text
作业名称、作业要求、提交截止日期、作业状态
作品图片、AI评分、老师维度得分、综合评语、留言
已交/未交名单、上缴率、扣分作业列表
评价标签、对应评价话术
```

对应师维模块：

```text
作品馆
档案室
小评
备课本课后沉淀
班级学情摘要
```

### 4.4 课堂常规与过程记录

| 表名 | table_id | 记录数 | 与师维关系 |
| --- | --- | ---: | --- |
| 学科常规提交表 | tbll1lvDPRdXEMQy | 655 | 课堂记录、小教课堂观察 |
| 学科常规统计表 | tblH63O8LCApqT67 | 1125 | 班级常规画像、学生过程性表现 |

课堂常规助手写入规则：

```text
目标表：学科常规提交表
只写字段：班级、学生姓名、具体内容、分数变动、原因
不写字段：类型、学号、星期、节次、记录时间
```

服务器接口形态：

```text
GET/POST /api/routine/ai/status
POST     /api/routine/ai/parse
POST     /api/routine/ai/commit
```

安全机制：

```text
parse 只做 dry-run，不写入。
commit 需要 confirm=true。
写入前校验班级、学生、分数范围。
部分写入失败时返回 manual_reconcile_required。
```

对应师维模块：

```text
教室 · 课堂记录
备课本 · 课后记录
档案室 · 课堂证据
小教 / 小管协同
```

### 4.5 学期总表、能量与激励

| 表名 | table_id | 记录数 | 与师维关系 |
| --- | --- | ---: | --- |
| 学期总表 | tblSwq8R71o4UF99 | 1124 | 学生学期画像、档案室 |
| 能量系统表 | tblRhyPQQxFmd6lP | 1125 | 激励体系、过程性评价 |
| 能量记录表 | tblz7sk50a10yDfp | 8 | 能量变动日志 |
| 等级配置表 | tblFA6pcrkiQepUo | 20 | 等级规则 |
| 勋章配置表 | tblNAMwM3Eeqh4MT | 3 | 勋章规则 |
| 学生勋章记录表 | tblsZrZ8Lni44Fys | 0 | 勋章记录 |

对应师维模块：

```text
档案室
学生画像
过程性评价
班主任 / 教师协同视图
```

## 5. 对师维空间的映射

### 备课室

优先接入：

```text
大单元主表
课时子表
教学环节表
教师课表
备课总表
作业信息表
```

用途：

```text
学期规划
备课本
周课表
班级进度与排课
课前包
```

### 资料室

优先接入：

```text
单课备课表(老）
大单元主表中的教学资源清单
课时子表中的教师准备 / 学生准备
教学环节表中的 PPT 页面说明
标签管理表中的评价话术
```

用途：

```text
教材课例
资源候选
评价话术
可复用模板
```

### 教室

优先接入：

```text
教师课表
教学环节表
学科常规提交表
学科常规统计表
```

用途：

```text
本节课执行
课堂观察
常规记录
课后轻记录
```

### 作品馆

优先接入：

```text
作品提交表
作业信息表
作品评价表
标签管理表
```

用途：

```text
作品墙
作品筛选
AI 初评 / 教师复核
展览候选
```

### 档案室

优先接入：

```text
学期总表
作品评价表
作品提交表
学科常规统计表
作业统计表
能量系统表
```

用途：

```text
已完成备课
课堂证据
学生作品证据
学期画像
教学成果包
```

## 6. 推荐底层对象

可从飞书表抽象成这些师维对象：

```text
teacher_profile
teacher_schedule_slot
unit_plan
lesson_plan
lesson_step
lesson_package
assignment_task
submission_record
artwork_record
evaluation_record
routine_event
routine_stat
student_term_profile
energy_event
badge_rule
```

其中当前备课室最先需要：

```text
teacher_schedule_slot
unit_plan
lesson_plan
lesson_step
assignment_task
```

## 7. 接入路线

### V0：本地快照只读接入

```text
读取 D:\Documents\New project\feishu_full_dump\main
过滤徐涛老师、三年级、美术、2025-2026学年第二学期
接入周课表和班级排课
不读 token，不写飞书
```

### V1：后端只读适配器

```text
新增 backend schedule adapter
使用服务器 /home/admin/feishu_login_ocr.py 的连接方式
只开放后端内部读取
前端通过师维 API 获取净化后的课表 ViewModel
```

### V2：教师确认后的受控写入

```text
仅对明确允许的业务表开放写入
每个写入动作必须有教师确认、字段白名单、审计记录和回滚策略
课堂常规提交表可参考现有 5 字段写入规则
```

## 8. 当前禁止事项

```text
不要把 APP_SECRET 写到前端。
不要把 tenant_access_token 暴露给浏览器。
不要在静态 HTML 中写飞书密钥。
不要直接复制旧备份中的硬编码 secret。
不要写飞书公式字段 / 系统字段。
不要绕过教师确认写入课堂常规或作品评价。
```

## 9. 下一步建议

先做：

```text
FEISHU_SNAPSHOT_SCHEDULE_TO_PREP_ROOM_V1
```

具体任务：

```text
1. 从 full dump 读取教师课表。
2. 用徐涛老师三年级美术课表替换当前周课表的模拟课位。
3. 保留教学工作计划提供的课题进度。
4. 将 teacher_schedule_slot 与 lesson_plan 做静态匹配。
5. 文档标明 source_kind = feishu_full_dump_snapshot。
```

再做：

```text
BACKEND_FEISHU_READONLY_SCHEDULE_ADAPTER_V0
```

用于未来真实后端读取，不进入前端密钥。

