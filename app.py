from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Use a strong key in production

users = {}  # key = email, value = password (plain text for now)

# Optional: login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    if 'user_email' in session:
        return render_template('index.html', user=session['user_email'])
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users:
            flash("User already exists!", "danger")
        else:
            users[email] = password
            flash("Signup successful. Please log in.", "success")
            return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['user_email'] = email
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))


@app.route('/search', methods=['POST'])
def search():
    city = request.form['city']
    checkin = request.form['checkin']
    checkout = request.form['checkout']
    guests = request.form['guests']

    hotels = [
        {
            'name': 'Grand Palace Hotel',
            'price': 35000,
            'location': city,
            'image': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8aG90ZWx8ZW58MHx8MHx8fDA%3D',
            'rating': 4.5
        },
        {
            'name': 'Sunset Resort',
            'price': 50000,
            'location': city,
            'image': 'https://images.unsplash.com/photo-1586611292717-f828b167408c?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDZ8fGhvdGVsfGVufDB8fDB8fHww',
            'rating': 4.2
        },
        {
            'name': 'Palm Paradise',
            'price': 55000,
            'location': city,
            'image': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGhvdGVsfGVufDB8fDB8fHww',
            'rating': 4.0
        },
        {
            'name': 'Oasis Residence',
            'price': 40000,
            'location': city,
            'image': 'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzB8fGhvdGVsfGVufDB8fDB8fHww',
            'rating': 4.4
        },
        {
            'name': 'Residence Retreat',
            'price': 48000,
            'location': city,
            'image': 'https://images.unsplash.com/photo-1631049552057-403cdb8f0658?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTU0fHxob3RlbHxlbnwwfHwwfHx8MA%3D%3D',
            'rating': 4.5
        },
        {
            'name': 'Riviera Retreat',
            'price': 30000,
            'location': city,
            'image': 'https://images.unsplash.com/photo-1623812058330-ccfa078cffb3?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDI2fHxob3RlbHxlbnwwfHwwfHx8MA%3D%3D',
            'rating': 4.0
        },
        {
            'name': 'Palette Paradise',
            'price': 50000,
            'location': city,
            'image': 'https://images.unsplash.com/photo-1615460549969-36fa19521a4f?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Njh8fGhvdGVsfGVufDB8fDB8fHww',
            'rating': 4.2
        },
        {
            'name': 'DreamyDestiny Suites',
            'price': 50000,
            'location': city,
            'image': 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGhvdGVsfGVufDB8fDB8fHww',
            'rating': 4.5
        },
        {
            'name': 'Budget Inn',
            'price': 80000,
            'location': city,
            'image': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGhvdGVsfGVufDB8fDB8fHww',
            'rating': 3.9
        }
    ]

    return render_template('results.html', city=city, checkin=checkin, checkout=checkout, guests=guests, hotels=hotels)


@app.route('/book', methods=['POST'])
def book():
    hotel_name = request.form['hotel_name']
    price = request.form['price']
    city = request.form['city']
    checkin = request.form['checkin']
    checkout = request.form['checkout']
    guests = request.form['guests']

    rooms = [
        {
            'type': 'Single Room',
            'image': 'https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aG90ZWx8ZW58MHx8MHx8fDA%3D',
            'beds': 1,
            'price': int(price),
            'amenities': ['Free Wi-Fi', 'AC', 'TV']
        },
        {
            'type': 'Double Room',
            'image': 'https://plus.unsplash.com/premium_photo-1670360414903-19e5832f8bc4?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjF8fGRvdWJsZSUyMHJvb218ZW58MHx8MHx8fDA%3D',
            'beds': 2,
            'price': int(price) + 30,
            'amenities': ['Free Wi-Fi', 'AC', 'TV', 'Mini Fridge']
        },
        {
            'type': 'Deluxe Suite',
            'image': 'https://images.unsplash.com/photo-1729605411476-defbdab14c54?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGRlbHV4ZSUyMHJvb218ZW58MHx8MHx8fDA%3D',
            'beds': 2,
            'price': int(price) + 60,
            'amenities': ['Free Wi-Fi', 'AC', 'TV', 'Mini Bar', 'Jacuzzi']
        }
    ]

    return render_template('room_details.html', hotel_name=hotel_name, city=city,
                           checkin=checkin, checkout=checkout, guests=guests, rooms=rooms)


@app.route('/confirm', methods=['POST'])
def confirm():
    hotel_name = request.form['hotel_name']
    room_type = request.form['room_type']
    room_price = request.form['room_price']
    city = request.form['city']
    checkin = request.form['checkin']
    checkout = request.form['checkout']
    guests = request.form['guests']

    return render_template('confirm.html', hotel_name=hotel_name, room_type=room_type,
                           room_price=room_price, city=city, checkin=checkin,
                           checkout=checkout, guests=guests)



@app.route('/payment', methods=['POST'])
def payment():
    booking_details = request.form
    return render_template('payment.html', **booking_details)


@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    # This would be triggered after "payment"
    booking_details = request.form
    return render_template('confirm.html', **booking_details)



if __name__ == '__main__':
    app.run(debug=True)