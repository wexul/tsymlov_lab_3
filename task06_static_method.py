"""Задание 6 (средняя сложность): класс со статическим методом.

TemperatureConverter — класс-утилита для перевода температур между
шкалами Цельсия, Фаренгейта и Кельвина. Методы объявлены через
@staticmethod: им не нужен ни экземпляр (self), ни класс (cls) —
они вызываются прямо на классе. Для контраста добавлен @classmethod
absolute_zero(), который возвращает константу в шкале класса.

Запуск:
    python task06_static_method.py          # демонстрация
    python task06_static_method.py 36.6     # перевод °C во все шкалы
"""

from __future__ import annotations

import sys

ABSOLUTE_ZERO_C = -273.15


class TemperatureConverter:
    """Утилиты перевода температур; экземпляр не требуется."""

    scale = "C"

    @staticmethod
    def _check_physical(celsius: float) -> None:
        """Отклоняет температуры ниже абсолютного нуля."""
        if celsius < ABSOLUTE_ZERO_C:
            raise ValueError(
                f"температура {celsius} °C ниже абсолютного нуля "
                f"({ABSOLUTE_ZERO_C} °C)")

    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Переводит градусы Цельсия в Фаренгейты."""
        TemperatureConverter._check_physical(celsius)
        return celsius * 9 / 5 + 32

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Переводит градусы Фаренгейта в Цельсии."""
        celsius = (fahrenheit - 32) * 5 / 9
        TemperatureConverter._check_physical(celsius)
        return celsius

    @staticmethod
    def celsius_to_kelvin(celsius: float) -> float:
        """Переводит градусы Цельсия в Кельвины."""
        TemperatureConverter._check_physical(celsius)
        return celsius - ABSOLUTE_ZERO_C

    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        """Переводит Кельвины в градусы Цельсия."""
        if kelvin < 0:
            raise ValueError(f"температура {kelvin} K ниже "
                             "абсолютного нуля (0 K)")
        return kelvin + ABSOLUTE_ZERO_C

    @classmethod
    def absolute_zero(cls) -> float:
        """Возвращает абсолютный ноль в шкале класса (classmethod)."""
        if cls.scale == "C":
            return ABSOLUTE_ZERO_C
        if cls.scale == "F":
            return cls.celsius_to_fahrenheit(ABSOLUTE_ZERO_C)
        return 0.0


def demo() -> None:
    """Демонстрация статических методов класса."""
    print("Статические методы вызываются на классе без экземпляра:")
    table = [0, 36.6, 100, -40]
    print(f"{'°C':>8} {'°F':>10} {'K':>10}")
    for celsius in table:
        fahrenheit = TemperatureConverter.celsius_to_fahrenheit(celsius)
        kelvin = TemperatureConverter.celsius_to_kelvin(celsius)
        print(f"{celsius:>8} {fahrenheit:>10.2f} {kelvin:>10.2f}")
    print("Обратный перевод: 98.6 °F = "
          f"{TemperatureConverter.fahrenheit_to_celsius(98.6):.2f} °C")
    print("classmethod absolute_zero(): "
          f"{TemperatureConverter.absolute_zero()} °C")
    print("Попытка перевести -300 °C (ниже абсолютного нуля):")
    try:
        TemperatureConverter.celsius_to_fahrenheit(-300)
    except ValueError as error:
        print(f"  Ошибка: {error}")


def main() -> None:
    """Точка входа: перевод аргумента °C во все шкалы или демо."""
    if len(sys.argv) > 1:
        try:
            celsius = float(sys.argv[1].replace(",", "."))
            fahrenheit = TemperatureConverter.celsius_to_fahrenheit(celsius)
            kelvin = TemperatureConverter.celsius_to_kelvin(celsius)
        except ValueError as error:
            print(f"Ошибка: {error}")
            sys.exit(1)
        print(f"{celsius} °C = {fahrenheit:.2f} °F = {kelvin:.2f} K")
    else:
        demo()


if __name__ == "__main__":
    main()
