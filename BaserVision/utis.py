import time

def get_current_time():
    current_time = time.localtime()
    formatted_time = time.strftime('%Y-%m-%d-%H-%M-%S', current_time)
    microseconds = int((time.time() % 1) * 1e6)
    return f"{formatted_time}-{microseconds:06d}"