# Latest Review Entry

```text
REVIEW_STAGE=1013I_R0_UNIFIED_TEACHER_AGENT_AND_CAPABILITY_BOUNDARY_CONTRACT
FINAL_STATUS=PASS_UNIFIED_TEACHER_AGENT_AND_CAPABILITY_BOUNDARY_CONTRACT
LATEST_COMPLETED_PRODUCT_STAGE=1013I_R0_UNIFIED_TEACHER_AGENT_AND_CAPABILITY_BOUNDARY_CONTRACT
LATEST_COMPLETED_MODEL_STAGE=1013P_MINIMAX_M3_THINKING_MODES_BENCHMARK
NEXT_RECOMMENDED_STAGE=1013I_R0A_VISIBLE_NAMING_HOTFIX
DEFAULT_MODEL_RECOMMENDATION=MiniMax-M3_WITH_THINKING_DISABLED
DEEP_REASONING_OPTION=MiniMax-M3_WITH_THINKING_ADAPTIVE
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Summary

This entry updates the prep-room review package through the unified teacher-agent and capability-boundary contract. The current chain is:

```text
1013F_R2D2_CASE_REFERENCE_STRUCTURE_ASSIMILATION
-> 1013F_R2D2_REVIEW_GATE_BEFORE_1013G
-> 1013G_PREP_CANDIDATE_REVIEW_SANDBOX
-> 1013G_TEACHER_REVIEW_PREP_ONLY
-> 1013H_SANDBOX_APPLY_TO_PREVIEW_ONLY
-> 1013I_TEACHER_SELF_PREP_INPUT_MINIMAL_FLOW
-> 1013I_R0_UNIFIED_TEACHER_AGENT_AND_CAPABILITY_BOUNDARY_CONTRACT
```

1013I_R0 freezes the teacher-visible naming and backend capability boundary before candidate-card seeding continues. It records the canonical role as `unified_teacher_agent`, the current display name as `小教`, and keeps public-beta rename room through `rename_allowed_before_public_beta=true`.

It also deprecates `小备`, `小评`, `小管`, and `小美` as teacher-visible front-stage agent names. Legacy names may remain only as internal/historical aliases in migration maps, existing paths, audit packages, and review evidence. R0 explicitly forbids global search/replace.

The scan found current 1013I visible `小备` hits and deferred those to `1013I_R0A_VISIBLE_NAMING_HOTFIX`. R0 does not edit the 1013I files.

Start with:

```text
README.md
REVIEW_PACKAGE_MANIFEST.md
1013I_R0_unified_teacher_agent_and_capability_boundary_contract/1013I_R0_report.md
1013I_R0_unified_teacher_agent_and_capability_boundary_contract/1013I_R0_result.json
1013I_R0_unified_teacher_agent_and_capability_boundary_contract/unified_teacher_agent_and_capability_boundary_contract.md
```

## Accepted Product Baseline

```text
1013F_R2D2_CASE_REFERENCE_STRUCTURE_ASSIMILATION
1013F_R2D2_REVIEW_GATE_BEFORE_1013G
1013G_PREP_CANDIDATE_REVIEW_SANDBOX
1013G_TEACHER_REVIEW_PREP_ONLY
1013H_SANDBOX_APPLY_TO_PREVIEW_ONLY
1013I_TEACHER_SELF_PREP_INPUT_MINIMAL_FLOW
1013I_R0_UNIFIED_TEACHER_AGENT_AND_CAPABILITY_BOUNDARY_CONTRACT
```

## Current Naming Contract

```text
canonical_agent_role=unified_teacher_agent
current_display_name=小教
teacher_visible_agent_names_allowed=["小教"]
deprecated_teacher_visible_agent_names=["小备","小评","小管","小美"]
lesson_prep_capability_key=lesson_prep
xiaobei_legacy_status=deprecated_internal_only
legacy_alias_allowed_only_in_migration_map=true
repo_path_rename_required_now=false
global_search_replace_allowed=false
```

## Current 1013I Scan

```text
current_1013I_visible_xiaobei_hits_found=true
current_1013I_visible_xiaobei_hits_deferred_to_R0A=true
teacher_visible_xiaobei_hits=[]
teacher_visible_deprecated_agent_hits=[]
```

## Next Recommended Stage

```text
1013I_R0A_VISIBLE_NAMING_HOTFIX
```

If opened, the next stage should repair the current 1013I teacher-visible naming hits only. It should not rename repo paths, historical package names, validators, or prior audit evidence, and should not proceed to candidate-card seeding until the naming hotfix passes.

## Boundary

```text
provider_called=false
model_called=false
formal_apply_performed=false
lesson_body_modified=false
html_body_modified=false
database_written=false
memory_written=false
feishu_written=false
official_export_created=false
official_archive_created=false
main_project_committed=false
main_project_pushed=false
```
