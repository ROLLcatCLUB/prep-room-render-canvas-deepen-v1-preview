# 1013L R5 Main Shell Backend ViewModel Readonly Fetch Adapter

## Result

R5 adds a thin readonly fetch adapter for the canonical main shell. It exposes a full shell ViewModel endpoint and per-state ViewModel endpoint, while keeping existing big-unit, single-lesson, courseware, display, material, and schedule work as reusable RenderStage sources.

The visible shell is the previously polished `1013J_R1M` prep-room page. R5 does not replace it with the simplified M1 shell.

## What Changed

- Added `prep_room_main_shell_fetch_adapter_1013L_R5.py`
- Registered readonly routes in `routes.py`
- Generated a static R5 shell copy from the original polished prep-room page with embedded fetch adapter metadata
- Generated contract, adapter map, full response fixture, and state response fixtures
- Generated desktop courseware screenshot smoke for the R5 shell copy

## Boundary

No provider/model call, no runtime write, no database/memory/Feishu write, no formal apply, no formal frontend binding, and no main project push.

## Next

`1013L_R6_MAIN_SHELL_READONLY_FETCH_VISIBLE_SMOKE`
