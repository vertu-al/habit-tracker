"""Tests for functional habit analytics."""

from datetime import date, datetime

from app.analytics import (
    current_streak_for_habit,
    get_all_habits,
    get_habits_by_periodicity,
    habit_with_longest_streak,
    longest_streak_for_habit,
    longest_streak_overall,
)

from app.models import Habit, Periodicity

def test_get_all_habits_returns_all_items() -> None:
    habits = [
        Habit(
            name="Read",
            description="Read daily",
            periodicity=Periodicity.DAILY,
        ),
        Habit(
            name="Exercise",
            description="Exercise weekly",
            periodicity=Periodicity.WEEKLY,
        ),
    ]

    result = get_all_habits(habits)

    assert result == habits
    assert result is not habits


def test_filter_habits_by_periodicity() -> None:
    habits = [
        Habit(
            name="Read",
            description="Read daily",
            periodicity=Periodicity.DAILY,
        ),
        Habit(
            name="Meditate",
            description="Meditate daily",
            periodicity=Periodicity.DAILY,
        ),
        Habit(
            name="Exercise",
            description="Exercise weekly",
            periodicity=Periodicity.WEEKLY,
        ),
    ]

    daily_habits = get_habits_by_periodicity(
        habits,
        Periodicity.DAILY,
    )

    assert [habit.name for habit in daily_habits] == [
        "Read",
        "Meditate",
    ]


def test_daily_longest_streak() -> None:
    habit = Habit(
        name="Read",
        description="Read daily",
        periodicity=Periodicity.DAILY,
        completions=[
            datetime(2026, 7, 20, 9, 0),
            datetime(2026, 7, 21, 9, 0),
            datetime(2026, 7, 22, 9, 0),
            datetime(2026, 7, 25, 9, 0),
        ],
    )

    assert longest_streak_for_habit(habit) == 3


def test_daily_duplicate_dates_count_once() -> None:
    habit = Habit(
        name="Drink water",
        description="Drink water daily",
        periodicity=Periodicity.DAILY,
        completions=[
            datetime(2026, 7, 20, 8, 0),
            datetime(2026, 7, 20, 18, 0),
            datetime(2026, 7, 21, 9, 0),
        ],
    )

    assert longest_streak_for_habit(habit) == 2


def test_weekly_longest_streak() -> None:
    habit = Habit(
        name="Exercise",
        description="Exercise weekly",
        periodicity=Periodicity.WEEKLY,
        completions=[
            datetime(2026, 7, 6, 10, 0),
            datetime(2026, 7, 13, 10, 0),
            datetime(2026, 7, 20, 10, 0),
            datetime(2026, 8, 3, 10, 0),
        ],
    )

    assert longest_streak_for_habit(habit) == 3


def test_empty_habit_has_zero_streak() -> None:
    habit = Habit(
        name="Journal",
        description="Journal daily",
        periodicity=Periodicity.DAILY,
    )

    assert longest_streak_for_habit(habit) == 0


def test_longest_streak_overall() -> None:
    read = Habit(
        name="Read",
        description="Read daily",
        periodicity=Periodicity.DAILY,
        completions=[
            datetime(2026, 7, 20),
            datetime(2026, 7, 21),
        ],
    )

    meditate = Habit(
        name="Meditate",
        description="Meditate daily",
        periodicity=Periodicity.DAILY,
        completions=[
            datetime(2026, 7, 20),
            datetime(2026, 7, 21),
            datetime(2026, 7, 22),
            datetime(2026, 7, 23),
        ],
    )

    assert longest_streak_overall([read, meditate]) == 4


def test_habit_with_longest_streak() -> None:
    read = Habit(
        name="Read",
        description="Read daily",
        periodicity=Periodicity.DAILY,
        completions=[
            datetime(2026, 7, 20),
            datetime(2026, 7, 21),
        ],
    )

    exercise = Habit(
        name="Exercise",
        description="Exercise weekly",
        periodicity=Periodicity.WEEKLY,
        completions=[
            datetime(2026, 7, 6),
            datetime(2026, 7, 13),
            datetime(2026, 7, 20),
        ],
    )

    result = habit_with_longest_streak([read, exercise])

    assert result is exercise

def test_current_daily_streak_completed_today() -> None:
    habit = Habit(
        name="Read",
        description="Read daily",
        periodicity=Periodicity.DAILY,
        completions=[
            datetime(2026, 7, 20),
            datetime(2026, 7, 21),
            datetime(2026, 7, 22),
        ],
    )

    result = current_streak_for_habit(
        habit,
        reference_date=date(2026, 7, 22),
    )

    assert result == 3


def test_current_daily_streak_completed_yesterday() -> None:
    habit = Habit(
        name="Meditate",
        description="Meditate daily",
        periodicity=Periodicity.DAILY,
        completions=[
            datetime(2026, 7, 19),
            datetime(2026, 7, 20),
            datetime(2026, 7, 21),
        ],
    )

    result = current_streak_for_habit(
        habit,
        reference_date=date(2026, 7, 22),
    )

    assert result == 3


def test_current_daily_streak_resets_after_missed_period() -> None:
    habit = Habit(
        name="Journal",
        description="Journal daily",
        periodicity=Periodicity.DAILY,
        completions=[
            datetime(2026, 7, 17),
            datetime(2026, 7, 18),
            datetime(2026, 7, 19),
        ],
    )

    result = current_streak_for_habit(
        habit,
        reference_date=date(2026, 7, 22),
    )

    assert result == 0


def test_current_weekly_streak() -> None:
    habit = Habit(
        name="Exercise",
        description="Exercise weekly",
        periodicity=Periodicity.WEEKLY,
        completions=[
            datetime(2026, 7, 6),
            datetime(2026, 7, 13),
            datetime(2026, 7, 20),
        ],
    )

    result = current_streak_for_habit(
        habit,
        reference_date=date(2026, 7, 22),
    )

    assert result == 3


def test_current_streak_is_zero_without_completions() -> None:
    habit = Habit(
        name="Read",
        description="Read daily",
        periodicity=Periodicity.DAILY,
    )

    result = current_streak_for_habit(
        habit,
        reference_date=date(2026, 7, 22),
    )

    assert result == 0