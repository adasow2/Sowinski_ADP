from src.app import KugisApp
from src.create_window import create_window


def main_window():
    window = create_window()
    KugisApp(window)
    window.mainloop()


if __name__ == "__main__":
    main_window()