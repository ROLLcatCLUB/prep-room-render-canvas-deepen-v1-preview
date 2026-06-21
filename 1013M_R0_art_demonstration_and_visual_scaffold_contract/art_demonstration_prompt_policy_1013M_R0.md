# 1013M_R0 Prompt Policy

## Rule

When the lesson asks students to create an art work, the generation prompt must include an `art_demonstration_and_visual_scaffold` block.

The output must not stop at:

```text
教师示范，学生创作。
```

It must generate a classroom-usable demonstration plan.

## Prompt Requirements

Ask the model or generation adapter to produce:

```text
1. 示范目的：这次示范解决学生什么困难。
2. 观察看点：学生看示范时要抓住什么。
3. 工具与技法：教师示范哪些工具、材料或绘画方法。
4. 绘画步骤：学生可以按什么顺序做。
5. 三步口令：一句能记住的过程口令。
6. 常见问题：学生容易画错、做乱或走偏在哪里。
7. 修正方法：教师如何示范调整。
8. 同龄作品：看哪些学生作品，打开什么思路。
9. 不照抄提醒：学习方法，不复制画面。
10. 动手前检查：学生开始前确认什么。
```

## Teacher-Facing Style

Use teacher-readable prose:

```text
先定主色，再找伙伴，最后一点亮。
```

Avoid raw engineering labels in the main lesson body:

```text
demo_purpose
visual_attention_points
common_mistakes_and_repairs
```

Raw labels may appear only in validator, schema, or collapsed reference metadata.

## Anti-Copy Rule

The prompt must distinguish:

```text
可以学习方法、配色关系、构图思路、留白方式。
不直接照抄老师范画或同龄作品。
困难学生可以临摹局部方法，但需要改成自己的画面。
```

## Courseware Rule

The prompt should also produce courseware hints:

```text
示范步骤页
三步口令页
错例对比页
同龄作品页
动手前检查页
```

The courseware hints are preview-only screen seeds and do not connect to a real whiteboard, PPT export, provider, or runtime.
