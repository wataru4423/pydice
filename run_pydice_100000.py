#!/usr/bin/env python3
"""Script to run pydice 100,000 times and save results to CSV."""

import csv
import random
from typing import List


def roll(pairs: int, bones: int, weight: bool) -> List[int]:
    """Dice roll function (copied from pydice.main)

    Args:
        pairs (int): Number of dice
        bones (int): Number of sides
        weight (bool): Weighted dice

    Returns:
        List[int]: Value of each die
    """
    if weight:
        weights = [1] * (bones - 1) + [3]
        return random.choices(range(1, bones + 1), k=pairs, weights=weights)
    return random.choices(range(1, bones + 1), k=pairs)


def run_pydice_100000(
    dice: str = "1d6",
    weight: bool = False,
    output_file: str = "pydice_100000_results.csv",
    iterations: int = 100000,
) -> None:
    """Run pydice multiple times and save results to CSV.
    
    Args:
        dice: Dice format string (e.g., "1d6", "2d20")
        weight: Whether to use weighted dice
        output_file: Path to the output CSV file
        iterations: Number of iterations to run
    """
    # Parse dice string
    pairs_str, bones_str = dice.split("d")
    pairs = int(pairs_str)
    bones = int(bones_str)
    
    print(f"Running pydice {iterations} times with {dice} (weight={weight})...")
    
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["iteration"] + [f"die_{i+1}" for i in range(pairs)] + ["sum"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(1, iterations + 1):
            # Roll the dice
            rolls = roll(pairs, bones, weight)
            total = sum(rolls)
            
            # Prepare row data
            row = {"iteration": i, "sum": total}
            for idx, value in enumerate(rolls):
                row[f"die_{idx+1}"] = value
            
            writer.writerow(row)
            
            # Print progress every 10,000 iterations
            if i % 10000 == 0:
                print(f"Completed {i}/{iterations} iterations...")
    
    print(f"Done! Results saved to {output_file}")


if __name__ == "__main__":
    # Default: run with 1d6, no weight
    run_pydice_100000(dice="1d6", weight=False)
