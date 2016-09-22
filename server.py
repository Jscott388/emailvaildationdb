from flask import Flask, render_template, redirect, request, flash, session
import datetime
import time
import re
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app, 'emailsdb')
app.secret_key = 'thissecret'

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/create', methods=['POST'])
def create():

    if EMAIL_REGEX.match(request.form['email']):
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {
                'email': request.form['email']
        }

        mysql.query_db(query,data)
    else:
        flash("Invalid Email", 'error')
        return redirect ('/')
    return redirect('/success')


@app.route('/success', methods=['GET'])
def success():
    if (request.method == 'GET'):
        query = "SELECT id, email, created_at FROM emails"
        emails = mysql.query_db(query)
        timestamp = datetime.datetime.strftime(emails[0]['created_at'], "%B %d, %Y - %I:%M %p ")
        emailID = emails[0]['id']
        email = emails[0]['email']
        data = {'email': email, 'time': timestamp, 'ID': emailID}

        print data
    return render_template('success.html', all_emails=data)

app.run(debug=True)
