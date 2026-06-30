---
type: component-contract
status: in-review
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-06-14
maturity_score: 72
tags: [orbit, design-brain, component-contract, gap]
---

# Component Contract: `toast-notification`

Real component: `Toast` from `@efficio/orbit`.

Source:
- `packages/orbit/src/feedback/Toast.tsx`
- `packages/orbit/src/feedback/Toast.module.css`
- `packages/orbit/src/feedback/Toast.test.tsx`

## Purpose
Confirm background results or recoverable system events without interrupting work.

## Public API

| Prop | Type | Default | Required | Notes |
| ---- | ---- | ------- | -------- | ----- |
| `type` | `'Success' \| 'Error' \| 'Info' \| 'Warning' \| 'Mute' \| 'NoStatus'` | none | yes | Controls colour, icon, live-region role. |
| `message` | `string` | none | yes | Visible message. |
| `visible` | `boolean` | none | yes | Returns `null` when false. |
| `onDismiss` | `() => void` | undefined | no | Enables close button and auto-dismiss timer. |
| `actions` | `ToastAction[]` | undefined | no | Optional action buttons. |

`ToastAction`: `label`, `onClick`, optional `variant: 'Primary' | 'Secondary'`.

## Variants
Success, Error, Info, Warning, Mute, NoStatus, with optional actions and dismiss.

## States
- Hidden: returns `null`.
- Visible: fixed top toast.
- Auto-dismiss: when `visible` and `onDismiss` are provided, dismisses after 3000ms.
- Error uses alert/assertive live region; other types use status/polite.
- Loading/progress is not built in.

## Density
Fixed toast spacing; no density prop.

## Themes
Works through status and toast tokens; Orbit overrides status colours.

## Tokens Used
`--orbit-color-status-high-bg-success`, `--orbit-color-status-high-bg-error`,
`--orbit-color-status-high-bg-information`, `--orbit-color-status-high-bg-warning`,
`--orbit-color-status-high-bg-no-status`, `--orbit-color-white`,
`--orbit-color-black`, `--orbit-color-text-primary`,
`--orbit-color-btn-tertiary-fg`, `--orbit-color-focus-ring`,
`--orbit-space-base`, `--orbit-space-s`, `--orbit-space-xs`, `--orbit-space-m`,
`--orbit-radius-sm`, `--orbit-shadow-lg`, `--orbit-text-body-size`,
`--orbit-text-body-weight`, `--orbit-text-body-leading`, `--orbit-font-family-sans`,
`--orbit-font-weight-medium`, `--orbit-btn-height-small`, `--orbit-z-toast`,
`--orbit-toast-max-width`.

## Accessibility
- Error toast uses `role="alert"` and `aria-live="assertive"`.
- Non-error toast uses `role="status"` and `aria-live="polite"`.
- Dismiss button has type and label `Dismiss <type> toast`.
- Tests cover action handlers and `NoStatus`.

## Motion
Source uses `toastSlideIn 0.3s ease`; no reduced-motion rule found.

## Content / Copy
Messages must say what happened. Error messages need a recovery path when possible.

## Do / Don't
- Do use actions for immediate recovery.
- Don't use a toast as the only record of a high-stakes procurement decision.
- Don't use vague error copy.

## Golden Example
`design-brain/examples/button-states.md`

## Gap Report
- Major: no reduced-motion handling for toast animation.
- Major: loading/progress toast is not built in.
- Minor: auto-dismiss duration is a literal, not a token.
