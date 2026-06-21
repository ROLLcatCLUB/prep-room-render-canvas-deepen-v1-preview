# GPT Review Prompt: 1013L R5 Main Shell Fetch Adapter

Please review the fixed GitHub package for:

```text
STAGE=1013L_R5_MAIN_SHELL_BACKEND_VIEWMODEL_READONLY_FETCH_ADAPTER
EXPECTED_STATUS=PASS_1013L_R5_MAIN_SHELL_BACKEND_VIEWMODEL_READONLY_FETCH_ADAPTER
```

Focus on whether the current package preserves the product direction:

```text
one persistent prep-room shell
top menu persistent
middle RenderStage dynamic
bottom Agent input persistent
content pages are RenderStage states
no disconnected new page line
```

Key files:

```text
LATEST_REVIEW_ENTRY.md
REVIEW_PACKAGE_MANIFEST.md
1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/1013L_R5_result.json
1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/main_shell_backend_viewmodel_fetch_contract_1013L_R5.json
1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/main_shell_state_fetch_adapter_map_1013L_R5.json
1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/main_shell_viewmodel_readonly_response_fixture_1013L_R5.json
1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/shiwei_main_render_shell_1013L_R5_fetch_adapter_static.html
source_delta_1013L_R5/
```

Validation expectations:

```text
readonly_fetch_adapter_only=true
new_disconnected_page_created=false
formal_frontend_binding_allowed=false
runtime_connected=false
provider_called=false
model_called=false
database_written=false
memory_written=false
feishu_written=false
formal_apply_performed=false
main_project_pushed=false
```

Please check:

1. R5 reuses the 1013L M1 canonical shell rather than reopening a disconnected page.
2. R5 adds a thin readonly ViewModel fetch adapter only.
3. Big-unit and courseware states reuse existing readonly/fixture sources.
4. Agent routing is normalized through `active_capability`, not visible names.
5. It is reasonable to continue to:

```text
1013L_R6_MAIN_SHELL_READONLY_FETCH_VISIBLE_SMOKE
```
