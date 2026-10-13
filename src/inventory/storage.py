import json
from pathlib import Path

DEFAULT_PATH = Path("inventory.json")


def load(path: Path = DEFAULT_PATH) -> dict:
    if not path.exists():
        return {"fields": [], "items": []}
    with path.open() as f:
        return json.load(f)


def save(data: dict, path: Path = DEFAULT_PATH) -> None:
    with path.open("w") as f:
        json.dump(data, f, indent=2)

#- load()  returns an empty inventory the first time (no file yet),
#           otherwise reads the file.
# - save()  writes the data back. indent=2 makes the file easy to read.
# - Path("inventory.json") is relative, so the file is created in the
#   folder you run the app from.
