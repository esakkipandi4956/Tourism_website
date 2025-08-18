from flask import Blueprint, render_template, request, redirect, url_for, session
from db import mysql  # ✅ Safe import

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        print(f"[DEBUG] Email: {email}, Password: {password}")

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        print(f"[DEBUG] DB Result: {user}")
        cur.close()

        if user:
            session['email'] = email
            return redirect(url_for('index'))
        else:
            print("[DEBUG] Invalid credentials shown")
            return render_template('signin.html', error="Invalid credentials")

    return render_template('signin.html')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s OR email=%s", (username, email))
        existing = cur.fetchone()
        if existing:
            message = "Username or email already exists"
        else:
            cur.execute("INSERT INTO users(username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            mysql.connection.commit()
            cur.close()
            session['email'] = email
            return redirect(url_for('index'))
        cur.close()
    return render_template('signup.html', message=message)

@auth_bp.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))
