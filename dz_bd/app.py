from pymongo import MongoClient
import sys

client = MongoClient("mongodb://localhost:27017/")
db = client["UniversityDB"]

students = db["students"]
grades = db["grades"]
disciplines = db["disciplines"]
professors = db["professors"]

def show_all_students():
    print("\nСписок студентов")
    all_students = students.find()
    for s in all_students:
        print(f"{s['student_id']}: {s['last_name']} {s['first_name']} - группа {s['group']}")

def find_student():
    name = input("Введите фамилию: ")
    result = students.find({"last_name": name})
    for s in result:
        print(f"{s['student_id']}: {s['last_name']} {s['first_name']} - группа {s['group']}")

def show_grades():
    sid = input("Введите номер зачетки: ")
    student = students.find_one({"student_id": sid})
    if student:
        print(f"{student['last_name']} {student['first_name']}")
        student_grades = grades.find({"student_id": sid})
        for g in student_grades:
            print(f"{g['discipline_name']}: {g['grade']}")
    else:
        print("Студент не найден")

def add_student():
    new_student = {
        "student_id": input("Номер зачетки: "),
        "first_name": input("Имя: "),
        "last_name": input("Фамилия: "),
        "group": input("Группа: ")
    }
    students.insert_one(new_student)
    print("Студент добавлен")

def add_grade():
    sid = input("Номер зачетки: ")
    student = students.find_one({"student_id": sid})
    if not student:
        print("Студент не найден")
        return
    
    print("Дисциплины:")
    all_disc = disciplines.find()
    for d in all_disc:
        print(f"- {d['name']}")
    
    disc_name = input("Название дисциплины: ")
    grade_val = input("Оценка: ")
    
    new_grade = {
        "student_id": sid,
        "discipline_name": disc_name,
        "grade": grade_val
    }
    grades.insert_one(new_grade)
    print("Оценка добавлена")

def menu():
    while True:
        print("\n1. Все студенты")
        print("2. Поиск по фамилии")
        print("3. Оценки студента")
        print("4. Добавить студента")
        print("5. Добавить оценку")
        print("6. Выход")
        
        choice = input("Выберите: ")
        
        if choice == "1":
            show_all_students()
        elif choice == "2":
            find_student()
        elif choice == "3":
            show_grades()
        elif choice == "4":
            add_student()
        elif choice == "5":
            add_grade()
        elif choice == "6":
            sys.exit(0)
        else:
            print("Неверный ввод")

if __name__ == "__main__":
    menu()