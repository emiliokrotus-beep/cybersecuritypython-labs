def main():
    # 1. ПОЧАТКОВІ ДАНІ
    # Числові рівні для текстових рівнів безпеки
    levels = {
        "Public Blockchain": 1,
        "Permissioned": 2,
        "Private Network": 3,
    }

    users = {
        "blockchain_dev":        {"clearance": 3, "active": True},
        "smart_contract_auditor": {"clearance": 3, "active": True},
        "crypto_trader":         {"clearance": 2, "active": True},
        # додайте інших користувачів, яких видно нижче на фото
    }

    resources = [
        ("smart_contracts",   "Private Network"),
        ("audit_reports",     "Private Network"),
        ("trading_algorithms", "Permissioned"),
        ("wallet_interface",  "Public Blockchain"),
        ("private_keys",      "Private Network"),
        ("public_blockchain", "Public Blockchain"),
        ("defi_protocols",    "Private Network"),
        ("validator_nodes",   "Private Network"),
        ("market_data",       "Permissioned"),
        ("community_forum",   "Public Blockchain"),
    ]

    blocked_users = set()

    line = "=" * 70

    # 2. ВИВЕДЕННЯ СПИСКУ РЕСУРСІВ
    print(line)
    print("Список ресурсів та рівні безпеки")
    print(line)
    for res_name, level_name in resources:
        print(f"Ресурс: {res_name.ljust(18)} | Рівень безпеки: {level_name}")

    print()
    print(line)
    print("Перевірка прав доступу користувачів")
    print(line)
    print()

    # 3. ПЕРЕВІРКА ДОСТУПУ
    for username in users:
        print(f"--- Доступ для: {username} ---")

        for res_name, level_name in resources:
            res_level = levels[level_name]

            if username not in users:
                result = "DENY (User not found)"
            elif username in blocked_users:
                result = "DENY (User is blocked)"
            elif not users[username]["active"]:
                result = "DENY (Account inactive)"
            elif users[username]["clearance"] >= res_level:
                result = "ALLOW"
            else:
                result = "DENY (Insufficient clearance)"

            print(f"user={username} resource={res_name} -> {result}")

        print()  # порожній рядок між користувачами


if __name__ == "__main__":
    main()