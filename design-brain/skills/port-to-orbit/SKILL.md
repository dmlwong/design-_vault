---
name: port-to-orbit
description: Port an external or AI-generated prototype (especially from Lovable, but also v0, Bolt, Figma Make, or a one-off React snippet) onto Orbit's tokens, components, and standards. Use this skill whenever the user wants to bring a prototype "into Orbit", "make this match our system", convert an external component to Orbit, migrate Lovable output, or align imported UI with the design brain. Always use this for any port/migration of UI into Orbit.
---

# Port to Orbit

Convert external UI into Orbit-compliant UI. This generalises the existing
Lovable-to-Orbit port workflow (component mapping, token translation, validation).

## Workflow
1. **Inventory.** List the imported screen's components, styles, and hardcoded values.
2. **Component mapping.** Map each imported element to an existing Orbit component +
   contract (`components/`). Anything with no match -> propose a new component (write a
   contract from `_TEMPLATE.md`) before coding it.
3. **Token translation.** Replace every literal visual value with a Tier-2 semantic
   token (`tokens.md`). No hardcoded values survive the port.
4. **State + a11y completion.** Add the states the prototype skipped (loading/empty/
   error/disabled) and bring it to WCAG 2.2 AA (`accessibility.md`).
5. **Theme + density.** Verify `efficio` and `orbit`, comfortable and compact.
6. **Validation checklist.** Run the `AGENTS.md` section 5 Definition of Done. Report
   deviations.

## Benchmark-Proven Rules
The 2026-06-15 Lovable port benchmark used `Test` as the
source prototype and passed at `18/18`. Apply these rules to future ports:

- Replace ShadCN/Tailwind components with Orbit components instead of restyling them.
- Translate raw Tailwind tokens, OKLCH values, pixel column widths, radii, and icon
  sizes into Orbit semantic or component tokens.
- Preserve the useful information architecture, but add missing Orbit states: loading,
  empty, error, disabled/permission, active filters, selected detail, density, and
  theme.
- Prefer Orbit `Table` plus pagination/server-side pagination over virtualized div rows
  unless a virtual-table contract exists.
- If the prototype uses dropdown checkbox menus for column visibility, use approved
  Orbit controls such as column presets, or record the menu/checkbox-list contract gap.
- If the prototype uses avatars/resource stacks, keep the composition token-backed and
  accessible, then record whether an Avatar contract is needed.

## References
- Token governance: `../../tokens.md`
- Contract template: `../../components/_TEMPLATE.md`
- Lovable port pattern: `../../patterns/lovable-port.md`
- Lovable port example: `../../examples/lovable-initiatives-port.md`
- Anti-patterns: `../../anti-patterns.md`

## Report Format

End every port with:

```text
COMPONENT MAPPING
- Imported element -> Orbit contract -> status

TOKEN TRANSLATION
- Literal value -> semantic/component token -> status

MISSING STATES ADDED
- Component/state -> implementation note

ACCESSIBILITY FIXES
- Issue -> fix

DEVIATIONS
- Anything that cannot match Orbit yet, with reason and owner
```

## Source-Required Follow-Up

Keep adding accepted benchmark results and porting gaps back into this skill. The skill
is authoritative for prototype migration, but component/pattern contracts win whenever a
specific Orbit contract exists.
