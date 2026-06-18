from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6I_BIG_UNIT_PREP_HTML_FIXTURE_AFTER_REVIEW_APPROVAL"
FINAL_STATUS = "PASS_1013I_R6I_BIG_UNIT_PREP_HTML_FIXTURE_AFTER_REVIEW_APPROVAL"
INHERITS_FROM = "1013I_R6H_BIG_UNIT_PREP_PAGE_FIXTURE_REVIEW_BEFORE_HTML"
R6H_PASS_STATUS = "PASS_1013I_R6H_BIG_UNIT_PREP_PAGE_FIXTURE_REVIEW_BEFORE_HTML"
NEXT_STAGE = "1013I_R6J_BIG_UNIT_PREP_HTML_FIXTURE_VISUAL_REVIEW_GATE"
STAGE_DIR_NAME = "1013I_R6I_big_unit_prep_html_fixture_after_review_approval"
VALIDATOR_NAME = "validate_1013I_R6I_big_unit_prep_html_fixture_after_review_approval.py"
HTML_NAME = "big_unit_prep_html_fixture_1013I_R6I.html"
CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]
SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)app[_-]?secret\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)tenant[_-]?access[_-]?token\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)cookie\s*[:=]\s*['\"][^'\"]{20,}"),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_output_root(root: Path) -> Path:
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    if (root / "REVIEW_PACKAGE_MANIFEST.md").exists() and (root / "LATEST_REVIEW_ENTRY.md").exists():
        return root
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def e(value: Any) -> str:
    return html.escape(str(value), quote=True)


def load_inputs(output_root: Path) -> dict[str, Any]:
    r6g = output_root / "1013I_R6G_big_unit_prep_page_fixture_after_user_approval"
    r6h = output_root / "1013I_R6H_big_unit_prep_page_fixture_review_before_html"
    return {
        "r6g_result": read_json(r6g / "1013I_R6G_result.json"),
        "page_fixture": read_json(r6g / "big_unit_prep_page_fixture_1013I_R6G.json"),
        "action_state": read_json(r6g / "big_unit_prep_page_action_state_1013I_R6G.json"),
        "r6h_result": read_json(r6h / "1013I_R6H_result.json"),
        "html_readiness": read_json(r6h / "html_readiness_matrix_1013I_R6H.json"),
    }


def boundary() -> dict[str, bool]:
    return {
        "html_fixture_created": True,
        "static_html_only": True,
        "runtime_connected": False,
        "product_runtime_called": False,
        "html_ui_implementation_allowed": False,
        "ui_implementation_started": False,
        "r7_visual_review_entered": False,
        "normal_candidate_card_generation_allowed": False,
        "writes_unit_package": False,
        "writes_lesson_body": False,
        "verified_textbook_anchor_created": False,
        "official_claim_created": False,
        "big_unit_generation_performed": False,
        "single_lesson_generation_performed": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "official_export_created": False,
        "official_archive_created": False,
        "main_project_pushed": False,
    }


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


def render_status_badge(text: str, kind: str = "neutral") -> str:
    return f'<span class="badge badge-{e(kind)}">{e(text)}</span>'


def build_html(inputs: dict[str, Any]) -> str:
    fixture = inputs["page_fixture"]
    action_state = inputs["action_state"]
    first = fixture["first_screen"]
    confirmation_items = first["middle"]["items"]
    columns = first["lower"]["columns"]
    timeline_section = next(section for section in fixture["sections"] if section["section_id"] == "big_unit_chain_light_timeline")
    timeline = timeline_section["timeline"]
    position_section = next(section for section in fixture["sections"] if section["section_id"] == "lesson_position_candidate")
    textbook_section = next(section for section in fixture["sections"] if section["section_id"] == "textbook_anchor_candidates")
    actions = action_state["teacher_actions"]

    confirmation_html = "\n".join(
        f"""
        <li class="check-item">
          <span class="check-dot">!</span>
          <div>
            <strong>{e(item["label"])}</strong>
            <p>{e(item["why_required"])}</p>
          </div>
        </li>
        """
        for item in confirmation_items
    )
    columns_html = "\n".join(
        f"""
        <article class="summary-tile">
          <div class="tile-label">{e(col["teacher_label"])}</div>
          <strong>{e(col["summary"])}</strong>
          {render_status_badge("待教师确认", "warn")}
        </article>
        """
        for col in columns
    )
    timeline_html = "\n".join(
        f"""
        <li class="timeline-node">
          <span class="node-index">{idx}</span>
          <div>
            <strong>{e(node["teacher_title"])}</strong>
            <p>{e(node["one_sentence_purpose"])}</p>
            <span class="field-preview">{e(" / ".join(node.get("field_label_preview", [])))}</span>
          </div>
        </li>
        """
        for idx, node in enumerate(timeline, start=1)
    )
    position_html = "\n".join(
        f"""
        <button class="position-option" type="button">
          <span>{e(option["teacher_label"])}</span>
          {render_status_badge("待选", "neutral")}
        </button>
        """
        for option in position_section["options"]
    )
    actions_html = "\n".join(
        f"""
        <button class="action-button" type="button">
          <span>{e(action["teacher_label"])}</span>
          {render_status_badge("降级草稿" if action["action_id"] == "continue_degraded_single_lesson_draft" else "仅预览确认", "danger" if action["action_id"] == "continue_degraded_single_lesson_draft" else "preview")}
        </button>
        """
        for action in actions
    )
    source_lesson = textbook_section["candidate"]["source_request_lesson"]
    unit_titles = " / ".join(textbook_section["candidate"]["candidate_anchor"]["unit_title_candidates"])

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{e(fixture["teacher_visible_title"])} · R6I 静态样张</title>
  <style>
    :root {{
      --ink: #20252b;
      --muted: #66717d;
      --line: #d9e0e2;
      --paper: #f7f8f5;
      --panel: #ffffff;
      --green: #315f52;
      --blue: #315d8c;
      --amber: #9b6a20;
      --red: #9b3c35;
      --mint: #e7f2ed;
      --sky: #e8f0f7;
      --warn: #fff4d8;
    }}
    * {{ box-sizing: border-box; }}
    html {{ overflow-x: hidden; }}
    body {{
      margin: 0;
      font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--paper);
      letter-spacing: 0;
      overflow-x: hidden;
    }}
    h1, h2, h3, p, li, span, strong, button, summary, div {{
      overflow-wrap: anywhere;
      word-break: break-word;
    }}
    .page {{
      min-height: 100vh;
      display: grid;
      grid-template-columns: minmax(240px, 300px) minmax(0, 1fr) minmax(220px, 280px);
      gap: 16px;
      padding: 18px;
    }}
    .page > *, .panel, .main, .summary-tile, .timeline-node, .position-option, .action-button {{
      min-width: 0;
    }}
    .header {{
      grid-column: 1 / -1;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 12px;
    }}
    .header h1 {{ margin: 0; font-size: 22px; font-weight: 700; }}
    .header p {{ margin: 4px 0 0; color: var(--muted); font-size: 13px; }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }}
    .panel h2 {{ margin: 0 0 10px; font-size: 16px; }}
    .main {{
      display: grid;
      gap: 14px;
      align-content: start;
    }}
    .decision-banner {{
      border-left: 5px solid var(--amber);
      background: var(--warn);
      padding: 14px;
      border-radius: 8px;
    }}
    .decision-banner strong {{ display: block; font-size: 18px; margin-bottom: 6px; }}
    .decision-banner p {{ margin: 0; color: #5e4a21; line-height: 1.6; }}
    .check-list {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 9px; }}
    .check-item {{ display: grid; grid-template-columns: 24px 1fr; gap: 10px; align-items: start; }}
    .check-dot {{
      width: 22px; height: 22px; border-radius: 50%;
      display: inline-grid; place-items: center;
      background: var(--amber); color: #fff; font-weight: 700; font-size: 12px;
    }}
    .check-item p {{ margin: 3px 0 0; color: var(--muted); font-size: 13px; line-height: 1.5; }}
    .summary-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }}
    .summary-tile {{ border: 1px solid var(--line); border-radius: 8px; padding: 12px; background: #fbfcfb; }}
    .tile-label {{ color: var(--muted); font-size: 12px; margin-bottom: 6px; }}
    .badge {{
      display: inline-flex; align-items: center; gap: 4px;
      min-height: 22px; padding: 2px 7px; border-radius: 999px;
      font-size: 12px; margin-top: 8px; border: 1px solid transparent;
      white-space: nowrap;
    }}
    .badge-warn {{ background: #fff4d8; color: var(--amber); border-color: #ead49c; }}
    .badge-preview {{ background: var(--sky); color: var(--blue); border-color: #c9d8ea; }}
    .badge-danger {{ background: #fde9e7; color: var(--red); border-color: #efc1bc; }}
    .badge-neutral {{ background: #eef1f0; color: var(--muted); border-color: #d8dddc; }}
    .timeline {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; }}
    .timeline-node {{
      display: grid; grid-template-columns: 28px 1fr; gap: 10px;
      border: 1px solid var(--line); border-radius: 8px; padding: 10px; background: #fbfcfb;
    }}
    .node-index {{
      width: 26px; height: 26px; border-radius: 50%; display: grid; place-items: center;
      color: #fff; background: var(--green); font-size: 13px; font-weight: 700;
    }}
    .timeline-node p {{ margin: 4px 0 6px; color: var(--muted); font-size: 13px; line-height: 1.5; }}
    .field-preview {{ display: block; max-width: 100%; color: var(--blue); font-size: 12px; }}
    .position-grid {{ display: grid; gap: 8px; }}
    .position-option, .action-button {{
      width: 100%; min-height: 40px; border: 1px solid var(--line); border-radius: 8px;
      background: #fff; color: var(--ink); display: flex; justify-content: space-between;
      align-items: center; gap: 10px; padding: 8px 10px; text-align: left; font: inherit;
    }}
    .action-button {{ background: #fbfcfb; }}
    .reference details {{ border: 1px solid var(--line); border-radius: 8px; padding: 10px; background: #fbfcfb; }}
    .reference summary {{ cursor: default; font-weight: 700; }}
    .reference p {{ color: var(--muted); line-height: 1.6; font-size: 13px; }}
    .anchor-meta {{ display: grid; gap: 8px; font-size: 13px; }}
    .anchor-meta span {{ color: var(--muted); }}
    @media (max-width: 960px) {{
      .page {{ display: block; width: 100%; max-width: 100vw; padding: 12px; }}
      .page > * {{ margin-bottom: 12px; }}
      .header {{ align-items: flex-start; flex-direction: column; }}
      .summary-grid {{ grid-template-columns: 1fr; }}
      .timeline-node, .check-item {{ grid-template-columns: 1fr; }}
      .node-index, .check-dot {{ margin-bottom: 2px; }}
      .field-preview, .timeline-node p, .check-item p, .decision-banner p {{
        word-break: break-all;
      }}
    }}
  </style>
</head>
<body>
  <main class="page" data-stage="1013I_R6I" data-static-html-only="true">
    <header class="header">
      <div>
        <h1>{e(fixture["teacher_visible_title"])}</h1>
        <p>静态 HTML 样张 · 不接运行时 · 不写正文 · 不生成大单元</p>
      </div>
      <div>
        {render_status_badge("静态样张", "preview")}
        {render_status_badge("不允许正式应用", "danger")}
      </div>
    </header>

    <aside class="panel">
      <h2>大单元推进链</h2>
      <ol class="timeline" aria-label="四个阶段候选轻时间线">
        {timeline_html}
      </ol>
    </aside>

    <section class="main">
      <div class="decision-banner">
        <strong>为什么现在还不能直接生成单课</strong>
        <p>{e(first["top"]["teacher_copy"])}</p>
      </div>

      <section class="panel">
        <h2>{e(first["middle"]["teacher_copy"])}</h2>
        <ul class="check-list">
          {confirmation_html}
        </ul>
      </section>

      <section class="summary-grid" aria-label="候选摘要">
        {columns_html}
      </section>

      <section class="panel">
        <h2>本课承担什么任务</h2>
        <div class="position-grid">
          {position_html}
        </div>
      </section>

      <section class="panel">
        <h2>教师动作</h2>
        <div class="position-grid">
          {actions_html}
        </div>
      </section>
    </section>

    <aside class="panel reference">
      <h2>教材锚点候选</h2>
      <div class="anchor-meta">
        <strong>{e(source_lesson["grade"])} {e(source_lesson["subject"])}《{e(source_lesson["lesson_title"])}》</strong>
        <span>候选单元：{e(unit_titles)}</span>
        <span>状态：待教师确认，不是正式教材锚点</span>
      </div>
      <hr />
      <details>
        <summary>只读依据和风险提醒</summary>
        <p>官方材料只作为字段和表达参考，不覆盖课标、教材锚点、大单元链或教师确认。确认类动作只进入预览确认，不写正式数据。</p>
      </details>
    </aside>
  </main>
</body>
</html>
"""


def create_screenshots(stage_dir: Path, html_path: Path) -> dict[str, Any]:
    browser = find_browser()
    screenshots: list[dict[str, Any]] = []
    if browser is None:
        return {
            "screenshot_smoke_pass": False,
            "screenshot_error": "browser_not_found",
            "screenshots": screenshots,
        }
    viewports = [
        {"id": "desktop", "width": 1440, "height": 1100},
        {"id": "mobile", "width": 390, "height": 1100},
    ]
    for viewport in viewports:
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6I_{viewport['id']}.png"
        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-cache",
            "--disable-default-apps",
            "--no-first-run",
            f"--window-size={viewport['width']},{viewport['height']}",
            f"--screenshot={out}",
            "file:///" + html_path.as_posix(),
        ]
        run = subprocess.run(cmd, text=True, capture_output=True, timeout=60)
        if run.returncode != 0:
            return {
                "screenshot_smoke_pass": False,
                "screenshot_error": run.stderr[-500:],
                "screenshots": screenshots,
            }
        width, height = png_size(out)
        screenshots.append(
            {
                "viewport": viewport["id"],
                "path": out.name,
                "width": width,
                "height": height,
                "bytes": out.stat().st_size,
            }
        )
    return {
        "screenshot_smoke_pass": all(item["bytes"] > 10000 for item in screenshots),
        "screenshot_error": None,
        "screenshots": screenshots,
    }


def scan_deprecated_visible_names(paths: list[Path]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name in DEPRECATED_VISIBLE_NAMES:
            if name in text:
                hits.append({"path": str(path), "name": name})
    return hits


def scan_secrets(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append(str(path))
                break
    return hits


def build_manifest(stage_dir: Path, html_path: Path, visual_smoke: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "html_fixture": html_path.name,
        "static_html_only": True,
        "runtime_connected": False,
        "visual_smoke": visual_smoke,
        "files": sorted(path.name for path in stage_dir.iterdir() if path.is_file()),
    }


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013I_R6I Big Unit Prep HTML Fixture Report

```text
STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}
HTML_FIXTURE_CREATED=true
STATIC_HTML_ONLY=true
RUNTIME_CONNECTED=false
HTML_UI_IMPLEMENTATION_ALLOWED=false
```

## Result

```text
decision_first_layout_visible={str(result["decision_first_layout_visible"]).lower()}
blocking_reason_visible={str(result["blocking_reason_visible"]).lower()}
missing_confirmations_visible={str(result["missing_confirmations_visible"]).lower()}
preview_only_badges_visible={str(result["preview_only_badges_visible"]).lower()}
degraded_draft_label_visible={str(result["degraded_draft_label_visible"]).lower()}
official_reference_collapsed_by_default={str(result["official_reference_collapsed_by_default"]).lower()}
big_unit_chain_rendered_as_light_timeline={str(result["big_unit_chain_rendered_as_light_timeline"]).lower()}
light_timeline_node_count={result["light_timeline_node_count"]}
lesson_position_teacher_labels_visible={str(result["lesson_position_teacher_labels_visible"]).lower()}
backend_role_keys_hidden_or_low_weight={str(result["backend_role_keys_hidden_or_low_weight"]).lower()}
screenshot_smoke_pass={str(result["screenshot_smoke_pass"]).lower()}
```

## Boundary

R6I creates a static HTML fixture only. It does not modify the main prep-room HTML, does not connect runtime, does not call provider/model, does not generate unit or lesson content, and does not write database, memory, Feishu, export, or archive.
"""


def build_result(output_root: Path, stage_dir: Path, html_path: Path, visual_smoke: dict[str, Any], stage_files: list[Path]) -> dict[str, Any]:
    html_text = html_path.read_text(encoding="utf-8")
    latest_text = (output_root / "LATEST_REVIEW_ENTRY.md").read_text(encoding="utf-8")
    manifest_text = (output_root / "REVIEW_PACKAGE_MANIFEST.md").read_text(encoding="utf-8")
    r6h_result = read_json(
        output_root
        / "1013I_R6H_big_unit_prep_page_fixture_review_before_html"
        / "1013I_R6H_result.json"
    )
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "r6h_result_present": True,
        "r6h_final_status": r6h_result.get("final_status"),
        "r6h_pass": r6h_result.get("final_status") == R6H_PASS_STATUS,
        "latest_entry_points_to_r6i": f"REVIEW_STAGE={STAGE_ID}" in latest_text
        and f"FINAL_STATUS={FINAL_STATUS}" in latest_text,
        "latest_entry_next_stage_is_r6j": f"NEXT_RECOMMENDED_STAGE={NEXT_STAGE}" in latest_text,
        "manifest_includes_r6i": STAGE_ID in manifest_text and f"{STAGE_DIR_NAME}/" in manifest_text,
        "manifest_next_stage_is_r6j": NEXT_STAGE in manifest_text,
        "html_fixture_created": html_path.exists(),
        "static_html_only": 'data-static-html-only="true"' in html_text,
        "decision_first_layout_visible": "为什么现在还不能直接生成单课" in html_text,
        "blocking_reason_visible": "需要先确认教材锚点、大单元推进链和这节课承担的任务" in html_text,
        "missing_confirmations_visible": "还差这些确认" in html_text and "确认教材版本" in html_text,
        "preview_only_badges_visible": "仅预览确认" in html_text,
        "degraded_draft_label_visible": "降级草稿" in html_text,
        "official_reference_collapsed_by_default": "<details>" in html_text and "<details open" not in html_text,
        "big_unit_chain_rendered_as_light_timeline": "四个阶段候选轻时间线" in html_text,
        "light_timeline_node_count": html_text.count('class="timeline-node"'),
        "lesson_position_teacher_labels_visible": "单元开头：先激发兴趣、建立问题" in html_text
        and "暂不确定：需要老师补充单元材料" in html_text,
        "backend_role_keys_hidden_or_low_weight": all(
            key not in html_text
            for key in [
                "unit_entry",
                "concept_building",
                "method_learning",
                "creative_production",
                "critique_and_revision",
                "unknown_pending_teacher_confirm",
            ]
        ),
        "screenshot_smoke_pass": visual_smoke.get("screenshot_smoke_pass") is True,
        "screenshot_count": len(visual_smoke.get("screenshots", [])),
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(stage_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **boundary(),
    }
    required_true = [
        "r6h_result_present",
        "r6h_pass",
        "latest_entry_points_to_r6i",
        "latest_entry_next_stage_is_r6j",
        "manifest_includes_r6i",
        "manifest_next_stage_is_r6j",
        "html_fixture_created",
        "static_html_only",
        "decision_first_layout_visible",
        "blocking_reason_visible",
        "missing_confirmations_visible",
        "preview_only_badges_visible",
        "degraded_draft_label_visible",
        "official_reference_collapsed_by_default",
        "big_unit_chain_rendered_as_light_timeline",
        "lesson_position_teacher_labels_visible",
        "backend_role_keys_hidden_or_low_weight",
        "screenshot_smoke_pass",
    ]
    required_false = [
        "runtime_connected",
        "product_runtime_called",
        "html_ui_implementation_allowed",
        "ui_implementation_started",
        "r7_visual_review_entered",
        "normal_candidate_card_generation_allowed",
        "writes_unit_package",
        "writes_lesson_body",
        "verified_textbook_anchor_created",
        "official_claim_created",
        "big_unit_generation_performed",
        "single_lesson_generation_performed",
        "provider_called",
        "model_called",
        "formal_apply_performed",
        "database_written",
        "memory_written",
        "feishu_written",
        "official_export_created",
        "official_archive_created",
        "main_project_pushed",
    ]
    failures = [key for key in required_true if result.get(key) is not True]
    failures.extend([key for key in required_false if result.get(key) is not False])
    if result.get("light_timeline_node_count") != 4:
        failures.append("light_timeline_node_count")
    if result.get("screenshot_count") != 2:
        failures.append("screenshot_count")
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    if failures:
        result["final_status"] = "FAIL_1013I_R6I_BIG_UNIT_PREP_HTML_FIXTURE_AFTER_REVIEW_APPROVAL"
    return result


def copy_source_delta(root: Path, output_root: Path) -> None:
    source = root / "scripts" / VALIDATOR_NAME
    target = output_root / "source_delta_1013I_R6I" / "scripts" / VALIDATOR_NAME
    if source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    root = args.root.resolve()
    output_root = resolve_output_root(root)
    inputs = load_inputs(output_root)
    stage_dir = output_root / STAGE_DIR_NAME
    html_path = stage_dir / HTML_NAME
    write_text(html_path, build_html(inputs))
    visual_smoke = create_screenshots(stage_dir, html_path)
    write_json(stage_dir / "visual_smoke_1013I_R6I.json", visual_smoke)
    write_json(stage_dir / "html_fixture_manifest_1013I_R6I.json", build_manifest(stage_dir, html_path, visual_smoke))
    result_path = stage_dir / "1013I_R6I_result.json"
    report_path = stage_dir / "1013I_R6I_report.md"
    stage_files = [
        html_path,
        stage_dir / "visual_smoke_1013I_R6I.json",
        stage_dir / "html_fixture_manifest_1013I_R6I.json",
        result_path,
        report_path,
    ]
    result = build_result(output_root, stage_dir, html_path, visual_smoke, stage_files)
    write_json(result_path, result)
    write_text(report_path, build_report(result))
    copy_source_delta(root, output_root)
    if result["final_status"] != FINAL_STATUS:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    print(f"{FINAL_STATUS}: {result_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
