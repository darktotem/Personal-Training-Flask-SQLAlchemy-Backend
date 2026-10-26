from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise


#  model validations

def test_exercise_blank_name_rejected():
    with pytest.raises(ValueError):
        Exercise(name='  ', category='core')


def test_exercise_category_is_lowercased():
    assert Exercise(name='Plank', category='CORE').category == 'core'


def test_workout_negative_duration_rejected():
    with pytest.raises(ValueError):
        Workout(date=date.today(), duration_minutes=-5)


def test_workout_exercise_zero_reps_rejected():
    with pytest.raises(ValueError):
        WorkoutExercise(workout_id=1, exercise_id=1, reps=0)


# table constraints

def test_unique_exercise_name_constraint():
    db.session.add(Exercise(name='Squat', category='strength'))
    db.session.commit()
    db.session.add(Exercise(name='Squat', category='strength'))
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()


def test_workout_exercise_needs_a_measurement_constraint(sample):
    wo, ex = sample
    db.session.add(WorkoutExercise(workout_id=wo.id, exercise_id=ex.id))
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()


# relationships

def test_workout_has_many_exercises_through_workout_exercises(sample):
    wo, ex = sample
    db.session.add(WorkoutExercise(workout_id=wo.id, exercise_id=ex.id, reps=5))
    db.session.commit()
    assert wo.exercises == [ex]
    assert ex.workouts == [wo]