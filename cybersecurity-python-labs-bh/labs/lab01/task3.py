import os
import csv
import json
import hashlib
import functools
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from shared.student import VARIANT_NUMBER


# ==========================================
# КРОК 1 ТА 2: ВИНЯТКИ, ХЕШУВАННЯ ТА СІЛЬ
# ==========================================

# Папка data лежить поруч з цим файлом, незалежно від місця запуску
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


# Власний виняток для коротких паролів
class ValidationError(Exception):
    pass


# Мінімальна довжина пароля для варіанту 3 (8 символів)
MIN_PASSWORD_LENGTH = 8

# Персональна сіль: номер варіанту з shared/student.py, доповнений нулями
PERSONAL_SALT = f"{VARIANT_NUMBER:05d}"  # Для варіанту 3: "00003"


def generate_hash(password: str, salt: str = "00000") -> str:
    """Хешує пароль із сіллю за допомогою алгоритму SHA-1"""
    if password is None or salt is None or password == "" or salt == "":
        raise ValueError("Пароль або сіль не можуть бути порожніми!")

    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValidationError(f"Пароль занадто короткий! Мінімум: {MIN_PASSWORD_LENGTH} символів.")

    # Конкатенація пароля та солі + хешування
    full_string = password + salt
    return hashlib.sha1(full_string.encode('utf-8')).hexdigest()



# КРОК 6: ДЕКОРАТОР ДЛЯ ЛОГУВАННЯ В JSON

def log_event(func):
    """Декоратор, який записує кожну спробу входу у файл log.json"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Витягуємо ім'я користувача з аргументів функції
        username = kwargs.get('username') or (args[0] if args else "unknown")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Викликаємо функцію аутентифікації
            success = func(*args, **kwargs)
            result_str = "success" if success else "failure"
        except Exception as e:
            result_str = "failure"
            save_log(username, result_str, timestamp, args, kwargs)
            raise e

        save_log(username, result_str, timestamp, args, kwargs)
        return success

    return wrapper


def save_log(username, result, timestamp, args, kwargs):
    """Допоміжна функція для запису логу в JSON-файл"""
    log_path = os.path.join(DATA_DIR, "log.json")

    log_entry = {
        "event": "login",
        "user": username,
        "result": result,
        "timestamp": timestamp,
        # Пароль у журнал не пишемо, тому args і kwargs порожні
        "args": [],
        "kwargs": {}
    }

    # Читаємо існуючі логи або створюємо новий список
    logs = []
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []

    logs.append(log_entry)

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=4)



# 3: РЕЄСТРАЦІЯ КОРИСТУВАЧІВ

# Кортеж із 10 користувачами (login, password)
users_to_register = (
    ("admin", "adminPass123"),
    ("user1", "secureWord99"),
    ("alex", "qwerty789"),
    ("maria", "mar1a_secret"),
    ("olga", "olgaSuper!"),
    ("ivan", "ivan2026_pass"),
    ("john", "johnnyBGood"),
    ("kate", "katerina9"),
    ("petro", "petroPowerful"),
    ("guest", "guestPassword")
)


def create_user(username, password):
    #Створюю кортеж (username, hash_value)
    hash_value = generate_hash(password, PERSONAL_SALT)
    return (username, hash_value)


def create_users(users_list):
    #Створю базу даних у форматі CSV
    dir_path = DATA_DIR
    # Автоматичне створення папки, якщо її немає
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, "users.csv")

    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for username, password in users_list:
            user_data = create_user(username, password)
            writer.writerow(user_data)


# КРОК 4 ТА 5: ЧИТАННЯ ТА АУТЕНТИФІКАЦІЯ

def read_database():
    """Зчитує CSV файл у список і виводить красиву структуровану таблицю"""
    file_path = os.path.join(DATA_DIR, "users.csv")
    users_db = []

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                users_db.append(row)


    print("\n" + "=" * 70)
    print(f"{'ЛОГІН':<15} | {'ХЕШ ПАРОЛЯ (SHA-1)':<50}")
    print("=" * 70)
    for username, hash_val in users_db:
        print(f"{username:<15} | {hash_val:<50}")
    print("=" * 70 + "\n")

    return users_db


@log_event
def login(username: str, password: str, users_db: list) -> bool:
    """Перевіряє логін та пароль користувача"""
    if not username or not password:
        raise ValueError("Логін або пароль не можуть бути порожніми строками!")

    # Генерую хеш введеного пароля з нашою сіллю
    input_hash = generate_hash(password, PERSONAL_SALT)

    # Шукаю користувача в базі даних
    for db_user, db_hash in users_db:
        if db_user == username:
            return db_hash == input_hash

    return False


# ==========================================
# КРОК 7 ТА 8: ОБРОБКА ВИНЯТКІВ ТА ГОЛОВНА ФУНКЦІЯ
# ==========================================

def main():
    try:
        print("1. Реєстрація користувачів та запис у CSV...")
        create_users(users_to_register)

        print("2. Зчитування бази даних та виведення таблиці:")
        users_db = read_database()

        print("3. Тестування аутентифікації (Логування записується в JSON)...")

        # Тест 1: Правильний вхід
        res1 = login("admin", "adminPass123", users_db)
        print(f"Спроба входу admin/adminPass123 -> Результат: {res1}")

        # Тест 2: Неправильний пароль
        res2 = login("user1", "wrong_pass", users_db)
        print(f"Спроба входу user1/wrong_pass -> Результат: {res2}")

        # Тест 3: Неіснуючий користувач
        res3 = login("hacker", "some_password", users_db)
        print(f"Спроба входу hacker/some_password -> Результат: {res3}")

        # Тест 4: Провокуємо ValidationError (пароль коротший за 8 символів)
        print("\nСпроба входу з коротким паролем:")
        login("alex", "123", users_db)

    except FileNotFoundError:
        print("Помилка: Файл або директорію не знайдено.")
    except PermissionError:
        print("Помилка: Немає прав доступу для роботи з файлами.")
    except IOError:
        print("Помилка: Збій введення-виведення при роботі з файлом.")
    except ValidationError as ve:
        print(f"Помилка валідації: {ve}")
    except ValueError as val_err:
        print(f"Помилка значення: {val_err}")
    except Exception as e:
        print(f"Непередбачувана помилка: {e}")


if __name__ == "__main__":
    main()