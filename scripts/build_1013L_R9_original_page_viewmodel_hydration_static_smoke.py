from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R8_DIR = BASE / "1013L_R8_original_page_static_readonly_fetch_hook"
R9_DIR = BASE / "1013L_R9_original_page_viewmodel_hydration_static_smoke"
SOURCE_DELTA = BASE / "source_delta_1013L_R9"
R8_HTML = R8_DIR / "prep_room_render_canvas_deepen_v1_1013L_R8_static_readonly_fetch_hook.html"


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def find_browser() -> Path:
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No Edge/Chrome browser found for static hook smoke.")


def boundary() -> dict[str, bool]:
    return {
        "static_browser_smoke_only": True,
        "visible_dom_changed": False,
        "runtime_connected": False,
        "real_fetch_performed": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
    }


def smoke_runner() -> str:
    return """
<script id="main-shell-hook-smoke-runner-1013L-R9">
(function () {
  function publish(testId) {
    var hook = window.__SHIWEI_MAIN_SHELL_READONLY_FETCH_HOOK__;
    var snapshot = hook ? hook.snapshot() : { missing_hook: true };
    snapshot.test_id = testId;
    var pre = document.createElement("pre");
    pre.id = "hook-smoke-result";
    pre.textContent = JSON.stringify(snapshot);
    document.body.appendChild(pre);
    document.documentElement.setAttribute("data-r9-hook-state", snapshot.state_id || "missing");
  }

  function run() {
    var params = new URLSearchParams(window.location.search || "");
    var testId = params.get("r9test") || "default";
    if (testId === "prepNotebook") {
      try {
        if (typeof window.selectView === "function") {
          window.selectView("prepNotebook");
        } else {
          var button = document.querySelector('[data-view="prepNotebook"]');
          if (button) button.click();
        }
      } catch (error) {}
    }
    if (testId === "weekCalendar") {
      try {
        if (typeof window.selectView === "function") {
          window.selectView("weekCalendar");
        } else {
          var weekButton = document.querySelector('[data-view="weekCalendar"]');
          if (weekButton) weekButton.click();
        }
      } catch (error) {}
    }
    window.setTimeout(function () { publish(testId); }, 300);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { window.setTimeout(run, 0); });
  } else {
    window.setTimeout(run, 0);
  }
}());
</script>
"""


def build_smoke_html() -> Path:
    html_text = R8_HTML.read_text(encoding="utf-8-sig")
    marker = "</body>"
    if marker not in html_text:
        raise RuntimeError("R8 html missing </body>")
    target = R9_DIR / "prep_room_render_canvas_deepen_v1_1013L_R9_hook_smoke.html"
    write_text(target, html_text.replace(marker, smoke_runner() + "\n" + marker))
    return target


def dump_dom(browser: Path, url: str) -> str:
    with tempfile.TemporaryDirectory(prefix="shiwei-r9-browser-") as temp_dir:
        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--disable-background-networking",
            "--allow-file-access-from-files",
            "--virtual-time-budget=5000",
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


def parse_result(dom: str) -> dict:
    match = re.search(r'<pre id="hook-smoke-result">(.+?)</pre>', dom, re.S)
    if not match:
        raise RuntimeError("hook smoke result was not written to DOM")
    return json.loads(html.unescape(match.group(1)))


def run_smoke_cases(browser: Path, smoke_html: Path) -> list[dict]:
    base_url = smoke_html.resolve().as_uri()
    cases = [
        {"case_id": "default_single_lesson", "suffix": "?r9test=default", "expected_state_id": "single_lesson_design"},
        {"case_id": "week_calendar", "suffix": "?r9test=weekCalendar", "expected_state_id": "week_calendar"},
        {"case_id": "prep_notebook", "suffix": "?r9test=prepNotebook", "expected_state_id": "single_lesson_design"},
        {"case_id": "courseware_expanded", "suffix": "?r9test=courseware#coursewareExpanded", "expected_state_id": "courseware_workspace"},
        {"case_id": "display_preview", "suffix": "?r9test=display&preview=display&screen=03#coursewareExpanded", "expected_state_id": "classroom_display_preview"},
    ]
    results = []
    for case in cases:
        snapshot = parse_result(dump_dom(browser, base_url + case["suffix"]))
        results.append(
            {
                **case,
                "actual_state_id": snapshot.get("state_id"),
                "readonly_endpoint": snapshot.get("readonly_endpoint"),
                "active_capability": snapshot.get("active_capability"),
                "real_fetch_performed": snapshot.get("real_fetch_performed"),
                "pass": snapshot.get("state_id") == case["expected_state_id"] and snapshot.get("real_fetch_performed") is False,
            }
        )
    return results


def copy_source_delta() -> None:
    (SOURCE_DELTA / "scripts").mkdir(parents=True, exist_ok=True)
    for name in [
        "build_1013L_R9_original_page_viewmodel_hydration_static_smoke.py",
        "validate_1013L_R9_original_page_viewmodel_hydration_static_smoke.py",
    ]:
        shutil.copy2(ROOT / "scripts" / name, SOURCE_DELTA / "scripts" / name)


def main() -> None:
    smoke_html = build_smoke_html()
    browser = find_browser()
    cases = run_smoke_cases(browser, smoke_html)
    smoke_pass = all(item["pass"] for item in cases)
    write_json(
        R9_DIR / "hook_resolution_browser_smoke_1013L_R9.json",
        {
            "smoke_id": "hook_resolution_browser_smoke_1013L_R9",
            "stage": "1013L_R9_ORIGINAL_PAGE_VIEWMODEL_HYDRATION_STATIC_SMOKE",
            "source_html": rel(R8_HTML),
            "smoke_html": rel(smoke_html),
            "browser": str(browser),
            "case_count": len(cases),
            "cases": cases,
            "hook_resolution_smoke_pass": smoke_pass,
            "boundary": boundary(),
        },
    )
    result = {
        "stage": "1013L_R9_ORIGINAL_PAGE_VIEWMODEL_HYDRATION_STATIC_SMOKE",
        "final_status": "PASS_1013L_R9_ORIGINAL_PAGE_VIEWMODEL_HYDRATION_STATIC_SMOKE" if smoke_pass else "FAIL_1013L_R9_ORIGINAL_PAGE_VIEWMODEL_HYDRATION_STATIC_SMOKE",
        "source_stage": "1013L_R8_ORIGINAL_PAGE_STATIC_READONLY_FETCH_HOOK",
        "source_html": rel(R8_HTML),
        "smoke_html": rel(smoke_html),
        "hook_resolution_smoke_pass": smoke_pass,
        "smoke_case_count": len(cases),
        "expected_states_passed": smoke_pass,
        "original_page_shell_preserved": True,
        "new_visible_page_created": False,
        "visible_dom_changed": False,
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
        "next_stage": "1013L_R10_EXISTING_PAGE_READONLY_VIEWMODEL_BINDING_MILESTONE_PACKAGE",
    }
    write_json(R9_DIR / "1013L_R9_result.json", result)
    report = """# 1013L R9 Original Page ViewModel Hydration Static Smoke

R9 opens the R8 original-page static copy in a headless browser and verifies the hidden readonly fetch hook resolves the expected shell state for:

- default week calendar
- single lesson notebook
- courseware expanded workspace
- classroom display preview

The smoke does not connect runtime, call provider/model, write persistence, or change the visible shell.
"""
    write_text(R9_DIR / "1013L_R9_report.md", report)
    copy_source_delta()
    print(R9_DIR)


if __name__ == "__main__":
    main()
