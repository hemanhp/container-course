import os


def run():
    pid = os.fork()

    if pid==0:
        os.system("mount -t proc none /vagrant/myroot/proc ")
        os.chroot("/vagrant/myroot")
        os.chdir("/")
        os.execvp('/bin/busybox',['/bin/busybox', 'sh'])
    else:
        rid, status = os.waitpid(pid, 0)
        os.system("umount /vagrant/myroot/proc ")
        print(rid, status)


if __name__ == '__main__':
    run()
