# 1013M MiniMax M3 Connection Smoke

- FINAL_STATUS: `PASS_MINIMAX_M3_CONNECTED`
- Model: `MiniMax-M3`
- Provider: `openai_compatible` over MiniMax env credentials
- Business-call default: `thinking: {"type":"disabled"}`
- Token field for M3: `max_completion_tokens`

The smoke call returned valid JSON:

```json
{
  "ok": true,
  "model_check": "m3"
}
```

Boundary: no database write, no memory write, no Feishu write, no formal apply, and no main project push.
