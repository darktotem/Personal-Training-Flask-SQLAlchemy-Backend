from flask import Flask, jsonify, make_response
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
    return make_response({}, 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    return make_response({}, 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    return make_response({}, 201)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    return make_response('', 204)


@app.route('/exercises', methods=['GET'])
def get_exercises():
    return make_response({}, 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    return make_response({}, 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    return make_response({}, 201)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    return make_response('', 204)


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
           methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    return make_response({}, 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
