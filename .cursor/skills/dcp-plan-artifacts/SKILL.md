---
name: dcp-plan-artifacts
description: Write planning documents (PRDs, ADRs, design docs, test plans, review reports, debug findings) to the .plans/ directory. Use when creating working artifacts, design documents, or any planning output that shouldn't be committed to the repo.
---

# DCP Plan Artifacts

All planning and working documents go in the `.plans/` directory at the repo root. This directory is git-ignored to keep the repo clean.

## When to Use

Write to `.plans/` for:
- PRDs, feature specs, user stories
- Architecture Decision Records (ADRs)
- Design documents, API contracts
- Test plans, QA checklists
- Review reports, audit findings
- Debug investigation notes
- Migration plans, rollout strategies

Do NOT write to `.plans/` for:
- Source code, test files
- README.md, API docs, changelogs (these are committed)
- Configuration files

## Naming Convention

`.plans/<mode>-<descriptive-name>.md`

| Mode | Example |
|---|---|
| Product | `.plans/product-user-auth-prd.md` |
| Architect | `.plans/architect-api-redesign.md` |
| Tester | `.plans/tester-payment-flow-test-plan.md` |
| Reviewer | `.plans/reviewer-pr-42-findings.md` |
| Debugger | `.plans/debugger-oom-investigation.md` |
| Automation | `.plans/automation-e2e-regression-plan.md` |

## Setup

Create `.plans/` if it doesn't exist. It should already be in `.gitignore` (added by `init_repo`).

## Lifecycle

- Users clean `.plans/` manually when done
- Modes do NOT auto-delete artifacts from other modes
- Files persist across sessions for continuity
