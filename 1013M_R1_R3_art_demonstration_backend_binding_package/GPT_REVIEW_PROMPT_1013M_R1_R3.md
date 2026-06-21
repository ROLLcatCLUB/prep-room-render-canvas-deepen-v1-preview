# GPT Review Prompt: 1013M R0 + R1-R3 Art Demonstration Binding

Please review the 1013M milestone package.

## Accepted Context

The user identified a key小学美术 teaching requirement:

```text
Before students draw / paint / design / make, the lesson must include a teacher demonstration and visual scaffold block.
```

This block should solve:

```text
tools and techniques
drawing steps
memorable three-step mantra
common mistakes and repair
peer examples
anti-copy guidance
pre-creation check
courseware screen seeds
```

## Review Scope

Review these stages:

```text
1013M_R0_ART_DEMONSTRATION_AND_VISUAL_SCAFFOLD_CONTRACT
1013M_R1_R3_ART_DEMONSTRATION_BACKEND_BINDING_PACKAGE
```

## Must Check

1. R0 defines the correct teaching-semantic contract.
2. R1 request envelope can require art demonstration when art creation is detected.
3. R2 prompt binding prevents generic text like "教师示范".
4. R3 normalized output inserts `demo / 示范与支架`.
5. R3 creates courseware screen seeds for demonstration, mantra, mistakes, peer examples, and pre-creation check.
6. Existing runtime contracts are not patched directly.
7. No provider/model/runtime/database/memory/Feishu/formal apply occurs.

## Expected Boundary

```text
provider_called=false
model_called=false
runtime_connected=false
database_written=false
memory_written=false
feishu_written=false
formal_apply_performed=false
lesson_body_modified=false
main_project_pushed=false
```

## Decision Format

Please return:

```text
REVIEW_DECISION=ACCEPT | ACCEPT_WITH_FIX | REJECT
ACCEPTED_STAGE=...
FINAL_STATUS=...
NEXT_STAGE=...
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
```
