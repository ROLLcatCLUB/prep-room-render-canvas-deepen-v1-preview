import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_DIR = ROOT / "docs" / "experiments" / "agent_capability_spike_0952B"
AUDIT_REPORT = ROOT / "docs" / "audit" / "agent_capability_spike_0952B_report.md"

INPUT_FILE = EXPERIMENT_DIR / "agent_input_0952B.json"
RAW_FILE = EXPERIMENT_DIR / "agent_raw_response_0952B.md"
FINAL_FILE = EXPERIMENT_DIR / "agent_final_lesson_design_0952B.md"
SELF_REVIEW_FILE = EXPERIMENT_DIR / "agent_self_review_0952B.md"
RESULT_FILE = EXPERIMENT_DIR / "agent_result_0952B.json"

STAGE_ID = "0952B_AGENT_CAPABILITY_EXPERIENCE_SPIKE"
STAGE_TYPE = "agent_capability_spike_only"
STATUS_READY = "AGENT_EXPERIENCE_READY"
STATUS_PROVIDER_NOT_CONFIGURED = "FAIL_PROVIDER_NOT_CONFIGURED"
STATUS_PROVIDER_TIMEOUT = "FAIL_PROVIDER_TIMEOUT"
STATUS_PROVIDER_CALL_FAILED = "FAIL_PROVIDER_CALL_FAILED"

FORBIDDEN_FLAGS = {
    "mock_used": False,
    "hardcoded_response_used": False,
    "memory_read": False,
    "memory_write": False,
    "feishu_writeback": False,
    "formal_scoring": False,
    "server_deploy": False,
    "database_write": False,
    "production_endpoint_created": False,
    "frontend_modified": False,
    "backend_route_modified": False,
}


def load_dotenv_without_override() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def first_env(names):
    for name in names:
        value = (os.environ.get(name) or "").strip()
        if value:
            return name, value
    return "", ""


def normalize_base_url(value):
    text = str(value or "").strip().rstrip("/")
    lower = text.lower()
    if lower.endswith("/chat/completions"):
        return text[: -len("/chat/completions")]
    if lower.endswith("/text/chatcompletion_v2"):
        return text[: -len("/text/chatcompletion_v2")]
    return text


def resolve_provider_config():
    minimax_name, minimax_key = first_env(["MINIAMX_API_KEY", "MINIMAX_API_KEY"])
    openai_name, openai_key = first_env(["OPENAI_API_KEY"])
    if minimax_key:
        base_url = normalize_base_url(
            os.environ.get("MINIAMX_BASE_URL")
            or os.environ.get("MINIMAX_BASE_URL")
            or os.environ.get("MINIAMX_API_BASE")
            or os.environ.get("MINIMAX_API_BASE")
            or "https://api.minimaxi.com/v1"
        )
        model = (
            os.environ.get("XIAOBEI_AGENT_SPIKE_MODEL")
            or os.environ.get("XIAOBEI_AI_MODEL_DEFAULT")
            or "MiniMax-M3"
            or os.environ.get("MINIAMX_MODEL")
            or os.environ.get("MINIMAX_MODEL")
        ).strip()
        return {
            "provider_configured": True,
            "provider_family": "minimax_openai_compatible",
            "credential_env": minimax_name,
            "api_key": minimax_key,
            "base_url": base_url,
            "model": model,
        }
    if openai_key:
        base_url = normalize_base_url(os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1")
        model = (
            os.environ.get("XIAOBEI_AGENT_SPIKE_MODEL")
            or os.environ.get("XIAOBEI_AI_MODEL_DEFAULT")
            or os.environ.get("OPENAI_MODEL")
            or "gpt-4.1-mini"
        ).strip()
        return {
            "provider_configured": True,
            "provider_family": "openai_compatible",
            "credential_env": openai_name,
            "api_key": openai_key,
            "base_url": base_url,
            "model": model,
        }
    return {
        "provider_configured": False,
        "provider_family": "",
        "credential_env": "",
        "api_key": "",
        "base_url": "",
        "model": "",
    }


def build_agent_input():
    return {
        "stage_id": STAGE_ID,
        "stage_type": STAGE_TYPE,
        "business_type": "lesson_design",
        "textbook": "苏少版三年级美术",
        "topic": "青绿中国色",
        "duration_minutes": 40,
        "teacher_need": (
            "希望学生理解青绿山水中石青、石绿、藤黄、赭石的设色规律，"
            "能观察《千里江山图》的色彩节奏，并迁移到自己的山水设色练习中。"
        ),
        "required_outputs": [
            "教学目标",
            "教学重难点",
            "课堂流程",
            "教师关键提问",
            "学生活动",
            "板书/大屏设计",
            "评价方式",
            "可能问题与调整",
            "自我质量检查",
            "二次修订版",
        ],
        "boundaries": {
            "mock_allowed": False,
            "hardcoded_response_allowed": False,
            "memory_allowed": False,
            "feishu_writeback_allowed": False,
            "formal_scoring_allowed": False,
            "server_deploy_allowed": False,
            "production_endpoint_allowed": False,
        },
    }


def build_prompt(agent_input):
    system_prompt = (
        "你是小备 Agent，一名懂小学美术课堂的备课助手。"
        "你要真实完成备课任务，而不是解释你会怎么做。"
        "回答必须面向教师可直接阅读和二次修改，避免空泛口号。"
        "不要编造真实学生数据，不要提及系统密钥、后端、memory、Feishu 或部署。"
    )
    user_prompt = f"""
请完成一次真实备课能力试跑。

业务类型：{agent_input["business_type"]}
教材：{agent_input["textbook"]}
课题：{agent_input["topic"]}
课时：{agent_input["duration_minutes"]}分钟
教师需求：{agent_input["teacher_need"]}

你必须按下面结构输出：

# 一、需求理解
# 二、课时设计初稿
## 1. 教学目标
## 2. 教学重难点
## 3. 课堂流程
## 4. 教师关键提问
## 5. 学生活动
## 6. 板书/大屏设计
## 7. 评价方式
## 8. 可能问题与调整
# 三、自我质量检查
请指出初稿的问题，不要只说优点。
# 四、二次修订版
请给出一份教师可直接拿去改的完整修订稿。
# 五、质量自评
围绕“教学目标是否准确、流程是否可上课、美术学科逻辑、青绿设色规律、教师语言、学生任务、评价设计、课堂可操作性、是否像小备、是否值得继续产品化”逐项判断。
""".strip()
    return system_prompt, user_prompt


def resolve_endpoint(base_url):
    lower = base_url.lower()
    if lower.endswith("/text/chatcompletion_v2"):
        return ""
    if "api.minimaxi.com" in lower:
        return "/text/chatcompletion_v2"
    return "/chat/completions"


def call_provider_once(config, system_prompt, user_prompt):
    max_tokens = int(os.environ.get("XIAOBEI_AGENT_SPIKE_MAX_TOKENS") or "3000")
    timeout_seconds = int(os.environ.get("XIAOBEI_AGENT_SPIKE_TIMEOUT_SECONDS") or "240")
    body = {
        "model": config["model"],
        "temperature": 0.35,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['api_key']}",
    }
    endpoint = resolve_endpoint(config["base_url"])
    request = urllib.request.Request(
        f"{config['base_url']}{endpoint}",
        data=data,
        headers=headers,
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            response_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:800]
        raise RuntimeError(f"provider_http_{exc.code}: {redact_sensitive(detail)}") from exc
    except Exception as exc:
        message = str(exc)
        if "timed out" in message.lower() or isinstance(exc, TimeoutError):
            raise TimeoutError("provider_timeout: The read operation timed out") from exc
        raise RuntimeError(f"provider_request_failed: {redact_sensitive(message)}") from exc

    latency_ms = round((time.perf_counter() - started) * 1000)
    parsed = json.loads(response_body)
    if isinstance(parsed, dict):
        base_resp = parsed.get("base_resp")
        if isinstance(base_resp, dict) and str(base_resp.get("status_code", "0")) not in {"", "0", "None"}:
            raise RuntimeError(f"provider_business_error: {redact_sensitive(str(base_resp))}")
        content = ((((parsed.get("choices") or [])[0] or {}).get("message") or {}).get("content") or "")
        if not content and isinstance(parsed.get("reply"), str):
            content = parsed["reply"]
    else:
        content = ""
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("provider_empty_response")
    return content.strip(), latency_ms


def call_provider(config, system_prompt, user_prompt):
    attempts = int(os.environ.get("XIAOBEI_AGENT_SPIKE_RETRIES") or "1") + 1
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            raw_text, latency_ms = call_provider_once(config, system_prompt, user_prompt)
            return raw_text, latency_ms, attempt
        except TimeoutError as exc:
            last_error = exc
            if attempt >= attempts:
                raise
            time.sleep(1.5)
        except Exception as exc:
            last_error = exc
            if attempt >= attempts:
                raise
            time.sleep(1.5)
    raise RuntimeError(str(last_error or "provider_call_failed"))


def redact_sensitive(text):
    text = str(text or "")
    patterns = [
        (r"Bearer\s+[A-Za-z0-9._\-]+", "Bearer <REDACTED>"),
        (r"sk-[A-Za-z0-9._\-]{8,}", "sk-<REDACTED>"),
        (r"(?i)(api[_-]?key[\"'\s:=]+)[A-Za-z0-9._\-]+", r"\1<REDACTED>"),
        (r"(?i)(token[\"'\s:=]+)[A-Za-z0-9._\-]+", r"\1<REDACTED>"),
        (r"C:\\Users\\Administrator", "<USER_HOME_REDACTED>"),
    ]
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    return text


def extract_section(raw_text, start_heading, stop_headings):
    start = raw_text.find(start_heading)
    if start < 0:
        return ""
    end = len(raw_text)
    for heading in stop_headings:
        idx = raw_text.find(heading, start + len(start_heading))
        if idx >= 0:
            end = min(end, idx)
    return raw_text[start:end].strip()


def build_quality_review(raw_text, success):
    checks = [
        ("教学目标是否准确", "教学目标"),
        ("教学流程是否可上课", "课堂流程"),
        ("是否体现美术学科逻辑", "美术"),
        ("是否体现青绿山水设色规律", "石青"),
        ("是否有教师语言", "教师关键提问"),
        ("是否有学生任务", "学生活动"),
        ("是否有评价设计", "评价方式"),
        ("是否有课堂可操作性", "40分钟"),
        ("是否比普通 GPT 更像小备", "二次修订版"),
        ("是否值得继续产品化", "质量自评"),
    ]
    rows = []
    for item, token in checks:
        passed = bool(success and token in raw_text)
        rows.append(
            {
                "item": item,
                "status": "needs_human_review" if success else "not_available_provider_not_configured",
                "auto_signal_present": passed,
                "note": "已在模型输出中找到相关结构或关键词。" if passed else "需要人工复核或等待真实 provider 输出。",
            }
        )
    return rows


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def generate_report(result, agent_input, raw_text, final_text, self_review_text):
    quality_lines = [
        "| 项目 | 状态 | 自动信号 | 说明 |",
        "| --- | --- | --- | --- |",
    ]
    for row in result["quality_review"]:
        quality_lines.append(
            f"| {row['item']} | {row['status']} | {str(row['auto_signal_present']).lower()} | {row['note']} |"
        )
    provider_line = "已真实调用 provider。" if result["provider_called"] else "未调用 provider：provider 未配置或调用不可用。"
    report = f"""# {result['stage_id']} Report

## 1. 定位

{result['stage_id']} 是 agent_capability_spike_only。它不测试 Demo 页面，不测试 mock_safe_response，不做产品封板，不创建正式 endpoint。

## 2. Provider 调用结果

- provider_configured={str(result['provider_configured']).lower()}
- provider_called={str(result['provider_called']).lower()}
- provider_family={result.get('provider_family') or ''}
- model_name={result.get('model_name') or ''}
- final_status={result['final_status']}

{provider_line}

## 3. 输入任务

- 业务类型：{agent_input['business_type']}
- 教材：{agent_input['textbook']}
- 课题：{agent_input['topic']}
- 课时：{agent_input['duration_minutes']} 分钟
- 教师需求：{agent_input['teacher_need']}

## 4. 输出摘要

- raw_response_file={RAW_FILE.relative_to(ROOT).as_posix()}
- final_lesson_design_file={FINAL_FILE.relative_to(ROOT).as_posix()}
- self_review_file={SELF_REVIEW_FILE.relative_to(ROOT).as_posix()}

## 5. 质量评审表

{chr(10).join(quality_lines)}

## 6. 禁止项

- mock_used=false
- hardcoded_response_used=false
- memory_read=false
- memory_write=false
- feishu_writeback=false
- formal_scoring=false
- server_deploy=false
- database_write=false
- production_endpoint_created=false
- frontend_modified=false
- backend_route_modified=false

## 7. Caveat

{result['stage_id']} 只保存本地实验文件。若 provider_called=false，则本轮没有得到真实 Agent 出活质量，只能说明真实 provider sandbox 未配置或不可用。严禁把失败文件当作备课质量结果。

## 8. 结论

{result['stage_id']} = {result['final_status']}
"""
    write_text(AUDIT_REPORT, report)


def main():
    load_dotenv_without_override()
    EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)
    agent_input = build_agent_input()
    write_json(INPUT_FILE, agent_input)

    config = resolve_provider_config()
    provider_called = False
    raw_text = ""
    final_text = ""
    self_review_text = ""
    failure_reason = ""
    latency_ms = None

    if not config["provider_configured"]:
        failure_reason = "provider_not_configured: missing MINIAMX_API_KEY / MINIMAX_API_KEY or OPENAI_API_KEY"
        raw_text = "# Provider not configured\n\n真实 provider 未配置，本轮没有调用模型，也没有生成课时设计。"
        final_text = "真实 provider 未配置；未生成课时设计。"
        self_review_text = "真实 provider 未配置；未产生 Agent 自我检查。"
        final_status = STATUS_PROVIDER_NOT_CONFIGURED
    else:
        system_prompt, user_prompt = build_prompt(agent_input)
        try:
            raw_text, latency_ms, attempts_used = call_provider(config, system_prompt, user_prompt)
            provider_called = True
            final_text = extract_section(raw_text, "# 四、二次修订版", ["# 五、质量自评"]) or raw_text
            self_review_text = extract_section(raw_text, "# 三、自我质量检查", ["# 四、二次修订版"]) or extract_section(raw_text, "# 五、质量自评", [])
            if not self_review_text:
                self_review_text = "模型输出未能按标题解析出自我检查段落，请人工查看 raw response。"
            final_status = STATUS_READY
        except TimeoutError as exc:
            failure_reason = str(exc)
            raw_text = f"# Provider call failed\n\n{redact_sensitive(failure_reason)}"
            final_text = "真实 provider 调用超时；未生成可评估课时设计。"
            self_review_text = "真实 provider 调用超时；未产生 Agent 自我检查。"
            final_status = STATUS_PROVIDER_TIMEOUT
        except Exception as exc:
            failure_reason = str(exc)
            raw_text = f"# Provider call failed\n\n{redact_sensitive(failure_reason)}"
            final_text = "真实 provider 调用失败；未生成可评估课时设计。"
            self_review_text = "真实 provider 调用失败；未产生 Agent 自我检查。"
            final_status = STATUS_PROVIDER_CALL_FAILED

    write_text(RAW_FILE, raw_text)
    write_text(FINAL_FILE, final_text)
    write_text(SELF_REVIEW_FILE, self_review_text)

    result = {
        "stage_id": STAGE_ID,
        "stage_type": STAGE_TYPE,
        "business_type": "lesson_design",
        "topic": "青绿中国色",
        "provider_configured": bool(config["provider_configured"]),
        "provider_called": bool(provider_called),
        "provider_family": config.get("provider_family") or "",
        "model_name": config.get("model") or "",
        "credential_env_present": bool(config.get("credential_env")),
        "latency_ms": latency_ms,
        "timeout_seconds": int(os.environ.get("XIAOBEI_AGENT_SPIKE_TIMEOUT_SECONDS") or "240"),
        "max_tokens": int(os.environ.get("XIAOBEI_AGENT_SPIKE_MAX_TOKENS") or "3000"),
        "retry_count": int(os.environ.get("XIAOBEI_AGENT_SPIKE_RETRIES") or "1"),
        "attempts_used": locals().get("attempts_used", 0),
        **FORBIDDEN_FLAGS,
        "result_persisted_to_local_experiment_files": True,
        "input_file": INPUT_FILE.relative_to(ROOT).as_posix(),
        "raw_response_file": RAW_FILE.relative_to(ROOT).as_posix(),
        "final_lesson_design_file": FINAL_FILE.relative_to(ROOT).as_posix(),
        "self_review_file": SELF_REVIEW_FILE.relative_to(ROOT).as_posix(),
        "audit_report_file": AUDIT_REPORT.relative_to(ROOT).as_posix(),
        "failure_reason": redact_sensitive(failure_reason),
        "quality_review": build_quality_review(raw_text, provider_called),
        "final_status": final_status,
    }
    write_json(RESULT_FILE, result)
    generate_report(result, agent_input, raw_text, final_text, self_review_text)
    print(f"0952B_PROVIDER_CALLED={str(provider_called).lower()}")
    print(f"0952B_MODEL_NAME={result['model_name']}")
    print(f"0952B_FINAL_STATUS={final_status}")


if __name__ == "__main__":
    main()

