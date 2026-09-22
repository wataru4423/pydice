# Requirements

This document defines the functional and non-functional requirements for Pydice, a command-line dice rolling simulator built with Python and Typer.

## 1. Overview

Pydice is a CLI tool that simulates rolling dice. Users specify dice in the `NdM` format, where `N` is the number of dice and `M` is the number of sides per die, and the tool prints the roll result to standard output.

- CLI command: `pydice`
- Dice format: `NdM` (e.g., `2d6`)
- Limits: 1–100 dice, 1–1000 sides (max: `100d1000`)

## 2. Functional Requirements

### FR-1: Dice Roll Execution

- The tool SHALL roll the specified dice and print the result.
- If no dice argument is given, the tool SHALL roll a single 6-sided die (`1d6`) by default.
- Each die SHALL return a uniformly random integer between 1 and the number of sides (inclusive).
- The default output SHALL be the sum of all rolled values.

### FR-2: Dice Format Validation

- The tool SHALL accept dice in the `NdM` format.
- The number of dice `N` SHALL be an integer between 1 and 100 (inclusive).
- The number of sides `M` SHALL be an integer between 1 and 1000 (inclusive).
- If the argument does not match the valid format or range, the tool SHALL print an error message (`Invalid dice format. Use NdM (e.g., 2d6, 1d20). Max: 100d1000.`) and exit with a non-zero status code (1).

### FR-3: Show Each Roll (`--each`)

- When the `--each` option is set, the tool SHALL print the value of each individual die instead of the sum.
- Values SHALL be printed as a comma-separated list (e.g., `5, 2, 4`).

### FR-4: Weighted Dice (`--weight`)

- When the `--weight` option is set, the highest face of each die SHALL be weighted 3x relative to the other faces (i.e., 3x more likely to appear than any other face).
- `--weight` SHALL be combinable with `--each`.

### FR-5: Version Display (`--version`)

- When the `--version` option is set, the tool SHALL print the application name and version (e.g., `pydice 0.5.0`) and exit with status code 0.
- The version SHALL be read from the package metadata defined in `pyproject.toml`.

## 3. Non-Functional Requirements

### NFR-1: Runtime Environment

- The tool SHALL run on Python >= 3.13.
- The tool SHALL depend only on Typer (`typer>=0.16.0`) as a runtime dependency.

### NFR-2: Interface Consistency

- All roll logic SHALL live in a testable function (`roll()`) separate from the CLI layer.
- The dice format bounds (1–100 dice, 1–1000 sides) SHALL be kept in sync between the validation regex (`DICE_PATTERN`) and any future validation logic.

### NFR-3: Testability

- All functional requirements SHALL be covered by unit tests and property-based tests (`pytest`, `pytest-mock`, `hypothesis`).
- Tests SHALL run with `uv run pytest`.

### NFR-4: Exit Codes

- Successful execution SHALL exit with status code 0.
- Invalid input SHALL exit with status code 1 and print a descriptive error message to standard output.
