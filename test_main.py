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