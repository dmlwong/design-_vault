---
name: port-to-orbit
description: Port an external or AI-generated prototype (especially from Lovable, but also v0, Bolt, Figma Make, or a one-off React snippet) onto Orbit's tokens, components, and standards. Use this skill whenever the user wants to bring a prototype "into Orbit", "make this match our system", convert an external component to Orbit, migrate Lovable output, or align imported UI with the design brain. Always use this for any port/migration of UI into Orbit.
---

# Port to Orbit

Convert external UI into Orbit-compliant UI. This generalises the existing
Lovable-to-Orbit port workflow (component mapping, token translation, validation).

## Workflow
0. **Identify the platform first** (`AGENTS.md` §2.2). Connected Platform vs Orbit /
   Client changes density bias, card padding, and copy voice — the platform deltas live
   in `design-brain/defaults.md` and `design-brain/platforms/`. Unclear → ask before
   porting. Note the input's shape too: a Lovable/React prototype and an `explore`
   concept (plain HTML/CSS/JS, deliberately un-Orbit) port differently — for the
   latter, the mapping target is the *behaviour and layout intent*, not the markup.
1. **Inventory.** List the imported screen's components, styles, and hardcoded values.
2. **Component mapping.** Map each imported element to an existing Orbit component +
   contract (`design-brain/components/`). Anything with no match -> propose a new
   component (write a contract from `design-brain/components/_TEMPLATE.md`) before
   coding it — and route `write-stories` for it, or the port re-creates the story
   coverage gap.
3. **Token translation.** Replace every literal visual value with a Tier-2 semantic
   token (`design-brain/tokens.md`). No hardcoded values survive the port.
4. **State + a11y completion.** Add the states the prototype skipped (loading/empty/
   error/disabled) and bring it to WCAG 2.2 AA (`design-brain/accessibility.md`).
5. **Theme + density — verify by rendering, not by inspection.** Where stories exist,
   flip the Storybook **Theme** toolbar and both densities (`design-brain/storybook.md`);
   otherwise state the mechanism used. Run `npm run audit:design-system` — it exists
   precisely to catch what step 3 forbids.
6. **Validation checklist.** Run the full `AGENTS.md` section 5 Definition of Done —
   including the `<OrbitInspector />` mount rule for generated prototypes (§2.8) and
   copy/motion checks. Report deviations. This is a pre-flight; the design-reviewer
   owns the verdict.

## Benchmark-Proven Rules
The 2026-06-15 Lovable port benchmark (source prototype name withheld from projections;
result recorded in `design-brain/examples/lovable-initiatives-port.md`) passed at
`18/18`. Apply these rules to future ports:

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
- Token governance: `design-brain/tokens.md`
- Orbit defaults + platform deltas: `design-brain/defaults.md`
- Platform profiles: `design-brain/platforms/`
- Contract template: `design-brain/components/_TEMPLATE.md`
- Lovable port pattern: `design-brain/patterns/lovable-port.md`
- Lovable port example: `design-brain/examples/lovable-initiatives-port.md`
- The Lovable projection the prototype came from (mapping table, known gaps):
  `design-brain/lovable/knowledge-base.md`
- Anti-patterns: `design-brain/anti-patterns.md`
- Storybook / render-verification: `design-brain/storybook.md`

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

COPY & MOTION
- Copy per design-brain/ux-copy.md; motion per design-brain/motion.md -> status

INSPECTOR
- <OrbitInspector /> mount status (generated prototypes; see design-reviewer's
  existence caveat while the package does not yet ship the export)

STORIES
- New components created by the port -> write-stories routed? y/n

DEVIATIONS
- Anything that cannot match Orbit yet, with reason and owner
```

On correction by a human, append the lesson to `design-brain/lessons/INBOX.md`
(`AGENTS.md` §6) before continuing.

## Source-Required Follow-Up

Keep adding accepted benchmark results and porting gaps back into this skill. The skill
is authoritative for prototype migration, but component/pattern contracts win whenever a
specific Orbit contract exists.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[AGENTS|AGENTS]] · [[design-brain/accessibility|accessibility]] · [[design-brain/anti-patterns|anti-patterns]] · [[design-brain/components/_TEMPLATE|components _TEMPLATE]] · [[design-brain/defaults|defaults]] · [[design-brain/examples/lovable-initiatives-port|lovable-initiatives-port]] · [[design-brain/lessons/INBOX|lessons INBOX]] · [[design-brain/lovable/knowledge-base|knowledge-base]] · [[design-brain/patterns/lovable-port|lovable-port]] · [[design-brain/storybook|storybook]] · [[design-brain/tokens|tokens]]
<!-- graph-links:end -->
