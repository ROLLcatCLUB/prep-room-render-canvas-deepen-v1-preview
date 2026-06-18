# 1013I R5B Big Unit Context Node Record

- FINAL_STATUS: `PASS_1013I_R5B_BIG_UNIT_CONTEXT_NODE_RECORD`
- NEXT_STAGE: `1013I_R6_TEACHER_SELF_PREP_RENDER_SURFACE_ALPHA_WITH_BIG_UNIT_PLACEHOLDER`
- Scope: contract-only / fixture-only record of the big-unit context node.

## Why This Node Exists

The teacher self-prep chain cannot treat a lesson as isolated. Before candidate cards are generated, the system must reserve a check for the lesson's position inside the larger unit.

Original chain:

```text
teacher_input -> review_cards -> preview_only
```

Revised chain:

```text
teacher_input -> big_unit_context_check -> lesson_position_judgement -> review_cards -> preview_only
```

## Future Hook

- Official big-unit materials may be read later through a read-only extraction chain.
- R5B does not parse real official materials.
- If big-unit materials are missing, the UI may continue single-lesson prep with a visible recommendation to supplement unit context.
- R6 must reserve a big-unit position placeholder if render surface work continues.

## Boundary

- actual_material_parsing_performed=false
- provider_called=false
- model_called=false
- formal_apply_performed=false
- lesson_body_modified=false
- html_body_modified=false
- database_written=false
- memory_written=false
- feishu_written=false
- official_export_created=false
- official_archive_created=false
