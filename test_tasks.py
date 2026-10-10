"""Модульные тесты всех заданий лабораторной №3 (unittest).

Запуск: python -m unittest -v
"""

from __future__ import annotations

import json
import math
import tempfile
import unittest
from pathlib import Path

from task04_figure import Circle, Figure, Rectangle, Triangle
from task05_json_serialization import JsonSerializable, Student
from task06_static_method import ABSOLUTE_ZERO_C, TemperatureConverter
from task09_abc_shape import (
    CircleShape,
    RectangleShape,
    Shape,
    TriangleShape,
    total_area,
)
from task10_iterator import FibonacciIterator


class TestFigure(unittest.TestCase):
    """Задание 4: класс «Фигура» и наследники."""

    def test_rectangle_area_and_perimeter(self) -> None:
        rect = Rectangle(3, 4)
        self.assertEqual(rect.area(), 12)
        self.assertEqual(rect.perimeter(), 14)

    def test_circle_area_and_perimeter(self) -> None:
        circle = Circle(1)
        self.assertAlmostEqual(circle.area(), math.pi)
        self.assertAlmostEqual(circle.perimeter(), 2 * math.pi)

    def test_triangle_heron(self) -> None:
        triangle = Triangle(3, 4, 5)
        self.assertAlmostEqual(triangle.area(), 6.0)
        self.assertEqual(triangle.perimeter(), 12)

    def test_base_class_methods_raise(self) -> None:
        with self.assertRaises(NotImplementedError):
            Figure().area()
        with self.assertRaises(NotImplementedError):
            Figure().perimeter()

    def test_non_positive_dimensions_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Rectangle(0, 4)
        with self.assertRaises(ValueError):
            Circle(-1)
        with self.assertRaises(ValueError):
            Triangle(3, 0, 5)

    def test_triangle_inequality(self) -> None:
        with self.assertRaises(ValueError):
            Triangle(1, 1, 5)
        with self.assertRaises(ValueError):
            Triangle(1, 2, 3)

    def test_polymorphism(self) -> None:
        figures: list[Figure] = [Rectangle(2, 3), Triangle(3, 4, 5)]
        self.assertAlmostEqual(sum(f.area() for f in figures), 12.0)
        self.assertIsInstance(figures[0], Figure)

    def test_describe_format(self) -> None:
        text = Rectangle(3, 4).describe()
        self.assertIn("прямоугольник", text)
        self.assertIn("площадь = 12", text)


class TestTemperatureConverter(unittest.TestCase):
    """Задание 6: класс со статическими методами."""

    def test_known_conversions(self) -> None:
        conv = TemperatureConverter
        self.assertAlmostEqual(conv.celsius_to_fahrenheit(100), 212.0)
        self.assertAlmostEqual(conv.celsius_to_fahrenheit(-40), -40.0)
        self.assertAlmostEqual(conv.fahrenheit_to_celsius(32), 0.0)
        self.assertAlmostEqual(conv.celsius_to_kelvin(0), 273.15)
        self.assertAlmostEqual(conv.kelvin_to_celsius(0),
                               ABSOLUTE_ZERO_C)

    def test_round_trip(self) -> None:
        conv = TemperatureConverter
        for celsius in (-40, 0, 36.6, 100):
            restored = conv.fahrenheit_to_celsius(
                conv.celsius_to_fahrenheit(celsius))
            self.assertAlmostEqual(restored, celsius)

    def test_below_absolute_zero_rejected(self) -> None:
        with self.assertRaises(ValueError):
            TemperatureConverter.celsius_to_fahrenheit(-300)
        with self.assertRaises(ValueError):
            TemperatureConverter.fahrenheit_to_celsius(-1000)
        with self.assertRaises(ValueError):
            TemperatureConverter.kelvin_to_celsius(-1)

    def test_absolute_zero_boundary_allowed(self) -> None:
        result = TemperatureConverter.celsius_to_kelvin(ABSOLUTE_ZERO_C)
        self.assertAlmostEqual(result, 0.0)

    def test_callable_on_class_and_instance(self) -> None:
        via_class = TemperatureConverter.celsius_to_fahrenheit(0)
        via_instance = TemperatureConverter().celsius_to_fahrenheit(0)
        self.assertEqual(via_class, via_instance)

    def test_absolute_zero_classmethod(self) -> None:
        self.assertEqual(TemperatureConverter.absolute_zero(),
                         ABSOLUTE_ZERO_C)


class TestFibonacciIterator(unittest.TestCase):
    """Задание 10: класс-итератор."""

    def test_first_numbers(self) -> None:
        self.assertEqual(list(FibonacciIterator(10)),
                         [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])

    def test_zero_and_one(self) -> None:
        self.assertEqual(list(FibonacciIterator(0)), [])
        self.assertEqual(list(FibonacciIterator(1)), [0])

    def test_negative_count_rejected(self) -> None:
        with self.assertRaises(ValueError):
            FibonacciIterator(-1)

    def test_iterator_protocol(self) -> None:
        iterator = FibonacciIterator(3)
        self.assertIs(iter(iterator), iterator)
        self.assertEqual(next(iterator), 0)
        self.assertEqual(next(iterator), 1)
        self.assertEqual(next(iterator), 1)
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_exhausted_iterator_stays_empty(self) -> None:
        iterator = FibonacciIterator(2)
        list(iterator)
        self.assertEqual(list(iterator), [])

    def test_works_with_builtin_functions(self) -> None:
        self.assertEqual(sum(FibonacciIterator(10)), 88)
        self.assertEqual(max(FibonacciIterator(7)), 8)


class TestJsonSerialization(unittest.TestCase):
    """Задание 5 (повышенная): сериализация объектов в JSON."""

    def test_round_trip(self) -> None:
        student = Student("Полошков Ярослав Витальевич",
                          "220042-11", [5, 4, 5])
        restored = Student.from_json(student.to_json())
        self.assertEqual(restored, student)

    def test_to_json_is_valid_json_with_cyrillic(self) -> None:
        student = Student("Иванов Иван", "220042-11", [4])
        text = student.to_json()
        self.assertIn("Иванов Иван", text)
        self.assertEqual(json.loads(text)["group"], "220042-11")

    def test_save_and_load_file(self) -> None:
        student = Student("Петров Пётр", "220042-11", [3, 5])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "student.json"
            student.save(path)
            self.assertEqual(Student.load(path), student)

    def test_load_missing_file(self) -> None:
        with self.assertRaises(FileNotFoundError):
            Student.load("definitely_missing_file.json")

    def test_invalid_json_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Student.from_json("{not json}")
        with self.assertRaises(ValueError):
            Student.from_json("[1, 2, 3]")

    def test_missing_required_field(self) -> None:
        with self.assertRaises(ValueError):
            Student.from_dict({"group": "220042-11"})

    def test_student_validation(self) -> None:
        with self.assertRaises(ValueError):
            Student("  ", "220042-11")
        with self.assertRaises(ValueError):
            Student("Иванов Иван", "")
        with self.assertRaises(ValueError):
            Student("Иванов Иван", "220042-11", [6])

    def test_average_grade(self) -> None:
        self.assertEqual(Student("А Б", "Г").average_grade(), None)
        student = Student("А Б", "Г", [5, 4, 5])
        self.assertAlmostEqual(student.average_grade(), 14 / 3)

    def test_mixin_requires_overrides(self) -> None:
        with self.assertRaises(NotImplementedError):
            JsonSerializable().to_json()
        with self.assertRaises(NotImplementedError):
            JsonSerializable.from_json("{}")


class TestAbcShape(unittest.TestCase):
    """Задание 9 (повышенная): абстрактный класс через abc."""

    def test_abstract_class_not_instantiable(self) -> None:
        with self.assertRaises(TypeError):
            Shape()  # type: ignore[abstract]

    def test_concrete_shapes_are_shapes(self) -> None:
        for shape in (CircleShape(1), RectangleShape(2, 3),
                      TriangleShape(3, 4, 5)):
            self.assertIsInstance(shape, Shape)
        self.assertTrue(issubclass(CircleShape, Shape))

    def test_areas_and_perimeters(self) -> None:
        self.assertAlmostEqual(CircleShape(1).area(), math.pi)
        self.assertAlmostEqual(CircleShape(1).perimeter(), 2 * math.pi)
        self.assertEqual(RectangleShape(3, 4).area(), 12)
        self.assertEqual(RectangleShape(3, 4).perimeter(), 14)
        self.assertAlmostEqual(TriangleShape(3, 4, 5).area(), 6.0)

    def test_total_area(self) -> None:
        shapes = [CircleShape(1), RectangleShape(3, 4)]
        self.assertAlmostEqual(total_area(shapes), math.pi + 12)

    def test_name_property(self) -> None:
        self.assertEqual(CircleShape(1).name, "круг")
        self.assertEqual(TriangleShape(3, 4, 5).name, "треугольник")

    def test_validation(self) -> None:
        with self.assertRaises(ValueError):
            CircleShape(0)
        with self.assertRaises(ValueError):
            RectangleShape(-2, 3)
        with self.assertRaises(ValueError):
            TriangleShape(1, 1, 5)

    def test_describe_inherited_from_abc(self) -> None:
        self.assertIn("круг", CircleShape(2).describe())


if __name__ == "__main__":
    unittest.main()
