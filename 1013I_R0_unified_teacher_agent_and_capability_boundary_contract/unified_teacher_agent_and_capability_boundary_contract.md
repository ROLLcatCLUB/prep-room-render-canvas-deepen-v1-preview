# Unified Teacher Agent and Capability Boundary Contract

- STAGE: `1013I_R0_UNIFIED_TEACHER_AGENT_AND_CAPABILITY_BOUNDARY_CONTRACT`
- Contract type: naming and capability boundary only.
- Runtime/apply status: no provider/model call, no formal apply, no lesson body/html write.

## Canonical Role

```json
{
  "canonical_agent_role": "unified_teacher_agent",
  "current_display_name": "小教",
  "display_name_status": "current_product_name",
  "rename_allowed_before_public_beta": true
}
```

## Teacher-Visible Rule

- Allowed teacher-visible agent name now: `小教`
- Deprecated teacher-visible names: `小备`, `小评`, `小管`, `小美`
- Legacy engineering aliases may remain only in migration maps, historical package names, paths, and review evidence.
- Do not perform global search/replace across repo paths, historical audit packages, validators, or stage names.

## Capability Boundary

- `lesson_prep`: 备课能力
- `classroom_companion`: 课堂伴随能力
- `learning_evidence`: 学习证据能力
- `assessment_review`: 评价能力
- `assessment_summary`: 评价汇总能力
- `resource_retrieval`: 资源检索能力
- `archive`: 归档能力
- `export_draft`: 导出草稿能力

## Next Stage

`1013I_R0A_VISIBLE_NAMING_HOTFIX` should repair current teacher-visible copy only. It must not rename historical paths or perform a broad replacement.
