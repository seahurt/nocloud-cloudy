import os


BASE_URL = '/kvm/'

Ubuntu = os.path.join(BASE_URL, 'cloud-images/ubuntu.base.img')

CentOS = os.path.join(BASE_URL, 'cloud-images/centos.base.img')

INTERFACE_MAP = {
    'ubuntu': 'ens3',
    'centos': 'eth0'
}

IMG_MAP = {
    'ubuntu': {
        'path': Ubuntu,
        'version': 'Ubuntu 16.04'
    },
    'centos': {
        'path': CentOS,
        'version': 'CentOS 7.0'  # 7.5 is not in virt-install's db, so we just set 7.x to 7.0
    }
}

SEED_CMD = '/usr/bin/genisoimage -output {seed_path} -volid cidata -joliet -rock {meta_data_path} {user_data_path}'

IMG_CMD = '/usr/bin/qemu-img create -f qcow2 -b {baseimg_path} {new_img_path} {disk_size}'

VM_CMD = '/usr/bin/virt-install --import --name={name} --ram={mem} \
--vcpus={cpu} --disk {img_path},format=qcow2,bus=virtio \
--disk {seed_path},device=cdrom \
--network bridge=br0,model=virtio \
--os-type=linux --os-variant="{osvar}" \
--noautoconsole'

IMG_PATH = os.path.join(BASE_URL, 'vms/{name}.img')
SEED_PATH = os.path.join(BASE_URL, 'vms/{name}.seed.iso')


META_DATA = os.path.join(BASE_URL, 'metadata/{name}/meta-data')
USER_DATA = os.path.join(BASE_URL, 'metadata/{name}/user-data')


NETWORK_ID = '192.168.100'


DEBUG = True
