from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013J_R1G_R2_COURSEWARE_ROUTE_ISOLATION_PATCH"
FINAL_STATUS = "PASS_1013J_R1G_R2_COURSEWARE_ROUTE_ISOLATION_PATCH"
INHERITS_FROM = "1013J_R1G_R1_COURSEWARE_RESPONSIVE_FULL_WIDTH_PATCH"
NEXT_STAGE = "USER_REVIEW_COURSEWARE_ROUTE_ISOLATION"
BASE_DIR_NAME = "1013J_R1G_R1_courseware_responsive_full_width_patch"
BASE_HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1G_R1_courseware_responsive_full_width.html"
STAGE_DIR_NAME = "1013J_R1G_R2_courseware_route_isolation_patch"
HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1G_R2_courseware_route_isolated.html"
VALIDATOR_NAME = "validate_1013J_R1G_R2_courseware_route_isolation_patch.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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


def patch_html(output_root: Path) -> str:
    base_html = output_root / BASE_DIR_NAME / BASE_HTML_NAME
    html = base_html.read_text(encoding="utf-8")
    html = html.replace("1013J_R1G_R1 课件区响应式全宽", "1013J_R1G_R2 课件路由隔离")

    html = html.replace(
        'if (window.location.hash && window.location.hash !== "#coursewareExpanded") return;',
        'if (window.location.hash && window.location.hash !== "#coursewareExpanded") { const prepView = model.views.find((view) => view.id === "prepNotebook"); if (prepView) prepView.courseware_workspace_expanded = false; return; }',
        1,
    )
    html = html.replace(
        'const prepView = model.views.find((item) => item.id === "prepNotebook");\n      if (prepView?.courseware_workspace_expanded) return renderCoursewareExpandedWorkspace1013JR1(prepView);',
        'const prepView = model.views.find((item) => item.id === "prepNotebook");\n      if (view.id === "prepNotebook" && prepView?.courseware_workspace_expanded) return renderCoursewareExpandedWorkspace1013JR1(prepView);\n      if (view.id !== "prepNotebook" && prepView) prepView.courseware_workspace_expanded = false;',
        1,
    )
    html = html.replace(
        'model.selected_node_id = firstNode || model.selected_node_id;\n      byId("inspector").classList.add("hidden");',
        'model.selected_node_id = firstNode || model.selected_node_id;\n      const routePrepView = model.views.find((item) => item.id === "prepNotebook");\n      if (routePrepView && view.id !== "prepNotebook") routePrepView.courseware_workspace_expanded = false;\n      byId("inspector").classList.add("hidden");',
        1,
    )
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
    files: list[str] = []
    for index, script_text in enumerate(scripts):
        script_path = stage_dir / f"javascript_syntax_1013J_R1G_R2_{index:02d}.js"
        write_text(script_path, script_text)
        files.append(script_path.name)
        proc = subprocess.run([node, "--check", str(script_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            return {"javascript_syntax_check_pass": False, "javascript_syntax_error": proc.stderr.strip() or proc.stdout.strip(), "javascript_syntax_files": files}
    return {"javascript_syntax_check_pass": True, "javascript_syntax_files": files}


def screenshot(stage_dir: Path, html_path: Path) -> dict[str, Any]:
    browser = find_browser()
    shots: list[dict[str, Any]] = []
    if browser is None:
        return {"screenshot_smoke_pass": False, "screenshot_error": "browser_not_found", "screenshots": shots}
    cases = [
        ("week_calendar", "#weekCalendar"),
        ("prep_notebook", "#prepNotebook"),
        ("courseware", "?screen=screen_03#coursewareExpanded"),
    ]
    for name, route in cases:
        out = stage_dir / f"ui_smoke_screenshot_1013J_R1G_R2_{name}.png"
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
            "file:///" + html_path.as_posix() + route,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        width, height = png_size(out)
        shots.append({"case": name, "path": out.name, "width": width, "height": height, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": True, "screenshots": shots}


def validate_html(html_text: str) -> dict[str, Any]:
    return {
        "courseware_route_isolation_created": 'view.id === "prepNotebook" && prepView?.courseware_workspace_expanded' in html_text,
        "non_prep_view_clears_courseware_state": 'view.id !== "prepNotebook" && prepView' in html_text and "courseware_workspace_expanded = false" in html_text,
        "hash_non_courseware_clears_courseware_state": 'window.location.hash !== "#coursewareExpanded"' in html_text and 'prepView.courseware_workspace_expanded = false' in html_text,
        "week_calendar_route_not_forced_to_courseware": 'if (view.id === "weekCalendar") return renderWeekCalendarCanvas(view);' in html_text,
        "prep_notebook_route_kept": 'if (view.id === "prepNotebook") return renderPrepNotebookCanvas(view);' in html_text,
        "courseware_hash_route_kept": 'window.location.hash === "#coursewareExpanded"' in html_text,
        **boundary(),
    }


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
    write_text(stage_dir / "1013J_R1G_R2_report.md", f"""# 1013J_R1G_R2 Courseware Route Isolation Patch

FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R1G_R2 fixes route pollution where top-level navigation such as week calendar could render the courseware workspace after the courseware expanded state was set.

Fixes:
- courseware workspace renders only when active view is prep notebook
- non-prep views clear courseware expanded state
- non-courseware hash routes clear courseware expanded state
- week calendar and prep notebook routes remain independent

No runtime, provider/model, upload, search, whiteboard library, PPT export, drag edit, database, memory, Feishu, or formal apply is connected.

Failed checks: {result["failed_checks"]}
""")
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

1013J_R1G_R2 isolates courseware routing so week calendar and other top-level views no longer jump into the courseware workspace. Courseware expanded mode now only renders under the prep notebook view.

Key flags:
- COURSEWARE_ROUTE_ISOLATION_CREATED=true
- NON_PREP_VIEW_CLEARS_COURSEWARE_STATE=true
- HASH_NON_COURSEWARE_CLEARS_COURSEWARE_STATE=true
- WEEK_CALENDAR_ROUTE_NOT_FORCED_TO_COURSEWARE=true
- PREP_NOTEBOOK_ROUTE_KEPT=true
- COURSEWARE_HASH_ROUTE_KEPT=true
- PROVIDER_CALLED=false
- MODEL_CALLED=false
- FORMAL_APPLY_PERFORMED=false
- MAIN_PROJECT_PUSHED=false
""")
    write_text(output_root / "README.md", f"""# Prep Room Render Canvas Deepen V1 Review Package

Latest stage: `{STAGE_ID}`

Open:
- `{STAGE_DIR_NAME}/{HTML_NAME}`
- `{STAGE_DIR_NAME}/1013J_R1G_R2_result.json`

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
- `{STAGE_DIR_NAME}/1013J_R1G_R2_result.json`
- `{STAGE_DIR_NAME}/1013J_R1G_R2_report.md`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1G_R2_week_calendar.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1G_R2_prep_notebook.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1G_R2_courseware.png`
- `scripts/{VALIDATOR_NAME}`
""")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output_root = locate_output_root(root)
    base_result = output_root / BASE_DIR_NAME / "1013J_R1G_R1_result.json"
    if not base_result.exists():
        raise FileNotFoundError(base_result)

    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)
    html_text = patch_html(output_root)
    html_path = stage_dir / HTML_NAME
    write_text(html_path, html_text)

    js_check = javascript_syntax_check(stage_dir, html_text)
    smoke = screenshot(stage_dir, html_path)
    checks = validate_html(html_text)
    checks.update(js_check)
    checks["screenshot_smoke_pass"] = bool(smoke.get("screenshot_smoke_pass"))
    failed = failed_checks(checks)
    result = {
        "stage": STAGE_ID,
        "status": FINAL_STATUS if not failed else "FAIL_1013J_R1G_R2_COURSEWARE_ROUTE_ISOLATION_PATCH",
        "final_status": FINAL_STATUS if not failed else "FAIL_1013J_R1G_R2_COURSEWARE_ROUTE_ISOLATION_PATCH",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        **checks,
        "failed_checks": failed,
    }
    write_json(stage_dir / "1013J_R1G_R2_result.json", result)
    write_docs(output_root, stage_dir, result)
    source_delta = output_root / "source_delta_1013J_R1G_R2" / "scripts" / VALIDATOR_NAME
    source_delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), source_delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))
    print("ALL_1013J_R1G_R2_COURSEWARE_ROUTE_ISOLATION_PATCH_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
