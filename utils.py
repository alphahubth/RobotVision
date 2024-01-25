import time

def get_current_time():
    current_time = time.localtime()
    formatted_time = time.strftime('%Y-%m-%d-%H-%M-%S', current_time)
    microseconds = int((time.time() % 1) * 1e6)
    return f"{formatted_time}-{microseconds:06d}"


def get_current_sec():
    current_time = time.localtime()
    formatted_time = time.strftime('%Y-%m-%d-%H-%M-%S', current_time)
    return f"{formatted_time}"


def get_current_date():
    current_time = time.localtime()
    formatted_time = time.strftime('%Y-%m-%d', current_time)
    return f"{formatted_time}"


