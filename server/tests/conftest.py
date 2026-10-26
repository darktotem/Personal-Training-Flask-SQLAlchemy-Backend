import os
os.environ['DATABASE_URI'] = 'sqlite:///:memory:'

from datetime import date

import pytest

from app import app
from models import db, Exercise, Workout


@pytest.fixture(autouse=True)
def setup_db():
    app.config['TESTING'] = True
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield
        db.session.remove()


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def sample():
    ex = Exercise(name='Squat', category='strength', equipment_needed=False)
    wo = Workout(date=date(2026, 10, 26), duration_minutes=45, notes='Legs')
    db.session.add_all([ex, wo])
    db.session.commit()
    return wo, ex