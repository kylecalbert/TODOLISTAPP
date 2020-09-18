import json

from flask import Flask, render_template, request, redirect, url_for, jsonify

from flask_mysqldb import MySQL
import requests
import secrets

app = Flask(__name__)
app.config['MYSQL_USER'] =secrets.MYSQL_USER
app.config['MYSQL_PASSWORD'] = secrets.MYSQL_PASSWORD
app.config['MYSQL_HOST'] = secrets.MYSQL_HOST
app.config['MYSQL_DB'] = secrets.MYSQL_DB
MYSQL_CURSORCLASS = 'DictCursor' #returns data as dictionary


mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks_table")
    tasks_table = cur.fetchall()
    #line below used to create table
    #cur.execute('''CREATE TABLE tasks_table(id Integer PRIMARY KEY AUTO_INCREMENT, text VARCHAR(100),complete BOOLEAN)''')
    return render_template('base.html',tasks_table =tasks_table)



@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get('title')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks_table (text,complete) VALUES(%s,%s)", [title,False])
    mysql.connection.commit()
    print(title)
    return redirect(url_for("index"))


@app.route("/delete/<id>")
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks_table where id ="+id)
    mysql.connection.commit()
    return redirect(url_for("index"))

@app.route("/update/<id>")
def update(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks_table SET complete = %s where id = "+id, [True])
    mysql.connection.commit()
    return redirect(url_for("index"))







if __name__ == '__main__':
    app.run(debug=True)

