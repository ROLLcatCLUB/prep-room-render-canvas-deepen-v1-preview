# Unified Teacher Agent Profile and Capability Contract

- STAGE: `1013I_R0_UNIFIED_TEACHER_AGENT_PROFILE_AND_CAPABILITY_CONTRACT`
- Contract type: engineering role, assistant profile, and capability boundary.
- Runtime/apply status: no provider/model call, no formal apply, no lesson body/html write.

## Layering

- Platform brand: `师维`
- Engineering role: `unified_teacher_agent`
- Current default display name: `小教`
- User-customizable later: display name, wake name, voice profile, TTS state, speaking style, tone, response style.

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

Do not write new artifacts as only `{"agent":"小教"}`. Function belongs to `capability_key`; identity belongs to `agent_role`; visible name belongs to `assistant_profile.display_name`.

## Capability Keys

- `lesson_prep`: 备课能力
- `classroom_companion`: 课堂伴随能力
- `learning_evidence`: 学习证据能力
- `assessment_review`: 评价能力
- `assessment_summary`: 评价汇总能力
- `resource_retrieval`: 资料能力
- `archive`: 归档能力
- `export_draft`: 导出草稿能力

## Legacy Names

`小备`, `小评`, `小管`, and `小美` are deprecated as teacher-visible independent agents. They may remain in legacy paths, historical audit packages, migration maps, and compatibility aliases only.

## Next Stage

`1013I_R0A_VISIBLE_NAMING_AND_PROFILE_HOTFIX` should repair current 1013I visible naming and agent field shape into the profile contract. It must not rename historical paths or perform broad replacement.
