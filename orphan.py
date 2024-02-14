import os
import time


def create_orphan():

    pid = os.fork()

    if pid == 0:
        print("Child process created with PID:", os.getpid())
        time.sleep(30)
        print("Child process exiting")
    else:
        print("Parent process with PID:", os.getpid())
        time.sleep(10)
        exit(0)


if __name__ == "__main__":
    create_orphan()