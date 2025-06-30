import random
from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(
    bones: Annotated[
        int, typer.Option(min=1, max=1000, help="Number of sides on the dice")
    ] = 6,
    pairs: Annotated[
        int, typer.Option(min=1, max=100, help="Number of dice to roll")
    ] = 1,
    weight: bool = False,
):
    """Dice roll application.\n
    Default: to roll a 6-sided dice.\n
    If --weight is set, last number will be weighted to 3.
    """

    def roll(bones, pairs, weight):
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

        return sum(dice)

    print(roll(bones, pairs, weight))
