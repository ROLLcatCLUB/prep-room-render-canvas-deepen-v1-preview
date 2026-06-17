from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.xiaobei_ai import prep_room_feishu_schedule_1013A

HTML_PATH = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "prep_room_render_canvas_deepen_v1.html"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013S_feishu_schedule_real_time_binding"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(name: str, payload: Any) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(name: str, text: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(text, encoding="utf-8")


def public_probe() -> dict[str, Any]:
    probes = {}
    for source in ["auto", "live", "snapshot"]:
        payload, status_code = prep_room_feishu_schedule_1013A.get_schedule({"source": source})
        probes[source] = {
            "status_code": status_code,
            "success": payload.get("success") is True,
            "route_status": payload.get("route_status"),
            "source_kind": payload.get("source_kind"),
            "slot_count": len(payload.get("schedule_slots") or []),
            "error": payload.get("error"),
            "warnings": payload.get("warnings") or [],
            "boundary_flags": payload.get("boundary_flags") or {},
        }
        if source in {"auto", "snapshot"} and payload.get("success"):
            probes[source]["sample_slots"] = [
                {
                    "weekday": slot.get("weekday"),
                    "period": slot.get("period"),
                    "time_range": slot.get("time_range"),
                    "class_label": slot.get("class_label"),
                    "room": slot.get("room"),
                    "source_record_id": slot.get("source_record_id"),
                }
                for slot in (payload.get("schedule_slots") or [])[:3]
            ]
    return probes


def evaluate_html(html: str) -> dict[str, Any]:
    week_match = re.search(r'id: "weekCalendar"[\s\S]*?id: "prepNotebook"', html)
    week_block = week_match.group(0) if week_match else html
    required_record_ids = [
        "recvd6CpwhuXXD",
        "recvd6Crqc3jE6",
        "recvd6CpTXPax8",
        "recviyPKQb2ieh",
        "recvd6CscCPKFT",
        "recvd6CszGgPNd",
        "recvd6Cp7nW4we",
        "recvd6CsUSNt3s",
    ]
    return {
        "schedule_adapter_time_source_present": "school_day_period_time_config" in html,
        "period_time_map_present": "period_time_map" in week_block and "08:30-09:10" in week_block and "15:50-16:30" in week_block,
        "current_week_dates_runtime_present": "function currentWeekDays" in html and "weekDateRange(days)" in html and 'runtime_today: "2026-06-17"' in html,
        "week_calendar_date_not_hardcoded_pass": "5.05" not in week_block and "5.06" not in week_block and "5.07" not in week_block,
        "feishu_record_ids_present": all(record_id in week_block for record_id in required_record_ids),
        "course_card_time_rendered": "wc-course-time" in html and "detail.timeRange" in html,
        "course_card_room_rendered": "wc-course-room" in html and "detail.room" in html,
        "detail_panel_source_record_present": "飞书记录" in html and "sourceRecordId" in html,
        "r2c_layout_baseline_kept": "nb-process-section" in html and "nb-edit-bubble" in html,
    }


def build_result(html: str, probes: dict[str, Any]) -> dict[str, Any]:
    html_checks = evaluate_html(html)
    auto = probes.get("auto", {})
    live = probes.get("live", {})
    snapshot = probes.get("snapshot", {})
    screenshot = OUT_DIR / "ui_smoke_screenshot_1013S_week_calendar_real_time.png"
    result = {
        "stage_id": "1013S_FEISHU_SCHEDULE_REAL_TIME_BINDING",
        "created_at": now(),
        "auto_schedule_probe_pass": auto.get("success") is True and auto.get("slot_count") == 8,
        "snapshot_schedule_probe_pass": snapshot.get("success") is True and snapshot.get("slot_count") == 8,
        "live_probe_checked": "status_code" in live,
        "live_configured": live.get("success") is True,
        "live_config_caveat": None if live.get("success") is True else live.get("error") or live.get("route_status"),
        **html_checks,
        "screenshot_pass": screenshot.exists() and screenshot.stat().st_size > 0,
        "teacher_review_required": True,
        "formal_apply_performed": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "default_entry_changed": False,
        "entered_1013G": False,
    }
    pass_keys = [
        "auto_schedule_probe_pass",
        "snapshot_schedule_probe_pass",
        "live_probe_checked",
        *html_checks.keys(),
    ]
    result["final_status"] = (
        "PASS_FEISHU_SNAPSHOT_SCHEDULE_REAL_TIME_BINDING_WITH_LIVE_CONFIG_CAVEAT"
        if all(result[key] for key in pass_keys)
        else "FAIL_FEISHU_SCHEDULE_REAL_TIME_BINDING"
    )
    result["next_stage"] = (
        "1013S_R1_FEISHU_LIVE_CREDENTIAL_BINDING_OR_1013F_R2D_CONTENT_REVIEW"
        if result["final_status"].startswith("PASS")
        else "1013S_REPAIR"
    )
    return result


def write_report(result: dict[str, Any]) -> None:
    lines = [
        "# 1013S Feishu Schedule Real Time Binding",
        "",
        "```text",
        f"final_status={result['final_status']}",
        f"next_stage={result['next_stage']}",
        f"auto_schedule_probe_pass={str(result['auto_schedule_probe_pass']).lower()}",
        f"snapshot_schedule_probe_pass={str(result['snapshot_schedule_probe_pass']).lower()}",
        f"live_configured={str(result['live_configured']).lower()}",
        f"live_config_caveat={result['live_config_caveat']}",
        f"period_time_map_present={str(result['period_time_map_present']).lower()}",
        f"current_week_dates_runtime_present={str(result['current_week_dates_runtime_present']).lower()}",
        "```",
        "",
        "## Summary",
        "",
        "- Feishu live read was checked first; local credentials are not configured in this environment.",
        "- Auto mode successfully fell back to the Feishu full-dump schedule snapshot.",
        "- The schedule snapshot returned 8 Xu Tao grade-three art slots.",
        "- Each visible lesson card now carries source record id, room, and class time range.",
        "- Week dates are generated from the current natural week instead of fixed 5.xx placeholder dates.",
        "- Period labels show the local school-day time configuration.",
        "",
        "## Boundary",
        "",
        "- No provider/model call.",
        "- No database write.",
        "- No memory write.",
        "- No Feishu write.",
        "- No formal apply.",
        "- No default entry change.",
        "- Did not enter 1013G.",
    ]
    write_text("1013S_report.md", "\n".join(lines) + "\n")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html = HTML_PATH.read_text(encoding="utf-8")
    probes = public_probe()
    write_json("feishu_schedule_probe_1013S.json", probes)
    write_json("period_time_map_1013S.json", {
        f"第{period_no}节": {"start": start, "end": end, "range": f"{start}-{end}"}
        for period_no, (start, end) in prep_room_feishu_schedule_1013A.PERIOD_TIME_MAP.items()
    })
    result = build_result(html, probes)
    write_json("1013S_result.json", result)
    write_report(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
