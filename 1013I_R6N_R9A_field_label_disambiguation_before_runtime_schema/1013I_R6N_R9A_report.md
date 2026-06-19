# 1013I_R6N_R9A Field Label Disambiguation

FINAL_STATUS=PASS_1013I_R6N_R9A_FIELD_LABEL_DISAMBIGUATION_BEFORE_RUNTIME_SCHEMA
INHERITS_FROM=1013I_R6N_R9_BIG_UNIT_DESIGN_FIELD_MODEL
NEXT_STAGE=1013I_R6O_BIG_UNIT_FIELD_MODEL_TO_PAGE_RENDER_FIXTURE

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

Validation: PASS_1013I_R6N_R9A_FIELD_LABEL_DISAMBIGUATION_BEFORE_RUNTIME_SCHEMA
Failed checks: []
