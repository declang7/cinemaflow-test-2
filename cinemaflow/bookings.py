from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .extensions import db
from .models import Show, Booking, Hall

bookings_bp = Blueprint('bookings', __name__, template_folder='templates', url_prefix='/bookings')

@bookings_bp.route('/<int:show_id>/seats', methods=['GET', 'POST'])
@login_required
def select_seats(show_id):
    show = Show.query.get_or_404(show_id)
    if request.method == 'POST':
        seat_numbers = request.form.getlist('seats')
        if not seat_numbers:
            flash('Please select at least one seat.')
            return redirect(request.url)
        # Check if seats are available
        for seat in seat_numbers:
            existing = Booking.query.filter_by(show_id=show_id, seat_number=seat).first()
            if existing:
                flash(f'Seat {seat} is already booked.')
                return redirect(request.url)
        # Create bookings
        for seat in seat_numbers:
            booking = Booking(user_id=current_user.id, show_id=show_id, seat_number=seat)
            db.session.add(booking)
        db.session.commit()
        flash('Booking successful!')
        return redirect(url_for('movies.list_movies'))
    # Determine booked seats
    booked_seats = [b.seat_number for b in Booking.query.filter_by(show_id=show_id).all()]
    hall = Hall.query.get(show.hall_id)
    seats = range(1, hall.capacity + 1)
    return render_template('bookings/seats.html', show=show, seats=seats, booked_seats=booked_seats)

@bookings_bp.route('/')
@login_required
def list_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('bookings/list.html', bookings=bookings)
