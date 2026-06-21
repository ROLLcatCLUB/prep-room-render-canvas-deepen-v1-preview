from __future__ import annotations

import json
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R13_DIR = BASE / "1013L_R13_existing_page_big_unit_viewmodel_visible_hydration"
R14_DIR = BASE / "1013L_R14_existing_page_big_unit_viewmodel_visual_smoke"
SOURCE_DELTA = BASE / "source_delta_1013L_R14"
R13_HTML = R13_DIR / "prep_room_render_canvas_deepen_v1_1013L_R13_big_unit_visible_hydration.html"


STAGE = "1013L_R14_EXISTING_PAGE_BIG_UNIT_VIEWMODEL_VISUAL_SMOKE"
FINAL_STATUS = "PASS_1013L_R14_EXISTING_PAGE_BIG_UNIT_VIEWMODEL_VISUAL_SMOKE"
NEXT_STAGE = "1013L_R15_EXISTING_PAGE_HYDRATION_MILESTONE_PACKAGE"


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
    raise FileNotFoundError("No Edge/Chrome browser found for R14 visual smoke.")


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"Not a PNG: {path}")
    return struct.unpack(">II", data[16:24])


def boundary() -> dict[str, bool]:
    return {
        "visual_smoke_only": True,
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


def take_screenshot(browser: Path, url: str, out: Path, width: int, height: int) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="shiwei-r14-browser-") as temp_dir:
        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--disable-background-networking",
            "--allow-file-access-from-files",
            f"--window-size={width},{height}",
            f"--user-data-dir={temp_dir}",
            f"--screenshot={out}",
            url,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)


def dump_dom(browser: Path, url: str) -> str:
    with tempfile.TemporaryDirectory(prefix="shiwei-r14-dom-") as temp_dir:
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
        completed = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
        return completed.stdout


def visual_cases() -> list[dict]:
    return [
        {
            "case_id": "desktop_big_unit_viewmodel_hydrated",
            "suffix": "?r13=bigUnit",
            "width": 1920,
            "height": 1080,
            "screenshot": "ui_smoke_1013L_R14_desktop_big_unit.png",
            "required_markers": [
                'data-1013l-r13-big-unit-surface="true"',
                "第一单元《多变的色彩》",
                "课标依据",
                "课时任务链",
            ],
        },
        {
            "case_id": "desktop_normal_shell_still_available",
            "suffix": "?r14=normal",
            "width": 1920,
            "height": 1080,
            "screenshot": "ui_smoke_1013L_R14_desktop_normal.png",
            "required_markers": [
                "ai-tool-strip",
                "courseware_screen_seed_03_color_comparison_1013K_R25",
            ],
        },
        {
            "case_id": "mobile_big_unit_viewmodel_hydrated",
            "suffix": "?r13=bigUnit",
            "width": 390,
            "height": 1400,
            "screenshot": "ui_smoke_1013L_R14_mobile_big_unit.png",
            "required_markers": [
                "第一单元《多变的色彩》",
                "核心素养",
            ],
        },
    ]


def run_visual_smoke(browser: Path) -> dict:
    base_url = R13_HTML.resolve().as_uri()
    cases = []
    for case in visual_cases():
        out = R14_DIR / case["screenshot"]
        url = base_url + case["suffix"]
        take_screenshot(browser, url, out, case["width"], case["height"])
        dom = dump_dom(browser, url)
        missing = [marker for marker in case["required_markers"] if marker not in dom]
        width, height = png_size(out)
        cases.append(
            {
                **case,
                "path": rel(out),
                "actual_width": width,
                "actual_height": height,
                "bytes": out.stat().st_size,
                "missing_markers": missing,
                "pass": width == case["width"]
                and height == case["height"]
                and out.stat().st_size > 10000
                and missing == [],
            }
        )
    return {
        "visual_smoke_id": "big_unit_viewmodel_visual_smoke_1013L_R14",
        "stage": STAGE,
        "source_html": rel(R13_HTML),
        "case_count": len(cases),
        "cases": cases,
        "visual_smoke_pass": all(item["pass"] for item in cases),
        "boundary": boundary(),
    }


def copy_source_delta() -> None:
    (SOURCE_DELTA / "scripts").mkdir(parents=True, exist_ok=True)
    for name in [
        "build_1013L_R14_existing_page_big_unit_viewmodel_visual_smoke.py",
        "validate_1013L_R14_existing_page_big_unit_viewmodel_visual_smoke.py",
    ]:
        shutil.copy2(ROOT / "scripts" / name, SOURCE_DELTA / "scripts" / name)


def main() -> None:
    smoke = run_visual_smoke(find_browser())
    write_json(R14_DIR / "big_unit_viewmodel_visual_smoke_1013L_R14.json", smoke)
    result = {
        "stage": STAGE,
        "final_status": FINAL_STATUS if smoke["visual_smoke_pass"] else f"FAIL_{STAGE}",
        "source_stage": "1013L_R13_EXISTING_PAGE_BIG_UNIT_VIEWMODEL_VISIBLE_HYDRATION",
        "source_html": rel(R13_HTML),
        "visual_smoke_pass": smoke["visual_smoke_pass"],
        "screenshot_count": smoke["case_count"],
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
        "github_uploaded": False,
        "next_stage": NEXT_STAGE,
        "boundary": boundary(),
    }
    write_json(R14_DIR / "1013L_R14_result.json", result)
    report = """# 1013L R14 Existing Page Big Unit ViewModel Visual Smoke

R14 screenshots the R13 existing-shell big-unit ViewModel hydration:

- desktop big-unit route
- desktop normal prep shell
- mobile big-unit route

It does not change page logic, connect runtime, call provider/model, write persistence, or push the main project.
"""
    write_text(R14_DIR / "1013L_R14_report.md", report)
    copy_source_delta()
    print(R14_DIR)


if __name__ == "__main__":
    main()
