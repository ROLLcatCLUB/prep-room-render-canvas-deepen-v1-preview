# 1013I R0A Visible Naming And Profile Hotfix

- FINAL_STATUS: `PASS_1013I_R0A_VISIBLE_NAMING_AND_PROFILE_HOTFIX`
- NEXT_STAGE: `1013I_R1_CANDIDATE_CARD_SEED_FROM_SELF_PREP_REQUEST`
- Boundary: current 1013I successor artifacts only; no global replacement, no runtime/provider/model, no formal apply.

## Hotfix Scope

- Replace teacher-visible deprecated assistant name in current 1013I successor artifacts.
- Upgrade old `agent` field shape to `agent_role + assistant_profile + active_space + active_capability`.
- Preserve original 1013I artifacts as historical input; R1 should read the R0A successor artifacts.

## Result

- original_deprecated_visible_hit_count=3
- deprecated_visible_hit_count_after_hotfix=0
- legacy_agent_field_after_hotfix=false
- agent_role=unified_teacher_agent
- current_default_display_name=小教
- active_capability=lesson_prep

## Boundary Flags

- original_1013I_artifacts_modified=false
- global_search_replace_performed=false
- repo_path_rename_performed=false
- provider_called=false
- model_called=false
- formal_apply_performed=false
- lesson_body_modified=false
- html_body_modified=false
- database_written=false
- memory_written=false
- feishu_written=false
