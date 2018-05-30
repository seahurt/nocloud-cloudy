from .img import *
from .seed import *
from .vm import *


def makeCmd(ip, dns, mem, cpu, disk, hostname, name, passwd, expire, sshkey, ostype):
    from backend.img import createImg
    from backend.seed import createSeed
    from backend.vm import createVM
    seed_cmd = createSeed(name=name, ip=ip, dns=dns, passwd=passwd, expire=expire, sshkey=sshkey, hostname=hostname, ostype=ostype)
    img_cmd = createImg(name=name, disk=disk, ostype=ostype)
    vm_cmd = createVM(name=name, mem=mem, cpu=cpu, ostype=ostype)
    return ' && '.join([seed_cmd, img_cmd, vm_cmd, 'echo Done'])

