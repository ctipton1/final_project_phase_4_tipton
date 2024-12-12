from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
import plotly.figure_factory as ff
from datetime import timedelta

tractor_maintenance = Blueprint('tractor_maintenance', __name__)

@tractor_maintenance.route('/maintenance', methods=['GET', 'POST'])
def manage_maintenance():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        tractor_id = request.form['tractor_id']
        description = request.form['description']
        date = request.form['date']
        status = request.form['status']

        cursor.execute(
            'INSERT INTO maintenance (tractor_id, description, date, status) VALUES (%s, %s, %s, %s)',
            (tractor_id, description, date, status)
        )
        db.commit()
        flash('Maintenance record added successfully!', 'success')
        return redirect(url_for('tractor_maintenance.manage_maintenance'))

    # Fetch maintenance records and tractor info
    cursor.execute('SELECT m.*, t.model FROM maintenance m JOIN tractors t ON m.tractor_id = t.tractor_id')
    maintenance_records = cursor.fetchall()

    # Fetch available tractors for the dropdown
    cursor.execute('SELECT tractor_id, model, brand FROM tractors')
    tractors = cursor.fetchall()

    # Prepare Gantt chart data
    gantt_data = []
    for record in maintenance_records:
        start_date = record['date']  # Already a datetime.date object
        end_date = start_date + timedelta(days=1)  # Adjust end date for visibility
        gantt_data.append({
            'Task': f"{record['model']} ({record['description']})",
            'Start': start_date.strftime('%Y-%m-%d'),
            'Finish': end_date.strftime('%Y-%m-%d'),
            'Resource': record['status']
        })

    # Add fallback trace if no data exists
    if not gantt_data:
        gantt_data.append({
            'Task': 'No Data',
            'Start': '2024-01-01',
            'Finish': '2024-01-01',
            'Resource': 'No Data'
        })

    # Create Gantt chart
    gantt_fig = ff.create_gantt(
        gantt_data,
        index_col='Resource',
        show_colorbar=True,
        group_tasks=True,
        showgrid_x=True,
        showgrid_y=True,
        bar_width=0.3,
        height=600,
        title='Maintenance Timeline'
    )

    # Add hover information
    for task in gantt_fig['data']:
        task['hoverinfo'] = 'x+text'
        task['text'] = [f"{t['Task']} - {t['Resource']}" for t in gantt_data]

    # Optionally set a date range
    gantt_fig.update_xaxes(
        range=['2024-01-01', '2024-12-31']
    )

    timeline_div = gantt_fig.to_html(full_html=False)

    return render_template('tractor_maintenance.html', maintenance_records=maintenance_records, tractors=tractors, timeline_div=timeline_div)


@tractor_maintenance.route('/delete_maintenance/<int:maintenance_id>', methods=['POST'])
def delete_maintenance(maintenance_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM maintenance WHERE maintenance_id = %s', (maintenance_id,))
    db.commit()
    flash('Maintenance record deleted!', 'danger')
    return redirect(url_for('tractor_maintenance.manage_maintenance'))


@tractor_maintenance.route('/update_maintenance/<int:maintenance_id>', methods=['GET', 'POST'])
def update_maintenance(maintenance_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        tractor_id = request.form['tractor_id']
        description = request.form['description']
        date = request.form['date']
        status = request.form['status']

        cursor.execute(
            '''
            UPDATE maintenance
            SET tractor_id = %s, description = %s, date = %s, status = %s
            WHERE maintenance_id = %s
            ''',
            (tractor_id, description, date, status, maintenance_id)
        )
        db.commit()
        flash('Maintenance record updated successfully!', 'success')
        return redirect(url_for('tractor_maintenance.manage_maintenance'))

    # Fetch the current maintenance record
    cursor.execute(
        'SELECT * FROM maintenance WHERE maintenance_id = %s',
        (maintenance_id,)
    )
    maintenance_record = cursor.fetchone()

    # Fetch available tractors for the dropdown
    cursor.execute('SELECT tractor_id, model, brand FROM tractors')
    tractors = cursor.fetchall()

    return render_template(
        'edit_maintenance.html',
        maintenance_record=maintenance_record,
        tractors=tractors
    )
