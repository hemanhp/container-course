import os
import ctypes

libc = ctypes.CDLL('libc.so.6', use_errno=True)

CLONE_NEWNS = 	0x00020000



def unsharens(flag):
    result = libc.unshare(flag)

    if result<0:
        err_no = ctypes.get_errno()
        print(err_no)




def run():
    pid = os.fork()

    if pid==0:
        unsharens(CLONE_NEWNS)
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
