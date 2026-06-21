# GPT Review Prompt: 1013K Curriculum To Big Unit Backend Chain

Please review the `1013K` backend review package.

## Decision Target

Check whether the local backend chain correctly moves from curriculum-standard control to big-unit preview render ViewModel, without crossing runtime, provider/model, database, memory, Feishu, or formal-apply boundaries.

## Review Entry Files

Start with:

- `LATEST_REVIEW_ENTRY.md`
- `REVIEW_PACKAGE_MANIFEST.md`
- `1013K_M1_curriculum_to_big_unit_review_milestone_package/1013K_M1_result.json`
- `1013K_M2_big_unit_render_viewmodel_backend_milestone_package/1013K_M2_result.json`
- `1013K_R7_big_unit_preview_surface_to_render_viewmodel_contract/1013K_R7_result.json`
- `1013K_R8_big_unit_render_viewmodel_readonly_endpoint_contract/1013K_R8_result.json`

Then inspect the source deltas:

- `source_delta_1013K_R0/`
- `source_delta_1013K_R1/`
- `source_delta_1013K_R2/`
- `source_delta_1013K_R3/`
- `source_delta_1013K_R4/`
- `source_delta_1013K_R5/`
- `source_delta_1013K_R6/`
- `source_delta_1013K_R7/`
- `source_delta_1013K_R8/`

## Expected Chain

```text
R0: curriculum standard derivation backend contract
R1: in-memory curriculum profile dry run
R2: curriculum profile to candidate envelope
R3: candidate envelope to static big-unit sections
R4: static sections to teacher review surface
M1: R0-R4 milestone package
R5: teacher action state dry run
R6: accepted-preview state to preview surface fixture
R7: preview surface to chunked render ViewModel
R8: future readonly endpoint contract without route registration
M2: R5-R8 milestone package
```

## Must Hold

```text
section_chunks_renderable_independently=true
whole_document_blob_required=false
route_registered=false
runtime_connected=false
provider_called=false
model_called=false
database_written=false
memory_written=false
feishu_written=false
formal_apply_performed=false
unit_package_written=false
lesson_body_modified=false
html_body_modified=false
```

## Review Questions

1. Is the curriculum-standard control layer treated as upstream control rather than content generation?
2. Do textbook-anchor, big-unit-chain, and teacher-confirmation gates block normal generation as intended?
3. Does the degraded-preview path remain clearly preview-only?
4. Does R7 define a chunked ViewModel that can render section-by-section instead of a whole-document blob?
5. Does R8 remain a contract/fixture only, with no route registration or runtime connection?
6. Are any source files or result files leaking provider/model, database, memory, Feishu, or formal-apply behavior?

## Expected Decision Shape

```text
REVIEW_DECISION=ACCEPT | ACCEPT_WITH_MINOR_FIX | HOLD
ACCEPTED_STAGE=1013K_M2_BIG_UNIT_RENDER_VIEWMODEL_BACKEND_MILESTONE_PACKAGE
NEXT_STAGE=1013K_R9_BIG_UNIT_READONLY_ENDPOINT_DRY_RUN_WITHOUT_ROUTE_REGISTRATION
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
ROUTE_REGISTRATION_ALLOWED=false
```
