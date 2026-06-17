from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013A_FEISHU_FORMAL_SCHEDULE_READONLY_ADAPTER"
BASE_PATH = "/api/xiaobei/prep-room"
DEFAULT_TABLE_ID = "tbl7OxfE4YPSE6GU"
DEFAULT_DUMP_PATH = Path(r"D:\Documents\New project\feishu_full_dump\main\tbl7OxfE4YPSE6GU.json")
DEFAULT_TEACHER = "徐涛"
DEFAULT_SUBJECT = "美术"
DEFAULT_GRADE = "三年级"
DEFAULT_SEMESTER = "2025-2026学年第二学期"

DAY_ID = {
    "周一": "mon",
    "周二": "tue",
    "周三": "wed",
    "周四": "thu",
    "周五": "fri",
    "周六": "sat",
    "周日": "sun",
}

PERIOD_TIME_MAP = {
    1: ("08:30", "09:10"),
    2: ("09:20", "10:00"),
    3: ("10:20", "11:00"),
    4: ("11:10", "11:50"),
    5: ("13:20", "14:00"),
    6: ("14:10", "14:50"),
    7: ("15:00", "15:40"),
    8: ("15:50", "16:30"),
}

LESSON_CONTEXT = {
    "lesson_code": "1-2",
    "lesson_title": "色彩的感觉",
    "unit": "第一单元 多变的色彩",
    "duration_minutes": 40,
    "prep_assistant": "小备",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        if "text" in value:
            return str(value.get("text") or "").strip()
        if "name" in value:
            return str(value.get("name") or "").strip()
        return " ".join(part for part in (_text(item) for item in value.values()) if part).strip()
    if isinstance(value, list):
        return " ".join(part for part in (_text(item) for item in value) if part).strip()
    return str(value).strip()


def _env_value(names: tuple[str, ...]) -> str:
    for name in names:
        value = (os.environ.get(name) or "").strip()
        if value:
            return value
    return ""


def _dump_path() -> Path:
    configured = _env_value(("XIAOBEI_FEISHU_SCHEDULE_DUMP_PATH", "FEISHU_SCHEDULE_DUMP_PATH"))
    if configured:
        return Path(configured)
    dump_dir = _env_value(("XIAOBEI_FEISHU_FULL_DUMP_DIR", "FEISHU_FULL_DUMP_DIR"))
    if dump_dir:
        return Path(dump_dir) / "tbl7OxfE4YPSE6GU.json"
    return DEFAULT_DUMP_PATH


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _tenant_token() -> tuple[str, str]:
    token = _env_value(("FEISHU_TENANT_ACCESS_TOKEN", "TENANT_ACCESS_TOKEN"))
    if token:
        return token, "tenant_token_env"
    app_id = _env_value(("FEISHU_APP_ID", "LARK_APP_ID"))
    app_secret = _env_value(("FEISHU_APP_SECRET", "LARK_APP_SECRET"))
    if not app_id or not app_secret:
        return "", "missing_app_credentials"
    body = json.dumps({"app_id": app_id, "app_secret": app_secret}, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=12) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if payload.get("code") == 0 and payload.get("tenant_access_token"):
        return str(payload["tenant_access_token"]), "app_credentials_env"
    return "", f"tenant_token_error_{payload.get('code', 'unknown')}"


def _live_config() -> dict[str, Any]:
    app_token = _env_value(
        (
            "FEISHU_SCHEDULE_APP_TOKEN",
            "FEISHU_TEACHER_SCHEDULE_APP_TOKEN",
            "FEISHU_BITABLE_APP_TOKEN",
            "FEISHU_APP_TOKEN",
        )
    )
    table_id = _env_value(
        (
            "FEISHU_SCHEDULE_TABLE_ID",
            "FEISHU_TEACHER_SCHEDULE_TABLE_ID",
            "FEISHU_TABLE_ID",
        )
    ) or DEFAULT_TABLE_ID
    token, token_source = _tenant_token()
    return {
        "configured": bool(app_token and table_id and token),
        "app_token_present": bool(app_token),
        "table_id_present": bool(table_id),
        "tenant_token_present": bool(token),
        "token_source": token_source,
        "_app_token": app_token,
        "_table_id": table_id,
        "_token": token,
    }


def _list_live_records() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    config = _live_config()
    if not config["configured"]:
        return [], {
            "success": False,
            "code": "feishu_live_not_configured",
            "public_config": {k: v for k, v in config.items() if not k.startswith("_")},
        }
    app_token = config["_app_token"]
    table_id = config["_table_id"]
    token = config["_token"]
    records: list[dict[str, Any]] = []
    page_token = ""
    started = time.perf_counter()
    while True:
        params = {"page_size": "500"}
        if page_token:
            params["page_token"] = page_token
        query = urllib.parse.urlencode(params)
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records?{query}"
        request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"}, method="GET")
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
        if payload.get("code") != 0:
            return records, {
                "success": False,
                "code": f"feishu_live_error_{payload.get('code', 'unknown')}",
                "message": str(payload.get("msg") or "")[:160],
            }
        data = payload.get("data") or {}
        items = data.get("items") or []
        records.extend(items if isinstance(items, list) else [])
        page_token = str(data.get("page_token") or "")
        if not data.get("has_more") or not page_token:
            break
    return records, {
        "success": True,
        "code": "feishu_live_read_ok",
        "latency_ms": round((time.perf_counter() - started) * 1000),
        "record_count": len(records),
        "public_config": {k: v for k, v in config.items() if not k.startswith("_")},
    }


def _list_snapshot_records() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    path = _dump_path()
    if not path.exists():
        return [], {"success": False, "code": "snapshot_missing", "path": str(path)}
    payload = _read_json(path)
    records = payload.get("records") or []
    return records if isinstance(records, list) else [], {
        "success": True,
        "code": "snapshot_read_ok",
        "table_id": payload.get("table_id") or DEFAULT_TABLE_ID,
        "table_name": payload.get("table_name") or "教师课表",
        "record_count": len(records) if isinstance(records, list) else 0,
        "dump_last_modified": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0).isoformat(),
    }


def _record_fields(record: dict[str, Any]) -> dict[str, Any]:
    fields = record.get("fields") if isinstance(record, dict) else {}
    return fields if isinstance(fields, dict) else {}


def _record_id(record: dict[str, Any]) -> str:
    return _text(record.get("record_id")) or _text(record.get("id"))


def _grade_prefix(grade: str) -> str:
    if "三" in grade:
        return "三"
    if "四" in grade:
        return "四"
    if "五" in grade:
        return "五"
    if "六" in grade:
        return "六"
    return grade[:1]


def _compact_class_label(class_name: str) -> str:
    text = class_name.replace("（", "(").replace("）", ")").replace(" ", "")
    text = text.replace("三年级", "三").replace("四年级", "四").replace("五年级", "五").replace("六年级", "六")
    text = text.replace("(", "").replace(")", "")
    return text


def _period_number(period: str) -> int:
    digits = "".join(ch for ch in period if ch.isdigit())
    return int(digits) if digits else 0


def _period_time(period_no: int) -> dict[str, str]:
    start, end = PERIOD_TIME_MAP.get(period_no, ("", ""))
    return {
        "start_time": start,
        "end_time": end,
        "time_range": f"{start}-{end}" if start and end else "",
        "time_source": "school_day_period_time_config",
    }


def _filter_records(records: list[dict[str, Any]], filters: dict[str, str]) -> list[dict[str, Any]]:
    grade_marker = _grade_prefix(filters["grade"])
    matched = []
    for record in records:
        fields = _record_fields(record)
        teacher = _text(fields.get("授课教师"))
        subject = _text(fields.get("课程名称"))
        semester = _text(fields.get("学期"))
        class_name = _text(fields.get("班级"))
        if filters["teacher"] and filters["teacher"] not in teacher:
            continue
        if filters["subject"] and filters["subject"] != subject:
            continue
        if filters["semester"] and filters["semester"] != semester:
            continue
        if filters["grade"] and not class_name.startswith(grade_marker):
            continue
        matched.append(record)
    return matched


def _slot_from_record(record: dict[str, Any], source_kind: str) -> dict[str, Any]:
    fields = _record_fields(record)
    weekday = _text(fields.get("星期"))
    period = _text(fields.get("节次"))
    class_name = _text(fields.get("班级"))
    period_no = _period_number(period)
    day_id = DAY_ID.get(weekday, "")
    record_id = _record_id(record)
    class_label = _compact_class_label(class_name)
    time_info = _period_time(period_no)
    return {
        "slot_id": f"fs-{record_id or weekday + period + class_name}",
        "source_record_id": record_id,
        "source_table_id": DEFAULT_TABLE_ID,
        "source_kind": source_kind,
        "teacher_name": _text(fields.get("授课教师")),
        "semester": _text(fields.get("学期")),
        "subject": _text(fields.get("课程名称")),
        "grade": DEFAULT_GRADE,
        "class_name": class_name,
        "class_label": class_label,
        "weekday": weekday,
        "weekday_id": day_id,
        "period": period,
        "period_no": period_no,
        **time_info,
        "room": _text(fields.get("教室")),
        "lesson_ref": deepcopy(LESSON_CONTEXT),
        "package_status": "正式课表 · 待备课",
    }


def _sort_slots(slots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    day_order = {day: index for index, day in enumerate(["mon", "tue", "wed", "thu", "fri", "sat", "sun"])}
    return sorted(slots, key=lambda item: (day_order.get(item.get("weekday_id"), 99), item.get("period_no") or 99, item.get("class_label") or ""))


def _build_week_calendar_patch(slots: list[dict[str, Any]], source_kind: str) -> dict[str, Any]:
    slot_map: dict[str, list[dict[str, Any]]] = {}
    prep_items: list[dict[str, str]] = []
    for slot in slots:
        if not slot["weekday_id"] or not slot["period_no"]:
            continue
        key = f"p{slot['period_no']}-{slot['weekday_id']}"
        item = {
            "id": f"wc-{slot['slot_id']}",
            "type": "lesson",
            "classLabel": slot["class_label"],
            "code": slot["lesson_ref"]["lesson_code"],
            "title": slot["lesson_ref"]["lesson_title"],
            "packageStatus": slot["package_status"],
            "sourceRecordId": slot["source_record_id"],
            "room": slot["room"],
            "sourceKind": source_kind,
            "startTime": slot.get("start_time", ""),
            "endTime": slot.get("end_time", ""),
            "timeRange": slot.get("time_range", ""),
            "timeSource": slot.get("time_source", ""),
        }
        slot_map.setdefault(key, []).append(item)
        prep_items.append(
            {
                "title": f"{slot['weekday']} {slot['period']} {slot['class_label']}《{slot['lesson_ref']['lesson_title']}》",
                "time": slot.get("time_range", ""),
                "status": "进入备课本候选",
            }
        )
    return {
        "term": DEFAULT_SEMESTER,
        "active_grade": DEFAULT_GRADE,
        "source_badge": "飞书正式课表" if source_kind == "feishu_live_readonly" else "飞书课表快照",
        "period_time_map": {
            f"第{period_no}节": {"start": start, "end": end, "range": f"{start}-{end}"}
            for period_no, (start, end) in PERIOD_TIME_MAP.items()
        },
        "time_source": "school_day_period_time_config",
        "slots": slot_map,
        "prep_items": prep_items[:8],
        "alerts": [
            f"已读取{len(slots)}条{DEFAULT_TEACHER}老师{DEFAULT_GRADE}{DEFAULT_SUBJECT}课表。",
            "课表只进入备课室预览，不写回飞书。",
            "课题仍由备课本当前课例和教学工作计划提供，等待教师确认。",
        ],
        "package_summary": [
            ["课表来源", "正式" if source_kind == "feishu_live_readonly" else "快照"],
            ["本周课位", f"{len(slots)}节"],
            ["待备课", f"{len(slots)}项"],
            ["写回", "0次"],
        ],
    }


def _boundary(source_kind: str, live_meta: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "readonly": True,
        "feishu_live_read_allowed": True,
        "feishu_api_called": source_kind == "feishu_live_readonly",
        "feishu_written": False,
        "database_written": False,
        "memory_written": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "frontend_secret_exposed": False,
        "tenant_token_exposed": False,
        "live_meta_public": {k: v for k, v in (live_meta or {}).items() if k not in {"message"}},
    }


def _filters_from_payload(payload: dict[str, Any] | None) -> dict[str, str]:
    payload = payload if isinstance(payload, dict) else {}
    return {
        "teacher": _text(payload.get("teacher") or os.environ.get("XIAOBEI_PREP_ROOM_TEACHER") or DEFAULT_TEACHER),
        "subject": _text(payload.get("subject") or os.environ.get("XIAOBEI_PREP_ROOM_SUBJECT") or DEFAULT_SUBJECT),
        "grade": _text(payload.get("grade") or os.environ.get("XIAOBEI_PREP_ROOM_GRADE") or DEFAULT_GRADE),
        "semester": _text(payload.get("semester") or os.environ.get("XIAOBEI_PREP_ROOM_SEMESTER") or DEFAULT_SEMESTER),
    }


def get_schedule(payload: dict[str, Any] | None = None) -> tuple[dict[str, Any], int]:
    payload = payload if isinstance(payload, dict) else {}
    requested_source = _text(payload.get("source") or os.environ.get("XIAOBEI_FEISHU_SCHEDULE_SOURCE") or "auto").lower()
    if requested_source not in {"auto", "live", "snapshot"}:
        requested_source = "auto"
    filters = _filters_from_payload(payload)
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    source_kind = "feishu_full_dump_snapshot"
    source_meta: dict[str, Any] = {}

    if requested_source in {"auto", "live"}:
        try:
            live_records, live_meta = _list_live_records()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
            live_records, live_meta = [], {"success": False, "code": "feishu_live_request_failed", "message": str(exc)[:160]}
        if live_meta.get("success"):
            records = live_records
            source_kind = "feishu_live_readonly"
            source_meta = live_meta
        elif requested_source == "live":
            return {
                "success": False,
                "stage_id": STAGE_ID,
                "route_status": "blocked_missing_or_failed_live_feishu",
                "source_mode_requested": requested_source,
                "source_kind": "feishu_live_readonly",
                "filters": filters,
                "error": live_meta.get("code") or "feishu_live_unavailable",
                "boundary_flags": _boundary("feishu_live_readonly", live_meta),
            }, 424
        else:
            warnings.append(live_meta.get("code") or "feishu_live_unavailable")

    if not records:
        snapshot_records, snapshot_meta = _list_snapshot_records()
        records = snapshot_records
        source_kind = "feishu_full_dump_snapshot"
        source_meta = snapshot_meta
        if not snapshot_meta.get("success"):
            return {
                "success": False,
                "stage_id": STAGE_ID,
                "route_status": "snapshot_unavailable",
                "source_mode_requested": requested_source,
                "source_kind": source_kind,
                "filters": filters,
                "error": snapshot_meta.get("code") or "snapshot_unavailable",
                "boundary_flags": _boundary(source_kind),
            }, 404

    matched = _filter_records(records, filters)
    slots = _sort_slots([_slot_from_record(record, source_kind) for record in matched])
    patch = _build_week_calendar_patch(slots, source_kind)
    response = {
        "success": True,
        "stage_id": STAGE_ID,
        "route_status": "readonly_schedule_adapter_active",
        "generated_at": _now_iso(),
        "source_mode_requested": requested_source,
        "source_kind": source_kind,
        "source_meta": source_meta,
        "warnings": warnings,
        "filters": filters,
        "teacher_profile": {
            "teacher_name": filters["teacher"],
            "subject": filters["subject"],
            "grade": filters["grade"],
            "semester": filters["semester"],
            "schedule_slot_count": len(slots),
        },
        "schedule_slots": slots,
        "week_calendar_patch": patch,
        "prep_room_binding": {
            "binding_status": "ready_for_prep_notebook_context",
            "current_lesson": deepcopy(LESSON_CONTEXT),
            "teacher_review_required": True,
            "formal_apply_performed": False,
        },
        "boundary_flags": _boundary(source_kind, source_meta),
    }
    return response, 200


def status() -> tuple[dict[str, Any], int]:
    live = _live_config()
    dump = _dump_path()
    return {
        "success": True,
        "stage_id": STAGE_ID,
        "route_status": "readonly_schedule_adapter_available",
        "live_config": {k: v for k, v in live.items() if not k.startswith("_")},
        "snapshot_available": dump.exists(),
        "default_source": os.environ.get("XIAOBEI_FEISHU_SCHEDULE_SOURCE", "auto"),
        "boundary_flags": _boundary("feishu_full_dump_snapshot"),
    }, 200


def register_routes(bp, cors_preflight):
    from flask import jsonify, request

    @bp.route(f"{BASE_PATH}/schedule/status", methods=["GET", "OPTIONS"])
    def prep_room_schedule_status_route_1013A():
        if request.method == "OPTIONS":
            return cors_preflight()
        response, status_code = status()
        return jsonify(response), status_code

    @bp.route(f"{BASE_PATH}/schedule", methods=["GET", "POST", "OPTIONS"])
    def prep_room_schedule_route_1013A():
        if request.method == "OPTIONS":
            return cors_preflight()
        payload = request.get_json(silent=True) if request.method == "POST" else dict(request.args)
        response, status_code = get_schedule(payload)
        return jsonify(response), status_code
