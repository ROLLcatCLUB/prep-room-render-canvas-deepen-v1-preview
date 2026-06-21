# 1013L R16A · R5 Guard Closure Note For Current Line

## Decision

`PASS_1013L_R16A_R5_GUARD_CLOSURE_NOTE_FOR_CURRENT_LINE`

This package reviews the older R5 GPT guard feedback against the current R13/R16 existing-page line. It does not create a new page, connect runtime, call provider/model, or write any database/memory/Feishu state.

## Guard A · Visible Agent Name

Current visible courseware/prep-room phrases have been moved to `小教` where they were still teacher-facing (`小教草稿`, `对小教说一句`). Legacy hidden adapter JSON may still include `小备` as a customizable profile value; that is recorded as legacy data, not a routing key.

## Guard B · State Count

R5 registry has 8 states while the fetch adapter has 7. The registry-only state is `prep_notebook`, treated as an alias/envelope for the existing single-lesson notebook surface. The concrete readonly fetch state remains `single_lesson_design` unless a distinct runtime need appears.

## Guard C · Route Evidence

The current line remains static hydration. Runtime route smoke is therefore held, not skipped: before real runtime binding, create an independent route map/fetch smoke for the concrete state endpoints.

## Boundary

- Runtime connected: false
- Provider/model called: false
- Database/memory/Feishu written: false
- Formal apply performed: false
- Main project pushed: false
- GitHub uploaded: false
