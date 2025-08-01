import pytest
from hypothesis import given
from hypothesis import strategies as st
from pytest_mock import MockerFixture
from typer.testing import CliRunner

from .main import app, roll

runner = CliRunner()


class TestMain:
    """Test suite for the main CLI application."""

    def test_invoke(self):
        """Tests launch application"""
        result = runner.invoke(app)
        assert result.exit_code == 0

    def test_version_option(self, mocker: MockerFixture):
        """Tests the --version option."""
        mocker.patch("importlib.metadata.version", return_value="0.1.0")
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "pydice 0.1.0" in result.stdout

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

    def test_each_die_value_returned_a_dice(self):
        """Tests that each die value is returned a die."""
        result = runner.invoke(app, ["1d1", "--each"])
        assert result.exit_code == 0
        assert result.stdout == "1\n"

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

    def test_main_with_weight_option(self):
        """Tests that the --weight option calls roll() with weight=True."""
        result = runner.invoke(app, ["3d6", "--weight"])
        assert result.exit_code == 0

    @pytest.mark.parametrize(
        "dice_input, expected_exit_code",
        [
            ("0d0", 1),
            ("0d1", 1),
            ("1d0", 1),
            ("1d1", 0),
            ("01d1", 1),
            ("1d01", 1),
            ("101d6", 1),
            ("100d6", 0),
            ("1d1001", 1),
            ("1d1000", 0),
        ],
    )
    def test_corner_cases(self, dice_input, expected_exit_code):
        """Tests corner cases for dice input format."""
        result = runner.invoke(app, [dice_input])
        assert result.exit_code == expected_exit_code


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

    def test_weights_are_correctly_set_when_weighted(self, mocker: MockerFixture):
        """
        Tests that the entire weights list is correctly constructed when weight=True.
        """
        mock_choices = mocker.patch("pydice.main.random.choices")
        bones = 6
        roll(pairs=1, bones=bones, weight=True)

        expected_weights = [1] * (bones - 1) + [3]
        kwargs = mock_choices.call_args.kwargs

        assert "weights" in kwargs
        assert kwargs["weights"] == expected_weights


class TestDiceProperty:
    """Test suite for property-based testing of the roll function."""

    @given(
        st.integers(min_value=1, max_value=100),
        st.integers(min_value=1, max_value=1000),
    )
    def test_dice_property(self, pairs, bones):
        """Property-based test for the roll function."""
        result = roll(pairs, bones, weight=False)
        assert len(result) == pairs
        assert all(1 <= die_roll <= bones for die_roll in result)
