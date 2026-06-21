# 1013L R10 Existing Page Readonly ViewModel Binding Milestone Package

## Decision

R10 packages the local R7-R9 line as a GitHub-reviewable milestone.

The visible shell remains the existing polished 1013J_R1M prep-room page. R7 maps original interactions to readonly states, R8 injects a hidden static readonly fetch hook, and R9 verifies the hook in Edge headless across the main original page routes.

## Verified Routes

- default existing page -> `single_lesson_design`
- explicit week calendar -> `week_calendar`
- explicit prep notebook -> `single_lesson_design`
- courseware expanded -> `courseware_workspace`
- classroom display preview -> `classroom_display_preview`

## Boundary

No new visible shell, no runtime fetch, no provider/model call, no database/memory/Feishu write, no formal apply, and no main project push.
