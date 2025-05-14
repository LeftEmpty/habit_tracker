# Habit Tracker
> Developed as a university portfolio project for IU, Python Object-Oriented and Functional Programming (OOFP) module.

A Python-based Habit Tracking App built using basic `Python`, `sqlite3`, `Tkinter`.

Final Grade: *@tbd*

<br>

## 📋 Table of Contents

- [📌 Summary](#summary)
- [🚀 Basic Usage](#basic-usage)
- [✨ Features](#features)
- [🛠️ Installation Guide](#installation-guide)
- [🐞 Known Issues](#known-issues)

<br>

## 📌 Summary

This application allows users to create, subscribe to, and manage habits.
Habits can be tracked daily, weekly, or on specific days.
Each habit is linked to user-specific progress, and optionally shared publicly.

<br>

## 🚀 Basic Usage

0. Launch the application [(installation)](#installation-guide).
1. Log in or register a user.
2. Create habits, or subscribe to one in the public list.
3. Mark habits as completed.
4. Edit habits as necessary.
5. View statistics and track streaks & progress over time.

### Demonstration

> @TODO - video demonstration

<br>

## ✨ Features

- Structured GUI using `Tkinter` incl. screen base class & popup widgets.
- Split habit data and habit subscription structure.
  - Easily support public habits.
  - Deletion / Editing rules apply appropriately.
- Habit creation, deletion, editing.
- Track completion with streaks
- Customizable periodicity (daily, weekly, specific weekdays)
- Multi-user support
- Data persistence via SQLite3
- Database logger
- Test unit
- Package Manager `Poetry` [(poetry docs)](https://python-poetry.org/docs/basic-usage/)

<br>

## 🛠️ Installation Guide

> If you have any problems installing or running this program, please message me via my student email or Teams, so I can help.

<details>
<summary><strong>Linux</strong></summary>

### Linux Installation

1. Clone the repo:

    ```bash
    git clone https://github.com/your-repo/habit-tracker.git
    cd habit-tracker
    ```

2. Install requirements via `Poetry`

    ```bash
    poetry install
    ```

3. Launch the app

    ```bash
    poetry run python run.py
    ```

- If you have trouble with poetry or don't want to use it:
  - Currently the project only has 2 dependencies:
    - `Python >3.10`
    - `Tkinter`
  - Install these with your package manager
    - example (Arch-based):

    ```bash
    sudo pacman -S python, tk
    ```

  - Then just launch the app using:

    ```bash
    python run.py
    ```

</details>

<details>
<summary><strong>Windows</strong></summary>

### Windows Installation

1. Clone the repo:

    ```bash
    git clone https://github.com/your-repo/habit-tracker.git
    cd habit-tracker
    ```

2. Step 3 should be optional on Windows, due to `Tkinter` being included in every python installation. <br>
(If Python was installed via the binaries on their website)

3. (Install requirements via `Poetry`)

    ```bash
    poetry install
    ```

4. Launch the app
    - using poetry (enables virtual environment)

    ```bash
    poetry run python run.py
    ```

    - default python launch

    ```bash
    python run.py
    ```

</details>

<br>

## 🐞 Known Issues

> List of currently known issues / bugs. These are low priority problems that may or may not be fixed after phase 2 depending on tutor feedback.

- Editing `Periodicity` on habits via the `EditHabitPopup` doesn't apply
  - easy fix, but haven't gotten around to it yet.
- GUI is not very responsive to different screen / window sizes.
