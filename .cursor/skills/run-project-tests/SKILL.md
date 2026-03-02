---
name: run-project-tests
description: Detect and run the project's test suite, install dependencies if needed, and report results. Use when you need to run tests, verify code changes, check for regressions, or validate a fix.
---

# Run Project Tests

Detect the project's test framework, install dependencies if needed, execute the test suite, and report results clearly.

## Detection Order

1. **Check repo memory** (already loaded at mode start) — look for a test command in conventions or context
2. **Detect from project files**:

| File | Command |
|---|---|
| `pyproject.toml` / `setup.cfg` | `pytest` |
| `package.json` | `npm test` |
| `Makefile` with `test` target | `make test` |
| `Cargo.toml` | `cargo test` |
| `go.mod` | `go test ./...` |

## Execution Steps

1. **Install dependencies** if not already installed:
   - Python: `pip install -e ".[dev]"` or `pip install -r requirements-dev.txt`
   - Node: `npm install`
   - Rust: `cargo build` (tests compile on run)

2. **Activate virtual environment** if Python (check for `.venv/`)

3. **Run the test suite** using the detected command

4. **Report results clearly**:
   - Total passed / failed / skipped / errors
   - For failures: show the test name, error message, and relevant traceback
   - Verdict: PASS (all green) or FAIL (with summary of what broke)

## After Tests

- If tests **pass**: proceed with the task
- If tests **fail**: investigate and fix before considering the task complete
- If failures are **pre-existing** (not caused by your changes): note them and proceed, but flag them

## Scoped Runs

When only a subset of tests is relevant (e.g., after modifying one module):
- Run the full suite first to establish a baseline
- Then run targeted tests for faster iteration: `pytest path/to/test_file.py -v`
