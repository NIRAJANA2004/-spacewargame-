# database.py
import mysql.connector

def insert_player_name(player_name):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="HELLOWORLD",
            database="space_war"
        )
        cursor = connection.cursor()
        query = "INSERT INTO users (player_name) VALUES (%s)"
        cursor.execute(query, (player_name,))
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
