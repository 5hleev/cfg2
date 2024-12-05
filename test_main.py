import unittest
from unittest.mock import patch, mock_open
import os
from main import parse_maven_dependencies, build_mermaid_graph, save_mermaid_to_file


class TestDependencyVisualizer(unittest.TestCase):

    def test_parse_maven_dependencies(self):
        pom_content = """<project><dependencies>
        <dependency>
            <groupId>org.example</groupId>
            <artifactId>example-artifact</artifactId>
        </dependency>
        </dependencies></project>"""
        result = parse_maven_dependencies(pom_content)
        self.assertEqual(result, {"org.example:example-artifact": []})

    def test_build_mermaid_graph(self):
        dependencies = {"org.example:example-artifact": []}
        result = build_mermaid_graph(dependencies)
        expected = """graph TD
    org.example:example-artifact"""
        self.assertEqual(result.strip(), expected.strip())

    @patch("builtins.open", new_callable=mock_open)
    def test_save_mermaid_to_file(self, mock_file):
        mermaid_graph = "graph TD\n    A --> B"
        temp_file = "test.mmd"
        save_mermaid_to_file(mermaid_graph, temp_file)

        # Проверяем, что файл открылся для записи
        mock_file.assert_called_with(temp_file, 'w')

        # Проверяем, что правильный контент был записан в файл
        mock_file().write.assert_called_with(mermaid_graph)


if __name__ == "__main__":
    unittest.main()