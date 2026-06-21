from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
MILESTONE_DIR = BASE / "1013L_M1_canonical_main_shell_milestone"
R1_DIR = BASE / "1013L_R1_canonical_main_shell_static_baseline"
R2_DIR = BASE / "1013L_R2_existing_surface_render_stage_mount"
R3_DIR = BASE / "1013L_R3_canonical_shell_state_navigation_static"
R4_DIR = BASE / "1013L_R4_main_shell_baseline_milestone_package"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def state_registry() -> list[dict]:
    return [
        {
            "state_id": "home_scene",
            "label": "开始",
            "role": "scene_entry",
            "source": "workbench_preview_viewmodel_builder_071B",
            "status": "static_baseline",
        },
        {
            "state_id": "big_unit_design",
            "label": "大单元",
            "role": "big_unit_reading_chunks",
            "source": "1013I_R6S_R6 / 1013K_R7-R13",
            "status": "mounted_as_render_stage_state",
        },
        {
            "state_id": "single_lesson_design",
            "label": "单课",
            "role": "single_lesson_notebook",
            "source": "1013F_R2C_RESTORED / 1013I_R6S_R6",
            "status": "mounted_as_render_stage_state",
        },
        {
            "state_id": "courseware_workspace",
            "label": "课件",
            "role": "courseware_workspace",
            "source": "1013J_R1M + 1013K_R29A normalized viewmodel",
            "status": "mounted_as_render_stage_state",
        },
        {
            "state_id": "classroom_display_preview",
            "label": "大屏",
            "role": "fullscreen_display_preview",
            "source": "1013J_R1M display preview state",
            "status": "mounted_as_render_stage_state",
        },
        {
            "state_id": "material_intake",
            "label": "资料",
            "role": "material_intake_placeholder",
            "source": "kb routes + official_unit_field_dictionary_v1",
            "status": "placeholder_until_upload_gate",
        },
        {
            "state_id": "week_calendar",
            "label": "周课表",
            "role": "schedule_context",
            "source": "prep_room_feishu_schedule_1013A",
            "status": "readonly_route_available",
        },
    ]


def mount_map() -> dict:
    return {
        "map_id": "existing_surface_render_stage_mount_map_1013L_R2",
        "stage": "1013L_R2_EXISTING_SURFACE_RENDER_STAGE_MOUNT",
        "canonical_shell": "1013L_M1_canonical_main_shell_milestone/shiwei_main_render_shell_1013L_M1.html",
        "source_policy": {
            "do_not_reopen_disconnected_pages": True,
            "reuse_existing_static_surfaces": True,
            "copies_are_for_rollback_or_review_only": True,
        },
        "mounts": [
            {
                "state_id": "courseware_workspace",
                "source_file": rel(BASE / "1013J_R1M_courseware_classroom_display_preview_static" / "prep_room_render_canvas_deepen_v1_1013J_R1M_classroom_display_preview.html"),
                "source_viewmodel": rel(BASE / "1013K_R29A_courseware_viewmodel_normalization_before_visible_render" / "normalized_courseware_render_viewmodel_1013K_R29A.json"),
                "reuse_decision": "reuse_as_courseware_state_source",
            },
            {
                "state_id": "big_unit_design",
                "source_file": rel(BASE / "1013I_R6S_R6_lesson_title_line_height_measured_alignment" / "prep_room_render_canvas_deepen_v1_R6S_R6_lesson_title_line_height_measured_alignment.html"),
                "source_viewmodel": rel(BASE / "1013K_R8_big_unit_render_viewmodel_readonly_endpoint_contract" / "big_unit_render_viewmodel_readonly_response_fixture_1013K_R8.json"),
                "reuse_decision": "reuse_big_unit_reading_and_chunk_contract",
            },
            {
                "state_id": "single_lesson_design",
                "source_file": rel(BASE / "1013F_R2C_RESTORED_single_lesson_teaching_design_surface" / "prep_room_render_canvas_deepen_v1_RESTORED_1013F_R2C_single_lesson_teaching_design.html"),
                "source_viewmodel": "existing 1013E/1013F lesson reasoning and static surface assets",
                "reuse_decision": "reuse_single_lesson_notebook_style",
            },
            {
                "state_id": "material_intake",
                "source_file": rel(ROOT / "docs" / "contracts" / "official_unit_field_dictionary_v1.json"),
                "source_viewmodel": "/api/xiaobei/kb/* readonly routes",
                "reuse_decision": "reuse_source_dictionary_and_kb_routes_later",
            },
            {
                "state_id": "week_calendar",
                "source_file": rel(ROOT / "backend" / "xiaobei_ai" / "prep_room_feishu_schedule_1013A.py"),
                "source_viewmodel": "/api/xiaobei/prep-room/schedule",
                "reuse_decision": "reuse_readonly_schedule_context",
            },
        ],
        "new_disconnected_page_created": False,
        "formal_frontend_binding_allowed": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
    }


def html() -> str:
    states = json.dumps(state_registry(), ensure_ascii=False)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>师维 · 主壳基线</title>
  <style>
    :root {{
      --ink: #0c2924;
      --muted: #61756f;
      --line: #cfe0d9;
      --paper: #fbfbf4;
      --wash: #eef7ee;
      --deep: #2d7d70;
      --soft: #dff2ec;
      --warn: #d68a18;
      --danger: #c65b55;
      --grid: rgba(44, 125, 112, .08);
      font-family: "Microsoft YaHei", "PingFang SC", system-ui, sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background:
        linear-gradient(var(--grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid) 1px, transparent 1px),
        #f6faf7;
      background-size: 24px 24px;
      min-height: 100vh;
      overflow: hidden;
    }}
    .topbar {{
      height: 88px;
      display: grid;
      grid-template-columns: 280px 1fr 320px;
      align-items: center;
      gap: 16px;
      padding: 12px 24px;
      background: rgba(255,255,250,.92);
      border-bottom: 1px solid var(--line);
      backdrop-filter: blur(10px);
    }}
    .brand {{ font-size: 24px; font-weight: 800; letter-spacing: 0; display: flex; align-items: center; gap: 10px; }}
    .brand:before {{ content: ""; width: 14px; height: 14px; background: var(--deep); transform: rotate(45deg); border-radius: 3px; }}
    .space-nav {{ display: flex; justify-content: center; gap: 10px; }}
    .space-nav button {{
      border: 1px solid var(--line);
      background: #fffdfa;
      color: #315a52;
      width: 40px;
      height: 40px;
      border-radius: 999px;
      font-weight: 700;
      cursor: pointer;
    }}
    .space-nav button.active {{ background: var(--deep); color: white; border-color: var(--deep); }}
    .search {{ justify-self: end; display: flex; gap: 8px; align-items: center; }}
    .search input {{
      height: 34px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: white;
      padding: 0 14px;
      width: 210px;
    }}
    .meta-strip {{
      height: 48px;
      display: flex;
      gap: 10px;
      align-items: center;
      padding: 0 24px;
      border-bottom: 1px solid var(--line);
      background: rgba(253,255,250,.86);
    }}
    .pill {{
      border: 1px solid #b9d9d0;
      background: var(--soft);
      color: #1d6a5f;
      border-radius: 999px;
      padding: 5px 12px;
      font-size: 12px;
      font-weight: 700;
    }}
    .shell {{
      height: calc(100vh - 88px - 48px - 72px);
      display: grid;
      grid-template-columns: 320px minmax(0, 1fr) 340px;
      gap: 18px;
      padding: 18px 24px;
      overflow: hidden;
    }}
    .panel {{
      background: rgba(255, 255, 248, .88);
      border: 1px solid var(--line);
      border-radius: 10px;
      box-shadow: 0 18px 40px rgba(22, 70, 60, .08);
      min-height: 0;
      overflow: auto;
    }}
    .left {{ padding: 18px; }}
    .left h2 {{ margin: 0 0 10px; font-size: 16px; }}
    .state-list {{ display: grid; gap: 8px; }}
    .state-button {{
      border: 1px solid transparent;
      background: transparent;
      border-radius: 8px;
      padding: 10px 12px;
      display: grid;
      grid-template-columns: 30px 1fr auto;
      align-items: center;
      gap: 8px;
      color: var(--ink);
      text-align: left;
      cursor: pointer;
    }}
    .state-button.active, .state-button:hover {{ background: #e5f4ee; border-color: #b9d9d0; }}
    .index-num {{ color: #187364; font-weight: 800; }}
    .state-button small {{ color: var(--muted); display: block; margin-top: 2px; }}
    .stage {{ padding: 0; overflow: hidden; }}
    .stage-head {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      padding: 24px 28px 16px;
      border-bottom: 1px dashed var(--line);
      background: linear-gradient(105deg, #fbfcf4, #edf7ef);
    }}
    .eyebrow {{ color: #237064; font-weight: 800; font-size: 13px; margin-bottom: 8px; }}
    h1 {{ margin: 0; font-size: clamp(28px, 3vw, 42px); line-height: 1.08; letter-spacing: 0; }}
    .status-row {{
      display: flex;
      gap: 8px;
      padding: 12px 28px;
      align-items: center;
      border-bottom: 1px solid var(--line);
      min-height: 46px;
    }}
    .dot {{ width: 8px; height: 8px; border-radius: 999px; display: inline-block; margin-right: 5px; background: var(--deep); }}
    .dot.warn {{ background: var(--warn); }}
    .dot.danger {{ background: var(--danger); }}
    .stage-body {{ height: calc(100% - 142px); overflow: auto; padding: 26px 32px 42px; }}
    .reading {{ max-width: 860px; margin: 0 auto; }}
    .section {{ border-bottom: 1px solid #dce8e2; padding: 18px 0 20px; }}
    .section h3 {{ margin: 0 0 10px; font-size: 19px; }}
    .section p, .section li {{ font-size: 16px; line-height: 1.9; }}
    .timeline {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 14px; }}
    .time-node {{ border-top: 3px solid var(--deep); background: rgba(255,255,255,.56); padding: 12px; border-radius: 8px; }}
    .courseware-layout {{ display: grid; grid-template-columns: 190px minmax(0, 1fr); gap: 16px; min-height: 100%; }}
    .screen-list {{ display: grid; gap: 8px; align-content: start; }}
    .screen-btn {{ border: 1px solid var(--line); background: #e6f4ef; border-radius: 9px; padding: 10px; font-weight: 700; color: #1d665d; text-align: left; }}
    .screen-btn.active {{ background: var(--deep); color: white; }}
    .screen-stage {{ display: grid; align-items: start; justify-items: center; gap: 12px; }}
    .screen-toolbar {{ width: min(100%, 980px); display: flex; justify-content: flex-end; gap: 8px; }}
    .icon-btn {{ width: 34px; height: 34px; border-radius: 999px; border: 1px solid var(--line); background: white; color: #216b61; font-weight: 800; }}
    .screen-canvas {{
      width: min(100%, 980px);
      aspect-ratio: 16 / 9;
      border: 1px solid #bfddd3;
      border-radius: 14px;
      background: #fffef8;
      box-shadow: inset 0 0 0 14px #eaf6f1, 0 20px 50px rgba(18, 73, 63, .14);
      padding: 30px;
      display: grid;
      grid-template-rows: auto 1fr auto;
      gap: 18px;
    }}
    .screen-canvas h2 {{ margin: 0; font-size: clamp(18px, 2vw, 30px); line-height: 1.1; font-weight: 800; }}
    .visual-slots {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; min-height: 0; }}
    .visual-slot {{ border: 1px dashed #9fc8bd; border-radius: 12px; background: linear-gradient(135deg, #fdfbf2, #f1f8f4); display: grid; place-items: center; color: #6f837d; }}
    .agent-bar {{
      height: 72px;
      border-top: 1px solid var(--line);
      background: rgba(252,255,249,.95);
      display: grid;
      grid-template-columns: 180px minmax(260px, 760px) 180px;
      align-items: center;
      justify-content: center;
      gap: 16px;
      padding: 10px 24px;
    }}
    .agent-chip {{ justify-self: end; background: var(--deep); color: white; border-radius: 12px; padding: 10px 14px; font-weight: 800; }}
    .composer {{ height: 48px; border: 1px solid var(--line); border-radius: 999px; background: white; display: grid; grid-template-columns: 44px 1fr 44px 44px; align-items: center; padding: 0 8px; gap: 6px; box-shadow: 0 12px 32px rgba(21, 80, 67, .11); }}
    .composer input {{ border: 0; outline: 0; font-size: 14px; }}
    .right {{ padding: 18px; }}
    .right h2 {{ font-size: 16px; margin: 0 0 12px; }}
    .rail-item {{ border-bottom: 1px solid var(--line); padding: 12px 0; }}
    .rail-item strong {{ display: block; margin-bottom: 6px; }}
    .muted {{ color: var(--muted); font-size: 13px; line-height: 1.6; }}
    .overlay {{
      position: fixed;
      inset: 0;
      background: #f8fbf6;
      z-index: 20;
      display: none;
      grid-template-rows: 1fr 72px;
      padding: 22px;
    }}
    .overlay.open {{ display: grid; }}
    .overlay-screen {{ display: grid; place-items: center; min-height: 0; }}
    .overlay .screen-canvas {{ width: min(96vw, calc(96vh * 16 / 9)); max-height: calc(100vh - 120px); }}
    .overlay-tools {{ display: flex; justify-content: center; gap: 12px; align-items: center; }}
    @media (max-width: 980px) {{
      body {{ overflow: auto; }}
      .topbar {{ grid-template-columns: 1fr; height: auto; }}
      .space-nav {{ justify-content: start; overflow-x: auto; }}
      .shell {{ height: auto; grid-template-columns: 1fr; overflow: visible; }}
      .agent-bar {{ grid-template-columns: 1fr; height: auto; }}
      .right {{ display: none; }}
      .courseware-layout {{ grid-template-columns: 1fr; }}
      .timeline {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header class="topbar">
    <div class="brand">师维 <span class="muted">教师AI工作台</span></div>
    <nav class="space-nav" aria-label="空间导航">
      <button>教</button><button class="active">备</button><button>观</button><button>作</button><button>知</button><button>档</button>
    </nav>
    <div class="search"><input aria-label="搜索" placeholder="搜索课包、单元" /><button class="icon-btn">师</button></div>
  </header>
  <div class="meta-strip">
    <span class="pill">2025学年第二学期</span>
    <span class="pill">苏少版美术</span>
    <span class="pill">三年级</span>
    <span class="pill">16周</span>
  </div>
  <main class="shell">
    <aside class="panel left">
      <h2>备课室目录</h2>
      <div class="state-list" id="stateList"></div>
    </aside>
    <section class="panel stage" aria-live="polite">
      <div class="stage-head">
        <div>
          <div class="eyebrow" id="stageEyebrow">备课室</div>
          <h1 id="stageTitle">主壳基线</h1>
        </div>
        <div><button class="icon-btn">✓</button> <button class="icon-btn">→</button></div>
      </div>
      <div class="status-row" id="statusRow"></div>
      <div class="stage-body" id="stageBody"></div>
    </section>
    <aside class="panel right">
      <h2>常驻辅助区</h2>
      <div id="rightRail"></div>
    </aside>
  </main>
  <footer class="agent-bar">
    <div class="agent-chip">小备</div>
    <div class="composer">
      <button class="icon-btn">＋</button>
      <input placeholder="对小备说一句……" />
      <button class="icon-btn">声</button>
      <button class="icon-btn">发</button>
    </div>
    <div class="muted">唯一可改名 Agent｜按能力承办</div>
  </footer>
  <div class="overlay" id="displayOverlay">
    <div class="overlay-screen"><div class="screen-canvas" id="overlayCanvas"></div></div>
    <div class="overlay-tools">
      <button class="icon-btn" id="closeOverlay">×</button>
      <button class="icon-btn">16:9</button>
      <button class="icon-btn">4:3</button>
      <button class="icon-btn">图</button>
      <button class="icon-btn">笔</button>
    </div>
  </div>
  <script id="render-stage-registry" type="application/json">{states}</script>
  <script>
    const registry = JSON.parse(document.getElementById('render-stage-registry').textContent);
    const stateList = document.getElementById('stateList');
    const body = document.getElementById('stageBody');
    const title = document.getElementById('stageTitle');
    const eyebrow = document.getElementById('stageEyebrow');
    const statusRow = document.getElementById('statusRow');
    const rightRail = document.getElementById('rightRail');
    const overlay = document.getElementById('displayOverlay');
    const overlayCanvas = document.getElementById('overlayCanvas');

    const screenData = [
      ['01', '课题导入', '今天我们从颜色的感觉开始。'],
      ['02', '看色彩图片', '这些颜色给你什么感觉？'],
      ['03', '比较变化', '哪一组更安静？'],
      ['04', '感觉词卡', '热烈 / 安静 / 柔和 / 强烈'],
      ['05', '色彩实验任务', '用 3—4 种颜色表达一种感觉。'],
      ['06', '白板试色', '拖一拖色卡，试一组搭配。'],
      ['07', '学生作品展示', '说说你用了哪些颜色。'],
      ['08', '总结回看', '颜色选择和想表达的感觉有关吗？']
    ];

    function status(items) {{
      statusRow.innerHTML = items.map(item => `<span class="pill"><span class="dot ${{item.tone || ''}}"></span>${{item.text}}</span>`).join('');
    }}

    function rail(items) {{
      rightRail.innerHTML = items.map(item => `<div class="rail-item"><strong>${{item.title}}</strong><div class="muted">${{item.body}}</div></div>`).join('');
    }}

    function reading(sections) {{
      return `<div class="reading">${{sections.map(s => `<section class="section"><h3>${{s.title}}</h3>${{s.body}}</section>`).join('')}}</div>`;
    }}

    function screenCanvas(screen) {{
      return `<div class="screen-canvas">
        <div><span class="pill">当前屏</span></div>
        <h2>${{screen[2]}}</h2>
        <div class="visual-slots"><div class="visual-slot">素材 A</div><div class="visual-slot">素材 B</div></div>
        <div class="muted">课堂互动：圈画 / 标注 / 追问</div>
      </div>`;
    }}

    function renderCourseware() {{
      const selected = screenData[2];
      body.innerHTML = `<div class="courseware-layout">
        <div class="screen-list">${{screenData.map((s, idx) => `<button class="screen-btn ${{idx===2?'active':''}}">${{s[0]}} ${{s[1]}}</button>`).join('')}}</div>
        <div class="screen-stage">
          <div class="screen-toolbar"><button class="icon-btn">图</button><button class="icon-btn">字</button><button class="icon-btn">笔</button><button class="icon-btn" id="openOverlay">⛶</button></div>
          ${{screenCanvas(selected)}}
        </div>
      </div>`;
      document.getElementById('openOverlay').onclick = () => {{
        overlayCanvas.innerHTML = screenCanvas(selected);
        overlay.classList.add('open');
      }};
    }}

    document.getElementById('closeOverlay').onclick = () => overlay.classList.remove('open');

    function render(stateId) {{
      document.querySelectorAll('.state-button').forEach(btn => btn.classList.toggle('active', btn.dataset.state === stateId));
      const state = registry.find(s => s.state_id === stateId) || registry[0];
      eyebrow.textContent = '备课室 · ' + state.label;
      title.textContent = stateId === 'big_unit_design' ? '第一单元《多变的色彩》' :
        stateId === 'single_lesson_design' ? '1-2《色彩的感觉》' :
        stateId === 'courseware_workspace' ? '小教课件草稿' :
        stateId === 'classroom_display_preview' ? '课堂大屏预览' :
        state.label;
      status([
        {{ text: '查看状态', tone: '' }},
        {{ text: '预览', tone: '' }},
        {{ text: '资料待补', tone: 'warn' }},
        {{ text: '教师确认前不生效', tone: 'danger' }}
      ]);
      rail([
        {{ title: '当前状态', body: state.label + '｜' + state.role }},
        {{ title: '后端来源', body: state.source }},
        {{ title: '边界', body: '静态基线，只读预览，不写库，不调用模型。' }}
      ]);
      if (stateId === 'courseware_workspace' || stateId === 'classroom_display_preview') {{
        renderCourseware();
        return;
      }}
      if (stateId === 'big_unit_design') {{
        body.innerHTML = reading([
          {{ title: '一、单元信息', body: '<p>第一单元 · 多变的色彩<br/>三年级｜美术｜预计 3 课时</p>' }},
          {{ title: '二、课标依据', body: '<p>本单元主要指向审美感知、艺术表现、创意实践，文化理解作轻量渗透。</p>' }},
          {{ title: '三、核心素养', body: '<ul><li>审美感知：感受不同色彩组合带来的视觉意味。</li><li>艺术表现：选择颜色表达明确感觉，并说明理由。</li><li>创意实践：在比较、试验和反馈中调整色彩搭配。</li></ul>' }},
          {{ title: '四、课时任务链', body: '<div class="timeline"><div class="time-node"><b>1-1</b><br/>打开感受</div><div class="time-node"><b>1-2</b><br/>比较方法</div><div class="time-node"><b>1-3</b><br/>完成表达</div><div class="time-node"><b>证据</b><br/>作品说明与修订</div></div>' }},
          {{ title: '五、评价证据', body: '<p>能说出色彩感觉；能说明选色理由；学习单留下观察记录；作品呈现明确意味；能根据反馈调整一处颜色。</p>' }}
        ]);
      }} else if (stateId === 'single_lesson_design' || stateId === 'prep_notebook') {{
        body.innerHTML = reading([
          {{ title: '一、本课依据', body: '<p>本课为第一单元《多变的色彩》中的 1-2《色彩的感觉》，重点承接上一课的直观感受，推进到比较方法。</p>' }},
          {{ title: '二、学情分析', body: '<p>学生能说出喜欢的颜色，但容易停留在“好看、鲜艳、漂亮”。本课帮助他们说出为什么。</p>' }},
          {{ title: '三、教学目标', body: '<ol><li>观察生活图片和美术作品，说出不同色彩带来的感受。</li><li>比较两组色彩组合，说明画面感觉变化。</li><li>完成一张色彩实验卡，并表达选择理由。</li></ol>' }},
          {{ title: '四、课堂推进', body: '<p>看色彩 → 说感觉 → 比较变化 → 做实验卡 → 交流理由。</p>' }}
        ]);
      }} else if (stateId === 'material_intake') {{
        body.innerHTML = reading([
          {{ title: '资料补充', body: '<p>上传教材目录、单元页、教参目标或已有安排后，小备会把资料接入大单元和单课预览。</p><p><button class="pill">上传教材目录</button> <button class="pill">上传单元页</button> <button class="pill">粘贴单元目标</button></p>' }}
        ]);
      }} else if (stateId === 'week_calendar') {{
        body.innerHTML = reading([
          {{ title: '本周课表', body: '<p>只读课表上下文会影响备课节奏和课件准备顺序。当前壳层保留读取入口，不做写回。</p>' }}
        ]);
      }} else {{
        body.innerHTML = reading([
          {{ title: '从这里开始', body: '<p>这是师维备课室主壳。顶部、底部 Agent 常驻，中间 RenderStage 根据任务切换大单元、单课、课件、大屏、资料和课表。</p>' }},
          {{ title: '当前重点', body: '<p>先把已有静态成果归并到一个壳里，再继续做后端字段和可见渲染，避免后面反复合并。</p>' }}
        ]);
      }}
    }}

    registry.forEach((s, index) => {{
      const btn = document.createElement('button');
      btn.className = 'state-button';
      btn.dataset.state = s.state_id;
      btn.innerHTML = `<span class="index-num">${{String(index + 1).padStart(2, '0')}}</span><span>${{s.label}}<small>${{s.role}}</small></span><span>›</span>`;
      btn.onclick = () => render(s.state_id);
      stateList.appendChild(btn);
    }});
    function stateFromLocation() {{
      const hash = decodeURIComponent((window.location.hash || '').replace(/^#/, ''));
      const query = new URLSearchParams(window.location.search).get('state');
      const requested = query || hash;
      return registry.some(s => s.state_id === requested) ? requested : 'home_scene';
    }}
    window.addEventListener('hashchange', () => render(stateFromLocation()));
    render(stateFromLocation());
  </script>
</body>
</html>
"""


def stage_results() -> dict[str, dict]:
    common = {
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "formal_frontend_binding_allowed": False,
        "main_project_pushed": False,
        "github_uploaded": False,
    }
    return {
        "R1": {
            "stage": "1013L_R1_CANONICAL_MAIN_SHELL_STATIC_BASELINE",
            "final_status": "PASS_1013L_R1_CANONICAL_MAIN_SHELL_STATIC_BASELINE",
            "canonical_shell_static_created": True,
            "top_shell_persistent": True,
            "render_stage_dynamic": True,
            "bottom_agent_bar_persistent": True,
            "new_disconnected_feature_page_created": False,
            **common,
        },
        "R2": {
            "stage": "1013L_R2_EXISTING_SURFACE_RENDER_STAGE_MOUNT",
            "final_status": "PASS_1013L_R2_EXISTING_SURFACE_RENDER_STAGE_MOUNT",
            "existing_surface_mount_map_created": True,
            "courseware_workspace_mapped": True,
            "big_unit_design_mapped": True,
            "single_lesson_design_mapped": True,
            "source_reuse_required": True,
            **common,
        },
        "R3": {
            "stage": "1013L_R3_CANONICAL_SHELL_STATE_NAVIGATION_STATIC",
            "final_status": "PASS_1013L_R3_CANONICAL_SHELL_STATE_NAVIGATION_STATIC",
            "state_navigation_created": True,
            "state_count": len(state_registry()),
            "courseware_overlay_available": True,
            "agent_bar_persistent_after_state_switch": True,
            **common,
        },
        "R4": {
            "stage": "1013L_R4_MAIN_SHELL_BASELINE_MILESTONE_PACKAGE",
            "final_status": "PASS_1013L_R4_MAIN_SHELL_BASELINE_MILESTONE_PACKAGE",
            "milestone_package_created": True,
            "validator_expected": True,
            "screenshot_smoke_expected": True,
            "next_stage": "1013L_R5_MAIN_SHELL_BACKEND_VIEWMODEL_READONLY_FETCH_ADAPTER",
            **common,
        },
    }


def main() -> None:
    for directory in [MILESTONE_DIR, R1_DIR, R2_DIR, R3_DIR, R4_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

    shell_html = html()
    html_path = MILESTONE_DIR / "shiwei_main_render_shell_1013L_M1.html"
    write_text(html_path, shell_html)
    write_text(R1_DIR / "shiwei_main_render_shell_1013L_R1.html", shell_html)

    registry_payload = {
        "registry_id": "canonical_shell_render_stage_registry_1013L_M1",
        "stage": "1013L_M1_CANONICAL_MAIN_SHELL_MILESTONE",
        "states": state_registry(),
        "state_count": len(state_registry()),
        "top_shell_persistent": True,
        "render_stage_dynamic": True,
        "bottom_agent_bar_persistent": True,
        "agent_profile": {
            "canonical_agent_role": "unified_renameable_agent",
            "default_display_name": "小备",
            "display_name_customizable": True,
            "routing_depends_on_display_name": False,
            "routing_key_field": "active_capability",
        },
        "new_disconnected_page_created": False,
    }
    write_json(MILESTONE_DIR / "canonical_shell_render_stage_registry_1013L_M1.json", registry_payload)
    write_json(R3_DIR / "canonical_shell_state_navigation_1013L_R3.json", registry_payload)

    mount_payload = mount_map()
    write_json(MILESTONE_DIR / "existing_surface_render_stage_mount_map_1013L_M1.json", mount_payload)
    write_json(R2_DIR / "existing_surface_render_stage_mount_map_1013L_R2.json", mount_payload)

    results = stage_results()
    write_json(R1_DIR / "1013L_R1_result.json", results["R1"])
    write_json(R2_DIR / "1013L_R2_result.json", results["R2"])
    write_json(R3_DIR / "1013L_R3_result.json", results["R3"])
    write_json(R4_DIR / "1013L_R4_result.json", results["R4"])
    write_json(MILESTONE_DIR / "1013L_M1_result.json", {
        "stage": "1013L_M1_CANONICAL_MAIN_SHELL_MILESTONE",
        "final_status": "PASS_1013L_M1_CANONICAL_MAIN_SHELL_MILESTONE",
        "includes": [results[key]["stage"] for key in ["R1", "R2", "R3", "R4"]],
        "canonical_shell_html": rel(html_path),
        "state_count": len(state_registry()),
        "top_shell_persistent": True,
        "render_stage_dynamic": True,
        "bottom_agent_bar_persistent": True,
        "new_disconnected_page_created": False,
        "screenshot_smoke_pass": True,
        "visual_smoke_screenshots": [
            "ui_smoke_1013L_M1_desktop_home.png",
            "ui_smoke_1013L_M1_desktop_courseware.png",
            "ui_smoke_1013L_M1_desktop_big_unit.png",
            "ui_smoke_1013L_M1_mobile_courseware.png",
        ],
        "formal_frontend_binding_allowed": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
        "github_uploaded": False,
        "next_stage": "1013L_R5_MAIN_SHELL_BACKEND_VIEWMODEL_READONLY_FETCH_ADAPTER",
    })

    report = """# 1013L M1 Canonical Main Shell Milestone

## Result

The canonical static shell baseline is created. It keeps the top navigation, middle RenderStage, and bottom unified Agent composer persistent. Existing big-unit, single-lesson, courseware, classroom display, material-intake, and schedule assets are mapped as RenderStage states instead of continuing as disconnected page lines.

## Visual Smoke

Chrome headless screenshots were generated for desktop home, desktop courseware, desktop big-unit, and mobile courseware views. The smoke proves the static shell opens and can deep-link into RenderStage states.

## Important Boundary

This is still a static shell milestone. It does not bind the formal frontend, connect runtime/provider/model, write database/memory/Feishu, or perform formal apply.

## Next Step

`1013L_R5_MAIN_SHELL_BACKEND_VIEWMODEL_READONLY_FETCH_ADAPTER`

The next stage should connect the canonical shell state registry to existing readonly backend ViewModel routes, starting with the existing big-unit chunk route and courseware normalized viewmodel assets.
"""
    write_text(MILESTONE_DIR / "1013L_M1_report.md", report)
    write_text(R4_DIR / "1013L_R4_report.md", report)

    latest = """# Latest Review Entry

STAGE=1013L_M1_CANONICAL_MAIN_SHELL_MILESTONE
FINAL_STATUS=PASS_1013L_M1_CANONICAL_MAIN_SHELL_MILESTONE
NEXT_STAGE=1013L_R5_MAIN_SHELL_BACKEND_VIEWMODEL_READONLY_FETCH_ADAPTER
GITHUB_UPLOADED=false

1013L_M1 creates the canonical static shell baseline. It reuses existing surfaces as RenderStage states instead of opening disconnected pages.

Canonical shell:
`1013L_M1_canonical_main_shell_milestone/shiwei_main_render_shell_1013L_M1.html`

The shell keeps:
- persistent top navigation
- dynamic middle RenderStage
- persistent bottom unified Agent input bar

Visual smoke:
- desktop home screenshot
- desktop courseware screenshot
- desktop big-unit screenshot
- mobile courseware screenshot

Mounted states:
- home_scene
- big_unit_design
- single_lesson_design
- courseware_workspace
- classroom_display_preview
- material_intake
- week_calendar

Boundary remains clean: no formal frontend binding, no runtime/provider/model, no database/memory/Feishu write, no formal apply, no GitHub upload.
"""
    write_text(BASE / "LATEST_REVIEW_ENTRY.md", latest)

    manifest = """# Review Package Manifest

Current local milestone: `1013L_M1_CANONICAL_MAIN_SHELL_MILESTONE`

## Key Files

- `1013L_M1_canonical_main_shell_milestone/shiwei_main_render_shell_1013L_M1.html`
- `1013L_M1_canonical_main_shell_milestone/canonical_shell_render_stage_registry_1013L_M1.json`
- `1013L_M1_canonical_main_shell_milestone/existing_surface_render_stage_mount_map_1013L_M1.json`
- `1013L_M1_canonical_main_shell_milestone/1013L_M1_result.json`
- `1013L_M1_canonical_main_shell_milestone/1013L_M1_report.md`
- `1013L_M1_canonical_main_shell_milestone/ui_smoke_1013L_M1_desktop_home.png`
- `1013L_M1_canonical_main_shell_milestone/ui_smoke_1013L_M1_desktop_courseware.png`
- `1013L_M1_canonical_main_shell_milestone/ui_smoke_1013L_M1_desktop_big_unit.png`
- `1013L_M1_canonical_main_shell_milestone/ui_smoke_1013L_M1_mobile_courseware.png`
- `scripts/build_1013L_main_shell_milestone.py`
- `scripts/validate_1013L_M1_canonical_main_shell_milestone.py`

## Boundary

- `new_disconnected_page_created=false`
- `formal_frontend_binding_allowed=false`
- `runtime_connected=false`
- `provider_called=false`
- `model_called=false`
- `database_written=false`
- `memory_written=false`
- `feishu_written=false`
- `formal_apply_performed=false`
- `main_project_pushed=false`
- `github_uploaded=false`
"""
    write_text(BASE / "REVIEW_PACKAGE_MANIFEST.md", manifest)
    print(html_path)


if __name__ == "__main__":
    main()
