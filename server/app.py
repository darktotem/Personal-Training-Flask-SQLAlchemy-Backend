from sqlite3 import IntegrityError

from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()
workout_exercise_schema = WorkoutExerciseSchema()


def error(message, status):
    return make_response(jsonify({'errors': message}), status)

# Define Routes here
@app.route('/workouts', methods=['GET'])
def get_workouts():
   workouts = Workout.query.order_by(Workout.date.desc()).all()
   return make_response(jsonify(workouts_schema.dump(workouts)), 200)

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error('Workout not found.', 404)
    return make_response(jsonify(workout_detail_schema.dump(workout)), 200)

@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.get_json(silent=True) or {})
    except ValidationError as e:
        return error(e.messages, 400)

    try:
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
    except (ValueError, IntegrityError) as e:
        db.session.rollback()
        return error(str(e), 400)

    return make_response(jsonify(workout_schema.dump(workout)), 201)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error('Workout not found.', 404)
    db.session.delete(workout)  # cascades to WorkoutExercises
    db.session.commit()
    return make_response('', 204)


@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.name).all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error('Exercise not found.', 404)
    return make_response(jsonify(exercise_detail_schema.dump(exercise)), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json(silent=True) or {})
    except ValidationError as e:
        return error(e.messages, 400)

    try:
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error('An exercise with that name already exists.', 400)
    except ValueError as e:
        db.session.rollback()
        return error(str(e), 400)

    return make_response(jsonify(exercise_schema.dump(exercise)), 201)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    return make_response('', 204)


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
           methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    return make_response({}, 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
