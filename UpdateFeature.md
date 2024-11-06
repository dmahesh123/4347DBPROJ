#CHANGES MADE

**Fetch and Display Craft IDs for Update:**

Added a fetch_craft_ids() function to retrieve available Craft IDs from the Craft table.
A dropdown menu labeled "Select Craft ID to Update" allows the user to select a Craft ID. This dropdown is populated with Craft IDs and triggers the load_craft_data() function on selection to load existing data for that ID.

**Modify load_craft_data() to Load Selected Craft Data:**

Adjusted load_craft_data() to load the selected Craft’s details (UserID, CraftName, DifficultyLevel, EstimatedTime, and AgeRange) into the form fields, allowing for easy updating.
Combined Add and Update Form:

Merged the functionality of adding and updating a craft into a single form by reusing the input fields for both operations.
Side-by-Side Buttons for Adding and Updating:

Added a button_frame to place the "Add Craft" and "Update Craft" buttons side by side at the bottom of the form for a more intuitive layout.
Both buttons share the same styling (bg='blue', fg='white', and padding) to provide a cohesive UI experience.

**Dropdown Refresh:**

Added a periodic refresh for the Craft ID dropdown menu using root.after(100, lambda: craft_id_dropdown.config(values=fetch_craft_ids())) to ensure it updates with any new Craft IDs created.
Styling Improvements:

Enhanced button color consistency with both buttons in blue (bg='blue') and white text (fg='white').
Updated Title:

Changed the title to "Add New Craft or Updated An Existing One" to clarify that the form can be used for both adding and updating crafts.