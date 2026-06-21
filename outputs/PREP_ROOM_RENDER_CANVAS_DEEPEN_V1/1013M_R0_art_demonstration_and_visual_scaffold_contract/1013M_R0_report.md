# 1013M_R0 Report

## Stage

```text
1013M_R0_ART_DEMONSTRATION_AND_VISUAL_SCAFFOLD_CONTRACT
```

## What Changed

This stage captures the primary-school art teaching requirement around teacher demonstration:

```text
示范不是给学生照抄范画。
示范要解决工具、技法、步骤、视觉标准和创作支架。
```

The stage creates a contract, schema, prompt policy, courseware mapping, and sample fixture for an `art_demonstration_and_visual_scaffold` block.

It also creates a copied static page fixture from R36:

```text
prep_room_render_canvas_deepen_v1_1013M_R0_art_demo_visual_scaffold.html
```

The copied page inserts:

```text
探究
-> 示范与支架
-> 表现
```

## Page-Level Result

The new static page adds a teacher-readable "示范与支架" section with:

```text
明确看点
示范技法
记住口令
辨析错例
借鉴不照抄
```

It keeps the existing R36 page as the rollback baseline and does not overwrite it.

## Backend / Prompt-Level Result

The contract defines required generation fields:

```text
demo_purpose
visual_attention_points
tools_and_techniques
drawing_process_steps
memory_phrase
common_mistakes_and_repairs
peer_example_scaffold
anti_copy_guidance
pre_creation_check
assessment_link
```

The prompt policy requires future generation to produce a concrete demonstration plan instead of generic text such as "教师示范".

## Courseware Mapping

The demonstration block maps to courseware screen candidates:

```text
teacher_demo_screen
step_mantra_screen
mistake_comparison_screen
peer_example_screen
pre_creation_check_screen
```

In the current static page fixture, the new demonstration paragraphs reuse existing right-rail screen draft IDs so this stage does not introduce a disconnected courseware page.

## Boundaries

```text
new_disconnected_page_created=false
r36_baseline_overwritten=false
runtime_connected=false
provider_called=false
model_called=false
database_written=false
memory_written=false
feishu_written=false
formal_apply_performed=false
github_uploaded=false
```

## Next Recommended Step

After user review, the next stage can either:

```text
1013M_R1_ART_DEMONSTRATION_FIELD_TO_GENERATION_REQUEST_ENVELOPE
```

or, if the user wants visible page polish first:

```text
1013M_R0A_ART_DEMONSTRATION_PAGE_READING_POLISH
```

The recommended priority is to connect the contract to the generation request envelope before further visual polish.
