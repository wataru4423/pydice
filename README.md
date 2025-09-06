# Pydice

CLI dice roll application.

## Description

This is a simple command-line dice rolling simulator built with Python and Typer.

## Installation

You can install `pydice` using uv:

```bash
git clone https://github.com/wataru4423/pydice.git
cd pydice
uv tool install .
```

## Usage

The command is `pydice`. You can roll dice in the `NdM` format, where `N` is the number of dice and `M` is the number of sides.

### Basic Roll

By default, it rolls a 6-sided die.

```bash
$ pydice
4
```

You can specify the number of dice and sides.

```bash
$ pydice 2d8
9
```

### Show Each Roll

Use the `--each` option to see the result of each individual die.

```bash
$ pydice 3d6 --each
5, 2, 4
```

### Weighted Dice

Use the `--weight` option to give the highest number on the die a weight of 3, making it more likely to appear.

```bash
$ pydice 1d20 --weight
20
```

### Get Version

Use the `--version` option to display the application version.

```bash
$ pydice --version
pydice 0.4.1
```

## Development

To set up the project for development:

1.  Clone the repository:
    ```bash
    git clone https://github.com/wataru4423/pydice.git
    cd pydice
    ```

2.  Create a virtual environment and install the dependencies:
    ```bash
    uv sync
    # Activating a virtual environment
    source .venv/bin/activate
    ```

3.  Run the tests:
    ```bash
    pytest
    ```
