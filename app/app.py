from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
# WARNING: replace with a secure random secret key in production
app.secret_key = "Devops-assignment2"

# Dummy data (in-memory)
shows = [
    {"id": 1, "title": "Inception", "time": "7:00 PM", "price": 250},
    {"id": 2, "title": "Interstellar", "time": "9:00 PM", "price": 300},
    {"id": 3, "title": "Oppenheimer", "time": "6:30 PM", "price": 350}
]
bookings = []

@app.route('/')
def home():
    featured = shows[:3]
    return render_template('index.html', featured=featured)

@app.route('/book/<int:show_id>', methods=['GET', 'POST'])
def book(show_id):
    show = next((s for s in shows if s['id'] == show_id), None)
    if not show:
        flash('Show not found', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        seats = request.form.get('seats')
        date = request.form.get('date')

        # simple validation
        if not all([name, email, seats, date]):
            flash('Please fill in all fields', 'danger')
            return redirect(url_for('book', show_id=show_id))

        try:
            seats = int(seats)
            if seats <= 0 or seats > 10:
                raise ValueError
        except ValueError:
            flash('Seats must be a number between 1 and 10', 'danger')
            return redirect(url_for('book', show_id=show_id))

        total = seats * show['price']
        booking_ref = f"BK-{int(datetime.utcnow().timestamp())}"
        booking = {
            "ref": booking_ref,
            "name": name,
            "email": email,
            "show": show['title'],
            "time": show['time'],
            "seats": seats,
            "date": date,
            "total": total
        }
        bookings.append(booking)
        return render_template('confirmation.html', booking=booking)

    return render_template('book.html', show=show)

@app.route('/bookings')
def view_bookings():
    return render_template('bookings.html', bookings=bookings)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/health')
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
