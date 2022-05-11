import mysql.connector
import json
from flask import Flask

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

  cursor.execute("CREATE TABLE IF NOT EXISTS person (name VARCHAR(255), last_name VARCHAR(255))")
  cursor.execute("INSERT INTO person VALUES ('Hector', 'Ocampo')")
  cursor.execute("INSERT INTO person VALUES ('Andrea', 'Fernandez')")
  cursor.execute("INSERT INTO person VALUES ('Javier', 'Rosero')")
  mydb.commit()

  cursor.close()
  mydb.close()

  return 'init database'

if __name__ == "__main__":
  app.run(host ='0.0.0.0')