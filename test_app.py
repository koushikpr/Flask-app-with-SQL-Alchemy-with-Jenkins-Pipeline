import json
import pytest
from app import app, db, Movie, Genre, Actor, Technician

# Test configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
client = app.test_client()

# Define test data
movie_data = {
    "name": "Test Movie",
    "year_of_release": 2022,
    "user_ratings": 8.5,
}

genre_data = {
    "name": "Action",
}

actor_data = {
    "name": "John Doe",
}

technician_data = {
    "name": "Jane Smith",
}

@pytest.fixture
def setup_database():
    with app.app_context():
        db.create_all()

        # Create test data
        genre = Genre(**genre_data)
        actor = Actor(**actor_data)
        technician = Technician(**technician_data)
        movie = Movie(**movie_data)

        db.session.add_all([genre, actor, technician, movie])
        db.session.commit()

    yield db

    # Teardown the database after the test
    with app.app_context():
        db.drop_all()

def test_get_all_movies(setup_database):
    response = client.get('/movies')
    assert response.status_code == 200

def test_get_specific_movie(setup_database):
    movie_id = Movie.query.first().id
    response = client.get(f'/movies/{movie_id}')
    assert response.status_code == 200

def test_update_movie(setup_database):
    movie_id = Movie.query.first().id
    update_data = {
        "name": "Updated Movie",
        "year_of_release": 2023,
        "user_ratings": 9.0,
    }
    response = client.post(f'/movies/{movie_id}', json=update_data)
    assert response.status_code == 200

    # Verify the movie has been updated
    updated_movie = Movie.query.get(movie_id)
    assert updated_movie.name == update_data['name']
    assert updated_movie.year_of_release == update_data['year_of_release']
    assert updated_movie.user_ratings == update_data['user_ratings']

def test_delete_movie(setup_database):
    movie_id = Movie.query.first().id
    response = client.delete(f'/movies/{movie_id}')
    assert response.status_code == 200

    # Verify the movie has been deleted
    deleted_movie = Movie.query.get(movie_id)
    assert deleted_movie is None
