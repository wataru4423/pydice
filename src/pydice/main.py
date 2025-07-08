import random
import re
from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(
    dice: Annotated[str, typer.Argument(help="Dice to roll, e.g. 2d6")] = "1d6",
    bones: Annotated[
        int, typer.Option(min=1, max=1000, help="Number of sides on the dice")
    ] = 6,
    pairs: Annotated[
        int, typer.Option(min=1, max=100, help="Number of dice to roll")
    ] = 1,
    weight: Annotated[bool, typer.Option(help="Weighted dice")] = False,
    each: Annotated[bool, typer.Option(help="Return each die value")] = False,
):
    """Dice roll application.\n
    Default: to roll a 6-sided dice and return sum value.\n
    If --weight is set, last number will be weighted to 3.\n
    If --each is set, each die value will be returned instead of the sum value.
    """

    if not re.fullmatch(r"(\d{1,2}|100)[d](\d{1,3}|1000)", dice):
        print("Invalid dice format. Please use the format like 2d6.")
        raise typer.Exit(code=1)

    pairs, bones = map(int, dice.split("d"))

    rolls = roll(bones, pairs, weight)
    if each:
        print(*rolls, sep=", ")
    else:
        print(sum(rolls))


def roll(bones: int, pairs: int, weight: bool) -> list[int]:
    """
    dice roll function
    """
    die = list(range(1, bones + 1))
    if weight:
        weights = [1] * bones
        weights[-1] = 3
        dice = random.choices(die, k=pairs, weights=weights)
    else:
        dice = random.choices(die, k=pairs)

    return dice
