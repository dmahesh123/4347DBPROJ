import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk

# Set up the MySQL database connection
conn = mysql.connector.connect(
    host="localhost",    # Use "localhost" if running on the same machine
    user="root",         # MySQL username (CHANGE THIS)
    password="apple",  # MySQL password (CHANGE THIS)
    database="project"   # Database name (CHANGE THIS)
)
cursor = conn.cursor()

# Fetch available UserIDs from Users table
def fetch_user_ids():
    cursor.execute("SELECT UserID FROM Users ORDER BY UserID") # SQL statement
    return [row[0] for row in cursor.fetchall()]

# Fetch available CraftIDs
def fetch_craft_ids():
    cursor.execute("SELECT CraftID FROM Craft ORDER BY CraftID") # SQL statement
    craft_ids = [row[0] for row in cursor.fetchall()]
    # print("Craft IDs:", craft_ids)  # Debugging output
    return craft_ids

# fetch available craft names
def fetch_craft_names():
    cursor.execute("SELECT CraftName FROM Craft ORDER BY CraftID") # SQL statement
    craft_names = [row[0] for row in cursor.fetchall()]
    # print("Craft IDs:", craft_ids)  # Debugging output
    return craft_names

# Fetch next available CraftID
def get_next_craft_id():
    cursor.execute("SELECT COALESCE(MAX(CraftID), 0) + 1 FROM Craft") # SQL statement
    return cursor.fetchone()[0]

# insert a new craft
def insert_craft_db(craft_id, user_id, craft_name, difficulty_level, estimated_time, age_range):
    try:
        cursor.execute("""
            INSERT INTO Craft (CraftID, UserID, CraftName, DifficultyLevel, EstimatedTime, AgeRange)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (craft_id, user_id, craft_name, difficulty_level, estimated_time, age_range))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise Exception(f"Error inserting craft: {str(e)}")


# delete a craft by name
def delete_craft_db(craft_name):
    try:
        cursor.execute("DELETE FROM Craft WHERE CraftName = %s", (craft_name,))
        conn.commit()
        return cursor.rowcount  # Return the number of rows affected by the deletion
    except mysql.connector.Error as e:
        conn.rollback()
        raise Exception(f"Error deleting craft: {str(e)}") 


# Define function for updating a craft
def update_craft_db(craft_name, difficulty_level, estimated_time, age_range):
    try:
        cursor.execute("""
            UPDATE Craft
            SET DifficultyLevel = %s, EstimatedTime = %s, AgeRange = %s
            WHERE CraftName = %s
        """, (difficulty_level, estimated_time, age_range, craft_name))
        conn.commit()
        return cursor.rowcount  # return number of rows affected by the update
    except mysql.connector.Error as e:
        conn.rollback()
        raise Exception(f"Error updating craft: {str(e)}")  

def close_connection():
    conn.close()