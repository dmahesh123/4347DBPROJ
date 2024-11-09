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


# Database functions
# Fetch available UserIDs from Users table
def fetch_user_ids():
    cursor.execute("SELECT UserID FROM Users ORDER BY UserID")
    return [row[0] for row in cursor.fetchall()]

# Fetch available CraftIDs
def fetch_craft_ids():
    cursor.execute("SELECT CraftID FROM Craft ORDER BY CraftID")
    craft_ids = [row[0] for row in cursor.fetchall()]
    print("Craft IDs:", craft_ids)  # Debugging output
    return craft_ids

# Fetch next available CraftID
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

        # use %s as placeholders
        cursor.execute("""
            INSERT INTO Craft (CraftID, UserID, CraftName, DifficultyLevel, EstimatedTime, AgeRange)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (craft_id, user_id, craft_name, difficulty_level, estimated_time, age_range))
        conn.commit()
        messagebox.showinfo("Success", f"Craft idea '{craft_name}' inserted successfully with ID {craft_id}!")

        # Clear the form
        insert_name_entry.delete(0, tk.END)
        difficulty_var.set('')  # Clear difficulty selection
        insert_time_entry.delete(0, tk.END)
        insert_age_entry.delete(0, tk.END)
        user_id_var.set('')

    except mysql.connector.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error inserting craft: {str(e)}")



# Define function for deleting a craft by CraftName
def delete_craft():
    craft_name = delete_name_entry.get()
    if not craft_name:
        messagebox.showerror("Error", "Craft Name is required for deletion!")
        return

    try:
        cursor.execute("DELETE FROM Craft WHERE CraftName = %s", (craft_name,))
        conn.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Success", f"Craft idea '{craft_name}' deleted successfully!")
            delete_name_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Not Found", f"No craft found with name '{craft_name}'.")

    except mysql.connector.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error deleting craft: {str(e)}")


# Define function for updating a craft
def update_craft():
    craft_name = update_name_entry.get()
    difficulty_level = update_difficulty_var.get()
    estimated_time = update_time_entry.get()
    age_range = update_age_entry.get()

    if not craft_name:
        messagebox.showerror("Error", "Craft Name is required for updating!")
        return

    try:
        estimated_time = int(estimated_time)
        if estimated_time <= 0 or estimated_time > 180:
            messagebox.showerror("Error", "Estimated time must be between 1 and 180 minutes!")
            return
    except ValueError:
        messagebox.showerror("Error", "Estimated time must be a number!")
        return

    if not (age_range.count('-') == 1 and all(part.strip().isdigit() for part in age_range.split('-'))):
        messagebox.showerror("Error", "Age range must be in format 'X-Y' (e.g., '5-10')")
        return

    if not all([craft_name, difficulty_level, estimated_time, age_range]):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        cursor.execute("""
            UPDATE Craft
            SET DifficultyLevel = %s, EstimatedTime = %s, AgeRange = %s
            WHERE CraftName = %s
        """, (difficulty_level, estimated_time, age_range, craft_name))
        conn.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", f"Craft '{craft_name}' updated successfully!")
            update_name_entry.delete(0, tk.END)
            update_difficulty_var.set('')
            update_time_entry.delete(0, tk.END)
            update_age_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Not Found", f"No craft found with name '{craft_name}'.")

    except mysql.connector.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error updating craft: {str(e)}")


# Tkinter GUI setup
root = tk.Tk()
root.title("Craft Ideas Database Operations")
root.geometry("400x950")

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
user_id_dropdown = ttk.Combobox(form_frame, textvariable=user_id_var, state='readonly', width=11)
user_id_dropdown['values'] = fetch_user_ids()
user_id_dropdown.pack(anchor='w', pady=(0, 10))

# Craft Name input
tk.Label(form_frame, text="Craft Name:").pack(anchor='w')
insert_name_entry = tk.Entry(form_frame)
insert_name_entry.pack(fill=tk.X, pady=(0, 10))

# Difficulty Level input with predefined values
tk.Label(form_frame, text="Difficulty Level:").pack(anchor='w')
difficulty_var = tk.StringVar()
difficulty_dropdown = ttk.Combobox(form_frame, textvariable=difficulty_var, state='readonly')
difficulty_levels = ['Easy', 'Medium', 'Hard']
difficulty_dropdown['values'] = difficulty_levels
# Calculate width based on the longest item
difficulty_max_length = max(len(item) for item in difficulty_levels)+5
difficulty_dropdown.config(width=difficulty_max_length)
difficulty_dropdown.pack(anchor='w', pady=(0, 10))

# Estimated Time input
tk.Label(form_frame, text="Estimated Time (minutes):").pack(anchor='w')
insert_time_entry = tk.Entry(form_frame, width=14)
insert_time_entry.pack(anchor='w', pady=(0, 10))

# Age Range input
tk.Label(form_frame, text="Age Range (e.g., 5-10):").pack(anchor='w')
insert_age_entry = tk.Entry(form_frame, width=14)
insert_age_entry.pack(anchor='w', pady=(0, 10))

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

# Delete section title and entry below the Add Craft button
delete_label = tk.Label(main_frame, text="Delete Craft", font=('Arial', 14, 'bold'))
delete_label.pack(pady=(20, 10))

# Craft Name label for delete
tk.Label(main_frame, text="Craft Name to Delete:").pack(anchor='w')

# Craft Name input for delete
delete_name_entry = tk.Entry(main_frame)
delete_name_entry.pack(fill=tk.X, pady=(0, 10))

# Delete button
delete_button = tk.Button(
    main_frame,
    text="Delete Craft",
    command=delete_craft,
    bg='#F44336',
    fg='white',
    font=('Arial', 10, 'bold'),
    padx=20,
    pady=5
)
delete_button.pack(pady=10)

# Update section in the GUI
update_label = tk.Label(main_frame, text="Update Craft", font=('Arial', 14, 'bold'))
update_label.pack(pady=(20, 10))

# Craft Name input for update
tk.Label(main_frame, text="Craft Name to Update:").pack(anchor='w')
update_name_entry = tk.Entry(main_frame)
update_name_entry.pack(fill=tk.X, pady=(0, 10))

# Difficulty Level input for update
tk.Label(main_frame, text="New Difficulty Level:").pack(anchor='w')
update_difficulty_var = tk.StringVar()
update_difficulty_dropdown = ttk.Combobox(main_frame, textvariable=update_difficulty_var, state='readonly')
update_difficulty_dropdown['values'] = ['Easy', 'Medium', 'Hard']
update_difficulty_dropdown.pack(fill=tk.X, pady=(0, 10))

# Estimated Time input for update
tk.Label(main_frame, text="New Estimated Time (minutes):").pack(anchor='w')
update_time_entry = tk.Entry(main_frame)
update_time_entry.pack(fill=tk.X, pady=(0, 10))

# Age Range input for update
tk.Label(main_frame, text="New Age Range (e.g., 5-10):").pack(anchor='w')
update_age_entry = tk.Entry(main_frame)
update_age_entry.pack(fill=tk.X, pady=(0, 10))

# Update button
update_button = tk.Button(
    main_frame,
    text="Update Craft",
    command=update_craft,
    bg='#FFA500',
    fg='white',
    font=('Arial', 10, 'bold'),
    padx=20,
    pady=5
)
update_button.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()

# Close the connection when done
conn.close()