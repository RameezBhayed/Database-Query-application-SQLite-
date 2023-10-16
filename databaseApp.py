import sqlite3
import json
import xml.etree.ElementTree as ET

# Connecting to SQLite database
try:
    conn = sqlite3.connect("HyperionDev.db")
except sqlite3.Error:
    print("Please store your database as HyperionDev.db")
    quit()

cur = conn.cursor()


# function to check if the user command has the correct number of arguments.
def usage_is_incorrect(input, num_args):
    if len(input) != num_args + 1:
        print(f"The {input[0]} command requires {num_args} arguments.")
        return True
    return False


# Function to store data in JSON format
def store_data_as_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


# Function to store data in XML format
def store_data_as_xml(data, columns, filename):
    root = ET.Element("data")
    for record in data:
        item = ET.SubElement(root, "item")
        for index, value in enumerate(record):
            ET.SubElement(item, columns[index]).text = str(value)
    tree = ET.ElementTree(root)
    tree.write(filename)


# ask the user if they want to store the results and determine the file format
def offer_to_store(data, columns):
    while True:
        print("Would you like to store this result?")
        choice = input("Y/[N]? : ").strip().lower()
        if choice == "y":
            filename = input("Specify filename. Must end in .xml or .json: ")
            ext = filename.split(".")[-1]
            if ext == 'xml':
                store_data_as_xml(data, columns, filename)
                print(f"Data has been saved to {filename}")
                return
            elif ext == 'json':
                store_data_as_json([dict(zip(columns, record)) for record in data], filename)
                print(f"Data has been saved to {filename}")
                return
            else:
                print("Invalid file extension. Please use .xml or .json.")
        elif choice == 'n':
            print("Data not saved.")
            return
        else:
            print("Invalid choice")


# Main menu
usage = '''
Please make sure to follow the input instructions when choosing an option Eg. (vs GG00100200319)
What would you like to do?
d - demo
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taken by teacher_id
lnc                        - list all students who haven't completed their course
lf                         - list all students who have completed their course and achieved 30 or below
e                          - exit this program

Type your option here: '''

print("Welcome to the data querying app!")

# Main loop where user can interact with the system
while True:
    print()
    user_input = input(usage).split(" ")
    print()
    command = user_input[0]
    if len(user_input) > 1:
        args = user_input[1:]

# command to display student names
    if command == 'd':
        data = cur.execute("SELECT first_name, last_name FROM Student").fetchall()
        for firstname, surname in data:
            print(f"{firstname} {surname}")
        offer_to_store(data, ["first_name", "last_name"])

# Command to view subjects taken by a student
    elif command == 'vs':
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        query = """
        SELECT c.course_name
        FROM Course c
        JOIN StudentCourse sc ON c.course_code = sc.course_code
        WHERE sc.student_id = ?
        """
        data = cur.execute(query, (student_id,)).fetchall()
        for course_name, in data:
            print(course_name)
        offer_to_store(data, ["course_name"])

# command to lookup address for a given firstname and surname
    elif command == 'la':
        if usage_is_incorrect(user_input, 2):
            continue
        firstname, surname = args[0], args[1]
        query = """
        SELECT a.street, a.city, a.province, a.postal_code, a.country
        FROM Address a
        JOIN Student s ON a.address_id = s.address_id
        WHERE s.first_name = ? AND s.last_name = ?
        """
        data = cur.execute(query, (firstname, surname)).fetchall()
        for street, city, province, postal_code, country in data:
            print(f"{street}, {city}")
        offer_to_store(data, ["street", "city"])

# command to list reviews for a given student
    elif command == 'lr':
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        query = """
        SELECT r.review_text
        FROM Review r
        WHERE r.student_id = ?
        """
        data = cur.execute(query, (student_id,)).fetchall()
        for review_text, in data:
            print(review_text)
        offer_to_store(data, ["review_text"])

# Command to list all courses taught by teacher
    elif command == 'lc':
        if usage_is_incorrect(user_input, 1):
            continue
        teacher_id = args[0]
        query = """
        SELECT c.course_name
        FROM Course c
        WHERE c.teacher_id = ?
        """
        data = cur.execute(query, (teacher_id,)).fetchall()
        for course_name, in data:
            print(course_name)
            offer_to_store(data, ["course_name"])

# command to list all students who haven't completed their course
    elif command == 'lnc':
        query = """
                SELECT s.student_id, s.first_name, s.last_name, s.email, c.course_name
                FROM Student s
                JOIN StudentCourse sc ON s.student_id = sc.student_id
                JOIN Course c ON sc.course_code = c.course_code
                WHERE sc.mark IS NULL
                """
        data = cur.execute(query).fetchall()
        for student_id, first_name, last_name, email, course_name in data:
            print(f"Student ID: {student_id}, Name: {first_name} {last_name}, Email: {email}, Course: {course_name}")
        offer_to_store(data, ["student_id", "first_name", "last_name", "email", "course_name"])

# command to list all students who have completed their course and achieved 30 or below
    elif command == 'lf':
        query = """
                SELECT s.student_id, s.first_name, s.last_name, s.email, c.course_name, sc.mark
                FROM Student s
                JOIN StudentCourse sc ON s.student_id = sc.student_id
                JOIN Course c ON sc.course_code = c.course_code
                WHERE sc.mark <= 30 AND sc.mark IS NOT NULL
                """
        data = cur.execute(query).fetchall()
        for student_id, first_name, last_name, email, course_name, mark in data:
            print(
                f"Student ID: {student_id}, Name: {first_name} {last_name}, Email: {email}, Course: {course_name}, Mark: {mark}")
        offer_to_store(data, ["student_id", "first_name", "last_name", "email", "course_name", "mark"])

    elif command == 'e':
        print("Programme exited successfully!")
        break

    else:
        print(f"Incorrect command: '{command}'")

