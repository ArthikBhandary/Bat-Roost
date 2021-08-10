def is_int_convertible(str):
    if not str:
        # If NULL
        return False
    try:
        int(str)
        return True
    except ValueError:
        return False
