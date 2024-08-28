DEBUG = False

def debug(*args, force=False, **kwargs):
    if DEBUG or force:
        print(*args, **kwargs)
