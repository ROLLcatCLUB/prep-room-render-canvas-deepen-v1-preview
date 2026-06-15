# PREP_ROOM_RENDER_CANVAS_DEEPEN_V1

This package turns the v5 prep-room static preview into a render-canvas preview.

## Files

- `prep_room_render_canvas_deepen_v1.html`

## Preview Boundary

- Static fixture only.
- No API call.
- No model/provider call.
- No database, memory, Feishu, export, or formal apply.
- Teacher review is required for every pending change.

## Reused Project Patterns

- `frontend/home.html`: scene-level ViewModel plus renderer function split.
- `frontend/xiaojiao-preview.html`: work state to render directive to surface renderer idea.
- `docs/foundation/xiaojiao_dynamic_work_panel_contract_1000C.md`: dynamic panel / inspector contract direction.
- `docs/foundation/xiaojiao_core_pack_to_preview_surface_contract_1012C.md`: render directive safety shape.
- `backend/xiaobei_ai/workbench_preview_viewmodel_builder_071B.py`: preview safety flags and teacher-review boundary.

## Canvas Shape

```text
PrepRoomWorkState
-> composePrepRoomRenderDirective()
-> window.PREP_ROOM_RENDER_VIEW_MODEL
-> renderPrepRoomCanvas()
-> renderWeekPackageCanvas()
-> renderMonthProgressCanvas()
-> renderFlexibleSemesterMapCanvas()
```

Current V1 keeps the composer implicit inside the static fixture and exposes the renderer functions on `window` for later adapter work.
