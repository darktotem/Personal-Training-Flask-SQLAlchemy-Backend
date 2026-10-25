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

    @validates('date')
    def validate_date(self, key, value):
        if not isinstance(value, date):
            raise ValueError('date must be a valid date.')
        return value

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError('duration_minutes must be a positive integer.')
        return value

    def __repr__(self):
        return f'<Workout {self.id} {self.date}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    __table_args__ = (
        CheckConstraint('reps IS NULL OR reps > 0', name='ck_we_reps_positive'),
        CheckConstraint('sets IS NULL OR sets > 0', name='ck_we_sets_positive'),
        CheckConstraint('duration_seconds IS NULL OR duration_seconds > 0',
                        name='ck_we_duration_positive'),
        CheckConstraint(
            'reps IS NOT NULL OR sets IS NOT NULL OR duration_seconds IS NOT NULL',
            name='ck_we_has_measurement'),
        UniqueConstraint('workout_id', 'exercise_id', name='uq_workout_exercise'),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps', 'sets', 'duration_seconds')
    def validate_positive(self, key, value):
        if value is None:
            return value
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError(f'{key} must be a positive integer.')
        return value

    def __repr__(self):
        return f'<WorkoutExercise w={self.workout_id} e={self.exercise_id}>'