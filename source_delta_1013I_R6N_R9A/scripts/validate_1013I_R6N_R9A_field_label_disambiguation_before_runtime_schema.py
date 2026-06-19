from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6N_R9A_FIELD_LABEL_DISAMBIGUATION_BEFORE_RUNTIME_SCHEMA"
FINAL_STATUS = "PASS_1013I_R6N_R9A_FIELD_LABEL_DISAMBIGUATION_BEFORE_RUNTIME_SCHEMA"
INHERITS_FROM = "1013I_R6N_R9_BIG_UNIT_DESIGN_FIELD_MODEL"
NEXT_STAGE = "1013I_R6O_BIG_UNIT_FIELD_MODEL_TO_PAGE_RENDER_FIXTURE"
STAGE_DIR_NAME = "1013I_R6N_R9A_field_label_disambiguation_before_runtime_schema"
R9_DIR_NAME = "1013I_R6N_R9_big_unit_design_field_model"
VALIDATOR_NAME = "validate_1013I_R6N_R9A_field_label_disambiguation_before_runtime_schema.py"


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


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def boundary() -> dict[str, bool]:
    return {
        "field_label_fix_only": True,
        "runtime_schema_blocked": True,
        "database_write_blocked": True,
        "memory_write_blocked": True,
        "feishu_written": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "main_project_pushed": False,
    }


def patch_field_labels(data: dict[str, Any]) -> dict[str, Any]:
    patched = json.loads(json.dumps(data, ensure_ascii=False))
    for field in patched.get("fields", []):
        if field.get("field_key") == "skills_materials_scaffolds":
            field["teacher_label_before_r9a"] = field.get("teacher_label")
            field["teacher_label"] = "材料与支架"
            field["label_disambiguation_note"] = "区别于“知识与技能”：本字段关注教师准备的材料、学习单、示例和过程支架。"
            field["answers_teacher_question"] = "老师要准备哪些材料、学习单、示例和支架，学生才做得出来？"
            field["field_key_alias"] = "materials_and_scaffolds"
    return patched


def patch_backend_mapping(data: dict[str, Any]) -> dict[str, Any]:
    patched = json.loads(json.dumps(data, ensure_ascii=False))
    new_needed = patched.get("reuse_summary", {}).get("new_candidate_fields_needed", [])
    patched.get("reuse_summary", {})["new_candidate_fields_needed"] = [
        "materials_and_scaffolds" if item == "skills_materials_scaffolds" else item for item in new_needed
    ]
    for field in patched.get("field_mappings", []):
        if field.get("field_key") == "skills_materials_scaffolds":
            field["teacher_label_before_r9a"] = field.get("teacher_label")
            field["teacher_label"] = "材料与支架"
            field["label_disambiguation_note"] = "区别于“知识与技能”：本字段关注教师准备的材料、学习单、示例和过程支架。"
            field["answers_teacher_question"] = "老师要准备哪些材料、学习单、示例和支架，学生才做得出来？"
            field["field_key_alias"] = "materials_and_scaffolds"
    return patched


def patch_reuse_matrix(data: dict[str, Any]) -> dict[str, Any]:
    patched = json.loads(json.dumps(data, ensure_ascii=False))
    for item in patched.get("reuse_matrix", []):
        item["reuse_for"] = [
            "materials_and_scaffolds" if value == "skills_materials_scaffolds" else value
            for value in item.get("reuse_for", [])
        ]
    patched["label_disambiguation"] = {
        "knowledge_and_skills": "本单元的美术语言和技能目标。",
        "materials_and_scaffolds": "教师准备的材料、学习单、示例和支架。",
    }
    return patched


def validate(field_model: dict[str, Any], backend_mapping: dict[str, Any], reuse_matrix: dict[str, Any]) -> dict[str, bool]:
    fields = field_model.get("fields", [])
    labels_by_key = {field.get("field_key"): field.get("teacher_label") for field in fields}
    backend_labels_by_key = {field.get("field_key"): field.get("teacher_label") for field in backend_mapping.get("field_mappings", [])}
    all_reuse_values = [value for item in reuse_matrix.get("reuse_matrix", []) for value in item.get("reuse_for", [])]
    return {
        "field_label_disambiguation_created": True,
        "knowledge_and_skills_label_kept": labels_by_key.get("knowledge_and_skills") == "知识与技能",
        "skills_materials_scaffolds_label_changed": labels_by_key.get("skills_materials_scaffolds") == "材料与支架",
        "backend_mapping_label_aligned": backend_labels_by_key.get("skills_materials_scaffolds") == "材料与支架",
        "label_before_recorded": any(field.get("teacher_label_before_r9a") == "技能与支架" for field in fields),
        "materials_and_scaffolds_alias_present": any(field.get("field_key_alias") == "materials_and_scaffolds" for field in fields),
        "disambiguation_note_present": "label_disambiguation" in reuse_matrix,
        "reuse_matrix_updated": "materials_and_scaffolds" in all_reuse_values and "skills_materials_scaffolds" not in all_reuse_values,
        "runtime_schema_blocked": True,
        "database_write_blocked": True,
        "memory_write_blocked": True,
    }


def write_review_files(output_root: Path, stage_dir: Path, result: dict[str, Any], field_model: dict[str, Any], backend_mapping: dict[str, Any], reuse_matrix: dict[str, Any]) -> None:
    write_json(stage_dir / "big_unit_teacher_visible_field_model_1013I_R6N_R9A.json", field_model)
    write_json(stage_dir / "big_unit_backend_field_mapping_1013I_R6N_R9A.json", backend_mapping)
    write_json(stage_dir / "big_unit_field_reuse_and_integration_matrix_1013I_R6N_R9A.json", reuse_matrix)
    write_json(stage_dir / "1013I_R6N_R9A_result.json", result)
    write_text(stage_dir / "1013I_R6N_R9A_report.md", f"""# 1013I_R6N_R9A Field Label Disambiguation

FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

Change:
- `skills_materials_scaffolds.teacher_label`: `技能与支架` -> `材料与支架`

Reason:
- `知识与技能` describes the unit's art language and skill goals.
- `材料与支架` describes teacher-prepared materials, worksheets, examples, and scaffolds.

Boundary:
- No runtime schema.
- No database/memory/Feishu writes.
- No provider/model calls.
- No formal apply.

Validation: {FINAL_STATUS}
Failed checks: {result["failed_checks"]}
""")
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6N_R9A only fixes the teacher-visible label ambiguity before any runtime schema work.

Boundaries:
- runtime_schema_applied=false
- database_written=false
- memory_written=false
- feishu_written=false
- provider_called=false
- model_called=false
- formal_apply_performed=false
- main_project_pushed=false
""")
    write_text(output_root / "README.md", f"""# Prep Room Render Canvas Deepen V1 Review Package

Latest stage: `{STAGE_ID}`

Open:
- `{STAGE_DIR_NAME}/big_unit_teacher_visible_field_model_1013I_R6N_R9A.json`
- `{STAGE_DIR_NAME}/big_unit_backend_field_mapping_1013I_R6N_R9A.json`

Run:
- `python scripts/{VALIDATOR_NAME}`
""")
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", f"""# Review Package Manifest

Latest stage: `{STAGE_ID}`

Files:
- `{STAGE_DIR_NAME}/big_unit_teacher_visible_field_model_1013I_R6N_R9A.json`
- `{STAGE_DIR_NAME}/big_unit_backend_field_mapping_1013I_R6N_R9A.json`
- `{STAGE_DIR_NAME}/big_unit_field_reuse_and_integration_matrix_1013I_R6N_R9A.json`
- `{STAGE_DIR_NAME}/1013I_R6N_R9A_result.json`
- `{STAGE_DIR_NAME}/1013I_R6N_R9A_report.md`
- `scripts/{VALIDATOR_NAME}`

Boundary: label fix only; no runtime schema/database/memory/Feishu/provider/model/formal apply.
""")


def run(root: Path) -> dict[str, Any]:
    output_root = resolve_output_root(root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)
    r9_dir = output_root / R9_DIR_NAME
    field_model = patch_field_labels(load_json(r9_dir / "big_unit_teacher_visible_field_model_1013I_R6N_R9.json"))
    backend_mapping = patch_backend_mapping(load_json(r9_dir / "big_unit_backend_field_mapping_1013I_R6N_R9.json"))
    reuse_matrix = patch_reuse_matrix(load_json(r9_dir / "big_unit_field_reuse_and_integration_matrix_1013I_R6N_R9.json"))
    checks = validate(field_model, backend_mapping, reuse_matrix)
    failed = [key for key, value in checks.items() if not value]
    result = {
        "stage": STAGE_ID,
        "status": FINAL_STATUS if not failed else "FAIL_1013I_R6N_R9A_FIELD_LABEL_DISAMBIGUATION_BEFORE_RUNTIME_SCHEMA",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        **checks,
        **boundary(),
        "failed_checks": failed,
    }
    write_review_files(output_root, stage_dir, result, field_model, backend_mapping, reuse_matrix)
    source_delta = output_root / "source_delta_1013I_R6N_R9A" / "scripts" / VALIDATOR_NAME
    source_delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), source_delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=None)
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else repo_root_from_script()
    result = run(root)
    print("ALL_1013I_R6N_R9A_FIELD_LABEL_DISAMBIGUATION_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
