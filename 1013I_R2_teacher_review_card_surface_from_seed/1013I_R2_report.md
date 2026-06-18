# 1013I R2 Teacher Review Card Surface From Seed

- FINAL_STATUS: `PASS_1013I_R2_TEACHER_REVIEW_CARD_SURFACE_FROM_SEED`
- NEXT_STAGE: `1013I_R3_SELF_PREP_PREVIEW_CHAIN_FROM_REVIEW_CARDS`
- Boundary: teacher review surface only; action execution and preview-chain state are deferred to R3.

## Cards

- review_card_count=3
- review_card_ids=review_card_01_candidate_seed_learning_problem_1013I_R1, review_card_02_candidate_seed_material_scaffold_1013I_R1, review_card_03_candidate_seed_review_chain_1013I_R1

## Required UI Data

- Each card includes title, source teacher input, assistant suggestion, why-this-suggestion, risk note, and teacher action options.
- accept_to_preview_option_present=true
- revise_option_present=true
- reject_option_present=true

## Boundary Flags

- accept_to_preview_executed=false
- review_surface_only=true
- teacher_review_required=true
- provider_called=false
- model_called=false
- formal_apply_performed=false
- lesson_body_modified=false
- html_body_modified=false
- database_written=false
- memory_written=false
- feishu_written=false
