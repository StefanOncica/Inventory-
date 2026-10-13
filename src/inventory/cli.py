from inventory import storage

FIELD_TYPES = {
    "text": str,
    "int": int,
    "float": float,
    "bool": lambda s: s.strip().lower() in ("y", "yes", "true", "1"),
}

def prompt(message: str) -> str:
    return input(message).strip()

def choose(options: list[str]) -> int | None:
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    choice = prompt("> ")
    if choice.isdigit() and 1 <= int(choice) <= len(options):
        return int(choice) - 1
    print("Invalid choice.")
    return None

def read_value(field: dict, current=None):
    hint = f" [{current}]" if current is not None else ""
    while True:
        raw = prompt(f"{field['name']} ({field['type']}){hint}: ")
        if raw == "" and current is not None:
            return current
        try:
            return FIELD_TYPES[field["type"]](raw)
        except ValueError:
            print(f"Expected a value of type {field['type']}.")

def add_field(data: dict) -> None:
        name = prompt("Field name: ")
        if not name:
            return
        if any(f["name"] == name for f in data["fields"]):
            print(f"Field '{name}' already exists.")
            return
        print("Field type:")
        types = list(FIELD_TYPES)
        idx = choose(types)
        if idx is None:
            return
        data["fields"].append({"name": name, "type": types[idx]})
        for item in data["items"]:
            item.setdefault(name, None)
        print(f"Added field '{name}'.")

def remove_field(data: dict) -> None:
    if not data["fields"]:
        print("No fields defined.")
        return
    print("Remove which field?")
    idx = choose([f["name"] for f in data["fields"]])
    if idx is None:
        return
    name = data["fields"].pop(idx)["name"]
    for item in data["items"]:
        item.pop(name, None)
    print(f"Removed field '{name}'.")

def show_fields(data: dict) -> None:
    if not data["fields"]:
        print("No fields defined.")
    for f in data["fields"]:
        print(f"  - {f['name']} ({f['type']})")

def add_item(data: dict) -> None:
    if not data["fields"]:
        print("Define some fields first.")
        return
    item = {f["name"]: read_value(f) for f in data["fields"]}
    data["items"].append(item)
    print("Item added.")

def list_items(data: dict) -> None:
    if not data["items"]:
        print("Inventory is empty.")
        return
    names = [f["name"] for f in data["fields"]]
    rows = [[str(item.get(n, "")) for n in names] for item in data["items"]]
    widths = [max(len(n), *(len(r[i]) for r in rows)) for i, n in enumerate(names)]
    print("#   " + "  ".join(n.ljust(w) for n, w in zip(names, widths)))
    for i, row in enumerate(rows, 1):
        print(f"{i:<3} " + "  ".join(v.ljust(w) for v, w in zip(row, widths)))

def pick_item(data: dict) -> int | None:
        list_items(data)
        if not data["items"]:
            return None
        choice = prompt("Item number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(data["items"]):
            return int(choice) - 1
        print("Invalid item number.")
        return None

def edit_item(data: dict) -> None:
    idx = pick_item(data)
    if idx is None:
        return
    item = data["items"][idx]
    print("Press Enter to keep the current value.")
    for f in data["fields"]:
        item[f["name"]] = read_value(f, item.get(f["name"]))
    print("Item updated.")

def delete_item(data: dict) -> None:
    idx = pick_item(data)
    if idx is None:
        return
    data["items"].pop(idx)
    print("Item deleted.")

MENU = [
    ("Show fields", show_fields),
    ("Add field", add_field),
    ("Remove field", remove_field),
    ("Add item", add_item),
    ("List items", list_items),
    ("Edit item", edit_item),
    ("Delete item", delete_item),
]


def run() -> None:
    data = storage.load()
    print(f"Inventory loaded from {storage.DEFAULT_PATH}")
    while True:
        print("\nWhat would you like to do?")
        idx = choose([label for label, _ in MENU] + ["Save and quit"])
        if idx is None:
            continue
        if idx == len(MENU):
            break
        MENU[idx][1](data)
        storage.save(data)
    storage.save(data)
    print("Saved. Bye!")
