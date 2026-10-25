from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates
from marshmallow import Schema, fields, validate, validates as validates_field
from marshmallow import validates_schema, ValidationError
from datetime import date

db = SQLAlchemy()

# Define Models here
class Exercise(db.Model):
    # Exercise entity representing distinct fitness movements.
    __tablename__ = 'exercises'

    __table_args__ = (
        CheckConstraint('length(trim(name)) > 0', name='ck_exercise_name_not_blank'),
        CheckConstraint('length(trim(category)) > 0', name='ck_exercise_category_not_blank'),
    )

    #Primary key for the Exercise model
    id = db.Column(db.Integer, primary_key=True)

    #Attributes for the Exercise model and their constraints
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    #Relationships
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise',
        cascade='all, delete-orphan')
    
    workouts = db.relationship(
        'Workout', secondary='workout_exercises', back_populates='exercises',
        viewonly=True)

    @validates('name')
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Exercise name must be a non-empty string.')
        if len(value) > 100:
            raise ValueError('Exercise name must be 100 characters or fewer.')
        return value.strip()

    @validates('category')
    def validate_category(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Exercise category must be a non-empty string.')
        return value.strip().lower()

    @validates('equipment_needed')
    def validate_equipment(self, key, value):
        if not isinstance(value, bool):
            raise ValueError('equipment_needed must be a boolean.')
        return value
    
    def __repr__(self):
        return f'<Exercise {self.id} {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    #Primary key for the Workout model
    id = db.Column(db.Integer, primary_key=True)

    #Attributes for the Workout model and their constraints
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='ck_workout_duration_positive'),
    )

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout',
        cascade='all, delete-orphan')
    
    exercises = db.relationship(
        'Exercise', secondary='workout_exercises', back_populates='workouts',
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

    #Primary key for the WorkoutExercise model
    id = db.Column(db.Integer, primary_key=True)

    #Attributes for the WorkoutExercise model and their constraints
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

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

    #Schema
class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(load_default=False)

    @validates_field('name')
    def validate_name_not_blank(self, value, **kwargs):
        if not value.strip():
            raise ValidationError('Name cannot be blank.')

    @validates_field('category')
    def validate_category_not_blank(self, value, **kwargs):
        if not value.strip():
            raise ValidationError('Category cannot be blank.')

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(load_default=None, allow_none=True)




class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(load_default=None, allow_none=True)
    sets = fields.Int(load_default=None, allow_none=True)
    duration_seconds = fields.Int(load_default=None, allow_none=True)

    @validates_schema
    def require_a_measurement(self, data, **kwargs):
        if all(data.get(k) is None for k in ('reps', 'sets', 'duration_seconds')):
            raise ValidationError(
                'Provide at least one of reps, sets, or duration_seconds.')


# Output-only schemas with nested data
class WorkoutExerciseDetailSchema(WorkoutExerciseSchema):
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutExerciseForExerciseSchema(WorkoutExerciseSchema):
    workout = fields.Nested(WorkoutSchema, dump_only=True)


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseDetailSchema),
                                    dump_only=True)


class ExerciseDetailSchema(ExerciseSchema):
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseForExerciseSchema),
                                    dump_only=True)
