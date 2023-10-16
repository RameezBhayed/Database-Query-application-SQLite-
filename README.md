# Database-Query-application-SQL-

This is the Python script for a data querying application I made that interacts with an SQLite database to perform various operations based on user commands. Below is a description of the key components and functionalities of my script:

Database Connection:
The script starts by connecting to an SQLite database named "HyperionDev.db" using the sqlite3 library.

Functions:
usage_is_incorrect(input, num_args): This function checks if the user's command has the correct number of arguments and returns True if the usage is incorrect.
store_data_as_json(data, filename): Stores data in JSON format in the specified file.
store_data_as_xml(data, columns, filename): Stores data in XML format in the specified file.
offer_to_store(data, columns): Asks the user if they want to store the results and determines the file format (JSON or XML) for data storage.

Main Menu:
The script displays a main menu to the user, where they can choose various options by entering commands.

Options in Main Menu:
d: Demonstrates querying and displaying data from the database.
vs <student_id>: Allows the user to view subjects taken by a specific student.
la <firstname> <surname>: Looks up the address for a given student based on their first name and surname.
lr <student_id>: Lists reviews for a given student based on their student ID.
lc <teacher_id>: Lists all courses taught by a specific teacher based on their teacher ID.
lnc: Lists all students who haven't completed their courses.
lf: Lists all students who have completed their courses and achieved a score of 30 or below.
e: Exits the program.

Data Retrieval and Display:
Depending on the user's chosen command, the script performs SQL queries on the SQLite database and retrieves data.
The retrieved data is displayed to the user in a formatted manner.

Data Storage Option:
After displaying data to the user, the script asks if the user wants to store the results.
If the user chooses to store the results, they are prompted to specify a filename with a .json or .xml extension, and the data is saved in the corresponding format.

Loop and Exit:
The script runs in a loop, allowing the user to execute multiple commands until they choose to exit (e option).

Error Handling:
The script handles potential errors, such as incorrect command usage and invalid file extensions.
Overall, this script provides a command-line interface for querying and interacting with a database, making it possible to retrieve and display information based on user commands and optionally save the results in JSON or XML formats. It can be used as a simple database querying tool.
