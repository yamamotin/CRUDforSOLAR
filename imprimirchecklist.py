import csv

def printExcel():
  try:

    # Connect to database
    conn=sql.connect('database.db')

  # Export data into CSV file
    print("Exporting data into CSV............")
    cursor = conn.cursor()
    cursor.execute("select * from User where monitorando = False")
    with open("checklist.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter="\t")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)

    dirpath = os.getcwd() + "/employee_data.csv"
    print("Data exported Successfully into {}".format(dirpath))

  except Error as e:
    print(e)

  # Close database connection
  finally:
    conn.close()
