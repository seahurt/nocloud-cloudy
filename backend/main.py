import img
import seed
import vm


def makeCmd(ip, dns, mem, cpu, disk, hostname, name, passwd, expire, sshkey, ostype):
    seed_cmd = seed.createSeed(name=name, ip=ip, dns=dns, passwd=passwd, expire=expire, sshkey=sshkey, hostname=hostname)
    img_cmd = img.createImg(name=name, disk=disk, ostype=ostype)
    vm_cmd = vm.createVM(name=name, mem=mem, cpu=cpu)
    return ' && '.join([seed_cmd, img_cmd, vm_cmd, 'echo Done'])

