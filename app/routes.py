from flask import Blueprint, render_template, request, redirect
import psycopg2
import os
from app.forms import AppointmentForm

bp = Blueprint('main', __name__)

CONNECTION_PARAMETERS = {
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "dbname": os.environ.get("DB_NAME"),
    "host": os.environ.get("DB_HOST"),
}

@bp.route('/', methods=['GET', 'POST'])
def main():
    form = AppointmentForm()
    if form.validate_on_submit():
        req = dict(request.form)
        req['start_datetime'] = req['start_date'] +" " + req['start_time']
        req['end_datetime'] = req['end_date'] + " " + req['end_time']
        if not "private" in req:
            req["private"] = False
        with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
            with conn.cursor() as curs:
                curs.execute('''INSERT INTO appointments (name, start_datetime, end_datetime, description, private)
                                values (%(name)s, %(start_datetime)s, %(end_datetime)s, %(description)s, %(private)s);''', req)
        return redirect("/")       

    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor() as curs:
            curs.execute('''SELECT id, name, start_datetime, end_datetime
                            FROM appointments
                            ORDER BY start_datetime;''')
            result = curs.fetchall()
    

    return render_template('main.html', rows=result, form=form)

    
