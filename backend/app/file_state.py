ACTIVE_FILE = None


def set_active_file(filename: str):
    global ACTIVE_FILE
    ACTIVE_FILE = filename


def get_active_file():
    return ACTIVE_FILE