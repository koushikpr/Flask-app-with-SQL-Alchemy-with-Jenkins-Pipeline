from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, render_template

db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    year_of_release = db.Column(db.Integer, nullable=False)
    user_ratings = db.Column(db.Float)

    # Relationships
    genres = db.relationship('Genre', secondary='movie_genre')
    actors = db.relationship('Actor', secondary='movie_actor')
    technicians = db.relationship('Technician', secondary='movie_technician')

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class Technician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

# Association tables
movie_genre = db.Table('movie_genre',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)

movie_actor = db.Table('movie_actor',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'))
)

movie_technician = db.Table('movie_technician',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('technician_id', db.Integer, db.ForeignKey('technician.id'))
)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_database.db'
db.init_app(app)


# Routing

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


# GET ALL Movies
@app.route('/movies', methods=['GET'])
def get_all_movies():
    # Implement pagination and filters as needed
    movies = Movie.query.all()
    # Convert the movies to a JSON format or customize as needed
    return jsonify(movies)



# GET and POST Specific Movie
@app.route('/movies/<int:movie_id>', methods=['GET', 'POST'])
def get_update_movie(movie_id):
    if request.method == 'GET':
        movie = Movie.query.get_or_404(movie_id)
        # Convert the movie to a JSON format or customize as needed
        return jsonify(movie)
    elif request.method == 'POST':
        movie = Movie.query.get_or_404(movie_id)

        # Parse the JSON data from the request
        data = request.json

        # Update the movie attributes
        movie.name = data.get('name', movie.name)
        movie.year_of_release = data.get('year_of_release', movie.year_of_release)
        movie.user_ratings = data.get('user_ratings', movie.user_ratings)

        # Update relationships
        if 'genres' in data:
            movie.genres = [Genre.query.get_or_404(genre_id) for genre_id in data['genres']]

        if 'actors' in data:
            movie.actors = [Actor.query.get_or_404(actor_id) for actor_id in data['actors']]

        if 'technicians' in data:
            movie.technicians = [Technician.query.get_or_404(tech_id) for tech_id in data['technicians']]

        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': 'Movie updated successfully'})
        # Implement logic to update the movie

        # ...


# DELETE a specific movie
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'Movie deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    # for production use 
    # app.run(host='0.0.0.0')