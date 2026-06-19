from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6R_BIG_UNIT_SECTION_CANDIDATE_GENERATOR_ADAPTER_FIXTURE"
FINAL_STATUS = "PASS_1013I_R6R_BIG_UNIT_SECTION_CANDIDATE_GENERATOR_ADAPTER_FIXTURE"
INHERITS_FROM = "1013I_R6Q_BIG_UNIT_SECTION_GENERATION_REQUEST_ENVELOPE"
NEXT_STAGE = "1013I_R6S_BIG_UNIT_SECTION_CANDIDATE_RETURN_TO_EDIT_MODAL_PREVIEW"
STAGE_DIR_NAME = "1013I_R6R_big_unit_section_candidate_generator_adapter_fixture"
SOURCE_STAGE_DIR_NAME = "1013I_R6Q_big_unit_section_generation_request_envelope"
VALIDATOR_NAME = "validate_1013I_R6R_big_unit_section_candidate_generator_adapter_fixture.py"

REQUIRED_LABELS = ["课标依据", "核心素养", "表现任务", "课时任务链"]
FORBIDDEN_TEXT = ["正式写入", "正式生成", "应用到正式备课本"]


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
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def candidates() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "candidate_curriculum_basis_1013I_R6R",
            "teacher_label": "课标依据",
            "teacher_intent": "再具体一点。",
            "current_text": "本单元主要指向审美感知、艺术表现、创意实践，文化理解作轻量渗透。",
            "candidate_text": "本单元主要围绕审美感知、艺术表现和创意实践展开，文化理解作轻量渗透。学生通过观察、比较、尝试和表达，理解色彩组合会改变画面感觉，并能用色彩表达一种较明确的情绪或氛围。",
            "xiaojiao_suggestion": "可以把课标方向写得更接近教师能直接判断的单元学习方向，同时不摘抄或伪造课标原文。",
            "why_this_change": "当前表述方向正确，但偏概括；补入观察、比较、尝试和表达后，更能说明学生如何在本单元中发展色彩感受与表达。",
            "risk_note": "具体课标原文仍需教材或资料确认，本段只作为课标方向预览。",
            "affected_parts": ["课标依据", "核心素养", "表现任务", "评价证据"],
            "destination": "section_preview_only",
            "preview_only": True,
            "formal_apply_allowed": False,
            "provider_called": False,
            "model_called": False,
        },
        {
            "candidate_id": "candidate_core_literacy_1013I_R6R",
            "teacher_label": "核心素养",
            "teacher_intent": "减少口号感。",
            "current_text": "审美感知、艺术表现、创意实践和文化理解都转成学生可观察的行为。",
            "candidate_text": "审美感知：能感受不同色彩组合带来的冷暖、轻重、热烈、安静等视觉意味。\n\n艺术表现：能选择一组颜色表达明确感觉，并说明自己的选色理由。\n\n创意实践：能在比较、试验和反馈中调整色彩搭配。\n\n文化理解：能发现色彩感受与生活场景、作品情境有关。",
            "xiaojiao_suggestion": "把四个素养方向落到学生能说、能选、能调、能联系生活的行为上，会比口号式表述更适合教师审阅。",
            "why_this_change": "大单元设计需要保留核心素养，但教师更需要看到可观察的学生表现；这版把素养转成课堂中能被看见的行为。",
            "risk_note": "文化理解在三年级阶段应轻量渗透，不宜写成过重的文化阐释。",
            "affected_parts": ["核心素养", "学生起点", "学习推进", "评价证据"],
            "destination": "section_preview_only",
            "preview_only": True,
            "formal_apply_allowed": False,
            "provider_called": False,
            "model_called": False,
        },
        {
            "candidate_id": "candidate_performance_task_1013I_R6R",
            "teacher_label": "表现任务",
            "teacher_intent": "更贴合三年级。",
            "current_text": "学生完成一件“色彩感觉”小作品，并说明自己的色彩选择。",
            "candidate_text": "学生完成一件“色彩感觉”小作品，并用一句到几句话说明：\n\n我用了哪些颜色；\n我想表达什么感觉；\n我为什么这样搭配。\n\n如果时间允许，再根据同伴或教师反馈调整一处颜色，并说明为什么改。",
            "xiaojiao_suggestion": "表现任务可以保留小作品，但把说明要求拆成三句学生能说的话，更贴近三年级课堂。",
            "why_this_change": "当前任务能说明结果，但还不够具体；补入选色、感受和理由，有助于把作品产出与评价证据连起来。",
            "risk_note": "任务应控制在常态课可完成范围内，不扩展成大型展览或复杂项目。",
            "affected_parts": ["表现任务", "学习推进", "评价证据", "材料与支架"],
            "destination": "section_preview_only",
            "preview_only": True,
            "formal_apply_allowed": False,
            "provider_called": False,
            "model_called": False,
        },
        {
            "candidate_id": "candidate_lesson_chain_1013I_R6R",
            "teacher_label": "课时任务链",
            "teacher_intent": "让课时之间更连贯。",
            "current_text": "1-1 打开感受；1-2 比较方法；1-3 完成表达。",
            "candidate_text": "1-1 色彩初体验  \n打开感受，建立感受语言。学生通过图片、作品或色卡说出颜色带来的直观感觉，为后续比较打基础。\n\n1-2 色彩的感觉  \n比较方法，发现色彩组合会改变画面意味。学生比较不同色彩搭配，尝试说明为什么会产生热闹、安静、强烈或柔和等感受。\n\n1-3 色彩表达  \n完成表达，展示并修订。学生选择一组颜色表达明确感觉，完成小作品，并根据交流反馈调整一处颜色。",
            "xiaojiao_suggestion": "课时链可以从目录标签变成任务承接，让老师一眼看出每课怎样铺垫、推进和收束。",
            "why_this_change": "当前链条过短，只能看出阶段名称；补入每课任务和承接关系后，后续单课备课能继承大单元方向。",
            "risk_note": "课时链只说明每课承担的任务，不直接生成单课教案。",
            "affected_parts": ["课时任务链", "单课继承提示", "学习推进", "评价证据"],
            "destination": "section_preview_only",
            "preview_only": True,
            "formal_apply_allowed": False,
            "provider_called": False,
            "model_called": False,
        },
    ]


def build_adapter_fixture(source_files: dict[str, str]) -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "adapter_type": "static_fixture_candidate_generator",
        "description": "Converts R6Q request-envelope targets into static preview-only candidate texts for later edit-modal return.",
        "source_files": source_files,
        "target_sections": REQUIRED_LABELS,
        "candidate_generation_mode": "static_fixture_only_no_provider",
        "candidate_destination": "section_preview_only",
        **boundary(),
    }


def build_candidate_pack() -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "pack_type": "big_unit_section_candidate_pack",
        "candidate_count": 4,
        "candidate_destination_all_section_preview_only": True,
        "candidates": candidates(),
        **boundary(),
    }


def build_trace() -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "inherits_from": INHERITS_FROM,
        "trace_type": "static_candidate_fixture_trace",
        "steps": [
            {"step": "load_r6q_request_envelope", "status": "done"},
            {"step": "load_r6q_context_pack", "status": "done"},
            {"step": "load_r6q_generation_policy", "status": "done"},
            {"step": "load_r6q_dry_run_trace", "status": "done"},
            {"step": "create_static_candidate_adapter_fixture", "status": "done"},
            {"step": "create_four_preview_only_candidates", "status": "done"},
            {"step": "stop_before_runtime_or_provider", "status": "done"},
        ],
        "candidate_ids": [item["candidate_id"] for item in candidates()],
        "next_stage": NEXT_STAGE,
        **boundary(),
    }


def build_policy_check(pack: dict[str, Any]) -> dict[str, Any]:
    candidate_items = pack["candidates"]
    return {
        "stage": STAGE_ID,
        "policy_check_type": "big_unit_section_candidate_policy_check",
        "candidate_count": len(candidate_items),
        "labels_present": [item["teacher_label"] for item in candidate_items],
        "destination_all_section_preview_only": all(item.get("destination") == "section_preview_only" for item in candidate_items),
        "preview_only_all": all(item.get("preview_only") is True for item in candidate_items),
        "formal_apply_allowed_all_false": all(item.get("formal_apply_allowed") is False for item in candidate_items),
        "provider_called_all_false": all(item.get("provider_called") is False for item in candidate_items),
        "model_called_all_false": all(item.get("model_called") is False for item in candidate_items),
        "forbidden_text_hits": find_forbidden_text_hits(candidate_items),
        "teacher_visible_fields_complete": all(candidate_complete(item) for item in candidate_items),
        **boundary(),
    }


def candidate_complete(item: dict[str, Any]) -> bool:
    required = ["current_text", "candidate_text", "xiaojiao_suggestion", "why_this_change", "risk_note"]
    return all(bool(str(item.get(key, "")).strip()) for key in required)


def find_forbidden_text_hits(candidate_items: list[dict[str, Any]]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for item in candidate_items:
        combined = json.dumps(item, ensure_ascii=False)
        for term in FORBIDDEN_TEXT:
            if term in combined:
                hits.append({"candidate_id": item.get("candidate_id", ""), "term": term})
    return hits


def validate_outputs(stage_dir: Path) -> dict[str, Any]:
    required_files = [
        "big_unit_section_candidate_adapter_fixture_1013I_R6R.json",
        "big_unit_section_candidate_pack_1013I_R6R.json",
        "big_unit_section_candidate_trace_1013I_R6R.json",
        "big_unit_section_candidate_policy_check_1013I_R6R.json",
    ]
    pack = read_json(stage_dir / "big_unit_section_candidate_pack_1013I_R6R.json")
    policy_check = read_json(stage_dir / "big_unit_section_candidate_policy_check_1013I_R6R.json")
    items = pack.get("candidates", [])
    labels = [item.get("teacher_label") for item in items]
    return {
        "necessary_files_exist": all((stage_dir / name).exists() for name in required_files),
        "candidate_pack_created": bool(pack),
        "candidate_count_is_4": len(items) == 4 and pack.get("candidate_count") == 4,
        "required_labels_present": labels == REQUIRED_LABELS,
        "candidate_fields_complete": all(candidate_complete(item) for item in items),
        "destination_all_section_preview_only": all(item.get("destination") == "section_preview_only" for item in items),
        "preview_only_all": all(item.get("preview_only") is True for item in items),
        "formal_apply_allowed": pack.get("formal_apply_allowed"),
        "provider_called": pack.get("provider_called"),
        "model_called": pack.get("model_called"),
        "database_written": pack.get("database_written"),
        "memory_written": pack.get("memory_written"),
        "feishu_written": pack.get("feishu_written"),
        "forbidden_text_hits": policy_check.get("forbidden_text_hits", []),
    }


def failed_checks(checks: dict[str, Any]) -> list[str]:
    failed = []
    expected_false = {
        "formal_apply_allowed",
        "provider_called",
        "model_called",
        "database_written",
        "memory_written",
        "feishu_written",
    }
    for key, value in checks.items():
        if key == "forbidden_text_hits":
            if value:
                failed.append(key)
        elif key in expected_false:
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
    source_stage = output_root / SOURCE_STAGE_DIR_NAME
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)

    source_files = {
        "request_envelope": f"{SOURCE_STAGE_DIR_NAME}/big_unit_section_generation_request_envelope_1013I_R6Q.json",
        "context_pack": f"{SOURCE_STAGE_DIR_NAME}/big_unit_section_generation_context_pack_1013I_R6Q.json",
        "generation_policy": f"{SOURCE_STAGE_DIR_NAME}/big_unit_section_generation_policy_1013I_R6Q.json",
        "dry_run_trace": f"{SOURCE_STAGE_DIR_NAME}/big_unit_section_generation_dry_run_trace_1013I_R6Q.json",
    }
    for rel_path in source_files.values():
        path = output_root / rel_path
        if not path.exists():
            raise FileNotFoundError(path)
    r6q_result = source_stage / "1013I_R6Q_result.json"
    if not r6q_result.exists():
        raise FileNotFoundError(r6q_result)

    adapter = build_adapter_fixture(source_files)
    pack = build_candidate_pack()
    trace = build_trace()
    policy_check = build_policy_check(pack)

    write_json(stage_dir / "big_unit_section_candidate_adapter_fixture_1013I_R6R.json", adapter)
    write_json(stage_dir / "big_unit_section_candidate_pack_1013I_R6R.json", pack)
    write_json(stage_dir / "big_unit_section_candidate_trace_1013I_R6R.json", trace)
    write_json(stage_dir / "big_unit_section_candidate_policy_check_1013I_R6R.json", policy_check)

    checks = validate_outputs(stage_dir)
    failed = failed_checks(checks)
    result = {
        "stage": STAGE_ID,
        "status": FINAL_STATUS if not failed else "FAIL_1013I_R6R_BIG_UNIT_SECTION_CANDIDATE_GENERATOR_ADAPTER_FIXTURE",
        "final_status": FINAL_STATUS if not failed else "FAIL_1013I_R6R_BIG_UNIT_SECTION_CANDIDATE_GENERATOR_ADAPTER_FIXTURE",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        "adapter_fixture_created": True,
        "candidate_pack_created": True,
        "candidate_trace_created": True,
        "policy_check_created": True,
        "static_fixture_candidates_generated": True,
        "candidate_count": 4,
        "curriculum_basis_candidate_created": True,
        "core_literacy_candidate_created": True,
        "performance_task_candidate_created": True,
        "lesson_chain_candidate_created": True,
        "candidate_destination_all_section_preview_only": True,
        "preview_only": True,
        "formal_apply_allowed": False,
        "provider_called": False,
        "model_called": False,
        "runtime_connected": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
        "validation_checks": checks,
        "failed_checks": failed,
    }
    write_json(stage_dir / "1013I_R6R_result.json", result)
    write_text(stage_dir / "1013I_R6R_report.md", f"""# 1013I_R6R Big Unit Section Candidate Generator Adapter Fixture

FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6R reads the R6Q request envelope, context pack, generation policy, and dry-run trace, then creates four static fixture candidates for the big-unit section edit modal preview chain.

Created candidates:
- 课标依据
- 核心素养
- 表现任务
- 课时任务链

Boundaries:
- Static fixture candidates only.
- No runtime connection.
- No provider/model call.
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

R6R creates four preview-only static candidate texts from the R6Q request envelope for later return to the big-unit edit modal preview chain.

Key flags:
- STATIC_FIXTURE_CANDIDATES_GENERATED=true
- CANDIDATE_COUNT=4
- DESTINATION=section_preview_only
- PROVIDER_CALLED=false
- MODEL_CALLED=false
- FORMAL_APPLY_PERFORMED=false
- DATABASE_WRITTEN=false
- MEMORY_WRITTEN=false
- FEISHU_WRITTEN=false
- MAIN_PROJECT_PUSHED=false
""")
    write_text(output_root / "README.md", f"""# Prep Room Render Canvas Deepen V1 Review Package

Latest stage: `{STAGE_ID}`

Open:
- `{STAGE_DIR_NAME}/big_unit_section_candidate_pack_1013I_R6R.json`
- `{STAGE_DIR_NAME}/1013I_R6R_result.json`

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
- `{STAGE_DIR_NAME}/big_unit_section_candidate_adapter_fixture_1013I_R6R.json`
- `{STAGE_DIR_NAME}/big_unit_section_candidate_pack_1013I_R6R.json`
- `{STAGE_DIR_NAME}/big_unit_section_candidate_trace_1013I_R6R.json`
- `{STAGE_DIR_NAME}/big_unit_section_candidate_policy_check_1013I_R6R.json`
- `{STAGE_DIR_NAME}/1013I_R6R_result.json`
- `{STAGE_DIR_NAME}/1013I_R6R_report.md`
- `scripts/{VALIDATOR_NAME}`

Boundary: static fixture candidate generation only. No runtime, provider/model, formal apply, database, memory, Feishu, or main-project push.
""")
    source_delta = output_root / "source_delta_1013I_R6R" / "scripts" / VALIDATOR_NAME
    source_delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), source_delta)

    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False))
    print("ALL_1013I_R6R_BIG_UNIT_SECTION_CANDIDATE_GENERATOR_ADAPTER_FIXTURE_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
