import sqlite3
from flask import Flask, render_template, g

# Path to the already created database
PATH = 'db/jobs.sqlite'

app = Flask(__name__)

# Global database connection
def open_connection():
    connection = getattr(g, '_connection', None)
    if connection == None:
        connection = g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
    return connection

# Query database function
def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection
    # Query database function results
    cursor = connection.execute(sql, values)
    if commit == True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results

# Close the connection decorator
@app.teardown_appcontext
# Close the connection
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()

@app.route('/')
@app.route('/jobs')
def jobs():
    return render_template('index.html')
