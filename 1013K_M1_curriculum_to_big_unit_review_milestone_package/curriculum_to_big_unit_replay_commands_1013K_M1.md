# 1013K M1 Replay Commands

Run from `D:\Documents\SmartEdu\xiaobei-core`.

1. `python -m py_compile backend\xiaobei_ai\prep_room_curriculum_standard_derivation_1013K_R0.py scripts\validate_1013K_R0_curriculum_standard_derivation_backend_contract.py`
2. `python scripts\validate_1013K_R0_curriculum_standard_derivation_backend_contract.py`
3. `python -m py_compile backend\xiaobei_ai\prep_room_curriculum_derivation_runtime_dry_run_1013K_R1.py scripts\validate_1013K_R1_curriculum_derivation_profile_runtime_dry_run.py`
4. `python scripts\validate_1013K_R1_curriculum_derivation_profile_runtime_dry_run.py`
5. `python -m py_compile backend\xiaobei_ai\prep_room_curriculum_profile_candidate_envelope_1013K_R2.py scripts\validate_1013K_R2_curriculum_profile_to_big_unit_candidate_envelope.py`
6. `python scripts\validate_1013K_R2_curriculum_profile_to_big_unit_candidate_envelope.py`
7. `python -m py_compile backend\xiaobei_ai\prep_room_big_unit_static_section_preview_1013K_R3.py scripts\validate_1013K_R3_big_unit_candidate_envelope_to_static_section_preview.py`
8. `python scripts\validate_1013K_R3_big_unit_candidate_envelope_to_static_section_preview.py`
9. `python -m py_compile backend\xiaobei_ai\prep_room_big_unit_review_surface_1013K_R4.py scripts\validate_1013K_R4_static_section_preview_to_review_surface_fixture.py`
10. `python scripts\validate_1013K_R4_static_section_preview_to_review_surface_fixture.py`
11. `python -m py_compile scripts\validate_1013K_M1_curriculum_to_big_unit_review_milestone_package.py`
12. `python scripts\validate_1013K_M1_curriculum_to_big_unit_review_milestone_package.py`

Expected: every validator prints `ALL_..._CHECKS_OK` and M1 final status is PASS.
