# 1013I_R6N_R9 Big Unit Field Archive Policy

FINAL_STATUS=PASS_1013I_R6N_R9_BIG_UNIT_DESIGN_FIELD_MODEL
INHERITS_FROM=1013I_R6N_R8_BIG_UNIT_DESIGN_RESTYLED_AS_LESSON_NOTEBOOK_UI

## Decision

本阶段归档的是大单元字段模型和后端映射候选，不是正式 runtime schema，不写数据库，不写 memory，不写 Feishu。

## Archive Layers

1. `big_unit_teacher_visible_field_model_1013I_R6N_R9.json`
   - 教师可见栏目、教学问题、呈现层、资料来源、缺资料动作。

2. `big_unit_backend_field_mapping_1013I_R6N_R9.json`
   - 字段与现有 `unit_package`、课标控制层、官方只读抽取、单课继承落点的候选映射。

3. `big_unit_field_reuse_and_integration_matrix_1013I_R6N_R9.json`
   - 哪些现有后端对象可以复用，哪些只能作为来源参考，哪些需要新增候选字段。

## Reuse Rule

- 优先复用 R6D 的 `unit_package` 作为容器。
- 优先复用 R6E 的官方字段字典作为来源候选。
- 优先复用 R6C 的课标控制层作为上游约束。
- 单课页暂不改 UI，但作为继承落点参考。

## Forbidden

- 不把字段写入正式数据库。
- 不接 runtime/provider/model。
- 不把官方案例或字段候选当作正式教材锚点。
- 不把 raw engineering keys 暴露到主阅读区。
