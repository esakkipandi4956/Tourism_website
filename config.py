# config.py

class Config:
    SECRET_KEY = 'Esakki1234'

    # MySQL for auth
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Esakki@1976'
    MYSQL_DB = 'signup'
    MYSQL_CURSORCLASS = 'DictCursor'

    # Mail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'esakkipandi7066@gmail.com'
    MAIL_PASSWORD = 'ryfy gkxa cwpg ydnw'

    # Booking DB via PyMySQL
    BOOKING_DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Esakki@1976',
        'database': 'booking'
    }
