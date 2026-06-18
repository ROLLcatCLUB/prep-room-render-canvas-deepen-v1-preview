# Review Package Manifest

```text
package_line=PREP_ROOM_RENDER_CANVAS_DEEPEN_V1
manifest_updated_at=2026-06-18
current_review_entry=LATEST_REVIEW_ENTRY.md
current_handoff=SESSION_HANDOFF_20260618_PREP_ROOM_M3_AND_R2D_NEXT.md
main_project_committed=false
main_project_pushed=false
```

## Purpose

This review package gives the next GPT/Codex session a clean external audit entry for the prep-room render-canvas line, including the accepted prep-notebook reading/editing baseline, content review, Feishu schedule real-time preview caveat, and MiniMax M3 model benchmark results.

## Start Here

```text
README.md
LATEST_REVIEW_ENTRY.md
SESSION_HANDOFF_20260618_PREP_ROOM_M3_AND_R2D_NEXT.md
```

The handoff is the preferred entry for a new session. It records:

- current accepted product baseline;
- current model recommendation;
- Feishu schedule caveat;
- next suggested stage;
- strict no-write/no-formal-apply boundaries.

## Current Product Baseline

Accepted recent prep-notebook stages:

```text
1013F_R2B2_LAYOUT_CLEANUP
1013F_R2C_CLASSROOM_EVENT_DETAIL_POLISH
1013F_R2D_CONTENT_REVIEW_THEN_CASE_REFERENCE_ASSIMILATION
```

Recommended next product stage:

```text
1013F_R2D2_CASE_REFERENCE_STRUCTURE_ASSIMILATION
```

Do not enter:

```text
1013G_TEACHER_REVIEW_ACTIONS
```

unless the user explicitly asks.

## Current Model Baseline

Accepted model line:

```text
1013M_MINIMAX_M3_CONNECTION
1013N_MINIMAX_M3_VS_M27_HIGHSPEED_COMPARISON
1013O_MINIMAX_M3_VS_M27_HIGHSPEED_MULTI_ROUND_BENCHMARK
1013P_MINIMAX_M3_THINKING_MODES_BENCHMARK
```

Current recommendation:

```text
default=MiniMax-M3 + thinking disabled
deep_reasoning=MiniMax-M3 + thinking adaptive
do_not_use=thinking.type enabled
do_not_omit_thinking=true
```

## Included Stage Directories

```text
1013F_R1_teacher_readable_inline_reasoning_surface/
1013F_R2A_information_hierarchy_edit_surface_repair/
1013F_R2B_teacher_readable_copy_and_visual_tone_repair/
1013F_R2B1_edit_bubble_annotation_surface/
1013F_R2B2_layout_cleanup/
1013F_R2C_classroom_event_detail_polish/
1013F_R2D_content_review_then_case_reference_assimilation/
1013F_view_edit_ui_binding/
1013S_feishu_schedule_real_time_binding/
1013M_minimax_m3_connection/
1013N_minimax_m3_vs_m27_highspeed_comparison/
1013O_minimax_m3_vs_m27_highspeed_multi_round/
1013P_minimax_m3_thinking_modes_benchmark/
```

## Included Source Delta Directories

```text
source_delta_1013F/
source_delta_1013F_R1/
source_delta_1013F_R2A/
source_delta_1013F_R2B/
source_delta_1013F_R2B1/
source_delta_1013F_R2B2/
source_delta_1013F_R2C/
source_delta_1013F_R2D/
source_delta_1013S/
source_delta_1013M/
source_delta_1013N/
source_delta_1013O/
source_delta_1013P/
```

## Key Files

```text
prep_room_render_canvas_deepen_v1.html
README.md
LATEST_REVIEW_ENTRY.md
REVIEW_PACKAGE_MANIFEST.md
SESSION_HANDOFF_20260618_PREP_ROOM_M3_AND_R2D_NEXT.md
```

## Important Reports

```text
1013F_R2D_content_review_then_case_reference_assimilation/1013F_R2D_report.md
1013S_feishu_schedule_real_time_binding/1013S_report.md
1013M_minimax_m3_connection/1013M_report.md
1013N_minimax_m3_vs_m27_highspeed_comparison/1013N_report.md
1013O_minimax_m3_vs_m27_highspeed_multi_round/1013O_report.md
1013P_minimax_m3_thinking_modes_benchmark/1013P_report.md
1013P_minimax_m3_thinking_modes_benchmark/1013P_interpretation_note.md
```

## Boundary

```text
review_package_only=true
formal_apply_performed=false
database_written=false
memory_written=false
feishu_written=false
official_export_created=false
official_archive_created=false
entered_1013G=false
main_project_committed=false
main_project_pushed=false
```

## Secret Policy

The package must not include:

- real API keys;
- real APP_SECRET values;
- tenant access tokens;
- bearer tokens;
- cookies;
- server dumps containing secrets.

Provider traces are redacted before upload. Configuration examples may contain placeholder variable names only.

## Review Notes

- R2D found no mature same-topic local case for `1-2《色彩的感觉》`.
- Official Grade 3 resources may be used for calibration.
- Local `渐变的魅力` and `走进青绿山水` are AI-generated or AI-assisted references, useful only for structure-level comparison.
- Feishu live schedule was checked, but local credentials were not configured; the preview uses a local full-dump snapshot plus local school-period time mapping.
- MiniMax M3 is now the recommended default because the multi-round benchmark showed lower latency and at least comparable structured-output quality versus M2.7-highspeed.
