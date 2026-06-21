from __future__ import annotations

import json
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R11_DIR = BASE / "1013L_R11_existing_page_readonly_viewmodel_static_hydration_apply"
R12_DIR = BASE / "1013L_R12_existing_page_hydrated_viewmodel_visual_smoke"
SOURCE_DELTA = BASE / "source_delta_1013L_R12"
R11_HTML = R11_DIR / "prep_room_render_canvas_deepen_v1_1013L_R11_static_hydration_apply.html"


STAGE = "1013L_R12_EXISTING_PAGE_HYDRATED_VIEWMODEL_VISUAL_SMOKE"
FINAL_STATUS = "PASS_1013L_R12_EXISTING_PAGE_HYDRATED_VIEWMODEL_VISUAL_SMOKE"
NEXT_STAGE = "1013L_R13_EXISTING_PAGE_BIG_UNIT_VIEWMODEL_VISIBLE_HYDRATION"


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
    raise FileNotFoundError("No Edge/Chrome browser found for R12 visual smoke.")


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
    with tempfile.TemporaryDirectory(prefix="shiwei-r12-browser-") as temp_dir:
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


def visual_cases() -> list[dict]:
    return [
        {
            "case_id": "desktop_normal_hydrated_courseware_rail",
            "suffix": "?r12=normal",
            "width": 1920,
            "height": 1080,
            "screenshot": "ui_smoke_1013L_R12_desktop_normal.png",
        },
        {
            "case_id": "desktop_courseware_expanded_hydrated",
            "suffix": "?r12=courseware#coursewareExpanded",
            "width": 1920,
            "height": 1080,
            "screenshot": "ui_smoke_1013L_R12_desktop_courseware_expanded.png",
        },
        {
            "case_id": "desktop_display_preview_hydrated",
            "suffix": "?preview=display&screen=03#coursewareExpanded",
            "width": 1920,
            "height": 1080,
            "screenshot": "ui_smoke_1013L_R12_desktop_display_preview.png",
        },
        {
            "case_id": "mobile_normal_hydrated",
            "suffix": "?r12=mobile",
            "width": 390,
            "height": 844,
            "screenshot": "ui_smoke_1013L_R12_mobile_normal.png",
        },
    ]


def run_visual_smoke(browser: Path) -> dict:
    base_url = R11_HTML.resolve().as_uri()
    cases = []
    for case in visual_cases():
        out = R12_DIR / case["screenshot"]
        take_screenshot(browser, base_url + case["suffix"], out, case["width"], case["height"])
        width, height = png_size(out)
        cases.append(
            {
                **case,
                "path": rel(out),
                "actual_width": width,
                "actual_height": height,
                "bytes": out.stat().st_size,
                "pass": width == case["width"] and height == case["height"] and out.stat().st_size > 10000,
            }
        )
    return {
        "visual_smoke_id": "hydrated_viewmodel_visual_smoke_1013L_R12",
        "stage": STAGE,
        "source_html": rel(R11_HTML),
        "case_count": len(cases),
        "cases": cases,
        "visual_smoke_pass": all(item["pass"] for item in cases),
        "boundary": boundary(),
    }


def copy_source_delta() -> None:
    (SOURCE_DELTA / "scripts").mkdir(parents=True, exist_ok=True)
    for name in [
        "build_1013L_R12_existing_page_hydrated_viewmodel_visual_smoke.py",
        "validate_1013L_R12_existing_page_hydrated_viewmodel_visual_smoke.py",
    ]:
        shutil.copy2(ROOT / "scripts" / name, SOURCE_DELTA / "scripts" / name)


def main() -> None:
    browser = find_browser()
    smoke = run_visual_smoke(browser)
    write_json(R12_DIR / "hydrated_viewmodel_visual_smoke_1013L_R12.json", smoke)
    result = {
        "stage": STAGE,
        "final_status": FINAL_STATUS if smoke["visual_smoke_pass"] else f"FAIL_{STAGE}",
        "source_stage": "1013L_R11_EXISTING_PAGE_READONLY_VIEWMODEL_STATIC_HYDRATION_APPLY",
        "source_html": rel(R11_HTML),
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
    write_json(R12_DIR / "1013L_R12_result.json", result)
    report = """# 1013L R12 Existing Page Hydrated ViewModel Visual Smoke

R12 takes visual smoke screenshots of the R11 hydrated existing page:

- desktop normal prep page
- desktop courseware expanded workspace
- desktop classroom display preview
- mobile normal prep page

It does not change page logic, connect runtime, call provider/model, or write persistence.
"""
    write_text(R12_DIR / "1013L_R12_report.md", report)
    copy_source_delta()
    print(R12_DIR)


if __name__ == "__main__":
    main()
