"""Tests for the habit service layer."""

from datetime import datetime

import pytest

from app.database import HabitRepository
from app.models import Periodicity
from app.services import HabitService


@pytest.fixture
def service(tmp_path) -> HabitService:
    repository = HabitRepository(
        tmp_path / "test_habits.db"
    )

    return HabitService(repository)


def test_create_habit(service: HabitService) -> None:
    habit = service.create_habit(
        name="Read",
        description="Read twenty minutes",
        periodicity=Periodicity.DAILY,
    )

    assert habit.habit_id is not None
    assert habit.name == "Read"
    assert habit.periodicity == Periodicity.DAILY


def test_get_all_habits(service: HabitService) -> None:
    service.create_habit(
        name="Read",
        description="Read daily",
        periodicity=Periodicity.DAILY,
    )

    service.create_habit(
        name="Exercise",
        description="Exercise weekly",
        periodicity=Periodicity.WEEKLY,
    )

    habits = service.get_all_habits()

    assert len(habits) == 2


def test_complete_habit(service: HabitService) -> None:
    habit = service.create_habit(
        name="Meditate",
        description="Meditate daily",
        periodicity=Periodicity.DAILY,
    )

    completion_time = datetime(2026, 7, 22, 10, 0)

    service.complete_habit(
        habit.habit_id,
        completion_time,
    )

    stored_habit = service.get_habit(habit.habit_id)

    assert stored_habit is not None
    assert stored_habit.completions == [completion_time]


def test_delete_habit(service: HabitService) -> None:
    habit = service.create_habit(
        name="Journal",
        description="Write daily",
        periodicity=Periodicity.DAILY,
    )

    result = service.delete_habit(habit.habit_id)

    assert result is True
    assert service.get_habit(habit.habit_id) is None
