"""Задание 9 (повышенная сложность): абстрактный класс через abc.

Shape — абстрактный базовый класс (abc.ABC): создать его экземпляр
нельзя (TypeError), а наследник обязан реализовать абстрактные методы
area() и perimeter() и абстрактное свойство name. Конкретные фигуры
(CircleShape, RectangleShape, TriangleShape) реализуют интерфейс, что
позволяет писать полиморфные функции вроде total_area().

Запуск:
    python task09_abc_shape.py           # демонстрация
    python task09_abc_shape.py circle 2  # площадь и периметр круга
    python task09_abc_shape.py rect 3 4  # площадь и периметр прямоуг.
    python task09_abc_shape.py tri 3 4 5 # площадь и периметр треуг-ка
"""

from __future__ import annotations

import math
import sys
from abc import ABC, abstractmethod


class Shape(ABC):
    """Абстрактная фигура: интерфейс area/perimeter/name."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Название фигуры (абстрактное свойство)."""

    @abstractmethod
    def area(self) -> float:
        """Площадь фигуры (абстрактный метод)."""

    @abstractmethod
    def perimeter(self) -> float:
        """Периметр фигуры (абстрактный метод)."""

    def describe(self) -> str:
        """Общий неабстрактный метод, унаследованный всеми фигурами."""
        return (f"{self.name}: площадь = {self.area():.4g}, "
                f"периметр = {self.perimeter():.4g}")


def _check_positive(values: tuple[float, ...], what: str) -> None:
    """Проверяет, что все размеры положительны."""
    for value in values:
        if value <= 0:
            raise ValueError(f"{what} должны быть положительными, "
                             f"получено {value}")


class CircleShape(Shape):
    """Круг (конкретная реализация абстрактной фигуры)."""

    def __init__(self, radius: float) -> None:
        _check_positive((radius,), "радиус")
        self.radius = radius

    @property
    def name(self) -> str:
        """Название фигуры."""
        return "круг"

    def area(self) -> float:
        """Площадь круга: pi * r^2."""
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        """Длина окружности: 2 * pi * r."""
        return 2 * math.pi * self.radius


class RectangleShape(Shape):
    """Прямоугольник (конкретная реализация абстрактной фигуры)."""

    def __init__(self, width: float, height: float) -> None:
        _check_positive((width, height), "стороны прямоугольника")
        self.width = width
        self.height = height

    @property
    def name(self) -> str:
        """Название фигуры."""
        return "прямоугольник"

    def area(self) -> float:
        """Площадь прямоугольника: a * b."""
        return self.width * self.height

    def perimeter(self) -> float:
        """Периметр прямоугольника: 2 * (a + b)."""
        return 2 * (self.width + self.height)


class TriangleShape(Shape):
    """Треугольник (конкретная реализация абстрактной фигуры)."""

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

    @property
    def name(self) -> str:
        """Название фигуры."""
        return "треугольник"

    def area(self) -> float:
        """Площадь по формуле Герона."""
        half = self.perimeter() / 2
        return math.sqrt(half * (half - self.side_a)
                         * (half - self.side_b) * (half - self.side_c))

    def perimeter(self) -> float:
        """Периметр треугольника: a + b + c."""
        return self.side_a + self.side_b + self.side_c


def total_area(shapes: list[Shape]) -> float:
    """Суммарная площадь списка фигур (полиморфная функция)."""
    return sum(shape.area() for shape in shapes)


def build_shape(kind: str, params: list[float]) -> Shape:
    """Создаёт фигуру по имени и списку параметров."""
    if kind == "circle" and len(params) == 1:
        return CircleShape(params[0])
    if kind == "rect" and len(params) == 2:
        return RectangleShape(params[0], params[1])
    if kind == "tri" and len(params) == 3:
        return TriangleShape(params[0], params[1], params[2])
    raise ValueError(
        "неверные аргументы; форматы: circle r | rect a b | tri a b c")


def demo() -> None:
    """Демонстрация абстрактного класса и полиморфизма."""
    print("Попытка создать экземпляр абстрактного класса Shape():")
    try:
        Shape()  # type: ignore[abstract]
    except TypeError as error:
        print(f"  TypeError: {error}")

    shapes: list[Shape] = [CircleShape(2), RectangleShape(3, 4),
                           TriangleShape(3, 4, 5)]
    print("Конкретные фигуры (наследники Shape):")
    for shape in shapes:
        print(" ", shape.describe())
    print(f"Полиморфная total_area(): {total_area(shapes):.4g}")
    print(f"isinstance(CircleShape(1), Shape): "
          f"{isinstance(CircleShape(1), Shape)}")
    print(f"issubclass(TriangleShape, Shape): "
          f"{issubclass(TriangleShape, Shape)}")


def main() -> None:
    """Точка входа: разбор аргументов или демонстрация."""
    if len(sys.argv) > 1:
        try:
            params = [float(item.replace(",", "."))
                      for item in sys.argv[2:]]
            shape = build_shape(sys.argv[1], params)
        except ValueError as error:
            print(f"Ошибка: {error}")
            sys.exit(1)
        print(shape.describe())
    else:
        demo()


if __name__ == "__main__":
    main()
