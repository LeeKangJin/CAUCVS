import sqlite3
conn = sqlite3.connect('SmartMicrowave.db')
cur = conn.cursor()
cur.execute('create table CVSFood (FoodCategory, TargetTemperature, OperationTime700, OperationTime1000)')
values = [('tri kimbap', '70', '30', '20'), ('kimbap', '70', '30', '20'),
          ('lunch box', '70', '130', '110'), ('hamburger', '70', '40', '30'), ('hotbar', '70', '30', '20')]
cur.executemany('insert into CVSFood values(?,?,?,?)', values)
conn.commit()
conn.close()


