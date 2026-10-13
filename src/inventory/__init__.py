from inventory.cli import run


def main() -> None:
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")
