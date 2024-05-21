import os
import ast

def find_imports_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return imports

def scan_project_for_imports(project_path):
    all_imports = set()
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imports = find_imports_in_file(file_path)
                all_imports.update(imports)
    return all_imports

def write_requirements_txt(imports, output_file='requirements.txt'):
    with open(output_file, 'w', encoding='utf-8') as file:
        for imp in sorted(imports):
            file.write(f"{imp}\n")

def main():
    project_path = os.path.dirname(os.path.abspath(__file__))
    all_imports = scan_project_for_imports(project_path)
    write_requirements_txt(all_imports)

if __name__ == '__main__':
    main()