from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import mysql.connector
from config import DATABASE_CONFIG
import razorpay
import pymysql
import os
import cups

app = Flask(__name__)
app.secret_key = "supersecretkey"


# MySQL Connection
def get_db_connection():
    return mysql.connector.connect(**DATABASE_CONFIG)
#---------------------------------------------
def print_file(file_path):
    conn = cups.Connection()
    printers = conn.getPrinters()
    printer_name = list(printers.keys())[0]  # Select the first printer
    conn.printFile(printer_name, file_path, "Smart Printer Job", {})
    print(f"Sent {file_path} to printer {printer_name}")

from flask import send_file

@app.route('/print/<file_name>', methods=['GET'])
def print_document(file_name):
    file_path = f"./uploads/{file_name}"
    try:
        print_file(file_path)
        return f"Print job sent for {file_name}"
    except Exception as e:
        return f"Error printing file: {str(e)}"
#------------------------------------------------
# Import Configurations
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        if user_id == "RA2311003050355" and password == "Srm@ist":
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin.html')

@app.route('/calculate_price', methods=['POST'])
def calculate_price():
    data = request.json
    copies = int(data['copies'])
    color = data['color']
    price_per_copy = 10 if color == "color" else 5
    total_price = copies * price_per_copy
    return jsonify({"total_price": total_price})

@app.route('/make_payment', methods=['POST'])
def make_payment():
    data = request.json
    amount = int(data['amount']) * 100
    payment_order = razorpay_client.order.create(dict(amount=amount, currency="INR", payment_capture='1'))
    return jsonify({"order_id": payment_order['id']})

@app.route('/print', methods=['POST'])
def trigger_print():
    data = request.json
    file_paths = data['file_paths']
    for file in file_paths:
        os.system(f"lp {file}")
    return jsonify({"status": "success", "message": "Printing started"})

#if __name__ == '__main__':
  #  app.run(debug=True)
