# 1013K_R7 Big Unit Preview Surface To Render ViewModel Contract Report

STAGE=1013K_R7_BIG_UNIT_PREVIEW_SURFACE_TO_RENDER_VIEWMODEL_CONTRACT
FINAL_STATUS=PASS_1013K_R7_BIG_UNIT_PREVIEW_SURFACE_TO_RENDER_VIEWMODEL_CONTRACT
INHERITS_FROM=1013K_R6_BIG_UNIT_REVIEW_ACTION_STATE_TO_PREVIEW_SURFACE_FIXTURE
NEXT_STAGE=1013K_R8_BIG_UNIT_RENDER_VIEWMODEL_READONLY_ENDPOINT_CONTRACT
LOCAL_ONLY_SMALL_PACKAGE=true
GITHUB_UPLOAD_DEFERRED_UNTIL_NEXT_MILESTONE=true

## Scope

R7 turns the R6 big-unit preview surface into a frontend render ViewModel contract and fixture. The ViewModel is chunk-based, so sections can render and update independently.

## Key Checks

```text
viewmodel_kind=prep_room_big_unit_design_preview
chunk_count=10
mapping_count=10
section_chunks_renderable_independently=true
whole_document_blob_required=false
can_stream_section_by_section=true
can_update_single_section_preview=true
provider_called=false
model_called=false
database_written=false
memory_written=false
formal_apply_performed=false
```

## Validator

validator_pass=true
failed_checks=[]
