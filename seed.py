#! python
import sys
import os
import re

iso_cmd = '/usr/bin/genisoimage -output {name}.seed.iso -volid cidata -joliet -rock {userdata} {metadata}'

img_cmd = '/usr/bin/qemu-img create -f qcow2 -b {baseimg} {name}.img {disk}'

virt_cmd = '/usr/bin/virt-install --import --name={name} --ram={mem} \
--vcpus={cpu} --disk /cifs/webvirtmgr/vms/{name}.img,format=qcow2,bus=virtio \
--disk /cifs/webvirtmgr/vms/{name}.seed.iso,device=cdrom \
--network bridge=br0,model=virtio \
--os-type=linux --os-variant={osvar} \
--noautoconsole '

# kvm_cmd = 'kvm -m {mem} -smp 2 \
# -drive file={disk},if=virtio,cache=none,aio=native \
# -drive file={meta},if=virtio \
# -net nic,vlan=0,model=virtio,macaddr={mac} \
# -nographic -curses'

usage = '''
Usage: python3 {bin} <ip: 20~50> <prefix> <type: ubuntu|centos> [<cpu: 1> <mem: 1024(mb)> <disk: 10G>]
'''
# <disk size: 10G> <cpu: 1> <mem: 1024m>
ubuntu_base_img = '/cifs/webvirtmgr/cloud-images/ubuntu.base.img'
centos_base_img = '/cifs/webvirtmgr/cloud-images/centos.base.img'


if(len(sys.argv) < 4):
    sys.exit(usage.format(bin=sys.argv[0]))

ip = sys.argv[1]

prefix = sys.argv[2]

img_type = sys.argv[3].lower()
if img_type not in ['ubuntu', 'centos']:
    sys.exit('Image type should only be ubuntu or centos')

baseimg = ubuntu_base_img if img_type == 'ubuntu' else centos_base_img
osvar = 'Ubuntu16.04' if img_type == 'ubuntu' else 'CentOS7.0'

cpu = '1'
mem = '1024'
disk = '10G'

try:
    cpu = sys.argv[4]
    mem = sys.argv[5]
    disk = sys.argv[6]
except IndexError:
    pass


# size = sys.argv[4]

# cpu = sys.argv[5]

# mem = sys.argv[6]
interface_name = 'ens3' if img_type == 'ubuntu' else 'eth0'

user_data_file = '/cifs/webvirtmgr/metadata/user-data'
meta_data_file = '/cifs/webvirtmgr/metadata/meta-data'

with open(user_data_file, 'w') as uf:
    uf.write('#cloud-config\n')
    uf.write('password: gm2018\n')
    uf.write('ssh_pwauth: True\n')

with open(meta_data_file, 'w') as mf:
    mf.write('instance-id: iid-local01\n')
    mf.write('network-interfaces: |\n')
    mf.write('  auto %s\n' % interface_name)
    mf.write('  iface %s inet static\n' % interface_name)
    mf.write('  address 172.17.50.%s\n' % ip)
    mf.write('  network 172.17.50.0\n')
    mf.write('  broadcast 172.17.50.255\n')
    mf.write('  netmask 255.255.255.0')
    mf.write('  gateway 172.17.50.1\n')
    mf.write('  dns-nameservers 114.114.114.114, 223.5.5.5\n')

name = '.'.join([prefix, img_type, str(ip)])
os.chdir('/cifs/webvirtmgr/vms')
os.system(iso_cmd.format(name=name, userdata=user_data_file, metadata=meta_data_file))
os.system(img_cmd.format(baseimg=baseimg, name=name, disk=disk))
os.system(virt_cmd.format(name=name, osvar=osvar, mem=mem, cpu=cpu))
print('Done')

