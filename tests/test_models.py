"""Tests for the habit domain model."""

from datetime import datetime

import pytest

from app.models import Habit, Periodicity


def test_create_daily_habit() -> None:
    habit = Habit(
        name="Drink water",
        description="Drink two litres of water",
        periodicity=Periodicity.DAILY,
    )

    assert habit.name == "Drink water"
    assert habit.description == "Drink two litres of water"
    assert habit.periodicity == Periodicity.DAILY
    assert habit.habit_id is None
    assert habit.completions == []


def test_complete_habit() -> None:
    habit = Habit(
        name="Read",
        description="Read for twenty minutes",
        periodicity=Periodicity.DAILY,
    )

    completion_time = datetime(2026, 7, 22, 20, 30)
    returned_time = habit.complete(completion_time)

    assert returned_time == completion_time
    assert habit.completions == [completion_time]


def test_periodicity_can_be_created_from_string() -> None:
    habit = Habit(
        name="Exercise",
        description="Complete one workout",
        periodicity="weekly",
    )

    assert habit.periodicity == Periodicity.WEEKLY


def test_empty_name_is_rejected() -> None:
    with pytest.raises(ValueError, match="Habit name must not be empty"):
        Habit(
            name="   ",
            description="Invalid habit",
            periodicity=Periodicity.DAILY,
        )


def test_invalid_periodicity_is_rejected() -> None:
    with pytest.raises(ValueError, match="daily.*weekly"):
        Habit(
            name="Meditate",
            description="Meditate regularly",
            periodicity="monthly",
        )