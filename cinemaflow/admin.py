from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from datetime import datetime

from .extensions import db
from .models import Movie, Hall, Show, Booking

admin_bp = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin')

# Helper to ensure only managers or admins can access admin routes
def require_manager():
    if not current_user.is_authenticated or current_user.role not in ('manager', 'admin'):
        abort(403)

@admin_bp.route('/movies/new', methods=['GET', 'POST'])
@login_required
def create_movie():
    require_manager()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if not title:
            flash('Title is required.')
        else:
            movie = Movie(title=title, description=description)
            db.session.add(movie)
            db.session.commit()
            flash('Movie created successfully.')
            return redirect(url_for('movies.list_movies'))
    return render_template('admin/create_movie.html')

@admin_bp.route('/shows/new', methods=['GET', 'POST'])
@login_required
def create_show():
    require_manager()
    movies = Movie.query.all()
    halls = Hall.query.all()
    if request.method == 'POST':
        movie_id = request.form.get('movie_id')
        hall_id = request.form.get('hall_id')
        show_time_str = request.form.get('show_time')
        try:
            show_time = datetime.strptime(show_time_str, '%Y-%m-%d %H:%M')
        except (TypeError, ValueError):
            flash('Invalid show time format.')
            return redirect(request.url)
        show = Show(movie_id=movie_id, hall_id=hall_id, show_time=show_time)
        db.session.add(show)
        db.session.commit()
        flash('Show scheduled successfully.')
        return redirect(url_for('movies.list_movies'))
    return render_template('admin/create_show.html', movies=movies, halls=halls)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    require_manager()
    total_bookings = Booking.query.count()
    return render_template('admin/dashboard.html', total_bookings=total_bookings)
