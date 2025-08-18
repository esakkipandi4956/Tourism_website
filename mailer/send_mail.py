from flask import current_app
from flask_mail import Message

# 🧳 Tourism Booking Email
def send_confirmation_email(name, email, destination, travel_date, offer, people, total_amount, payment_url):
    try:
        mail = current_app.extensions['mail']
        body = f"""
Hi {name},

Thank you for booking your trip to {destination}!

📅 Travel Date: {travel_date}
🎁 Offer: {offer}
👥 Number of People: {people}
💰 Total Amount: ₹{total_amount}

👉 Complete your payment here: {payment_url}

We look forward to making your journey memorable!

Warm regards,  
🌍 Travel Team
"""
        msg = Message(subject="✅ Booking Confirmation",
                      sender=current_app.config['MAIL_USERNAME'],
                      recipients=[email],
                      body=body)
        mail.send(msg)
    except Exception as e:
        print("Email error:", e)

# 🚕 Cab Booking Email
def send_cab_confirmation_email(to_email, name, pickup, drop, cab_type, distance, fare):
    try:
        mail = current_app.extensions['mail']
        body = f"""
Hi {name},

✅ Your cab has been successfully booked!

📍 Pickup Location: {pickup}
🏁 Drop Location: {drop}
🚖 Cab Type: {cab_type}
📏 Estimated Distance: {distance} km
💸 Estimated Fare: ₹{fare}

Thanks for choosing our cab service. Have a safe and pleasant journey!

Best regards,  
🚖 Tourism Cab Booking Team
"""
        msg = Message(subject="🚕 Cab Booking Confirmation",
                      sender=current_app.config['MAIL_USERNAME'],
                      recipients=[to_email],
                      body=body)
        mail.send(msg)
        print(f"Confirmation email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
