import pyodbc
import tkinter as tk
from tkinter import messagebox, ttk

# make sure to use your own values in order to set up the connection
conn = pyodbc.connect(
    'DRIVER={YOUR DRIVER HERE};'
    'SERVER=YOUR SERVER HERE;'
    'DATABASE=YOUR DATABASE NAME HERE, our SQL is in EcoCraft.sql;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()


def fetch_user_ids():
    cursor.execute("SELECT UserID, UserName FROM Users ORDER BY UserID")
    users = cursor.fetchall()
    return [(f"{row.UserID} - {row.UserName}", row.UserID) for row in users]


def get_next_craft_id():
    cursor.execute("SELECT ISNULL(MAX(CraftID), 0) + 1 FROM Craft")
    return cursor.fetchone()[0]


def query_crafts_by_difficulty(difficulty):
    try:
        cursor.execute("""
            SELECT CraftName, EstimatedTime, AgeRange, Theme, u.UserName
            FROM Craft c
            JOIN Users u ON c.UserID = u.UserID
            WHERE DifficultyLevel = ?
            ORDER BY CraftName
        """, difficulty)

        crafts = cursor.fetchall()

        result_window = tk.Toplevel(root)
        result_window.title(f"{difficulty} Difficulty Crafts")
        result_window.geometry("600x400")

        tree = ttk.Treeview(result_window, columns=('Craft', 'Time', 'Age', 'Theme', 'Creator'), show='headings')

        tree.heading('Craft', text='Craft Name')
        tree.heading('Time', text='Time (min)')
        tree.heading('Age', text='Age Range')
        tree.heading('Theme', text='Theme')
        tree.heading('Creator', text='Created By')

        scrollbar = ttk.Scrollbar(result_window, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        result_window.grid_rowconfigure(0, weight=1)
        result_window.grid_columnconfigure(0, weight=1)

        for craft in crafts:
            tree.insert('', 'end', values=(craft.CraftName, craft.EstimatedTime,
                                           craft.AgeRange, craft.Theme, craft.UserName))

    except pyodbc.Error as e:
        messagebox.showerror("Database Error", f"Error querying crafts: {str(e)}")


def quit_application():
    if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
        conn.close()
        root.quit()


def insert_craft():
    try:
        craft_id = get_next_craft_id()
        user_id = user_id_dict[user_id_var.get()]
        craft_name = insert_name_entry.get()
        difficulty_level = difficulty_var.get()
        craft_type = craft_type_var.get()
        theme = theme_entry.get()

        try:
            estimated_time = int(insert_time_entry.get())
            if estimated_time <= 0 or estimated_time > 360:  # max is 6 hours min is 0 mins
                messagebox.showerror("Error", "Estimated time must be between 1 and 360 minutes!")
                return
        except ValueError:
            messagebox.showerror("Error", "Estimated time must be a number!")
            return

        age_range = insert_age_entry.get()

        if not (age_range.count('-') == 1 and all(part.strip().isdigit() for part in age_range.split('-'))):
            messagebox.showerror("Error", "Age range must be in format 'X-Y' (e.g., '5-10')")
            return

        if not all([user_id, craft_name, difficulty_level, estimated_time, age_range]):
            messagebox.showerror("Error", "All fields are required!")
            return

        cursor.execute("""
           INSERT INTO Craft (CraftID, UserID, CraftName, DifficultyLevel, EstimatedTime, AgeRange, CraftType, Theme)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
       """, (craft_id, user_id, craft_name, difficulty_level, estimated_time, age_range, craft_type, theme))

        if craft_type == 'Seasonal':
            cursor.execute("INSERT INTO SeasonalCraft (CraftID) VALUES (?)", (craft_id,))
        elif craft_type == 'Decorative':
            cursor.execute("INSERT INTO DecorativeCraft (CraftID) VALUES (?)", (craft_id,))
        elif craft_type == 'Educational':
            cursor.execute("INSERT INTO EducationalCraft (CraftID) VALUES (?)", (craft_id,))

        conn.commit()
        messagebox.showinfo("Success", f"Craft idea '{craft_name}' inserted successfully with ID {craft_id}!")

        clear_form()


    except pyodbc.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error inserting craft: {str(e)}")


def clear_form():
    insert_name_entry.delete(0, tk.END)
    difficulty_var.set('')
    craft_type_var.set('')
    insert_time_entry.delete(0, tk.END)
    insert_age_entry.delete(0, tk.END)
    theme_entry.delete(0, tk.END)
    user_id_var.set('')


def delete_craft():
    craft_name = delete_name_entry.get()
    if not craft_name:
        messagebox.showerror("Error", "Craft Name is required for deletion!")
        return

    try:

        cursor.execute("SELECT CraftID FROM Craft WHERE CraftName = ?", (craft_name,))
        result = cursor.fetchone()

        if result:
            craft_id = result[0]

            cursor.execute("DELETE FROM SeasonalCraft WHERE CraftID = ?", (craft_id,))
            cursor.execute("DELETE FROM DecorativeCraft WHERE CraftID = ?", (craft_id,))
            cursor.execute("DELETE FROM EducationalCraft WHERE CraftID = ?", (craft_id,))

            cursor.execute("DELETE FROM CraftMaterialRelation WHERE CraftID = ?", (craft_id,))
            cursor.execute("DELETE FROM CraftToolRelation WHERE CraftID = ?", (craft_id,))
            cursor.execute("DELETE FROM Instructions WHERE CraftID = ?", (craft_id,))

            cursor.execute("DELETE FROM Craft WHERE CraftID = ?", (craft_id,))

            conn.commit()
            messagebox.showinfo("Success", f"Craft idea '{craft_name}' and all related records deleted successfully!")
            delete_name_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Not Found", f"No craft found with name '{craft_name}'.")


    except pyodbc.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error deleting craft: {str(e)}")


def update_craft():
    craft_name = update_name_entry.get()
    new_difficulty_level = update_difficulty_var.get()
    new_theme = update_theme_entry.get()
    new_estimated_time = update_time_entry.get()
    new_age_range = update_age_entry.get()

    if not craft_name:
        messagebox.showerror("Error", "Craft Name is required for updating!")
        return

    try:
        new_estimated_time = int(new_estimated_time)
        if new_estimated_time <= 0 or new_estimated_time > 180:
            messagebox.showerror("Error", "Estimated time must be between 1 and 180 minutes!")
            return
    except ValueError:
        messagebox.showerror("Error", "Estimated time must be a number!")
        return

    if not (new_age_range.count('-') == 1 and all(part.strip().isdigit() for part in new_age_range.split('-'))):
        messagebox.showerror("Error", "Age range must be in format 'X-Y' (e.g., '5-10')")
        return

    try:

        cursor.execute("""
            UPDATE Craft 
            SET DifficultyLevel = ?, EstimatedTime = ?, AgeRange = ?, Theme = ?
            WHERE CraftName = ?
        """, (new_difficulty_level, new_estimated_time, new_age_range, new_theme, craft_name))

        conn.commit()
        messagebox.showinfo("Success", f"Craft '{craft_name}' updated successfully!")

        update_name_entry.delete(0, tk.END)
        update_difficulty_var.set('')
        update_theme_entry.delete(0, tk.END)
        update_time_entry.delete(0, tk.END)
        update_age_entry.delete(0, tk.END)

    except pyodbc.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error updating craft: {str(e)}")


root = tk.Tk()
root.title("Craft Ideas Database Operations")
root.geometry("600x950")  # size of the GUI

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.grid(row=0, column=0, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


def create_frame_with_title(parent, title_text):
    frame = tk.Frame(parent)
    title_label = tk.Label(frame, text=title_text, font=('Arial', 14, 'bold'))
    title_label.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

    return frame


insert_frame = create_frame_with_title(main_frame, "Add New Craft")
insert_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

tk.Label(insert_frame, text="User:").grid(row=1, column=0, sticky='w')
user_id_var = tk.StringVar()
user_ids = fetch_user_ids()
user_id_dict = {f"{uid} - {name}": uid for name, uid in user_ids}
user_id_dropdown = ttk.Combobox(insert_frame, textvariable=user_id_var, state='readonly')
user_id_dropdown['values'] = list(user_id_dict.keys())
user_id_dropdown.grid(row=1, column=1, pady=5, sticky="ew")

tk.Label(insert_frame, text="Craft Name:").grid(row=2, column=0, sticky='w')
insert_name_entry = tk.Entry(insert_frame)
insert_name_entry.grid(row=2, column=1, pady=5, sticky="ew")

tk.Label(insert_frame, text="Difficulty Level:").grid(row=3, column=0, sticky='w')
difficulty_var = tk.StringVar()
difficulty_dropdown = ttk.Combobox(insert_frame, textvariable=difficulty_var, state='readonly')
difficulty_dropdown['values'] = ['Easy', 'Medium', 'Hard']
difficulty_dropdown.grid(row=3, column=1, pady=5, sticky="ew")

tk.Label(insert_frame, text="Craft Type:").grid(row=4, column=0, sticky='w')
craft_type_var = tk.StringVar()
craft_type_dropdown = ttk.Combobox(insert_frame, textvariable=craft_type_var, state='readonly')
craft_type_dropdown['values'] = ['Seasonal', 'Decorative', 'Educational']
craft_type_dropdown.grid(row=4, column=1, pady=5, sticky="ew")

tk.Label(insert_frame, text="Theme:").grid(row=5, column=0, sticky='w')
theme_entry = tk.Entry(insert_frame)
theme_entry.grid(row=5, column=1, pady=5, sticky="ew")

tk.Label(insert_frame, text="Estimated Time (minutes):").grid(row=6, column=0, sticky='w')
insert_time_entry = tk.Entry(insert_frame)
insert_time_entry.grid(row=6, column=1, pady=5, sticky="ew")

tk.Label(insert_frame, text="Age Range (e.g., 5-10):").grid(row=7, column=0, sticky='w')
insert_age_entry = tk.Entry(insert_frame)
insert_age_entry.grid(row=7, column=1, pady=5, sticky="ew")

insert_button = tk.Button(
    insert_frame,
    text="Add Craft",
    command=insert_craft,
    bg='#4CAF50',
    fg='white',
    font=('Arial', 10, 'bold'),
    padx=20,
    pady=5
)
insert_button.grid(row=8, column=0, columnspan=2, pady=10)

delete_frame = create_frame_with_title(main_frame, "Delete Craft")
delete_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

tk.Label(delete_frame, text="Craft Name to Delete:").grid(row=1, column=0, sticky='w')
delete_name_entry = tk.Entry(delete_frame)
delete_name_entry.grid(row=1, column=1, pady=5, sticky="ew")
delete_button = tk.Button(
    delete_frame, text="Delete Craft", command=delete_craft,
    bg='#F44336', fg='white', font=('Arial', 10, 'bold')
)
delete_button.grid(row=2, column=0, columnspan=2, pady=5)

update_frame = create_frame_with_title(main_frame, "Update Craft")
update_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

tk.Label(update_frame, text="Craft Name to Update:").grid(row=1, column=0, sticky='w')
update_name_entry = tk.Entry(update_frame)
update_name_entry.grid(row=1, column=1, pady=5, sticky="ew")

tk.Label(update_frame, text="New Difficulty Level:").grid(row=2, column=0, sticky='w')
update_difficulty_var = tk.StringVar()
update_difficulty_dropdown = ttk.Combobox(update_frame, textvariable=update_difficulty_var, state='readonly')
update_difficulty_dropdown['values'] = ['Easy', 'Medium', 'Hard']
update_difficulty_dropdown.grid(row=2, column=1, pady=5, sticky="ew")

tk.Label(update_frame, text="New Theme:").grid(row=3, column=0, sticky='w')
update_theme_entry = tk.Entry(update_frame)
update_theme_entry.grid(row=3, column=1, pady=5, sticky="ew")

tk.Label(update_frame, text="New Estimated Time (minutes):").grid(row=4, column=0, sticky='w')
update_time_entry = tk.Entry(update_frame)
update_time_entry.grid(row=4, column=1, pady=5, sticky="ew")

tk.Label(update_frame, text="New Age Range (e.g., 5-10):").grid(row=5, column=0, sticky='w')
update_age_entry = tk.Entry(update_frame)
update_age_entry.grid(row=5, column=1, pady=5, sticky="ew")

update_button = tk.Button(
    update_frame,
    text="Update Craft",
    command=update_craft,
    bg='#FF9800',
    fg='white',
    font=('Arial', 10, 'bold'),
    padx=20,
    pady=5
)
update_button.grid(row=6, column=0, columnspan=2, pady=10)

query_frame = create_frame_with_title(main_frame, "Query Crafts")
query_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")

easy_button = tk.Button(
    query_frame,
    text="Show Easy Crafts",
    command=lambda: query_crafts_by_difficulty('Easy'),
    bg='#2196F3',
    fg='white',
    font=('Arial', 10, 'bold'),
    padx=20,
    pady=5
)
easy_button.grid(row=1, column=0, pady=5, padx=5)

medium_button = tk.Button(
    query_frame,
    text="Show Medium Crafts",
    command=lambda: query_crafts_by_difficulty('Medium'),
    bg='#2196F3',
    fg='white',
    font=('Arial', 10, 'bold'),
    padx=20,
    pady=5
)
medium_button.grid(row=1, column=1, pady=5, padx=5)

hard_button = tk.Button(
    query_frame,
    text="Show Hard Crafts",
    command=lambda: query_crafts_by_difficulty('Hard'),
    bg='#2196F3',
    fg='white',
    font=('Arial', 10, 'bold'),
    padx=20,
    pady=5
)
hard_button.grid(row=1, column=2, pady=5, padx=5)

quit_button = tk.Button(
    main_frame,
    text="Quit Application",
    command=quit_application,
    bg='#9E9E9E',
    fg='white',
    font=('Arial', 10, 'bold'),
    padx=20,
    pady=5
)
quit_button.grid(row=4, column=0, pady=20)

root.mainloop()

conn.close()
