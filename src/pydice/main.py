import importlib.metadata
import random
import re
from typing import Annotated, Optional

import typer

__version__ = importlib.metadata.version("pydice")
app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(f"pydice: {__version__}")
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
    """Dice roll application
    Default: to roll a 6-sided dice and return sum value.
    Max: 100d1000.
    First number: Number of dice.
    Second number: Number of sides.
    If --weight is set, last number will be weighted to 3.
    If --each is set, each die value will be returned instead of the sum value.
    """

    if not re.fullmatch(r"([1-9]\d?|100)[d]([1-9]\d{0,2}|1000)", dice):
        print("Invalid dice format. Please use the format like 2d6.")
        raise typer.Exit(code=1)
    else:
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
    die = list(range(1, bones + 1))
    if weight:
        weights = [1] * bones
        weights[-1] = 3
        dice = random.choices(die, k=pairs, weights=weights)
    else:
        dice = random.choices(die, k=pairs)

    return dice
