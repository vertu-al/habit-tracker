"""Tests for the SQLite habit repository."""

from datetime import datetime

import pytest

from app.database import HabitRepository
from app.models import Habit, Periodicity


@pytest.fixture
def repository(tmp_path) -> HabitRepository:
    """Create an isolated temporary database for each test."""

    return HabitRepository(tmp_path / "test_habits.db")


def test_add_and_retrieve_habit(
    repository: HabitRepository,
) -> None:
    habit = Habit(
        name="Read",
        description="Read for twenty minutes",
        periodicity=Periodicity.DAILY,
    )

    repository.add_habit(habit)
    stored_habit = repository.get_habit(habit.habit_id)

    assert habit.habit_id is not None
    assert stored_habit is not None
    assert stored_habit.name == "Read"
    assert stored_habit.periodicity == Periodicity.DAILY


def test_get_all_habits(
    repository: HabitRepository,
) -> None:
    repository.add_habit(
        Habit(
            name="Read",
            description="Read daily",
            periodicity=Periodicity.DAILY,
        )
    )

    repository.add_habit(
        Habit(
            name="Exercise",
            description="Exercise weekly",
            periodicity=Periodicity.WEEKLY,
        )
    )

    habits = repository.get_all_habits()

    assert len(habits) == 2
    assert [habit.name for habit in habits] == [
        "Read",
        "Exercise",
    ]


def test_add_completion(
    repository: HabitRepository,
) -> None:
    habit = repository.add_habit(
        Habit(
            name="Meditate",
            description="Meditate daily",
            periodicity=Periodicity.DAILY,
        )
    )

    completion_time = datetime(2026, 7, 22, 9, 0)
    repository.add_completion(
        habit.habit_id,
        completion_time,
    )

    stored_habit = repository.get_habit(habit.habit_id)

    assert stored_habit is not None
    assert stored_habit.completions == [completion_time]


def test_daily_duplicate_completion_is_rejected(
    repository: HabitRepository,
) -> None:
    habit = repository.add_habit(
        Habit(
            name="Drink water",
            description="Drink water daily",
            periodicity=Periodicity.DAILY,
        )
    )

    repository.add_completion(
        habit.habit_id,
        datetime(2026, 7, 22, 9, 0),
    )

    with pytest.raises(
        ValueError,
        match="already been completed",
    ):
        repository.add_completion(
            habit.habit_id,
            datetime(2026, 7, 22, 18, 0),
        )


def test_weekly_duplicate_completion_is_rejected(
    repository: HabitRepository,
) -> None:
    habit = repository.add_habit(
        Habit(
            name="Exercise",
            description="Exercise weekly",
            periodicity=Periodicity.WEEKLY,
        )
    )

    repository.add_completion(
        habit.habit_id,
        datetime(2026, 7, 20, 10, 0),
    )

    with pytest.raises(
        ValueError,
        match="already been completed",
    ):
        repository.add_completion(
            habit.habit_id,
            datetime(2026, 7, 24, 10, 0),
        )


def test_delete_habit(
    repository: HabitRepository,
) -> None:
    habit = repository.add_habit(
        Habit(
            name="Journal",
            description="Write in journal",
            periodicity=Periodicity.DAILY,
        )
    )

    deleted = repository.delete_habit(habit.habit_id)

    assert deleted is True
    assert repository.get_habit(habit.habit_id) is None