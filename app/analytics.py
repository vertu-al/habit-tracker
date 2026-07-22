"""Functional analytics for habit tracking."""

from datetime import date, datetime, timedelta
from itertools import groupby

from app.models import Habit, Periodicity


def get_all_habits(habits: list[Habit]) -> list[Habit]:
    """Return all habits without modifying the input."""

    return list(habits)


def get_habits_by_periodicity(
    habits: list[Habit],
    periodicity: Periodicity,
) -> list[Habit]:
    """Return habits matching the specified periodicity."""

    return list(
        filter(
            lambda habit: habit.periodicity == periodicity,
            habits,
        )
    )


def longest_streak_for_habit(habit: Habit) -> int:
    """Return the longest completed-period streak for one habit."""

    period_dates = _completion_periods(habit)

    if not period_dates:
        return 0

    groups = groupby(
        enumerate(period_dates),
        key=lambda item: _grouping_key(
            item[0],
            item[1],
            habit.periodicity,
        ),
    )

    return max(
        len(list(group))
        for _, group in groups
    )

def current_streak_for_habit(
    habit: Habit,
    reference_date: date | None = None,
    ) -> int:
    """Return the habit's current consecutive-period streak."""

    period_dates = _completion_periods(habit)

    if not period_dates:
        return 0

    today = reference_date or date.today()

    if habit.periodicity == Periodicity.DAILY:
        current_period = today
        step = timedelta(days=1)
    else:
        current_period = today - timedelta(
            days=today.weekday()
        )
        step = timedelta(weeks=1)

    latest_period = period_dates[-1]

    if latest_period not in {
        current_period,
        current_period - step,
    }:
        return 0

    streak = 1
    expected_period = latest_period - step

    for period in reversed(period_dates[:-1]):
        if period == expected_period:
            streak += 1
            expected_period -= step
        elif period < expected_period:
            break

    return streak

def longest_streak_overall(habits: list[Habit]) -> int:
    """Return the longest streak among all habits."""

    return max(
        map(longest_streak_for_habit, habits),
        default=0,
    )


def habit_with_longest_streak(
    habits: list[Habit],
) -> Habit | None:
    """Return the habit with the longest streak."""

    return max(
        habits,
        key=longest_streak_for_habit,
        default=None,
    )


def _completion_periods(habit: Habit) -> list[date]:
    """Return sorted unique dates representing completed periods."""

    if habit.periodicity == Periodicity.DAILY:
        periods = map(
            lambda completion: completion.date(),
            habit.completions,
        )
    else:
        periods = map(
            _start_of_iso_week,
            habit.completions,
        )

    return sorted(set(periods))


def _start_of_iso_week(timestamp: datetime) -> date:
    """Return the Monday of the timestamp's ISO week."""

    completion_date = timestamp.date()

    return completion_date - timedelta(
        days=completion_date.weekday()
    )


def _grouping_key(
    index: int,
    period_date: date,
    periodicity: Periodicity,
) -> date:
    """Create a constant key for consecutive periods."""

    step = (
        timedelta(days=1)
        if periodicity == Periodicity.DAILY
        else timedelta(weeks=1)
    )

    return period_date - index * step