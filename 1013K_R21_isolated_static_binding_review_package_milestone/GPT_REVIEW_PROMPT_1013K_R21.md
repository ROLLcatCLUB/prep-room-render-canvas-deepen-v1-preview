# GPT Review Prompt: 1013K_R21 Isolated Static Binding Review Package Milestone

Please review this package as an isolated static frontend binding milestone, not as a formal frontend mount.

## Review Target

```text
STAGE=1013K_R21_ISOLATED_STATIC_BINDING_REVIEW_PACKAGE_MILESTONE
INHERITS_FROM=1013K_R20_ISOLATED_STATIC_BINDING_POLISH_VISUAL_SMOKE
EXPECTED_STATUS=PASS_1013K_R21_ISOLATED_STATIC_BINDING_REVIEW_PACKAGE_MILESTONE
NEXT_STAGE=1013K_R22_FRONTEND_BINDING_DECISION_AFTER_REVIEW
```

## What To Check

1. R19 polished HTML keeps all 10 readonly chunk mount ids and the isolated fixture contract.
2. R19 improves the reading surface without turning the isolated fixture into a formal frontend page.
3. R20 screenshots are nonblank and show the polished isolated fixture on desktop and mobile.
4. The material prompt is lighter and teacher-readable.
5. The package keeps the M3/R18 boundary: formal frontend mounting remains blocked.

## Key Files

- `1013K_R19_isolated_static_binding_reading_surface_polish/isolated_static_binding_reading_surface_polish_1013K_R19.html`
- `1013K_R19_isolated_static_binding_reading_surface_polish/1013K_R19_result.json`
- `1013K_R20_isolated_static_binding_polish_visual_smoke/ui_smoke_screenshot_1013K_R20_desktop.png`
- `1013K_R20_isolated_static_binding_polish_visual_smoke/ui_smoke_screenshot_1013K_R20_mobile.png`
- `1013K_R20_isolated_static_binding_polish_visual_smoke/1013K_R20_result.json`
- `1013K_R21_isolated_static_binding_review_package_milestone/1013K_R21_result.json`

## Boundary

```text
formal_frontend_page_modified=false
formal_frontend_mount_allowed_next=false
runtime_connected=false
provider_called=false
model_called=false
database_written=false
memory_written=false
feishu_written=false
formal_apply_performed=false
main_project_pushed=false
```

## Requested Review Decision

Please return one of:

```text
REVIEW_DECISION=ACCEPT
REVIEW_DECISION=ACCEPT_WITH_MINOR_FIX
REVIEW_DECISION=HOLD
```

If accepted, the next stage should still be a decision gate:

```text
NEXT_STAGE=1013K_R22_FRONTEND_BINDING_DECISION_AFTER_REVIEW
FORMAL_FRONTEND_MOUNT_ALLOWED=false
```
