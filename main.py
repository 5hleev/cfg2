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