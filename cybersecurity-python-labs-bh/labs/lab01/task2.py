def main():
    # 1. ТВОЇ ПОЧАТКОВІ ДАНІ
    users = {
        "security_chief": {"role": "security_officer", "clearance": 4, "department": "Security", "active": True},
        "network_admin": {"role": "network_admin", "clearance": 3, "department": "Network", "active": True},
        "help_desk": {"role": "support", "clearance": 1, "department": "Support", "active": True},
        "auditor_ext": {"role": "auditor", "clearance": 3, "department": "Audit", "active": True},
        "temp_worker": {"role": "temporary", "clearance": 1, "department": "Temp", "active": False}
    }

    resources = [
        ("incident_reports", 4), ("network_topology", 3), ("user_manual", 1),
        ("vulnerability_scans", 3), ("root_access", 4), ("help_tickets", 1),
        ("penetration_tests", 4), ("firewall_rules", 3), ("software_licenses", 2),
        ("faq_docs", 1)
    ]

    blocked_users = {"temp_worker", "fired_employee", "compromised_acc"}

    # Створимо повний список усіх користувачів, яких треба перевірити (включаючи заблокованих, яких немає в системі)
    all_usernames = set(users.keys()).union(blocked_users)

    # 2. ГОЛОВНИЙ ЦИКЛ ПЕРЕВІРКИ
    # Перебираємо кожного користувача
    for username in all_usernames:

        # Перебираємо кожен ресурс (назва та цифровий рівень безпеки)
        for res_name, res_level in resources:

            # Правило 1: Користувача немає в системі
            if username not in users:
                result = "DENY (User not found)"

            # Правило 2: Користувач є в списку заблокованих
            elif username in blocked_users:
                result = "DENY (User is blocked)"

            # Правило 3: Обліковий запис неактивний
            elif users[username]["active"] == False:
                result = "DENY (Account inactive)"

            # Правило 4: Рівень допуску достатній (більший або дорівнює рівню ресурсу)
            elif users[username]["clearance"] >= res_level:
                result = "ALLOW"

            # Правило 5: Рівень допуску замалий
            else:
                result = "DENY (Insufficient clearance)"

            # 3. ВИВЕДЕННЯ РЕЗУЛЬТАТУ НА ЕКРАН (строго за форматом з картинки)
            print(f"user=[{username}] resource=[{res_name}] -> {result}")


if __name__ == "__main__":
    main()