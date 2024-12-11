from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

customers = Blueprint('customers', __name__)

@customers.route('/customers', methods=['GET', 'POST'])
def manage_customers():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cursor.execute('INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)', (name, email, phone))
        db.commit()

        flash('Customer added successfully!', 'success')
        return redirect(url_for('customers.manage_customers'))

    cursor.execute('SELECT * FROM customers')
    all_customers = cursor.fetchall()
    return render_template('customers.html', all_customers=all_customers)

@customers.route('/update_customer/<int:customer_id>', methods=['GET', 'POST'])
def update_customer(customer_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cursor.execute('UPDATE customers SET name = %s, email = %s, phone = %s WHERE customer_id = %s', (name, email, phone, customer_id))
        db.commit()

        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customers.manage_customers'))

    cursor.execute('SELECT * FROM customers WHERE customer_id = %s', (customer_id,))
    current_customer = cursor.fetchone()
    return render_template('update_customer.html', current_customer=current_customer)

@customers.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM customers WHERE customer_id = %s', (customer_id,))
    db.commit()

    flash('Customer deleted successfully!', 'danger')
    return redirect(url_for('customers.manage_customers'))
