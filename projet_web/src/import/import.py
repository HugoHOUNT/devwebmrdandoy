import csv
import mysql.connector


link = mysql.connector.connect(
    host='mysql',
    database='rna',
    user='root',
    password=""

)


cur = link.cursor()
with open('./data/rna1.csv', 'r', encoding='ISO-8859-1') as f:
    reader=csv.reader(f, delimiter=';')
    next(reader) 
    for row in reader:
        print(row[0])
        cur.execute(
            "INSERT INTO data (rna_id, rna_id_ex, gestion) VALUES (%s, %s, %s)",
            (row[0], row[1], row[3])
        )
        link.commit()
link.close()        