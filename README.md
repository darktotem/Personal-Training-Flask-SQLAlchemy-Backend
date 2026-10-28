# Workout Tracker API

A backend REST API for a workout tracking app used by personal trainers. Trainers can create workouts, create reusable exercises, and add exercises to workouts with reps, sets and duration. Built with Flask, SQLAlchemy and Marshmallow.

## Features

- Create, view and delete workouts and exercises
- Add an exercise to a workout with reps, sets and/or duration
- Validation at three layers: database table constraints, model validations and Marshmallow schema validations
- Deleting a workout or exercise also removes its linked workout-exercise rows
- Seed script with example data and a pytest test suite

## Data model

- **Exercise**: `id`, `name`, `category`, `equipment_needed`
- **Workout**: `id`, `date`, `duration_minutes`, `notes`
- **WorkoutExercise** (join table): `id`, `workout_id`, `exercise_id`, `reps`, `sets`, `duration_seconds`

A workout has many exercises through WorkoutExercise, and an exercise has many workouts through WorkoutExercise.

## Installation

Requires Python 3 and [Pipenv](https://pipenv.pypa.io).

```bash

git clone <your-repo-url>
cd folder name
pipenv install --dev
pipenv shell
cd server
export FLASK_APP=app.py
flask db upgrade head
python seed.py
```

If the `migrations/` folder does not exist yet, create it first:

```bash
flask db init
flask db migrate -m "create exercises, workouts and workout_exercises tables"
flask db upgrade head
```

Running `python seed.py` again resets the data without duplicating it.

## Running the app

From the `server/` folder:

```bash
python app.py
```

The API runs at `http://localhost:5555`. (`flask run --port 5555` also works.)


## Validations

- **Table constraints:** unique exercise names; non-blank name and category; positive duration, reps, sets and duration_seconds; at least one of reps, sets or duration_seconds; an exercise can only be added to a workout once.
- **Model validations:** trimmed non-empty names and categories, lower-cased category, boolean `equipment_needed`, valid date, positive integers for numeric fields.
- **Schema validations:** required fields, length and range checks, strict integer types, blank-value checks, and a rule requiring at least one of reps, sets or duration_seconds.




ngrok =  https://c610-102-211-144-250.ngrok-free.app