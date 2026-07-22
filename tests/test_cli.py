"""Tests for CLI input helpers."""

from datetime import date, datetime
from unittest.mock import patch

from app.cli import HabitTrackerCLI
from app.models import Habit, Periodicity

def test_completion_date_uses_today_when_empty() -> None:
    with patch("builtins.input", return_value=""):
        result = HabitTrackerCLI._ask_completion_date()

    assert result is not None
    assert result.date() == datetime.now().date()


def test_completion_date_accepts_valid_date() -> None:
    with patch(
        "builtins.input",
        return_value="2026-07-01",
    ):
        result = HabitTrackerCLI._ask_completion_date()

    assert result == datetime(2026, 7, 1)


def test_completion_date_rejects_invalid_format(
    capsys,
) -> None:
    with patch(
        "builtins.input",
        return_value="01-07-2026",
    ):
        result = HabitTrackerCLI._ask_completion_date()

    captured = capsys.readouterr()

    assert result is None
    assert "Invalid date" in captured.out


def test_completion_date_rejects_future_date(
    capsys,
) -> None:
    with patch(
        "builtins.input",
        return_value="2999-01-01",
    ):
        result = HabitTrackerCLI._ask_completion_date()

    captured = capsys.readouterr()

    assert result is None
    assert "future" in captured.out

def test_print_month_shows_completed_days(
    capsys,
) -> None:
    habit = Habit(
        name="Read",
        description="Read daily",
        periodicity=Periodicity.DAILY,
        completions=[
            datetime(2026, 7, 1),
            datetime(2026, 7, 3),
        ],
    )

    HabitTrackerCLI._print_month(
        habit,
        reference_date=date(2026, 7, 22),
    )

    captured = capsys.readouterr()

    assert "Read — July 2026" in captured.out
    assert "■" in captured.out
    assert "▲" in captured.out


def test_print_month_ignores_other_months(
    capsys,
) -> None:
    habit = Habit(
        name="Exercise",
        description="Exercise weekly",
        periodicity=Periodicity.WEEKLY,
        completions=[
            datetime(2026, 6, 30),
        ],
    )

    HabitTrackerCLI._print_month(
        habit,
        reference_date=date(2026, 7, 22),
    )

    captured = capsys.readouterr()

    calendar_output = captured.out.split(
        "■ completed"
    )[0]

    assert "■" not in calendar_output