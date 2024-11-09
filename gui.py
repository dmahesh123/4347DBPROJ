import tkinter as tk
from tkinter import messagebox, ttk
import db_operations as db

craft_names = db.fetch_craft_names()

# insert craft with input validation
def insert_craft():
    try:
        craft_id = db.get_next_craft_id()  # Get next Craft ID from the database
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

        # Call the insert_craft function from main
        db.insert_craft_db(craft_id, user_id, craft_name, difficulty_level, estimated_time, age_range)
        messagebox.showinfo("Success", f"Craft idea '{craft_name}' inserted successfully with ID {craft_id}!")

        # Clear the form
        insert_name_entry.delete(0, tk.END)
        difficulty_var.set('')  
        insert_time_entry.delete(0, tk.END)
        insert_age_entry.delete(0, tk.END)
        user_id_var.set('')

        update_craft_names()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# delete craft by name with input validation
def delete_craft():
    craft_name = delete_name_var.get()
    if not craft_name:
        messagebox.showerror("Error", "Craft Name is required for deletion!")
        return

    try:
        rows_affected = db.delete_craft_db(craft_name)
        if rows_affected > 0:
            messagebox.showinfo("Success", f"Craft idea '{craft_name}' deleted successfully!")
            delete_name_dropdown.set('') 

            update_craft_names()
        else:
            messagebox.showwarning("Not Found", f"No craft found with name '{craft_name}'.")
    
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Define function for updating a craft
def update_craft():
    craft_name = update_name_var.get()
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
        rows_affected = db.update_craft_db(craft_name, difficulty_level, estimated_time, age_range)
        if rows_affected > 0:
            messagebox.showinfo("Success", f"Craft '{craft_name}' updated successfully!")
            update_name_dropdown.set('')
            update_difficulty_var.set('')
            update_time_entry.delete(0, tk.END)
            update_age_entry.delete(0, tk.END)
            
            update_craft_names()
        else:
            messagebox.showwarning("Not Found", f"No craft found with name '{craft_name}'.")

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def update_craft_names():
    # Fetch updated craft names from the database
    craft_names = db.fetch_craft_names()

    # Clear the existing items in the listbox and combobox
    craft_listbox.delete(0, tk.END)
    delete_name_dropdown['values'] = craft_names
    update_name_dropdown['values'] = craft_names

    # Insert updated craft names into the listbox
    for craft in craft_names:
        craft_listbox.insert(tk.END, craft)

# Tkinter GUI setup
root = tk.Tk()
root.title("Craft Ideas Database Operations")
root.geometry("550x800")

# Main frame with padding
main_frame = tk.Frame(root, padx=0, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a frame for the form with proper spacing
form_frame = tk.Frame(main_frame)
form_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=20)


######## Insert Section 
# Title 
title_label = tk.Label(form_frame, text="Add New Craft", font=('Arial', 14, 'bold'))
title_label.pack(pady=(0,0))

# UserID selection
tk.Label(form_frame, text="User ID:").pack(anchor='w')
user_id_var = tk.StringVar()
user_id_dropdown = ttk.Combobox(form_frame, textvariable=user_id_var, state='readonly', width=10)
user_id_dropdown['values'] = db.fetch_user_ids()
user_id_dropdown.pack(anchor='w', pady=(0, 10))

# Craft Name input
tk.Label(form_frame, text="Craft Name:").pack(anchor='w')
insert_name_entry = tk.Entry(form_frame)
insert_name_entry.pack(fill=tk.X, pady=(0, 10))

# This frame will hold difficulty and estimated time
input_frame1 = tk.Frame(form_frame)
input_frame1.pack(fill=tk.X, pady=(0, 10))

# Difficulty Level input with predefined values
tk.Label(input_frame1, text="Difficulty Level:").grid(row=0, column=0, sticky='w', padx=(0,5))
difficulty_var = tk.StringVar()
difficulty_dropdown = ttk.Combobox(input_frame1, textvariable=difficulty_var, state='readonly', width=11)
difficulty_dropdown['values'] = ['Easy', 'Medium', 'Hard']
difficulty_dropdown.grid(row=1, column=0)

# Estimated Time input
tk.Label(input_frame1, text="Estimated Time (minutes):").grid(row=0, column=1, sticky='w', padx=(35,0))
insert_time_entry = tk.Entry(input_frame1, width=14)
insert_time_entry.grid(row=1, column=1, padx=(5,0))

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
insert_button.pack(pady=5)


######## Delete section title and entry below the Add Craft button
delete_label = tk.Label(form_frame, text="Delete Craft", font=('Arial', 14, 'bold'))
delete_label.pack(pady=(30,0))

# Craft Name label for delete
tk.Label(form_frame, text="Craft Name to Delete:").pack(anchor='w')

# Craft Name input for delete
delete_name_var = tk.StringVar()
delete_name_dropdown = ttk.Combobox(form_frame, textvariable=delete_name_var, state='readonly')
delete_name_dropdown['values'] = craft_names
delete_name_dropdown.pack(fill=tk.X, anchor='w', pady=(0, 10))

# Delete button
delete_button = tk.Button(
    form_frame,
    text="Delete Craft",
    command=delete_craft,
    bg='#F44336',
    fg='white',
    font=('Arial', 10, 'bold'),
    padx=20,
    pady=5
)
delete_button.pack(pady=5)


######## Update section in the GUI
update_label = tk.Label(form_frame, text="Update Craft", font=('Arial', 14, 'bold'))
update_label.pack(pady=(30,0))

# Craft Name input for update
tk.Label(form_frame, text="Craft Name to Update:").pack(anchor='w')
update_name_var = tk.StringVar() 
update_name_dropdown = ttk.Combobox(form_frame, textvariable=update_name_var, state='readonly') 
update_name_dropdown['values'] = craft_names
update_name_dropdown.pack(fill=tk.X, anchor='w', pady=(0, 10)) 

# This frame will hold difficulty and estimated time
update_frame1 = tk.Frame(form_frame)
update_frame1.pack(fill=tk.X, pady=(0, 10))

# Difficulty Level input for update 
tk.Label(update_frame1, text="New Difficulty Level:").grid(row=0, column=0, sticky='w')
update_difficulty_var = tk.StringVar() 
update_difficulty_dropdown = ttk.Combobox(update_frame1, textvariable=update_difficulty_var, state='readonly', width=11) 
update_difficulty_dropdown['values'] = ['Easy', 'Medium', 'Hard'] 
update_difficulty_dropdown.grid(row=1, column=0)

# Estimated Time input for update
tk.Label(update_frame1, text="New Estimated Time (minutes):").grid(row=0, column=1, sticky='w', padx=(20,0))
update_time_entry = tk.Entry(update_frame1, width=14)
update_time_entry.grid(row=1, column=1, sticky='w', padx=(20,0))

# Age Range input for update
tk.Label(form_frame, text="New Age Range (e.g., 5-10):").pack(anchor='w')
update_age_entry = tk.Entry(form_frame, width=11)
update_age_entry.pack(anchor='w', pady=(0, 0))

# Update button
update_button = tk.Button(
    form_frame,
    text="Update Craft",
    command=update_craft,
    bg='#FFA500',
    fg='white',
    font=('Arial', 10, 'bold'),
    padx=20,
    pady=5
)
update_button.pack(pady=5)

# Right frame 
list_frame = tk.Frame(main_frame)
list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)

craft_listbox = tk.Listbox(list_frame, width=30, height=10)
craft_listbox.pack(fill=tk.BOTH, expand=True)
for craft in craft_names:
    craft_listbox.insert(tk.END, craft)

# Function to handle selection
def on_craft_select(event):
    selected_craft = craft_listbox.get(craft_listbox.curselection())
    print(f"Selected craft: {selected_craft}")
    # Add code here to perform an action, like loading craft details

# Bind listbox click to function
craft_listbox.bind("<<ListboxSelect>>", on_craft_select)


# Start the Tkinter main loop
root.mainloop()

# Close the connection when done
db.close_connection()
