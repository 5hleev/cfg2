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
