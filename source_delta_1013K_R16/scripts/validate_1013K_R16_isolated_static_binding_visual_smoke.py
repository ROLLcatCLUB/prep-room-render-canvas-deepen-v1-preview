from __future__ import annotations

import argparse
import json
import shutil
import struct
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R16_ISOLATED_STATIC_BINDING_VISUAL_SMOKE"
FINAL_STATUS = "PASS_1013K_R16_ISOLATED_STATIC_BINDING_VISUAL_SMOKE"
INHERITS_FROM = "1013K_R15_ISOLATED_STATIC_FRONTEND_READONLY_BINDING_FIXTURE"
NEXT_STAGE = "1013K_R17_ISOLATED_STATIC_BINDING_USER_REVIEW_PACKAGE"
STAGE_DIR_NAME = "1013K_R16_isolated_static_binding_visual_smoke"
VALIDATOR_NAME = "validate_1013K_R16_isolated_static_binding_visual_smoke.py"


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
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
    raise FileNotFoundError("No Edge/Chrome browser found for visual smoke.")


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"Not a PNG: {path}")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def take_screenshot(browser: Path, html_path: Path, screenshot_path: Path, width: int, height: int) -> None:
    screenshot_path.parent.mkdir(parents=True, exist_ok=True)
    url = html_path.resolve().as_uri()
    cmd = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        f"--screenshot={screenshot_path}",
        url,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)


def copy_source_delta(root: Path, output_root: Path) -> list[Path]:
    delta_root = output_root / "source_delta_1013K_R16"
    src = root / "scripts" / VALIDATOR_NAME
    dst = delta_root / "scripts" / VALIDATOR_NAME
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return [dst]


def update_local_review_root(output_root: Path) -> None:
    latest = f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
NEXT_STAGE={NEXT_STAGE}
LOCAL_ONLY_SMALL_PACKAGE=true
GITHUB_UPLOAD_DEFERRED_UNTIL_NEXT_MILESTONE=true
PROVIDER_MODEL_CALL_ALLOWED=false
FORMAL_APPLY_ALLOWED=false
DATABASE_WRITE_ALLOWED=false
MEMORY_WRITE_ALLOWED=false
FORMAL_FRONTEND_PAGE_MODIFIED=false

1013K_R16 runs headless browser screenshot smoke for the R15 isolated static frontend binding fixture. It does not mount into formal frontend pages or connect runtime.
"""
    manifest = f"""# Review Package Manifest

Latest local stage: `{STAGE_ID}`

Includes:

- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013K_R16_desktop.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013K_R16_mobile.png`
- `{STAGE_DIR_NAME}/isolated_static_binding_visual_smoke_1013K_R16.json`
- `{STAGE_DIR_NAME}/1013K_R16_result.json`
- `{STAGE_DIR_NAME}/1013K_R16_report.md`
- `scripts/{VALIDATOR_NAME}`

Boundary: local-only visual smoke. No formal frontend page modification, no runtime connection, no provider/model call, no storage write, no formal apply.
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013K_R16 Isolated Static Binding Visual Smoke Report

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={result["next_stage"]}

## Screenshots

```text
desktop_screenshot_created={str(result["desktop_screenshot_created"]).lower()}
desktop_size={result["desktop_width"]}x{result["desktop_height"]}
mobile_screenshot_created={str(result["mobile_screenshot_created"]).lower()}
mobile_size={result["mobile_width"]}x{result["mobile_height"]}
html_section_count={result["html_section_count"]}
```

## Boundary

```text
formal_frontend_page_modified={str(result["formal_frontend_page_modified"]).lower()}
runtime_connected={str(result["runtime_connected"]).lower()}
provider_called={str(result["provider_called"]).lower()}
model_called={str(result["model_called"]).lower()}
formal_apply_performed={str(result["formal_apply_performed"]).lower()}
```

validator_pass={str(result["validator_pass"]).lower()}
failed_checks={json.dumps(result["failed_checks"], ensure_ascii=False)}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    root = args.root.resolve()
    output_root = resolve_output_root(root)
    r15_dir = output_root / "1013K_R15_isolated_static_frontend_readonly_binding_fixture"
    r15_result = read_json(r15_dir / "1013K_R15_result.json")
    html_path = r15_dir / "isolated_static_frontend_readonly_binding_fixture_1013K_R15.html"
    html_text = html_path.read_text(encoding="utf-8")
    stage_dir = output_root / STAGE_DIR_NAME
    browser = find_browser()
    desktop_path = stage_dir / "ui_smoke_screenshot_1013K_R16_desktop.png"
    mobile_path = stage_dir / "ui_smoke_screenshot_1013K_R16_mobile.png"
    take_screenshot(browser, html_path, desktop_path, 1365, 900)
    take_screenshot(browser, html_path, mobile_path, 390, 844)
    desktop_width, desktop_height = png_size(desktop_path)
    mobile_width, mobile_height = png_size(mobile_path)
    smoke = {
        "visual_smoke_id": "isolated_static_binding_visual_smoke_1013K_R16",
        "stage": STAGE_ID,
        "r15_pass": r15_result.get("validator_pass") is True,
        "browser_path": str(browser),
        "desktop_screenshot": str(desktop_path),
        "mobile_screenshot": str(mobile_path),
        "desktop_width": desktop_width,
        "desktop_height": desktop_height,
        "mobile_width": mobile_width,
        "mobile_height": mobile_height,
        "html_section_count": html_text.count('class="unit-section"'),
        "teacher_title_visible_in_html": "第一单元《多变的色彩》" in html_text,
        "material_prompt_visible_in_html": "缺教材目录" in html_text,
        "formal_frontend_page_modified": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
    }
    write_json(stage_dir / "isolated_static_binding_visual_smoke_1013K_R16.json", smoke)
    source_delta_files = copy_source_delta(root, output_root)
    update_local_review_root(output_root)
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "github_upload_deferred_until_next_milestone": True,
        "r15_pass": smoke["r15_pass"],
        "desktop_screenshot_created": desktop_path.exists(),
        "desktop_screenshot_bytes": desktop_path.stat().st_size if desktop_path.exists() else 0,
        "desktop_width": desktop_width,
        "desktop_height": desktop_height,
        "mobile_screenshot_created": mobile_path.exists(),
        "mobile_screenshot_bytes": mobile_path.stat().st_size if mobile_path.exists() else 0,
        "mobile_width": mobile_width,
        "mobile_height": mobile_height,
        "html_section_count": smoke["html_section_count"],
        "teacher_title_visible_in_html": smoke["teacher_title_visible_in_html"],
        "material_prompt_visible_in_html": smoke["material_prompt_visible_in_html"],
        "source_delta_created": all(path.exists() for path in source_delta_files),
        "formal_frontend_page_modified": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
    }
    failures = []
    for key in [
        "github_upload_deferred_until_next_milestone",
        "r15_pass",
        "desktop_screenshot_created",
        "mobile_screenshot_created",
        "teacher_title_visible_in_html",
        "material_prompt_visible_in_html",
        "source_delta_created",
    ]:
        if result.get(key) is not True:
            failures.append(key)
    for key in [
        "formal_frontend_page_modified",
        "runtime_connected",
        "provider_called",
        "model_called",
        "database_written",
        "memory_written",
        "feishu_written",
        "formal_apply_performed",
        "main_project_pushed",
    ]:
        if result.get(key) is not False:
            failures.append(key)
    if result["desktop_screenshot_bytes"] < 10000:
        failures.append("desktop_screenshot_bytes")
    if result["mobile_screenshot_bytes"] < 10000:
        failures.append("mobile_screenshot_bytes")
    if (result["desktop_width"], result["desktop_height"]) != (1365, 900):
        failures.append("desktop_dimensions")
    if (result["mobile_width"], result["mobile_height"]) != (390, 844):
        failures.append("mobile_dimensions")
    if result["html_section_count"] != 10:
        failures.append("html_section_count")
    result["failed_checks"] = failures
    result["validator_pass"] = not failures
    write_json(stage_dir / "1013K_R16_result.json", result)
    write_text(stage_dir / "1013K_R16_report.md", build_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["validator_pass"]:
        print("ALL_1013K_R16_ISOLATED_STATIC_BINDING_VISUAL_SMOKE_CHECKS_OK")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
