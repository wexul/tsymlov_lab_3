"""Задание 4 (средняя сложность): класс «Фигура» (площадь, периметр).

Базовый класс Figure задаёт общий интерфейс (area, perimeter, describe),
конкретные фигуры (Rectangle, Circle, Triangle) наследуют его и
реализуют свои формулы. Демонстрация показывает полиморфизм: одна и та
же операция describe() вызывается для объектов разных классов.

Запуск:
    python task04_figure.py            # демонстрация на наборе фигур
    python task04_figure.py rect 3 4   # площадь и периметр прямоугольника
    python task04_figure.py circle 5   # площадь и длина окружности
    python task04_figure.py tri 3 4 5  # площадь и периметр треугольника
"""

from __future__ import annotations

import math
import sys


class Figure:
    """Базовый класс геометрической фигуры.

    Определяет общий интерфейс: area() и perimeter(). Наследники
    обязаны переопределить оба метода, иначе получат NotImplementedError.
    """

    name = "фигура"

    def area(self) -> float:
        """Возвращает площадь фигуры."""
        raise NotImplementedError(
            "area() должен быть переопределён в наследнике")

    def perimeter(self) -> float:
        """Возвращает периметр фигуры."""
        raise NotImplementedError(
            "perimeter() должен быть переопределён в наследнике")

    def describe(self) -> str:
        """Возвращает строку с названием, площадью и периметром."""
        return (f"{self.name}: площадь = {self.area():.4g}, "
                f"периметр = {self.perimeter():.4g}")


def _check_positive(values: tuple[float, ...], what: str) -> None:
    """Проверяет, что все размеры положительны."""
    for value in values:
        if value <= 0:
            raise ValueError(f"{what} должны быть положительными, "
                             f"получено {value}")


class Rectangle(Figure):
    """Прямоугольник по двум сторонам."""

    name = "прямоугольник"

    def __init__(self, width: float, height: float) -> None:
        _check_positive((width, height), "стороны прямоугольника")
        self.width = width
        self.height = height

    def area(self) -> float:
        """Площадь прямоугольника: a * b."""
        return self.width * self.height

    def perimeter(self) -> float:
        """Периметр прямоугольника: 2 * (a + b)."""
        return 2 * (self.width + self.height)


class Circle(Figure):
    """Круг по радиусу."""

    name = "круг"

    def __init__(self, radius: float) -> None:
        _check_positive((radius,), "радиус")
        self.radius = radius

    def area(self) -> float:
        """Площадь круга: pi * r^2."""
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        """Длина окружности: 2 * pi * r."""
        return 2 * math.pi * self.radius


class Triangle(Figure):
    """Треугольник по трём сторонам; площадь — по формуле Герона."""

    name = "треугольник"

    def __init__(self, side_a: float, side_b: float,
                 side_c: float) -> None:
        _check_positive((side_a, side_b, side_c), "стороны треугольника")
        if (side_a + side_b <= side_c or side_b + side_c <= side_a
                or side_a + side_c <= side_b):
            raise ValueError(
                f"стороны {side_a}, {side_b}, {side_c} не образуют "
                "треугольник (нарушено неравенство треугольника)")
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    def area(self) -> float:
        """Площадь по формуле Герона."""
        half = self.perimeter() / 2
        return math.sqrt(half * (half - self.side_a)
                         * (half - self.side_b) * (half - self.side_c))

    def perimeter(self) -> float:
        """Периметр треугольника: a + b + c."""
        return self.side_a + self.side_b + self.side_c


def build_figure(kind: str, params: list[float]) -> Figure:
    """Создаёт фигуру по имени и списку параметров."""
    if kind == "rect" and len(params) == 2:
        return Rectangle(params[0], params[1])
    if kind == "circle" and len(params) == 1:
        return Circle(params[0])
    if kind == "tri" and len(params) == 3:
        return Triangle(params[0], params[1], params[2])
    raise ValueError(
        "неверные аргументы; форматы: rect a b | circle r | tri a b c")


def demo() -> None:
    """Демонстрация полиморфной работы с набором фигур."""
    figures: list[Figure] = [
        Rectangle(3, 4),
        Circle(5),
        Triangle(3, 4, 5),
        Rectangle(10, 0.5),
    ]
    print("Набор фигур (полиморфный вызов describe()):")
    for figure in figures:
        print(" ", figure.describe())
    total = sum(figure.area() for figure in figures)
    print(f"Суммарная площадь всех фигур: {total:.4g}")
    print("Попытка создать треугольник со сторонами 1, 1, 5:")
    try:
        Triangle(1, 1, 5)
    except ValueError as error:
        print(f"  Ошибка: {error}")


def main() -> None:
    """Точка входа: разбор аргументов или демонстрация."""
    if len(sys.argv) > 1:
        try:
            params = [float(item.replace(",", "."))
                      for item in sys.argv[2:]]
            figure = build_figure(sys.argv[1], params)
        except ValueError as error:
            print(f"Ошибка: {error}")
            sys.exit(1)
        print(figure.describe())
    else:
        demo()


if __name__ == "__main__":
    main()
