import os
import ctypes

libc = ctypes.CDLL('libc.so.6', use_errno=True)

CLONE_NEWNS = 	0x00020000
CLONE_NEWUTS = 	0x04000000
CLONE_NEWPID =	0x20000000
CLONE_NEWCGROUP	=	0x02000000
CLONE_NEWNET=	0x40000000


BASE_DIR="/home/vagrant/ubuntu"
WORK_DIR="/home/vagrant/work"
UPPER_DIR="/home/vagrant/upper"
ROOT_FS = '/home/vagrant/uroot'


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


def create_memory_group():
    base_dir = '/sys/fs/cgroup/memory'
    cd_dir = os.path.join(
        base_dir, "front")

    if not os.path.exists(cd_dir):
        os.makedirs(cd_dir)
    tasks_file = os.path.join(cd_dir, 'tasks')
    open(tasks_file, 'w').write(str(os.getpid()))

    mem_limit_in_bytes_file = os.path.join(
        cd_dir, 'memory.limit_in_bytes')
    open(mem_limit_in_bytes_file, 'w').write(str(512 * 1024 * 1024))


def child_func(stack):

    # os.system(f"cp -r /home/vagrant/ubuntu {ROOT_FS}")
    os.system(f"mount -t overlay -o lowerdir={BASE_DIR},upperdir={UPPER_DIR},workdir={WORK_DIR} overlay {ROOT_FS}")
    create_memory_group()
    set_hostname("front")
    os.system(f"mount -t proc none {ROOT_FS}/proc")
    os.system(f"mount -t sysfs sysfs {ROOT_FS}/sys")
    os.system(f"mount -t tmpfs none  {ROOT_FS}/tmp")
    os.chroot(f"{ROOT_FS}")
    os.chdir("/")
    os.execvp('/bin/bash', ['/bin/bash'])

def run():


    child_func_type = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
    child_func_c = child_func_type(child_func)

    stack = ctypes.c_void_p(libc.sbrk(0))


    pid = libc.clone(child_func_c, stack, CLONE_NEWNS | CLONE_NEWPID| CLONE_NEWUTS |CLONE_NEWCGROUP|CLONE_NEWNET| 17 )
    _, status = os.waitpid(pid, 0)




if __name__ == '__main__':
    run()
