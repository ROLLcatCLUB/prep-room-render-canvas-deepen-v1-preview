# 1013E_R3 Prompt Template

## System Prompt

你是师维备课室的小备。你的任务是推演课堂如何发生，只输出 JSON 候选，不写整篇教案，不做正式应用。

## Sample User Prompt

{"task":"把教师意图推演成课时展开图。只返回 JSON，不写完整教案。","case":{"case_id":"standard_daily_cold_warm_more_visual","lesson_design_mode":"standard_daily","grade":"三年级","subject":"美术","unit":"色彩单元","topic":"1-2《色彩的感觉》","duration_minutes":40,"lesson_position":"unit_middle","teacher_input":"学生对冷暖色不太理解，要设计得更直观一点。","student_baseline":"学生知道常见颜色，也会说喜欢，但冷暖色理解停在表层。","expected_focus":["冷暖色","直观材料","探究","学习单","评价证据"]},"output_shape":{"lesson_unfolding_graph":{"lesson_design_mode":"string","design_context":{"grade":"三年级","subject":"美术","topic":"1-2《色彩的感觉》"},"cognitive_grounding":{"core_learning_problem":"string","student_baseline":"string","real_stuck_point":"string","target_shift":"从...到...","key_focus":"string","key_difficulty":"string"},"constraints":{"total_duration_minutes":40,"resource_budget":"low|medium|high","class_condition":"string","lesson_position":"unit_middle","material_conditions":["string"]},"main_event_sequence":["E1"],"classroom_events":[{"event_id":"E1","event_name":"string","duration":{"recommended_minutes":5,"min_minutes":3,"max_minutes":7,"time_risk":"string"},"execution_view":{"teacher_focus_cue":"老师可直接说的一句话","core_question":"string","student_task":"string","teacher_summary_sentence":"string"},"design_view":{"learning_purpose":"string","design_intent":"string","student_state_before":"string","student_state_after":"string","teacher_action":"string","student_action":"string","big_screen_state":"string","textbook_or_material_state":"string","learning_sheet_state":"string","assessment_evidence":"string","transition_from_previous":"string","transition_to_next":"string","risk_and_adjustment":"string"},"student_response_model":[{"type":"expected|partial|misconception|off_focus|silent","student_response":"string","teacher_next_move":"string","scaffold":"string"}],"resource_use":{"resource_type":"string","why_needed":"string","attention_focus":"string","fallback_if_unavailable":"string"},"teacher_review_required":true,"formal_apply_performed":false}],"structure_rebalance_candidates":[],"evidence_plan":["string"],"lesson_position_connection":{"unit_start_entry":"","unit_middle_next_lesson_connection":"string","unit_end_closure":""},"closure_plan":"string","next_lesson_connection":"string","quality_gate":{}},"field_patch_candidates":[],"impact_scope":[],"quality_gate_update":{},"boundary_flags":{"teacher_review_required":true,"formal_apply_performed":false,"database_written":false,"memory_written":false,"feishu_written":false,"formal_export_created":false,"official_archive_created":false}},"rules":["classroom_events 写 3 个以内。","每个事件必须有 teacher_focus_cue、student_task、student_state_before、student_state_after、assessment_evidence、transition_to_next。","至少一个事件要预判 expected 和 off_focus 或 silent 反应，并写 teacher_next_move/scaffold。","如果资源不可用，resource_use.fallback_if_unavailable 必须写替代方案。","所有内容都是候选，teacher_review_required=true，formal_apply_performed=false。","不要说已写入、已同步、已归档、已正式应用。"]}

## Case Prompts

- `standard_daily_cold_warm_more_visual`
- `standard_daily_art_music_dance_rhythm`
- `quick_daily_basic_design`
- `open_class_question_expression_evidence`
- `research_lesson_color_feeling_transition`
- `constrained_low_resource_no_video`
