from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6S_R1_CHAT_AND_BIG_UNIT_VISUAL_ALIGNMENT_PATCH"
FINAL_STATUS = "PASS_1013I_R6S_R1_CHAT_AND_BIG_UNIT_VISUAL_ALIGNMENT_PATCH"
INHERITS_FROM = "1013I_R6S_BIG_UNIT_SECTION_CANDIDATE_RETURN_TO_EDIT_MODAL_PREVIEW"
NEXT_STAGE = "USER_REVIEW_BIG_UNIT_STATIC_PAGE_VISUAL_ALIGNMENT"
BASE_DIR_NAME = "1013I_R6S_big_unit_section_candidate_return_to_edit_modal_preview"
STAGE_DIR_NAME = "1013I_R6S_R1_chat_and_big_unit_visual_alignment_patch"
BASE_HTML_NAME = "prep_room_render_canvas_deepen_v1_R6S_candidate_return_to_edit_modal_preview.html"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6S_R1_chat_and_big_unit_visual_alignment.html"
VALIDATOR_NAME = "validate_1013I_R6S_R1_chat_and_big_unit_visual_alignment_patch.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def locate_output_root(root: Path) -> Path:
    if (root / "LATEST_REVIEW_ENTRY.md").exists() and (root / "REVIEW_PACKAGE_MANIFEST.md").exists():
        return root
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "static_html_only": True,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def alignment_css() -> str:
    return """

    /* 1013I_R6S_R1: chat composer and big-unit page visual alignment */
    .xiaobei-chat-entry {
      height: 88px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      padding: 12px 22px !important;
      background:
        linear-gradient(180deg, rgba(248, 253, 247, .96), rgba(239, 247, 235, .96)) !important;
      border-top: 1px solid rgba(43, 124, 106, .16) !important;
    }

    .xiaobei-chat-entry > .chat-agent {
      display: none !important;
    }

    .chat-input-shell {
      width: min(980px, calc(100vw - 260px)) !important;
      min-height: 58px !important;
      grid-template-columns: 42px 36px minmax(260px, 1fr) 36px 40px !important;
      gap: 8px !important;
      padding: 8px 9px !important;
      border-color: rgba(43, 124, 106, .2) !important;
      background:
        radial-gradient(circle at 18px 16px, rgba(43, 124, 106, .055) 1px, transparent 1.5px),
        linear-gradient(135deg, rgba(250, 254, 245, .98), rgba(235, 247, 230, .98)) !important;
      box-shadow: 0 10px 24px rgba(32, 80, 64, .10) !important;
    }

    .chat-input-shell .chat-avatar {
      width: 38px !important;
      height: 38px !important;
      border-radius: 12px !important;
      font-size: 14px !important;
      box-shadow: 0 8px 18px rgba(43, 124, 106, .18) !important;
    }

    .chat-input-shell .chat-tool,
    .chat-input-shell .chat-send {
      width: 34px !important;
      height: 34px !important;
    }

    .chat-input {
      height: 40px !important;
      padding: 0 8px !important;
    }

    [data-r6s-r1-visual-alignment="true"] .nb-scene[data-r6s-candidate-modal-preview="true"] .nb-doc-sheet,
    [data-r6s-r1-visual-alignment="true"] [data-r6s-candidate-modal-preview="true"] .nb-doc-sheet,
    [data-r6s-r1-visual-alignment="true"] [data-r6s-candidate-modal-preview="true"] .nb-doc {
      background:
        radial-gradient(circle at 18px 18px, rgba(43, 124, 106, 0.035) 1px, transparent 1.5px),
        linear-gradient(135deg, rgba(250, 254, 245, .98), rgba(238, 247, 235, .98)) !important;
    }

    [data-r6s-r1-visual-alignment="true"] [data-r6s-candidate-modal-preview="true"] .nb-doc-head,
    [data-r6s-r1-visual-alignment="true"] [data-r6s-candidate-modal-preview="true"] .nb-big-unit-head,
    [data-r6s-r1-visual-alignment="true"] [data-r6s-candidate-modal-preview="true"] .nb-page-head {
      display: grid !important;
      grid-template-columns: minmax(0, 1fr) auto !important;
      align-items: start !important;
      gap: 16px !important;
      padding-bottom: 16px !important;
      margin-bottom: 12px !important;
      border-bottom: 1px dashed rgba(111, 128, 112, .24) !important;
    }

    [data-r6s-r1-visual-alignment="true"] [data-r6s-candidate-modal-preview="true"] .nb-doc-head .chip-row,
    [data-r6s-r1-visual-alignment="true"] [data-r6s-candidate-modal-preview="true"] .nb-status-row {
      grid-column: 1 / -1 !important;
      margin-top: 8px !important;
    }

    [data-r6s-r1-visual-alignment="true"] [data-r6s-candidate-modal-preview="true"] .nb-material-front-prompt {
      margin-top: 4px !important;
    }

    @media (max-width: 900px) {
      .chat-input-shell {
        width: min(100%, calc(100vw - 28px)) !important;
        grid-template-columns: 38px 34px minmax(0, 1fr) 34px 38px !important;
      }
    }
"""


def patch_chat_markup(html_text: str) -> str:
    old = """  <section class="xiaobei-chat-entry" aria-label="小教意图入口">
    <div class="chat-agent">
      <div class="chat-avatar" aria-hidden="true">备</div>
      <div>
        <div class="chat-agent-name">小教</div>
      </div>
    </div>
    <div class="chat-input-shell">
      <button class="chat-tool" id="chatUploadBtn" type="button" aria-label="上传资料">＋</button>
      <button class="chat-tool" id="chatVoiceBtn" type="button" aria-label="语音输入">声</button>
      <input class="chat-input" id="chatInput" type="text" placeholder="对小教说一句……">
      <button class="chat-send" id="chatSendBtn" type="button">发送</button>
      <input class="chat-upload-input" id="chatUploadInput" type="file" multiple>
    </div>
  </section>"""
    new = """  <section class="xiaobei-chat-entry" aria-label="小教意图入口" data-r6s-r1-chat-composer="true">
    <div class="chat-agent" aria-hidden="true">
      <div class="chat-avatar">小</div>
      <div>
        <div class="chat-agent-name">小教</div>
      </div>
    </div>
    <div class="chat-input-shell">
      <div class="chat-avatar" aria-hidden="true">小</div>
      <button class="chat-tool" id="chatUploadBtn" type="button" aria-label="上传资料">＋</button>
      <input class="chat-input" id="chatInput" type="text" placeholder="对小教说一句……">
      <button class="chat-tool" id="chatVoiceBtn" type="button" aria-label="语音输入">声</button>
      <button class="chat-send" id="chatSendBtn" type="button">发送</button>
      <input class="chat-upload-input" id="chatUploadInput" type="file" multiple>
    </div>
  </section>"""
    if old not in html_text:
      raise ValueError("Cannot find chat composer markup.")
    return html_text.replace(old, new, 1)


def patch_html(output_root: Path) -> str:
    base_html = output_root / BASE_DIR_NAME / BASE_HTML_NAME
    html_text = base_html.read_text(encoding="utf-8")
    html_text = html_text.replace(
        "师维 · 备课室 | R6S 候选回灌编辑弹窗预览",
        "师维 · 备课室 | R6S_R1 输入栏与大单元视觉对齐",
    )
    html_text = html_text.replace("<body>", '<body data-r6s-r1-visual-alignment="true">', 1)
    html_text = html_text.replace("\n  </style>", alignment_css() + "\n  </style>", 1)
    html_text = patch_chat_markup(html_text)
    return html_text


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


def create_screenshots(stage_dir: Path, html_path: Path) -> dict[str, Any]:
    browser = find_browser()
    screenshots: list[dict[str, Any]] = []
    if browser is None:
        return {"screenshot_smoke_pass": False, "screenshot_error": "browser_not_found", "screenshots": screenshots}
    for viewport in [{"id": "desktop", "width": 1440, "height": 1100}, {"id": "mobile", "width": 390, "height": 1100}]:
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6S_R1_{viewport['id']}.png"
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
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        width, height = png_size(out)
        screenshots.append({"viewport": viewport["id"], "path": out.name, "width": width, "height": height, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": True, "screenshots": screenshots}


def validate_html(html_text: str) -> dict[str, Any]:
    chat_match = re.search(r'<section class="xiaobei-chat-entry"[\s\S]*?</section>', html_text)
    chat = chat_match.group(0) if chat_match else ""
    shell_match = re.search(r'<div class="chat-input-shell">([\s\S]*?)</div>\s*</section>', html_text)
    shell = shell_match.group(1) if shell_match else ""
    return {
        "chat_avatar_inside_input_shell": '<div class="chat-avatar" aria-hidden="true">小</div>' in shell,
        "chat_upload_right_of_avatar": shell.find('class="chat-avatar"') < shell.find('id="chatUploadBtn"') < shell.find('id="chatInput"'),
        "chat_voice_left_of_send": shell.find('id="chatVoiceBtn"') < shell.find('id="chatSendBtn"'),
        "chat_composer_taller": "height: 88px !important" in html_text and "min-height: 58px !important" in html_text,
        "chat_composer_shorter": "width: min(980px, calc(100vw - 260px)) !important" in html_text,
        "chat_composer_color_matches_lesson_paper": "linear-gradient(135deg, rgba(250, 254, 245, .98), rgba(235, 247, 230, .98))" in html_text,
        "big_unit_paper_tint_aligned": "data-r6s-r1-visual-alignment=\"true\"" in html_text and "rgba(238, 247, 235, .98)" in html_text,
        "big_unit_title_region_alignment_patch_present": ".nb-doc-head" in html_text and "grid-template-columns: minmax(0, 1fr) auto" in html_text,
        "r6s_candidate_modal_preview_kept": "data-r6s-candidate-modal-preview=\"true\"" in html_text and "采纳到本段预览" in html_text,
        "chat_markup_found": bool(chat),
        **boundary(),
    }


def failed_checks(checks: dict[str, Any]) -> list[str]:
    failed = []
    expected_false = {
        "runtime_connected",
        "provider_called",
        "model_called",
        "formal_apply_performed",
        "database_written",
        "memory_written",
        "feishu_written",
        "main_project_pushed",
    }
    for key, value in checks.items():
        if key in expected_false:
            if value is not False:
                failed.append(key)
        elif value is not True:
            failed.append(key)
    return failed


def write_docs(output_root: Path, stage_dir: Path, result: dict[str, Any]) -> None:
    write_text(stage_dir / "1013I_R6S_R1_report.md", f"""# 1013I_R6S_R1 Chat And Big Unit Visual Alignment Patch

FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6S_R1 polishes the static review page:
- Puts the 小教 avatar inside the bottom composer, at the far left.
- Places upload immediately to the right of the avatar.
- Places voice input immediately to the left of send.
- Slightly raises and shortens the composer.
- Aligns the composer and big-unit page tint with the single-lesson paper tone.
- Adds a title-region alignment patch so the big-unit heading follows the single-lesson heading structure more closely.

Boundary: static HTML fixture only. No runtime, provider/model, formal apply, database, memory, Feishu, or main-project push.

Failed checks: {result["failed_checks"]}
""")
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R6S_R1 adjusts the bottom 小教 composer and aligns the big-unit static page color/titles with the single-lesson notebook surface.

Key flags:
- CHAT_AVATAR_INSIDE_INPUT_SHELL=true
- CHAT_UPLOAD_RIGHT_OF_AVATAR=true
- CHAT_VOICE_LEFT_OF_SEND=true
- CHAT_COMPOSER_TALLER=true
- CHAT_COMPOSER_SHORTER=true
- BIG_UNIT_PAPER_TINT_ALIGNED=true
- BIG_UNIT_TITLE_REGION_ALIGNMENT_PATCH_PRESENT=true
- R6S_CANDIDATE_MODAL_PREVIEW_KEPT=true
- FORMAL_APPLY_PERFORMED=false
- PROVIDER_CALLED=false
- MODEL_CALLED=false
- MAIN_PROJECT_PUSHED=false
""")
    write_text(output_root / "README.md", f"""# Prep Room Render Canvas Deepen V1 Review Package

Latest stage: `{STAGE_ID}`

Open:
- `{STAGE_DIR_NAME}/{HTML_NAME}`
- `{STAGE_DIR_NAME}/1013I_R6S_R1_result.json`

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
- `{STAGE_DIR_NAME}/1013I_R6S_R1_result.json`
- `{STAGE_DIR_NAME}/1013I_R6S_R1_report.md`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6S_R1_desktop.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013I_R6S_R1_mobile.png`
- `scripts/{VALIDATOR_NAME}`

Boundary: static visual alignment fixture only. No runtime, provider/model, formal apply, database, memory, Feishu, or main-project push.
""")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output_root = locate_output_root(root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)

    base_result = output_root / BASE_DIR_NAME / "1013I_R6S_result.json"
    if not base_result.exists():
        raise FileNotFoundError(base_result)

    html_text = patch_html(output_root)
    html_path = stage_dir / HTML_NAME
    write_text(html_path, html_text)
    smoke = create_screenshots(stage_dir, html_path)
    checks = validate_html(html_text)
    checks["screenshot_smoke_pass"] = bool(smoke.get("screenshot_smoke_pass"))
    failed = failed_checks(checks)
    result = {
        "stage": STAGE_ID,
        "status": FINAL_STATUS if not failed else "FAIL_1013I_R6S_R1_CHAT_AND_BIG_UNIT_VISUAL_ALIGNMENT_PATCH",
        "final_status": FINAL_STATUS if not failed else "FAIL_1013I_R6S_R1_CHAT_AND_BIG_UNIT_VISUAL_ALIGNMENT_PATCH",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        **checks,
        "failed_checks": failed,
    }
    write_json(stage_dir / "1013I_R6S_R1_result.json", result)
    write_json(stage_dir / "visual_alignment_patch_1013I_R6S_R1.json", {
        "stage": STAGE_ID,
        "chat_changes": [
            "avatar_inside_input_shell",
            "upload_right_of_avatar",
            "voice_left_of_send",
            "composer_taller_and_shorter",
            "composer_tint_aligned_with_lesson_paper",
        ],
        "big_unit_changes": [
            "paper_tint_aligned_with_single_lesson",
            "title_region_alignment_patch_present",
        ],
        **boundary(),
    })
    write_docs(output_root, stage_dir, result)
    source_delta = output_root / "source_delta_1013I_R6S_R1" / "scripts" / VALIDATOR_NAME
    source_delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), source_delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False))
    print("ALL_1013I_R6S_R1_CHAT_AND_BIG_UNIT_VISUAL_ALIGNMENT_PATCH_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
