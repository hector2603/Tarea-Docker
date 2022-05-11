import mysql.connector
import json
from flask import Flask , request

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, Docker!'

@app.route('/people')
def get_people():
  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssw0rd1",
    database="docker"
  )
  cursor = mydb.cursor()


  cursor.execute("SELECT * FROM docker.person")

  row_headers=[x[0] for x in cursor.description] 

  results = cursor.fetchall()
  print(results)
  json_data= []
  for result in results:
    print(result)
    json_data.append(dict(zip(row_headers,result)))

  cursor.close()

  return json.dumps(json_data)

@app.route('/create', methods=['POST'])
def add_person():
  conn = None
  cursor = None
  json_data = request.get_json(force=True)
  _name = json_data['name']
  _lastName = json_data['lastName']
  sql = "INSERT INTO person (name, last_name)VALUES(%s, %s)"
  data = (_name, _lastName,)
  conn = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssw0rd1",
    database="docker"
  )
  cursor = conn.cursor()
  cursor.execute(sql, data)
  conn.commit()
  cursor.close() 
  conn.close()
  return "person created successfully"


@app.route('/update', methods=['POST'])
def update_person():
	conn = None
	cursor = None
	json_data = request.get_json(force=True)
	_name = json_data['name']
	_lastName = json_data['lastName']
	_id = json_data['id']
	sql = "UPDATE person SET name=%s, last_name=%s WHERE id=%s"
	data = (_name, _lastName, _id,)
	conn = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssw0rd1",
    database="docker"
  )
	cursor = conn.cursor()
	cursor.execute(sql, data)
	conn.commit()
	cursor.close() 
	conn.close()
	return "person updated successfully"


@app.route('/initdb')
def db_init():
  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssw0rd1"
  )
  cursor = mydb.cursor()

  cursor.execute("CREATE DATABASE IF NOT EXISTS docker")
  cursor.close()

  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssw0rd1",
    database="docker"
  )
  cursor = mydb.cursor()

  cursor.execute("CREATE TABLE IF NOT EXISTS person (id MEDIUMINT NOT NULL AUTO_INCREMENT ,name VARCHAR(255), last_name VARCHAR(255), PRIMARY KEY (id))")
  mydb.commit()

  cursor.close()
  mydb.close()

  return 'init database'

if __name__ == "__main__":
  app.run(host ='0.0.0.0')