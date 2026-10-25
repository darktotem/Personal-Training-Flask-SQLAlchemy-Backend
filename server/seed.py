
#!/usr/bin/env python3

from datetime import date, timedelta

from app import app
from models import *

with app.app_context():

    print('Clearing existing data...')
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print('Seeding exercises...')
    exercises = [
        Exercise(name='Push-up', category='strength', equipment_needed=False),
        Exercise(name='Squat', category='strength', equipment_needed=False),
        Exercise(name='Bench Press', category='strength', equipment_needed=True),
        Exercise(name='Deadlift', category='strength', equipment_needed=True),
        Exercise(name='Plank', category='core', equipment_needed=False),
        Exercise(name='Running', category='cardio', equipment_needed=False),
        Exercise(name='Jump Rope', category='cardio', equipment_needed=True),
        Exercise(name='Hamstring Stretch', category='flexibility', equipment_needed=False),
    ]
    db.session.add_all(exercises)
    db.session.commit()
    pushup, squat, bench, deadlift, plank, running, rope, stretch = exercises

    print('Seeding workouts...')
    today = date.today()
    workouts = [
        Workout(date=today - timedelta(days=4), duration_minutes=60,
                notes='Upper body focus. Felt strong.'),
        Workout(date=today - timedelta(days=2), duration_minutes=45,
                notes='Cardio and core.'),
        Workout(date=today, duration_minutes=75,
                notes='Full body session with mobility finisher.'),
    ]
    db.session.add_all(workouts)
    db.session.commit()
    w1, w2, w3 = workouts

    print('Linking exercises to workouts...')
    links = [
        WorkoutExercise(workout_id=w1.id, exercise_id=bench.id, reps=8, sets=4),
        WorkoutExercise(workout_id=w1.id, exercise_id=pushup.id, reps=20, sets=3),
        WorkoutExercise(workout_id=w1.id, exercise_id=plank.id, sets=3, duration_seconds=60),
        WorkoutExercise(workout_id=w2.id, exercise_id=running.id, duration_seconds=1200),
        WorkoutExercise(workout_id=w2.id, exercise_id=rope.id, sets=5, duration_seconds=90),
        WorkoutExercise(workout_id=w2.id, exercise_id=plank.id, sets=4, duration_seconds=45),
        WorkoutExercise(workout_id=w3.id, exercise_id=squat.id, reps=10, sets=4),
        WorkoutExercise(workout_id=w3.id, exercise_id=deadlift.id, reps=5, sets=5),
        WorkoutExercise(workout_id=w3.id, exercise_id=stretch.id, sets=2, duration_seconds=30),
    ]
    db.session.add_all(links)
    db.session.commit()

    print('Done seeding!')