import sqlite3

conexion = sqlite3.connect('bd_anuncios.db')

cursor = conexion.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

tablas = cursor.fetchall()

print("TABLAS DE LA BASE DE DATOS:")

for tabla in tablas:
    print(tabla[0])

conexion.close()