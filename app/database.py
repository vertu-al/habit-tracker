"""SQLite persistence for the habit tracker."""

import sqlite3
from datetime import datetime
from pathlib import Path

from app.models import Habit, Periodicity


class HabitRepository:
    """Store and retrieve habits using SQLite."""

    def __init__(self, database_path: str | Path = "data/habits.db") -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize_database()

    def _connect(self) -> sqlite3.Connection:
        """Create a database connection."""

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize_database(self) -> None:
        """Create the required database tables."""

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    periodicity TEXT NOT NULL
                        CHECK (periodicity IN ('daily', 'weekly')),
                    created_at TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completed_at TEXT NOT NULL,
                    period_key TEXT NOT NULL,
                    FOREIGN KEY (habit_id)
                        REFERENCES habits(id)
                        ON DELETE CASCADE,
                    UNIQUE (habit_id, period_key)
                )
                """
            )

    def add_habit(self, habit: Habit) -> Habit:
        """Insert a habit and return it with its database ID."""

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO habits (
                    name,
                    description,
                    periodicity,
                    created_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    habit.name,
                    habit.description,
                    habit.periodicity.value,
                    habit.created_at.isoformat(),
                ),
            )

            habit.habit_id = cursor.lastrowid

        return habit

    def get_habit(self, habit_id: int) -> Habit | None:
        """Return one habit or None if it does not exist."""

        with self._connect() as connection:
            habit_row = connection.execute(
                """
                SELECT id, name, description, periodicity, created_at
                FROM habits
                WHERE id = ?
                """,
                (habit_id,),
            ).fetchone()

            if habit_row is None:
                return None

            completion_rows = connection.execute(
                """
                SELECT completed_at
                FROM completions
                WHERE habit_id = ?
                ORDER BY completed_at
                """,
                (habit_id,),
            ).fetchall()

        return self._row_to_habit(habit_row, completion_rows)

    def get_all_habits(self) -> list[Habit]:
        """Return all stored habits and their completions."""

        with self._connect() as connection:
            habit_rows = connection.execute(
                """
                SELECT id, name, description, periodicity, created_at
                FROM habits
                ORDER BY id
                """
            ).fetchall()

            habits = []

            for habit_row in habit_rows:
                completion_rows = connection.execute(
                    """
                    SELECT completed_at
                    FROM completions
                    WHERE habit_id = ?
                    ORDER BY completed_at
                    """,
                    (habit_row["id"],),
                ).fetchall()

                habits.append(
                    self._row_to_habit(habit_row, completion_rows)
                )

        return habits

    def add_completion(
        self,
        habit_id: int,
        completed_at: datetime | None = None,
    ) -> datetime:
        """Record one completion for the relevant habit period."""

        habit = self.get_habit(habit_id)

        if habit is None:
            raise ValueError(f"Habit with ID {habit_id} does not exist.")

        timestamp = completed_at or datetime.now()
        period_key = self._get_period_key(
            timestamp,
            habit.periodicity,
        )

        try:
            with self._connect() as connection:
                connection.execute(
                    """
                    INSERT INTO completions (
                        habit_id,
                        completed_at,
                        period_key
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        habit_id,
                        timestamp.isoformat(),
                        period_key,
                    ),
                )
        except sqlite3.IntegrityError as error:
            raise ValueError(
                "This habit has already been completed "
                "during the current period."
            ) from error

        return timestamp

    def delete_habit(self, habit_id: int) -> bool:
        """Delete a habit and return whether it existed."""

        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM habits WHERE id = ?",
                (habit_id,),
            )

        return cursor.rowcount > 0

    @staticmethod
    def _get_period_key(
        timestamp: datetime,
        periodicity: Periodicity,
    ) -> str:
        """Return a unique identifier for a daily or weekly period."""

        if periodicity == Periodicity.DAILY:
            return timestamp.date().isoformat()

        iso_year, iso_week, _ = timestamp.isocalendar()
        return f"{iso_year}-W{iso_week:02d}"

    @staticmethod
    def _row_to_habit(
        habit_row: sqlite3.Row,
        completion_rows: list[sqlite3.Row],
    ) -> Habit:
        """Convert database rows into a Habit object."""

        return Habit(
            habit_id=habit_row["id"],
            name=habit_row["name"],
            description=habit_row["description"],
            periodicity=habit_row["periodicity"],
            created_at=datetime.fromisoformat(
                habit_row["created_at"]
            ),
            completions=[
                datetime.fromisoformat(row["completed_at"])
                for row in completion_rows
            ],
        )