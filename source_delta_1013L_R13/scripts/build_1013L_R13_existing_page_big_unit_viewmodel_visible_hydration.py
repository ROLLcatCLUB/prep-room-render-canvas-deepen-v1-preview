from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R11_DIR = BASE / "1013L_R11_existing_page_readonly_viewmodel_static_hydration_apply"
R13_DIR = BASE / "1013L_R13_existing_page_big_unit_viewmodel_visible_hydration"
SOURCE_DELTA = BASE / "source_delta_1013L_R13"
R11_HTML = R11_DIR / "prep_room_render_canvas_deepen_v1_1013L_R11_static_hydration_apply.html"
R11_PAYLOAD = R11_DIR / "readonly_viewmodel_static_hydration_payload_1013L_R11.json"


STAGE = "1013L_R13_EXISTING_PAGE_BIG_UNIT_VIEWMODEL_VISIBLE_HYDRATION"
FINAL_STATUS = "PASS_1013L_R13_EXISTING_PAGE_BIG_UNIT_VIEWMODEL_VISIBLE_HYDRATION"
NEXT_STAGE = "1013L_R14_EXISTING_PAGE_BIG_UNIT_VIEWMODEL_VISUAL_SMOKE"


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "visible_hydration_apply_only": True,
        "existing_page_reused": True,
        "new_visible_page_created": False,
        "new_shell_standard_created": False,
        "runtime_connected": False,
        "real_fetch_performed": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
        "formal_frontend_binding_allowed": False,
    }


def find_browser() -> Path:
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No Edge/Chrome browser found for R13 hydration smoke.")


def chunk_summary(chunk: dict) -> str:
    paragraphs = chunk.get("paragraphs") or []
    if paragraphs:
        return paragraphs[0]
    return chunk.get("summary") or ""


def r13_payload() -> dict:
    r11_payload = read_json(R11_PAYLOAD)
    big_unit_response = r11_payload.get("big_unit") or {}
    big_unit_viewmodel = big_unit_response.get("viewmodel") or {}
    section_chunks = big_unit_viewmodel.get("section_chunks") or []
    side_reference = big_unit_viewmodel.get("side_reference") or {}
    side_notes = big_unit_viewmodel.get("side_notes") or side_reference.get("items") or []
    material_prompt = big_unit_viewmodel.get("material_prompt") or {}
    return {
        "hydration_id": "existing_page_big_unit_viewmodel_visible_hydration_1013L_R13",
        "stage": STAGE,
        "source_html": rel(R11_HTML),
        "source_payload": rel(R11_PAYLOAD),
        "big_unit_viewmodel_id": big_unit_viewmodel.get("viewmodel_id"),
        "unit_title": big_unit_viewmodel.get("unit_title") or big_unit_viewmodel.get("header", {}).get("title"),
        "header": big_unit_viewmodel.get("header") or {},
        "status_strip": big_unit_viewmodel.get("status_strip") or {},
        "material_prompt": material_prompt,
        "section_chunks": section_chunks,
        "side_notes": side_notes,
        "summary": {
            "chunk_count": len(section_chunks),
            "side_note_count": len(side_notes),
            "material_action_count": len(material_prompt.get("actions") or []),
            "first_chunk_label": section_chunks[0].get("teacher_label") if section_chunks else "",
            "first_chunk_summary": chunk_summary(section_chunks[0]) if section_chunks else "",
        },
        "hydration_policy": {
            "reuse_existing_page_functions": True,
            "override_big_unit_render_surface_only": True,
            "left_tree_big_unit_entry_preserved": True,
            "right_resource_rail_preserved_as_readonly_reference": True,
            "route_query_for_review": "?r13=bigUnit",
            "no_new_shell": True,
        },
        "boundary": boundary(),
    }


def hydration_script(payload: dict) -> str:
    json_payload = json.dumps(payload, ensure_ascii=False, indent=2)
    js_payload = json.dumps(payload, ensure_ascii=False)
    return f"""
<style id="main-shell-big-unit-visible-hydration-style-1013L-R13">
  [data-1013l-r13-big-unit-hydrated="true"] .nb-doc[data-1013l-r13-doc="true"] {{
    max-width: 920px;
  }}
  [data-1013l-r13-big-unit-hydrated="true"] .nb-doc-section[data-1013l-r13-chunk="true"] {{
    padding: 14px 6px 16px;
  }}
  [data-1013l-r13-big-unit-hydrated="true"] .nb-doc-section[data-1013l-r13-chunk="true"] + .nb-doc-section[data-1013l-r13-chunk="true"] {{
    border-top: 1px solid rgba(41, 117, 99, .16);
  }}
  [data-1013l-r13-big-unit-hydrated="true"] .nb-doc-section[data-1013l-r13-chunk="true"] p,
  [data-1013l-r13-big-unit-hydrated="true"] .nb-doc-section[data-1013l-r13-chunk="true"] li {{
    line-height: 1.9;
  }}
  .r13-source-chip {{
    display: inline-flex;
    align-items: center;
    border-radius: 999px;
    padding: 2px 8px;
    margin-right: 6px;
    border: 1px solid rgba(41, 117, 99, .18);
    background: rgba(232, 247, 241, .62);
    color: #287260;
    font-size: 12px;
  }}
</style>
<script id="main-shell-big-unit-visible-hydration-payload-1013L-R13" type="application/json">
{json_payload}
</script>
<script id="main-shell-big-unit-visible-hydration-1013L-R13">
(function () {{
  var payload = {js_payload};
  var chunks = payload.section_chunks || [];
  var sideNotes = payload.side_notes || [];

  function escapeHtml(value) {{
    if (typeof window.html === "function") return window.html(value == null ? "" : String(value));
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }}

  function cnNumber(index) {{
    return ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二"][index] || String(index + 1);
  }}

  function materialPrompt() {{
    var prompt = payload.material_prompt || {{}};
    var actions = prompt.actions || ["上传教材目录", "上传单元页", "补充课时安排", "先按临时预览"];
    return '<section class="nb-material-front-prompt" aria-label="资料补充提示" data-1013l-r13-material-prompt="true">' +
      '<div class="nb-material-front-copy">' +
        '<div class="nb-material-front-title"><span class="nb-material-icon">!</span><span>还缺教材材料</span></div>' +
        '<p class="nb-material-front-note">' + escapeHtml(prompt.text || "补齐教材目录、单元页或课时安排后，小教再校准大单元设计。") + '</p>' +
      '</div>' +
      '<div class="nb-material-front-actions">' +
        actions.map(function (label) {{
          return '<button class="node-action secondary" type="button" data-pending="资料入口占位，当前只做静态预览。">' + escapeHtml(label) + '</button>';
        }}).join("") +
      '</div>' +
    '</section>';
  }}

  function renderChunk(chunk, index) {{
    var paragraphs = chunk.paragraphs || (chunk.summary ? [chunk.summary] : []);
    var badges = chunk.status_badges || [];
    return '<section class="nb-doc-section" id="chunk-' + escapeHtml(chunk.chunk_id || ("r13-" + index)) + '" data-1013l-r13-chunk="true" data-chunk-id="' + escapeHtml(chunk.chunk_id || "") + '">' +
      '<div class="nb-doc-section-head">' +
        '<div class="nb-doc-title">' + cnNumber(index) + '、' + escapeHtml(chunk.teacher_label || ("章节 " + (index + 1))) + '</div>' +
        '<button class="node-action secondary" type="button" data-pending="说明和依据在右侧折叠区。">查看说明</button>' +
      '</div>' +
      paragraphs.map(function (paragraph) {{ return '<p>' + escapeHtml(paragraph) + '</p>'; }}).join("") +
      (badges.length ? '<p>' + badges.map(function (badge) {{ return '<span class="quiet-tag">' + escapeHtml(badge) + '</span>'; }}).join(" ") + '</p>' : '') +
    '</section>';
  }}

  function statusLights() {{
    var lights = (payload.header || {{}}).status_lights || [
      {{ label: "预览", tone: "green" }},
      {{ label: "资料待补", tone: "yellow" }},
      {{ label: "教师确认前不生效", tone: "red" }}
    ];
    var toneMap = {{ green: "green", yellow: "amber", red: "red", amber: "amber" }};
    return lights.map(function (light) {{
      var tone = toneMap[light.tone] || "green";
      return '<span class="r6o-r1-status-light"><span class="r6o-r1-dot ' + tone + '"></span>' + escapeHtml(light.label) + '</span>';
    }}).join("");
  }}

  function renderBigUnitFromViewModel(view) {{
    return '<section class="nb-workspace" aria-label="第一单元多变的色彩大单元设计" data-1013l-r13-big-unit-surface="true">' +
      '<div class="nb-hero">' +
        '<div><div class="nb-kicker">' + escapeHtml((payload.header || {{}}).eyebrow || "大单元设计") + '</div>' +
        '<div class="nb-title">' + escapeHtml(payload.unit_title || "第一单元《多变的色彩》") + '</div></div>' +
        '<div class="nb-hero-actions">' +
          '<button class="node-action primary" data-pending="已保留为预览候选，教师确认前不写入正式备课本。">确认到预览</button>' +
          '<button class="node-action secondary" data-clear-big-unit="true">回到当前课时</button>' +
        '</div>' +
      '</div>' +
      '<div class="nb-state-bar" data-1013l-r13-state-bar="true">' +
        '<div class="nb-state-main"><span class="r6o-r1-status-pill">查看状态</span><span class="r6o-r1-status-pill">可预览</span>' + statusLights() + '</div>' +
        '<div class="nb-mode-toggle" aria-label="大单元状态"><button class="nb-mode-btn active" type="button">查看</button><button class="nb-mode-btn" type="button" data-pending="大单元编辑后续接弹窗，当前只做只读渲染。">编辑</button></div>' +
      '</div>' +
      materialPrompt() +
      '<div class="nb-doc" data-r6o-field-render-doc="true" data-1013k-readonly-render-doc="true" data-1013l-r13-doc="true" data-binding-mode="existing_page_big_unit_hydrated">' +
        '<div class="nb-doc-body-surface">' +
          chunks.map(renderChunk).join("") +
        '</div>' +
      '</div>' +
    '</section>';
  }}

  function renderRightRailFromViewModel(view) {{
    return '<aside class="nb-right-rail" aria-label="大单元资源库与依据">' +
      '<section class="nb-drawer r6p-resource-rail" data-r6p-right-resource-toolbar="true" data-1013l-r13-right-rail="true">' +
        '<div class="nb-drawer-title"><span>资源库与依据</span><button class="node-action secondary" type="button">按需打开</button></div>' +
        '<div class="r6p-tool-strip" aria-label="大单元资料入口">' +
          '<button class="node-action secondary r6p-tool" type="button">教材资料</button>' +
          '<button class="node-action secondary r6p-tool" type="button">课标依据</button>' +
          '<button class="node-action secondary r6p-tool" type="button">学习单</button>' +
          '<button class="node-action secondary r6p-tool" type="button">评价句式</button>' +
        '</div>' +
        '<div class="r6p-resource-item"><strong>当前预览</strong><p>小教已整理 ' + chunks.length + ' 个单元设计段落，教师确认前不写入正式备课本。</p></div>' +
        '<details class="r6p-resource-item"><summary>只读依据和风险提醒</summary>' +
          sideNotes.slice(0, 10).map(function (note) {{
            return '<p><span class="r13-source-chip">' + escapeHtml(note.teacher_label || "依据") + '</span>' + escapeHtml(note.risk_note || "教师确认前不生效。") + '</p>';
          }}).join("") +
        '</details>' +
      '</section>' +
    '</aside>';
  }}

  function applyBigUnitHydration() {{
    if (!chunks.length) return false;
    window.__SHIWEI_R13_BIG_UNIT_HYDRATION__ = payload;
    document.documentElement.setAttribute("data-1013l-r13-big-unit-hydrated", "true");
    document.documentElement.setAttribute("data-1013l-r13-big-unit-chunks", String(chunks.length));

    if (typeof renderBigUnitPrepSurface === "function") {{
      renderBigUnitPrepSurface = renderBigUnitFromViewModel;
      window.renderBigUnitPrepSurface = renderBigUnitFromViewModel;
    }}
    if (typeof renderBigUnitPrepRightPanel === "function") {{
      renderBigUnitPrepRightPanel = renderRightRailFromViewModel;
      window.renderBigUnitPrepRightPanel = renderRightRailFromViewModel;
    }}

    var query = new URLSearchParams(window.location.search || "");
    var wantsBigUnit = query.get("r13") === "bigUnit" || query.get("view") === "bigUnit" || window.location.hash === "#bigUnitDesign";
    if (wantsBigUnit && typeof openBigUnitPrepSurface === "function") {{
      openBigUnitPrepSurface("nb-unit-color", {{ skipRemember: true }});
      document.documentElement.setAttribute("data-1013l-r13-state", "big_unit_visible_hydration");
    }}
    return true;
  }}

  if (document.readyState === "loading") {{
    document.addEventListener("DOMContentLoaded", function () {{ window.setTimeout(applyBigUnitHydration, 80); }});
  }} else {{
    window.setTimeout(applyBigUnitHydration, 80);
  }}
}}());
</script>
"""


def inject_hydration(html_text: str, payload: dict) -> str:
    marker = "main-shell-big-unit-visible-hydration-1013L-R13"
    if marker in html_text:
        return html_text
    if "</body>" not in html_text:
        raise RuntimeError("source html has no closing body tag")
    return html_text.replace("</body>", hydration_script(payload) + "\n</body>")


def dump_dom(browser: Path, url: str) -> str:
    with tempfile.TemporaryDirectory(prefix="shiwei-r13-browser-") as temp_dir:
        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--disable-background-networking",
            "--allow-file-access-from-files",
            "--virtual-time-budget=6000",
            f"--user-data-dir={temp_dir}",
            "--dump-dom",
            url,
        ]
        completed = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60,
        )
        return completed.stdout


def run_smoke(browser: Path, html_path: Path) -> dict:
    base_url = html_path.resolve().as_uri()
    cases = [
        {
            "case_id": "normal_shell_not_forced_to_big_unit",
            "suffix": "?r13test=normal",
            "required_markers": [
                'data-1013l-r13-big-unit-hydrated="true"',
                "ai-tool-strip",
                "courseware_screen_seed_03_color_comparison_1013K_R25",
            ],
        },
        {
            "case_id": "big_unit_route_visible_chunks",
            "suffix": "?r13=bigUnit",
            "required_markers": [
                'data-1013l-r13-big-unit-hydrated="true"',
                'data-1013l-r13-big-unit-surface="true"',
                "第一单元《多变的色彩》",
                "课标依据",
                "核心素养",
                "课时任务链",
                "缺教材目录、单元页或课时安排",
            ],
        },
        {
            "case_id": "big_unit_hash_route_visible_chunks",
            "suffix": "#bigUnitDesign",
            "required_markers": [
                'data-1013l-r13-state="big_unit_visible_hydration"',
                "材料与支架",
                "评价证据",
            ],
        },
    ]
    results = []
    for case in cases:
        dom = dump_dom(browser, base_url + case["suffix"])
        missing = [marker for marker in case["required_markers"] if marker not in dom]
        results.append(
            {
                "case_id": case["case_id"],
                "expected_markers": case["required_markers"],
                "missing_markers": missing,
                "pass": missing == [],
            }
        )
    return {
        "smoke_id": "big_unit_visible_hydration_browser_smoke_1013L_R13",
        "stage": STAGE,
        "case_count": len(results),
        "cases": results,
        "big_unit_visible_hydration_smoke_pass": all(case["pass"] for case in results),
        "boundary": boundary(),
    }


def copy_source_delta() -> None:
    (SOURCE_DELTA / "scripts").mkdir(parents=True, exist_ok=True)
    for name in [
        "build_1013L_R13_existing_page_big_unit_viewmodel_visible_hydration.py",
        "validate_1013L_R13_existing_page_big_unit_viewmodel_visible_hydration.py",
    ]:
        shutil.copy2(ROOT / "scripts" / name, SOURCE_DELTA / "scripts" / name)


def main() -> None:
    payload = r13_payload()
    source_html = R11_HTML.read_text(encoding="utf-8-sig")
    html_path = R13_DIR / "prep_room_render_canvas_deepen_v1_1013L_R13_big_unit_visible_hydration.html"
    write_text(html_path, inject_hydration(source_html, payload))
    write_json(R13_DIR / "big_unit_visible_hydration_payload_1013L_R13.json", payload)
    smoke = run_smoke(find_browser(), html_path)
    write_json(R13_DIR / "big_unit_visible_hydration_browser_smoke_1013L_R13.json", smoke)
    result = {
        "stage": STAGE,
        "final_status": FINAL_STATUS if smoke["big_unit_visible_hydration_smoke_pass"] else f"FAIL_{STAGE}",
        "source_stage": "1013L_R11_EXISTING_PAGE_READONLY_VIEWMODEL_STATIC_HYDRATION_APPLY",
        "source_html": rel(R11_HTML),
        "hydrated_html": rel(html_path),
        "payload": rel(R13_DIR / "big_unit_visible_hydration_payload_1013L_R13.json"),
        "big_unit_chunk_count": payload["summary"]["chunk_count"],
        "side_note_count": payload["summary"]["side_note_count"],
        "existing_page_reused": True,
        "left_tree_big_unit_entry_preserved": True,
        "big_unit_viewmodel_visible_hydrated": True,
        "render_big_unit_surface_overridden_from_viewmodel": True,
        "right_resource_rail_preserved": True,
        "new_visible_page_created": False,
        "new_shell_standard_created": False,
        "runtime_connected": False,
        "real_fetch_performed": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
        "github_uploaded": False,
        "browser_smoke_pass": smoke["big_unit_visible_hydration_smoke_pass"],
        "smoke_case_count": smoke["case_count"],
        "next_stage": NEXT_STAGE,
        "boundary": boundary(),
    }
    write_json(R13_DIR / "1013L_R13_result.json", result)
    report = """# 1013L R13 Existing Page Big Unit ViewModel Visible Hydration

R13 continues from the existing R11 main-shell page. It does not create a new visible shell.

The stage overrides only the existing big-unit render surface and right reference rail so the big-unit page reads from the embedded readonly ViewModel chunks. The left notebook directory entry and current prep-room shell remain the same.

Review route for this static copy:

`?r13=bigUnit`

Boundary remains static-only: no runtime fetch, no provider/model, no database/memory/Feishu write, no formal apply, and no main project push.
"""
    write_text(R13_DIR / "1013L_R13_report.md", report)
    copy_source_delta()
    print(R13_DIR)


if __name__ == "__main__":
    main()
