import mysql.connector

def create_database():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS student_food_db")
        print("Database 'student_food_db' created or already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_database()
