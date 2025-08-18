from flask import Blueprint, request, jsonify, render_template, current_app as app
import pymysql
from datetime import datetime
from urllib.parse import quote
from mailer.send_mail import send_confirmation_email

booking_bp = Blueprint('booking_bp', __name__)

# Destination-wise pricing
price_map = {
    "Goa Beach Resort": 3500,
    "Ooty Hill Stay": 3000,
    "Jaipur Heritage Tour": 3200,
    "Kerala Houseboat Stay": 4000,
    "Darjeeling Himalayan Railway": 2800,
    "Andaman Island Escape": 4500,
    "Rajasthan Desert Safari": 3400,
    "Udaipur Lake Palace": 5000,
    "Manali Adventure Trip": 3900,
    "Veermata Jijabai Bhosale Zoo, Mumbai": 150,
    "National Zoological Park, New Delhi": 120,
    "Nehru Zoological Park, Hyderabad": 100,
    "Subramanya Swami Temple, Tiruchendur": 1500,
    "Tirupati Venkateswara Temple, Tirupati": 1800,
    "Khajuraho Temples, Madhya Pradesh": 2000,
    "Coutrallam": 1600,
    "Hogenakkal": 1800,
    "Shivanasamudra": 2000,
    "Anamudi": 3000,
    "Kangchenjunga": 4500,
    "Baba Budan giri": 3200,
    "Taj Mahal": 2700,
    "India Gate": 2500,
    "Charminar": 2400,
    "Goa Beach": 3000,
    "Varakala": 2800,
    "Andaman and Nicobar Beach": 5000,
    "Kanyakumari Sunrise Experience": 2800
}

# Function to get database connection
def get_booking_connection():
    cfg = app.config['BOOKING_DB_CONFIG']
    return pymysql.connect(
        host=cfg['host'],
        user=cfg['user'],
        password=cfg['password'],
        database=cfg['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


@booking_bp.route('/submit-booking', methods=['POST'])
def submit_booking():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    travel_date = datetime.strptime(data.get('date'), "%Y-%m-%d").date()
    destination = data.get('destination')
    offer = data.get('offer')
    people = int(data.get('people', 1))

    # Price Calculation
    price = price_map.get(destination, 3000)
    total = price * people

    try:
        conn = get_booking_connection()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO booking (name, email, travel_date, destination, offer, people, amount)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, email, travel_date, destination, offer, people, total))
            conn.commit()
        conn.close()
    except Exception as e:
        print("DB Error:", e)
        return jsonify({'error': 'Booking failed. Please try again.'}), 500

    # Payment URL
    payment_url = f"http://localhost:5000/payment?name={quote(name)}&amount={total}"

    send_confirmation_email(name, email, destination, travel_date, offer, people, total, payment_url)

    return jsonify({'message': 'Booking confirmed!', 'payment_url': payment_url})

@booking_bp.route("/payment")
def payment():
    return render_template("payment.html")

@booking_bp.route("/payment-success", methods=["POST"])
def payment_success():
    return "<h3 style='text-align:center; margin-top: 50px;'>✅ Payment Successful! Thank you for booking with us.</h3>"
