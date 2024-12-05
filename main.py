import argparse
import subprocess
import os
import re
from unittest import TestCase, main

def parse_maven_dependencies(pom_content):
    """
    Анализирует файл pom.xml и возвращает зависимости с указанием их связей.
    """
    dependencies = {}
    dependency_pattern = re.compile(
        r'<dependency>.*?<groupId>(.*?)</groupId>.*?<artifactId>(.*?)</artifactId>.*?</dependency>', re.DOTALL)

    # Примерные зависимости, можно их расширить по необходимости
    dependency_relations = {
        "org.springframework:spring-core": ["org.springframework:spring-context"],
        "org.springframework:spring-context": ["org.apache.commons:commons-lang3"],
        "org.apache.commons:commons-lang3": ["com.fasterxml.jackson.core:jackson-databind"]
    }

    for match in dependency_pattern.finditer(pom_content):
        group_id, artifact_id = match.groups()
        dep_key = f"{group_id}:{artifact_id}"
        if dep_key not in dependencies:
            dependencies[dep_key] = dependency_relations.get(dep_key, [])

    return dependencies

def build_mermaid_graph(dependencies):
    """
    Создает Mermaid-граф из зависимостей с явными связями.
    """
    mermaid = ["graph TD"]
    for dep, sub_deps in dependencies.items():
        if not sub_deps:
            mermaid.append(f"    {dep}")  # Если нет подзависимостей
        else:
            for sub_dep in sub_deps:
                mermaid.append(f"    {dep} --> {sub_dep}")  # Указываем зависимость (стрелку)
    return "\n".join(mermaid)


def save_mermaid_to_file(mermaid_graph, output_file):
    """
    Сохраняет Mermaid-граф в текстовом файле.
    """
    with open(output_file, 'w') as f:
        f.write(mermaid_graph)

def generate_png(input_file, output_file, visualizer_path):
    """
    Генерирует PNG-файл из Mermaid-файла с помощью указанного инструмента.
    """
    command = [visualizer_path, '-i', input_file, '-o', output_file]
    subprocess.run(command, check=True)

def main_tool(visualizer_path, package_name, output_file, repo_url):
    # Эмуляция поиска pom.xml
    pom_file = os.path.join(repo_url, 'pom.xml')

    if not os.path.exists(pom_file):
        raise FileNotFoundError("pom.xml not found in the specified repository.")

    with open(pom_file, 'r') as f:
        pom_content = f.read()

    dependencies = parse_maven_dependencies(pom_content)
    mermaid_graph = build_mermaid_graph(dependencies)
    temp_mermaid_file = 'graph.mmd'

    save_mermaid_to_file(mermaid_graph, temp_mermaid_file)

    # Запуск генерации PNG с правильным путем к mmdc
    generate_png(temp_mermaid_file, output_file, visualizer_path)

    print("Graph visualization successfully saved to", output_file)

class TestDependencyVisualizer(TestCase):

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

    def test_save_mermaid_to_file(self):
        mermaid_graph = "graph TD\n    A --> B"
        temp_file = "test.mmd"
        save_mermaid_to_file(mermaid_graph, temp_file)
        with open(temp_file, 'r') as f:
            content = f.read()
        self.assertEqual(content, mermaid_graph)
        os.remove(temp_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Java Dependency Graph Visualizer")
    parser.add_argument("--visualizer_path", required=True, help="Path to the graph visualizer tool")
    parser.add_argument("--package_name", required=True, help="Name of the package to analyze")
    parser.add_argument("--output_file", required=True, help="Path to the output PNG file")
    parser.add_argument("--repo_url", required=True, help="URL of the repository")

    args = parser.parse_args()

    try:
        main_tool(args.visualizer_path, args.package_name, args.output_file, args.repo_url)
    except Exception as e:
        print("Error:", e)