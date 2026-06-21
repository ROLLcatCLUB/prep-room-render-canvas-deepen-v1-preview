# 1013L_R0 Main Render Shell Backend Reuse Registry

## Conclusion

`1013L_R0` passes as a shell/backend reuse registry stage. It does not continue visible rendering into `1013K_R30`; instead it pauses that path and locks the next step as a canonical main shell promotion plan.

## Backup

A full Z-drive snapshot was created before this stage:

- `Z:/SmartEdu_Backups/xiaobei-core/full_snapshot_20260621_125633`
- `Z:/SmartEdu_Backups/xiaobei-core/SNAPSHOT_20260621_125633_BEFORE_1013L.md`

Verification matched source and snapshot: `40535` files and `1862809866` bytes on both sides.

## What This Stage Adds

- A read-only render shell registry backend module.
- A new registered route: `/api/prep-room/render-shell/registry`.
- A state lookup route: `/api/prep-room/render-shell/state/<state_id>`.
- A RenderStage registry for home, prep notebook, big unit design, single lesson design, courseware workspace, classroom display preview, material intake, and week calendar.
- A backend reuse matrix so future work reuses existing 071B, 1013K, 1013J, KB, subject-pack, and schedule assets instead of rewriting.
- A unified renameable agent policy. `??` and `??` are treated as legacy/display names, not route keys.

## Backend Reuse Decision

Reusable now:

- `workbench_preview_viewmodel_builder_071B` for safe ViewModel and gate normalization.
- `prep_room_big_unit_*_1013K` for curriculum, big-unit, preview, chunked readonly rendering, and fetch adapter contracts.
- `1013K_R25-R29A` courseware viewmodel assets for courseware RenderStage state.
- `official_unit_field_dictionary_v1`, `subject_packs/art`, `business_packs/education`, and `knowledge-base` for field/source grounding.
- `prep_room_feishu_schedule_1013A` for readonly schedule context.

Needs thin adapters later:

- single lesson inheritance from big-unit context.
- courseware viewmodel visible rendering into the canonical shell.
- material intake once upload/search gates are approved.

## Boundary

No runtime/provider/model/database/memory/Feishu/formal apply was performed. No new disconnected static page was created. No GitHub upload was performed.
