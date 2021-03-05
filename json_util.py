import json


def save_file(items, path):
    with open(path, 'w', newline='', encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False)


def open_file(path):
    with open(path, encoding="utf-8") as json_file:
        dm = json.load(json_file)
        return dm
