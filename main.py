from app.models import Habit, Periodicity


def main() -> None:
    habit = Habit(
        name="Drink water",
        description="Drink at least two litres of water",
        periodicity=Periodicity.DAILY,
    )

    habit.complete()

    print(habit)
    print(f"Completions: {len(habit.completions)}")


if __name__ == "__main__":
    main()
