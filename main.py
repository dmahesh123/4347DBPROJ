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

# Database functions
def fetch_user_ids():
    cursor.execute("SELECT UserID FROM Users ORDER BY UserID")
    return [row[0] for row in cursor.fetchall()]

def fetch_craft_ids():
    cursor.execute("SELECT CraftID FROM Craft ORDER BY CraftID")
    craft_ids = [row[0] for row in cursor.fetchall()]
    print("Craft IDs:", craft_ids)  # Debugging output
    return craft_ids

def get_next_craft_id():
    cursor.execute("SELECT COALESCE(MAX(CraftID), 0) + 1 FROM Craft")
    return cursor.fetchone()[0]

# Define form actions
def insert_craft():
    try:
        craft_id = get_next_craft_id()
        user_id = user_id_var.get()
        craft_name = insert_name_entry.get()
        difficulty_level = difficulty_var.get()

        # Validate estimated time input
        try:
            estimated_time = int(insert_time_entry.get())
            if estimated_time <= 0 or estimated_time > 180:
                messagebox.showerror("Error", "Estimated time must be between 1 and 180 minutes!")
                return
        except ValueError:
            messagebox.showerror("Error", "Estimated time must be a number!")
            return

        # Validate age range format
        age_range = insert_age_entry.get()
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

def load_craft_data():
    craft_id = craft_id_var.get()
    cursor.execute("SELECT UserID, CraftName, DifficultyLevel, EstimatedTime, AgeRange FROM Craft WHERE CraftID = ?", craft_id)
    result = cursor.fetchone()
    if result:
        user_id_var.set(result[0])
        insert_name_entry.delete(0, tk.END)
        insert_name_entry.insert(0, result[1])
        difficulty_var.set(result[2])
        insert_time_entry.delete(0, tk.END)
        insert_time_entry.insert(0, str(result[3]))
        insert_age_entry.delete(0, tk.END)
        insert_age_entry.insert(0, result[4])

def update_craft():
    try:
        craft_id = craft_id_var.get()
        user_id = user_id_var.get()
        craft_name = insert_name_entry.get()
        difficulty_level = difficulty_var.get()
        
        # Validate estimated time input
        try:
            estimated_time = int(insert_time_entry.get())
            if estimated_time <= 0 or estimated_time > 180:
                messagebox.showerror("Error", "Estimated time must be between 1 and 180 minutes!")
                return
        except ValueError:
            messagebox.showerror("Error", "Estimated time must be a number!")
            return

        # Validate age range format
        age_range = insert_age_entry.get()
        if not (age_range.count('-') == 1 and all(part.strip().isdigit() for part in age_range.split('-'))):
            messagebox.showerror("Error", "Age range must be in format 'X-Y' (e.g., '5-10')")
            return

        if not all([user_id, craft_name, difficulty_level, estimated_time, age_range]):
            messagebox.showerror("Error", "All fields are required!")
            return

        cursor.execute("""
            UPDATE Craft
            SET UserID = ?, CraftName = ?, DifficultyLevel = ?, EstimatedTime = ?, AgeRange = ?
            WHERE CraftID = ?
        """, (user_id, craft_name, difficulty_level, estimated_time, age_range, craft_id))
        conn.commit()
        messagebox.showinfo("Success", f"Craft idea '{craft_name}' updated successfully with ID {craft_id}!")

    except pyodbc.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error updating craft: {str(e)}")

# GUI setup
root = tk.Tk()
root.title("Craft Ideas Database Operations")
root.geometry("400x600")

# Main frame
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Title
title_label = tk.Label(main_frame, text="Add New Craft or Updated An Existing One", font=('Arial', 14, 'bold'))
title_label.pack(pady=(0, 20))

# Form frame
form_frame = tk.Frame(main_frame)
form_frame.pack(fill=tk.X)

# UserID selection
tk.Label(form_frame, text="User ID:").pack(anchor='w')
user_id_var = tk.StringVar()
user_id_dropdown = ttk.Combobox(form_frame, textvariable=user_id_var, state='readonly')
user_id_dropdown['values'] = fetch_user_ids()
user_id_dropdown.pack(fill=tk.X, pady=(0, 10))

# CraftID selection for update
tk.Label(form_frame, text="Select Craft ID to Update:").pack(anchor='w')
craft_id_var = tk.StringVar()
craft_id_dropdown = ttk.Combobox(form_frame, textvariable=craft_id_var, state='readonly')
craft_id_dropdown['values'] = fetch_craft_ids()
craft_id_var.set("Select Craft ID")
print("Dropdown values:", craft_id_dropdown['values'])  # Debugging output
craft_id_dropdown.pack(fill=tk.X, pady=(0, 10))

# Bind the selection event to load the data for the selected Craft ID
craft_id_dropdown.bind("<<ComboboxSelected>>", lambda e: load_craft_data())

# Craft Name input
tk.Label(form_frame, text="Craft Name:").pack(anchor='w')
insert_name_entry = tk.Entry(form_frame)
insert_name_entry.pack(fill=tk.X, pady=(0, 10))

# Difficulty Level input
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

# Info label for age range
age_info = tk.Label(form_frame, text="Format: minimum-maximum (e.g., 5-10)", font=('Arial', 8), fg='gray')
age_info.pack(anchor='w', pady=(0, 10))

# Button frame to place Add and Update buttons side by side
button_frame = tk.Frame(form_frame)
button_frame.pack(pady=20)

# Insert button
insert_button = tk.Button(
    button_frame,
    text="Add Craft",
    command=insert_craft,
    bg='blue',
    fg='white',
    font=('Arial', 10, 'bold'),
    padx=20,
    pady=5
)
insert_button.pack(side=tk.LEFT, padx=10)

# Update button
update_button = tk.Button(
    button_frame,
    text="Update Craft",
    command=update_craft,
    bg='blue',
    fg='white',
    font=('Arial', 10, 'bold'),
    padx=20,
    pady=5
)
update_button.pack(side=tk.LEFT, padx=10)

# Refresh the CraftID dropdown periodically
root.after(100, lambda: craft_id_dropdown.config(values=fetch_craft_ids()))

root.mainloop()

# Close the connection when done
conn.close()
