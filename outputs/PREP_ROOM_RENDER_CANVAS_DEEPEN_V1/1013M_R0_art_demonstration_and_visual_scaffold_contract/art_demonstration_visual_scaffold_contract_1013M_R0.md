# 1013M_R0 Art Demonstration And Visual Scaffold Contract

## Purpose

This contract defines a required teaching block for primary-school art lessons:

```text
art_demonstration_and_visual_scaffold
```

It is used when a lesson asks students to draw, paint, design, craft, compose, make, revise, or present a visual work. The block prevents a lesson plan from jumping directly from "students understand the idea" to "students create" without solving the practical classroom questions:

```text
What should the teacher demonstrate?
What visual point should students notice?
Which tool or technique may block students?
What step sequence should students remember?
What peer examples can open ideas without causing copying?
How does the demonstration connect to assessment evidence?
```

## Position In Lesson Flow

Recommended location:

```text
observation / inquiry
-> art_demonstration_and_visual_scaffold
-> student creation / practice
-> display and evaluation
```

For the current lesson fixture, this is inserted between:

```text
探究
-> 示范与支架
-> 表现
```

## Required Teacher-Visible Content

The teacher-facing lesson process should express the block as classroom prose, not as engineering fields.

Required content:

1. 示范目的  
   Explain what the demonstration solves before students start creating.

2. 观察看点  
   Tell students what to look at during the demonstration.

3. 工具与技法  
   Name the concrete tool, medium, method, or hand movement students may need.

4. 绘画步骤  
   Turn the action into a short sequence students can remember.

5. 口令或三部曲  
   Provide a memorable phrase such as "先定主色，再找伙伴，最后一点亮".

6. 常见问题与修正  
   Include at least one likely mistake and one correction strategy.

7. 同龄作品支架  
   Use peer examples to open ideas and visual standards.

8. 防临摹边界  
   Distinguish learning a method from copying a teacher or peer work.

9. 动手前检查  
   Give students a short check before they begin.

## Generation Policy

If a lesson has a student making task, the generator must not write only:

```text
教师示范。
```

It must specify:

```text
示范什么
看什么
怎么做
学生记住哪一句
可能错在哪里
看哪些同龄作品
如何避免照抄
动手前检查什么
```

## Courseware Relationship

The block should produce or reuse courseware screen candidates:

```text
teacher_demo_screen
step_mantra_screen
mistake_comparison_screen
peer_example_screen
pre_creation_check_screen
```

Whiteboard or canvas tools may be used later as a local screen block, but the block itself is not a blank whiteboard workspace.

## Boundaries

```text
provider_called=false
model_called=false
runtime_connected=false
database_written=false
memory_written=false
feishu_written=false
formal_apply_performed=false
lesson_body_formal_write=false
preview_only=true
```

This contract is a teaching-semantic and prompt-policy layer. It does not call a real provider/model and does not write formal lesson content.
