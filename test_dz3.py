import unittest
from dz3 import ConfigParser


class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.parser = ConfigParser()

    def test_parse_constant(self):
        """Тест парсинга строки с константой."""
        line = "name: John"
        key, value = self.parser.parse_constant(line)
        self.assertEqual(key, "name")
        self.assertEqual(value, "John")

    def test_parse_integer_constant(self):
        """Тест парсинга числовой константы."""
        line = "age: 25"
        key, value = self.parser.parse_constant(line)
        self.assertEqual(key, "age")
        self.assertEqual(value, 25)

    def test_parse_array(self):
        """Тест парсинга массива."""
        value = "{apple.orange.banana}"
        result = self.parser.parse_array(value)
        self.assertEqual(result, ["apple", "orange", "banana"])

    def test_parse_table(self):
        """Тест парсинга словаря table."""
        lines = [
            "table([",
            "key1=value1,",
            "key2=value2",
            "])"
        ]
        key, value = self.parser.parse_table(lines[0], iter(lines[1:]))
        expected_result = {
            "key1": "value1",
            "key2": "value2"
        }
        self.assertEqual(key, "table")
        self.assertEqual(value, expected_result)

    def test_parse_complete_data(self):
        """Тест парсинга полного файла."""
        lines = [
            "name: John",
            "age: 25",
            "fruits: {apple.orange.banana}",
            "table([",
            "key1=value1,",
            "key2=value2",
            "])"
        ]
        result = self.parser.parse(lines)
        expected_result = {
            "name": "John",
            "age": 25,
            "fruits": ["apple", "orange", "banana"],
            "table": {
                "key1": "value1",
                "key2": "value2"
            }
        }
        self.assertEqual(result, expected_result)

    def test_syntax_error_unknown_line(self):
        """Тест ошибки при неизвестной строке."""
        lines = ["unknown_line"]
        with self.assertRaises(SyntaxError):
            self.parser.parse(lines)

    def test_syntax_error_invalid_table(self):
        """Тест ошибки при некорректной таблице."""
        lines = [
            "table([",
            "key1=value1,",
            "key2",
            "])"
        ]
        with self.assertRaises(SyntaxError):
            self.parser.parse(lines)

    def test_syntax_error_unclosed_table(self):
        """Тест ошибки при незакрытой таблице."""
        lines = [
            "table([",
            "key1=value1,"
        ]
        with self.assertRaises(SyntaxError):
            self.parser.parse(lines)


if __name__ == "__main__":
    unittest.main()
