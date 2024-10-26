import os

def print_tree(directory, prefix="", level=0, max_level=2):
    if level > max_level:
        return

    # Ignore specific directories you do not want to display
    ignored_dirs = {'__pycache__', '.git', 'migrations'}
    ignored_extensions = {'.pyc', '.dist-info'}

    print(prefix + os.path.basename(directory) + "/")
    items = os.listdir(directory)
    items = [item for item in items if os.path.basename(os.path.join(directory, item)) not in ignored_dirs]

    for index, item in enumerate(items):
        path = os.path.join(directory, item)

        # Skip ignored files based on extensions
        if os.path.isfile(path) and any(path.endswith(ext) for ext in ignored_extensions):
            continue

        connector = "├── " if index < len(items) - 1 else "└── "
        if os.path.isdir(path):
            print_tree(path, prefix + ("│   " if connector == "├── " else "    "), level + 1, max_level)
        else:
            print(prefix + connector + item)

# Change the path below to match your directory path
print_tree("C:/Users/ASUS/Downloads/GolekMakanRek", max_level=2)
