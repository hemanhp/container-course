import os
import ctypes

libc = ctypes.CDLL('libc.so.6', use_errno=True)

CLONE_NEWNS = 	0x00020000
CLONE_NEWUTS = 	0x04000000
CLONE_NEWPID =	0x20000000
def unsharens(flag):
    result = libc.unshare(flag)

    if result<0:
        err_no = ctypes.get_errno()
        print(err_no)


def set_hostname(name):
    result = libc.sethostname(name.encode(), len(name))
    if result < 0:
        err_no = ctypes.get_errno()
        print(err_no)


def run():
    unsharens(CLONE_NEWPID)
    pid = os.fork()

    if pid==0:
        unsharens(CLONE_NEWNS | CLONE_NEWUTS)

        set_hostname("front")
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
