# 1013L R18 · Teacher Test Entry Milestone Package

## Status

`PASS_1013L_R18_TEACHER_TEST_ENTRY_MILESTONE_PACKAGE`

This milestone packages the existing-page teacher-test line from R16 through R17 and includes the R16A closure of the older R5 review guards.

## Included Stages

- R16: mobile layout polish and teacher test entry.
- R16A: R5 guard closure note for the current line.
- R17: desktop teacher-test smoke for big-unit, courseware edit, and classroom display preview.

## Teacher Entry

Open:

`1013L_R17_existing_page_teacher_test_desktop_smoke_package/prep_room_render_canvas_deepen_v1_1013L_R17_teacher_test_desktop.html`

Suggested URLs:

- Big unit: `?r13=bigUnit`
- Courseware edit: `?mode=edit#coursewareExpanded`
- Display preview: `?preview=display&screen=03#coursewareExpanded`

## Boundary

- Runtime connected: false
- Provider/model called: false
- Database/memory/Feishu written: false
- Formal apply performed: false
- Main project pushed: false

## Validators

From the main project root, the current local validators are:

```text
python scripts/validate_1013L_R16_existing_page_mobile_layout_polish_and_teacher_test_entry.py
python scripts/validate_1013L_R16A_r5_guard_closure_note_for_current_line.py
python scripts/validate_1013L_R17_existing_page_teacher_test_desktop_smoke_package.py
python scripts/validate_1013L_R18_teacher_test_entry_milestone_package.py
```

The review package also contains copies under `scripts/` for path inspection.
