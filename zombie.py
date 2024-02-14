import os
import time


def create_zombie():
    pid = os.fork()

    if pid == 0:
        print("Child process created with PID:", os.getpid())
        exit(0)
    else:
        print("Parent process with PID:", os.getpid())
        time.sleep(30)
        print("Parent process after sleeping")


if __name__ == "__main__":
    create_zombie()