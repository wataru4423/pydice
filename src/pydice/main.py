import importlib.metadata
import random
import re
from typing import Annotated, Optional

import typer

__version__ = importlib.metadata.version("pydice")
app = typer.Typer()

# Pre-compiled regex for dice format validation (1-100 dice, 1-1000 sides)
DICE_PATTERN = re.compile(r"^(100|[1-9]\d?)[d](1000|[1-9]\d{0,2})$")


def version_callback(value: bool):
    if value:
        print(f"pydice {__version__}")
        raise typer.Exit()


@app.command()
def main(
    dice: Annotated[str, typer.Argument(help="Dice to roll, e.g. 2d6.")] = "1d6",
    weight: Annotated[bool, typer.Option(help="Weighted dice.")] = False,
    each: Annotated[bool, typer.Option(help="Return each die value.")] = False,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show the version.",
        ),
    ] = None,
) -> None:
    """Dice roll application\n
    Default: to roll a 6-sided dice and return sum value.\n
    Max: 100d1000.\n
    First number: Number of dice.\n
    Second number: Number of sides.\n
    If --weight is set, last number will be weighted to 3.\n
    If --each is set, each die value will be returned instead of the sum value.\n
    """

    if not DICE_PATTERN.fullmatch(dice):
        print("Invalid dice format. Use NdM (e.g., 2d6, 1d20). Max: 100d1000.")
        raise typer.Exit(code=1)
    pairs, bones = map(int, dice.split("d"))

    rolls = roll(pairs, bones, weight)
    if each:
        print(*rolls, sep=", ")
    else:
        print(sum(rolls))


def roll(pairs: int, bones: int, weight: bool) -> list[int]:
    """Dice roll function

    Args:
        pairs (int): Number of dice
        bones (int): Number of sides
        weight (bool): Weighted dice


    Returns:
        list[int]: Value of each die
    """
    if weight:
        weights = [1] * (bones - 1) + [3]
        return random.choices(range(1, bones + 1), k=pairs, weights=weights)
    return random.choices(range(1, bones + 1), k=pairs)
