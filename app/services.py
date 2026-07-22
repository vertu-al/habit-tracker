"""Application service layer for habit management."""

from datetime import datetime

from app.database import HabitRepository
from app.models import Habit, Periodicity


class HabitService:
    """Coordinate habit-related application operations."""

    def __init__(self, repository: HabitRepository) -> None:
        self.repository = repository

    def create_habit(
        self,
        name: str,
        description: str,
        periodicity: Periodicity | str,
    ) -> Habit:
        """Create and store a new habit."""

        habit = Habit(
            name=name,
            description=description,
            periodicity=periodicity,
        )

        return self.repository.add_habit(habit)

    def get_all_habits(self) -> list[Habit]:
        """Return all stored habits."""

        return self.repository.get_all_habits()

    def get_habit(self, habit_id: int) -> Habit | None:
        """Return one habit by ID."""

        return self.repository.get_habit(habit_id)

    def complete_habit(
        self,
        habit_id: int,
        completed_at: datetime | None = None,
    ) -> datetime:
        """Record a completion for a habit."""

        return self.repository.add_completion(
            habit_id,
            completed_at,
        )

    def delete_habit(self, habit_id: int) -> bool:
        """Delete a habit."""

        return self.repository.delete_habit(habit_id)