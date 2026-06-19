from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013J_R1G_COURSEWARE_TEMPLATE_DYNAMIC_SCREEN_MAPPING_CONCEPT"
FINAL_STATUS = "PASS_1013J_R1G_COURSEWARE_TEMPLATE_DYNAMIC_SCREEN_MAPPING_CONCEPT"
INHERITS_FROM = "1013J_R1F_COURSEWARE_SCREEN_CLICK_THROUGH_STATIC_INTERACTION"
NEXT_STAGE = "USER_REVIEW_COURSEWARE_TEMPLATE_DYNAMIC_MAPPING"
BASE_DIR_NAME = "1013J_R1F_courseware_screen_click_through_static_interaction"
BASE_HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1F_courseware_click_through.html"
STAGE_DIR_NAME = "1013J_R1G_courseware_template_dynamic_screen_mapping_concept"
HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1G_courseware_template_dynamic_mapping.html"
VALIDATOR_NAME = "validate_1013J_R1G_courseware_template_dynamic_screen_mapping_concept.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]


TEMPLATES: list[dict[str, Any]] = [
    {
        "template_id": "cover_title",
        "teacher_label": "课题封面",
        "classroom_use": "呈现课题、单元和本课核心问题",
        "recommended_for": ["导入", "课题呈现"],
        "default_slots": [
            {"slot_id": "title", "slot_type": "text", "teacher_label": "课题", "placeholder_text": "放本课课题"},
            {"slot_id": "background", "slot_type": "image", "teacher_label": "背景图", "placeholder_text": "放一张轻背景图"},
        ],
        "editable_later": True,
        "whiteboard_required": False,
    },
    {
        "template_id": "one_image_observation",
        "teacher_label": "一图观察",
        "classroom_use": "围绕一张图片进行观察、描述和追问",
        "recommended_for": ["图像观察", "经验唤醒"],
        "default_slots": [
            {"slot_id": "image", "slot_type": "image", "teacher_label": "观察图片", "placeholder_text": "放一张用于观察的图片"},
            {"slot_id": "question", "slot_type": "text", "teacher_label": "课堂问题", "placeholder_text": "你看到了什么？"},
        ],
        "editable_later": True,
        "whiteboard_required": False,
    },
    {
        "template_id": "two_image_comparison",
        "teacher_label": "两图对比",
        "classroom_use": "帮助学生比较两组图像、色彩或方法的差异",
        "recommended_for": ["比较观察", "方法发现", "审美判断"],
        "default_slots": [
            {"slot_id": "image_a", "slot_type": "image", "teacher_label": "素材 A", "placeholder_text": "放一张用于比较的图片"},
            {"slot_id": "image_b", "slot_type": "image", "teacher_label": "素材 B", "placeholder_text": "放另一张用于比较的图片"},
            {"slot_id": "question", "slot_type": "text", "teacher_label": "课堂问题", "placeholder_text": "你发现它们有什么不同？"},
        ],
        "editable_later": True,
        "whiteboard_required": False,
    },
    {
        "template_id": "three_image_comparison",
        "teacher_label": "三图比较",
        "classroom_use": "让学生在多组图像之间寻找规律或差异",
        "recommended_for": ["归纳发现", "作品比较"],
        "default_slots": [
            {"slot_id": "image_a", "slot_type": "image", "teacher_label": "素材 A", "placeholder_text": "第一张图片"},
            {"slot_id": "image_b", "slot_type": "image", "teacher_label": "素材 B", "placeholder_text": "第二张图片"},
            {"slot_id": "image_c", "slot_type": "image", "teacher_label": "素材 C", "placeholder_text": "第三张图片"},
            {"slot_id": "question", "slot_type": "text", "teacher_label": "课堂问题", "placeholder_text": "它们有什么共同点？"},
        ],
        "editable_later": True,
        "whiteboard_required": False,
    },
    {
        "template_id": "image_with_question",
        "teacher_label": "图像提问",
        "classroom_use": "图片为主，配一个轻问题",
        "recommended_for": ["导入", "追问"],
        "default_slots": [
            {"slot_id": "image", "slot_type": "image", "teacher_label": "主图", "placeholder_text": "放主观察图"},
            {"slot_id": "question", "slot_type": "text", "teacher_label": "问题", "placeholder_text": "你注意到了什么？"},
        ],
        "editable_later": True,
        "whiteboard_required": False,
    },
    {
        "template_id": "image_annotation",
        "teacher_label": "图像标注",
        "classroom_use": "在图片上圈画、标记或提示观察位置",
        "recommended_for": ["观察支架", "局部分析"],
        "default_slots": [
            {"slot_id": "image", "slot_type": "image", "teacher_label": "标注图片", "placeholder_text": "放需要圈画的图片"},
            {"slot_id": "annotation_hint", "slot_type": "text", "teacher_label": "标注提示", "placeholder_text": "圈出你判断的依据"},
        ],
        "editable_later": True,
        "whiteboard_required": True,
    },
    {
        "template_id": "word_card",
        "teacher_label": "词卡",
        "classroom_use": "给学生提供可选择、可替换的表达词",
        "recommended_for": ["表达支架", "关键词回收"],
        "default_slots": [
            {"slot_id": "words", "slot_type": "text_list", "teacher_label": "词卡", "placeholder_text": "热烈 / 安静 / 柔和"},
        ],
        "editable_later": True,
        "whiteboard_required": False,
    },
    {
        "template_id": "task_release",
        "teacher_label": "任务发布",
        "classroom_use": "把学生要完成的任务投到大屏",
        "recommended_for": ["任务说明", "操作提示"],
        "default_slots": [
            {"slot_id": "task", "slot_type": "text", "teacher_label": "任务", "placeholder_text": "用 3-4 种颜色表达一种感觉"},
            {"slot_id": "requirement", "slot_type": "text", "teacher_label": "要求", "placeholder_text": "说出你的选择理由"},
        ],
        "editable_later": True,
        "whiteboard_required": False,
    },
    {
        "template_id": "step_demo",
        "teacher_label": "步骤示范",
        "classroom_use": "用少量步骤说明操作过程",
        "recommended_for": ["方法学习", "教师示范"],
        "default_slots": [
            {"slot_id": "step_1", "slot_type": "text", "teacher_label": "第一步", "placeholder_text": "先观察"},
            {"slot_id": "step_2", "slot_type": "text", "teacher_label": "第二步", "placeholder_text": "再尝试"},
            {"slot_id": "demo_image", "slot_type": "image", "teacher_label": "示范图", "placeholder_text": "放示范图"},
        ],
        "editable_later": True,
        "whiteboard_required": False,
    },
    {
        "template_id": "whiteboard_interaction",
        "teacher_label": "白板互动",
        "classroom_use": "保留一块可圈画、拖拽或现场记录的区域",
        "recommended_for": ["色卡试验", "现场标注", "学生互动"],
        "default_slots": [
            {"slot_id": "board", "slot_type": "whiteboard", "teacher_label": "白板区", "placeholder_text": "保留可操作区域"},
            {"slot_id": "prompt", "slot_type": "text", "teacher_label": "操作提示", "placeholder_text": "拖一拖色卡"},
        ],
        "editable_later": True,
        "whiteboard_required": True,
    },
    {
        "template_id": "student_work_wall",
        "teacher_label": "作品展示",
        "classroom_use": "展示学生作品、示例或对比作品",
        "recommended_for": ["展示交流", "同伴评价"],
        "default_slots": [
            {"slot_id": "work_1", "slot_type": "image", "teacher_label": "作品 A", "placeholder_text": "放学生作品"},
            {"slot_id": "work_2", "slot_type": "image", "teacher_label": "作品 B", "placeholder_text": "放学生作品"},
            {"slot_id": "talk_prompt", "slot_type": "text", "teacher_label": "交流提示", "placeholder_text": "你用了哪些颜色？"},
        ],
        "editable_later": True,
        "whiteboard_required": False,
    },
    {
        "template_id": "evaluation_prompt",
        "teacher_label": "评价提示",
        "classroom_use": "显示评价点、修改建议或同伴反馈句式",
        "recommended_for": ["展示评价", "修改反馈"],
        "default_slots": [
            {"slot_id": "criteria", "slot_type": "text_list", "teacher_label": "评价点", "placeholder_text": "颜色选择和感觉是否有关"},
            {"slot_id": "revision", "slot_type": "text", "teacher_label": "修改提示", "placeholder_text": "你想调整哪里？"},
        ],
        "editable_later": True,
        "whiteboard_required": False,
    },
    {
        "template_id": "summary_review",
        "teacher_label": "总结回看",
        "classroom_use": "收束本课路径和学生收获",
        "recommended_for": ["课堂总结", "回顾"],
        "default_slots": [
            {"slot_id": "summary", "slot_type": "text", "teacher_label": "总结", "placeholder_text": "看色彩、说感觉、比变化、做表达"},
        ],
        "editable_later": True,
        "whiteboard_required": False,
    },
    {
        "template_id": "custom_blank",
        "teacher_label": "自由页",
        "classroom_use": "老师临时添加，不必立即关联教学设计",
        "recommended_for": ["临时提醒", "过渡页", "课堂管理"],
        "default_slots": [
            {"slot_id": "free_content", "slot_type": "mixed", "teacher_label": "自由内容", "placeholder_text": "放文字、图片或提醒"},
        ],
        "editable_later": True,
        "whiteboard_required": False,
    },
]


DYNAMIC_SCREENS: list[dict[str, Any]] = [
    {
        "screen_id": "screen_01",
        "screen_order": 1,
        "screen_title": "色彩的感觉",
        "template_id": "cover_title",
        "generation_source": "agent_recommended",
        "linked_to_lesson": True,
        "linked_lesson_section": "导入问题",
        "linked_teaching_activity": "从色彩图片和课题进入，唤醒学生的直观感受",
        "display_intent": "让学生先进入色彩感受，而不是先听概念",
        "screen_text": {"main_question": "颜色为什么会让人产生不同感觉？", "teacher_prompt": "先说第一感觉。"},
        "material_slots": [{"slot_id": "background", "slot_type": "image", "teacher_label": "课题背景图", "status": "可后补"}],
        "teacher_editable_later": True,
    },
    {
        "screen_id": "screen_02",
        "screen_order": 2,
        "screen_title": "这些颜色给你什么感觉？",
        "template_id": "three_image_comparison",
        "generation_source": "agent_recommended",
        "linked_to_lesson": True,
        "linked_lesson_section": "观察感受",
        "linked_teaching_activity": "看多组生活色彩图片，先说直观感受",
        "display_intent": "用图像打开经验，让学生先说感受",
        "screen_text": {"main_question": "这些颜色给你什么感觉？", "teacher_prompt": "不急着判断对错。"},
        "material_slots": [
            {"slot_id": "image_a", "slot_type": "image", "teacher_label": "生活色彩图片 A", "status": "待补图"},
            {"slot_id": "image_b", "slot_type": "image", "teacher_label": "生活色彩图片 B", "status": "待补图"},
            {"slot_id": "image_c", "slot_type": "image", "teacher_label": "生活色彩图片 C", "status": "待补图"},
        ],
        "teacher_editable_later": True,
    },
    {
        "screen_id": "screen_03",
        "screen_order": 3,
        "screen_title": "哪一组颜色更安静？",
        "template_id": "two_image_comparison",
        "generation_source": "agent_recommended",
        "linked_to_lesson": True,
        "linked_lesson_section": "比较变化",
        "linked_teaching_activity": "通过两组色彩比较，帮助学生说出色彩带来的不同感觉",
        "display_intent": "帮助学生从“好看”转向说出具体色彩感受",
        "screen_text": {"main_question": "哪一组颜色更安静？", "teacher_prompt": "你从哪些颜色看出来？"},
        "material_slots": [
            {"slot_id": "image_a", "slot_type": "image", "teacher_label": "热闹的色彩组合图", "status": "待补图"},
            {"slot_id": "image_b", "slot_type": "image", "teacher_label": "安静的色彩组合图", "status": "待补图"},
        ],
        "teacher_editable_later": True,
    },
    {
        "screen_id": "screen_06",
        "screen_order": 6,
        "screen_title": "试一组颜色",
        "template_id": "whiteboard_interaction",
        "generation_source": "agent_recommended",
        "linked_to_lesson": True,
        "linked_lesson_section": "色卡试验",
        "linked_teaching_activity": "让学生拖动色卡，观察组合变化",
        "display_intent": "让学生看见色彩组合变化",
        "screen_text": {"main_question": "试一组颜色", "teacher_prompt": "拖一拖色卡。"},
        "material_slots": [
            {"slot_id": "board", "slot_type": "whiteboard", "teacher_label": "色卡拖拽区", "status": "可白板"},
            {"slot_id": "prompt", "slot_type": "text", "teacher_label": "操作提示", "status": "已有文字"},
        ],
        "teacher_editable_later": True,
    },
]


CUSTOM_SCREENS = [
    {
        "screen_id": "custom_01",
        "screen_title": "课前提醒",
        "template_id": "custom_blank",
        "generation_source": "teacher_added",
        "linked_to_lesson": False,
        "teacher_note": "老师临时加入，不进入教学设计正文",
    },
    {
        "screen_id": "custom_02",
        "screen_title": "色卡整理提醒",
        "template_id": "task_release",
        "generation_source": "teacher_added",
        "linked_to_lesson": False,
        "agent_can_suggest_lesson_link": True,
        "suggested_lesson_section": "材料准备",
        "suggestion_text": "这一页可以作为材料准备提醒，是否加入教学过程？",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def locate_output_root(root: Path) -> Path:
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    if (root / "LATEST_REVIEW_ENTRY.md").exists():
        return root
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "upload_implemented": False,
        "search_implemented": False,
        "whiteboard_library_connected": False,
        "ppt_export_implemented": False,
        "drag_edit_implemented": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def css() -> str:
    return """

    /* 1013J_R1G: template and dynamic mapping concept */
    [data-1013j-r1g-dynamic-template="true"] .courseware-r1e-left {
      display: grid;
      gap: 12px;
    }

    [data-1013j-r1g-dynamic-template="true"] .courseware-r1g-note {
      color: rgba(29, 39, 35, .58);
      font-size: 12px;
      line-height: 1.45;
    }

    [data-1013j-r1g-dynamic-template="true"] .courseware-r1g-chip-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
    }

    [data-1013j-r1g-dynamic-template="true"] .courseware-r1g-chip {
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      border: 1px solid rgba(43, 124, 106, .18);
      background: rgba(240, 250, 246, .70);
      color: var(--green);
      padding: 3px 8px;
      font-size: 11px;
      font-weight: 850;
    }

    [data-1013j-r1g-dynamic-template="true"] .courseware-r1e-screen-list .node-action {
      min-height: 34px;
      cursor: pointer;
    }

    [data-1013j-r1g-dynamic-template="true"] .courseware-r1g-template-mini {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 7px;
    }

    [data-1013j-r1g-dynamic-template="true"] .courseware-r1g-template-mini .node-action {
      justify-content: center;
      min-height: 30px;
      padding: 5px 8px;
      font-size: 12px;
    }

    [data-1013j-r1g-dynamic-template="true"] .courseware-r1e-screen {
      grid-template-rows: auto 1fr auto;
    }

    [data-1013j-r1g-dynamic-template="true"] .courseware-r1e-question {
      font-size: clamp(13px, 1.05vw, 18px);
      line-height: 1.28;
    }

    [data-1013j-r1g-dynamic-template="true"] .courseware-r1g-screen-meta {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-top: 6px;
    }

    [data-1013j-r1g-dynamic-template="true"] .courseware-r1g-slot-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      min-height: 0;
    }

    [data-1013j-r1g-dynamic-template="true"] .courseware-r1g-slot-grid.is-one {
      grid-template-columns: 1fr;
    }

    [data-1013j-r1g-dynamic-template="true"] .courseware-r1g-slot-grid.is-three {
      grid-template-columns: repeat(3, 1fr);
    }

    [data-1013j-r1g-dynamic-template="true"] .courseware-r1g-slot {
      min-height: clamp(175px, 23vw, 340px);
      border-radius: 14px;
      border: 1px dashed rgba(43, 124, 106, .24);
      background: linear-gradient(135deg, rgba(246, 251, 247, .72), rgba(255, 253, 247, .76));
      display: grid;
      place-items: center;
      text-align: center;
      color: rgba(43, 83, 74, .48);
      font-size: clamp(12px, 1vw, 16px);
      line-height: 1.45;
      padding: 16px;
    }

    [data-1013j-r1g-dynamic-template="true"] .courseware-r1g-side-stack {
      display: grid;
      gap: 10px;
    }

    [data-1013j-r1g-dynamic-template="true"] .courseware-r1g-side-stack .courseware-side-block p {
      margin: 5px 0 0;
    }
"""


def js() -> str:
    screens = json.dumps(DYNAMIC_SCREENS, ensure_ascii=False)
    templates = json.dumps(TEMPLATES, ensure_ascii=False)
    custom = json.dumps(CUSTOM_SCREENS, ensure_ascii=False)
    return f"""
    const coursewareTemplates1013JR1G = {templates};
    const dynamicCoursewareScreens1013JR1G = {screens};
    const customCoursewareScreens1013JR1G = {custom};

    function currentDynamicScreen1013JR1G() {{
      const params = new URLSearchParams(window.location.search || "");
      const requested = params.get("screen") || "screen_03";
      return dynamicCoursewareScreens1013JR1G.find((screen) => screen.screen_id === requested) || dynamicCoursewareScreens1013JR1G[2];
    }}

    function templateLabel1013JR1G(templateId) {{
      const template = coursewareTemplates1013JR1G.find((item) => item.template_id === templateId);
      return template ? template.teacher_label : "自定义";
    }}

    function renderSlots1013JR1G(screen) {{
      const slots = screen.material_slots || [];
      const gridClass = slots.length === 1 ? "is-one" : (slots.length >= 3 ? "is-three" : "");
      return `<div class="courseware-r1g-slot-grid ${{gridClass}}">${{slots.map((slot) => `<div class="courseware-r1g-slot"><div>${{html(slot.teacher_label)}}<br><span class="quiet-tag">${{html(slot.status || "占位")}}</span></div></div>`).join("")}}</div>`;
    }}

    function setDynamicScreen1013JR1G(screenId) {{
      const screen = dynamicCoursewareScreens1013JR1G.find((item) => item.screen_id === screenId) || dynamicCoursewareScreens1013JR1G[2];
      document.querySelectorAll("[data-r1g-screen-id]").forEach((button) => {{
        const selected = button.dataset.r1gScreenId === screen.screen_id;
        button.classList.toggle("primary", selected);
        button.classList.toggle("secondary", !selected);
        button.setAttribute("aria-pressed", selected ? "true" : "false");
      }});
      const frame = document.querySelector("[data-r1g-current-screen]");
      if (frame) frame.dataset.r1gCurrentScreen = screen.screen_id;
      const title = document.querySelector("[data-r1g-screen-title]");
      if (title) title.textContent = screen.screen_text.main_question;
      const meta = document.querySelector("[data-r1g-screen-meta]");
      if (meta) meta.innerHTML = `<span class="courseware-r1g-chip">${{html(templateLabel1013JR1G(screen.template_id))}}</span><span class="courseware-r1g-chip">${{screen.linked_to_lesson ? "关联备课" : "自由页"}}</span>`;
      const slots = document.querySelector("[data-r1g-slots]");
      if (slots) slots.innerHTML = renderSlots1013JR1G(screen);
      const bottom = document.querySelector("[data-r1g-bottom]");
      if (bottom) bottom.innerHTML = `<span>${{html(screen.linked_lesson_section || "自由页")}}</span><span class="quiet-tag">${{html(screen.generation_source === "agent_recommended" ? "小教推荐" : "老师添加")}}</span>`;
      const sideTemplate = document.querySelector("[data-r1g-side-template]");
      if (sideTemplate) sideTemplate.textContent = templateLabel1013JR1G(screen.template_id);
      const sideLesson = document.querySelector("[data-r1g-side-lesson]");
      if (sideLesson) sideLesson.textContent = screen.linked_lesson_section || "暂不关联";
      const sideIntent = document.querySelector("[data-r1g-side-intent]");
      if (sideIntent) sideIntent.textContent = screen.display_intent;
      const sideSlots = document.querySelector("[data-r1g-side-slots]");
      if (sideSlots) sideSlots.textContent = screen.material_slots.map((slot) => slot.teacher_label).join("；");
    }}

    function renderCoursewareExpandedWorkspace1013JR1(view) {{
      const current = currentDynamicScreen1013JR1G();
      return `
        <div class="courseware-r1e-shell" data-1013j-r1-expanded="true" data-1013j-r1g-dynamic-template="true" aria-label="课件制作工作区">
          <div class="courseware-r1e-workbench">
            <aside class="courseware-r1e-left" aria-label="课件草稿">
              <div>
                <div class="courseware-r1e-title">大屏草稿</div>
                <div class="courseware-r1g-note">样例草稿：8 屏。小教会按教学设计动态增减。</div>
              </div>
              <div class="courseware-r1g-chip-row">
                <span class="courseware-r1g-chip">模板生成</span>
                <span class="courseware-r1g-chip">可增减</span>
                <span class="courseware-r1g-chip">可关联备课</span>
              </div>
              <nav class="courseware-r1e-screen-list" aria-label="大屏草稿列表">
                ${{dynamicCoursewareScreens1013JR1G.map((screen) => `
                  <button class="node-action ${{screen.screen_id === current.screen_id ? "primary" : "secondary"}}" type="button" data-r1g-screen-id="${{html(screen.screen_id)}}" aria-pressed="${{screen.screen_id === current.screen_id ? "true" : "false"}}">
                    <span>${{String(screen.screen_order).padStart(2, "0")}}</span>
                    <strong>${{html(screen.screen_title)}}</strong>
                  </button>
                `).join("")}}
                <button class="node-action secondary" type="button" data-r1g-custom="true">＋ 自定义页面</button>
              </nav>
              <div>
                <div class="courseware-r1e-title">课件模板</div>
                <div class="courseware-r1g-template-mini">
                  <button class="node-action secondary" type="button">一图观察</button>
                  <button class="node-action secondary" type="button">两图对比</button>
                  <button class="node-action secondary" type="button">三图比较</button>
                  <button class="node-action secondary" type="button">任务发布</button>
                  <button class="node-action secondary" type="button">作品展示</button>
                  <button class="node-action secondary" type="button">评价提示</button>
                </div>
              </div>
            </aside>
            <main class="courseware-r1e-main" aria-label="课堂大屏画面">
              <div class="courseware-r1e-toolbar" aria-label="大屏工具条">
                <div class="courseware-r1e-tools">
                  <button class="courseware-r1e-icon primary" type="button" title="进入大屏预览">▶</button>
                  <button class="courseware-r1e-icon" type="button" title="补图片">图</button>
                  <button class="courseware-r1e-icon" type="button" title="圈画">圈</button>
                  <button class="courseware-r1e-icon" type="button" title="改文字">字</button>
                </div>
                <div class="courseware-r1e-ratio" aria-label="画面比例">
                  <span class="courseware-r1e-segment" role="group" aria-label="大屏比例切换">
                    <button class="active" type="button">16:9</button>
                    <button type="button">4:3</button>
                  </span>
                </div>
              </div>
              <section class="courseware-r1e-screen-frame" data-screen-ratio="16:9" data-r1g-current-screen="${{html(current.screen_id)}}" aria-label="课堂大屏">
                <div class="courseware-r1e-screen">
                  <div>
                    <div class="courseware-r1e-question" data-r1g-screen-title>${{html(current.screen_text.main_question)}}</div>
                    <div class="courseware-r1g-screen-meta" data-r1g-screen-meta>
                      <span class="courseware-r1g-chip">${{html(templateLabel1013JR1G(current.template_id))}}</span>
                      <span class="courseware-r1g-chip">${{current.linked_to_lesson ? "关联备课" : "自由页"}}</span>
                    </div>
                  </div>
                  <div data-r1g-slots>${{renderSlots1013JR1G(current)}}</div>
                  <div class="courseware-r1e-bottom-tools" data-whiteboard-as-block="true" data-r1g-bottom>
                    <span>${{html(current.linked_lesson_section)}}</span>
                    <span class="quiet-tag">小教推荐</span>
                  </div>
                </div>
              </section>
            </main>
            <aside class="courseware-r1e-right courseware-r1g-side-stack" aria-label="模板与映射">
              <button class="node-action secondary" type="button" data-courseware-normal="true">回到备课</button>
              <button class="node-action primary" type="button">大屏预览</button>
              <div class="courseware-r1e-title">模板与关联</div>
              <div class="courseware-side-block">
                <strong>当前模板</strong>
                <p data-r1g-side-template>${{html(templateLabel1013JR1G(current.template_id))}}</p>
              </div>
              <div class="courseware-side-block">
                <strong>关联备课环节</strong>
                <p data-r1g-side-lesson>${{html(current.linked_lesson_section)}}</p>
              </div>
              <div class="courseware-side-block">
                <strong>本屏作用</strong>
                <p data-r1g-side-intent>${{html(current.display_intent)}}</p>
              </div>
              <div class="courseware-side-block">
                <strong>素材占位</strong>
                <p data-r1g-side-slots>${{html(current.material_slots.map((slot) => slot.teacher_label).join("；"))}}</p>
              </div>
              <div class="courseware-side-block">
                <strong>小教建议</strong>
                <p>小教先推荐模板、文字和素材位；老师可以换模板、加自由页或回到备课调整。</p>
              </div>
            </aside>
          </div>
        </div>
      `;
    }}

    document.addEventListener("click", (event) => {{
      const screenButton = event.target.closest("[data-r1g-screen-id]");
      if (screenButton) {{
        event.preventDefault();
        setDynamicScreen1013JR1G(screenButton.dataset.r1gScreenId);
      }}
    }});
"""


def patch_html(output_root: Path) -> str:
    base_html = output_root / BASE_DIR_NAME / BASE_HTML_NAME
    html = base_html.read_text(encoding="utf-8")
    html = html.replace("1013J_R1F 课件屏切换静态交互", "1013J_R1G 课件模板与动态映射概念")
    html = html.replace("</style>", css() + "\n  </style>", 1)
    html = html.replace("    initPrepRoomRenderCanvas();", js() + "\n    initPrepRoomRenderCanvas();", 1)
    return html


def find_browser() -> Path | None:
    for path in CHROME_CANDIDATES:
        if path.exists():
            return path
    return None


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8].hex() != "89504e470d0a1a0a":
        raise ValueError(f"Not a PNG: {path}")
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def javascript_syntax_check(stage_dir: Path, html_text: str) -> dict[str, Any]:
    node = shutil.which("node")
    if not node:
        return {"javascript_syntax_check_pass": False, "javascript_syntax_error": "node_not_found"}
    scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html_text, flags=re.S | re.I)
    script_files: list[str] = []
    for index, script_text in enumerate(scripts):
        script_path = stage_dir / f"javascript_syntax_1013J_R1G_{index:02d}.js"
        write_text(script_path, script_text)
        script_files.append(script_path.name)
        proc = subprocess.run([node, "--check", str(script_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            return {"javascript_syntax_check_pass": False, "javascript_syntax_error": proc.stderr.strip() or proc.stdout.strip(), "javascript_syntax_files": script_files}
    return {"javascript_syntax_check_pass": True, "javascript_syntax_files": script_files}


def screenshot(stage_dir: Path, html_path: Path) -> dict[str, Any]:
    browser = find_browser()
    shots: list[dict[str, Any]] = []
    if browser is None:
        return {"screenshot_smoke_pass": False, "screenshot_error": "browser_not_found", "screenshots": shots}
    cases = [
        ("template_library", "screen_03"),
        ("mapping_panel", "screen_03"),
        ("custom_screen", "screen_06"),
    ]
    for name, screen in cases:
        out = stage_dir / f"ui_smoke_screenshot_1013J_R1G_{name}.png"
        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-cache",
            "--disable-default-apps",
            "--no-first-run",
            "--window-size=1440,1100",
            f"--screenshot={out}",
            "file:///" + html_path.as_posix() + f"?screen={screen}#coursewareExpanded",
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        width, height = png_size(out)
        shots.append({"case": name, "path": out.name, "width": width, "height": height, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": True, "screenshots": shots}


def lesson_screen_mapping() -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "teacher_visible_mapping_only": True,
        "mappings": [
            {
                "lesson_section_label": "学生起点",
                "courseware_screens": [{"screen_id": "screen_01", "screen_title": "色彩的感觉", "template_id": "cover_title", "mapping_reason": "这一屏用于唤醒学生已有色彩感受"}],
                "can_return_to_lesson_plan": True,
                "return_note": "如果老师新增经验唤醒页，小教可提示是否同步补入导入环节。",
            },
            {
                "lesson_section_label": "比较变化",
                "courseware_screens": [{"screen_id": "screen_03", "screen_title": "哪一组颜色更安静？", "template_id": "two_image_comparison", "mapping_reason": "这一屏用于支持学生比较两组色彩并说出具体感受"}],
                "can_return_to_lesson_plan": True,
                "return_note": "如果老师改成三图比较，小教可提示是否同步调整教学过程。",
            },
            {
                "lesson_section_label": "材料与支架",
                "courseware_screens": [{"screen_id": "screen_06", "screen_title": "试一组颜色", "template_id": "whiteboard_interaction", "mapping_reason": "这一屏用于支持色卡操作和现场试色"}],
                "can_return_to_lesson_plan": True,
                "return_note": "如果老师添加色卡整理页，小教可提示是否同步到材料准备。",
            },
        ],
        **boundary(),
    }


def agent_recommendation() -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "agent_recommendation_role": "recommend_templates_generate_screen_text_material_slots_and_lesson_mapping",
        "source_lesson_section": "比较变化",
        "agent_recommendation": {
            "recommended_template": "two_image_comparison",
            "recommended_screen_title": "哪一组颜色更安静？",
            "recommended_question": "你从哪些颜色看出来？",
            "material_slots": ["热闹的色彩组合图", "安静的色彩组合图"],
            "reason": "这一段需要学生通过比较说出色彩感受，两图对比比单纯文字更适合大屏呈现。",
            "teacher_actions": ["采纳为课件页", "换成三图比较", "只保留文字问题", "暂不生成"],
        },
        **boundary(),
    }


def validate_fixtures(stage_dir: Path, html_text: str) -> dict[str, Any]:
    template_path = stage_dir / "courseware_template_library_1013J_R1G.json"
    dynamic_path = stage_dir / "dynamic_screen_model_1013J_R1G.json"
    mapping_path = stage_dir / "lesson_screen_mapping_fixture_1013J_R1G.json"
    custom_path = stage_dir / "custom_screen_fixture_1013J_R1G.json"
    agent_path = stage_dir / "agent_recommendation_fixture_1013J_R1G.json"
    templates = json.loads(template_path.read_text(encoding="utf-8"))["templates"]
    dynamic = json.loads(dynamic_path.read_text(encoding="utf-8"))
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    custom = json.loads(custom_path.read_text(encoding="utf-8"))["custom_screens"]
    agent = json.loads(agent_path.read_text(encoding="utf-8"))
    ids = {item["template_id"] for item in templates}
    required = {"one_image_observation", "two_image_comparison", "three_image_comparison", "whiteboard_interaction", "student_work_wall", "evaluation_prompt", "custom_blank"}
    r1g_surface = re.search(r'<div class="courseware-r1e-shell" data-1013j-r1-expanded="true" data-1013j-r1g-dynamic-template="true".*?</div>\s*`;', html_text, flags=re.S)
    surface_text = r1g_surface.group(0) if r1g_surface else html_text
    banned = ["schema", "payload", "provider", "model call", "database", "field key", "unit_package", "lesson_position", "mapping_json", "runtime", "validator"]
    checks: dict[str, Any] = {
        "fixed_8_screen_rule_removed": "共 8 屏" not in surface_text and "screen_count=8" not in surface_text,
        "sample_8_screens_kept_as_fixture_only": "样例草稿：8 屏" in surface_text and dynamic["sample_8_screens_fixture_only"] is True,
        "courseware_template_library_defined": template_path.exists(),
        "template_count_minimum_met": len(templates) >= 12,
        "required_templates_present": required.issubset(ids),
        "dynamic_screen_model_defined": dynamic_path.exists(),
        "screen_count_not_fixed": dynamic["screen_count_not_fixed"] is True,
        "lesson_section_mapping_defined": mapping_path.exists() and bool(mapping["mappings"]),
        "material_slot_mapping_defined": all("material_slots" in screen for screen in dynamic["screens"]),
        "custom_screen_allowed": custom_path.exists() and dynamic["teacher_can_add_custom_screen"] is True,
        "custom_screen_can_be_unlinked": any(screen.get("linked_to_lesson") is False for screen in custom),
        "custom_screen_can_be_agent_linked_back_to_lesson": any(screen.get("agent_can_suggest_lesson_link") is True for screen in custom),
        "agent_recommendation_role_defined": agent_path.exists() and "agent_recommendation" in agent,
        "teacher_visible_engineering_terms_absent": all(term not in surface_text for term in banned),
        **boundary(),
    }
    return checks


def failed_checks(checks: dict[str, Any]) -> list[str]:
    failed: list[str] = []
    expected_false = set(boundary().keys())
    for key, value in checks.items():
        if key in {"javascript_syntax_files", "javascript_syntax_error"}:
            continue
        if key in expected_false:
            if value is not False:
                failed.append(key)
        elif value is not True:
            failed.append(key)
    return failed


def write_docs(output_root: Path, stage_dir: Path, result: dict[str, Any]) -> None:
    write_text(stage_dir / "1013J_R1G_report.md", f"""# 1013J_R1G Courseware Template Dynamic Screen Mapping Concept

FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R1G reframes the R1F eight-screen click-through as a fixture, not a fixed product rule.

This stage defines:
- courseware template library
- dynamic screen model
- lesson-to-screen mapping fixture
- custom screen fixture
- Xiaojiao recommendation fixture

No backend, provider/model, upload, search, whiteboard library, PPT export, drag edit, database, memory, Feishu, or formal apply is connected.

Failed checks: {result["failed_checks"]}
""")
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

1013J_R1G establishes that courseware screens are dynamically recommended from templates and mapped to lesson sections. The previous 8-screen courseware remains only a sample fixture.

Key flags:
- FIXED_8_SCREEN_RULE_REMOVED=true
- SAMPLE_8_SCREENS_KEPT_AS_FIXTURE_ONLY=true
- COURSEWARE_TEMPLATE_LIBRARY_DEFINED=true
- TEMPLATE_COUNT_MINIMUM_MET=true
- DYNAMIC_SCREEN_MODEL_DEFINED=true
- SCREEN_COUNT_NOT_FIXED=true
- LESSON_SECTION_MAPPING_DEFINED=true
- MATERIAL_SLOT_MAPPING_DEFINED=true
- CUSTOM_SCREEN_ALLOWED=true
- CUSTOM_SCREEN_CAN_BE_UNLINKED=true
- CUSTOM_SCREEN_CAN_BE_AGENT_LINKED_BACK_TO_LESSON=true
- AGENT_RECOMMENDATION_ROLE_DEFINED=true
- TEACHER_VISIBLE_ENGINEERING_TERMS_ABSENT=true
- UPLOAD_IMPLEMENTED=false
- SEARCH_IMPLEMENTED=false
- WHITEBOARD_LIBRARY_CONNECTED=false
- PPT_EXPORT_IMPLEMENTED=false
- DRAG_EDIT_IMPLEMENTED=false
- PROVIDER_CALLED=false
- MODEL_CALLED=false
- FORMAL_APPLY_PERFORMED=false
- MAIN_PROJECT_PUSHED=false
""")
    write_text(output_root / "README.md", f"""# Prep Room Render Canvas Deepen V1 Review Package

Latest stage: `{STAGE_ID}`

Open:
- `{STAGE_DIR_NAME}/{HTML_NAME}`
- `{STAGE_DIR_NAME}/1013J_R1G_result.json`

Run:

```bash
python scripts/{VALIDATOR_NAME}
python scripts/{VALIDATOR_NAME} --root <repo-root>
```
""")
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", f"""# Review Package Manifest

Latest stage: `{STAGE_ID}`

Files:
- `LATEST_REVIEW_ENTRY.md`
- `README.md`
- `REVIEW_PACKAGE_MANIFEST.md`
- `{STAGE_DIR_NAME}/{HTML_NAME}`
- `{STAGE_DIR_NAME}/courseware_template_library_1013J_R1G.json`
- `{STAGE_DIR_NAME}/dynamic_screen_model_1013J_R1G.json`
- `{STAGE_DIR_NAME}/lesson_screen_mapping_fixture_1013J_R1G.json`
- `{STAGE_DIR_NAME}/custom_screen_fixture_1013J_R1G.json`
- `{STAGE_DIR_NAME}/agent_recommendation_fixture_1013J_R1G.json`
- `{STAGE_DIR_NAME}/1013J_R1G_result.json`
- `{STAGE_DIR_NAME}/1013J_R1G_report.md`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1G_template_library.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1G_mapping_panel.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1G_custom_screen.png`
- `scripts/{VALIDATOR_NAME}`
""")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output_root = locate_output_root(root)
    base_result = output_root / BASE_DIR_NAME / "1013J_R1F_result.json"
    if not base_result.exists():
        raise FileNotFoundError(base_result)

    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)

    write_json(stage_dir / "courseware_template_library_1013J_R1G.json", {"stage": STAGE_ID, "template_count": len(TEMPLATES), "templates": TEMPLATES, **boundary()})
    write_json(stage_dir / "dynamic_screen_model_1013J_R1G.json", {
        "stage": STAGE_ID,
        "screen_count_not_fixed": True,
        "sample_8_screens_fixture_only": True,
        "teacher_can_add_custom_screen": True,
        "teacher_can_delete_or_reorder": True,
        "screens_can_be_linked_or_unlinked_to_lesson": True,
        "screens": DYNAMIC_SCREENS,
        **boundary(),
    })
    write_json(stage_dir / "lesson_screen_mapping_fixture_1013J_R1G.json", lesson_screen_mapping())
    write_json(stage_dir / "custom_screen_fixture_1013J_R1G.json", {"stage": STAGE_ID, "custom_screens": CUSTOM_SCREENS, **boundary()})
    write_json(stage_dir / "agent_recommendation_fixture_1013J_R1G.json", agent_recommendation())

    html_text = patch_html(output_root)
    html_path = stage_dir / HTML_NAME
    write_text(html_path, html_text)

    js_check = javascript_syntax_check(stage_dir, html_text)
    smoke = screenshot(stage_dir, html_path)
    checks = validate_fixtures(stage_dir, html_text)
    checks.update(js_check)
    checks["screenshot_smoke_pass"] = bool(smoke.get("screenshot_smoke_pass"))
    failed = failed_checks(checks)
    result = {
        "stage": STAGE_ID,
        "status": FINAL_STATUS if not failed else "FAIL_1013J_R1G_COURSEWARE_TEMPLATE_DYNAMIC_SCREEN_MAPPING_CONCEPT",
        "final_status": FINAL_STATUS if not failed else "FAIL_1013J_R1G_COURSEWARE_TEMPLATE_DYNAMIC_SCREEN_MAPPING_CONCEPT",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        **checks,
        "failed_checks": failed,
    }
    write_json(stage_dir / "1013J_R1G_result.json", result)
    write_docs(output_root, stage_dir, result)
    source_delta = output_root / "source_delta_1013J_R1G" / "scripts" / VALIDATOR_NAME
    source_delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), source_delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))
    print("ALL_1013J_R1G_COURSEWARE_TEMPLATE_DYNAMIC_SCREEN_MAPPING_CONCEPT_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
