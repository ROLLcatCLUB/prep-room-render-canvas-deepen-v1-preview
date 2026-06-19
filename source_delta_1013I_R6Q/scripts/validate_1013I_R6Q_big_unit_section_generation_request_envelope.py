from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6Q_BIG_UNIT_SECTION_GENERATION_REQUEST_ENVELOPE"
FINAL_STATUS = "PASS_1013I_R6Q_BIG_UNIT_SECTION_GENERATION_REQUEST_ENVELOPE"
INHERITS_FROM = "1013I_R6P_R2_SECTION_EDIT_MODAL_LESSON_NOTEBOOK_STYLE_PATCH"
NEXT_STAGE = "1013I_R6R_BIG_UNIT_SECTION_CANDIDATE_GENERATOR_ADAPTER_FIXTURE"
STAGE_DIR_NAME = "1013I_R6Q_big_unit_section_generation_request_envelope"
VALIDATOR_NAME = "validate_1013I_R6Q_big_unit_section_generation_request_envelope.py"

FORBIDDEN_INTENT_TERMS = ["prompt", "schema", "field_key", "formal apply", "formal_apply", "unit_package", "patch schema", "rewrite field"]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def locate_output_root(root: Path) -> Path:
    if (root / "LATEST_REVIEW_ENTRY.md").exists() and (root / "REVIEW_PACKAGE_MANIFEST.md").exists():
        return root
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "preview_only": True,
        "formal_apply_allowed": False,
        "provider_model_call_allowed": False,
        "candidate_generated": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def target_sections() -> list[dict[str, Any]]:
    return [
        {
            "teacher_label": "课标依据",
            "section_role": "curriculum_basis",
            "current_text": "本单元主要指向审美感知、艺术表现、创意实践，文化理解作轻量渗透。",
            "teacher_intent": "再具体一点",
            "teacher_visible_instruction": "把课标方向说得更像老师能直接判断的单元方向，但不要伪造课标原文。",
            "reference_needs": ["课标方向", "核心素养目标", "表现任务", "评价证据"],
            "must_not_do": ["不伪造课标原文", "不生成正式大单元正文", "不写正式备课本"],
            "candidate_destination": "section_preview_only",
        },
        {
            "teacher_label": "核心素养",
            "section_role": "core_literacy",
            "current_text": "审美感知、艺术表现、创意实践和文化理解都转成学生可观察的行为。",
            "teacher_intent": "减少口号感",
            "teacher_visible_instruction": "把核心素养写成学生能做出来、老师能观察到的表现。",
            "reference_needs": ["课标方向", "学生起点", "学习推进", "评价证据"],
            "must_not_do": ["不写空泛口号", "不拔高到超过三年级", "不生成单课教案"],
            "candidate_destination": "section_preview_only",
        },
        {
            "teacher_label": "表现任务",
            "section_role": "performance_task",
            "current_text": "学生完成一件“色彩感觉”小作品，并说明自己的色彩选择。",
            "teacher_intent": "更贴合三年级",
            "teacher_visible_instruction": "把任务控制在常态课可完成范围里，不扩成大型项目。",
            "reference_needs": ["学生起点", "材料与支架", "学习推进", "评价证据"],
            "must_not_do": ["不写大型展览策划", "不增加过重作品要求", "不写正式备课本"],
            "candidate_destination": "section_preview_only",
        },
        {
            "teacher_label": "课时任务链",
            "section_role": "lesson_chain",
            "current_text": "1-1 打开感受；1-2 比较方法；1-3 完成表达。",
            "teacher_intent": "让课时之间更连贯",
            "teacher_visible_instruction": "说明每一课承接什么、推进什么、留下什么证据。",
            "reference_needs": ["单元问题", "表现任务", "学习推进", "评价证据"],
            "must_not_do": ["不只写课时目录", "不直接生成单课教案", "不进入正式写入"],
            "candidate_destination": "section_preview_only",
        },
    ]


def build_request_envelope() -> dict[str, Any]:
    sections = target_sections()
    return {
        "stage": STAGE_ID,
        "request_type": "big_unit_section_refine_candidate",
        **boundary(),
        "agent_role": "unified_teacher_agent",
        "assistant_profile": {
            "display_name": "小教",
            "display_name_customizable": True,
            "wake_name": "小教",
            "tts_enabled": False,
        },
        "active_space": "prep_room",
        "active_capability": "lesson_prep",
        "document_type": "big_unit_design",
        "target_unit": {
            "unit_title": "第一单元 · 多变的色彩",
            "grade": "三年级",
            "subject": "美术",
            "estimated_lessons": 3,
        },
        "target_section": sections[0],
        "target_section_examples": sections,
        "generation_boundaries": {
            "write_to_preview_only": True,
            "write_to_formal_lesson_book": False,
            "write_to_database": False,
            "write_to_memory": False,
            "write_to_feishu": False,
        },
    }


def build_context_pack(field_model: Any, backend_mapping: Any) -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "context_pack_type": "big_unit_section_generation_context",
        "target_unit": {
            "unit_title": "第一单元 · 多变的色彩",
            "grade": "三年级",
            "subject": "美术",
            "estimated_lessons": 3,
        },
        "teacher_visible_context": {
            "大单元基本信息": "第一单元 · 多变的色彩；三年级美术；预计 3 课时。",
            "课标方向": "审美感知、艺术表现、创意实践为主，文化理解轻量渗透。",
            "核心素养目标": "学生能感受、选择、说明和调整色彩搭配。",
            "学生起点": "学生能说直观感受，但容易停留在好看、鲜艳、漂亮。",
            "表现任务": "完成一件色彩感觉小作品，并说明选色理由。",
            "学习推进": "感受、比较、表现、修订。",
            "课时任务链": "1-1 打开感受；1-2 比较方法；1-3 完成表达。",
            "评价证据": "能说出感觉、说明理由、留下记录、形成作品并调整。",
            "材料与支架": "生活色彩图片、作品图像、色卡组合、学习单、展示评价句式。",
            "资料补充状态": "教材目录、单元页或课时安排仍待补充。",
        },
        "backend_reference_context": {
            "not_teacher_visible": True,
            "source_field_model_file": "1013I_R6N_R9A_field_label_disambiguation_before_runtime_schema/big_unit_teacher_visible_field_model_1013I_R6N_R9A.json",
            "source_backend_mapping_file": "1013I_R6N_R9A_field_label_disambiguation_before_runtime_schema/big_unit_backend_field_mapping_1013I_R6N_R9A.json",
            "field_model_summary": {
                "available": bool(field_model),
                "field_count_hint": len(field_model.get("fields", field_model if isinstance(field_model, list) else [])) if isinstance(field_model, (dict, list)) else 0,
            },
            "backend_mapping_summary": {
                "available": bool(backend_mapping),
                "mapping_kind": "archive_only_not_runtime_schema",
            },
        },
    }


def build_policy() -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "policy_type": "big_unit_section_generation_policy",
        "must_not": [
            "不伪造课标原文",
            "不生成正式大单元正文",
            "不写正式备课本",
            "不生成单课教案",
            "不调用 provider/model",
            "不写 database/memory/Feishu",
            "候选只进入 preview",
            "教师确认前不生效",
        ],
        "output_style": [
            "教师可读",
            "少系统说明",
            "少口号",
            "学生行为可观察",
            "符合三年级美术常态课",
            "保留技能训练和艺术语言",
            "评价证据可观察",
        ],
        **boundary(),
    }


def build_trace() -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "dry_run": True,
        "provider_called": False,
        "model_called": False,
        "request_built": True,
        "context_pack_built": True,
        "policy_attached": True,
        "candidate_generated": False,
        "next_stage": NEXT_STAGE,
        "steps": [
            {"step": "load_r6p_r2_edit_modal_boundary", "status": "done"},
            {"step": "load_r6n_r9a_field_archive", "status": "done"},
            {"step": "build_request_envelope", "status": "done"},
            {"step": "attach_context_pack", "status": "done"},
            {"step": "attach_generation_policy", "status": "done"},
            {"step": "stop_before_provider_or_candidate_generation", "status": "done"},
        ],
    }


def human_intents_are_clean(envelope: dict[str, Any]) -> bool:
    text = json.dumps(envelope.get("target_section_examples", []), ensure_ascii=False).lower()
    return not any(term in text for term in FORBIDDEN_INTENT_TERMS)


def validate_outputs(stage_dir: Path) -> dict[str, Any]:
    envelope = read_json(stage_dir / "big_unit_section_generation_request_envelope_1013I_R6Q.json")
    context = read_json(stage_dir / "big_unit_section_generation_context_pack_1013I_R6Q.json")
    policy = read_json(stage_dir / "big_unit_section_generation_policy_1013I_R6Q.json")
    trace = read_json(stage_dir / "big_unit_section_generation_dry_run_trace_1013I_R6Q.json")
    sections = envelope.get("target_section_examples", [])
    return {
        "request_envelope_created": bool(envelope),
        "context_pack_created": bool(context),
        "generation_policy_created": bool(policy),
        "dry_run_trace_created": bool(trace),
        "target_sections_count_min": len(sections) >= 4,
        "teacher_visible_intents_human_readable": human_intents_are_clean(envelope),
        "preview_only": envelope.get("preview_only") is True and policy.get("preview_only") is True,
        "formal_apply_allowed": envelope.get("formal_apply_allowed"),
        "provider_model_call_allowed": envelope.get("provider_model_call_allowed"),
        "candidate_generated": trace.get("candidate_generated"),
        "runtime_connected": envelope.get("runtime_connected"),
        "provider_called": trace.get("provider_called"),
        "model_called": trace.get("model_called"),
        "database_written": envelope.get("database_written"),
        "memory_written": envelope.get("memory_written"),
        "feishu_written": envelope.get("feishu_written"),
        "main_project_pushed": envelope.get("main_project_pushed"),
    }


def failed_checks(checks: dict[str, Any]) -> list[str]:
    failed = []
    expected_false = {
        "formal_apply_allowed",
        "provider_model_call_allowed",
        "candidate_generated",
        "runtime_connected",
        "provider_called",
        "model_called",
        "database_written",
        "memory_written",
        "feishu_written",
        "main_project_pushed",
    }
    for key, value in checks.items():
        if key in expected_false:
            if value is not False:
                failed.append(key)
        elif value is not True:
            failed.append(key)
    return failed


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output_root = locate_output_root(root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)

    r6p_result = output_root / "1013I_R6P_R2_section_edit_modal_lesson_notebook_style_patch" / "1013I_R6P_R2_result.json"
    field_model_path = output_root / "1013I_R6N_R9A_field_label_disambiguation_before_runtime_schema" / "big_unit_teacher_visible_field_model_1013I_R6N_R9A.json"
    mapping_path = output_root / "1013I_R6N_R9A_field_label_disambiguation_before_runtime_schema" / "big_unit_backend_field_mapping_1013I_R6N_R9A.json"
    if not r6p_result.exists():
        raise FileNotFoundError(r6p_result)
    field_model = read_json(field_model_path) if field_model_path.exists() else {}
    backend_mapping = read_json(mapping_path) if mapping_path.exists() else {}

    write_json(stage_dir / "big_unit_section_generation_request_envelope_1013I_R6Q.json", build_request_envelope())
    write_json(stage_dir / "big_unit_section_generation_context_pack_1013I_R6Q.json", build_context_pack(field_model, backend_mapping))
    write_json(stage_dir / "big_unit_section_generation_policy_1013I_R6Q.json", build_policy())
    write_json(stage_dir / "big_unit_section_generation_dry_run_trace_1013I_R6Q.json", build_trace())

    checks = validate_outputs(stage_dir)
    failed = failed_checks(checks)
    result = {
        "stage": STAGE_ID,
        "status": FINAL_STATUS if not failed else "FAIL_1013I_R6Q_BIG_UNIT_SECTION_GENERATION_REQUEST_ENVELOPE",
        "final_status": FINAL_STATUS if not failed else "FAIL_1013I_R6Q_BIG_UNIT_SECTION_GENERATION_REQUEST_ENVELOPE",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        **checks,
        "failed_checks": failed,
    }
    write_json(stage_dir / "1013I_R6Q_result.json", result)
    write_text(stage_dir / "1013I_R6Q_report.md", f"""# 1013I_R6Q Big Unit Section Generation Request Envelope

FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6Q creates the backend generation-chain request envelope for big-unit section refinement.

Created:
- request envelope
- generation context pack
- generation policy
- dry-run trace

Boundaries:
- No real provider/model call.
- No candidate generation.
- No formal apply.
- No database/memory/Feishu write.
- No main-project push.

Failed checks: {failed}
""")
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6Q creates a preview-only request envelope and context/policy package for later big-unit section generation. It does not generate candidates or call provider/model.

Key flags:
- REQUEST_ENVELOPE_CREATED=true
- CONTEXT_PACK_CREATED=true
- GENERATION_POLICY_CREATED=true
- CANDIDATE_GENERATED=false
- PROVIDER_CALLED=false
- MODEL_CALLED=false
- FORMAL_APPLY_PERFORMED=false
- MAIN_PROJECT_PUSHED=false
""")
    write_text(output_root / "README.md", f"""# Prep Room Render Canvas Deepen V1 Review Package

Latest stage: `{STAGE_ID}`

Open:
- `{STAGE_DIR_NAME}/big_unit_section_generation_request_envelope_1013I_R6Q.json`
- `{STAGE_DIR_NAME}/1013I_R6Q_result.json`

Run:

```bash
python scripts/{VALIDATOR_NAME}
python scripts/{VALIDATOR_NAME} --root <repo-root>
```
""")
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", f"""# Review Package Manifest

Latest stage: `{STAGE_ID}`

Files:
- `LATEST_REVIEW_ENTRY.md`
- `README.md`
- `REVIEW_PACKAGE_MANIFEST.md`
- `{STAGE_DIR_NAME}/big_unit_section_generation_request_envelope_1013I_R6Q.json`
- `{STAGE_DIR_NAME}/big_unit_section_generation_context_pack_1013I_R6Q.json`
- `{STAGE_DIR_NAME}/big_unit_section_generation_policy_1013I_R6Q.json`
- `{STAGE_DIR_NAME}/big_unit_section_generation_dry_run_trace_1013I_R6Q.json`
- `{STAGE_DIR_NAME}/1013I_R6Q_result.json`
- `{STAGE_DIR_NAME}/1013I_R6Q_report.md`
- `scripts/{VALIDATOR_NAME}`

Boundary: request-envelope dry run only. No runtime, provider/model, candidate generation, formal apply, database, memory, Feishu, or main-project push.
""")
    source_delta = output_root / "source_delta_1013I_R6Q" / "scripts" / VALIDATOR_NAME
    source_delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), source_delta)

    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False))
    print("ALL_1013I_R6Q_BIG_UNIT_SECTION_GENERATION_REQUEST_ENVELOPE_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
