import os


def run():
    pid = os.fork()

    if pid==0:
        os.execvp('/bin/bash',['/bin/bash'])
    else:
        rid, status = os.waitpid(pid, 0)
        print(rid, status)


if __name__ == '__main__':
    run()
