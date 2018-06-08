import sqlite3
conn = sqlite3.connect('SmartMicrowave.db')
cur = conn.cursor()
cur.execute('create table CVSFood (FoodCategory, TargetTemperature, OperationTime700, OperationTime1000)')
values = [('tri kimbap', '38', '30', '20'), ('kimbap', '38', '30', '20'),
          ('lunch box', '45', '130', '110'), ('hamburger', '43', '40', '30'), ('hotbar', '55', '30', '20')]
cur.executemany('insert into CVSFood values(?,?,?,?)', values)
conn.commit()
conn.close()


