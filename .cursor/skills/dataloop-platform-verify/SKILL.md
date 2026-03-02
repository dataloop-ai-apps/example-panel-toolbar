---
name: dataloop-platform-verify
description: Verify implementations, check state, reproduce bugs, or validate test results on the Dataloop platform using browser MCP tools. Use when you need to verify behavior on Dataloop, check platform state, inspect UI, or validate deployed changes.
---

# Dataloop Platform Verification

Use browser MCP tools to interact with the Dataloop platform for verification, debugging, or validation.

## URLs

| Environment | URL |
|---|---|
| Production / RC | `https://rc-con.dataloop.ai/projects/ade9ba40-0fa3-4157-a135-21dea7af4f4a` |
| Local dev | `http://local.dataloop.ai:8443/projects` |

## Login Flow

1. Navigate to the target URL
2. If a login page appears, read credentials from environment variables:
   - Email: `DATALOOP_EMAIL`
   - Password: `DATALOOP_PASSWORD`
3. Enter credentials and proceed

## SSL Issues

If blocked by an SSL/certificate warning page, type `thisisunsafe` to bypass it.

## Missing Credentials

If `DATALOOP_EMAIL` or `DATALOOP_PASSWORD` environment variables are not set, ask the user for credentials before proceeding. Do not attempt to log in without valid credentials.

## When to Use

- **Developer mode**: Verify implementation correctness after coding
- **Reviewer mode**: Check impact of code changes on the platform
- **Tester mode**: Validate test results and inspect platform state
- **Debugger mode**: Reproduce bugs and investigate live issues
- **Automation mode**: Validate automated test behavior against the platform
