from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

rental_records = Blueprint('rental_records', __name__)

@rental_records.route('/rental_records', methods=['GET', 'POST'])
def manage_rentals():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        tractor_id = request.form['tractor_id']
        customer_id = request.form['customer_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        cursor.execute('INSERT INTO rental_records (tractor_id, customer_id, start_date, end_date) VALUES (%s, %s, %s, %s)',
                       (tractor_id, customer_id, start_date, end_date))
        db.commit()

        flash('Rental record added successfully!', 'success')
        return redirect(url_for('rental_records.manage_rentals'))

    cursor.execute('SELECT * FROM rental_records')
    all_rentals = cursor.fetchall()
    return render_template('rental_records.html', all_rentals=all_rentals)

@rental_records.route('/update_rental/<int:rental_id>', methods=['GET', 'POST'])
def update_rental(rental_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        tractor_id = request.form['tractor_id']
        customer_id = request.form['customer_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        cursor.execute('UPDATE rental_records SET tractor_id = %s, customer_id = %s, start_date = %s, end_date = %s WHERE rental_id = %s',
                       (tractor_id, customer_id, start_date, end_date, rental_id))
        db.commit()

        flash('Rental record updated successfully!', 'success')
        return redirect(url_for('rental_records.manage_rentals'))

    cursor.execute('SELECT * FROM rental_records WHERE rental_id = %s', (rental_id,))
    current_rental = cursor.fetchone()
    return render_template('update_rental.html', current_rental=current_rental)

@rental_records.route('/delete_rental/<int:rental_id>', methods=['POST'])
def delete_rental(rental_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM rental_records WHERE rental_id = %s', (rental_id,))
    db.commit()

    flash('Rental record deleted successfully!', 'danger')
    return redirect(url_for('rental_records.manage_rentals'))
