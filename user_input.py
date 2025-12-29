import mysql.connector

def insert_player():
    name = input("Enter your player name: ")

    try:
        connection = mysql.connector.connect(
            host="localhost",      
            user="root",            # your MySQL username
            password="HELLOWORLD",  # your MySQL password
            database="space_war"
        )

        cursor = connection.cursor()

        query = "INSERT INTO users (player_name) VALUES (%s)"
        cursor.execute(query, (name,))
        connection.commit()

        print(f"Welcome {name}! Your name has been saved.")
        return cursor.lastrowid  

    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    insert_player()
