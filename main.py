import pyodbc
import tkinter as tk
from tkinter import messagebox, ttk
# Set up the database connection
conn = pyodbc.connect(
    'DRIVER={PostgreSQL};'
    'SERVER=localhost;'
    'DATABASE=ecocraft;'
    'UID=postgres;'
    'PWD=lolo;'
)
cursor = conn.cursor()


# Fetch available UserIDs from Users table
def fetch_user_ids():
    cursor.execute("SELECT UserID FROM Users ORDER BY UserID")
    return [row[0] for row in cursor.fetchall()]

# Fetch next available CraftID
def get_next_craft_id():
    cursor.execute("SELECT COALESCE(MAX(CraftID), 0) + 1 FROM Craft")
    return cursor.fetchone()[0]


# Define function for inserting a craft
def insert_craft():
    try:
        craft_id = get_next_craft_id()
        user_id = user_id_var.get()
        craft_name = insert_name_entry.get()
        difficulty_level = difficulty_var.get()

        # Validate estimated time input
        try:
            estimated_time = int(insert_time_entry.get())
            # Validate time is within reasonable range
            if estimated_time <= 0 or estimated_time > 180:  # max 3 hours
                messagebox.showerror("Error", "Estimated time must be between 1 and 180 minutes!")
                return
        except ValueError:
            messagebox.showerror("Error", "Estimated time must be a number!")
            return

        age_range = insert_age_entry.get()
        # Validate age range format
        if not (age_range.count('-') == 1 and all(part.strip().isdigit() for part in age_range.split('-'))):
            messagebox.showerror("Error", "Age range must be in format 'X-Y' (e.g., '5-10')")
            return

        # Validate required fields
        if not all([user_id, craft_name, difficulty_level, estimated_time, age_range]):
            messagebox.showerror("Error", "All fields are required!")
            return

        cursor.execute("""
            INSERT INTO Craft (CraftID, UserID, CraftName, DifficultyLevel, EstimatedTime, AgeRange)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (craft_id, user_id, craft_name, difficulty_level, estimated_time, age_range))
        conn.commit()
        messagebox.showinfo("Success", f"Craft idea '{craft_name}' inserted successfully with ID {craft_id}!")

        # Clear the form
        insert_name_entry.delete(0, tk.END)
        difficulty_var.set('')  # Clear difficulty selection
        insert_time_entry.delete(0, tk.END)
        insert_age_entry.delete(0, tk.END)
        user_id_var.set('')

    except pyodbc.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error inserting craft: {str(e)}")


# Tkinter GUI setup
root = tk.Tk()
root.title("Craft Ideas Database Operations")
root.geometry("400x500")

# Main frame with padding
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Title
title_label = tk.Label(main_frame, text="Add New Craft", font=('Arial', 14, 'bold'))
title_label.pack(pady=(0, 20))

# Create a frame for the form with proper spacing
form_frame = tk.Frame(main_frame)
form_frame.pack(fill=tk.X)

# UserID selection
tk.Label(form_frame, text="User ID:").pack(anchor='w')
user_id_var = tk.StringVar()
user_id_dropdown = ttk.Combobox(form_frame, textvariable=user_id_var, state='readonly')
user_id_dropdown['values'] = fetch_user_ids()
user_id_dropdown.pack(fill=tk.X, pady=(0, 10))

# Craft Name input
tk.Label(form_frame, text="Craft Name:").pack(anchor='w')
insert_name_entry = tk.Entry(form_frame)
insert_name_entry.pack(fill=tk.X, pady=(0, 10))

# Difficulty Level input with predefined values
tk.Label(form_frame, text="Difficulty Level:").pack(anchor='w')
difficulty_var = tk.StringVar()
difficulty_dropdown = ttk.Combobox(form_frame, textvariable=difficulty_var, state='readonly')
difficulty_dropdown['values'] = ['Easy', 'Medium', 'Hard']
difficulty_dropdown.pack(fill=tk.X, pady=(0, 10))

# Estimated Time input
tk.Label(form_frame, text="Estimated Time (minutes):").pack(anchor='w')
insert_time_entry = tk.Entry(form_frame)
insert_time_entry.pack(fill=tk.X, pady=(0, 10))

# Age Range input
tk.Label(form_frame, text="Age Range (e.g., 5-10):").pack(anchor='w')
insert_age_entry = tk.Entry(form_frame)
insert_age_entry.pack(fill=tk.X, pady=(0, 10))

# Info label for age range format
age_info = tk.Label(form_frame, text="Format: minimum-maximum (e.g., 5-10)", font=('Arial', 8), fg='gray')
age_info.pack(anchor='w', pady=(0, 10))

# Insert button
insert_button = tk.Button(
    form_frame,
    text="Add Craft",
    command=insert_craft,
    bg='#4CAF50',
    fg='white',
    font=('Arial', 10, 'bold'),
    padx=20,
    pady=5
)
insert_button.pack(pady=20)

root.mainloop()

# Close the connection when done
conn.close()