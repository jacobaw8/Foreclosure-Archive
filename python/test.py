import mysql.connector
from mysql.connector import errorcode
import csv


try:
  mydb = mysql.connector.connect(
    host="Please stop",
    user="Searching for",
    password="My database",
    database="information"
    )
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = mydb.cursor()
  with open('archiver.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    count = 0
    for row in csv_reader:
      if(count == 0):
        count = 1
        continue
      #print(str(row[5]) + "test")
      query = "INSERT INTO foreclosure_listing" "(date_of_sale, case_num, county, address, phone, trailer, link)" "VALUES (%s, %s, %s, %s, %s, %s, %s)"
      vals = (str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]))
      cursor.execute(query, vals)
  mydb.commit()
  mydb.close()
