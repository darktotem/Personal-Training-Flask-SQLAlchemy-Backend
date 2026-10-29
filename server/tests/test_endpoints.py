from models import WorkoutExercise


# workouts

def test_get_workouts(client, sample):
    r = client.get('/workouts')
    assert r.status_code == 200
    assert len(r.get_json()) == 1


def test_get_workout_not_found(client):
    assert client.get('/workouts/999').status_code == 404


def test_create_workout(client):
    r = client.post('/workouts', json={'date': '2026-10-27', 'duration_minutes': 30})
    assert r.status_code == 201
    assert r.get_json()['duration_minutes'] == 30


def test_create_workout_invalid_duration(client):
    r = client.post('/workouts', json={'date': '2026-10-27', 'duration_minutes': -5})
    assert r.status_code == 400
    assert 'duration_minutes' in r.get_json()['errors']


def test_create_workout_missing_date(client):
    assert client.post('/workouts', json={'duration_minutes': 30}).status_code == 400


def test_workout_detail_includes_reps_sets_duration(client, sample):
    wo, ex = sample
    client.post(f'/workouts/{wo.id}/exercises/{ex.id}/workout_exercises',
                json={'reps': 10, 'sets': 3})
    data = client.get(f'/workouts/{wo.id}').get_json()
    we = data['workout_exercises'][0]
    assert we['reps'] == 10 and we['sets'] == 3
    assert we['exercise']['name'] == 'Squat'


def test_delete_workout_removes_workout_exercises(client, sample):
    wo, ex = sample
    client.post(f'/workouts/{wo.id}/exercises/{ex.id}/workout_exercises',
                json={'reps': 5})
    assert client.delete(f'/workouts/{wo.id}').status_code == 204
    assert client.get(f'/workouts/{wo.id}').status_code == 404
    assert WorkoutExercise.query.count() == 0


# ----------------------------------------------------------------- exercises

def test_create_exercise_and_duplicate(client):
    body = {'name': 'Lunge', 'category': 'Strength'}
    assert client.post('/exercises', json=body).status_code == 201
    assert client.post('/exercises', json=body).status_code == 400


def test_create_exercise_blank_name(client):
    r = client.post('/exercises', json={'name': ' ', 'category': 'core'})
    assert r.status_code == 400


def test_exercise_detail_includes_workouts(client, sample):
    wo, ex = sample
    client.post(f'/workouts/{wo.id}/exercises/{ex.id}/workout_exercises',
                json={'sets': 3})
    data = client.get(f'/exercises/{ex.id}').get_json()
    assert data['workout_exercises'][0]['workout']['id'] == wo.id


def test_delete_exercise_removes_workout_exercises(client, sample):
    wo, ex = sample
    client.post(f'/workouts/{wo.id}/exercises/{ex.id}/workout_exercises',
                json={'reps': 5})
    assert client.delete(f'/exercises/{ex.id}').status_code == 204
    assert WorkoutExercise.query.count() == 0
    assert client.delete(f'/exercises/{ex.id}').status_code == 404


# add to a workout

def test_add_exercise_to_workout(client, sample):
    wo, ex = sample
    url = f'/workouts/{wo.id}/exercises/{ex.id}/workout_exercises'
    assert client.post(url, json={'reps': 10, 'sets': 3}).status_code == 201
    assert client.post(url, json={'reps': 5}).status_code == 400  # duplicate pair


def test_add_exercise_requires_measurement(client, sample):
    wo, ex = sample
    r = client.post(f'/workouts/{wo.id}/exercises/{ex.id}/workout_exercises', json={})
    assert r.status_code == 400


def test_add_exercise_unknown_ids(client, sample):
    wo, _ = sample
    assert client.post(f'/workouts/{wo.id}/exercises/999/workout_exercises',
                       json={'reps': 5}).status_code == 404
    assert client.post('/workouts/999/exercises/1/workout_exercises',
                       json={'reps': 5}).status_code == 404