"""Application entry point."""

from app.cli import HabitTrackerCLI
from app.database import HabitRepository
from app.services import HabitService


def main() -> None:
    repository = HabitRepository("data/habits.db")
    service = HabitService(repository)
    cli = HabitTrackerCLI(service)

    cli.run()


if __name__ == "__main__":
    main()