from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

tractors = Blueprint('tractors', __name__)

@tractors.route('/tractors', methods=['GET', 'POST'])
def manage_tractors():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        model = request.form['model']
        brand = request.form['brand']
        type = request.form['type']
        availability = request.form['availability']

        cursor.execute('INSERT INTO tractors (model, brand, type, availability) VALUES (%s, %s, %s, %s)',
                       (model, brand, type, availability))
        db.commit()

        flash('Tractor added successfully!', 'success')
        return redirect(url_for('tractors.manage_tractors'))

    cursor.execute('SELECT * FROM tractors')
    all_tractors = cursor.fetchall()
    return render_template('tractors.html', all_tractors=all_tractors)

@tractors.route('/update_tractor/<int:tractor_id>', methods=['GET', 'POST'])
def update_tractor(tractor_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        model = request.form['model']
        brand = request.form['brand']
        type = request.form['type']
        availability = request.form['availability']

        cursor.execute('UPDATE tractors SET model = %s, brand = %s, type = %s, availability = %s WHERE tractor_id = %s',
                       (model, brand, type, availability, tractor_id))
        db.commit()

        flash('Tractor updated successfully!', 'success')
        return redirect(url_for('tractors.manage_tractors'))

    cursor.execute('SELECT * FROM tractors WHERE tractor_id = %s', (tractor_id,))
    current_tractor = cursor.fetchone()
    return render_template('update_tractor.html', current_tractor=current_tractor)

@tractors.route('/delete_tractor/<int:tractor_id>', methods=['POST'])
def delete_tractor(tractor_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM tractors WHERE tractor_id = %s', (tractor_id,))
    db.commit()

    flash('Tractor deleted successfully!', 'danger')
    return redirect(url_for('tractors.manage_tractors'))
