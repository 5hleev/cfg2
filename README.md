Разработать инструмент командной строки для визуализации графазависимостей, включая транзитивные зависимости. Сторонние средства дляполучения зависимостей использовать нельзя.
Зависимости определяются по имени пакета языка Java (Maven). Дляописания графа зависимостей используется представление Mermaid.
Визуализатор должен выводить результат в виде сообщения об успешномвыполнении и сохранять граф в файле формата png.

Ключами командной строки задаются:

• Путь к программе для визуализации графов.

• Имя анализируемого пакета.

• Путь к файлу с изображением графа зависимостей.

• URL-адрес репозитория.

Все функции визуализатора зависимостей должны быть покрыты тестами.

Описание функций:

parse_maven_dependencies(pom_content) - Принимает содержимое файла pom.xml в виде строки.
Возвращает словарь, где ключи — это groupId:artifactId каждой зависимости, а значения — это список зависимостей, от которых зависит текущая зависимость (в вашей версии список всегда пустой).

build_mermaid_graph(dependencies) - Принимает словарь зависимостей, созданный функцией parse_maven_dependencies.Строит связь зависимостей в виде A --> B, если зависимости вложены (но в текущей версии кода вложенных зависимостей нет).

save_mermaid_to_file(mermaid_graph, output_file) - Сохраняет Mermaid-граф (созданный build_mermaid_graph) в файл с указанным именем.

generate_png(input_file, output_file, visualizer_path) - Использует команду Mermaid CLI (mmdc), чтобы преобразовать Mermaid-граф из файла в изображение PNG.

main_tool(visualizer_path, package_name, output_file, repo_url) - Эта функция объединяет всё вместе:
Проверяет, существует ли файл pom.xml в указанной папке repo_url.
Считывает содержимое pom.xml.
Парсит зависимости с помощью parse_maven_dependencies.
Генерирует Mermaid-граф из зависимостей с помощью build_mermaid_graph.
Сохраняет граф в файл graph.mmd с помощью save_mermaid_to_file.
Вызывает generate_png, чтобы преобразовать граф в PNG-файл.
Сообщает пользователю, что PNG-файл успешно создан.

3 функции тестов:test_parse_maven_dependencies(self);test_build_mermaid_graph(self);test_save_mermaid_to_file(self, mock_file)/

Запуск программы:python main.py --visualizer_path "путь к .cmd" --package_name "my-java-package" --output_file "папка в которую сохраним png" --repo_url "путь к репозиторию pom"

Тесты:

![image](https://github.com/user-attachments/assets/9286af45-5b47-424d-a874-3086f9dea782)

![image](https://github.com/user-attachments/assets/d18eff98-9bb5-4ea6-8d7d-7febc0cdb3cd)

![image](https://github.com/user-attachments/assets/676c8e1c-4370-4141-bc5e-d22a62f74cd4)


