# Habit Tracker – Software Concept

## 1. Project Objective

The goal of this project is to develop a command-line habit tracking application using Python while demonstrating object-oriented and functional programming principles.

The application enables users to create habits, record completions, analyse progress through different statistics, and store all information persistently using a SQLite database.

The project was designed with a layered architecture to separate user interaction, business logic, persistence, and analytical functionality.

---

## 2. Functional Requirements

The application provides the following functionality:

- Create daily and weekly habits
- Delete habits
- Store habits persistently
- Record habit completions
- Prevent duplicate completions within the same period
- Display all tracked habits
- Filter habits by periodicity
- Calculate the current streak
- Calculate the longest streak
- Identify the habit with the longest streak
- Display a monthly completion history
- Provide an interactive command-line interface

---

## 3. Architecture

The application follows a layered software architecture.

```

User

↓

Command-Line Interface

↓

Service Layer

↓

Repository

↓

SQLite Database

```

Each layer has a clearly defined responsibility.

The user interface handles interaction with the user.

The service layer coordinates application logic.

The repository manages database access.

SQLite provides persistent storage.

Analytical calculations are implemented independently from the persistence layer.

---

## 4. Software Components

### models.py

Defines the Habit domain model and the Periodicity enumeration.

Responsibilities:

- represent a habit
- validate input
- store completion timestamps

---

### database.py

Implements the repository responsible for all SQLite interactions.

Responsibilities:

- create database tables
- insert habits
- retrieve habits
- record completions
- delete habits

---

### services.py

Coordinates operations between the command-line interface and the repository.

Responsibilities:

- create habits
- retrieve habits
- complete habits
- delete habits

---

### analytics.py

Contains pure analytical functions.

Responsibilities:

- filter habits
- calculate current streaks
- calculate longest streaks
- identify the habit with the longest streak
- generate completion statistics

---

### cli.py

Implements the command-line interface.

Responsibilities:

- display menus
- receive user input
- present statistics
- display monthly completion history

---

## 5. Database Design

The application stores information in two relational tables.

### habits

| Column | Description |
|---------|-------------|
| id | Primary key |
| name | Habit name |
| description | Habit description |
| periodicity | Daily or weekly |
| created_at | Creation timestamp |

### completions

| Column | Description |
|---------|-------------|
| id | Primary key |
| habit_id | Foreign key |
| completed_at | Completion timestamp |
| period_key | Daily or weekly period identifier |

The relationship between both tables is one-to-many.

One habit can have many completion records.

---

## 6. Design Decisions

Several architectural decisions were made to improve maintainability and readability.

### Repository Pattern

Database operations are isolated inside the repository.

This separates persistence from application logic and makes future database changes easier.

### Service Layer

The service layer separates business logic from user interaction.

The command-line interface never communicates directly with the database.

### Functional Analytics

Analytical calculations are implemented as pure functions.

These functions receive habits as input and return calculated values without modifying application state.

This demonstrates functional programming concepts.

### SQLite

SQLite was selected because it is lightweight, requires no external server, and is fully integrated into Python.

### Enumerations

Habit periodicity is represented by an enumeration (`Periodicity`) instead of plain strings.

This reduces invalid input and improves type safety.

---

## 7. Completion Rules

The application allows only one completion within the relevant tracking period.

Daily habits:

- one completion per calendar day

Weekly habits:

- one completion per ISO calendar week

The database enforces this rule using a unique constraint on `(habit_id, period_key)`.

---

## 8. Analytics

The application provides several analytical functions.

Current functionality includes:

- list all habits
- filter daily habits
- filter weekly habits
- calculate the current streak
- calculate the longest streak
- identify the habit with the longest streak
- display a monthly completion calendar

The analytical functions are implemented independently of the database and user interface.

---

## 9. Testing

The project uses **pytest** for automated testing.

The test suite verifies:

- domain model validation
- database persistence
- service layer behaviour
- analytical calculations
- command-line helper functions

The final implementation contains **34 automated tests**, all of which pass successfully.

---

## 10. Future Improvements

Possible future extensions include:

- coloured terminal output
- editable habits
- reminder notifications
- CSV export
- graphical user interface
- cloud synchronisation
- multiple user accounts

---

## 11. Learning Outcomes

During this project I gained practical experience in:

- object-oriented software development
- functional programming
- layered software architecture
- SQLite database design
- automated testing with pytest
- debugging and refactoring
- command-line application development
- separation of concerns
- repository and service design patterns

## Reflection

Developing this application demonstrated that building software extends beyond writing code. Designing clear interfaces between components, separating responsibilities, and validating functionality through automated tests proved just as important as implementing individual features.

Throughout the project, the architecture evolved incrementally. New functionality—such as current streak calculations, monthly completion history, and improved analytics—could be integrated with minimal changes to existing code because of the layered design. This highlighted the practical benefits of modular software engineering principles.

Overall, the project strengthened both my understanding of object-oriented programming and my appreciation for functional programming as a complementary approach for implementing analytical operations.