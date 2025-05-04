def print_slow(str, end_line = True):
    for i in str:
        print(i, end = "")
        time.sleep(0.02)
    print() if end_line else None