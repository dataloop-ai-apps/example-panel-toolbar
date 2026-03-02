---
name: dcp-active-learning
description: Record learnings, decisions, and gotchas to DCP memory using update_memory. Use when finishing a task, receiving review feedback, discovering a bug pattern, establishing a new convention, or when the user uses strong directives like "always", "never", "must".
---

# DCP Active Learning

Record insights to repo memory so future sessions benefit. Uses the `update_memory` MCP tool with section `learnings`, operation `append`.

## When to Record

- After completing any significant task
- When discovering non-obvious behavior or gotchas
- When establishing or changing a pattern/convention
- When receiving review feedback
- When the user states a strong directive (see auto-detect below)

## How to Record

Call `update_memory` with:
- `repo_path`: the repository path (same one used for `read_memory` at the start)
- `section`: `"learnings"`
- `operation`: `"append"`
- `content`: a dict with `summary` and `category`

The system auto-generates `id`, `date`, and `confidence`.

## Categories

| Category | Use When | Typical Confidence |
|---|---|---|
| `decisions` | Non-obvious implementation choices, new patterns established, architectural decisions | 70-95 |
| `review_feedback` | Feedback from code reviews, recurring review comments | 70-85 |
| `gotchas` | Tricky behaviors, non-obvious constraints, surprising side effects | 60-80 |
| `bug_patterns` | Root causes found during debugging, recurring bugs | 70-85 |
| `edge_cases` | Edge cases discovered during testing | 65-80 |

## Confidence Levels

- **80+** = enforced guideline (treated as a rule in future sessions)
- **50-79** = recommended practice
- **20-49** = informational note
- **0-19** = experimental / untested

When the same insight appears 3+ times, escalate to confidence 90+.

## Auto-Detect Strong Directives

When the user or a reviewer uses strong language, record immediately:

**Trigger phrases**: "always", "never", "must", "required", "should always", "don't ever", "every time", "without exception"

**Flow**:
1. Acknowledge: "Got it - [paraphrase the directive]"
2. Offer: "Should I record this as a learning so it's remembered?"
3. If yes: record with confidence 85+

**Example**:
> User: "Tests should always go in a dedicated folder"
> → Record: `{summary: "Tests should always go in a dedicated folder", category: "decisions"}` with confidence 90

## Supplementary Memory Updates

Beyond learnings, some discoveries warrant updating other sections:

| Discovery | Section | Operation |
|---|---|---|
| Architecture changed or new components | `architecture` | `set` |
| New convention established | `conventions` | `append` |
| Known issue or caveat | `context` | `append` |

Always pass `repo_path` for these calls too.
