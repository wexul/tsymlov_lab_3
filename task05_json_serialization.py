"""Задание 5 (повышенная сложность): класс для сериализации в JSON.

JsonSerializable — класс-примесь: наследнику достаточно реализовать
to_dict() и from_dict(), а сериализация в строку (to_json/from_json)
и в файл (save/load) он получает готовой. Демонстрация на классе
Student: объект -> JSON -> объект (round-trip) и сохранение списка
объектов в файл с последующей загрузкой.

Запуск:
    python task05_json_serialization.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Self


class JsonSerializable:
    """Примесь: сериализация объекта в JSON через to_dict/from_dict."""

    def to_dict(self) -> dict[str, Any]:
        """Возвращает словарь с данными объекта (у наследников)."""
        raise NotImplementedError(
            "to_dict() должен быть переопределён в наследнике")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Создаёт объект из словаря (у наследников)."""
        raise NotImplementedError(
            "from_dict() должен быть переопределён в наследнике")

    def to_json(self, *, indent: int | None = None) -> str:
        """Сериализует объект в JSON-строку (кириллица не экранируется)."""
        return json.dumps(self.to_dict(), ensure_ascii=False,
                          indent=indent)

    @classmethod
    def from_json(cls, text: str) -> Self:
        """Восстанавливает объект из JSON-строки."""
        try:
            data = json.loads(text)
        except json.JSONDecodeError as error:
            raise ValueError(f"некорректный JSON: {error}") from error
        if not isinstance(data, dict):
            raise ValueError("JSON должен содержать объект (словарь), "
                             f"получен {type(data).__name__}")
        return cls.from_dict(data)

    def save(self, path: str | Path) -> None:
        """Сохраняет объект в JSON-файл."""
        Path(path).write_text(self.to_json(indent=2),
                              encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> Self:
        """Загружает объект из JSON-файла."""
        file_path = Path(path)
        if not file_path.is_file():
            raise FileNotFoundError(f"файл не найден: {file_path}")
        return cls.from_json(file_path.read_text(encoding="utf-8"))


class Student(JsonSerializable):
    """Студент: ФИО, группа, список оценок. Поддерживает JSON."""

    def __init__(self, full_name: str, group: str,
                 grades: list[int] | None = None) -> None:
        if not full_name.strip():
            raise ValueError("ФИО не может быть пустым")
        if not group.strip():
            raise ValueError("группа не может быть пустой")
        for grade in grades or []:
            if not isinstance(grade, int) or not 2 <= grade <= 5:
                raise ValueError(f"оценка должна быть целым числом "
                                 f"от 2 до 5, получено {grade!r}")
        self.full_name = full_name
        self.group = group
        self.grades = list(grades or [])

    def average_grade(self) -> float | None:
        """Средний балл или None, если оценок нет."""
        if not self.grades:
            return None
        return sum(self.grades) / len(self.grades)

    def to_dict(self) -> dict[str, Any]:
        """Преобразует студента в словарь для JSON."""
        return {"full_name": self.full_name, "group": self.group,
                "grades": self.grades}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Student:
        """Создаёт студента из словаря с проверкой полей."""
        try:
            return cls(full_name=data["full_name"],
                       group=data["group"],
                       grades=data.get("grades", []))
        except KeyError as error:
            raise ValueError(
                f"в данных нет обязательного поля {error}") from error

    def __eq__(self, other: object) -> bool:
        """Студенты равны, если совпадают все поля."""
        if not isinstance(other, Student):
            return NotImplemented
        return (self.full_name == other.full_name
                and self.group == other.group
                and self.grades == other.grades)

    def __repr__(self) -> str:
        """Техническое представление студента."""
        return (f"Student({self.full_name!r}, {self.group!r}, "
                f"{self.grades!r})")


def demo() -> None:
    """Демонстрация round-trip сериализации и работы с файлом."""
    student = Student("Полошков Ярослав Витальевич", "220042-11",
                      [5, 4, 5])
    print("Исходный объект:", student)
    text = student.to_json(indent=2)
    print("Объект -> JSON:")
    print(text)
    restored = Student.from_json(text)
    print("JSON -> объект:", restored)
    print(f"Round-trip: restored == student -> {restored == student}")

    path = Path("students_demo.json")
    group = [student, Student("Иванов Иван Иванович", "220042-11")]
    path.write_text(
        json.dumps([item.to_dict() for item in group],
                   ensure_ascii=False, indent=2),
        encoding="utf-8")
    loaded = [Student.from_dict(item)
              for item in json.loads(path.read_text(encoding="utf-8"))]
    print(f"Список из {len(group)} студентов сохранён в {path} "
          f"и загружен обратно: {loaded == group}")
    path.unlink()
    print(f"Временный файл {path} удалён.")

    print("Попытка разобрать битый JSON '{not json}':")
    try:
        Student.from_json("{not json}")
    except ValueError as error:
        print(f"  Ошибка: {error}")


if __name__ == "__main__":
    demo()
