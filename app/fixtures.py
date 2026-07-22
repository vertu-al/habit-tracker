"""Predefined habit and completion data for demonstration and testing."""

from datetime import datetime, timedelta

from app.database import HabitRepository
from app.models import Habit, Periodicity


def load_example_data(repository: HabitRepository) -> None:
    """Load five predefined habits with four weeks of tracking data.

    Data is only inserted when the database contains no habits.
    """

    if repository.get_all_habits():
        return

    today = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)

    habits = [
        Habit(
            name="Read",
            description="Read for at least twenty minutes",
            periodicity=Periodicity.DAILY,
            created_at=today - timedelta(days=28),
        ),
        Habit(
            name="Meditate",
            description="Meditate for ten minutes",
            periodicity=Periodicity.DAILY,
            created_at=today - timedelta(days=28),
        ),
        Habit(
            name="Journal",
            description="Write a short journal entry",
            periodicity=Periodicity.DAILY,
            created_at=today - timedelta(days=28),
        ),
        Habit(
            name="Exercise",
            description="Complete one exercise session",
            periodicity=Periodicity.WEEKLY,
            created_at=today - timedelta(days=28),
        ),
        Habit(
            name="Plan the week",
            description="Review goals and plan the coming week",
            periodicity=Periodicity.WEEKLY,
            created_at=today - timedelta(days=28),
        ),
    ]

    stored_habits = [
        repository.add_habit(habit)
        for habit in habits
    ]

    read, meditate, journal, exercise, planning = stored_habits

    # Daily habit: long uninterrupted streak.
    for days_ago in range(27, -1, -1):
        repository.add_completion(
            read.habit_id,
            today - timedelta(days=days_ago),
        )

    # Daily habit: regular completions with occasional missed days.
    for days_ago in range(27, -1, -2):
        repository.add_completion(
            meditate.habit_id,
            today - timedelta(days=days_ago),
        )

    # Daily habit: more irregular completion pattern.
    for days_ago in (27, 26, 23, 21, 20, 16, 15, 12, 8, 7, 3, 1):
        repository.add_completion(
            journal.habit_id,
            today - timedelta(days=days_ago),
        )

    # Weekly habits: one completion in each of four weeks.
    for weeks_ago in range(3, -1, -1):
        repository.add_completion(
            exercise.habit_id,
            today - timedelta(weeks=weeks_ago),
        )

    for weeks_ago in (3, 2, 0):
        repository.add_completion(
            planning.habit_id,
            today - timedelta(weeks=weeks_ago),
        )
    