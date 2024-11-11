Running the EcoCraft GUI on Windows with SQL Server Management Studio
Please follow these steps to set up and run the EcoCraft program

1. Verify that Python 3.10.11 is installed on your machine. To check you can use 
Python --version
Also, make sure that you have SQL Server management studio running in order to use our database definitions and populated tables.

2. Install the required packages to run this program. Using PowerShell/terminal, pip install pyodbc by running pip install pyodbc.

Confirm the installation using 
pip show pyodbc

3. Set up a database connection to your IDE. Open PowerShell and run this command to identify the available ODBC drivers on your machine:
Get-OdbcDriver | Select-Object Name

Make note of this driver name and update it in the connection code for step 5. Also, make note of your machine's server and database name to create the connection. 


4.  To load the database schema, open SQL Management Studio and use the provided EcoCraft.sql to set up the database schema. Execute the SQL file to create and populate the data in the SQL environment. 


5. Run the GUI program using main.py in your IDE as the source file and ensure that you replace the fields in the connection code with your information as mentioned in step 4.


# Set up the database connection
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};' # use the driver for your machine
    'SERVER=DESKTOP-XXXXXX;' # use your server name
    'DATABASE=EcoCraft;' #use what you named the database
    'Trusted_Connection=yes;'
)

6. Run the program to launch the GUI interface and you should now be able to interact with the database based on your SQL server set up.

7. To troubleshoot, make sure that the SQL server is running and that the correct server name and database are used. If you get the error "driver not found," double-check the driver name or install the appropriate driver. 
