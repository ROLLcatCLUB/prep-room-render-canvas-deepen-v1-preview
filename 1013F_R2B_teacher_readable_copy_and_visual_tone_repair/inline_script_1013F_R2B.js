
    window.PREP_ROOM_RENDER_VIEW_MODEL = {
      stage_code: "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1",
      renderer_mode: "static_fixture_only",
      active_view: "weekCalendar",
      selected_node_id: "wc-wed-p2",
      view_scroll_positions: {},
      role: {
        id: "art_teacher",
        label: "美术教师"
      },
      shell: {
        name: "ShiweiShell",
        top: "TopSpaceNav",
        stage: "RenderStage",
        bottom: "BottomIntentBar"
      },
      space: {
        id: "prep_room",
        label: "备课室",
        agent_position: "xiaobei_prep_assistant"
      },
      safety: {
        provider_called: false,
        model_called: false,
        api_connected: false,
        feishu_schedule_read_allowed: true,
        feishu_schedule_write_performed: false,
        database_write_performed: false,
        formal_apply_performed: false,
        teacher_review_required: true
      },
      schedule_adapter: {
        stage_id: "1013A_FEISHU_FORMAL_SCHEDULE_READONLY_ADAPTER",
        endpoint: "http://127.0.0.1:8082/api/xiaobei/prep-room/schedule",
        source_kind: "feishu_full_dump_snapshot",
        live_read_allowed: true,
        write_allowed: false,
        status: "课表快照已绑定，正式凭据就绪后自动读取只读接口"
      },
      flow_steps: [
        { id: "prep_room", label: "备课室", current: true },
        { id: "classroom", label: "教室", current: false },
        { id: "gallery", label: "作品馆", current: false },
        { id: "archive", label: "档案室", current: false },
        { id: "loop", label: "回流", current: false }
      ],
      negotiation: {
        assistant_name: "小教",
        assistant_role: "备课室主助理 · 小教/小管协同",
        prompt: "对小教说一句",
        input_value: "帮我看看本周哪些课前包还没备齐，先处理今天和明天要上的课。",
        chips: [
          "某个课包来不及准备",
          "学校活动占用一节课",
          "公开课要提前",
          "想保留作品产出"
        ],
        understanding: [
          "影响范围：第10-11周《青绿中国色》、第12周《足下生辉》和本学期作品沉淀。",
          "小教判断：先处理今日和明日课前包缺口，周六调休课由小教协同保持预演。",
          "协同对象：小美补学习单视觉，小评预置评价维度，小管等待归档字段。"
        ],
        notes: {
          weekCalendar: "周课表已绑定正式课表只读来源；当前展示徐涛老师三年级美术正式课位，后续凭据就绪后可自动刷新。",
          prepNotebook: "备课本当前聚焦真实课题 1-2《色彩的感觉》：默认读课，编辑时再集中处理段落候选、资料引用和待沉淀内容。",
          classProgressSchedule: "班级排课使用真实课题和正式课位作为落点依据，但顺延和调课仍等待教师确认。",
          flexibleSemesterMap: "学期规划已采用 16 周教学进度：教材学习 19 课时、创艺节 4 课时、机动 6 课时。"
        }
      },
      views: [
        {
          id: "weekCalendar",
          label: "周课表",
          title: "本周课表",
          kicker: "Week Calendar Board",
          summary: "展示本周每天每节课要上的班级、课题、课前包准备状态，以及活动、调课、节假日和调休占用。用于课前执行，不替代班级进度与排课。",
          term: "2025-2026学年第二学期",
          active_grade: "三年级",
          week_label: "正式课表周",
          date_range: "课表只读",
          grade_options: ["三年级", "四年级", "五年级", "六年级"],
          week_modes: ["上一周", "本周", "下一周"],
          days: [
            { id: "mon", label: "周一", date: "5.05", state: "past" },
            { id: "tue", label: "周二", date: "5.06", state: "past" },
            { id: "wed", label: "周三", date: "5.07", state: "past" },
            { id: "thu", label: "周四", date: "5.08", state: "today" },
            { id: "fri", label: "周五", date: "5.09", state: "future" },
            { id: "sat", label: "周六", date: "5.10", state: "workday" },
            { id: "sun", label: "周日", date: "5.11", state: "weekend" }
          ],
          periods: ["第1节", "第2节", "第3节", "第4节", "第5节", "第6节", "第7节", "第8节"],
          slots: {
            "p6-mon": [{ id: "wc-feishu-mon-p6-g35", type: "lesson", classLabel: "三5班", code: "1-2", title: "色彩的感觉", packageStatus: "正式课表 · 待备课" }],
            "p7-mon": [{ id: "wc-feishu-mon-p7-g31", type: "lesson", classLabel: "三1班", code: "1-2", title: "色彩的感觉", packageStatus: "正式课表 · 待备课" }],
            "p6-tue": [{ id: "wc-feishu-tue-p6-g33", type: "lesson", classLabel: "三3班", code: "1-2", title: "色彩的感觉", packageStatus: "正式课表 · 待备课" }],
            "p3-wed": [{ id: "wc-feishu-wed-p3-g34", type: "lesson", classLabel: "三4班", code: "1-2", title: "色彩的感觉", packageStatus: "正式课表 · 待备课" }],
            "p7-wed": [{ id: "wc-feishu-wed-p7-g33", type: "lesson", classLabel: "三3班", code: "1-2", title: "色彩的感觉", packageStatus: "正式课表 · 待备课" }],
            "p7-thu": [{ id: "wc-feishu-thu-p7-g32", type: "lesson", classLabel: "三2班", code: "1-2", title: "色彩的感觉", packageStatus: "正式课表 · 待备课" }],
            "p5-fri": [{ id: "wc-feishu-fri-p5-g32", type: "lesson", classLabel: "三2班", code: "1-2", title: "色彩的感觉", packageStatus: "正式课表 · 待备课" }],
            "p7-fri": [{ id: "wc-feishu-fri-p7-g31", type: "lesson", classLabel: "三1班", code: "1-2", title: "色彩的感觉", packageStatus: "正式课表 · 待备课" }]
          },
          prep_items: [
            { title: "周一第6节 三5班《色彩的感觉》", status: "进入备课本候选" },
            { title: "周一第7节 三1班《色彩的感觉》", status: "进入备课本候选" },
            { title: "周二第6节 三3班《色彩的感觉》", status: "进入备课本候选" },
            { title: "周三第3节 三4班《色彩的感觉》", status: "进入备课本候选" },
            { title: "周三第7节 三3班《色彩的感觉》", status: "进入备课本候选" },
            { title: "周四第7节 三2班《色彩的感觉》", status: "进入备课本候选" },
            { title: "周五第5节 三2班《色彩的感觉》", status: "进入备课本候选" },
            { title: "周五第7节 三1班《色彩的感觉》", status: "进入备课本候选" }
          ],
          alerts: [
            "已接入徐涛老师三年级美术 8 条正式课位快照。",
            "课表只作为备课上下文，不写回来源系统。",
            "本轮聚焦 1-2《色彩的感觉》主备课画布，课题仍需教师确认。"
          ],
          package_summary: [
            ["课表来源", "正式"],
            ["课位", "8节"],
            ["待备课", "8项"],
            ["写回", "0次"]
          ]
        },
        {
          id: "prepNotebook",
          label: "备课本",
          title: "2025学年第二学期 · 三年级美术备课本",
          kicker: "Prep Notebook",
          summary: "本学期正在生长的过程性工作本。它承接学期、单元、课时、班级课时、课前包、课堂记录、作品证据和课后反思。",
          active_node: "nb-lesson-1-2",
          prep_notebook_mode: "view",
          active_edit_target: {
            section_id: "teaching_process",
            step_id: "explore",
            label: "教学过程 · 探究环节"
          },
          expanded_intent_steps: [],
          lesson_design_mode: "standard_daily",
          lesson_design_modes: [
            { id: "quick_daily", label: "快速", note: "今天能上就行" },
            { id: "standard_daily", label: "标准", note: "正常教学使用" },
            { id: "refined_lesson", label: "精磨", note: "想上得更稳" },
            { id: "open_class", label: "公开课", note: "展示或教研" }
          ],
          reasoning_trace: {
            status: "idle",
            active_index: -1,
            teacher_input: "",
            result: "",
            stages: [
              {
                title: "先判断备课程度",
                pending: "根据这节课准备到什么程度，决定要不要追问、资料用到多深。",
                done: "按当前备课程度处理：优先补齐可上课的教学判断，不写成长篇教案。"
              },
              {
                title: "再看学生卡在哪里",
                pending: "判断孩子现在是不会概念，还是说不清感受，或者不会把感受用到作品里。",
                done: "学生可能停在“好看/不好看”的表层表达，需要更直观的分类和说明。"
              },
              {
                title: "定位要改的位置",
                pending: "把你的话落到具体段落、教学环节和材料位置。",
                done: "已定位到：学情分析、教学过程 · 探究环节、学习单与评价。"
              },
              {
                title: "检查依据和影响",
                pending: "同步检查教材、课标、资料室材料，以及大屏、学习单、评价证据会不会被带动。",
                done: "会影响三处：大屏要有对比图，学习单要有记录格，评价要看学生能否说出理由。"
              },
              {
                title: "整理成候选",
                pending: "把修改收成候选，等待你确认，不直接写进正式结果。",
                done: "已整理为两处候选：探究环节加色卡分组，学习单加感受记录格。"
              }
            ]
          },
          cover: {
            title: "三年级美术 · 2025学年第二学期",
            subtitle: "来源：正式课表 + 2025学年第二学期三年级美术教学工作计划",
            metrics: [
              ["正式课位", "8节"],
              ["当前课例", "1-2"],
              ["待确认", "4项"],
              ["写回", "0次"]
            ]
          },
          tree: [
            {
              id: "nb-term",
              title: "学期工作",
              tone: "green",
              items: [
                { id: "nb-plan", code: "计划", title: "学期规划", status: "done" },
                { id: "nb-schedule", code: "排课", title: "班级进度与排课", status: "warn" },
                { id: "nb-week", code: "周历", title: "周课表", status: "warn" }
              ]
            },
            {
              id: "nb-unit-color",
              title: "第一单元 多变的色彩",
              tone: "green",
              items: [
                { id: "nb-lesson-1-1", code: "1-1", title: "渐变的魅力", status: "done" },
                { id: "nb-lesson-1-2", code: "1-2", title: "色彩的感觉", status: "warn" },
                { id: "nb-lesson-1-3", code: "1-3", title: "渐变的节奏", status: "draft" }
              ]
            },
            {
              id: "nb-unit-shape",
              title: "第二单元 辽阔的海洋",
              tone: "blue",
              items: [
                { id: "nb-lesson-2-1", code: "2-1", title: "奇异的海洋生物", status: "done" },
                { id: "nb-lesson-2-2", code: "2-2", title: "跳动的蓝色心脏", status: "done" },
                { id: "nb-lesson-2-3", code: "2-3", title: "守护生命的摇篮", status: "done" }
              ]
            },
            {
              id: "nb-unit-red",
              title: "第三单元 红领巾告诉我",
              tone: "red",
              items: [
                { id: "nb-lesson-3-1", code: "3-1", title: "影像创作", status: "done" },
                { id: "nb-lesson-3-2", code: "3-2", title: "红色精神传承", status: "done" }
              ]
            },
            {
              id: "nb-unit-qinglv",
              title: "第四单元 青绿中国色",
              tone: "amber",
              items: [
                { id: "nb-lesson-4-1", code: "4-1", title: "矿物颜料与青绿山水", status: "warn" },
                { id: "nb-lesson-4-2", code: "4-2", title: "诗画合一", status: "draft" }
              ]
            },
            {
              id: "nb-unit-shoes",
              title: "第五单元 足下生辉",
              tone: "green",
              items: [
                { id: "nb-lesson-5-1", code: "5-1", title: "鞋的写生与设计", status: "draft" },
                { id: "nb-lesson-5-2", code: "5-2", title: "废旧材料创意做鞋", status: "draft" },
                { id: "nb-lesson-5-3", code: "5-3", title: "足下生辉作品完成", status: "draft" }
              ]
            },
            {
              id: "nb-unit-tiger",
              title: "第六单元 虎虎生威",
              tone: "amber",
              items: [
                { id: "nb-lesson-6-1", code: "6-1", title: "民间虎文化", status: "draft" },
                { id: "nb-lesson-6-2", code: "6-2", title: "布老虎制作", status: "draft" }
              ]
            },
            {
              id: "nb-unit-diary",
              title: "第七单元 成长日记",
              tone: "blue",
              items: [
                { id: "nb-lesson-7-1", code: "7-1", title: "序列画与视觉笔记本", status: "draft" },
                { id: "nb-lesson-7-2", code: "7-2", title: "成长记录", status: "draft" }
              ]
            },
            {
              id: "nb-unit-festival",
              title: "创艺节 足球梦",
              tone: "amber",
              items: [
                { id: "nb-lesson-f-1", code: "F-1", title: "走近足球文化", status: "draft" },
                { id: "nb-lesson-f-2", code: "F-2", title: "我的班级球衣", status: "draft" },
                { id: "nb-lesson-f-3", code: "F-3", title: "足球奖杯设计", status: "draft" },
                { id: "nb-lesson-f-4", code: "F-4", title: "加油海报与闭幕展", status: "draft" }
              ]
            }
          ],
          current_lesson: {
            code: "1-2",
            title: "色彩的感觉",
            unit: "第一单元 多变的色彩",
            status: "可上课 · 2项待确认",
            brief: "本课使用真实课题 1-2《色彩的感觉》。当前学生档案和课堂反馈尚未接入，学情先按三年级常见认知做预设，后续再由真实记录校准。",
            design_brief_summary: {
              problem: "学生知道颜色，也会说喜欢或不喜欢，但还需要把颜色和感受、场景、作品表达联系起来。",
              shift: "从看到颜色，到说出感受，再到有意识地用色彩表达心情或场景。",
              route: "生活感受 → 图片观察 → 色卡分类 → 分层小练习 → 作品说明",
              evidence: "看学生能否说出理由、能否在作品中用色表达、能否解释自己的选择。"
            },
            teacher_display_label_map: {
              cognitive_grounding: "本课方向",
              core_learning_problem: "学生卡点",
              target_shift: "从哪到哪",
              key_focus: "要紧的事",
              key_difficulty: "易卡住处",
              classroom_event: "课堂推进",
              execution_view: "课堂这样做",
              design_view: "为什么这样",
              student_response_model: "学生可能会",
              scaffold: "卡住怎么办",
              assessment_evidence: "怎么算学会",
              transition_to_next: "接下来"
            },
            reasoning_binding_1013F: {
              status: "R4推演 · 只读候选",
              judgment: "这节课的关键不是让学生记住冷暖色名称，而是帮助学生从“颜色好看”走向“能说出颜色带来的感受”。",
              learning_problem: "学生把冷暖色当成颜色名称或固定答案，缺少从视觉感受到理由表达的连接。",
              target_shift: "从能说颜色名称和喜欢不喜欢，到能根据温暖、清凉、安静、热烈等感受进行分类并说明理由。",
              route_summary: "先用生活图片唤起感受，再通过色卡分类帮助学生建立冷暖体验，最后把感受转化为自己的色彩表达。",
              time_arrangement: "40分钟：4 + 8 + 10 + 13 + 5。",
              next_lesson_connection: "下一课可以回看本课理由句，再进入更完整的色彩表达。",
              evidence_points: [
                "学生能把色卡或图片放入感受类别，并说出理由。",
                "学生能在学习单中写出颜色、感受和理由之间的关系。"
              ],
              events: [
                {
                  id: "EVT_1",
                  label: "唤起颜色经验",
                  minutes: "4分钟",
                  focus: "今天不急着分对错，先说颜色让你想到什么。",
                  question: "看到这个颜色，你身体里先出现什么感觉？",
                  task: "每人说一个颜色联想。",
                  evidence: "学生能说出至少一个感受词。",
                  change: "会说颜色名和喜好 → 知道今天要说颜色带来的感觉"
                },
                {
                  id: "EVT_2",
                  label: "对比观察",
                  minutes: "8分钟",
                  focus: "只看颜色，别先看画得像不像。",
                  question: "这两组颜色让你觉得哪里不一样？",
                  task: "同桌选一组图，说出冷/暖或其他感受。",
                  evidence: "同桌能说出一组颜色差异理由。",
                  change: "有感受词但分类不稳 → 能发现同一画面换色后感受会变"
                },
                {
                  id: "EVT_3",
                  label: "色卡分类探究",
                  minutes: "10分钟",
                  focus: "你们不是给颜色找标准答案，而是给感受找证据。",
                  question: "为什么这张色卡应该放在这里？",
                  task: "小组把色卡贴到感受词下，并准备一句理由。",
                  evidence: "色卡归类和理由表达。",
                  change: "能感受差异但理由松散 → 能把色卡放入感受类别并说明依据"
                },
                {
                  id: "EVT_4",
                  label: "表达小练习",
                  minutes: "13分钟",
                  focus: "选两三种颜色，画出一种你想表达的感觉。",
                  question: "你的颜色组合想让别人感到什么？",
                  task: "完成一格小画，并写一句理由。",
                  evidence: "颜色、感受、理由相连。",
                  change: "已能分类但还未表达个人感受 → 能用颜色组合表达一种心情或场景"
                },
                {
                  id: "EVT_5",
                  label: "分享证据",
                  minutes: "5分钟",
                  focus: "我们不评谁最好看，只听颜色和理由是否连得上。",
                  question: "他的颜色让你感受到他说的意思了吗？",
                  task: "两三位学生展示，小组补一句建议。",
                  evidence: "学生能用理由评价同伴作品。",
                  change: "完成小练习但还未校准表达 → 能听懂同伴理由并修正自己的表达"
                }
              ],
              active_event_id: "EVT_3",
              patch_candidate: {
                target_event_id: "EVT_3",
                target_label: "教学过程 · 色卡分类探究",
                summary: "建议改探究环节：加入色卡分类和理由表达，让学生把冷暖感受说清楚。",
                before: "原来只是让学生观察冷暖色，学生可能仍停留在“颜色好看”。",
                after: "学生先按“温暖、清凉、安静、热烈”等感受给色卡分类，再选择一张色卡说出理由。",
                why: "这样能把抽象的冷暖感受变成可操作的分类活动，也能留下学生是否理解的证据。",
                responses: [
                  ["可能回答", "能围绕色卡分类说出一个具体发现。", "追问依据，让学生把感受和材料连起来。", "用“我看到...所以觉得...”句式。"],
                  ["可能误解", "只说好看、漂亮或直接背答案。", "让学生指向画面或色卡中的具体部分。", "提供感受词卡和二选一比较。"],
                  ["沉默卡住", "学生看着材料但说不出来。", "先让同桌选词，再请学生补一个理由。", "给出“像太阳/像冰水/像晚上”的生活联想。"]
                ],
                impact_scope: [
                  ["大屏", "准备冷暖色对比图或黑板色块，并保留感受词。"],
                  ["学习单", "增加“我这样分类的理由”记录格，不做复杂表格。"],
                  ["评价证据", "评价时看学生是否能说出颜色与感受的关系。"],
                  ["教师引导", "教师追问分类依据，而不是直接判定对错。"],
                  ["学生活动", "学生从听讲改为动手分类、说明理由。"],
                  ["时间安排", "探究环节保留10分钟，展示人数不足时压缩交流。"],
                  ["下一课承接", "下一课可以回看本课理由句，再进入更完整的色彩表达。"]
                ],
                actions: ["采纳到本段", "继续精修", "追问原因", "暂不采用"]
              },
              candidate_error_message: "小教这次没有整理出可用候选，建议重新说一下你想调整的地方。"
            },
            status_cards: [
              ["正式课位", "8节", "done"],
              ["查看状态", "可阅读", "done"],
              ["编辑状态", "待开启", "warn"],
              ["本课材料", "可调用", "done"],
              ["分层任务", "待确认", "missing"]
            ],
            sections: [
              {
                id: "basis",
                title: "本课依据",
                status: "已确认",
                sources: ["教材", "课标", "正式课表"],
                body: [
                  "本课为第一单元《多变的色彩》中的 1-2《色彩的感觉》，不再使用临时拟题。",
                  "本课重点不是让学生背冷暖色概念，而是让学生把生活经验、作品观察和自己的色彩表达联系起来。"
                ]
              },
              {
                id: "analysis",
                title: "学情分析",
                status: "待真实记录校准",
                sources: ["教师经验", "课堂预设"],
                body: [
                  "三年级学生通常能说出自己喜欢的颜色，也能凭直觉说“明亮、暗、热闹、安静”等感受，但容易停留在“好看/不好看”的表层判断。",
                  "他们已经有生活色彩经验，但还需要借助图片、色卡、生活物品和作品范例，把颜色与情绪、场景、表达意图建立联系。",
                  "本版学情是预设，不冒充真实学生画像；等资料库、学生档案和课堂反馈接入后，再用真实班级差异修正。"
                ]
              },
              {
                id: "goals",
                title: "教学目标",
                status: "可上课",
                sources: ["课标", "本课学情"],
                body: [
                  "观察生活图片和美术作品，能说出不同色彩带来的冷暖、强弱、安静或热烈等感受。",
                  "能用一组色彩完成一个小练习，表达自己的心情、场景或故事，不只是在纸上涂满颜色。",
                  "能用一句话解释自己的色彩选择，并听懂同伴表达中的色彩感受。"
                ]
              },
              {
                id: "keypoints",
                title: "教学重难点",
                status: "待确认",
                sources: ["教材", "教师判断"],
                body: [
                  "重点：能感受色彩与情绪、场景之间的联系，并用语言表达自己的色彩体验。",
                  "难点：从“颜色好看”推进到“为什么这种颜色让我有这样的感觉”，并把这种感受用在自己的小练习中。"
                ]
              },
              {
                id: "preparation",
                title: "教学准备",
                status: "可调用",
                sources: ["资料室", "教师准备"],
                body: [
                  "教师准备：冷暖色生活图片、作品图、色卡或生活物品、情绪词卡、示范小稿、课堂计时和展示页面。",
                  "学生准备：绘画工具、色彩体验记录单。教材可在感知环节打开，不把看教材变成形式。"
                ]
              },
              {
                id: "assessment",
                title: "学习单与评价",
                status: "待确认",
                sources: ["学习单", "评价证据"],
                body: [
                  "学习单不做复杂表格，只保留三格：我看到的颜色、我感受到的情绪、我想表达的场景。",
                  "作业分层：基础层选择 2-3 种颜色表达一种感受；进阶层用冷暖或明暗对比表达一个场景；挑战层为作品加一句说明，解释色彩选择。",
                  "评价看三件事：能否说出色彩感受，能否把感受用于画面，能否用一句话解释自己的选择。"
                ]
              },
              {
                id: "reflection",
                title: "课后记录与沉淀",
                status: "待上课后补充",
                sources: ["档案室"],
                body: [
                  "课堂后记录学生是否能从“好看”转向“颜色带来的感受”，保留 2-3 件有代表性的作品和学生说明。",
                  "暂不进入正式沉淀；等教师确认后，再把作品证据、课堂观察和下次调整写入档案室。"
                ]
              }
            ],
            process_steps: [
              {
                id: "intro",
                name: "导入",
                time: "3分钟",
                summary: "播放两组色彩气氛差异明显的生活图片，让学生先说“看到这些颜色有什么感觉”。不急着讲概念，先把生活经验带进课堂。",
                tags: ["生活经验", "激活感受"],
                intent: {
                  role: "唤起经验，判断学生能否说出基本感受。",
                  design: "先让学生从熟悉场景进入，避免一开始就把课变成概念讲解。",
                  transition: "从生活感受进入作品观察，为后面的色彩比较铺垫。",
                  student: "多数学生能说出喜欢或不喜欢，但表达可能很笼统。",
                  teacher: "追问“你为什么会有这种感觉”，把回答从好看引向原因。",
                  activity: "学生观察图片，快速说出一个颜色和一个感受词。",
                  screen: "大屏展示两组图片和三个提示词：温暖、安静、热烈。",
                  material: "暂不发学习单，先让学生口头表达。",
                  evidence: "学生能否说出至少一个颜色带来的感受。",
                  risk: "如果学生只说好看，教师给出情绪词卡作支架。"
                }
              },
              {
                id: "sense",
                name: "感知",
                time: "7分钟",
                summary: "出示生活图片和作品范例，引导学生比较不同色彩给人的冷暖、明暗和情绪差异，建立“色彩会影响感受”的初步联系。",
                tags: ["作品观察", "建立联系"],
                intent: {
                  role: "建立色彩与感受之间的联系。",
                  design: "用作品和生活图并置，帮助学生看见色彩不是孤立知识，而是表达感受的方式。",
                  transition: "承接导入中的直觉感受，推进到有依据的比较。",
                  student: "学生可能能分辨颜色差异，但还需要学习怎样说理由。",
                  teacher: "示范一句表达：“这组橙黄色让我觉得温暖，因为像阳光。”",
                  activity: "学生两两比较图片，说出颜色和感受的对应关系。",
                  screen: "大屏显示图片对比、关键词和一句表达样例。",
                  material: "可打开教材范图，不要求学生长时间阅读文字。",
                  evidence: "学生能否用“颜色 + 感受 + 原因”说一句话。",
                  risk: "如果比较太抽象，教师减少图片数量，只保留一冷一暖两组。"
                }
              },
              {
                id: "explore",
                name: "探究",
                time: "10分钟",
                summary: "学生分组观察色卡和生活物品，尝试把颜色分成“温暖、清凉、安静、热烈”等感受类型，并说出理由。",
                tags: ["分组判断", "说出理由"],
                intent: {
                  role: "让学生把感受判断从看图迁移到自己分类和说明理由。",
                  design: "用色卡和实物降低理解门槛，让学生先动手分类，再用语言解释。",
                  transition: "承接感知环节的观察比较，推进到学生主动判断。",
                  student: "学生可能会按颜色名称分类，而不是按感受分类，需要教师追问。",
                  teacher: "巡视时追问“你把它放在这里，是因为它像什么，还是让你想到什么？”",
                  activity: "小组把色卡放到感受词旁边，并选择一张说理由。",
                  screen: "大屏显示分组任务、感受词和倒计时。",
                  material: "发放色卡和一张简短记录单。",
                  evidence: "学生能否说明分类理由，而不是只报颜色名称。",
                  risk: "如果分类混乱，教师先给一组示范，再让学生继续选择。"
                },
                candidate: "可加入“冷暖色物品分组”活动，让学生先分类再说理由；学习单增加“我的色彩感受”记录格。"
              },
              {
                id: "make",
                name: "表现",
                time: "15分钟",
                summary: "学生围绕“我心中的一种感受”进行色彩小练习，自选基础、进阶或挑战任务，用颜色表达一种心情、天气、场景或小故事。",
                tags: ["分层任务", "创作表达"],
                intent: {
                  role: "把理解转化为个人表达，让不同层次学生都有够得着的任务。",
                  design: "用分层选择避免作业太无聊或太难，给学生一点挑战但不超出认知。",
                  transition: "承接探究环节的分类理由，进入个人色彩表达。",
                  student: "基础层学生需要明确起步方式，能力强的学生需要更开放的表达空间。",
                  teacher: "先说明三层任务，再巡视提醒学生让颜色服务于感受。",
                  activity: "学生选择一层任务完成小练习，并准备一句说明。",
                  screen: "大屏显示三层任务、时间提醒和示范小稿。",
                  material: "使用绘画纸、色彩工具和学习单说明格。",
                  evidence: "作品是否能看出情绪或场景，学生能否解释选择。",
                  risk: "如果学生只追求涂满，教师提醒先确定一种感受再选色。"
                }
              },
              {
                id: "share",
                name: "交流展示",
                time: "5分钟",
                summary: "选择几件作品展示，学生用一句话说明自己的色彩选择，同伴说出自己读到的感受，教师归纳色彩和情绪表达的关系。",
                tags: ["表达说明", "同伴倾听"],
                intent: {
                  role: "把个人作品转化为可表达、可倾听、可评价的学习证据。",
                  design: "通过说和听，帮助学生确认色彩表达是否被同伴理解。",
                  transition: "承接表现环节的作品产出，回到本课目标的达成判断。",
                  student: "有些学生能画但说不清，需要一句话模板支撑。",
                  teacher: "引导学生用“我用了____色，因为我想表达____”说明。",
                  activity: "学生展示作品，同伴说感受到的情绪或场景。",
                  screen: "大屏展示作品照片和一句话说明模板。",
                  material: "学习单最后一格记录作品说明。",
                  evidence: "学生作品、说明句和同伴反馈构成本课主要证据。",
                  risk: "如果时间不够，保留两件典型作品，课后再补记录。"
                }
              }
            ],
            edit_context: {
              title: "教学过程 · 探究环节",
              judgment: "学生可能还停在“这个颜色好看”的描述，需要先通过色卡和生活物品分类，把感受变得看得见、说得出。",
              gap: "探究环节需要更直观；学习单需要有一个记录格承接分类理由。",
              related: ["色彩情感卡片", "冷暖色图片对比", "优秀课例《色彩的感觉》"],
              impacts: ["学习单增加“我看到的颜色 / 我感受到的情绪”记录格", "大屏准备冷暖色对比图和感受词卡", "评价证据记录学生能否说出分类理由"],
              candidate: "把探究环节改为“色卡和生活物品分组”：学生先按感受分类，再选择一张色卡说理由。",
              actions: ["并入本段", "替换本段", "再简化", "再具体一点", "补学习单", "补大屏呈现", "先放着"]
            },
            flow: ["正式课位", "备课本加工", "教师确认", "课堂执行记录", "档案室沉淀"]
          },
          right_panels: {
            view: [
              {
                title: "本课材料",
                tag: "资料室",
                items: ["教材原文片段", "冷暖色生活图片", "色彩情感卡片", "优秀课例《色彩的感觉》"]
              },
              {
                title: "可调用资料",
                tag: "按需打开",
                items: ["第一单元《多变的色彩》课标摘要", "课堂大屏图片组", "情绪词卡", "三层任务示例"]
              },
              {
                title: "待确认",
                tag: "2项",
                items: ["分层作业是否按基础/进阶/挑战三层呈现", "探究环节是否发学习单记录分类理由"]
              },
              {
                title: "待沉淀",
                tag: "档案室",
                items: ["学生作品照片", "学生一句话说明", "教师课后轻记录"]
              }
            ],
            edit: [
              {
                title: "当前编辑",
                tag: "探究环节",
                items: ["教学过程 · 探究环节", "目标：让学生把颜色感受说清楚，而不是只说好看。"]
              },
              {
                title: "小教判断",
                tag: "候选",
                items: ["探究环节需要更直观。", "色卡分组能把抽象感受变成可操作活动。", "这个改动会带动学习单和大屏一起调整。"]
              },
              {
                title: "影响范围",
                tag: "3处",
                items: ["学习单增加感受记录格", "大屏增加冷暖色对比图", "评价时记录学生说明理由"]
              },
              {
                title: "候选确认",
                tag: "待处理",
                items: ["并入探究环节", "补一页大屏提示", "学习单增加一格，不做复杂表格"]
              }
            ]
          }
        },
        {
          id: "classProgressSchedule",
          label: "班级排课",
          title: "班级进度与排课",
          kicker: "Class Progress Schedule Board",
          summary: "按授课年级查看各班真实课时落点。横向对比班级，纵向追踪周次，每周默认两个课时槽。",
          weekly_period_capacity: 2,
          grade_options: [
            { id: "g3", label: "三年级" },
            { id: "g4", label: "四年级" },
            { id: "g5", label: "五年级" },
            { id: "g6", label: "六年级" }
          ],
          active_grade: "g3",
          metrics: [
            { label: "授课班级", value: "5" },
            { label: "进度一致", value: "3" },
            { label: "待调整课时", value: "4" },
            { label: "当前周", value: "第10周" }
          ],
          class_headers: [
            { id: "c1", label: "三1班", current: "4-1", state: "normal" },
            { id: "c2", label: "三2班", current: "4-1", state: "normal" },
            { id: "c3", label: "三3班", current: "F-4", state: "behind" },
            { id: "c4", label: "三4班", current: "4-1", state: "rescheduled" },
            { id: "c5", label: "三5班", current: "4-2", state: "normal" }
          ],
          lesson_catalog: [
            {
              id: "unit-color",
              title: "单元1 多变的色彩",
              hours: "共3课时",
              tone: "green",
              lessons: [["1-1", "渐变的魅力"], ["1-2", "色彩的感觉"], ["1-3", "渐变的节奏"]]
            },
            {
              id: "unit-shape",
              title: "单元2 辽阔的海洋",
              hours: "共3课时",
              tone: "blue",
              lessons: [["2-1", "奇异的海洋生物"], ["2-2", "跳动的蓝色心脏"], ["2-3", "守护生命的摇篮"]]
            },
            {
              id: "unit-red",
              title: "单元3 红领巾告诉我",
              hours: "共2课时",
              tone: "red",
              lessons: [["3-1", "影像创作"], ["3-2", "红色精神传承"]]
            },
            {
              id: "unit-qinglv",
              title: "单元4 青绿中国色",
              hours: "共2课时",
              tone: "amber",
              lessons: [["4-1", "矿物颜料与青绿山水"], ["4-2", "诗画合一"]]
            },
            {
              id: "unit-shoes",
              title: "单元5 足下生辉",
              hours: "共3课时",
              tone: "green",
              lessons: [["5-1", "鞋的写生与设计"], ["5-2", "废旧材料创意做鞋"], ["5-3", "足下生辉作品完成"]]
            },
            {
              id: "unit-festival",
              title: "创艺节 足球梦",
              hours: "共4课时",
              tone: "amber",
              lessons: [["F-1", "走近足球文化"], ["F-2", "我的班级球衣"], ["F-3", "足球奖杯设计"], ["F-4", "加油海报与闭幕展"]]
            }
          ],
          week_axis: [
            { id: "w07", label: "第7周", date: "4.14 - 4.18", state: "past" },
            { id: "w08", label: "第8周", date: "4.21 - 4.25", state: "past" },
            { id: "w09", label: "第9周", date: "4.28 - 5.02", state: "past" },
            { id: "w10", label: "第10周", date: "5.05 - 5.09", state: "current" },
            { id: "w11", label: "第11周", date: "5.11 - 5.15", state: "future" },
            { id: "w12", label: "第12周", date: "5.18 - 5.22", state: "future" },
            { id: "w13", label: "第13周", date: "5.25 - 5.29", state: "future" }
          ],
          class_week_cells: {
            "w07-c1": [["lesson", "3-1", "影像创作"], ["lesson", "3-2", "红色精神传承"]],
            "w07-c2": [["lesson", "3-1", "影像创作"], ["lesson", "3-2", "红色精神传承"]],
            "w07-c3": [["lesson", "3-1", "影像创作"], ["lesson", "3-2", "红色精神传承"]],
            "w07-c4": [["lesson", "3-1", "影像创作"], ["lesson", "3-2", "红色精神传承"]],
            "w07-c5": [["lesson", "3-1", "影像创作"], ["lesson", "3-2", "红色精神传承"]],
            "w08-c1": [["lesson", "F-1", "走近足球文化"], ["lesson", "F-2", "我的班级球衣"]],
            "w08-c2": [["lesson", "F-1", "走近足球文化"], ["lesson", "F-2", "我的班级球衣"]],
            "w08-c3": [["activity", "", "足球联赛占用"], ["lesson", "F-1", "走近足球文化"]],
            "w08-c4": [["lesson", "F-1", "走近足球文化"], ["lesson", "F-2", "我的班级球衣"]],
            "w08-c5": [["lesson", "F-1", "走近足球文化"], ["lesson", "F-2", "我的班级球衣"]],
            "w09-c1": [["lesson", "F-3", "足球奖杯设计"], ["lesson", "F-4", "加油海报与闭幕展"]],
            "w09-c2": [["holiday", "", "五一停课"], ["holiday", "", "自动顺延"]],
            "w09-c3": [["lesson", "F-2", "我的班级球衣"], ["lesson", "F-3", "足球奖杯设计"]],
            "w09-c4": [["holiday", "", "五一停课"], ["holiday", "", "自动顺延"]],
            "w09-c5": [["lesson", "F-3", "足球奖杯设计"], ["lesson", "F-4", "加油海报与闭幕展"]],
            "w10-c1": [["lesson", "4-1", "矿物颜料与青绿山水"], ["lesson", "4-2", "诗画合一"]],
            "w10-c2": [["lesson", "4-1", "矿物颜料与青绿山水"], ["reschedule", "", "调课至周五"]],
            "w10-c3": [["makeup", "", "补完创艺节闭幕展"], ["lesson", "4-1", "矿物颜料与青绿山水"]],
            "w10-c4": [["lesson", "4-1", "矿物颜料与青绿山水"], ["lesson", "4-2", "诗画合一"]],
            "w10-c5": [["lesson", "4-1", "矿物颜料与青绿山水"], ["lesson", "4-2", "诗画合一"]],
            "w11-c1": [["future", "4-1", "青绿中国色复看"], ["future", "4-2", "诗画合一"]],
            "w11-c2": [["future", "4-1", "矿物颜料与青绿山水"], ["future", "4-2", "诗画合一"]],
            "w11-c3": [["future", "4-1", "矿物颜料与青绿山水"], ["future", "4-2", "诗画合一"]],
            "w11-c4": [["future", "4-1", "矿物颜料与青绿山水"], ["future", "4-2", "诗画合一"]],
            "w11-c5": [["future", "4-1", "矿物颜料与青绿山水"], ["future", "4-2", "诗画合一"]],
            "w12-c1": [["future", "5-1", "鞋的写生与设计"], ["future", "5-2", "废旧材料创意做鞋"]],
            "w12-c2": [["future", "5-1", "鞋的写生与设计"], ["future", "5-2", "废旧材料创意做鞋"]],
            "w12-c3": [["future", "5-1", "鞋的写生与设计"], ["future", "5-2", "废旧材料创意做鞋"]],
            "w12-c4": [["future", "5-1", "鞋的写生与设计"], ["future", "5-2", "废旧材料创意做鞋"]],
            "w12-c5": [["future", "5-1", "鞋的写生与设计"], ["future", "5-2", "废旧材料创意做鞋"]],
            "w13-c1": [["future", "5-2", "废旧材料创意做鞋"], ["future", "5-3", "足下生辉作品完成"]],
            "w13-c2": [["future", "5-2", "废旧材料创意做鞋"], ["future", "5-3", "足下生辉作品完成"]],
            "w13-c3": [["future", "5-2", "废旧材料创意做鞋"], ["future", "5-3", "足下生辉作品完成"]],
            "w13-c4": [["future", "5-2", "废旧材料创意做鞋"], ["future", "5-3", "足下生辉作品完成"]],
            "w13-c5": [["future", "5-2", "废旧材料创意做鞋"], ["future", "5-3", "足下生辉作品完成"]]
          },
          suggestions: [
            { tone: "warn", text: "第8-9周创艺节与五一假期会影响部分班级节奏，当前仅做静态预演。" },
            { tone: "info", text: "第10-11周进入第四单元《青绿中国色》，建议先确认两课时拆分。" },
            { tone: "warn", text: "三3班第10周仍有创艺节补完任务，接入真实课表后再判断是否顺延。" },
            { tone: "normal", text: "下周优先准备《矿物颜料与青绿山水》学习单、《诗画合一》观察卡。" }
          ]
        },
        {
          id: "flexibleSemesterMap",
          label: "学期规划",
          title: "学期规划",
          kicker: "Semester Plan",
          summary: "把单元课时目录和周次计划放在同一张规划表中，便于教师按周查看、调整和确认。",
          metrics: [
            { label: "教材单元", value: "7" },
            { label: "教材课时", value: "19" },
            { label: "创艺节", value: "4" },
            { label: "机动复习", value: "6" },
            { label: "周次", value: "16" }
          ],
          lanes: [
            {
              id: "lane-units",
              title: "教材学习",
              note: "来源于 2025 学年第二学期三年级美术教学工作计划，共 7 个单元、19 课时。",
              blocks: [
                {
                  id: "teaching-block-color",
                  title: "第一单元 多变的色彩",
                  state: "3课时",
                  weeks: "第2-3周",
                  detail: "渐变的魅力、色彩的感觉、渐变的节奏。",
                  actions: ["查看课时", "进入备课本"]
                },
                {
                  id: "teaching-block-shape",
                  title: "第二单元 辽阔的海洋",
                  state: "3课时",
                  weeks: "第3-6周",
                  detail: "奇异的海洋生物、跳动的蓝色心脏、守护生命的摇篮。",
                  actions: ["查看课时", "进入备课本"]
                },
                {
                  id: "teaching-block-red",
                  title: "第三单元 红领巾告诉我",
                  state: "2课时",
                  weeks: "第7周",
                  detail: "影像创作与红色精神传承，重点使用景别表达。",
                  actions: ["查看课时", "进入备课本"]
                },
                {
                  id: "teaching-block-qinglv",
                  title: "第四单元 青绿中国色",
                  state: "2课时",
                  weeks: "第10-11周",
                  detail: "矿物颜料、青绿山水、诗画合一。",
                  actions: ["拆成课时", "进入备课本"]
                },
                {
                  id: "teaching-block-shoes",
                  title: "第五单元 足下生辉",
                  state: "3课时",
                  weeks: "第12-13周",
                  detail: "鞋的写生与设计、废旧材料创意做鞋。",
                  actions: ["查看课时", "进入备课本"]
                },
                {
                  id: "teaching-block-tiger",
                  title: "第六单元 虎虎生威",
                  state: "2课时",
                  weeks: "第14周",
                  detail: "民间虎文化、布老虎制作。",
                  actions: ["查看课时", "进入备课本"]
                },
                {
                  id: "teaching-block-diary",
                  title: "第七单元 成长日记",
                  state: "2课时",
                  weeks: "第15周",
                  detail: "序列画、视觉笔记本、成长记录。",
                  actions: ["查看课时", "进入备课本"]
                }
              ]
            },
            {
              id: "lane-events",
              title: "创艺节与校历",
              note: "创艺节是独立课程板块，不挤占教材单元；节假日只作为扰动进入预演。",
              blocks: [
                {
                  id: "event-football-week-8",
                  title: "创艺节·足球梦 上",
                  state: "2课时",
                  weeks: "第8周",
                  detail: "走近足球文化、我的班级球衣。",
                  actions: ["查看活动", "进入备课本"]
                },
                {
                  id: "event-football-week-9",
                  title: "创艺节·足球梦 下",
                  state: "2课时",
                  weeks: "第9周",
                  detail: "足球奖杯设计、加油海报与闭幕展。",
                  actions: ["查看活动", "进入备课本"]
                },
                {
                  id: "event-qingming",
                  title: "清明假期",
                  state: "扰动",
                  weeks: "第5周",
                  detail: "4/4-4/6 清明假期，影响需由班级课表确认。",
                  actions: ["查看影响", "暂存"]
                },
                {
                  id: "event-mayday",
                  title: "五一假期",
                  state: "扰动",
                  weeks: "第9-10周",
                  detail: "5/1-5/5 五一假期与第10周收尾相邻。",
                  actions: ["查看影响", "暂存"]
                }
              ]
            },
            {
              id: "lane-buffer",
              title: "机动复习",
              note: "教学工作计划预留 6 课时，服务补完、复习、总结和考试周。",
              blocks: [
                {
                  id: "buffer-final",
                  title: "机动 / 复习 / 总结",
                  state: "2课时",
                  weeks: "第16周",
                  detail: "考试周，承接作品补完、学习证据整理和学期总结。",
                  actions: ["生成清单", "进入档案室"]
                },
                {
                  id: "buffer-reserve",
                  title: "机动课时池",
                  state: "6课时",
                  weeks: "全学期",
                  detail: "只作为缓冲，不自动替换正式单元课。",
                  actions: ["查看规则", "保留"]
                }
              ]
            }
          ],
          suggestions: [
            "第8-9周创艺节作为独立板块处理，不要并入教材单元。",
            "第10-11周进入《青绿中国色》，先确认 2 课时拆分，再写入备课本。",
            "第16周机动/复习/总结用于作品补完、学习证据整理和档案室沉淀。"
          ],
          plan_units: [
            {
              id: "plan-unit-color",
              title: "单元1 多变的色彩",
              hours: "共3课时",
              tone: "green",
              lessons: [
                ["1-1", "渐变的魅力"],
                ["1-2", "色彩的感觉"],
                ["1-3", "渐变的节奏"]
              ]
            },
            {
              id: "plan-unit-shape",
              title: "单元2 辽阔的海洋",
              hours: "共3课时",
              tone: "blue",
              lessons: [
                ["2-1", "奇异的海洋生物"],
                ["2-2", "跳动的蓝色心脏"],
                ["2-3", "守护生命的摇篮"]
              ]
            },
            {
              id: "plan-unit-red",
              title: "单元3 红领巾告诉我",
              hours: "共2课时",
              tone: "red",
              lessons: [
                ["3-1", "影像创作"],
                ["3-2", "红色精神传承"]
              ]
            },
            {
              id: "plan-unit-qinglv",
              title: "单元4 青绿中国色",
              hours: "共2课时",
              tone: "amber",
              lessons: [
                ["4-1", "矿物颜料与青绿山水"],
                ["4-2", "诗画合一"]
              ]
            },
            {
              id: "plan-unit-shoes",
              title: "单元5 足下生辉",
              hours: "共3课时",
              tone: "green",
              lessons: [
                ["5-1", "鞋的写生与设计"],
                ["5-2", "废旧材料创意做鞋"],
                ["5-3", "足下生辉作品完成"]
              ]
            },
            {
              id: "plan-unit-tiger",
              title: "单元6 虎虎生威",
              hours: "共2课时",
              tone: "amber",
              lessons: [
                ["6-1", "民间虎文化"],
                ["6-2", "布老虎制作"]
              ]
            },
            {
              id: "plan-unit-diary",
              title: "单元7 成长日记",
              hours: "共2课时",
              tone: "blue",
              lessons: [
                ["7-1", "序列画与视觉笔记本"],
                ["7-2", "成长记录"]
              ]
            },
            {
              id: "plan-unit-festival",
              title: "创艺节 足球梦",
              hours: "共4课时",
              tone: "amber",
              lessons: [
                ["F-1", "走近足球文化"],
                ["F-2", "我的班级球衣"],
                ["F-3", "足球奖杯设计"],
                ["F-4", "加油海报与闭幕展"]
              ]
            }
          ],
          plan_weeks: [
            { id: "plan-week-1", week: "第1周", date: "03.05", lessons: [["start-1", "开学第一课：美术世界，我来了！", "buffer"]] },
            { id: "plan-week-2", week: "第2周", date: "03.10 - 03.14", lessons: [["1-1", "渐变的魅力", "green"], ["1-2", "色彩的感觉", "green"]] },
            { id: "plan-week-3", week: "第3周", date: "03.17 - 03.21", lessons: [["1-3", "渐变的节奏", "green"], ["2-1", "奇异的海洋生物", "blue"]] },
            { id: "plan-week-4", week: "第4周", date: "03.24 - 03.28", lessons: [["2-2", "跳动的蓝色心脏", "blue"], ["2-3", "守护生命的摇篮", "blue"]] },
            { id: "plan-week-5", week: "第5周", date: "03.31 - 04.04", lessons: [["2-2", "辽阔的海洋延展", "blue"], ["event-qingming", "清明假期 4/4-4/6", "buffer"]] },
            { id: "plan-week-6", week: "第6周", date: "04.07 - 04.11", lessons: [["2-3", "辽阔的海洋整理", "blue"], ["league-6", "足球联赛月", "buffer"]] },
            { id: "plan-week-7", week: "第7周", date: "04.14 - 04.18", lessons: [["3-1", "影像创作", "red"], ["3-2", "红色精神传承", "red"]] },
            { id: "plan-week-8", week: "第8周", date: "04.21 - 04.25", lessons: [["F-1", "走近足球文化", "amber"], ["F-2", "我的班级球衣", "amber"]] },
            { id: "plan-week-9", week: "第9周", date: "04.28 - 05.02", lessons: [["F-3", "足球奖杯设计", "amber"], ["F-4", "加油海报与闭幕展", "amber"], ["event-mayday", "五一 5/1-5/5", "buffer"]] },
            { id: "plan-week-10", week: "第10周", date: "05.05 - 05.09", lessons: [["4-1", "矿物颜料与青绿山水", "amber"], ["4-2", "诗画合一", "amber"]] },
            { id: "plan-week-11", week: "第11周", date: "05.11 - 05.15", lessons: [["4-1b", "青绿中国色巩固", "amber"], ["4-2b", "诗画合一作品整理", "amber"]] },
            { id: "plan-week-12", week: "第12周", date: "05.18 - 05.22", lessons: [["5-1", "鞋的写生与设计", "green"], ["5-2", "废旧材料创意做鞋", "green"]] },
            { id: "plan-week-13", week: "第13周", date: "05.25 - 05.29", lessons: [["5-2b", "废旧材料创意做鞋", "green"], ["5-3", "足下生辉作品完成", "green"]] },
            { id: "plan-week-14", week: "第14周", date: "06.01 - 06.05", lessons: [["6-1", "民间虎文化", "amber"], ["6-2", "布老虎制作", "amber"]] },
            { id: "plan-week-15", week: "第15周", date: "06.09 - 06.13", lessons: [["7-1", "序列画与视觉笔记本", "blue"], ["7-2", "成长记录", "blue"]] },
            { id: "plan-week-16", week: "第16周", date: "06.16 - 06.21", lessons: [["buffer-final", "机动 / 复习 / 总结", "buffer"], ["exam-week", "考试周", "buffer"]] }
          ]
        }
      ],
      node_details: {
        "teaching-block-qinglv": {
          type: "学期地图节点",
          title: "编辑教学块：第四单元 青绿中国色",
          fields: [
            ["建议周次", "第10-11周"],
            ["当前安排", "第10-11周"],
            ["计划课时", "2课时"],
            ["来源", "2025学年第二学期三年级美术教学工作计划"],
            ["当前风险", "课时标题和材料清单待教师确认"]
          ],
          actions: ["确认拆课", "进入备课本", "生成课前包"]
        }
      },
      tools: [
        { id: "textbook", icon: "目", title: "教材解析", desc: "解析教材，建立学期结构，辅助单元重组。", actions: ["解析目录", "关联单元"] },
        { id: "unit", icon: "元", title: "单元重组", desc: "将教材内容重组成教学单元块，规划课包产出。", actions: ["重组青绿中国色", "重组辽阔的海洋"] },
        { id: "split", icon: "拆", title: "拆课", desc: "将单元拆分为课时草案和课包框架。", actions: ["拆分教学工作计划", "拆分创艺节课程"] },
        { id: "weekly", icon: "周", title: "周课表", desc: "查看本周每天每节课的班级、课题与课前包状态。", actions: ["生成周课表", "查看课前准备"] },
        { id: "reschedule", icon: "排", title: "重排工具", desc: "检查学校临时任务对学期计划的影响，生成重排方案。", actions: ["检查扰动", "生成重排方案", "查看影响范围"] },
        { id: "flow", icon: "流", title: "课堂流程", desc: "生成课时流程结构，纳入备课包。", actions: ["生成流程", "调整环节"] },
        { id: "worksheet", icon: "单", title: "学习单", desc: "基于课包生成学习单初稿，可交给小美。", actions: ["生成学习单", "交给小美优化"] },
        { id: "search", icon: "检", title: "知识库检索", desc: "查找资料、案例，完善课包。", actions: ["检索《千里江山图》", "查找青绿山水"] },
        { id: "xiaomei", icon: "美", title: "交给小美", desc: "将课包素材交小美做视觉设计。", actions: ["生成学习单背景", "生成PPT封面"] },
        { id: "xiaoping", icon: "评", title: "调用小评", desc: "把课包目标转成评价维度和课堂观察项。", actions: ["生成量规", "预设互评表"] },
        { id: "xiaoguan", icon: "管", title: "调用小管", desc: "预设作品归档字段和课后回流结构。", actions: ["生成归档字段", "检查数据回流"] }
      ],
      pending_changes: [
        {
          id: "pending-001",
        text: "小教已生成1个课前处理建议，等待教师确认。",
          source: "初始预演",
          applied: false
        }
      ]
    };

    const model = window.PREP_ROOM_RENDER_VIEW_MODEL;
    const byId = (id) => document.getElementById(id);
    const html = (value) => String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");

    const icons = {
      home: '<path d="M3 11.5 12 4l9 7.5"></path><path d="M5.5 10.5V20h13v-9.5"></path><path d="M9.5 20v-6h5v6"></path>',
      classroom: '<path d="M4 5h16v11H4z"></path><path d="M8 20h8"></path><path d="M12 16v4"></path>',
      prep: '<path d="M8 4h8"></path><path d="M7 8h10"></path><path d="M6 12h12"></path><path d="M8 16h8"></path><path d="M5 20h14"></path>',
      eye: '<path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6z"></path><circle cx="12" cy="12" r="2.5"></circle>',
      gallery: '<path d="M4 5h16v14H4z"></path><path d="m4 15 4-4 3 3 3-4 6 6"></path><circle cx="8.5" cy="8.5" r="1.5"></circle>',
      knowledge: '<path d="M5 4h10a4 4 0 0 1 4 4v12H8a3 3 0 0 1-3-3z"></path><path d="M8 4v13"></path>',
      archive: '<path d="M4 5h16v4H4z"></path><path d="M6 9v10h12V9"></path><path d="M10 13h4"></path>',
      layers: '<path d="m12 3 9 5-9 5-9-5z"></path><path d="m3 12 9 5 9-5"></path><path d="m3 16 9 5 9-5"></path>',
      flow: '<path d="M6 4v6"></path><path d="M6 14v6"></path><path d="M18 4v6"></path><path d="M18 14v6"></path><path d="M6 10h12"></path><path d="M12 10v4"></path><path d="m9 14 3 3 3-3"></path>',
      worksheet: '<path d="M7 3h10l2 2v16H5V5z"></path><path d="M9 9h6"></path><path d="M9 13h6"></path><path d="M9 17h4"></path>',
      palette: '<path d="M12 4a8 8 0 0 0 0 16h1.5a2 2 0 0 0 1.2-3.6 1.6 1.6 0 0 1 1-2.9H17a5 5 0 0 0 0-10z"></path><circle cx="8.5" cy="10" r=".8"></circle><circle cx="11" cy="7.5" r=".8"></circle><circle cx="14" cy="10" r=".8"></circle>',
      search: '<circle cx="11" cy="11" r="6"></circle><path d="m16 16 4 4"></path>',
      bell: '<path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"></path><path d="M10 20a2 2 0 0 0 4 0"></path>',
      user: '<circle cx="12" cy="8" r="4"></circle><path d="M4 21a8 8 0 0 1 16 0"></path>',
      classes: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path>',
      clock: '<circle cx="12" cy="12" r="9"></circle><path d="M12 7v5l3 2"></path>',
      upload: '<path d="M12 4v12"></path><path d="m7 9 5-5 5 5"></path><path d="M5 20h14"></path>',
      mic: '<path d="M12 4a3 3 0 0 0-3 3v5a3 3 0 0 0 6 0V7a3 3 0 0 0-3-3z"></path><path d="M5 11a7 7 0 0 0 14 0"></path><path d="M12 18v3"></path>',
      send: '<path d="m3 11 18-8-8 18-2-7z"></path><path d="m11 14 10-11"></path>',
      check: '<path d="M20 6 9 17l-5-5"></path>',
      monitor: '<path d="M4 5h16v11H4z"></path><path d="M8 20h8"></path><path d="M12 16v4"></path>',
      refresh: '<path d="M20 12a8 8 0 0 1-14 5"></path><path d="M4 12a8 8 0 0 1 14-5"></path><path d="M18 3v4h-4"></path><path d="M6 21v-4h4"></path>',
      scissors: '<circle cx="6" cy="7" r="3"></circle><circle cx="6" cy="17" r="3"></circle><path d="m9 9 11 8"></path><path d="m20 7-11 8"></path>',
      star: '<path d="m12 3 2.7 5.5 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.8 1-6.1-4.4-4.3 6.1-.9z"></path>',
      file: '<path d="M6 3h8l4 4v14H6z"></path><path d="M14 3v5h5"></path><path d="M9 13h6"></path><path d="M9 17h4"></path>',
      wand: '<path d="m4 20 12-12"></path><path d="m14 6 4 4"></path><path d="M6 4v3"></path><path d="M4.5 5.5h3"></path><path d="M19 15v3"></path><path d="M17.5 16.5h3"></path>',
      calendar: '<path d="M5 4h14v16H5z"></path><path d="M8 2v4"></path><path d="M16 2v4"></path><path d="M5 9h14"></path>',
      map: '<path d="m4 6 5-2 6 2 5-2v14l-5 2-6-2-5 2z"></path><path d="M9 4v14"></path><path d="M15 6v14"></path>',
      plus: '<path d="M12 5v14"></path><path d="M5 12h14"></path>',
      arrow: '<path d="M5 12h14"></path><path d="m13 6 6 6-6 6"></path>'
    };

    function icon(name, size = "") {
      const body = icons[name] || icons.arrow;
      return `<svg class="icon ${size}" viewBox="0 0 24 24" aria-hidden="true">${body}</svg>`;
    }

    function sr(text) {
      return `<span class="sr-only">${html(text)}</span>`;
    }

    function iconButtonLabel(text, iconName, iconOnly = true) {
      return `${icon(iconName)}${iconOnly ? sr(text) : `<span>${html(text)}</span>`}`;
    }

    function iconForAction(action) {
      const text = String(action || "");
      if (/送入|预览|大屏|课堂/.test(text)) return "monitor";
      if (/完善|补齐|检查|确认|完成/.test(text)) return "check";
      if (/重排|重组|调整|更新/.test(text)) return "refresh";
      if (/拆|压缩/.test(text)) return "scissors";
      if (/评价|量规|互评|小评/.test(text)) return "star";
      if (/资料|材料|查看|检索|学习单/.test(text)) return "file";
      if (/生成|预置|方案|小美/.test(text)) return "wand";
      return "arrow";
    }

    function iconForView(viewId) {
      if (viewId === "weekCalendar") return "calendar";
      if (viewId === "prepNotebook") return "worksheet";
      if (viewId === "classProgressSchedule") return "layers";
      if (viewId === "flexibleSemesterMap") return "map";
      return "prep";
    }

    function iconForTool(toolId) {
      const map = {
        textbook: "knowledge",
        unit: "layers",
        split: "scissors",
        weekly: "calendar",
        reschedule: "refresh",
        flow: "flow",
        worksheet: "worksheet",
        search: "search",
        xiaomei: "palette",
        xiaoping: "star",
        xiaoguan: "archive"
      };
      return map[toolId] || "wand";
    }

    function hydrateShellIcons() {
      const spaceIcons = {
        "大厅": "home",
        "教室": "classroom",
        "备课室": "prep",
        "课堂观察": "eye",
        "作品馆": "gallery",
        "知识馆": "knowledge",
        "档案室": "archive"
      };
      document.querySelectorAll(".space-btn").forEach((button) => {
        const label = button.getAttribute("aria-label") || "";
        button.title = label;
        button.innerHTML = iconButtonLabel(label, spaceIcons[label] || "home");
      });

      const searchIcon = document.querySelector(".search-box span");
      if (searchIcon) searchIcon.outerHTML = icon("search", "sm");

      const notification = document.querySelector(".nav-icon");
      if (notification) {
        notification.title = "通知";
        notification.innerHTML = `${iconButtonLabel("通知", "bell")}<span class="nav-badge">2</span>`;
      }

      const avatar = document.querySelector(".user-avatar");
      if (avatar) {
        avatar.title = "教师账号";
        avatar.innerHTML = iconButtonLabel("教师账号", "user");
      }

      const upload = byId("chatUploadBtn");
      if (upload) {
        upload.title = "上传资料";
        upload.innerHTML = iconButtonLabel("上传资料", "upload");
      }

      const voice = byId("chatVoiceBtn");
      if (voice) {
        voice.title = "语音输入";
        voice.innerHTML = iconButtonLabel("语音输入", "mic");
      }

      const send = byId("chatSendBtn");
      if (send) {
        send.title = "发送";
        send.setAttribute("aria-label", "发送");
        send.innerHTML = iconButtonLabel("发送", "send");
      }
    }

    function getActiveView() {
      return model.views.find((view) => view.id === model.active_view) || model.views[0];
    }

    function applyInitialViewFromHash() {
      const viewId = decodeURIComponent((window.location.hash || "").replace(/^#/, ""));
      if (!viewId) return;
      const prepView = model.views.find((view) => view.id === "prepNotebook");
      if (viewId === "prepNotebookEdit" && prepView) {
        model.active_view = "prepNotebook";
        prepView.prep_notebook_mode = "edit";
        prepView.expanded_intent_steps = ["explore"];
        prepView.active_edit_target = { section_id: "teaching_process", step_id: "explore", label: "教学过程 · 探究环节" };
      } else if (viewId === "prepNotebook1013F" && prepView) {
        model.active_view = "prepNotebook";
        prepView.prep_notebook_mode = "view";
        prepView.expanded_intent_steps = [];
        model.initial_scroll_target = "nb-1013f-binding";
      } else if (viewId === "prepNotebook1013FEdit" && prepView) {
        model.active_view = "prepNotebook";
        prepView.prep_notebook_mode = "edit";
        prepView.expanded_intent_steps = ["explore"];
        prepView.active_edit_target = { section_id: "teaching_process", step_id: "explore", label: "教学过程 · 色卡分类探究" };
        model.initial_scroll_target = "nb-1013f-patch-card";
      } else if (viewId === "prepNotebook1013FR1" && prepView) {
        model.active_view = "prepNotebook";
        prepView.prep_notebook_mode = "view";
        prepView.expanded_intent_steps = [];
        prepView.selected_paragraph_id = "";
        model.initial_scroll_target = "nb-section-teaching-process";
      } else if (viewId === "prepNotebook1013FR1Selected" && prepView) {
        model.active_view = "prepNotebook";
        prepView.prep_notebook_mode = "view";
        prepView.expanded_intent_steps = [];
        prepView.selected_paragraph_id = "p-explore-1";
        model.initial_scroll_target = "nb-step-explore";
      } else if (viewId === "prepNotebook1013FR2A" && prepView) {
        model.active_view = "prepNotebook";
        prepView.prep_notebook_mode = "view";
        prepView.expanded_intent_steps = [];
        prepView.selected_paragraph_id = "";
        model.initial_scroll_target = "nb-section-teaching-process";
      } else if (viewId === "prepNotebook1013FR2ASelected" && prepView) {
        model.active_view = "prepNotebook";
        prepView.prep_notebook_mode = "view";
        prepView.expanded_intent_steps = [];
        prepView.selected_paragraph_id = "p-explore-1";
        model.initial_scroll_target = "nb-step-explore";
      } else if (viewId === "prepNotebook1013FR2AEdit" && prepView) {
        model.active_view = "prepNotebook";
        prepView.prep_notebook_mode = "edit";
        prepView.expanded_intent_steps = [];
        prepView.selected_paragraph_id = "";
        prepView.active_edit_target = { section_id: "teaching_process", step_id: "explore", label: "教学过程 · 探究环节" };
        model.initial_scroll_target = "nb-step-explore";
      } else if (viewId === "prepNotebook1013FR2B" && prepView) {
        model.active_view = "prepNotebook";
        prepView.prep_notebook_mode = "view";
        prepView.expanded_intent_steps = [];
        prepView.selected_paragraph_id = "";
        model.initial_scroll_target = "nb-section-teaching-process";
      } else if (viewId === "prepNotebook1013FR2BSelected" && prepView) {
        model.active_view = "prepNotebook";
        prepView.prep_notebook_mode = "view";
        prepView.expanded_intent_steps = [];
        prepView.selected_paragraph_id = "p-explore-1";
        model.initial_scroll_target = "nb-step-explore";
      } else if (viewId === "prepNotebook1013FR2BEdit" && prepView) {
        model.active_view = "prepNotebook";
        prepView.prep_notebook_mode = "edit";
        prepView.expanded_intent_steps = [];
        prepView.selected_paragraph_id = "";
        prepView.active_edit_target = { section_id: "teaching_process", step_id: "explore", label: "教学过程 · 探究环节" };
        model.initial_scroll_target = "nb-step-explore";
      } else if (viewId === "prepNotebookIntent" && prepView) {
        model.active_view = "prepNotebook";
        prepView.prep_notebook_mode = "view";
        prepView.expanded_intent_steps = ["explore"];
        prepView.active_edit_target = { section_id: "teaching_process", step_id: "explore", label: "教学过程 · 探究环节" };
        model.initial_scroll_target = "nb-step-explore";
      } else if (viewId === "prepNotebookReasoning" && prepView) {
        model.active_view = "prepNotebook";
        const trace = prepView.reasoning_trace || {};
        trace.status = "done";
        trace.active_index = (trace.stages || []).length - 1;
        trace.teacher_input = "学生对冷暖色不太理解，要设计得更直观一点。";
        trace.result = "我先整理成两处候选：探究环节加色卡分组，学习单加感受记录格。等你确认。";
        prepView.reasoning_trace = trace;
        applyPrepReasoningCandidate(prepView);
      } else {
        if (!model.views.some((view) => view.id === viewId)) return;
        model.active_view = viewId;
        if (viewId === "prepNotebook" && prepView) {
          prepView.prep_notebook_mode = "view";
          prepView.expanded_intent_steps = [];
        }
      }
      const view = getActiveView();
      const firstWcNode = Object.values(view.slots || {}).flat()[0]?.id || "";
      model.selected_node_id = view.active_node || firstWcNode || model.selected_node_id;
    }

    function getPlanLessonDetail(nodeId) {
      const planView = model.views.find((view) => view.id === "flexibleSemesterMap");
      if (!planView || !String(nodeId).startsWith("plan-")) return null;
      const lessonId = String(nodeId).replace(/^plan-/, "");
      const week = (planView.plan_weeks || []).find((item) => item.lessons.some(([code]) => code === lessonId));
      const lesson = week?.lessons.find(([code]) => code === lessonId);
      if (!lesson) return null;
      const [code, title, tone] = lesson;
      return {
        type: "学期规划课时",
        title: code.startsWith("buffer") || code === "final-show" ? title : `${code} ${title}`,
        fields: [
          ["周次", week.week],
          ["日期", week.date],
          ["单元类型", tone === "blue" ? "海洋/成长类单元" : tone === "amber" ? "青绿中国色/创艺节单元" : tone === "red" ? "红色主题单元" : tone === "buffer" ? "机动与评价" : "教材学习单元"],
          ["正式边界", "仅生成预演，教师确认前不应用"]
        ],
        actions: ["调整周次", "生成课包", "查看影响"]
      };
    }

    function getNodeDetail(nodeId) {
      const nbElement = Array.from(document.querySelectorAll("[data-nb-detail]")).find((item) => item.dataset.node === nodeId);
      if (nbElement) {
        const detail = JSON.parse(nbElement.dataset.nbDetail);
        return {
          type: detail.type,
          title: `${detail.code} ${detail.title}`,
          fields: [
            ["所在目录", detail.group],
            ["当前状态", detail.status],
            ["空间边界", "备课本过程态，不等同于资料室或档案室"],
            ["正式边界", "仅生成预演，教师确认前不应用"]
          ],
          actions: ["打开工作页", "补齐课前包", "查看资料", "写课后记录"]
        };
      }
      const prepFieldElement = Array.from(document.querySelectorAll("[data-prep-field]")).find((item) => item.dataset.node === nodeId);
      if (prepFieldElement) {
        const detail = JSON.parse(prepFieldElement.dataset.prepField);
        return {
          type: detail.type,
          title: detail.title,
          fields: [
            ["当前状态", detail.state],
            ["字段内容", detail.body],
            ["依据", (detail.sources || []).join("、")],
            ["候选", (detail.candidates || []).join("；") || "暂无"],
            ["正式边界", "教师确认前不应用"]
          ],
          actions: ["确认候选", "继续打磨", "引用资料", "标记待沉淀"]
        };
      }
      const wcElement = Array.from(document.querySelectorAll("[data-wc-detail]")).find((item) => item.dataset.node === nodeId);
      if (wcElement) {
        const detail = JSON.parse(wcElement.dataset.wcDetail);
        return {
          type: "课前包详情",
          title: detail.code ? `${detail.classLabel} ${detail.code} ${detail.title}` : detail.title,
          fields: [
            ["时间", `${detail.day} ${detail.date} ${detail.period}`],
            ["班级", detail.classLabel || "全校/活动"],
            ["类型", wcCardTypeLabel(detail.type)],
            ["课前包状态", detail.packageStatus],
            ["已准备", detail.type === "warning" ? "课时设计、资源参考" : "课时设计、学习单、资源参考"],
            ["待处理", detail.type === "warning" ? "学习单/评价量规待确认" : "无正式写入，仅预演"],
            ["上次轻记录", detail.classLabel ? "学生对材料组合和色彩关系需要更多示范。" : "事件占用将影响后续课时落点。"]
          ],
          actions: ["打开课时设计", "确认学习单", "生成量规", "顺手记一笔"]
        };
      }
      const cpsElement = Array.from(document.querySelectorAll("[data-cps-detail]")).find((item) => item.dataset.node === nodeId);
      if (cpsElement) {
        const detail = JSON.parse(cpsElement.dataset.cpsDetail);
        return {
          type: "班级课时实例",
          title: detail.code ? `${detail.code} ${detail.title}` : detail.title,
          fields: [
            ["班级", detail.classLabel],
            ["周次", `${detail.week} ${detail.date}`],
            ["槽位", detail.slot],
            ["类型", cpsCardTypeLabel(detail.type)],
            ["联动", detail.type === "lesson" || detail.type === "future" ? "课包、学习单、评价量规、材料" : "小教调整候选、影响范围"],
            ["正式边界", "仅生成预演，教师确认前不应用"]
          ],
          actions: detail.type === "lesson" || detail.type === "future" ? ["查看课包", "推送下节准备", "生成量规"] : ["查看影响", "采用调整", "暂不处理"]
        };
      }
      const planDetail = getPlanLessonDetail(nodeId);
      if (planDetail) return planDetail;
      if (model.node_details[nodeId]) return model.node_details[nodeId];
      const allNodes = model.views.flatMap((view) => [
        ...(view.nodes || []),
        ...(view.weeks || []),
        ...((view.lanes || []).flatMap((lane) => lane.blocks || []))
      ]);
      const node = allNodes.find((item) => item.id === nodeId);
      if (!node) return null;
      return {
        type: "画布节点",
        title: node.title || node.label || node.id,
        fields: Object.entries(node)
          .filter(([key]) => !["id", "actions"].includes(key))
          .map(([key, value]) => [key, Array.isArray(value) ? value.join("、") : value]),
        actions: node.actions || ["生成预演"]
      };
    }

    function renderNegotiationPanel() {
      const panel = byId("negotiationPanel");
      if (!panel) return;
      const source = model.negotiation;
      const activeNote = source.notes[model.active_view] || source.notes.weekCalendar;
      panel.innerHTML = `
        <div class="assistant-head">
          <div class="assistant-avatar" aria-hidden="true">备</div>
          <div>
            <div class="assistant-name">${html(source.assistant_name)}</div>
            <div class="assistant-role">${html(source.assistant_role)}</div>
          </div>
        </div>

        <section class="section">
          <div class="section-title">
            <span>小教当前判断</span>
            <span class="quiet-tag">只预演</span>
          </div>
          <div class="agent-note" id="agentNote">${html(activeNote)}</div>
        </section>

        <section class="section">
          <div class="section-title">
            <span>影响摘要</span>
            <span class="state-tag">${html(getActiveView().label)}</span>
          </div>
          <ul class="result-list">
            ${source.understanding.map((item) => `<li>${html(item)}</li>`).join("")}
          </ul>
        </section>

        <section class="section">
          <div class="section-title"><span>快速入口</span><span class="quiet-tag">底部输入</span></div>
          <div class="chip-row">
            <button class="text-button" data-chat-fill="公开课提前，帮我看第3周怎么调整">公开课提前</button>
            <button class="text-button" data-chat-fill="先补齐《青绿中国色》的学习单和评价维度">补齐课包</button>
            <button class="text-button" data-action="open-current">查看当前选中节点</button>
          </div>
        </section>
      `;
    }

    function renderViewTabs() {
      byId("viewTabs").innerHTML = model.views.map((view) => `
        <button class="view-tab ${view.id === model.active_view ? "active" : ""}" data-view="${html(view.id)}" role="tab" aria-selected="${view.id === model.active_view}" aria-label="${html(view.label)}" title="${html(view.label)}">
          ${iconButtonLabel(view.label, iconForView(view.id))}
        </button>
      `).join("");
    }

    function renderCanvasHeader(view) {
      document.body.dataset.activeView = view.id;
      const contextTitle = byId("contextTitle");
      if (contextTitle) {
        contextTitle.innerHTML = `<span class="context-space-name">${html(model.space.label)}</span><span class="context-view-name">· ${html(view.label)}</span>`;
        contextTitle.title = `${model.space.label} · ${view.label}`;
      }
      renderViewTabs();
    }

    function renderMetrics(metrics) {
      return `
        <div class="metrics-row">
          ${metrics.map((metric) => `
            <div class="metric ${String(metric.label).includes("周") || String(metric.value).includes("周") ? "week-metric" : ""}">
              <div class="metric-value">${html(metric.value)}</div>
              <div class="metric-label">${html(metric.label)}</div>
            </div>
          `).join("")}
        </div>
      `;
    }

    function wcCardTypeLabel(type) {
      const map = {
        lesson: "正常上课",
        today: "今日课时",
        future: "未来课时",
        warning: "课前包未齐",
        reschedule: "调课",
        activity: "活动占用",
        holiday: "停课",
        makeup: "补课/顺延",
        done: "已完成"
      };
      return map[type] || "课时";
    }

    function nbStatusLabel(status) {
      const map = {
        done: "已完成",
        warn: "待确认",
        draft: "草稿",
        missing: "缺材料"
      };
      return map[status] || "过程态";
    }

    function nbMetricTone(label) {
      if (String(label).includes("缺")) return "missing";
      if (String(label).includes("待")) return "warn";
      return "done";
    }

    function renderPrepNotebookTree(view) {
      return view.tree.map((group) => `
        <section class="nb-tree-group">
          <div class="nb-tree-title"><span class="nb-tree-mark ${html(group.tone)}"></span>${html(group.title)}</div>
          <div class="nb-tree-items">
            ${group.items.map((item) => {
              const detail = {
                type: "备课本节点",
                group: group.title,
                code: item.code,
                title: item.title,
                status: nbStatusLabel(item.status)
              };
              return `
                <button class="nb-tree-button ${item.id === view.active_node ? "active" : ""}" type="button" data-node="${html(item.id)}" data-nb-detail="${html(JSON.stringify(detail))}" title="${html(item.title)}">
                  <span class="nb-node-code">${html(item.code)}</span>
                  <span class="nb-node-title">${html(item.title)}</span>
                  <span class="nb-status-dot ${html(item.status)}" aria-label="${html(nbStatusLabel(item.status))}"></span>
                </button>
              `;
            }).join("")}
          </div>
        </section>
      `).join("");
    }

    function prepNotebookMode(view) {
      return view.prep_notebook_mode === "edit" ? "edit" : "view";
    }

    function prepActiveTarget(view) {
      const target = view.active_edit_target || {};
      return {
        sectionId: target.section_id || "",
        stepId: target.step_id || "",
        label: target.label || "当前段落"
      };
    }

    function processStepById(view, stepId) {
      return (view.current_lesson?.process_steps || []).find((step) => step.id === stepId);
    }

    function renderSectionTags(items = []) {
      return items.length ? `<div class="nb-section-tags">${items.map((item) => `<span class="nb-section-tag">${html(item)}</span>`).join("")}</div>` : "";
    }

    function renderLessonSection(view, section, number) {
      const mode = prepNotebookMode(view);
      const target = prepActiveTarget(view);
      const focused = mode === "edit" && target.sectionId === section.id;
      return `
        <section class="nb-doc-section ${focused ? "edit-focus" : ""}" id="nb-section-${html(section.id)}">
          <div class="nb-doc-section-head">
            <div class="nb-doc-title">${html(number)}、${html(section.title)}</div>
            <button class="nb-soft-button" type="button" data-edit-target="section:${html(section.id)}" title="编辑本段">进入编辑</button>
          </div>
          <div class="nb-doc-body">
            ${(section.body || []).map((line) => `<p>${html(line)}</p>`).join("")}
          </div>
          ${renderSectionTags([...(section.sources || []), section.status].filter(Boolean))}
          ${section.candidate ? `<div class="nb-section-candidate">${html(section.candidate)}</div>` : ""}
          ${focused ? renderEditPanel(view, section.title) : ""}
        </section>
      `;
    }

    function renderIntentPanel(step) {
      const intent = step.intent || {};
      const items = [
        ["环节作用", intent.role],
        ["设计意图", intent.design],
        ["承上启下", intent.transition],
        ["学生当前状态", intent.student],
        ["教师动作", intent.teacher],
        ["学生活动", intent.activity],
        ["大屏状态", intent.screen],
        ["学习单 / 教材 / 材料", intent.material],
        ["评价证据", intent.evidence],
        ["风险与调整", intent.risk]
      ];
      return `
        <div class="nb-intent-panel">
          <div class="nb-intent-grid">
            ${items.map(([label, value]) => `
              <div class="nb-intent-item"><strong>${html(label)}</strong>${html(value || "待补充")}</div>
            `).join("")}
          </div>
        </div>
      `;
    }

    function readableStepPlan(step) {
      const plans = {
        intro: {
          paragraphs: [
            "先出示两组色彩气氛差异明显的生活图片，请学生说一说“这些颜色给你什么感觉”。这一段不急着讲冷暖色概念，而是把学生已有的生活经验调出来，让他们先敢说、会说。",
            "如果学生只说“好看”或“不好看”，教师可以追问：“你说的好看，是让你觉得热闹、安静，还是舒服？”必要时给出几个感受词，让回答从喜好慢慢走向理由。"
          ],
          hover: "先从生活图片进入，是为了让学生把颜色和真实感受连起来，不一上来背概念。",
          note: [
            ["为什么这样安排", "这一段服务于入课和诊断：先听学生能说到什么程度，再决定后面支架要给多细。"],
            ["学生可能卡在哪里", "学生容易停在“好看、漂亮”，还不能说出颜色为什么带来这种感觉。"],
            ["可以怎么支架", "给出温暖、安静、热烈等词卡，让学生先选词，再补一句理由。"],
            ["会带动什么", "大屏准备两组对比图片；学习单先不出现，避免打断口头表达。"]
          ]
        },
        sense: {
          paragraphs: [
            "接着把生活图片和教材中的作品放在一起看，请学生比较两组画面里的颜色哪里不同、带来的感觉哪里不同。教师示范一句表达：“这组橙黄色让我觉得温暖，因为像阳光。”",
            "这一段的重点不是找标准答案，而是让学生发现：颜色不只是名称，它会改变画面的气氛，也会影响观看者的情绪。"
          ],
          hover: "从直觉感受推进到有依据的比较，让学生开始说“颜色、感受、理由”的关系。",
          note: [
            ["为什么这样安排", "承接导入里的口头感受，借作品和生活图帮助学生看见色彩与情绪的关系。"],
            ["学生可能卡在哪里", "学生能看出颜色不一样，但理由容易空泛，或者只说画面内容。"],
            ["可以怎么支架", "用一句话模板示范：我看到____色，所以觉得____，因为____。"],
            ["会带动什么", "大屏保留图片对比和表达样例；教材范图只作观察材料，不做长篇讲解。"]
          ]
        },
        explore: {
          paragraphs: [
            "进入探究时，学生分组拿到色卡和少量生活物品，把颜色贴到“温暖、清凉、安静、热烈”等感受词下面。小组不是抢正确答案，而是要选一张色卡说清楚：为什么它适合放在这里。",
            "教师巡视时重点听理由。如果学生只是按红黄蓝绿分类，可以追问：“你把它放在这里，是因为它像什么，还是让你想到什么？”这样把分类活动从颜色名称拉回到感受证据。"
          ],
          hover: "这一段把抽象的冷暖感受变成动手分类和理由表达，是本课理解是否成立的关键。",
          note: [
            ["为什么这样安排", "学生对冷暖色不稳时，色卡分类能把抽象概念变成可操作活动。"],
            ["学生可能卡在哪里", "学生可能按颜色名称或个人喜好分类，而不是按感受说明理由。"],
            ["可以怎么支架", "先给一组示范，再让学生用“像____，所以我觉得____”补理由。"],
            ["会带动什么", "大屏需要保留感受词；学习单增加一句理由记录；观察学生能否说出分类依据。"]
          ]
        },
        make: {
          paragraphs: [
            "表现环节让学生围绕“我心中的一种感受”做色彩小练习。基础任务可以选一种感受配色；进阶任务画一个小场景；挑战任务尝试用两组颜色表现情绪变化。",
            "教师提醒学生先想清楚要表达什么，再选择颜色。这样作业既不只是涂满纸面，也不会一下子变成超出三年级能力的大创作。"
          ],
          hover: "这一段把前面的分类和理由转成个人表达，并用分层任务照顾不同学生。",
          note: [
            ["为什么这样安排", "把理解落到作品中，让学生用颜色表达心情、天气、场景或小故事。"],
            ["学生可能卡在哪里", "学生可能只追求涂得满、颜色多，而忽略自己想表达的感受。"],
            ["可以怎么支架", "给三层任务选择，基础层先够得着，能力强的学生再做更开放表达。"],
            ["会带动什么", "材料准备绘画纸和色彩工具；学习单保留一句作品说明。"]
          ]
        },
        share: {
          paragraphs: [
            "最后选择两三件作品交流。学生先用一句话说明自己的色彩选择，同伴再说自己读到的感受，教师把“颜色选择”和“情绪表达”之间的关系收回来。",
            "如果时间不够，不追求展示数量。保留一件表达清楚的作品和一件需要调整的作品，就能帮助全班看见：颜色有没有真正服务于自己想表达的意思。"
          ],
          hover: "收束时看学生能否把作品、感受和理由连起来，而不是只评价画得像不像。",
          note: [
            ["为什么这样安排", "用说和听检查本课目标是否达成，让作品成为可讨论的学习结果。"],
            ["学生可能卡在哪里", "有些学生能画出来，但说明句不清楚，需要模板帮他表达。"],
            ["可以怎么支架", "用“我用了____色，因为我想表达____”帮助学生完成说明。"],
            ["会带动什么", "课堂记录保留作品照片和学生说明，作为下节课承接材料。"]
          ]
        }
      };
      return plans[step.id] || {
        paragraphs: [step.summary || ""],
        hover: "这一段暂时没有可用的小教旁注。",
        note: [["小教旁注", "这一段暂时没有可用的小教旁注。"]]
      };
    }

    function paragraphAnchorId(step, index) {
      return `p-${step.id}-${index + 1}`;
    }

    function renderSelectedParagraphNote(view, plan, paragraphId) {
      if (view.selected_paragraph_id !== paragraphId) return "";
      return "";
    }

    function selectedParagraphContext(view) {
      const paragraphId = view.selected_paragraph_id;
      if (!paragraphId) return null;
      for (const step of view.current_lesson?.process_steps || []) {
        const plan = readableStepPlan(step);
        const paragraphs = plan.paragraphs || [step.summary || ""];
        for (let index = 0; index < paragraphs.length; index += 1) {
          const currentId = paragraphAnchorId(step, index);
          if (currentId === paragraphId) {
            const notes = (plan.note || []).slice(0, 4);
            return {
              paragraphId,
              step,
              paragraph: paragraphs[index],
              hover: plan.hover,
              notes: [
                ["小教判断", notes[0]?.[1] || plan.hover],
                ["学生可能卡在哪里", notes[1]?.[1] || "这一段暂时没有可用的小教旁注。"],
                ["可以怎么支架", notes[2]?.[1] || "先观察学生回答，再决定是否补支架。"],
                ["会影响什么", notes[3]?.[1] || "暂不生成额外修改。"]
              ]
            };
          }
        }
      }
      return null;
    }

    function renderSelectedParagraphSideNote(view) {
      const context = selectedParagraphContext(view);
      if (!context) return "";
      return `
        <section class="nb-side-note-card" data-inline-note>
          <div class="nb-drawer-title"><span>当前段落旁注</span><span class="quiet-tag">点空白收起</span></div>
          <div class="nb-side-note-kicker">${html(context.step.name)} · ${html(context.step.time)}</div>
          ${context.notes.map(([label, text]) => `
            <div class="nb-side-note-block"><strong>${html(label)}</strong>${html(text)}</div>
          `).join("")}
          <details class="nb-low-weight-fields">
            <summary>查看低权重来源</summary>
            <div>来源段落：${html(context.paragraph)}<br>raw field keys: classroom_event / design_view / execution_view</div>
          </details>
        </section>
      `;
    }

    function renderSelectedParagraphFloatNote(view, paragraphId) {
      if (view.selected_paragraph_id !== paragraphId || prepNotebookMode(view) === "edit") return "";
      const note = renderSelectedParagraphSideNote(view);
      return note ? `<div class="nb-paragraph-float-note">${note}</div>` : "";
    }

    function renderProcessStep(view, step, index) {
      const mode = prepNotebookMode(view);
      const target = prepActiveTarget(view);
      const isFocused = mode === "edit" && target.stepId === step.id;
      const plan = readableStepPlan(step);
      const stepParagraphIds = (plan.paragraphs || [step.summary]).map((_, paragraphIndex) => paragraphAnchorId(step, paragraphIndex));
      const hasSelectedParagraph = stepParagraphIds.includes(view.selected_paragraph_id);
      return `
        <article class="nb-readable-step ${isFocused ? "edit-focus" : ""}" id="nb-step-${html(step.id)}">
          <div class="nb-readable-head">
            <div class="nb-readable-title">
              ${index + 1}. ${html(step.name)}：${html((step.summary || step.name).split("，")[0])}
              <span>${html(step.time)} · ${html((step.tags || []).join(" / "))}</span>
            </div>
            <div class="nb-edit-tools">
              <button class="nb-soft-button" type="button" data-edit-target="process:${html(step.id)}">编辑</button>
            </div>
          </div>
          <div class="nb-readable-body">
            ${(plan.paragraphs || [step.summary]).slice(0, 2).map((paragraph, paragraphIndex) => {
              const paragraphId = paragraphAnchorId(step, paragraphIndex);
              const selected = view.selected_paragraph_id === paragraphId;
              return `
                <p class="nb-anchor-paragraph ${selected ? "selected" : ""}"
                   data-select-paragraph="${html(paragraphId)}"
                   data-hover-note="${html(plan.hover)}">${html(paragraph)}</p>
                ${renderSelectedParagraphNote(view, plan, paragraphId)}
              `;
            }).join("")}
            ${hasSelectedParagraph ? renderSelectedParagraphFloatNote(view, view.selected_paragraph_id) : ""}
          </div>
          ${step.candidate && isFocused ? `<div class="nb-step-candidate">${html(step.candidate)}</div>` : ""}
          ${isFocused ? renderEditPanel(view, `${step.name}环节`) : ""}
        </article>
      `;
    }

    function renderEditPanel(view, title) {
      const edit = view.current_lesson.edit_context || {};
      const patch = view.current_lesson?.reasoning_binding_1013F?.patch_candidate || {};
      const targetStep = processStepById(view, prepActiveTarget(view).stepId || "explore") || processStepById(view, "explore") || {};
      const plan = readableStepPlan(targetStep);
      const currentParagraph = (plan.paragraphs || [targetStep.summary || edit.candidate || ""]).find(Boolean) || "";
      const impactItems = (patch.impact_scope || []).slice(0, 3).map(([, text]) => text);
      return `
        <div class="nb-edit-panel">
          <div class="nb-edit-panel-title">
            <span>小教建议 · ${html(title)}</span>
            <span class="quiet-tag">待你确认</span>
          </div>
          <div class="nb-edit-surface">
            <div class="nb-edit-surface-block">
              <strong>当前段落</strong>
              ${html(currentParagraph)}
            </div>
            <div class="nb-edit-surface-block emphasis">
              <strong>小教建议</strong>
              ${html(patch.summary || edit.judgment || "先围绕当前段落形成候选，不直接生效。")}
            </div>
            <div class="nb-before-after">
              <div class="nb-edit-surface-block">
                <strong>修改前</strong>
                ${html(patch.before || "学生说一说颜色给自己的感觉。")}
              </div>
              <div class="nb-edit-surface-block">
                <strong>修改后</strong>
                ${html(patch.after || edit.candidate || "学生说出颜色带来的感受，并尝试补一句理由。")}
              </div>
            </div>
            <div class="nb-edit-surface-block">
              <strong>会影响什么</strong>
              ${(impactItems.length ? impactItems : edit.impacts || []).slice(0, 3).map((item) => `<div>${html(item)}</div>`).join("")}
            </div>
            <details class="nb-low-weight-fields">
              <summary>查看低权重来源</summary>
              <div>${html(edit.gap || "当前候选来自教学过程与影响范围推演。")} ${(edit.related || []).map((item) => html(item)).join(" / ")}<br>raw field keys: field_patch_candidates / impact_scope / student_response_model</div>
            </details>
          </div>
          <div class="nb-edit-tools">
            ${(patch.actions || ["采纳到本段", "继续精修", "追问原因", "暂不采用"]).slice(0, 4).map((action, index) => `
              <button class="nb-soft-button ${index === 0 ? "primary" : ""}" type="button" data-pending="小教已把「${html(action)}」放入待确认队列。">${html(action)}</button>
            `).join("")}
          </div>
        </div>
      `;
    }

    function renderProcessSection(view, number) {
      const lesson = view.current_lesson;
      return `
        <section class="nb-doc-section" id="nb-section-teaching-process">
          <div class="nb-doc-section-head">
            <div class="nb-doc-title">${html(number)}、教学过程</div>
            <span class="quiet-tag">轻点段落看小教旁注</span>
          </div>
          <div class="nb-readable-process">
            ${(lesson.process_steps || []).map((step, index) => renderProcessStep(view, step, index)).join("")}
          </div>
        </section>
      `;
    }

    function renderLessonDesignMode(view) {
      const modes = view.lesson_design_modes || [];
      const current = view.lesson_design_mode || "standard_daily";
      return `
        <div class="nb-mode-strip" aria-label="备课程度">
          <span class="quiet-tag">备课程度</span>
          ${modes.map((item) => `
            <button class="nb-mode-pill ${item.id === current ? "active" : ""}" type="button" data-lesson-mode="${html(item.id)}" title="${html(item.note)}">
              ${html(item.label)}
            </button>
          `).join("")}
        </div>
      `;
    }

    function renderLessonReasoningBrief(lesson) {
      const brief = lesson.design_brief_summary;
      if (!brief) return "";
      return `
        <section class="nb-reasoning-brief" aria-label="本课设计判断">
          <div class="nb-section-head"><span>本课设计判断</span><span class="quiet-tag">先判断，再生成候选</span></div>
          <div class="nb-reasoning-grid">
            <div class="nb-reasoning-item"><strong>要解决的问题</strong><span>${html(brief.problem)}</span></div>
            <div class="nb-reasoning-item"><strong>希望发生的变化</strong><span>${html(brief.shift)}</span></div>
            <div class="nb-reasoning-item"><strong>教学路径</strong><span>${html(brief.route)}</span></div>
            <div class="nb-reasoning-item"><strong>怎么看达成</strong><span>${html(brief.evidence)}</span></div>
          </div>
        </section>
      `;
    }

    function renderReasoningBinding1013F(view) {
      const binding = view.current_lesson?.reasoning_binding_1013F;
      if (!binding) return "";
      return `
        <section class="nb-binding-card" id="nb-1013f-binding" aria-label="小教课堂推演候选">
          <div class="nb-binding-head">
            <div class="nb-binding-title">
              小教读课提示
              <span>只读候选 · 不写入正式备课本</span>
            </div>
            <span class="quiet-tag">等你确认</span>
          </div>
          <div class="nb-binding-quote">${html(binding.judgment)}</div>
          <div class="nb-right-note">这条提示先帮助老师把本课读成一条课堂推进线；具体怎么上，已经放回下面的教学过程正文。轻点段落，可以看到小教为什么这样安排。</div>
        </section>
      `;
    }

    function renderPatchCandidate1013F(view) {
      const patch = view.current_lesson?.reasoning_binding_1013F?.patch_candidate;
      if (!patch) return "";
      return `
        <div class="nb-patch-card" id="nb-1013f-patch-card">
          <div class="nb-edit-panel-title">
            <span>${html(patch.summary)}</span>
            <span class="quiet-tag">只读候选</span>
          </div>
          <div class="nb-patch-row"><strong>建议修改位置</strong>${html(patch.target_label)}</div>
          <div class="nb-patch-row"><strong>原来可能的问题</strong>${html(patch.before)}</div>
          <div class="nb-patch-row"><strong>建议改成</strong>${html(patch.after)}</div>
          <div class="nb-patch-row"><strong>为什么这样改</strong>${html(patch.why)}</div>
          <div class="nb-impact-grid">
            ${(patch.impact_scope || []).map(([label, text]) => `
              <div class="nb-impact-item"><strong>${html(label)}</strong>${html(text)}</div>
            `).join("")}
          </div>
          <div class="nb-response-grid">
            ${(patch.responses || []).map(([label, student, nextMove, scaffold]) => `
              <div class="nb-response-item"><strong>${html(label)}</strong>${html(student)}<br>${html(nextMove)}<br>${html(scaffold)}</div>
            `).join("")}
          </div>
          <div class="nb-edit-tools">
            ${(patch.actions || []).map((action, index) => `
              <button class="nb-soft-button ${index === 0 ? "primary" : ""}" type="button" data-pending="已把「${html(action)}」放入预览确认队列，未写入正式备课本。">${html(action)}</button>
            `).join("")}
          </div>
        </div>
      `;
    }

    function renderReasoningTrace(view) {
      const trace = view.reasoning_trace || {};
      if (!trace.status || trace.status === "idle") return "";
      const stages = trace.stages || [];
      const activeIndex = Number.isFinite(trace.active_index) ? trace.active_index : -1;
      const isDone = trace.status === "done";
      return `
        <section class="nb-trace-card" aria-label="小教正在同步思考">
          <div class="nb-trace-head">
            <div class="nb-trace-title">
              <strong>${isDone ? "小教已整理出候选" : "小教正在同步思考"}</strong>
              <span>${html(trace.teacher_input ? `你刚才说：${trace.teacher_input}` : "我会把等待过程拆成几步给你看。")}</span>
            </div>
            <span class="quiet-tag">${isDone ? "待确认" : "处理中"}</span>
          </div>
          <div class="nb-trace-list">
            ${stages.map((stage, index) => {
              const state = isDone || index < activeIndex ? "done" : index === activeIndex ? "current" : "";
              const copy = state === "done" ? stage.done : stage.pending;
              return `
                <div class="nb-trace-step ${state}">
                  <span class="nb-trace-dot" aria-hidden="true"></span>
                  <span class="nb-trace-copy">
                    <strong>${html(stage.title)}</strong>
                    <span>${html(copy)}</span>
                  </span>
                </div>
              `;
            }).join("")}
          </div>
          ${trace.result ? `<div class="nb-trace-result">${html(trace.result)}</div>` : ""}
        </section>
      `;
    }

    function renderPrepNotebookRightPanel(view) {
      const mode = prepNotebookMode(view);
      const panels = view.right_panels?.[mode] || [];
      const title = mode === "edit" ? "编辑辅助" : "阅读辅助";
      const tag = mode === "edit" ? prepActiveTarget(view).label : "按需打开";
      return `
        <aside class="nb-drawer" aria-label="${html(title)}">
          <div class="nb-panel-head"><span>${html(title)}</span><span class="quiet-tag">${html(tag)}</span></div>
          ${panels.map((drawer) => `
            <section class="nb-drawer-card">
              <div class="nb-drawer-title"><span>${html(drawer.title)}</span><span class="quiet-tag">${html(drawer.tag)}</span></div>
              <ul class="nb-drawer-list">
                ${drawer.items.map((item) => `<li>${html(item)}</li>`).join("")}
              </ul>
            </section>
          `).join("")}
        </aside>
      `;
    }

    function renderPrepNotebookCanvas(view) {
      const lesson = view.current_lesson;
      const mode = prepNotebookMode(view);
      const sections = lesson.sections || [];
      const beforeProcess = sections.slice(0, 5);
      const afterProcess = sections.slice(5);
      return `
        <div class="nb-scene">
          <div class="nb-binder" aria-label="备课本活页夹">
            <aside class="nb-panel" aria-label="备课本目录">
              <div class="nb-cover">
                <div class="nb-cover-title">${html(view.cover.title)}</div>
                <div class="nb-cover-sub">${html(view.cover.subtitle)}</div>
                <div class="nb-metrics">
                  ${view.cover.metrics.map(([label, value]) => `
                    <div class="nb-metric ${nbMetricTone(label)}">
                      <span class="nb-metric-light" aria-hidden="true"></span>
                      <strong>${html(value)}</strong>
                      <span>${html(label)}</span>
                    </div>
                  `).join("")}
                </div>
              </div>
              <div class="nb-tree">${renderPrepNotebookTree(view)}</div>
            </aside>

            <div class="nb-gutter" aria-hidden="true"></div>

            <section class="nb-workspace" aria-label="当前课时工作页">
              <div class="nb-hero">
                <div>
                  <div class="nb-kicker">${html(lesson.unit)}</div>
                  <div class="nb-title">${html(lesson.code)}《${html(lesson.title)}》</div>
                </div>
                <div class="nb-hero-actions">
                  <button class="node-action primary" data-nb-mode="${mode === "edit" ? "view" : "edit"}">${iconButtonLabel(mode === "edit" ? "回到查看" : "进入编辑", mode === "edit" ? "eye" : "arrow")}</button>
                  <button class="node-action secondary" data-view="weekCalendar">${iconButtonLabel("返回周课表", "calendar")}</button>
                </div>
              </div>

              <div class="nb-state-bar">
                <div>
                  <span class="state-tag">${mode === "edit" ? "编辑状态" : "查看状态"}</span>
                  <span class="quiet-tag">${html(lesson.status)}</span>
                </div>
                <div class="nb-mode-toggle" aria-label="备课本状态">
                  <button class="nb-mode-btn ${mode === "view" ? "active" : ""}" type="button" data-nb-mode="view">查看</button>
                  <button class="nb-mode-btn ${mode === "edit" ? "active" : ""}" type="button" data-nb-mode="edit">编辑</button>
                </div>
              </div>

              ${renderLessonDesignMode(view)}
              ${renderReasoningTrace(view)}

              <section>
                <div class="nb-section-head"><span>本课状态</span><span class="quiet-tag">真实课题 · 候选预览</span></div>
                <div class="nb-status-grid">
                  ${lesson.status_cards.map(([label, value]) => `
                    <div class="nb-status-card">
                      <strong>${html(value)}</strong>
                      <span>${html(label)}</span>
                    </div>
                  `).join("")}
                </div>
              </section>

              ${mode === "edit" ? `<section>${renderEditPanel(view, prepActiveTarget(view).label)}</section>` : ""}

              <div class="nb-doc">
                <div class="nb-field-body">${html(lesson.brief)}</div>
                ${renderLessonReasoningBrief(lesson)}
                ${renderReasoningBinding1013F(view)}
                ${beforeProcess.map((section, index) => renderLessonSection(view, section, ["一", "二", "三", "四", "五"][index])).join("")}
                ${renderProcessSection(view, "六")}
                ${afterProcess.map((section, index) => renderLessonSection(view, section, ["七", "八", "九"][index])).join("")}
              </div>

              <section>
                <div class="nb-section-head"><span>流转关系</span><span class="quiet-tag">正在用 / 课堂 / 用完留下</span></div>
                <div class="nb-flow">
                  ${lesson.flow.map((step, index) => `<div class="nb-flow-step ${index === 1 ? "current" : ""}">${html(step)}</div>`).join("")}
                </div>
              </section>
            </section>
          </div>

          ${renderPrepNotebookRightPanel(view)}
        </div>
      `;
    }

    function renderWeekCalendarCard(item, day, period) {
      const detail = {
        id: item.id,
        day: day.label,
        date: day.date,
        period,
        type: item.type,
        classLabel: item.classLabel,
        code: item.code,
        title: item.title,
        packageStatus: item.packageStatus
      };
      const cardType = day.state === "today" && item.type === "lesson" ? "today" : item.type;
      return `
        <button class="wc-course-card ${html(cardType)}" type="button" data-node="${html(item.id)}" data-wc-detail="${html(JSON.stringify(detail))}" title="${html(item.title)}">
          ${item.classLabel ? `<span class="wc-course-class">${html(item.classLabel)}</span>` : ""}
          <span class="wc-course-title">${html(item.code ? `${item.code} ${item.title}` : item.title)}</span>
          <span class="wc-course-status">${html(item.packageStatus || wcCardTypeLabel(cardType))}</span>
        </button>
      `;
    }

    function renderWeekCalendarCanvas(view) {
      return `
        <div class="wc-scene">
          <div class="wc-control-row">
            <div class="wc-control-cluster">
              <span class="wc-chip week">${html(view.term)}</span>
              ${view.grade_options.map((grade) => `<button class="wc-chip ${grade === view.active_grade ? "active" : ""}" type="button" data-pending="已切换到${html(grade)}周课表预演，等待接入真实课表。">${html(grade)}</button>`).join("")}
              <span class="wc-chip week">${html(view.week_label)} · ${html(view.date_range)}</span>
              ${view.week_modes.map((mode) => `<button class="wc-chip ${mode === "本周" ? "active" : ""}" type="button" data-pending="${html(mode)}周课表已进入预演队列。">${html(mode)}</button>`).join("")}
              <button class="wc-chip" type="button" data-view="prepNotebook" title="进入备课本">备课本</button>
              <div class="wc-legend-row" aria-label="周课表状态图例">
                <span class="wc-legend-item"><span class="wc-dot"></span>正常</span>
                <span class="wc-legend-item"><span class="wc-dot today"></span>今日</span>
                <span class="wc-legend-item"><span class="wc-dot warning"></span>未齐</span>
                <span class="wc-legend-item"><span class="wc-dot reschedule"></span>调课</span>
                <span class="wc-legend-item"><span class="wc-dot activity"></span>活动</span>
                <span class="wc-legend-item"><span class="wc-dot holiday"></span>停课</span>
                <span class="wc-legend-item"><span class="wc-dot makeup"></span>补课</span>
              </div>
            </div>
          </div>
          <div class="wc-main-grid">
            <section class="wc-calendar-board" aria-label="本周课表">
              <div class="wc-header-row">
                <div class="wc-corner">节次</div>
                ${view.days.map((day) => `
                  <div class="wc-day-head ${html(day.state)}">
                    <div>
                      <div>${html(day.label)}</div>
                      <div class="wc-day-date">${html(day.date)}${day.state === "today" ? " · 今日" : day.state === "workday" ? " · 调休" : ""}</div>
                    </div>
                  </div>
                `).join("")}
              </div>
              ${view.periods.map((period, periodIndex) => `
                <div class="wc-period-row">
                  <div class="wc-period-label">${html(period)}</div>
                  ${view.days.map((day) => {
                    const slotKey = `p${periodIndex + 1}-${day.id}`;
                    const items = view.slots[slotKey] || [];
                    return `
                      <div class="wc-cell ${html(day.state)}">
                        ${items.length ? items.map((item) => renderWeekCalendarCard(item, day, period)).join("") : `<span class="wc-empty" aria-hidden="true"></span>`}
                      </div>
                    `;
                  }).join("")}
                </div>
              `).join("")}
            </section>
            <aside class="wc-side-panel" aria-label="课前执行信息">
              <section class="wc-side-section">
                <div class="wc-side-title"><span>今日课前准备</span><span class="quiet-tag">需处理</span></div>
                <div class="wc-side-list">
                  ${view.prep_items.map((item) => `<div class="wc-side-item"><strong>${html(item.title)}</strong>${html(item.status)}</div>`).join("")}
                </div>
              </section>
              <section class="wc-side-section">
                <div class="wc-side-title"><span>小教提醒</span><span class="quiet-tag">预演</span></div>
                <div class="wc-side-list">
                  ${view.alerts.map((item) => `<div class="wc-side-item">${html(item)}</div>`).join("")}
                </div>
              </section>
              <section class="wc-side-section">
                <div class="wc-side-title"><span>本周课前包</span><span class="quiet-tag">统计</span></div>
                <div class="wc-summary-row">
                  ${view.package_summary.map(([label, value]) => `<div class="wc-summary-cell"><strong>${html(value)}</strong>${html(label)}</div>`).join("")}
                </div>
              </section>
              <div class="chip-row" style="margin-top: 12px;">
                <button class="node-action primary" data-pending="小教已打开课前包处理预演，等待教师确认。">${iconButtonLabel("打开课前包", "arrow")}</button>
                <button class="node-action secondary" data-pending="小教已生成缺失材料候选，等待教师确认。">${iconButtonLabel("生成缺失材料", "wand")}</button>
              </div>
            </aside>
          </div>
        </div>
      `;
    }

    function cpsCardTypeLabel(type) {
      const map = {
        lesson: "课时",
        activity: "活动",
        holiday: "停课",
        reschedule: "调课",
        delay: "顺延",
        makeup: "补课",
        future: "未来",
        empty: "空"
      };
      return map[type] || "课时";
    }

    function renderClassProgressSlot(slot, week, klass, index) {
      const [type, code, title] = slot || ["empty", "", "未排课"];
      const cardType = week.state === "future" && type === "lesson" ? "future" : type;
      const detail = {
        week: week.label,
        date: week.date,
        classLabel: klass.label,
        slot: `第${index + 1}课时`,
        type: cardType,
        code,
        title
      };
      const nodeId = `cps-${week.id}-${klass.id}-${index + 1}`;
      return `
        <div class="cps-schedule-slot">
          <button class="cps-slot-card ${html(cardType)}" type="button" data-node="${html(nodeId)}" data-cps-detail="${html(JSON.stringify(detail))}" title="${html(title || cpsCardTypeLabel(cardType))}">
            <span class="lesson-code">${html(code)}</span>
            <span>${html(title || cpsCardTypeLabel(cardType))}</span>
          </button>
        </div>
      `;
    }

    function renderClassProgressScheduleCanvas(view) {
      return `
        <div class="cps-scene">
          <div class="cps-control-row">
            <div class="cps-control-cluster">
              <div class="cps-grade-switcher" aria-label="年级切换">
                ${view.grade_options.map((grade) => `<button class="cps-grade-btn ${grade.id === view.active_grade ? "active" : ""}" type="button" data-pending="已切换到${html(grade.label)}排课看板预演，等待接入真实课表。">${html(grade.label)}</button>`).join("")}
              </div>
              <div class="cps-summary-row" aria-label="排课摘要">
                ${view.metrics.map((metric) => `
                  <div class="cps-summary-card" title="${html(metric.label)}">
                    <div class="cps-summary-icon">${icon(metric.label.includes("班") ? "classes" : metric.label.includes("一致") ? "check" : metric.label.includes("调整") ? "clock" : "calendar")}</div>
                    <div class="cps-summary-value">${html(metric.value)}</div>
                  </div>
                `).join("")}
              </div>
              <div class="cps-legend-row" aria-label="排课状态图例">
                <span class="cps-legend-item"><span class="cps-legend-dot"></span>正常课时</span>
                <span class="cps-legend-item"><span class="cps-legend-dot future"></span>未来课</span>
                <span class="cps-legend-item"><span class="cps-legend-dot activity"></span>活动</span>
                <span class="cps-legend-item"><span class="cps-legend-dot holiday"></span>节假日</span>
                <span class="cps-legend-item"><span class="cps-legend-dot reschedule"></span>调课</span>
                <span class="cps-legend-item"><span class="cps-legend-dot makeup"></span>补课/顺延</span>
              </div>
            </div>
            <div class="cps-mode-switcher" aria-label="视图模式">
              <button class="cps-mode-btn active" type="button">全班对照</button>
              <button class="cps-mode-btn" type="button" data-pending="单班详情视图已进入预演队列。">单班详情</button>
              <button class="cps-mode-btn" type="button" data-pending="调整建议视图已进入预演队列。">调整建议</button>
            </div>
          </div>
          <div class="cps-main-grid">
            <aside class="cps-catalog" aria-label="单元课时目录">
              <div class="cps-panel-head"><span>单元课时目录</span><span class="quiet-tag">辅助栏</span></div>
              ${view.lesson_catalog.map((unit) => `
                <section class="cps-unit-group">
                  <div class="cps-unit-title">
                    <span class="cps-unit-name"><span class="cps-unit-mark ${html(unit.tone)}"></span>${html(unit.title)}</span>
                    <span class="cps-unit-hours">${html(unit.hours)}</span>
                  </div>
                  <div class="cps-catalog-lessons">
                    ${unit.lessons.map(([code, title]) => `<button class="cps-catalog-lesson" type="button" data-pending="已高亮 ${html(code)} 在各班中的课时落点。"><span class="lesson-code">${html(code)}</span><span>${html(title)}</span></button>`).join("")}
                  </div>
                </section>
              `).join("")}
            </aside>
            <section class="cps-board" aria-label="周次班级排课看板">
              <div class="cps-class-header-row">
                <div class="cps-corner-cell">周次</div>
                ${view.class_headers.map((klass) => `
                  <div class="cps-class-header ${klass.state === "behind" ? "risk" : ""}">
                    <div>
                      <div class="cps-class-name">${html(klass.label)}</div>
                      <div class="cps-class-progress">当前 ${html(klass.current)}</div>
                    </div>
                  </div>
                `).join("")}
              </div>
              ${view.week_axis.map((week) => `
                <div class="cps-week-row ${week.state === "current" ? "current" : ""} ${week.state === "future" ? "future" : ""}">
                  <div class="cps-week-axis">
                    <div>
                      <div class="cps-week-title">${html(week.label)}</div>
                      <div class="cps-week-date">${html(week.date)}</div>
                      ${week.state === "current" ? `<div class="cps-today-mark">当前周</div>` : ""}
                    </div>
                  </div>
                  ${view.class_headers.map((klass) => {
                    const slots = view.class_week_cells[`${week.id}-${klass.id}`] || [["empty", "", "未排课"], ["empty", "", "未排课"]];
                    return `
                      <div class="cps-class-week-cell">
                        <div class="cps-weekly-slot-stack">
                          ${[0, 1].map((slotIndex) => renderClassProgressSlot(slots[slotIndex], week, klass, slotIndex)).join("")}
                        </div>
                      </div>
                    `;
                  }).join("")}
                </div>
              `).join("")}
            </section>
            <aside class="cps-suggestions" aria-label="小教建议">
              <div class="cps-panel-head"><span>小教建议</span><span class="quiet-tag">需教师确认</span></div>
              <div class="cps-suggestion-list">
                ${view.suggestions.map((item, index) => `
                  <div class="cps-suggestion-item">
                    <div><span class="cps-suggestion-index">${index + 1}</span><strong>${html(item.tone === "normal" ? "下节准备" : "排课提醒")}</strong></div>
                    <div class="cps-suggestion-text">${html(item.text)}</div>
                  </div>
                `).join("")}
              </div>
              <div class="chip-row" style="margin-top: 12px;">
                <button class="node-action primary" data-pending="小教已生成调整方案预演，等待教师确认。">${iconButtonLabel("查看调整方案", "arrow")}</button>
                <button class="node-action secondary" data-pending="小教已生成下节课准备推送预演，等待教师确认。">${iconButtonLabel("推送下节准备", "send")}</button>
              </div>
            </aside>
          </div>
        </div>
      `;
    }

    function renderFlexibleSemesterMapCanvas(view) {
      return `
        <div class="semester-plan">
          <aside class="unit-catalog">
            <div class="plan-panel-head">
              <span>单元课时目录</span>
              <span class="quiet-tag">展开全部</span>
            </div>
            <div class="unit-list">
              ${view.plan_units.map((unit) => `
                <section class="unit-group">
                  <div class="unit-group-head">
                    <span class="unit-name"><span class="unit-color-mark ${html(unit.tone)}"></span>${html(unit.title)}</span>
                    <span class="unit-hours">${html(unit.hours)}</span>
                  </div>
                  <div class="lesson-list">
                    ${unit.lessons.map(([code, title]) => `
                      <div class="lesson-line">
                        <span class="lesson-code">${html(code)}</span>
                        <span>${html(title)}</span>
                      </div>
                    `).join("")}
                  </div>
                </section>
              `).join("")}
            </div>
          </aside>
          <section class="week-plan-board">
            <div class="plan-panel-head">
              <span>周次计划（每周 1-2 课时）</span>
              <span class="quiet-tag">教师确认后应用</span>
            </div>
            <div class="week-plan-list">
              ${view.plan_weeks.map((week) => `
                <div class="week-row">
                  <div class="week-label">
                    <div>
                      <div class="week-name">${html(week.week)}</div>
                      <div class="week-date">${html(week.date)}</div>
                    </div>
                  </div>
                  <div class="week-slots">
                    ${week.lessons.map(([code, title, tone]) => `
                      <button class="plan-lesson ${html(tone)}" data-node="${html(`plan-${code}`)}" title="${html(title)}">
                        <span class="lesson-code">${html(code.startsWith("buffer") || code.startsWith("event") || code.startsWith("league") || code.startsWith("start") || code.startsWith("exam") || code === "final-show" ? "" : code)}</span>
                        <span>${html(title)}</span>
                      </button>
                    `).join("")}
                  </div>
                </div>
              `).join("")}
            </div>
          </section>
        </div>
      `;
    }

    function renderActiveViewMarkup(view) {
      if (view.id === "weekCalendar") return renderWeekCalendarCanvas(view);
      if (view.id === "prepNotebook") return renderPrepNotebookCanvas(view);
      if (view.id === "classProgressSchedule") return renderClassProgressScheduleCanvas(view);
      return renderFlexibleSemesterMapCanvas(view);
    }

    function commitCanvasRender(view) {
      const renderLayer = byId("renderLayer");
      renderLayer.innerHTML = renderActiveViewMarkup(view);
      window.requestAnimationFrame(() => {
        renderLayer.classList.remove("is-entering");
      });
      renderNegotiationPanel();
      renderStatusBar();
      const canvasStage = byId("canvasStage");
      canvasStage.scrollTop = model.view_scroll_positions?.[view.id] || 0;
      if (model.initial_scroll_target) {
        const targetId = model.initial_scroll_target;
        model.initial_scroll_target = "";
        window.requestAnimationFrame(() => {
          const target = byId(targetId);
          if (target) target.scrollIntoView({ block: "center" });
        });
      }
    }

    function renderPrepRoomCanvas(options = {}) {
      const view = getActiveView();
      renderCanvasHeader(view);
      const renderLayer = byId("renderLayer");
      if (!options.animate) {
        commitCanvasRender(view);
        return;
      }
      renderLayer.classList.add("is-fading");
      window.clearTimeout(model.render_transition_timer);
      model.render_transition_timer = window.setTimeout(() => {
        renderLayer.classList.remove("is-fading");
        renderLayer.classList.add("is-entering");
        commitCanvasRender(view);
      }, 150);
    }

    function applyScheduleAdapterPatch(payload) {
      if (!payload?.success) return false;
      const patch = payload.week_calendar_patch || {};
      const weekView = model.views.find((view) => view.id === "weekCalendar");
      if (!weekView) return false;
      if (patch.term) weekView.term = patch.term;
      if (patch.active_grade) weekView.active_grade = patch.active_grade;
      if (patch.source_badge) weekView.week_label = patch.source_badge;
      if (payload.source_kind) weekView.date_range = payload.source_kind === "feishu_live_readonly" ? "正式只读" : "快照只读";
      if (patch.slots) weekView.slots = patch.slots;
      if (patch.prep_items) weekView.prep_items = patch.prep_items;
      if (patch.alerts) weekView.alerts = patch.alerts;
      if (patch.package_summary) weekView.package_summary = patch.package_summary;
      model.schedule_adapter.source_kind = payload.source_kind || model.schedule_adapter.source_kind;
      model.schedule_adapter.status = payload.source_kind === "feishu_live_readonly" ? "已读取正式课表，只读展示" : "已读取课表快照，只读展示";
      model.safety.api_connected = true;
      return true;
    }

    function bindLiveScheduleAdapter() {
      const adapter = model.schedule_adapter || {};
      if (adapter.fetch_attempted || !adapter.endpoint || !window.fetch) return;
      adapter.fetch_attempted = true;
      fetch(adapter.endpoint, { method: "GET" })
        .then((response) => (response.ok ? response.json() : null))
        .then((payload) => {
          if (!applyScheduleAdapterPatch(payload)) return;
          renderNegotiationPanel();
          if (model.active_view === "weekCalendar") {
            renderPrepRoomCanvas();
          }
        })
        .catch(() => {
          adapter.status = "本地后端未连接，继续使用内置快照";
        });
    }

    function toolShortLabel(tool) {
      const map = {
        textbook: "教材",
        unit: "单元",
        split: "拆课",
        weekly: "周历",
        reschedule: "重排",
        flow: "流程",
        worksheet: "学习单",
        search: "检索",
        xiaomei: "小美",
        xiaoping: "小评",
        xiaoguan: "小管"
      };
      return map[tool.id] || tool.title.slice(0, 3);
    }

    function renderToolRail() {
      const rail = byId("toolRail");
      if (!rail) return;
      rail.innerHTML = model.tools.map((tool, index) => `
        ${index === 5 ? `<div class="tool-separator" aria-hidden="true"></div>` : ""}
        <button class="tool-btn" data-tool="${html(tool.id)}" data-label="${html(tool.title)}" title="${html(tool.title)}" aria-label="${html(tool.title)}">
          ${iconButtonLabel(tool.title, iconForTool(tool.id))}
        </button>
      `).join("");
    }

    function placeInspectorNearPointer(inspector, pointerEvent) {
      if (!pointerEvent) return;
      const stage = byId("canvasStage");
      const stageRect = stage.getBoundingClientRect();
      const gap = 14;
      const fallbackWidth = 340;
      const fallbackHeight = 360;
      const width = inspector.offsetWidth || Math.min(fallbackWidth, Math.max(260, stageRect.width - 36));
      const height = inspector.offsetHeight || fallbackHeight;
      const minLeft = 18;
      const minTop = 18;
      const maxLeft = Math.max(minLeft, stage.clientWidth - width - 18);
      const maxTop = Math.max(minTop, stage.clientHeight - height - 18);
      const rawLeft = pointerEvent.clientX - stageRect.left + stage.scrollLeft + gap;
      const rawTop = pointerEvent.clientY - stageRect.top + stage.scrollTop + gap;
      const left = Math.min(Math.max(rawLeft, minLeft), maxLeft);
      const top = Math.min(Math.max(rawTop, minTop), maxTop);
      inspector.style.setProperty("--inspector-left", `${Math.round(left)}px`);
      inspector.style.setProperty("--inspector-top", `${Math.round(top)}px`);
    }

    function openInspector(targetId, options = {}) {
      const inspector = byId("inspector");
      const tool = model.tools.find((item) => item.id === targetId);
      const detail = tool
        ? {
            type: "工具详情",
            title: tool.title,
            fields: [["用途", tool.desc], ["边界", "只生成预演，不触发正式调用"], ["工具ID", tool.id]],
            actions: tool.actions
          }
        : getNodeDetail(targetId);

      if (!detail) {
        inspector.classList.add("hidden");
        return;
      }

      if (!tool) {
        model.selected_node_id = targetId;
      }

      inspector.innerHTML = `
        <div class="inspector-head">
          <div>
            <div class="inspector-kicker">${html(detail.type)}</div>
            <div class="inspector-title">${html(detail.title)}</div>
          </div>
          <button class="icon-close" id="closeInspectorBtn" aria-label="关闭检查器">×</button>
        </div>
        <div class="inspector-body">
          <div class="field-grid">
            ${detail.fields.map(([label, value]) => `
              <div class="field-row">
                <div class="field-label">${html(label)}</div>
                <div class="field-value">${html(value)}</div>
              </div>
            `).join("")}
          </div>
          <div>
            <div class="section-title"><span>可预演动作</span><span class="quiet-tag">需教师确认</span></div>
            <div class="inspector-actions">
              ${detail.actions.map((action) => `<button class="node-action icon-only inspector-action" title="${html(action)}" aria-label="${html(action)}" data-pending="小教已生成「${html(action)}」预演，等待教师确认。">${iconButtonLabel(action, iconForAction(action))}</button>`).join("")}
            </div>
          </div>
          <div class="pending-panel" id="inspectorPending">
            ${html(model.pending_changes[0]?.text || "暂无待确认预演。")}
          </div>
        </div>
      `;
      inspector.classList.remove("hidden");
      placeInspectorNearPointer(inspector, options.event);

      document.querySelectorAll(".canvas-node").forEach((node) => {
        node.classList.toggle("selected", node.dataset.node === model.selected_node_id);
      });
      document.querySelectorAll(".tool-btn").forEach((button) => {
        button.classList.toggle("active", button.dataset.tool === targetId);
      });

      if (!options.silent) {
        showToast(tool ? `已打开工具：${detail.title}` : `已选中：${detail.title}`);
      }
    }

    function addPendingChange(text, source = "画布预演") {
      const item = {
        id: `pending-${Date.now()}`,
        text,
        source,
        applied: false
      };
      model.pending_changes.unshift(item);
      renderStatusBar();
      const pending = byId("inspectorPending");
      if (pending) pending.textContent = item.text;
      showToast(text);
    }

    function prepNotebookView() {
      return model.views.find((view) => view.id === "prepNotebook");
    }

    function clearReasoningTraceTimers() {
      (model.reasoning_trace_timers || []).forEach((timer) => window.clearTimeout(timer));
      model.reasoning_trace_timers = [];
    }

    function applyPrepReasoningCandidate(prepView) {
      const lesson = prepView?.current_lesson;
      if (!prepView || !lesson) return;
      prepView.prep_notebook_mode = "edit";
      prepView.active_edit_target = { section_id: "teaching_process", step_id: "explore", label: "教学过程 · 探究环节" };
      prepView.expanded_intent_steps = Array.from(new Set([...(prepView.expanded_intent_steps || []), "explore"]));
      const analysis = (lesson.sections || []).find((section) => section.id === "analysis");
      if (analysis) {
        analysis.candidate = "候选：增加一条学情判断，学生可能能分辨颜色冷暖，但还需要借助色卡和生活物品把感受说具体。";
      }
      const explore = (lesson.process_steps || []).find((step) => step.id === "explore");
      if (explore) {
        explore.candidate = "候选：探究环节加入色卡和生活物品分组，让学生先按感受分类，再选择一张色卡说出理由。";
      }
      lesson.status = "新增候选待确认";
    }

    function startPrepReasoningTrace(text) {
      const prepView = prepNotebookView();
      if (!prepView) return;
      clearReasoningTraceTimers();
      const trace = prepView.reasoning_trace || {};
      trace.status = "running";
      trace.active_index = 0;
      trace.teacher_input = text;
      trace.result = "";
      prepView.reasoning_trace = trace;
      model.active_view = "prepNotebook";
      renderPrepRoomCanvas();
      showToast("小教开始同步思考");
      const stages = trace.stages || [];
      stages.forEach((stage, index) => {
        const timer = window.setTimeout(() => {
          trace.active_index = index;
          trace.status = "running";
          renderPrepRoomCanvas();
        }, index * 650);
        model.reasoning_trace_timers.push(timer);
      });
      const doneTimer = window.setTimeout(() => {
        trace.active_index = stages.length - 1;
        trace.status = "done";
        trace.result = "我先整理成两处候选：探究环节加色卡分组，学习单加感受记录格。等你确认。";
        applyPrepReasoningCandidate(prepView);
        addPendingChange(trace.result, "备课本编辑");
        renderPrepRoomCanvas();
      }, Math.max(1, stages.length) * 650 + 260);
      model.reasoning_trace_timers.push(doneTimer);
    }

    function renderFlowSteps() {
      return `
        <div class="flow-steps" aria-label="课包流转步骤">
          ${model.flow_steps.map((step, index) => `
            <span class="flow-step ${step.current ? "current" : ""}">
              <span class="flow-dot" aria-hidden="true"></span>
              <span>${html(step.label)}</span>
            </span>
            ${index < model.flow_steps.length - 1 ? `<span class="flow-sep" aria-hidden="true">›</span>` : ""}
          `).join("")}
        </div>
      `;
    }

    function renderStatusBar() {
      const latest = model.pending_changes[0];
      byId("statusMain").innerHTML = `
        ${renderFlowSteps()}
        <span class="status-text">${html(latest ? latest.text : "暂无待确认预演。")}</span>
      `;
      byId("statusCount").textContent = `${model.pending_changes.length} 项`;
    }

    let toastTimer = null;
    function showToast(text) {
      const toast = byId("toast");
      toast.textContent = text;
      toast.classList.add("show");
      window.clearTimeout(toastTimer);
      toastTimer = window.setTimeout(() => toast.classList.remove("show"), 1800);
    }

    function rememberActiveScroll() {
      const canvasStage = byId("canvasStage");
      if (!canvasStage) return;
      model.view_scroll_positions[model.active_view] = canvasStage.scrollTop;
    }

    function hideHoverNote() {
      const note = byId("nbHoverNote");
      if (!note) return;
      note.hidden = true;
      note.innerHTML = "";
    }

    function showHoverNote(text, event) {
      const note = byId("nbHoverNote");
      if (!note || !text) return;
      note.innerHTML = `<strong>小教判断</strong>${html(text)}`;
      const gap = 16;
      const width = 320;
      const left = Math.min(event.clientX + gap, window.innerWidth - width - 12);
      const top = Math.min(event.clientY + gap, window.innerHeight - 120);
      note.style.left = `${Math.max(12, left)}px`;
      note.style.top = `${Math.max(12, top)}px`;
      note.hidden = false;
    }

    function selectPrepParagraph(paragraphId) {
      const prepView = model.views.find((view) => view.id === "prepNotebook");
      if (!prepView || !paragraphId) return;
      rememberActiveScroll();
      prepView.selected_paragraph_id = prepView.selected_paragraph_id === paragraphId ? "" : paragraphId;
      renderPrepRoomCanvas();
    }

    function clearPrepParagraphSelection() {
      const prepView = model.views.find((view) => view.id === "prepNotebook");
      if (!prepView?.selected_paragraph_id) return false;
      rememberActiveScroll();
      prepView.selected_paragraph_id = "";
      renderPrepRoomCanvas();
      return true;
    }

    function setPrepNotebookMode(mode, options = {}) {
      const prepView = model.views.find((view) => view.id === "prepNotebook");
      if (!prepView) return;
      rememberActiveScroll();
      prepView.prep_notebook_mode = mode === "edit" ? "edit" : "view";
      if (options.stepId) {
        const step = processStepById(prepView, options.stepId);
        prepView.active_edit_target = {
          section_id: "teaching_process",
          step_id: options.stepId,
          label: `教学过程 · ${step?.name || "当前环节"}环节`
        };
        prepView.expanded_intent_steps = Array.from(new Set([...(prepView.expanded_intent_steps || []), options.stepId]));
      } else if (options.sectionId) {
        const section = (prepView.current_lesson.sections || []).find((item) => item.id === options.sectionId);
        prepView.active_edit_target = {
          section_id: options.sectionId,
          step_id: "",
          label: section?.title || "当前段落"
        };
      }
      renderPrepRoomCanvas();
      showToast(prepView.prep_notebook_mode === "edit" ? `已进入编辑：${prepActiveTarget(prepView).label}` : "已回到查看状态");
    }

    function setLessonDesignMode(modeId) {
      const prepView = model.views.find((view) => view.id === "prepNotebook");
      if (!prepView) return;
      const modes = prepView.lesson_design_modes || [];
      const selected = modes.find((item) => item.id === modeId);
      if (!selected) return;
      rememberActiveScroll();
      prepView.lesson_design_mode = selected.id;
      renderPrepRoomCanvas();
      showToast(`这节课先按“${selected.label}”准备`);
    }

    function handlePrepEditTarget(value) {
      const [kind, id] = String(value || "").split(":");
      if (!id) return;
      if (kind === "process") {
        setPrepNotebookMode("edit", { stepId: id });
      } else {
        setPrepNotebookMode("edit", { sectionId: id });
      }
    }

    function togglePrepIntent(stepId) {
      const prepView = model.views.find((view) => view.id === "prepNotebook");
      if (!prepView) return;
      rememberActiveScroll();
      const list = new Set(prepView.expanded_intent_steps || []);
      if (list.has(stepId)) {
        list.delete(stepId);
      } else {
        list.add(stepId);
      }
      prepView.expanded_intent_steps = Array.from(list);
      renderPrepRoomCanvas();
    }

    function selectView(viewId) {
      const canvasStage = byId("canvasStage");
      model.view_scroll_positions[model.active_view] = canvasStage.scrollTop;
      model.active_view = viewId;
      const view = getActiveView();
      const firstPlanLesson = view.plan_weeks?.[0]?.lessons?.[0]?.[0];
      const firstCpsWeek = view.week_axis?.[0]?.id;
      const firstCpsClass = view.class_headers?.[0]?.id;
      const firstCpsNode = firstCpsWeek && firstCpsClass ? `cps-${firstCpsWeek}-${firstCpsClass}-1` : "";
      const firstWcNode = Object.values(view.slots || {}).flat()[0]?.id || "";
      const firstNode = view.active_node || firstWcNode || view.nodes?.[0]?.id || view.weeks?.[0]?.id || firstCpsNode || (firstPlanLesson ? `plan-${firstPlanLesson}` : "") || view.lanes?.[0]?.blocks?.[0]?.id;
      model.selected_node_id = firstNode || model.selected_node_id;
      byId("inspector").classList.add("hidden");
      renderPrepRoomCanvas({ animate: true });
      showToast(`已切换到${view.label}画布`);
    }

    function bindEvents() {
      document.body.addEventListener("click", (event) => {
        const viewButton = event.target.closest("[data-view]");
        if (viewButton) {
          selectView(viewButton.dataset.view);
          return;
        }

        const prepModeButton = event.target.closest("[data-nb-mode]");
        if (prepModeButton) {
          setPrepNotebookMode(prepModeButton.dataset.nbMode);
          return;
        }

        const lessonModeButton = event.target.closest("[data-lesson-mode]");
        if (lessonModeButton) {
          setLessonDesignMode(lessonModeButton.dataset.lessonMode);
          return;
        }

        const prepEditTarget = event.target.closest("[data-edit-target]");
        if (prepEditTarget) {
          handlePrepEditTarget(prepEditTarget.dataset.editTarget);
          return;
        }

        const paragraphTarget = event.target.closest("[data-select-paragraph]");
        if (paragraphTarget) {
          selectPrepParagraph(paragraphTarget.dataset.selectParagraph);
          return;
        }

        const prepIntentButton = event.target.closest("[data-intent-step]");
        if (prepIntentButton) {
          togglePrepIntent(prepIntentButton.dataset.intentStep);
          return;
        }

        const spaceButton = event.target.closest(".space-btn");
        if (spaceButton) {
          event.preventDefault();
          showToast(`进入${spaceButton.getAttribute("aria-label") || "学校空间"}仍为预览入口`);
          return;
        }

        const chatFill = event.target.closest("[data-chat-fill]");
        if (chatFill) {
          const input = byId("chatInput");
          input.value = chatFill.dataset.chatFill;
          input.focus();
          return;
        }

        if (event.target.closest("#chatUploadBtn")) {
          byId("chatUploadInput").click();
          return;
        }

        if (event.target.closest("#chatVoiceBtn")) {
          addPendingChange("小教已打开语音意图入口预演，等待教师继续输入。", "小教意图入口");
          return;
        }

        if (event.target.closest("#chatSendBtn")) {
          submitChatMessage();
          return;
        }

        const pendingSource = event.target.closest("[data-pending]");
        if (pendingSource) {
          addPendingChange(pendingSource.dataset.pending);
          return;
        }

        const node = event.target.closest("[data-node]");
        if (node) {
          openInspector(node.dataset.node, { event });
          return;
        }

        const tool = event.target.closest("[data-tool]");
        if (tool) {
          openInspector(tool.dataset.tool, { event });
          return;
        }

        const intent = event.target.closest("[data-intent]");
        if (intent) {
          const input = byId("chatInput");
          input.value = input.value ? `${input.value}\n${intent.dataset.intent}` : intent.dataset.intent;
          input.focus();
          return;
        }

        const current = event.target.closest("[data-action='open-current']");
        if (current) {
          openInspector(model.selected_node_id, { event });
          return;
        }

        if (event.target.id === "closeInspectorBtn") {
          byId("inspector").classList.add("hidden");
          return;
        }

        if (model.active_view === "prepNotebook" && !event.target.closest("[data-select-paragraph], [data-inline-note], button, .nb-hover-note-popover, .nb-edit-panel, .nb-drawer")) {
          if (clearPrepParagraphSelection()) return;
        }
      });

      document.body.addEventListener("mousemove", (event) => {
        const paragraph = event.target.closest("[data-hover-note]");
        if (!paragraph || model.active_view !== "prepNotebook") {
          hideHoverNote();
          return;
        }
        showHoverNote(paragraph.dataset.hoverNote, event);
      });

      document.body.addEventListener("mouseleave", hideHoverNote);

      byId("chatInput").addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          submitChatMessage();
        }
      });

      byId("chatUploadInput").addEventListener("change", (event) => {
        const files = Array.from(event.target.files || []);
        if (!files.length) return;
        const names = files.slice(0, 3).map((file) => file.name).join("、");
        const more = files.length > 3 ? ` 等${files.length}个文件` : "";
        addPendingChange(`小教已接收资料「${names}${more}」的本地挂载预演，未上传到服务器。`, "资料入口");
        event.target.value = "";
      });

      document.body.addEventListener("keydown", (event) => {
        if (event.key !== "Enter" && event.key !== " ") return;
        const node = event.target.closest("[data-node]");
        if (node) {
          event.preventDefault();
          openInspector(node.dataset.node);
        }
      });
    }

    function submitChatMessage() {
      const input = byId("chatInput");
      const text = input.value.trim();
      if (!text) {
        showToast("先对小教说一句");
        input.focus();
        return;
      }
      model.negotiation.input_value = text;
      if (model.active_view === "prepNotebook") {
        startPrepReasoningTrace(text);
      } else {
        addPendingChange(`小教已收到意图：「${text}」，正在生成影响范围预演。`, "小教意图入口");
      }
      input.value = "";
    }

    function initPrepRoomRenderCanvas() {
      applyInitialViewFromHash();
      hydrateShellIcons();
      renderToolRail();
      renderNegotiationPanel();
      renderPrepRoomCanvas();
      bindEvents();
      bindLiveScheduleAdapter();
    }

    window.renderWeekCalendarCanvas = renderWeekCalendarCanvas;
    window.renderPrepNotebookCanvas = renderPrepNotebookCanvas;
    window.renderClassProgressScheduleCanvas = renderClassProgressScheduleCanvas;
    window.renderFlexibleSemesterMapCanvas = renderFlexibleSemesterMapCanvas;
    window.renderToolRail = renderToolRail;
    window.openInspector = openInspector;
    window.addPendingChange = addPendingChange;
    window.renderPrepRoomCanvas = renderPrepRoomCanvas;

    initPrepRoomRenderCanvas();
  