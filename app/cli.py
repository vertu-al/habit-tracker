"""Command-line interface for the habit tracker."""

from calendar import monthrange
from datetime import date, datetime

from app.analytics import (
    current_streak_for_habit,
    get_habits_by_periodicity,
    habit_with_longest_streak,
    longest_streak_for_habit,
    longest_streak_overall,
)

from app.models import Habit, Periodicity
from app.services import HabitService


class HabitTrackerCLI:
    """Interactive command-line interface."""

    def __init__(self, service: HabitService) -> None:
        self.service = service

    def run(self) -> None:
        """Start the application menu."""

        print("\nWelcome to the Habit Tracker.")

        while True:
            self._show_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self._create_habit()
            elif choice == "2":
                self._complete_habit()
            elif choice == "3":
                self._show_all_habits()
            elif choice == "4":
                self._show_analytics()
            elif choice == "5":
                self._delete_habit()
            elif choice == "6":
                print("Goodbye.")
                break
            else:
                print("Invalid option. Please choose 1 to 6.")

    @staticmethod
    def _show_menu() -> None:
        print(
            """
================================
          HABIT TRACKER
================================
1. Create habit
2. Complete habit
3. Show all habits
4. Show analytics
5. Delete habit
6. Exit
"""
        )

    def _create_habit(self) -> None:
        print("\nCreate a new habit")

        name = input("Name: ").strip()
        description = input("Description: ").strip()
        periodicity = self._ask_periodicity()

        try:
            habit = self.service.create_habit(
                name=name,
                description=description,
                periodicity=periodicity,
            )
        except ValueError as error:
            print(f"Could not create habit: {error}")
            return

        print(
            f"Habit created successfully "
            f"with ID {habit.habit_id}."
        )

    def _complete_habit(self) -> None:
        habits = self.service.get_all_habits()

        if not habits:
            print("\nNo habits are currently stored.")
            return

        self._print_habits(habits)

        habit_id = self._ask_habit_id(
            "Enter the ID of the completed habit: "
        )

        if habit_id is None:
            return

        completed_at = self._ask_completion_date()

        if completed_at is None:
            return

        try:
            self.service.complete_habit(
            habit_id,
            completed_at,
        )
        except ValueError as error:
            print(f"Could not complete habit: {error}")
            return

        print(
            "Habit completion recorded for "
            f"{completed_at.date().isoformat()}."
        )

    def _show_all_habits(self) -> None:
        habits = self.service.get_all_habits()

        if not habits:
            print("\nNo habits are currently stored.")
            return

        print("\nTracked habits")
        self._print_habits(habits)

    def _show_analytics(self) -> None:
        habits = self.service.get_all_habits()

        if not habits:
            print("\nNo habits are available for analysis.")
            return

        while True:
            print(
                """
Analytics
1. Show daily habits
2. Show weekly habits
3. Show longest streak overall
4. Show habit with longest streak
5. Show streak details
6. Show completion history
7. Return to main menu
"""
            )

            choice = input(
                "Choose an analytics option: "
            ).strip()

            if choice == "1":
                daily_habits = get_habits_by_periodicity(
                    habits,
                    Periodicity.DAILY,
                )
                self._print_habits(daily_habits)

            elif choice == "2":
                weekly_habits = get_habits_by_periodicity(
                    habits,
                    Periodicity.WEEKLY,
                )
                self._print_habits(weekly_habits)

            elif choice == "3":
                streak = longest_streak_overall(habits)
                print(f"\nLongest streak overall: {streak}")

            elif choice == "4":
                habit = habit_with_longest_streak(habits)

                if habit is None:
                    print("\nNo habit data available.")
                else:
                    streak = longest_streak_for_habit(
                        habit
                    )
                    print(
                        f"\nHabit with longest streak: "
                        f"{habit.name} ({streak})"
                    )

            elif choice == "5":
                self._show_one_habit_streak(habits)

            elif choice == "6":
                self._show_history(habits)

            elif choice == "7":
                break

            else:
                print(
                    "Invalid option. Please choose 1 to 6."
                )

    def _show_one_habit_streak(
        self,
        habits: list[Habit],
    ) -> None:
        self._print_habits(habits)

        habit_id = self._ask_habit_id(
            "Enter the habit ID: "
        )

        if habit_id is None:
            return

        habit = next(
            (
                habit
                for habit in habits
                if habit.habit_id == habit_id
            ),
            None,
        )

        if habit is None:
            print("Habit not found.")
            return

        current_streak = current_streak_for_habit(habit)
        longest_streak = longest_streak_for_habit(habit)

        print(f"\n{habit.name}")
        print(f"Current streak: {current_streak}")
        print(f"Longest streak: {longest_streak}")

    def _show_history(
        self,
        habits: list[Habit],
    ) -> None:

        self._print_habits(habits)

        habit_id = self._ask_habit_id(
            "Select habit ID: "
        )

        if habit_id is None:
            return

        habit = next(
            (
                h
                for h in habits
                if h.habit_id == habit_id
            ),
            None,
        )

        if habit is None:
            print("Habit not found.")
            return

        self._print_month(habit)

    def _delete_habit(self) -> None:
        habits = self.service.get_all_habits()

        if not habits:
            print("\nNo habits are currently stored.")
            return

        self._print_habits(habits)

        habit_id = self._ask_habit_id(
            "Enter the ID of the habit to delete: "
        )

        if habit_id is None:
            return

        confirmation = input(
            "Are you sure you want to delete this habit? "
            "(y/n): "
        ).strip().lower()

        if confirmation != "y":
            print("Deletion cancelled.")
            return

        deleted = self.service.delete_habit(habit_id)

        if deleted:
            print("Habit deleted.")
        else:
            print("Habit not found.")

    @staticmethod
    def _ask_periodicity() -> Periodicity:
        while True:
            value = input(
                "Periodicity (daily/weekly): "
            ).strip().lower()

            try:
                return Periodicity(value)
            except ValueError:
                print(
                    "Please enter either 'daily' or "
                    "'weekly'."
                )

    @staticmethod
    def _ask_habit_id(prompt: str) -> int | None:
        value = input(prompt).strip()

        try:
            return int(value)
        except ValueError:
            print("Please enter a valid numerical ID.")
            return None

    @staticmethod
    def _ask_completion_date() -> datetime | None:
        """Ask for a completion date or use the current date."""

        value = input(
            "Completion date (YYYY-MM-DD), "
            "or press Enter for today: "
        ).strip()

        if not value:
            return datetime.now()

        try:
         selected_date = datetime.strptime(
                value,
                "%Y-%m-%d",
            )
        except ValueError:
            print(
                "Invalid date. Please use the format "
                "YYYY-MM-DD."
            )
            return None

        if selected_date.date() > datetime.now().date():
            print("A completion cannot be recorded in the future.")
            return None

        return selected_date

    @staticmethod
    def _print_habits(habits: list[Habit]) -> None:
        """Print habits in a formatted table."""

        if not habits:
            print("\nNo matching habits found.")
            return

        print()

        header = (
            f"{'ID':<4}"
            f"{'Habit':<20}"
            f"{'Type':<10}"
            f"{'Current':<10}"
            f"{'Longest':<10}"
            f"{'Done':<8}"
        )

        print(header)
        print("-" * len(header))

        for habit in habits:
            current = current_streak_for_habit(habit)
            longest = longest_streak_for_habit(habit)

            print(
                f"{habit.habit_id:<4}"
                f"{habit.name:<20}"
                f"{habit.periodicity.value.capitalize():<10}"
                f"{current:<10}"
                f"{longest:<10}"
                f"{len(habit.completions):<8}"
            )

        print()
    
    @staticmethod
    def _print_month(
            habit: Habit,
            reference_date: date | None = None,
        ) -> None:
            """Print completion history for one calendar month."""

            selected_date = reference_date or date.today()
            year = selected_date.year
            month = selected_date.month

            print()
            print(f"{habit.name} — {selected_date.strftime('%B %Y')}")
            print("Mo Tu We Th Fr Sa Su")

            first_weekday, days = monthrange(year, month)

            completed = {
                completion.date()
                for completion in habit.completions
                if completion.year == year
                and completion.month == month
            }

            line = "   " * first_weekday

            for day in range(1, days + 1):
                current = date(year, month, day)

                if current in completed:
                    symbol = "■"
                elif current == selected_date:
                    symbol = "▲"
                else:
                    symbol = "○"

                line += f"{symbol}  "

                if current.weekday() == 6:
                    print(line.rstrip())
                    line = ""

            if line:
                print(line.rstrip())

            print()
            print("■ completed   ○ not completed   ▲ today")
            print()