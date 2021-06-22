def log(message, level = 1):
    if level == 1:
        print("[LOG]::> {}".format(message))
    elif level == 2:
        print("[WARNING]::> {}".format(message))
    else:
        print("[FATAL]::> {}".format(message))
        
    return