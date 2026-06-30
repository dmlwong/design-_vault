# patterns/ — Page-level pattern contracts

Component contracts cover the bricks; pattern contracts cover the buildings. A pattern is
a reusable *composition* — how components assemble into a screen or flow with a defined
behaviour. This is the layer that stops agents producing screens that use correct
components but compose them generically.

## When to write a pattern contract
- A composition recurs across surfaces (results dashboards, config wizards, list+detail).
- A screen sets precedent that future screens must follow.
- An agent keeps composing pages "correctly but wrong" — right bricks, wrong building.

## How agents use this
Building a full page or multi-component view → check this index for a matching pattern
**before** inventing a layout. Components defer to their contracts; the page defers to
the pattern.

## Index (fill in)
| Pattern | Surfaces | Status |
| ------- | -------- | ------ |
| `focus-mode-results` | ClauseIQ (precedent for all results views) | draft |
| `guided-conversational-workflow` | ClauseIQ card-based flows | draft |
| `list-detail` | shared | todo |
| `config-wizard` | Platform Config / New Playbook | todo |

> Seed the first two from your existing specs: the ClauseIQ focus-mode Results dashboard
> deep-dive and the Guided Conversational Workflow specification. They're already written —
> they just need converting into this template.
