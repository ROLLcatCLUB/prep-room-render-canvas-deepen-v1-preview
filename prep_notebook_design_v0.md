# 备课本设计 V0

STATUS=PREP_NOTEBOOK_V0_STATIC_PREVIEW
BOUNDARY=STATIC_FIXTURE_ONLY
RUNTIME=NO_API_NO_MODEL_NO_DATABASE_NO_MEMORY_WRITE

## 1. 模块定义

```text
备课本 = 本学期的过程性工作本
```

它不是普通文档，也不是资料库。它是备课室里的核心工作对象，用来承接：

```text
学期
→ 单元
→ 课时
→ 班级课时
→ 课前包
→ 课堂记录
→ 学生作品 / 评价证据
→ 课后反思
```

当前 V0 只做静态预览，用来验证页面结构，不接真实接口、不写数据库、不调用模型。

## 2. 与资料室 / 档案室边界

```text
资料室 = 备课前可调用的东西
备课本 = 本学期正在发生的工作
档案室 = 已经发生并确认沉淀的东西
```

简写：

```text
资料室：备用
备课本：正在用
档案室：用完留下
```

备课本可以引用资料室，也会在确认后把最终教案、课堂记录、学生作品证据、课后反思沉淀到档案室。

## 3. 页面结构

```text
左侧：备课本目录
中间：当前节点工作区
右侧：资料、建议、记录、课前包抽屉
底部：对小备说一句
```

当前集成位置：

```text
备课室 RenderStage
周课表
→ 备课本
→ 班级排课
→ 学期规划
```

周课表控制条内也提供 `备课本` 链接按钮，方便教师从本周课前执行切回本学期工作本。

## 4. 左侧目录

左侧目录采用思维导图式层级，但保持规整列表：

```text
2026春 · 三年级美术

学期工作
  计划 学期规划
  排课 班级进度与排课
  周历 周课表

单元一 色彩单元
  1-1 认识色彩
  1-2 色彩的感觉
  1-3 色彩的对比

单元二 造型表现
  2-1 拼贴练习
  2-2 纸艺造型
```

节点状态：

```text
done    已完成
warn    待确认
draft   草稿
missing 缺材料
```

## 5. 中间工作区

当前示例节点：

```text
1-2《色彩的感觉》
```

中间区显示：

```text
课时设计：待确认
学习单：已有候选
评价量规：未生成
资源参考：待选择
课堂记录：暂无
```

工作卡：

```text
课时设计
本课材料夹
班级课时
课后沉淀
```

## 6. 右侧抽屉

右侧抽屉第一版固定展示三组，后续可按点击状态动态切换：

```text
小备建议
可调用资料
待沉淀内容
```

抽屉不是大聊天区。它只负责补充建议、资料入口、课前包状态、历史记录和版本信息。

## 7. 数据字段预留

建议后续 ViewModel 保留：

```text
prep_notebook_id
term_id
subject_id
grade_id
unit_id
lesson_id
class_lesson_instance_id
lesson_design_state
worksheet_state
rubric_state
resource_reference_state
prep_package_state
classroom_record_state
student_work_evidence_state
reflection_state
archive_candidate_state
```

## 8. 集成边界

当前 V0 不做：

```text
不接真实 API
不写数据库
不调用模型
不上传文件
不写 memory
不生成正式档案
不替代资料室或档案室
```

当前 V0 只做：

```text
新增备课本看板入口
验证左目录 + 中工作区 + 右抽屉结构
保留底部小备意图栏
保留静态预演边界
```

## 9. 下一阶段

```text
PREP_NOTEBOOK_V0_USER_REVIEW
```

用户确认结构后，再考虑：

```text
备课本节点点击后切换中间工作区
从周课表课时卡跳到对应备课本课时
从班级排课实例跳到班级课时页
从资料室引用素材
从备课本确认后归档到档案室
```
