# Latest Review Entry

```text
REVIEW_STAGE=1013I_R0_UNIFIED_TEACHER_AGENT_PROFILE_AND_CAPABILITY_CONTRACT
FINAL_STATUS=PASS_UNIFIED_TEACHER_AGENT_PROFILE_AND_CAPABILITY_CONTRACT
LATEST_COMPLETED_PRODUCT_STAGE=1013I_R0_UNIFIED_TEACHER_AGENT_PROFILE_AND_CAPABILITY_CONTRACT
SUPERSEDES_STAGE=1013I_R0_UNIFIED_TEACHER_AGENT_AND_CAPABILITY_BOUNDARY_CONTRACT
LATEST_COMPLETED_MODEL_STAGE=1013P_MINIMAX_M3_THINKING_MODES_BENCHMARK
NEXT_RECOMMENDED_STAGE=1013I_R0A_VISIBLE_NAMING_AND_PROFILE_HOTFIX
DEFAULT_MODEL_RECOMMENDATION=MiniMax-M3_WITH_THINKING_DISABLED
DEEP_REASONING_OPTION=MiniMax-M3_WITH_THINKING_ADAPTIVE
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Summary

This entry updates the prep-room review package through the unified teacher-agent profile and capability contract. The current chain is:

```text
1013F_R2D2_CASE_REFERENCE_STRUCTURE_ASSIMILATION
-> 1013F_R2D2_REVIEW_GATE_BEFORE_1013G
-> 1013G_PREP_CANDIDATE_REVIEW_SANDBOX
-> 1013G_TEACHER_REVIEW_PREP_ONLY
-> 1013H_SANDBOX_APPLY_TO_PREVIEW_ONLY
-> 1013I_TEACHER_SELF_PREP_INPUT_MINIMAL_FLOW
-> 1013I_R0_UNIFIED_TEACHER_AGENT_AND_CAPABILITY_BOUNDARY_CONTRACT
-> 1013I_R0_UNIFIED_TEACHER_AGENT_PROFILE_AND_CAPABILITY_CONTRACT
```

1013I_R0 profile contract refines the previous R0 boundary contract. The engineering core is not `小教`; the engineering role is `unified_teacher_agent`. `小教` is only the current default display name, and the contract allows future teacher customization of display name, wake name, voice profile, TTS state, speaking style, tone, and response style.

Function is defined by `capability_key`, identity by `agent_role`, and visible name by `assistant_profile.display_name`.

Start with:

```text
README.md
REVIEW_PACKAGE_MANIFEST.md
1013I_R0_unified_teacher_agent_profile_and_capability_contract/1013I_R0_profile_report.md
1013I_R0_unified_teacher_agent_profile_and_capability_contract/1013I_R0_profile_result.json
1013I_R0_unified_teacher_agent_profile_and_capability_contract/unified_teacher_agent_profile_and_capability_contract.md
1013I_R0_unified_teacher_agent_profile_and_capability_contract/assistant_profile_schema_1013I_R0.json
```

## Accepted Product Baseline

```text
1013F_R2D2_CASE_REFERENCE_STRUCTURE_ASSIMILATION
1013F_R2D2_REVIEW_GATE_BEFORE_1013G
1013G_PREP_CANDIDATE_REVIEW_SANDBOX
1013G_TEACHER_REVIEW_PREP_ONLY
1013H_SANDBOX_APPLY_TO_PREVIEW_ONLY
1013I_TEACHER_SELF_PREP_INPUT_MINIMAL_FLOW
1013I_R0_UNIFIED_TEACHER_AGENT_PROFILE_AND_CAPABILITY_CONTRACT
```

## Current Profile Contract

```text
platform_brand=师维
agent_role=unified_teacher_agent
canonical_engineering_role=unified_teacher_agent
current_default_display_name=小教
display_name_customizable=true
wake_name_customizable=true
voice_profile_future_ready=true
tts_future_ready=true
teacher_visible_agent_names_allowed=["小教"]
deprecated_teacher_visible_agent_names=["小备","小评","小管","小美"]
lesson_prep_capability_key=lesson_prep
xiaobei_legacy_status=deprecated_internal_only
repo_path_rename_required_now=false
global_search_replace_allowed=false
```

## Required New Artifact Shape

```json
{
  "agent_role": "unified_teacher_agent",
  "assistant_profile": {
    "display_name": "小教",
    "display_name_customizable": true,
    "wake_name": "小教",
    "voice_profile_id": null,
    "tts_enabled": false
  },
  "active_space": "prep_room",
  "active_capability": "lesson_prep"
}
```

## Current 1013I Scan

```text
current_1013I_visible_xiaobei_hits_found=true
current_1013I_visible_xiaobei_hits_deferred_to_R0A=true
current_1013I_agent_field_shape_needs_profile_hotfix=true
teacher_visible_xiaobei_hits=[]
teacher_visible_deprecated_agent_hits=[]
```

## Next Recommended Stage

```text
1013I_R0A_VISIBLE_NAMING_AND_PROFILE_HOTFIX
```

If opened, the next stage should repair only current 1013I visible naming and agent-field shape into the profile contract. It should not rename repo paths, historical package names, validators, or prior audit evidence, and should not proceed to candidate-card seeding until the hotfix passes.

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
