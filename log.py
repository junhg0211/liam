from datetime import datetime


def message(*args, **kwargs):
    print(datetime.now(), *args, **kwargs)
