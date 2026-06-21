# 1013K M2 Replay Commands

Run from `D:\Documents\SmartEdu\xiaobei-core`.

1. `python -m py_compile backend\xiaobei_ai\prep_room_big_unit_review_action_state_1013K_R5.py scripts\validate_1013K_R5_big_unit_review_action_state_dry_run.py`
2. `python scripts\validate_1013K_R5_big_unit_review_action_state_dry_run.py`
3. `python -m py_compile backend\xiaobei_ai\prep_room_big_unit_preview_surface_1013K_R6.py scripts\validate_1013K_R6_big_unit_review_action_state_to_preview_surface_fixture.py`
4. `python scripts\validate_1013K_R6_big_unit_review_action_state_to_preview_surface_fixture.py`
5. `python -m py_compile backend\xiaobei_ai\prep_room_big_unit_render_viewmodel_1013K_R7.py scripts\validate_1013K_R7_big_unit_preview_surface_to_render_viewmodel_contract.py`
6. `python scripts\validate_1013K_R7_big_unit_preview_surface_to_render_viewmodel_contract.py`
7. `python -m py_compile backend\xiaobei_ai\prep_room_big_unit_viewmodel_endpoint_contract_1013K_R8.py scripts\validate_1013K_R8_big_unit_render_viewmodel_readonly_endpoint_contract.py`
8. `python scripts\validate_1013K_R8_big_unit_render_viewmodel_readonly_endpoint_contract.py`
9. `python -m py_compile scripts\validate_1013K_M2_big_unit_render_viewmodel_backend_milestone_package.py`
10. `python scripts\validate_1013K_M2_big_unit_render_viewmodel_backend_milestone_package.py`

Expected: every validator prints `ALL_..._CHECKS_OK` and M2 final status is PASS.
