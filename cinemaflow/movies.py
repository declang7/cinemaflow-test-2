from flask import Blueprint, render_template
from .models import Movie

movies_bp = Blueprint('movies', __name__, template_folder='templates', url_prefix='/movies')

@movies_bp.route('/')
def list_movies():
    movies = Movie.query.all()
    return render_template('movies/list.html', movies=movies)
