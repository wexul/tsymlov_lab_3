"""Собирает demo_output.txt реальными прогонами программ репозитория."""

import datetime
import subprocess

SEP = "-" * 70
out = []
out.append("Лабораторная работа №3, вариант 4 - фактические запуски "
           "программ")
out.append("=" * 70)
out.append("")
out.append("Дата выполнения: " + datetime.date.today().strftime("%d.%m.%Y"))
out.append("Python: 3.11.1")
out.append("ОС: Windows 10")
out.append("")
out.append("Файл собран автоматическим прогоном всех программ репозитория:")
out.append("каждый раздел содержит команду запуска, поданные аргументы")
out.append("и полный вывод программы с кодом возврата.")
out.append("")


def run(title, cmd):
    res = subprocess.run(cmd, capture_output=True, text=True,
                         encoding="utf-8")
    out.append(SEP)
    out.append(title)
    out.append(SEP)
    out.append("$ " + " ".join(cmd))
    out.append("")
    if res.stdout.strip():
        out.append(res.stdout.rstrip("\n"))
    if res.stderr.strip():
        out.append(res.stderr.rstrip("\n"))
    out.append("")
    out.append(f"код возврата: {res.returncode}")
    out.append("")


run("Задание 4 (средняя). Класс «Фигура»: демонстрация",
    ["py", "-3", "task04_figure.py"])
run("Задание 4. Прямоугольник через аргументы",
    ["py", "-3", "task04_figure.py", "rect", "3", "4"])
run("Задание 4. Круг через аргументы",
    ["py", "-3", "task04_figure.py", "circle", "5"])
run("Задание 4. Треугольник через аргументы",
    ["py", "-3", "task04_figure.py", "tri", "3", "4", "5"])
run("Задание 4. Ошибка: стороны не образуют треугольник",
    ["py", "-3", "task04_figure.py", "tri", "1", "1", "5"])
run("Задание 6 (средняя). Класс со статическим методом: демонстрация",
    ["py", "-3", "task06_static_method.py"])
run("Задание 6. Перевод 36.6 °C через аргумент",
    ["py", "-3", "task06_static_method.py", "36.6"])
run("Задание 6. Ошибка: температура ниже абсолютного нуля",
    ["py", "-3", "task06_static_method.py", "-300"])
run("Задание 10 (средняя). Класс-итератор: демонстрация",
    ["py", "-3", "task10_iterator.py"])
run("Задание 10. Первые 15 чисел Фибоначчи через аргумент",
    ["py", "-3", "task10_iterator.py", "15"])
run("Задание 10. Ошибка: отрицательное количество чисел",
    ["py", "-3", "task10_iterator.py", "-5"])
run("Задание 5 (повышенная). Сериализация объектов в JSON",
    ["py", "-3", "task05_json_serialization.py"])
run("Задание 9 (повышенная). Абстрактный класс через abc",
    ["py", "-3", "task09_abc_shape.py"])
run("Задание 9. Круг через аргументы",
    ["py", "-3", "task09_abc_shape.py", "circle", "2"])
run("Модульные тесты всех заданий (unittest)",
    ["py", "-3", "-m", "unittest", "-v"])
run("Проверка стиля кода (flake8)",
    ["py", "-3", "-m", "flake8", ".", "--statistics"])

with open("demo_output.txt", "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(out).rstrip("\n") + "\n")
print("demo_output.txt записан, строк:", len(out))
