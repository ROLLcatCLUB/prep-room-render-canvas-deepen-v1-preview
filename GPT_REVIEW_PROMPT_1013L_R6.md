# GPT Review Prompt: 1013L R6 Original UI Fetch Visible Smoke

Please review the fixed GitHub package for:

```text
STAGE=1013L_R6_MAIN_SHELL_ORIGINAL_UI_READONLY_FETCH_VISIBLE_SMOKE
EXPECTED_STATUS=PASS_1013L_R6_MAIN_SHELL_ORIGINAL_UI_READONLY_FETCH_VISIBLE_SMOKE
```

Context:

```text
R5 originally risked looking like a newly created simplified shell.
The corrected line must preserve the previously polished prep-room page as the visible shell.
The readonly fetch adapter may be injected as hidden metadata only.
```

Key checks:

```text
original_horizontal_tool_strip_preserved=true
original_view_tabs_preserved=true
original_data_view_switching_preserved=true
courseware_expanded_route_preserved=true
bottom_agent_input_preserved=true
fetch_adapter_metadata_present=true
new_shell_standard_created=false
simplified_shell_used_as_visible_shell=false
```

Key files:

```text
LATEST_REVIEW_ENTRY.md
REVIEW_PACKAGE_MANIFEST.md
1013L_R6_main_shell_original_ui_readonly_fetch_visible_smoke/1013L_R6_result.json
1013L_R6_main_shell_original_ui_readonly_fetch_visible_smoke/prep_room_render_canvas_deepen_v1_1013L_R6_original_ui_fetch_visible_smoke.html
1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/1013L_R5_result.json
1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/shiwei_main_render_shell_1013L_R5_fetch_adapter_static.html
source_delta_1013L_R6/
```

Please confirm:

1. The visible shell is the prior polished prep-room page, not a newly invented simplified shell.
2. The horizontal AI tool strip and original switching mechanism are preserved.
3. The R5 readonly fetch adapter remains present as hidden metadata.
4. No runtime/provider/model/database/memory/Feishu/formal apply happened.
5. It is reasonable to continue to:

```text
1013L_R7_MAIN_SHELL_READONLY_FETCH_ADAPTER_TO_ORIGINAL_PAGE_INTERACTION_BINDING_PLAN
```
