import pyodbc
import tkinter as tk
from tkinter import messagebox, ttk

# Set up the database connection
conn = pyodbc.connect(
    'DRIVER={ADD YOUR DRIVER HERE};'
    'SERVER=ADD YOUR SERVER HERE;'
    'DATABASE=ADD THE NAME OF YOUR DB;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()


# Fetch available UserIDs from Users table
def fetch_user_ids():
    cursor.execute("SELECT UserID FROM Users")
    return [row.UserID for row in cursor.fetchall()]


# Define function for inserting a craft
def insert_craft():
    user_id = user_id_var.get()
    craft_name = insert_name_entry.get()
    difficulty_level = insert_difficulty_entry.get()
    estimated_time = int(insert_time_entry.get())
    age_range = insert_age_entry.get()

    cursor.execute("""
        INSERT INTO Craft (UserID, CraftName, DifficultyLevel, EstimatedTime, AgeRange)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, craft_name, difficulty_level, estimated_time, age_range))
    conn.commit()
    messagebox.showinfo("Insert", "Craft idea inserted successfully!")


# Tkinter GUI setup
root = tk.Tk()
root.title("Craft Ideas Database Operations")
root.geometry("400x400")

# Insert Section
insert_frame = tk.Frame(root, padx=10, pady=10)
insert_frame.pack(pady=5)

tk.Label(insert_frame, text="Insert Craft Idea").grid(row=0, column=0, columnspan=2)


# CraftID selection
tk.Label(insert_frame, text="Craft ID:").grid(row=1, column=0)
craft_id_var = tk.StringVar()
craft_id_drop = ttk.Combobox(insert_frame, textvariable=craft_id_var)
craft_id_drop['values'] = fetch_user_ids()
craft_id_drop.grid(row=1, column=1)

# UserID selection
tk.Label(insert_frame, text="User ID:").grid(row=2, column=0)
user_id_var = tk.StringVar()
user_id_dropdown = ttk.Combobox(insert_frame, textvariable=user_id_var)
user_id_dropdown['values'] = fetch_user_ids()
user_id_dropdown.grid(row=2, column=1)

# Craft Name input
tk.Label(insert_frame, text="Craft Name:").grid(row=3, column=0)
insert_name_entry = tk.Entry(insert_frame)
insert_name_entry.grid(row=3, column=1)

# Difficulty Level input
tk.Label(insert_frame, text="Difficulty Level:").grid(row=4, column=0)
insert_difficulty_entry = tk.Entry(insert_frame)
insert_difficulty_entry.grid(row=4, column=1)

# Estimated Time input
tk.Label(insert_frame, text="Estimated Time (mins):").grid(row=5, column=0)
insert_time_entry = tk.Entry(insert_frame)
insert_time_entry.grid(row=5, column=1)

# Age Range input
tk.Label(insert_frame, text="Age Range:").grid(row=6, column=0)
insert_age_entry = tk.Entry(insert_frame)
insert_age_entry.grid(row=6, column=1)

# Insert button
insert_button = tk.Button(insert_frame, text="Insert", command=insert_craft)
insert_button.grid(row=7, column=0, columnspan=2)

root.mainloop()

# Close the connection when done
conn.close()
