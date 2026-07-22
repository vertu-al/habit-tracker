# Habit Tracker – Technical Concept

## 1. Project Objective

The purpose of this project is to develop a command-line habit tracking
application in Python. The system allows users to create daily and weekly
habits, record completions, persist data between sessions, and analyse habit
streaks.

## 2. Architecture

The application follows a layered architecture consisting of:

- a command-line interface,
- a service layer,
- a repository layer,
- a domain model,
- and a functional analytics module.

## 3. Components

### Habit

The Habit class represents an individual habit. It stores its name,
description, periodicity, creation timestamp, and completion timestamps.

### HabitService

The HabitService coordinates user actions such as creating, deleting, and
completing habits.

### HabitRepository

The HabitRepository is responsible for storing and retrieving habit data
using an SQLite database.

### Analytics Module

The analytics module provides pure functions for filtering habits and
calculating streaks.

## 4. Data Storage

The application uses SQLite with separate tables for habits and completion
records. One habit can have multiple completion records.

## 5. User Interaction

Users interact with the application through a command-line menu. The CLI
forwards requests to the service layer, which uses the repository to access
persistent data.

## 6. Design Rationale

The separation of responsibilities makes the application easier to test,
maintain, and extend. Object-oriented programming is used for the domain,
service, and persistence components, while functional programming is used
for the analytics module.
