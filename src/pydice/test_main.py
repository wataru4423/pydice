from hypothesis import given
from hypothesis import strategies as st
from pytest_mock import MockerFixture
from typer.testing import CliRunner

from .main import app, roll

runner = CliRunner()


class TestMain:
    """Test suite for the main CLI application."""

    def test_main_default(self, mocker: MockerFixture):
        """Tests the main function with default arguments."""
        mocker.patch("random.choices", return_value=[2])
        result = runner.invoke(app, ["1d6"])
        assert result.exit_code == 0
        assert result.stdout == "2\n"

    def test_main_stdout(self):
        """Tests the main function's stdout output."""
        result = runner.invoke(app, ["1d1"])
        assert result.exit_code == 0
        assert result.stdout == "1\n"

    def test_each_die_value_returned(self):
        """Tests that each die value is returned if each flag is set."""
        result = runner.invoke(app, ["2d1", "--each"])
        assert result.exit_code == 0
        assert result.stdout == "1, 1\n"

    def test_sum_value_returned(self):
        """Tests that sum value is returned."""
        result = runner.invoke(app, ["3d1"])
        assert result.exit_code == 0
        assert result.stdout == "3\n"

    def test_dice_format_error_message(self):
        """Tests error message when dice format is invalid."""
        result = runner.invoke(app, ["1D6"])
        assert result.exit_code == 1
        assert result.stdout == "Invalid dice format. Please use the format like 2d6.\n"

    def test_main_with_weight_option(self, mocker: MockerFixture):
        """Tests that the --weight option calls roll() with weight=True."""
        mock_roll = mocker.patch("pydice.main.roll", return_value=[1, 2, 3])
        result = runner.invoke(app, ["3d6", "--weight"])
        assert result.exit_code == 0
        assert result.stdout == "6\n"
        mock_roll.assert_called_once_with(pairs=3, bones=6, weight=True)

    def test_corner_case_0d0(self):
        result = runner.invoke(app, ["0d0"])
        assert result.exit_code == 1

    def test_corner_case_0d1(self):
        result = runner.invoke(app, ["0d1"])
        assert result.exit_code == 1

    def test_corner_case_1d0(self):
        result = runner.invoke(app, ["1d0"])
        assert result.exit_code == 1

    def test_corner_case_101d6(self):
        result = runner.invoke(app, ["101d6"])
        assert result.exit_code == 1

    def test_corner_case_100d6(self):
        result = runner.invoke(app, ["100d6"])
        assert result.exit_code == 0

    def test_corner_case_1d1001(self):
        result = runner.invoke(app, ["1d1001"])
        assert result.exit_code == 1

    def test_corner_case_1d1000(self):
        result = runner.invoke(app, ["1d1000"])
        assert result.exit_code == 0


class TestRoll:
    """Test suite for the roll function."""

    def test_roll_returns_list(self):
        """Tests that roll() returns a list."""
        result = roll(pairs=3, bones=6, weight=False)
        assert isinstance(result, list)

    def test_roll_return(self, mocker: MockerFixture):
        """Tests return value."""
        mocker.patch("random.choices", return_value=[1, 2, 3])
        result = roll(pairs=3, bones=6, weight=False)
        assert result == [1, 2, 3]

    def test_roll_returns_correct_number_of_dice(self):
        """Tests that roll() returns a list with the correct number of items."""
        result = roll(pairs=3, bones=6, weight=False)
        assert len(result) == 3

    def test_roll_values_are_within_bounds(self):
        """Tests that all rolled values are within the die's faces."""
        pairs = 10
        bones = 12
        result = roll(pairs, bones, weight=False)
        for die_roll in result:
            assert 1 <= die_roll <= bones

    def test_roll_with_weight(self, mocker: MockerFixture):
        """Tests roll() with weight=True calls random.choices with weights."""
        mock_choices = mocker.patch("random.choices", return_value=[1])
        bones = 6
        roll(pairs=1, bones=bones, weight=True)
        weights = [1 / (i + 1) for i in range(bones)]
        mock_choices.assert_called_once_with(
            population=range(1, bones + 1), weights=weights, k=1
        )

    @given(
        st.integers(min_value=1, max_value=100),
        st.integers(min_value=1, max_value=1000),
    )
    def test_roll_property(self, pairs, bones):
        """Property-based test for the roll function."""
        result = roll(pairs, bones, weight=False)
        assert len(result) == pairs
        assert all(1 <= die_roll <= bones for die_roll in result)
