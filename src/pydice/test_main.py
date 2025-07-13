from typer.testing import CliRunner

from .main import app, roll

runner = CliRunner()


def test_main_default():
    """Tests the main function with default arguments."""
    result = runner.invoke(app, ["1d6"])
    assert result.exit_code == 0


def test_main_stdout():
    """Tests the main function's stdout output."""
    result = runner.invoke(app, ["1d1"])
    assert result.exit_code == 0
    assert result.stdout == "1\n"


def test_corner_case_0d0():
    result = runner.invoke(app, ["0d0"])
    assert result.exit_code == 1


def test_corner_case_0d1():
    result = runner.invoke(app, ["0d1"])
    assert result.exit_code == 1


def test_corner_case_1d0():
    result = runner.invoke(app, ["1d0"])
    assert result.exit_code == 1


def test_corner_case_101d6():
    result = runner.invoke(app, ["101d6"])
    assert result.exit_code == 1


def test_corner_case_100d6():
    result = runner.invoke(app, ["100d6"])
    assert result.exit_code == 0


def test_corner_case_1d1001():
    result = runner.invoke(app, ["1d1001"])
    assert result.exit_code == 1


def test_corner_case_1d1000():
    result = runner.invoke(app, ["1d1000"])
    assert result.exit_code == 0


def test_dice_format_error_message():
    """Tests error message when dice format is invalid."""
    result = runner.invoke(app, ["0d6"])
    assert result.exit_code == 1
    assert result.stdout == "Invalid dice format. Please use the format like 2d6.\n"


def test_roll_returns_list():
    """Tests that roll() returns a list."""
    result = roll(pairs=3, bones=6, weight=False)
    assert isinstance(result, list)


def test_roll_returns_correct_number_of_dice():
    """Tests that roll() returns a list with the correct number of items."""
    result = roll(pairs=3, bones=6, weight=False)
    assert len(result) == 3


def test_roll_values_are_within_bounds():
    """Tests that all rolled values are within the die's faces."""
    pairs = 10
    bones = 12
    result = roll(pairs, bones, weight=False)
    for die_roll in result:
        assert 1 <= die_roll <= bones
