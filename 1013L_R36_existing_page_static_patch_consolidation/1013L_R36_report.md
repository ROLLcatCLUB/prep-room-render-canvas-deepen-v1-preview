# 1013L R36 · Existing Page Static Patch Consolidation

## Status

`PASS_1013L_R36_EXISTING_PAGE_STATIC_PATCH_CONSOLIDATION`

R36 preserves the old R35 file and creates a consolidated copy. It removes the old R22-R35 patch scripts/styles from the new copy and replaces them with one consolidated static script/style for:

- paragraph-level courseware cards;
- right-rail draft screen selection;
- pointed edit bubble;
- independent left/center/right scrolling.

## Metrics

Before: `{'script_tags': 25, 'style_tags': 16, 'set_interval_count': 12, 'mutation_observer_count': 2, 'query_selector_all_count': 54, 'courseware_screen_var_count': 3, 'bytes': 944035}`

After: `{'script_tags': 13, 'style_tags': 4, 'set_interval_count': 0, 'mutation_observer_count': 1, 'query_selector_all_count': 18, 'courseware_screen_var_count': 3, 'bytes': 851819}`

## Boundary

No runtime/provider/model/database/memory/Feishu/upload/search/material library/whiteboard library/formal apply/main push/GitHub upload.

## In-place small reading fix

After consolidation, R36 was patched in place rather than copied to a new page:

- Teaching-process micro rows now show short teacher-readable summary labels such as "打开感受", "展现差异", "提出概念", and "留下证据".
- "课堂后记" is separated into "教师课后反思" and "小教AI总结"; AI summary remains a candidate and does not replace teacher reflection.
- Prompt direction for later generation: each teaching-process paragraph should carry a compact `micro_title` that states the paragraph's classroom function, not a schema/debug label.
