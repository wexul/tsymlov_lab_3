"""Задание 10 (средняя сложность): создать класс-итератор.

FibonacciIterator — итератор по протоколу Python: метод __iter__
возвращает сам объект, __next__ выдаёт очередное число Фибоначчи и
бросает StopIteration, когда выдано count чисел. Благодаря протоколу
объект работает в цикле for, в list(), в sum() и т.д. Итератор
одноразовый: после исчерпания повторный обход не даёт элементов.

Запуск:
    python task10_iterator.py       # демонстрация
    python task10_iterator.py 15    # первые 15 чисел Фибоначчи
"""

from __future__ import annotations

import sys


class FibonacciIterator:
    """Итератор, выдающий первые count чисел Фибоначчи (0, 1, 1, 2...)."""

    def __init__(self, count: int) -> None:
        if count < 0:
            raise ValueError(f"количество чисел должно быть "
                             f"неотрицательным, получено {count}")
        self._count = count
        self._produced = 0
        self._current = 0
        self._following = 1

    def __iter__(self) -> FibonacciIterator:
        """Возвращает сам объект — так устроен протокол итератора."""
        return self

    def __next__(self) -> int:
        """Возвращает следующее число или бросает StopIteration."""
        if self._produced >= self._count:
            raise StopIteration
        value = self._current
        self._current, self._following = (
            self._following, self._current + self._following)
        self._produced += 1
        return value

    def __repr__(self) -> str:
        """Техническое представление с состоянием итератора."""
        return (f"FibonacciIterator(count={self._count}, "
                f"produced={self._produced})")


def demo() -> None:
    """Демонстрация протокола итератора на числах Фибоначчи."""
    count = 10
    iterator = FibonacciIterator(count)
    print(f"Создан {iterator!r}")
    print(f"iter(it) is it: {iter(iterator) is iterator} "
          "- объект сам является итератором")
    print(f"Первые {count} чисел через for: ", end="")
    print(" ".join(str(number) for number in iterator))
    print(f"После обхода итератор исчерпан: list(it) = {list(iterator)}")
    fresh = FibonacciIterator(10)
    print("Ручной вызов next() на новом итераторе:", next(fresh),
          next(fresh), next(fresh))
    print(f"sum(FibonacciIterator(10)) = {sum(FibonacciIterator(10))} "
          "- итератор работает со встроенными функциями")
    print("Попытка создать FibonacciIterator(-5):")
    try:
        FibonacciIterator(-5)
    except ValueError as error:
        print(f"  Ошибка: {error}")


def main() -> None:
    """Точка входа: N из аргумента или демонстрация."""
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
            numbers = list(FibonacciIterator(count))
        except ValueError as error:
            print(f"Ошибка: {error}")
            sys.exit(1)
        print(f"Первые {count} чисел Фибоначчи: {numbers}")
    else:
        demo()


if __name__ == "__main__":
    main()
