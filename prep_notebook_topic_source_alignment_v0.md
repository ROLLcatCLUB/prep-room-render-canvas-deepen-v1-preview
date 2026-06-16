# 备课本课题来源与连续性对齐 V0

生成日期：2026-06-16  
适用页面：`prep_room_render_canvas_deepen_v1.html`  
目标：备课本、周课表、班级排课、学期规划不再使用 GPT 临时拟题，而是优先使用本地知识库、教材目录和已有学期/单元资料中的连续课题。

## 1. 本次修正原则

```text
课题必须来自本地资料。
课题必须保持单元连续性。
同一套课题必须贯穿周课表、备课本、班级排课、学期规划。
页面原型不得为了填满界面临时编造“色彩游戏 / 冷暖对比 / 拼贴练习”等占位课题。
```

## 2. 已核对来源

### 2.1 教材目录候选

来源：

```text
context/textbook_catalog_snapshot_0931B.csv
```

已确认线索：

```text
苏少版 / 艺术·美术 / 三年级 / 上册 / 第二单元 / 色彩的碰撞
```

说明：该文件中三年级有新教材目录样板，但当前本地知识库中更完整的连续课例是三年级下册单元。

### 2.2 本地知识库 manifest

来源：

```text
knowledge-base/_manifests/items.csv
```

三年级下册已有完整连续资料：

```text
第一单元 多变的色彩
第二单元 守护生命的摇篮
第三单元 青绿中国色
```

### 2.3 内容库导出

来源：

```text
knowledge-base/_parsed/kb_art_g3_qinglv_content_export_001.txt
```

已确认：

```text
第三单元 青绿中国色
total_lessons = 4
lesson_content_count = 4
status = 草稿 · 4/4 课时已入内容库
linked_execution = 已生成 2 条执行作业
```

### 2.4 课例与备课文档

来源：

```text
knowledge-base/_parsed/
knowledge-base/lesson-cases/
```

当前页面使用三年级下册这条连续线，不使用临时拟题。

## 3. 当前采用的连续课题

### 第一单元 多变的色彩

```text
1-1 渐变的魅力
1-2 颜料的渐变
1-3 渐变的节奏
```

证据来源：

```text
knowledge-base/_manifests/items.csv
knowledge-base/lesson-cases/
```

### 第二单元 守护生命的摇篮

```text
2-1 走进海洋世界
2-2 变废为宝的艺术
2-3 制作海洋生物
2-4 守护海洋主题展
```

证据来源：

```text
knowledge-base/_manifests/items.csv
knowledge-base/lesson-cases/
```

### 第三单元 青绿中国色

```text
3-1 走进青绿山水
3-2 青绿色阶练习
3-3 心中的青绿山水
3-4 青绿山水展与评
```

证据来源：

```text
knowledge-base/_parsed/kb_art_g3_qinglv_content_export_001.txt
knowledge-base/_parsed/kb_art_g3_lesson_case_1_08f3e01f0b.txt
knowledge-base/_manifests/items.csv
knowledge-base/lesson-cases/
```

## 4. 页面替换范围

本次已将 `prep_room_render_canvas_deepen_v1.html` 中的以下视图统一到真实连续课题：

```text
周课表
备课本
班级进度与排课
学期规划
顶部/底部提示文案
右侧资料托盘候选
学期规划节点详情
AI 工具按钮建议
```

## 5. 明确删除的占位课题

本次从预览主数据中移除这些 GPT/占位式课题：

```text
色彩的感觉
色彩单元
色彩游戏
冷暖对比
综合色彩
线条的韵律
图案设计
创意拼贴
拼贴练习
纸艺造型
纹样设计
美术鉴赏
主题创作
综合创作
作品展示
```

## 6. 后续规则

后续 GPT 或 Codex 继续设计备课本时，必须遵守：

```text
1. 先查本地知识库 manifest 和 parsed 文本。
2. 同一年级同一学期只用一条连续课题链。
3. 如果没有真实课题，显示“待导入教材目录 / 待确认课题”，不要编。
4. 资料室候选必须标注来源，不提升为正式依据。
5. 周课表、班级排课、备课本、学期规划必须共用同一套 lesson_catalog。
```

推荐后续抽象字段：

```json
{
  "source_lesson_catalog": {
    "source": "knowledge-base/_manifests/items.csv",
    "grade": "三年级",
    "semester": "2026春学期",
    "subject": "美术",
    "units": [
      {
        "unit_code": "U01",
        "unit_title": "多变的色彩",
        "lessons": ["渐变的魅力", "颜料的渐变", "渐变的节奏"]
      },
      {
        "unit_code": "U02",
        "unit_title": "守护生命的摇篮",
        "lessons": ["走进海洋世界", "变废为宝的艺术", "制作海洋生物", "守护海洋主题展"]
      },
      {
        "unit_code": "U03",
        "unit_title": "青绿中国色",
        "lessons": ["走进青绿山水", "青绿色阶练习", "心中的青绿山水", "青绿山水展与评"]
      }
    ],
    "topic_policy": "no_gpt_fabricated_topics"
  }
}
```
