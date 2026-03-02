---
name: playwright-ci-execution
description: Configure and run Playwright tests with the correct browser mode based on the execution environment. Use when writing or running Playwright tests — detects whether to use headed (local) or headless (CI/Docker) mode automatically.
---

# Playwright Execution — Environment-Aware

Configure Playwright tests to work correctly in both local (headed) and CI/Docker (headless) environments.

## Step 1: Detect the Environment

Before writing or running tests, determine where you are:

| Signal | How to check | Means |
|--------|-------------|-------|
| `CI` env var is set | `process.env.CI` | CI pipeline → **headless** |
| `/.dockerenv` file exists | `fs.existsSync('/.dockerenv')` | Docker container → **headless** |
| `DISPLAY` env var is empty (Linux) | `!process.env.DISPLAY` | No display server → **headless** |
| `PWDEBUG=1` is set | `process.env.PWDEBUG === '1'` | User wants inspector → **headed** |
| None of the above | — | Local machine → **headed** |

**Quick rule:** if any CI/Docker/no-display signal is detected, use headless. Otherwise default to headed for interactive debugging.

## Step 2: Make Tests Environment-Aware

Tests should read the mode from configuration, never hardcode it.

### Playwright Config (`playwright.config.ts`)

```typescript
const isCI = !!process.env.CI || !process.env.DISPLAY;

export default defineConfig({
  use: {
    headless: isCI,
    screenshot: isCI ? 'only-on-failure' : 'off',
    trace: isCI ? 'retain-on-failure' : 'off',
  },
});
```

### Cucumber / BDD World Setup (`support/world.ts`)

```typescript
const isCI = !!process.env.CI || !process.env.DISPLAY;

this.browser = await chromium.launch({
  headless: isCI,
  slowMo: isCI ? 0 : 250,
});
```

### Respect `HEADLESS` env override

If the project already uses a `HEADLESS` env var, respect it as the top priority:

```typescript
const headless = process.env.HEADLESS !== undefined
  ? process.env.HEADLESS !== 'false'
  : (!!process.env.CI || !process.env.DISPLAY);
```

## Step 3: Verify Before Running

Before executing tests, check the repo's configuration for hardcoded values:

| Check | What to look for | Action if wrong |
|-------|-----------------|-----------------|
| `playwright.config.ts` | `headless` hardcoded to `true` or `false` | Replace with env-aware check |
| `world.ts` / `support/*.ts` | `chromium.launch({ headless: false })` | Replace with env-aware check |
| `.env` in repo | `PWDEBUG=1` in a headless environment | Remove or set to empty |
| `package.json` scripts | `--headed` flag hardcoded | Remove; let config decide |

## Common Failures in Headless Environments

| Error | Cause | Fix |
|-------|-------|-----|
| `Target page, context or browser has been closed` | PWDEBUG or headed mode without display | Use env-aware headless detection |
| `Failed to launch browser` / missing display | Headed mode in container | Ensure headless when no display |
| `Protocol error: Connection closed` | Browser OOM in container | Chromium needs ~512MB; check limits |

## Headless-Specific Settings

When running headless (CI, Docker, remote), also configure:

```typescript
actionTimeout: 15000,
navigationTimeout: 30000,
screenshot: 'only-on-failure',
trace: 'retain-on-failure',
video: 'retain-on-failure',
```

These capture debugging artifacts without requiring a display.
