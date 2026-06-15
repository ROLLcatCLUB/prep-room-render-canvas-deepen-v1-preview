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
ShiweiShell
├─ TopSpaceNav
├─ RenderStage
└─ BottomIntentBar

Current space = prep_room
Current bottom agent = xiaobei_prep_assistant

PrepRoomWorkState
-> composePrepRoomRenderDirective()
-> window.PREP_ROOM_RENDER_VIEW_MODEL
-> RenderStage renders PrepRoomCanvas
```

Current V1 keeps the composer implicit inside the static fixture and exposes the renderer functions on `window` for later adapter work.

## Visual Repair Notes

- View switching now uses a lightweight fade transition on the render layer.
- Week package cards show one primary gap plus two priority actions; secondary collaboration actions move to the floating inspector.
- Month progress cards keep only week, pressure, and keyword on the card; reason appears on hover and full detail remains in the inspector.
- The tool rail includes compact text labels under icons and wraps on tablet/mobile widths.
- The bottom status area uses a global flow step bar for `备课室 -> 教室 -> 作品馆 -> 档案室 -> 回流`.
- The top area now uses a compact product navigation bar and context row; the 小备 input has moved to a bottom chat entry with upload, voice, and send controls.
- The page now follows the shell principle: spaces are states rendered in the center stage, and agents are bottom intent-bar roles rather than room-internal page widgets.
- Visual rule update: week indicators should be prominent, while actions use pill or circular button shapes by default.
- Icon rule update: use a Lucide-like line icon style for circular controls; keep action text in `title` / accessible labels instead of visible button copy.
