TCSAFLUSH = 0

def tcgetattr(_):
    return [0] * 10

class error(Exception):
    pass

