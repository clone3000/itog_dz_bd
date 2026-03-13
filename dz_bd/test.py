from pymongo import MongoClient
import time
import random
import string

client = MongoClient("mongodb://localhost:27017/")
db = client["UniversityDB"]
students = db["students"]
grades = db["grades"]

def generate_student(counter):
    return {
        "student_id": f"TEST{counter:04d}",
        "first_name": "Test" + random.choice(string.ascii_uppercase),
        "last_name": "Testov" + random.choice(string.ascii_uppercase),
        "group": str(random.randint(1, 5))
    }

def generate_grade(student_id):
    disciplines = ["Базы данных", "Python", "Статистика", "Инструменты промышленной разработки"]
    return {
        "student_id": student_id,
        "discipline_name": random.choice(disciplines),
        "grade": str(random.randint(2, 5))
    }

print("Тестирование...")
print()

print("Тест записи (1000 операций)")
start = time.time()
for i in range(1000):
    student = generate_student(i + 1)
    students.insert_one(student)
    grade = generate_grade(student["student_id"])
    grades.insert_one(grade)
end = time.time()
write_time = end - start
print(f"Запись: {write_time:.2f} сек")
print(f"Скорость: {1000/write_time:.0f} операций/сек")
print()

print("Тест чтения (1000 операций)")
start = time.time()
for i in range(1000):
    students.find_one({"student_id": f"TEST{random.randint(1, 1000):04d}"})
    grades.find_one({"grade": str(random.randint(2, 5))})
end = time.time()
read_time = end - start
print(f"Чтение: {read_time:.2f} сек")
print(f"Скорость: {1000/read_time:.0f} операций/сек")
print()

students.delete_many({"student_id": {"$regex": "^TEST"}})
grades.delete_many({"student_id": {"$regex": "^TEST"}})

print("Тестирование завершено")