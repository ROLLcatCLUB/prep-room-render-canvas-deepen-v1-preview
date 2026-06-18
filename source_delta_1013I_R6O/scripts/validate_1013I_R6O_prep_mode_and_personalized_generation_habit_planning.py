from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6O_PREP_MODE_AND_PERSONALIZED_GENERATION_HABIT_PLANNING"
FINAL_STATUS = "PASS_1013I_R6O_PREP_MODE_AND_PERSONALIZED_GENERATION_HABIT_PLANNING"
INHERITS_FROM = "1013I_R6N_R6_MATERIAL_PROMPT_FRONTLOADED_HORIZONTAL"
NEXT_STAGE = "USER_REVIEW_PREP_MODE_PLANNING"
STAGE_DIR_NAME = "1013I_R6O_prep_mode_and_personalized_generation_habit_planning"
PLAN_NAME = "prep_mode_and_personalized_generation_habit_plan_1013I_R6O.md"
CONTRACT_NAME = "prep_mode_and_personalized_generation_habit_contract_1013I_R6O.json"
RESULT_NAME = "1013I_R6O_result.json"
VALIDATOR_NAME = "validate_1013I_R6O_prep_mode_and_personalized_generation_habit_planning.py"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_output_root(root: Path) -> Path:
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    if (root / "REVIEW_PACKAGE_MANIFEST.md").exists() and (root / "LATEST_REVIEW_ENTRY.md").exists():
        return root
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "planning_only": True,
        "ui_implementation_started": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "prompt_template_modified": False,
        "memory_written": False,
        "database_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
    }


def plan_markdown() -> str:
    return """# 备课模式与个人化生成习惯规划

```text
STAGE=1013I_R6O_PREP_MODE_AND_PERSONALIZED_GENERATION_HABIT_PLANNING
STATUS=PLANNING_ONLY
PRODUCT_LINE=备课模式与个人化生成习惯
NOT_A_PROMPT_TEMPLATE_EDITOR=true
```

## 1. 产品判断

这条线值得作为备课室重点规划。

它解决的不是“给老师三个按钮”，而是让备课室能够识别不同备课场景：

- 有时老师只想快速得到一版能用的常态课。
- 有时老师需要完整、稳妥、可教研的备课预览。
- 有时老师要精备公开课、研究课或赛课，需要分步确认和逐段打磨。
- 同一位老师的写法、栏目习惯、材料偏好和评价方式应该能逐步沉淀。
- 但共享模板、学校模板和系统模板必须有权限与审核，不能开放为“老师直接改系统提示词”。

产品前台命名：

```text
备课模式与个人化生成习惯
```

禁止前台命名：

```text
提示词模板编辑器
系统 prompt 编辑
schema 字段修改
模板 registry 写入
```

## 2. 三种备课模式

### 快速出稿

适合日常常规课、赶时间、先要一个靠谱框架。

系统行为：

- 少追问。
- 直接生成一版可读预览。
- 允许后续继续修改。
- 不强制完整课标、大单元链和评价证据展开。

教师可见表达：

```text
小教先帮你出一版可用预览，后面可以继续改。
```

### 完整备课

作为默认模式。适合常规教研、集体备课、正常质量的教学设计。

系统行为：

- 检查课标方向、学生起点、单元位置、课堂推进和评价证据。
- 适度追问，但不频繁打断老师。
- 输出较完整的备课预览。

教师可见表达：

```text
小教会先整理课标方向、学生起点、课堂推进和评价证据，再生成一份完整备课预览。
```

### 精备打磨

适合公开课、赛课、课题研究、论文案例、精品课。

系统行为：

- 先给栏目和方向。
- 教师确认栏目。
- 教师补充自己的想法。
- 系统逐段生成。
- 每段都可以讨论、修改、替换或继续打磨。

教师可见表达：

```text
我们先把这节课的结构搭好，再一段段打磨。
```

这句话只放在模式说明中，不放入最终备课本主阅读区。

## 3. 本次补充入口

教师的自然语言补充要被转成“本次生成条件”，不能只留在聊天记录里。

示例：

```text
老师说：我希望这节课多关注学生说不出颜色感觉的问题。
本次备课偏好：重点关注学生色彩表达语言不足的问题。

老师说：不要写得太公开课，常态一点。
写作偏好：常态课风格，避免公开课腔。

老师说：我想用生活图片导入，不想放视频。
材料偏好：生活图片导入；不使用视频资源。
```

教师可见名称：

```text
本次想法
我的补充
这次备课要注意
小教已记下
```

禁止教师可见名称：

```text
条件字段
系统提示词
模板变量
schema
```

## 4. 栏目协商，不叫字段协商

教师参与的是备课结构和写法，不是工程字段。

前台表达：

```text
这次备课你想保留哪些栏目？
- 课标依据
- 学生起点
- 学习目标
- 课堂推进
- 评价证据
- 材料支架
- 课后调整
```

教师删除栏目时：

```text
这次先不放“课后调整”。以后是否默认去掉，需要你确认后再记住。
```

系统内部可以映射为栏目模板或生成策略，但前台不暴露字段、prompt 或 registry。

## 5. 记忆层分级

### 本次有效

只影响当前备课。

```text
这次备课按你的想法来，不影响以后。
```

### 个人偏好

只影响当前教师。

可沉淀：

- 喜欢的栏目顺序。
- 常用课型写法。
- 不喜欢公开课腔。
- 偏好过程性评价。
- 常用材料类型。
- 喜欢简短学习单。

### 学校或学科组模板

影响多人，必须审批。

教师可见入口：

```text
申请设为美术组模板
```

### 系统默认模板

影响所有用户，只能平台管理员修改。

普通教师不能直接改。

## 6. 权限分层

| 权限 | 能改什么 | 是否需要审核 |
| --- | --- | --- |
| 普通教师 | 本次备课、个人偏好 | 不需要或轻确认 |
| 学科组长 | 学科组共享模板 | 需要确认 |
| 学校管理员 | 校本模板、学校默认结构 | 需要审核记录 |
| 系统管理员 | 平台默认模板、底层规则 | 严格审核 |

教师前台按钮：

```text
仅本次使用
保存为我的习惯
申请设为美术组模板
```

禁止前台按钮：

```text
修改全局 schema
修改系统 prompt
写入模板 registry
```

## 7. 分阶段实现路线

### 第一阶段：模式选择

只做：

```text
快速出稿
完整备课
精备打磨
```

每种模式只影响：

- 追问多少。
- 输出多细。
- 是否生成候选卡。
- 是否分步确认。

不接记忆，不开放模板编辑。

### 第二阶段：本次补充

老师可以输入：

```text
这节课我想重点关注……
不要……
我已有这些材料……
```

系统只把它作为本次生成条件。

### 第三阶段：保存为我的习惯

生成结束后询问：

```text
以后类似备课，也按这种写法吗？
```

教师确认后才写入个人偏好。

### 第四阶段：模板申请

教师可以申请：

```text
把这个结构设为美术组模板
```

需要学科组长或管理员审核。

### 第五阶段：深层模板治理

再考虑：

- 栏目模板。
- 写法模板。
- 校本模板。
- 共享模板。
- 模板版本。
- 审核记录。

## 8. 与当前备课室的结合

### 大单元页面

- 快速出稿：直接生成大单元临时预览。
- 完整备课：包含课标依据、核心素养、表现任务、课时任务链、评价证据、材料支架。
- 精备打磨：先确认课标方向、学生起点、表现任务和课时链，再生成。

### 单课页面

- 快速出稿：直接出一节课预览。
- 完整备课：输出目标、过程、评价证据和材料支架。
- 精备打磨：先确认课堂问题、关键活动、评价证据，再逐段生成。

## 9. 当前禁止

```text
不直接改底层提示词
不开放系统模板编辑
不写个人记忆
不写学校模板
不写数据库
不调用 provider/model
不 formal apply
不接 runtime
不推主项目树
```

## 10. 下一步建议

下一步可以开轻量设计阶段：

```text
1013I_R6O_R1_PREP_MODE_SELECTION_AND_THIS_RUN_NOTES_FIXTURE
```

目标：

```text
老师选择备课模式
老师补一句自己的想法
小教将其转成“本次生成条件”
生成后只展示“是否保存为我的习惯”的入口占位
```

不做：

```text
记忆写入
模板审批
系统 prompt 编辑
管理员后台
真实模型调用
```
"""


def contract_json() -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "product_line": "备课模式与个人化生成习惯",
        "not_prompt_template_editor": True,
        "modes": [
            {"key": "quick_draft", "teacher_label": "快速出稿", "default": False},
            {"key": "complete_prep", "teacher_label": "完整备课", "default": True},
            {"key": "deep_polish", "teacher_label": "精备打磨", "default": False},
        ],
        "teacher_visible_terms": ["本次想法", "我的补充", "这次备课要注意", "小教已记下", "保存为我的习惯"],
        "forbidden_teacher_visible_terms": ["系统提示词", "schema", "模板变量", "prompt", "registry"],
        "memory_layers": ["this_run_only", "personal_preference", "subject_group_template", "school_template", "system_default_template"],
        "permission_layers": ["teacher", "subject_lead", "school_admin", "system_admin"],
        "implementation_phases": [
            "mode_selection_only",
            "this_run_notes",
            "save_as_my_habit_after_confirmation",
            "template_application_with_approval",
            "deep_template_governance",
        ],
        "boundary": boundary(),
    }


def build_result(stage_dir: Path, contract: dict[str, Any]) -> dict[str, Any]:
    plan_text = (stage_dir / PLAN_NAME).read_text(encoding="utf-8")
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "planning_doc_created": (stage_dir / PLAN_NAME).exists(),
        "contract_created": (stage_dir / CONTRACT_NAME).exists(),
        "product_line_marked_as_key_planning": "重点规划" in plan_text or "值得作为备课室重点规划" in plan_text,
        "three_prep_modes_defined": all(text in plan_text for text in ["快速出稿", "完整备课", "精备打磨"]),
        "this_run_notes_defined": all(text in plan_text for text in ["本次想法", "我的补充", "本次生成条件"]),
        "memory_layers_defined": all(text in plan_text for text in ["本次有效", "个人偏好", "学校或学科组模板", "系统默认模板"]),
        "permission_layers_defined": all(role in plan_text for role in ["普通教师", "学科组长", "学校管理员", "系统管理员"]),
        "phased_implementation_defined": all(text in plan_text for text in ["第一阶段：模式选择", "第二阶段：本次补充", "第三阶段：保存为我的习惯", "第四阶段：模板申请", "第五阶段：深层模板治理"]),
        "teacher_language_not_engineering_language": all(term not in contract["teacher_visible_terms"] for term in ["schema", "prompt"]),
        "no_prompt_template_editor_positioning": contract["not_prompt_template_editor"] is True,
        **boundary(),
        "failed_checks": [],
    }
    required = [
        "planning_doc_created",
        "contract_created",
        "product_line_marked_as_key_planning",
        "three_prep_modes_defined",
        "this_run_notes_defined",
        "memory_layers_defined",
        "permission_layers_defined",
        "phased_implementation_defined",
        "teacher_language_not_engineering_language",
        "no_prompt_template_editor_positioning",
    ]
    result["failed_checks"] = [key for key in required if result.get(key) is not True]
    result["final_status"] = FINAL_STATUS if not result["failed_checks"] else "FAIL_1013I_R6O_PREP_MODE_AND_PERSONALIZED_GENERATION_HABIT_PLANNING"
    return result


def write_docs(output_root: Path, stage_dir: Path, result: dict[str, Any]) -> None:
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

```text
REVIEW_STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_RECOMMENDED_STAGE={NEXT_STAGE}
PRODUCT_LINE=备课模式与个人化生成习惯
PLANNING_DOC_CREATED={str(result["planning_doc_created"]).lower()}
THREE_PREP_MODES_DEFINED={str(result["three_prep_modes_defined"]).lower()}
THIS_RUN_NOTES_DEFINED={str(result["this_run_notes_defined"]).lower()}
MEMORY_LAYERS_DEFINED={str(result["memory_layers_defined"]).lower()}
PERMISSION_LAYERS_DEFINED={str(result["permission_layers_defined"]).lower()}
PHASED_IMPLEMENTATION_DEFINED={str(result["phased_implementation_defined"]).lower()}
NOT_PROMPT_TEMPLATE_EDITOR=true
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MEMORY_WRITE_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Summary

R6O records “备课模式与个人化生成习惯” as a key planning line. It defines quick/complete/deep-polish prep modes, this-run teacher notes, memory and permission layers, and a phased rollout that avoids exposing prompt/schema editing to teachers.
""")
    write_text(output_root / "README.md", f"""# PREP_ROOM_RENDER_CANVAS_DEEPEN_V1

Current stage: `{STAGE_ID}`

R6O records the prep-mode and personalized generation-habit planning line.
""")
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", f"""# Review Package Manifest

```text
current_stage={STAGE_ID}
final_status={result["final_status"]}
main_project_pushed=false
```

## Key Files

```text
{STAGE_DIR_NAME}/{PLAN_NAME}
{STAGE_DIR_NAME}/{CONTRACT_NAME}
{STAGE_DIR_NAME}/{RESULT_NAME}
scripts/{VALIDATOR_NAME}
source_delta_1013I_R6O/scripts/{VALIDATOR_NAME}
```
""")
    write_text(stage_dir / "1013I_R6O_report.md", f"""# 1013I_R6O Report

This stage records the prep-mode and personalized generation-habit product line as key planning.

- planning doc created: `{result["planning_doc_created"]}`
- three prep modes defined: `{result["three_prep_modes_defined"]}`
- this-run notes defined: `{result["this_run_notes_defined"]}`
- memory layers defined: `{result["memory_layers_defined"]}`
- permission layers defined: `{result["permission_layers_defined"]}`
- phased implementation defined: `{result["phased_implementation_defined"]}`
- not prompt-template editor: `true`

Boundary: planning only; no provider/model, memory write, database write, prompt-template modification, formal apply, or main-project push.
""")


def validate_result(result: dict[str, Any]) -> None:
    if result.get("failed_checks"):
        raise SystemExit("R6O validation failed: " + ", ".join(result["failed_checks"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    output_root = resolve_output_root(args.root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)

    contract = contract_json()
    write_text(stage_dir / PLAN_NAME, plan_markdown())
    write_json(stage_dir / CONTRACT_NAME, contract)
    result = build_result(stage_dir, contract)
    write_json(stage_dir / RESULT_NAME, result)
    write_docs(output_root, stage_dir, result)

    source_delta = output_root / "source_delta_1013I_R6O" / "scripts"
    source_delta.mkdir(parents=True, exist_ok=True)
    target = source_delta / VALIDATOR_NAME
    if Path(__file__).resolve() != target:
        shutil.copy2(Path(__file__).resolve(), target)

    result = build_result(stage_dir, contract)
    write_json(stage_dir / RESULT_NAME, result)
    write_docs(output_root, stage_dir, result)
    validate_result(result)
    print("ALL_1013I_R6O_PREP_MODE_PLANNING_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["final_status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
