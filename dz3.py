import json
import argparse
import re


class ConfigParser:
    def __init__(self):
        self.data = {}

    def parse(self, lines):
        """Главный метод парсинга."""
        lines_iterator = iter(lines)
        for line in lines_iterator:
            line = line.strip()
            if line.startswith("table(["):
                key, value = self.parse_table(line, lines_iterator)
                self.data[key] = value
            elif ":" in line:
                key, value = self.parse_constant(line)
                self.data[key] = value
            elif line.startswith(";"):
                # Игнорировать комментарии
                continue
            elif not line:  # Пропускаем пустые строки
                continue
            else:
                raise SyntaxError(f"Неизвестная строка: {line}")
        return self.data

    def parse_constant(self, line):
        """Парсинг констант."""
        key, value = map(str.strip, line.split(":", 1))
        return key, self.evaluate_value(value)

    def parse_table(self, line, lines_iterator):
        """Парсинг конструкции table с поддержкой многострочных словарей."""
        if not line.startswith("table(["):
            raise SyntaxError(f"Некорректный синтаксис словаря: {line.strip()}")

        content = line[len("table(["):].strip()
        result_lines = []

        # Считываем до закрывающей скобки "])"
        while not content.endswith("])"):
            result_lines.append(content)
            try:
                content = next(lines_iterator).strip()
            except StopIteration:
                raise SyntaxError("Не найдено закрывающей скобки для table.")

        # Добавляем последнюю строку (с "])") без нее самой
        result_lines.append(content[:-2].strip())

        # Объединяем строки и парсим пары ключ=значение
        content = " ".join(result_lines)
        pairs = [pair.strip() for pair in content.split(",") if pair.strip()]

        result = {}
        for pair in pairs:
            if "=" not in pair:
                raise SyntaxError(f"Ошибка в паре ключ=значение: {pair.strip()}")
            key, value = map(str.strip, pair.split("=", 1))
            result[key] = self.evaluate_value(value)

        return "table", result

    def evaluate_value(self, value):
        """Анализирует значение и возвращает соответствующий объект."""
        value = value.strip()
        if value.isdigit():
            return int(value)
        if value.startswith("{") and value.endswith("}"):
            return self.parse_array(value)
        if value.startswith("table([") and value.endswith("])"):
            return self.parse_table(value, iter([]))  # Пустой итератор для однострочного словаря
        return value

    def parse_array(self, value):
        """Парсинг массива."""
        if not value.startswith("{") or not value.endswith("}"):
            raise SyntaxError(f"Некорректный синтаксис массива: {value}")
        elements = [el.strip() for el in value[1:-1].split(".") if el.strip()]
        return elements


import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Парсер конфигурационного языка.")
    parser.add_argument("--input", required=True, help="Путь к входному файлу.")
    args = parser.parse_args()

    try:
        # Читаем файл построчно
        with open(args.input, "r", encoding="utf-8") as file:
            content = file.readlines()

        # Создаем экземпляр ConfigParser и обрабатываем данные
        config_parser = ConfigParser()
        parsed_data = config_parser.parse(content)

        # Выводим результат в формате JSON
        print(json.dumps(parsed_data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
