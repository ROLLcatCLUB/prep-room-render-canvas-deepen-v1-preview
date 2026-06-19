# 1013I_R6R Big Unit Section Candidate Generator Adapter Fixture

FINAL_STATUS=PASS_1013I_R6R_BIG_UNIT_SECTION_CANDIDATE_GENERATOR_ADAPTER_FIXTURE
INHERITS_FROM=1013I_R6Q_BIG_UNIT_SECTION_GENERATION_REQUEST_ENVELOPE
NEXT_STAGE=1013I_R6S_BIG_UNIT_SECTION_CANDIDATE_RETURN_TO_EDIT_MODAL_PREVIEW

R6R reads the R6Q request envelope, context pack, generation policy, and dry-run trace, then creates four static fixture candidates for the big-unit section edit modal preview chain.

Created candidates:
- 课标依据
- 核心素养
- 表现任务
- 课时任务链

Boundaries:
- Static fixture candidates only.
- No runtime connection.
- No provider/model call.
- No formal apply.
- No database/memory/Feishu write.
- No main-project push.

Failed checks: []
