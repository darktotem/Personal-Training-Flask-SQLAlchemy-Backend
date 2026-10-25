from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Define Models here
class Exercise(db.Model):
    __tablename__ = 'exercises'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)


    # Table constraints
    __table_args__ = (
        CheckConstraint('length(trim(name)) > 0', name='ck_exercise_name_not_blank'),
        CheckConstraint('length(trim(category)) > 0', name='ck_exercise_category_not_blank'),
    )

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise',
        cascade='all, delete-orphan')
    workouts = db.relationship(
        'Workout', secondary='workout_exercises', back_populates='exercises',
        viewonly=True)