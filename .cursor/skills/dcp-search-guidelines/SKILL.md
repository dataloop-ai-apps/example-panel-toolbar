---
name: dcp-search-guidelines
description: Search coding guidelines before making architectural decisions, suggesting patterns, or reviewing code. Use when designing APIs, choosing error handling patterns, creating file structures, writing tests, or making any decision that should follow team standards.
---

# DCP Guidelines Search

Use `search_guidelines` to find relevant coding standards before making decisions. This ensures consistency across the codebase and surfaces team knowledge the agent wouldn't otherwise know.

## When to Search

| Situation | Query Example |
|---|---|
| New file creation | `"file structure conventions"` |
| API design | `"API design patterns"`, `"REST conventions"` |
| Error handling | `"error handling patterns"` |
| Database operations | `"data access patterns"`, `"query conventions"` |
| Testing | `"testing conventions"`, `"test organization"` |
| Code review | `"code quality standards"` |
| Security-sensitive code | `"security best practices"` |
| Performance-critical code | `"performance guidelines"` |

## How to Search

Call `search_guidelines` with:
- `query`: natural language description of what you're looking for
- `languages`: (optional) filter by language, e.g. `["python"]`, `["typescript"]`
- `frameworks`: (optional) filter by framework, e.g. `["react"]`, `["fastapi"]`
- `categories`: (optional) filter by category, e.g. `["error-handling"]`, `["testing"]`
- `limit`: (optional) max results, default 5

## Citing Results

When a guideline influences your decision, cite it:

```
Guideline: [ID] - [Title]
  Confidence: [high/medium/low]
  Summary: [brief summary]
```

## No Results Found

If `search_guidelines` returns nothing relevant:
1. Note that no guidelines were found for this area
2. Proceed with general best practices
3. Consider recording the decision as a learning via `update_memory` so future sessions have guidance
