from flask import Blueprint, request, render_template, jsonify, current_app as app
import pymysql
from datetime import datetime
from mailer.send_mail import send_cab_confirmation_email

cab_bp = Blueprint('cab_bp', __name__)

# Price per km based on cab type
price_per_km = {
    "Mini": 10,
    "Sedan": 14,
    "SUV": 18
}

@cab_bp.route('/cab-booking', methods=['GET', 'POST'])
def cab_booking():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        cab_type = request.form.get('cab_type')
        pickup = request.form.get('pickup')
        drop = request.form.get('drop')
        distance = request.form.get('distance')  # e.g. "12.5 km"
        price = request.form.get('price').replace('₹', '')  # Remove rupee symbol if exists

        # Database insert
        conn = pymysql.connect(**app.config['CAB_DB_CONFIG'])
        cursor = conn.cursor()
        query = '''
            INSERT INTO cab_bookings (name, email, phone, cab_type, pickup, drop_location, distance, price, booking_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = (name, email, phone, cab_type, pickup, drop, distance, price, datetime.now())
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

        # Send confirmation email (and optionally SMS)
        send_cab_confirmation_email(email, name, cab_type, pickup, drop, distance, price)

        return jsonify({"status": "success", "message": "Cab booked successfully!"})

    return render_template('cab_booking.html')


@cab_bp.route('/admin/cab-requests')
def view_cab_requests():
    conn = pymysql.connect(**app.config['CAB_DB_CONFIG'])
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM cab_bookings ORDER BY booking_time DESC")
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin/cab_requests.html', bookings=bookings)
