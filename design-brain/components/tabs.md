---
type: component-contract
status: in-review
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-06-15
maturity_score: 82
tags: [orbit, design-brain, component-contract]
---

# Component Contract: `tabs`

## Purpose
Use tabs to switch between peer sections in the same page or tool context without
changing the user's broader workflow. In Orbit source, standalone tab triggers are
implemented by `TabButton`, and page-level tab bars are composed inside `PageHeader`.

## Source Links
- Component source:
  `packages/orbit/src/navigation/TabButton.tsx`
- Tab trigger styles:
  `packages/orbit/src/navigation/TabButton.module.css`
- Page-level composition:
  `packages/orbit/src/navigation/PageHeader.tsx`
- Page-level styles:
  `packages/orbit/src/navigation/PageHeader.module.css`
- Behavior tests:
  `packages/orbit/src/navigation/PageHeader.test.tsx`

## Anatomy
Tab list, tab trigger, label, optional numeric badge, optional active underline, and
associated tab panel. `PageHeader` owns the tab list; `TabButton` owns individual tab
semantics and visual state.

## Public API

### `TabButton`

| Prop | Type | Default | Required | Source |
| ---- | ---- | ------- | -------- | ------ |
| `active` | `boolean` | `false` | no | code |
| `status` | `'Rest' \| 'Hover' \| 'Disabled'` | `'Rest'` | no | code |
| `showUnderline` | `boolean` | `true` | no | code |
| `children` | `React.ReactNode` | none | yes | code |
| `ariaControls` | `string` | none | no | code |
| `disabled` | `boolean` | `false` | no | code |
| native button props | `Omit<ButtonHTMLAttributes, 'disabled'>` | varies | no | code |

### `PageHeader` Tab Composition

| Field / Prop | Type | Default | Required | Source |
| ------------ | ---- | ------- | -------- | ------ |
| `tabs[].id` | `string` | generated | no | code |
| `tabs[].label` | `string` | none | yes | code |
| `tabs[].badge` | `number` | none | no | code |
| `tabs[].panelId` | `string` | none | no | code |
| `tabs[].disabled` | `boolean` | `false` | no | code |
| `activeTab` | `number` | uncontrolled | no | code |
| `defaultActiveTab` | `number` | first selectable tab | no | code |
| `onTabChange` | `(index: number) => void` | none | no | code |
| `showTabUnderline` | `boolean` | `true` | no | code |

## Variants
- Standalone tab trigger via `TabButton`.
- Page-level tabs inside `PageHeader`.
- Active underline shown or hidden with `showUnderline` / `showTabUnderline`.
- Badge tabs use `Badge` with status `Red` for numeric badges.
- Disabled tabs are rendered but skipped by keyboard navigation.

## States
- Default: `status="Rest"` and `active=false`.
- Hover preview: `status="Hover"` adds the hover background class.
- Active: `active=true`, `aria-selected="true"`, `tabIndex=0`, semibold label, and
  active underline when enabled.
- Disabled: `disabled` or `status="Disabled"` disables click handling, sets
  `aria-disabled`, uses disabled button tokens, and sets `tabIndex=-1`.
- Panel loading, empty, and error states are owned by the tab panel content, not by
  `TabButton`.

## Density
No density prop exists. Current density is token-driven through `--orbit-tab-height`,
`--orbit-tab-inner-height`, `--orbit-tab-underline-height`, `--orbit-space-s`, and
`--orbit-space-base`. Compact page contexts should tune those tokens or page-header
CSS custom properties rather than adding one-off padding.

## Themes
Tabs support `efficio` and `orbit` through token resolution only. `PageHeader` uses
the root theme tokens and optional header preset gradients for tool headers.

## RBAC / Permissions
If a tab is unavailable because of permissions, prefer hiding it when the user must
not know the section exists. Use `disabled: true` only when the disabled reason can
be safely disclosed elsewhere in the UI.

## Tokens Used
- `--orbit-tab-height`
- `--orbit-tab-inner-height`
- `--orbit-tab-underline-height`
- `--orbit-radius-sm`
- `--orbit-space-s`
- `--orbit-space-base`
- `--orbit-color-bg-hover`
- `--orbit-color-border-focused`
- `--orbit-color-btn-secondary-fg`
- `--orbit-color-btn-secondary-fg-disabled`
- `--orbit-color-btn-secondary-bg-disabled`
- `--orbit-color-btn-secondary-bg-accent`
- `--orbit-color-btn-secondary-border-disabled`
- `--orbit-font-family-sans`
- `--orbit-text-sm`
- `--orbit-font-weight-regular`
- `--orbit-font-weight-semibold`
- `--orbit-leading-relaxed`
- `--orbit-leading-snug`

## Accessibility
- `TabButton` renders a native `button` with `role="tab"`.
- Active state maps to `aria-selected`.
- `ariaControls` maps to `aria-controls` and should reference the matching tab panel id.
- If `PageHeader` tabs provide `panelId`, every referenced panel id must exist in the
  mounted DOM. Inactive panels may be mounted as hidden `role="tabpanel"` sections, but
  `aria-controls` must not point at missing elements.
- `PageHeader` renders a `role="tablist"` with horizontal orientation and label
  `Page sections`.
- Numeric badge tabs should expose the count in the accessible tab name, for example
  `My QC tasks, 2 items`.
- `PageHeader` supports `ArrowRight`, `ArrowLeft`, `Home`, and `End`; disabled tabs
  are skipped.
- Tests confirm uncontrolled selection, controlled `onTabChange`, and arrow-key focus
  movement.

## Motion
Current source uses `transition: background-color 0.15s ease` on tab hover. Avoid
decorative panel transitions unless a product source proves they improve orientation.
Reduced-motion handling is a foundation gap tracked in `design-brain/motion.md`.

## Content / Copy
Use short nouns or noun phrases such as `Overview`, `Spend Analysis`, and `Suppliers`.
Numeric badges should be counts, not status labels. Avoid tabs for mandatory
step-by-step flows.

## Do / Don't
- Do use tabs for peer sections inside a page header.
- Do link tabs to panels with `panelId` when panels are present.
- Do mount a matching tab panel for every `panelId`, including inactive tabs.
- Do keep disabled tabs out of the keyboard loop.
- Don't use tabs as a wizard or sequential approval tracker.
- Don't create custom tab styling with hardcoded colours or spacing.

## Golden Example
`design-brain/examples/clauseiq-focus-mode-results.md`

## Gap Report
- No standalone `Tabs` wrapper component exists; `PageHeader` owns the proven tab-list
  behavior.
- No built-in panel loading, empty, or error state exists.
- Reduced-motion rules are not implemented in source.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[design-brain/examples/clauseiq-focus-mode-results|clauseiq-focus-mode-results]] · [[design-brain/motion|motion]]
<!-- graph-links:end -->
