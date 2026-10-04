"""Головний файл: запускає всі завдання лабораторної роботи №1."""

import task1
import task2
import task3


def main():
    """Послідовно запускає завдання 1, 2 і 3."""
    task1.main()
    print()

    task2.main()
    print()

    task3.main()


if __name__ == "__main__":
    main()