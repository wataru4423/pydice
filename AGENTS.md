# AGENTS.md

Guidance for AI agents (and human contributors) working on this repository.

## Project Overview

Pydice is a simple command-line dice rolling simulator built with Python and Typer.

- CLI command: `pydice`
- Dice format: `NdM` where `N` is the number of dice (1–100) and `M` is the number of sides (1–1000). Max: `100d1000`.
- Options: `--weight` (weights the highest face 3x), `--each` (print each die value instead of the sum), `--version`.

## Tech Stack

- Language: Python >= 3.13 (see `.python-version`)
- CLI framework: Typer (`typer>=0.16.0`)
- Build backend: Hatchling
- Package manager: uv (lockfile: `uv.lock`)
- Tests: pytest, pytest-mock, hypothesis

## Repository Layout

```
src/pydice/
  __init__.py      # package marker (currently empty)
  main.py          # CLI entrypoint, roll() logic, dice format regex
  test_main.py     # unit + property-based tests
pyproject.toml     # project metadata, deps, scripts (pydice = pydice.main:app)
README.md          # user-facing docs
```

The public entrypoint is `pydice.main:app` (a `typer.Typer()` instance). Roll logic lives in `roll()`, which is exercised directly by tests, separate from the CLI layer. Note that `roll()` is NOT a pure function: it calls `random.choices` and is therefore non-deterministic. Deterministic tests must patch `random.choices` (or `pydice.main.random.choices`) via `pytest-mock`.

## Development Setup

```bash
git clone https://github.com/wataru4423/pydice.git
cd pydice
uv sync
source .venv/bin/activate
```

## Common Commands

Run from the repository root.

- Install dependencies: `uv sync`
- Run tests: `uv run pytest` (or `pytest` inside the venv)
- Run a single test: `uv run pytest src/pydice/test_main.py::TestRoll::test_roll_returns_list`
- Run the CLI: `uv run pydice 2d6`
- Run with verbose: `uv run pytest -v`

## Coding Conventions

- Follow the existing style: 4-space indentation, standard library imports first, then third-party (typer), then local.
- Keep the CLI layer (`main`) thin; core logic belongs in testable functions like `roll()`. Note `roll()` relies on `random.choices`, so it is non-deterministic rather than pure.
- Use type annotations (e.g. `list[int]`, `Annotated[str, ...]`) as seen in `main.py`.
- Dice format is validated by the pre-compiled `DICE_PATTERN` regex. Keep `1–100` dice and `1–1000` sides bounds in sync between the regex and any new validation.
- Do not add inline or standalone code comments unless a comment is essential. The codebase is intentionally comment-free.
- Do not add new dependencies unless clearly required; the project deliberately keeps deps minimal.

## Testing Conventions

- Tests live in `src/pydice/test_main.py`, co-located with the module under test (import via `from .main import ...`).
- CLI tests use `typer.testing.CliRunner` and assert on `result.exit_code` and `result.stdout` (note the trailing `\n` in stdout).
- Use `pytest-mock` (`MockerFixture`) to patch `random.choices` (or `pydice.main.random.choices`) for deterministic tests.
- Property-based tests use `hypothesis`; bound inputs to the valid ranges (1–100 dice, 1–1000 sides) to match the CLI's accepted formats.
- Parametrized tests (`@pytest.mark.parametrize`) cover format edge cases — extend these when changing `DICE_PATTERN`.

## Versioning

- Version is the single source of truth in `pyproject.toml` (`version`) and is read at runtime via `importlib.metadata.version("pydice")` in `main.py`.
- When bumping the version, update `pyproject.toml`; `uv.lock` is updated by running `uv lock`. Tests patch `pydice.main.__version__` rather than hardcoding the value.

## Commit Conventions

- Use Conventional Commits (e.g. `fix:`, `feat:`, `docs:`, `test:`, `chore:`).
- Keep commit messages focused and descriptive, matching the style of recent history (`fix: Improve error message for invalid dice format`).
- Branch naming: feature branches follow `vibe/<short-slug>-<token>`; otherwise follow existing repo conventions.

## Pull Requests

- Open a pull request against `main` for any change.
- Ensure `uv run pytest` passes before requesting review.
- Keep PRs small and focused; describe the change and how it was verified.
