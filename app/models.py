"""Domain models for the habit tracker."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Periodicity(str, Enum):
    """Supported repetition periods for habits."""

    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class Habit:
    """Represent a habit and its recorded completions."""

    name: str
    description: str
    periodicity: Periodicity
    created_at: datetime = field(default_factory=datetime.now)
    completions: list[datetime] = field(default_factory=list)
    habit_id: int | None = None

    def __post_init__(self) -> None:
        """Validate the habit after initialization."""

        self.name = self.name.strip()
        self.description = self.description.strip()

        if not self.name:
            raise ValueError("Habit name must not be empty.")

        if not isinstance(self.periodicity, Periodicity):
            try:
                self.periodicity = Periodicity(self.periodicity)
            except ValueError as error:
                raise ValueError(
                    "Periodicity must be either 'daily' or 'weekly'."
                ) from error

    def complete(self, completed_at: datetime | None = None) -> datetime:
        """Record and return a completion timestamp."""

        timestamp = completed_at or datetime.now()
        self.completions.append(timestamp)
        return timestamp