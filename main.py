"""Application entry point."""

from app.cli import HabitTrackerCLI
from app.database import HabitRepository
from app.services import HabitService
from app.fixtures import load_example_data


def main() -> None:
    """Initialize and run the habit tracker application."""

    repository = HabitRepository("data/habits.db")
    load_example_data(repository)

    service = HabitService(repository)
    cli = HabitTrackerCLI(service)
    cli.run()

if __name__ == "__main__":
    main()