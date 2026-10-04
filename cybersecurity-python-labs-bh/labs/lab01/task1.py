import sys
import os
import random
import string
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'../../')))
from shared.student import STUDENT_NAME, GROUP_NAME, VARIANT_NUMBER


def main():
    print(GROUP_NAME, VARIANT_NUMBER)

    passwords = ["UserPass1!", "temp", "Cyber$ecur1ty", "guest", "P0w3rful@Pass",
    "login", "Defens3#2023", "abc123", "Elit3@Secur", "demo"]
    criteria = {"min_length": 9, "require_digits": True, "require_upper": True,
    "require_special": True}
    forbidden_passwords = {"temp", "guest", "login", "demo", "abc123", "user"}

    print(passwords)

    def newpass():
        random_tr = random.sample(range(len(passwords)), 3)
        random_tr.sort(reverse=True)

        poped_items=[]

        #print(random_tr)
        for i in random_tr:
            pa = passwords[i]
            #print(pa)
            poped=passwords.pop(i)
            poped_items.append(poped)


        #print("видалені:", poped_items)
        passwords.extend(poped_items)
        print("новий список",passwords)


    newpass()
    min_length = criteria["min_length"]

    ne_norm_passwords = []
    weak_passwords = []
    medium_passwords = []
    strong_passwords = []
    very_strong_passwords = []

    # Заборонені
    for i in passwords:
        if i in forbidden_passwords or len(i) < min_length:
            ne_norm_passwords.append(i)

    print("заборонені паролі", ne_norm_passwords)

    # Слабкі: не заборонений і є лише одна група символів
    for i in passwords:
        if i in forbidden_passwords or len(i) < min_length:
            continue

        digits = [b for b in i if b.isdigit()]
        upper = [b for b in i if b.isupper()]
        lower = [b for b in i if b.islower()]
        special = [b for b in i if b in string.punctuation]

        groups = 0
        if digits:
            groups += 1
        if upper:
            groups += 1
        if lower:
            groups += 1
        if special:
            groups += 1

        if groups == 1:
            weak_passwords.append(i)

    print("слабкі паролі", weak_passwords)

    # Середні: не заборонений, груп символів 2 і більше, але не всі критерії
    for i in passwords:
        if i in forbidden_passwords or len(i) < min_length:
            continue

        digits = [b for b in i if b.isdigit()]
        upper = [b for b in i if b.isupper()]
        lower = [b for b in i if b.islower()]
        special = [b for b in i if b in string.punctuation]

        groups = 0
        if digits:
            groups += 1
        if upper:
            groups += 1
        if lower:
            groups += 1
        if special:
            groups += 1

        all_criteria = digits and upper and special

        if groups >= 2 and not all_criteria:
            medium_passwords.append(i)

    print("середні паролі", medium_passwords)

    # Сильні: усі критерії, довжина менша за min_length + 4
    # (довгий пароль, який повторюється, теж сюди)
    for i in passwords:
        if i in forbidden_passwords or len(i) < min_length:
            continue

        digits = [b for b in i if b.isdigit()]
        upper = [b for b in i if b.isupper()]
        special = [b for b in i if b in string.punctuation]

        all_criteria = digits and upper and special
        is_short = len(i) < min_length + 4
        is_repeated = passwords.count(i) > 1

        if all_criteria and (is_short or is_repeated):
            strong_passwords.append(i)

    print("сильні паролі", strong_passwords)

    # Дуже сильні: усі критерії, довжина від min_length + 4, унікальний
    for i in passwords:
        if i in forbidden_passwords or len(i) < min_length:
            continue

        digits = [b for b in i if b.isdigit()]
        upper = [b for b in i if b.isupper()]
        special = [b for b in i if b in string.punctuation]

        all_criteria = digits and upper and special
        is_long = len(i) >= min_length + 4
        is_unique = passwords.count(i) == 1

        if all_criteria and is_long and is_unique:
            very_strong_passwords.append(i)

    print("дуже сильні паролі", very_strong_passwords)

    # Таблиця
    print()
    print(f"{'№':<4}{'Пароль':<18}{'Довжина':<10}{'Рівень'}")
    print("-" * 45)

    number = 1
    for i in passwords:
        if i in ne_norm_passwords:
            level = "Заборонений"
        elif i in weak_passwords:
            level = "Слабкий"
        elif i in medium_passwords:
            level = "Середній"
        elif i in strong_passwords:
            level = "Сильний"
        elif i in very_strong_passwords:
            level = "Дуже сильний"
        else:
            level = "не визначено"

        print(f"{number:<4}{i:<18}{len(i):<10}{level}")
        number += 1


if __name__ == "__main__":
    main()