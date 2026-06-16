# 飞书 API 与连接方式盘点 V0

生成日期：2026-06-16  
适用范围：`备课室 · 周课表 / 班级排课 / 学期规划 / 备课本` 的课表数据接入预研。  
目标：找清本地项目中现有飞书数据来源、OpenAPI 调用方式、连接边界和可用于徐涛老师课表接入的字段。

## 1. 结论

当前项目里有两条可用线索：

```text
1. 本地飞书真实数据快照
   可以立即用于静态预览接入徐涛老师课表。

2. 后端旧服务的飞书 OpenAPI 调用模板
   可以作为未来实时读取教师课表的代码参考，但需要重新走安全接入阶段。
```

当前不建议直接走：

```text
OpenClaw Feishu 插件 / 真实身份绑定 / 飞书写回
```

原因：

```text
OpenClaw 网关当前不可达，插件列表中也没有可用的 Feishu 插件。
历史权限文档明确：真实 Feishu 身份绑定、权限绑定、写回都处于 HOLD。
```

补充确认：

```text
飞书连接方式应以后端直连为准。
前端不直接拿飞书密钥，不保存 APP_SECRET，不读取 tenant_access_token。
当前服务器连接代码在 /home/admin/feishu_login_ocr.py。
```

## 2. 可立即使用的数据源：本地飞书真实快照

### 2.1 前端快照文件

来源：

```text
frontend/feishu-real-data-v1.js
```

关键内容：

```text
teacherProfile.teacherName = 徐涛老师
teacherProfile.subject = 美术
teacherProfile.teachingGrades = 三年级、四年级
teacherProfile.preferredGrade = 三年级
teacherProfile.commonClasses = 三年级5个班 · 四年级5个班
teacherProfile.scheduleSource = 飞书真实课表
teacherProfile.semester = 2025-2026学年第二学期
```

该文件声明的源目录：

```text
D:\Documents\New project\feishu_full_dump\main
```

其中课表表：

```text
tbl7OxfE4YPSE6GU.json
```

### 2.2 完整导出目录

来源：

```text
D:\Documents\New project\feishu_full_dump\main\tbl7OxfE4YPSE6GU.json
```

验证结果：

```text
table_name = 教师课表
table_id = tbl7OxfE4YPSE6GU
record_count = 53
```

字段：

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

| 星期 | 节次 | 班级 | 课程 | 教室 | 学期 |
| --- | --- | --- | --- | --- | --- |
| 周一 | 第6节 | 三(5)班 | 美术 | 美术一室 | 2025-2026学年第二学期 |
| 周一 | 第7节 | 三(1)班 | 美术 | 美术一室 | 2025-2026学年第二学期 |
| 周二 | 第6节 | 三(3)班 | 美术 | 美术一室 | 2025-2026学年第二学期 |
| 周三 | 第3节 | 三(4)班 | 美术 | 美术一室 | 2025-2026学年第二学期 |
| 周三 | 第7节 | 三(3)班 | 美术 | 美术一室 | 2025-2026学年第二学期 |
| 周四 | 第7节 | 三(2)班 | 美术 | 美术一室 | 2025-2026学年第二学期 |
| 周五 | 第5节 | 三(2)班 | 美术 | 美术一室 | 2025-2026学年第二学期 |
| 周五 | 第7节 | 三(1)班 | 美术 | 美术一室 | 2025-2026学年第二学期 |

说明：

```text
这 8 条是从本地飞书全量导出快照读取的真实课表记录。
不是本轮实时调用飞书 API 得到的最新数据。
```

## 3. 飞书表结构清单

来源：

```text
docs/reference/feishu_inventory_report.md
```

已记录表：

```text
教师课表 | tbl7OxfE4YPSE6GU
Records: 52
Fields: 8
```

字段示例：

```text
课表ID | auto_number
班级 | text
星期 | single_select
节次 | single_select
课程名称 | text
授课教师 | single_select
教室 | single_select
学期 | text
```

同一报告中还记录：

```text
teacher app: Cp00bzTYuawcvzs3064coGDCn7d
teacher 表中有教师姓名：徐涛
```

注意：

```text
表结构报告可作为字段依据。
实际课表记录优先读取本地 full dump 或实时 bitable records。
```

## 4. 后端 OpenAPI 调用模板

服务器主文件：

```text
/home/admin/feishu_login_ocr.py
```

本地可参考备份：

```text
outputs/server_backups/routine_ai_bot_0951N_20260615_152712_work/feishu_login_ocr.py
```

关键函数：

```text
get_tenant_access_token()
_list_bitable_records()
_post_bitable_record()
_put_bitable_record()
```

### 4.1 安全的环境变量式模板

来源：

```text
backend/xiaobei_ai/submission_transfer_0951I.py
```

该文件使用环境变量，不硬编码真实 secret。

环境变量名：

```text
FEISHU_APP_ID
FEISHU_APP_SECRET
FEISHU_TENANT_ACCESS_TOKEN
TENANT_ACCESS_TOKEN
FEISHU_ART_APP_TOKEN
ART_APP_TOKEN
FEISHU_ART_TABLE_ID
ART_TABLE_ID
```

获取 tenant token：

```text
POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
body = {
  "app_id": FEISHU_APP_ID,
  "app_secret": FEISHU_APP_SECRET
}
```

读取单条记录：

```text
GET https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}
headers = {
  "Authorization": "Bearer {tenant_access_token}"
}
```

写入记录：

```text
PUT https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}
headers = {
  "Authorization": "Bearer {tenant_access_token}",
  "Content-Type": "application/json"
}
body = {
  "fields": { ... }
}
```

本项目当前备课室预览只需要读课表，不需要写入。

课堂常规助手当前写入边界：

```text
目标表：学科常规提交表
只写字段：班级、学生姓名、具体内容、分数变动、原因
不写公式/系统字段：类型、学号、星期、节次、记录时间
```

这条规则可以作为后续师维写入飞书的字段白名单样板。

### 4.2 旧服务完整读取模板

来源：

```text
outputs/server_backups/submission_transfer_0951I_20260615_105819/feishu_login_ocr.patched.py
```

可复用的函数形态：

```text
get_tenant_access_token()
_list_bitable_records(app_token, table_id, token, page_size=500)
_list_bitable_fields(app_token, table_id, token, page_size=500)
_list_bitable_records_cached(bucket, app_token, table_id, token)
```

分页读取逻辑：

```text
GET https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records
params = {
  "page_size": 500,
  "page_token": page_token
}
```

字段读取逻辑：

```text
GET https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields
```

重要安全提醒：

```text
该旧备份文件中存在硬编码密钥痕迹。
后续不能直接复制该文件或暴露其中 secret。
只能复用函数结构，并改成环境变量 / SecretRef / 后端安全配置。
```

## 5. OpenClaw 状态

本机有 OpenClaw CLI：

```text
C:\Users\Administrator\AppData\Roaming\npm\openclaw.ps1
```

网关配置：

```text
127.0.0.1:18789
```

检查结果：

```text
OpenClaw gateway registered, but probe failed: ECONNREFUSED 127.0.0.1:18789
Gateway not reachable.
```

插件状态：

```text
plugins list 中没有启用的 Feishu / Lark 插件。
```

当前环境变量：

```text
XIAOBEI_OPENCLAW_AGENT_XIAOJIAO=<set>
XIAOBEI_OPENCLAW_AGENT_XIAOPING=<set>
```

未发现：

```text
FEISHU_APP_ID
FEISHU_APP_SECRET
FEISHU_TENANT_ACCESS_TOKEN
LARK_* 运行时环境变量
```

因此：

```text
本轮不能通过 OpenClaw 实时读取飞书。
```

## 6. 权限与边界

相关文档：

```text
docs/foundation/feishu_identity_permission_runtime_binding_authorization_gate_0986D.md
docs/foundation/feishu_account_center_integration_scope_contract_0988A.md
docs/foundation/feishu_local_permission_preview_bridge_readonly_apply_0986E.md
```

当前边界：

```text
真实 Feishu 身份绑定：HOLD
真实权限绑定：HOLD
飞书写回：禁止
前端直接读 token：禁止
本地只读 profile / schedule preview：允许
```

所以备课室当前推荐路线：

```text
第一阶段：读取本地 full dump / frontend 快照，接入真实课表静态预览。
第二阶段：做后端只读 Feishu schedule adapter，从环境变量或 SecretRef 获取授权。
第三阶段：在权限源明确后，再考虑真实运行时绑定。
```

## 7. 接入备课室的建议字段

从飞书教师课表映射到 `weekCalendar`：

```json
{
  "teacher_name": "徐涛",
  "semester": "2025-2026学年第二学期",
  "subject": "美术",
  "grade": "三年级",
  "class_name": "三(5)班",
  "weekday": "周一",
  "period": "第6节",
  "room": "美术一室",
  "source_record_id": "recvd6CpwhuXXD",
  "source_table_id": "tbl7OxfE4YPSE6GU",
  "source_kind": "feishu_full_dump_snapshot"
}
```

映射规则：

```text
星期 -> 周课表列
节次 -> 周课表行
班级 -> 课时卡班级
课程名称 -> 课程类型
教室 -> 课时卡地点 / hover
学期 -> 顶部上下文
record_id -> 后续追溯依据
```

## 8. 下一步

推荐下一步直接做：

```text
FEISHU_SCHEDULE_SNAPSHOT_TO_PREP_ROOM_V1
```

范围：

```text
读取本地 full dump 的教师课表表。
过滤 授课教师=徐涛、课程名称=美术、班级以“三”开头。
把 8 条三年级课表记录真实接入 `周课表`。
班级排课中的班级落点也改为以该课表为来源。
仍不调用飞书 API、不读 token、不写飞书。
```
