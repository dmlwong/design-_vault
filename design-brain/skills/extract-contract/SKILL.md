---
name: extract-contract
description: Generate an accurate component or pattern contract by extracting facts from existing source code instead of writing it by hand. Use this skill whenever the user asks to "write a contract for" an existing component, document a component, populate the design brain from the design system, convert a built screen into a pattern contract, or backfill contracts for the component library. Always use this when a component already exists in code and needs a contract.
---

# Extract Contract

Turn an existing implementation into a contract. The rule: **derive, don't transcribe** —
every fact that exists in code is read from code; hand-writing it creates drift.

## Inputs to locate (ask if not found)
- The component source (and its prop types / TypeScript interfaces)
- Its Storybook stories, if any (variants and states are often already enumerated there)
- The token files it consumes
- Usage sites in the prototype (to ground variants in reality)

## Workflow
1. **Read the source.** Extract: public API (props, types, defaults, required), variants,
   density behaviour, theme handling, existing states, tokens consumed, ARIA/keyboard
   behaviour, motion values.
2. **Read usage.** Find 2–3 real usage sites; note which variants/props are actually used.
   Flag props that exist but are never used.
3. **Fill the template.** Copy `design-brain/components/_TEMPLATE.md` (or
   `design-brain/patterns/_TEMPLATE.md` for a screen) and populate every section from the
   extracted facts. Mark each section as `from source` or `specified` (i.e. the contract
   is prescribing something the code doesn't yet do).
4. **Gap report.** List explicitly where the code falls short of the brain: missing
   states, hardcoded values, a11y gaps, theme-conditional logic. These become the
   contract's `specified` sections and a fix-list for the user.
5. **Link the golden example.** Point the contract's example at the real implementation
   or story. Update the index in `components/README.md` (or `patterns/README.md`).

## Quality bar
- API section matches the source **exactly** — verify prop-by-prop before presenting.
- No invented behaviour: anything not observed in code or stated by the user is marked
  `specified`, never passed off as existing.
- Output ends with the gap report, ordered by severity.

## References
- Component template: `../../components/_TEMPLATE.md`
- Pattern template: `../../patterns/_TEMPLATE.md`
- Token governance: `../../tokens.md`
