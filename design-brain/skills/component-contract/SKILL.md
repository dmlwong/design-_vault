---
name: component-contract
description: Build, refactor, or review a single Orbit UI component so it exactly matches its written contract and the Orbit design brain. Use this skill whenever the user asks to create a new component, rebuild or refactor an existing one, fix a component that "looks off" or "doesn't match the system", bring a component up to standard, or implement a component from a Figma frame or a contract spec — even if they don't say the word "contract". Always use this for component-level UI work on Orbit (ClauseIQ, MarketIQ, RFP Analytics, RFP Builder).
---

# Component Contract Builder

Produce a single Orbit component that is correct against (a) its contract in
`components/<name>.md` and (b) the always-on rules in `AGENTS.md`. This skill exists
because component-level work is where generic-AI aesthetics and missing states creep in.

## Workflow

### 1. Locate or create the contract
- If `components/<name>.md` exists, read it in full. It is authoritative.
- If it does not exist, **do not start coding.** Draft a contract from
  `components/_TEMPLATE.md`, fill every section, and confirm with the user first.
  A component without a contract has no definition of "correct".

### 2. Load required context
Read, in this order:
1. The contract (`components/<name>.md`)
2. `tokens.md` — and the real token source files it points to
3. The nearest golden example in `examples/` (match the component family)
4. `accessibility.md`, `motion.md`, `ux-copy.md` for the slices the component touches

### 3. Build to spec
- Consume **Tier-2 semantic tokens** only. No primitives, no hardcoded values.
- Implement **every** state the contract lists. The minimum set is:
  default, hover, focus-visible, active, disabled, loading, empty (if data-bearing),
  error. Missing states = incomplete, not "v1".
- Implement every variant and density mode in the contract.
- Honour RBAC / permission states described in the contract.
- Keep the public API (props) exactly as the contract specifies. If the API needs to
  change, update the contract first and flag it.

### 4. Self-review against the Definition of Done
Before presenting, verify the `AGENTS.md` §5 checklist line by line:
- [ ] Zero hardcoded visual values
- [ ] Correct in both `efficio` and `orbit` themes (no theme-conditional code)
- [ ] All states present
- [ ] Keyboard-operable, visible focus ring, WCAG 2.2 AA contrast
- [ ] Comfortable + compact density
- [ ] Copy per `ux-copy.md`, motion per `motion.md`
- [ ] No `anti-patterns.md` violations
If any item fails, fix it before showing the user. Do not present partial work as done.

### 5. Report
State plainly: which contract was used, which states/variants were implemented, any
deviations and why, and anything the contract was silent on that you had to decide.

## Hard stops
- A request to "just make it look nice" without tokens → redirect to tokens.
- A new component with no contract → write the contract first.
- A conflict between the request and `AGENTS.md` rules → stop and ask.

## References
- Contract template: `../../components/_TEMPLATE.md`
- Token governance: `../../tokens.md`
- Anti-patterns to avoid: `../../anti-patterns.md`
