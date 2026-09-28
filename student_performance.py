import json

students = []
DATA_FILE = "student_data.json"


def load_data():
    global students

    try:
        with open(DATA_FILE, "r") as file:
            students = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        students = []


def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)


def calculate_average(marks):
    total = 0

    for mark in marks:
        total += mark

    return round(total / len(marks), 2)


def calculate_grade(average):
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


def display_student(student):
    average = calculate_average(student["marks"])
    grade = calculate_grade(average)

    if grade == "F":
        result = "FAIL"
    else:
        result = "PASS"

    print("\n------------------------------")
    print("Student ID :", student["id"])
    print("Name       :", student["name"])
    print("Department :", student["department"])
    print("Semester   :", student["semester"])
    print("Marks      :", student["marks"])
    print("Average    :", average)
    print("Grade      :", grade)
    print("Result     :", result)
    print("------------------------------")


def get_marks():
    marks = []

    print("\nEnter marks for 5 subjects:")

    for i in range(5):
        while True:
            try:
                mark = float(input("Subject " + str(i + 1) + ": "))

                if 0 <= mark <= 100:
                    marks.append(mark)
                    break
                else:
                    print("Marks must be between 0 and 100.")

            except ValueError:
                print("Please enter a valid number.")

    return marks


def add_student():
    print("\n--- Add Student ---")

    student_id = input("Enter student ID: ").strip()

    for student in students:
        if str(student["id"]) == student_id:
            print("Student ID already exists.")
            return

    name = input("Enter student name: ").strip()
    department = input("Enter department: ").strip()

    while True:
        try:
            semester = int(input("Enter semester: "))

            if semester > 0:
                break
            else:
                print("Semester must be a positive number.")

        except ValueError:
            print("Please enter a valid semester.")

    marks = get_marks()

    student = {
        "id": student_id,
        "name": name,
        "department": department,
        "semester": semester,
        "marks": marks
    }

    students.append(student)
    save_data()

    print("\nStudent added successfully.")
    display_student(student)


def view_students():
    print("\n--- All Students ---")

    if len(students) == 0:
        print("No student records found.")
        return

    for student in students:
        display_student(student)


def search_student():
    print("\n--- Search Student ---")

    student_id = input("Enter student ID: ").strip()

    for student in students:
        if str(student["id"]) == student_id:
            display_student(student)
            return

    print("Student not found.")


def update_student():
    print("\n--- Update Student ---")

    student_id = input("Enter student ID: ").strip()

    for student in students:
        if str(student["id"]) == student_id:

            print("\nCurrent student details:")
            display_student(student)

            print("\nLeave a field empty to keep the old value.")

            new_name = input("Name [" + student["name"] + "]: ").strip()
            if new_name != "":
                student["name"] = new_name

            new_department = input(
                "Department [" + student["department"] + "]: "
            ).strip()

            if new_department != "":
                student["department"] = new_department

            new_semester = input(
                "Semester [" + str(student["semester"]) + "]: "
            ).strip()

            if new_semester != "":
                try:
                    new_semester = int(new_semester)

                    if new_semester > 0:
                        student["semester"] = new_semester
                    else:
                        print("Invalid semester. Old value kept.")

                except ValueError:
                    print("Invalid semester. Old value kept.")

            update_marks = input(
                "Do you want to update marks? (y/n): "
            ).strip().lower()

            if update_marks == "y":
                student["marks"] = get_marks()

            save_data()

            print("\nStudent information updated successfully.")
            display_student(student)
            return

    print("Student not found.")


def delete_student():
    print("\n--- Delete Student ---")

    student_id = input("Enter student ID: ").strip()

    for student in students:
        if str(student["id"]) == student_id:

            display_student(student)

            confirm = input("Do you really want to delete this student? (y/n): ")
            confirm = confirm.strip().lower()

            if confirm == "y":
                students.remove(student)
                save_data()
                print("Student deleted successfully.")
            else:
                print("Delete operation cancelled.")

            return

    print("Student not found.")


def show_top_performer():
    print("\n--- Top Performer ---")

    if len(students) == 0:
        print("No student records found.")
        return

    top_student = students[0]
    top_average = calculate_average(top_student["marks"])

    for student in students:
        average = calculate_average(student["marks"])

        if average > top_average:
            top_student = student
            top_average = average

    print("Top performer:")
    display_student(top_student)


def show_class_statistics():
    print("\n--- Class Statistics ---")

    if len(students) == 0:
        print("No student records found.")
        return

    total_students = len(students)
    total_average = 0
    passed_students = 0
    failed_students = 0

    subject_totals = [0, 0, 0, 0, 0]

    grade_count = {
        "A+": 0,
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "F": 0
    }

    highest_average = -1
    lowest_average = 101

    highest_student = None
    lowest_student = None

    for student in students:
        average = calculate_average(student["marks"])
        grade = calculate_grade(average)

        total_average += average
        grade_count[grade] += 1

        if grade == "F":
            failed_students += 1
        else:
            passed_students += 1

        if average > highest_average:
            highest_average = average
            highest_student = student

        if average < lowest_average:
            lowest_average = average
            lowest_student = student

        for i in range(5):
            subject_totals[i] += student["marks"][i]

    class_average = round(total_average / total_students, 2)
    pass_percentage = round((passed_students / total_students) * 100, 2)

    print("Total students :", total_students)
    print("Class average  :", class_average)
    print("Passed         :", passed_students)
    print("Failed         :", failed_students)
    print("Pass percentage:", pass_percentage, "%")

    print("\nSubject-wise average:")
    for i in range(5):
        subject_average = round(subject_totals[i] / total_students, 2)
        print("Subject", i + 1, ":", subject_average)

    print("\nGrade distribution:")
    for grade in grade_count:
        print(grade, ":", grade_count[grade])

    print("\nHighest average:")
    print(highest_student["name"], "-", highest_average)

    print("Lowest average:")
    print(lowest_student["name"], "-", lowest_average)


def show_menu():
    print("\n===================================")
    print("   STUDENT PERFORMANCE SYSTEM")
    print("===================================")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Show Top Performer")
    print("7. Show Class Statistics")
    print("8. Exit")
    print("===================================")


def main():
    load_data()

    while True:
        show_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            show_top_performer()
        elif choice == "7":
            show_class_statistics()
        elif choice == "8":
            save_data()
            print("Thank you for using Student Performance System.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


main()
