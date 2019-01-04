from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        ordering = ['id']


class Host(models.Model):
    name = models.CharField()
    cpu = models.PositiveSmallIntegerField('Total CPU Core', default=1)
    cpu_available = models.PositiveSmallIntegerField('Total CPU Core', default=0)
    mem = models.PositiveIntegerField('Total Memory Size(MB)', default=1024)
    mem_available = models.PositiveIntegerField('Total Memory Size(MB)', default=0)
    disk = models.PositiveIntegerField('Total Disk Size(GB)', default=10)
    disk_available = models.PositiveIntegerField('Total Disk Size(GB)', default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)


class Vhost(models.Model):
    name = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    ssh_key = models.TextField(blank=True, null=True)
    cpu = models.PositiveSmallIntegerField('CPU Core', default=1)
    mem = models.PositiveIntegerField('Memory Size (MB)', default=1024)
    disk_size = models.PositiveIntegerField('Disk Size (GB)', default=10)
    password_expire = models.BooleanField('Passreset on First Boot', default=False)
    hostname = models.CharField(max_length=30, default='localhost')
    dns1 = models.IPAddressField(default='114.114.114.114')
    dns2 = models.IPAddressField(default='223.5.5.5')
    status = models.CharField(max_length=15)  # created, start, shutdown, restart
    host = models.ForeignKey(Host, on_delete=models.PROTECT)
    image = models.ForeignKey('Images', on_delete=models.PROTECT)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def vm_dir(self):
        return os.path.join(settings.VMDIR, self.name)

    @property
    def meta_dir(self):
        return os.path.join(self.vm_dir, 'metadata')

    @property
    def user_data(self):
        return os.path.join(self.meta_dir, 'user-data')

    @property
    def meta_data(self):
        return os.path.join(self.meta_dir, 'meta-data')

    def create(self):
        self.create_meta_data()
        self.create_user_data()
        self.create_seed()
        self.create_disk()
        cmds = ['/usr/bin/virt-install', '--import', '--noautoconsole',
                f'--name={self.name}',
                f'--ram={self.mem}',
                f'--vcpus={self.cpu}',
                f'--disk {self.disk_img_file},format=qcow2,bus=virtio',
                f'--disk {self.seed_iso},device=cdrom',
                f'--network bridge=br0,model=virtio',
                f'--os-type=linux',
                f'--os-variant="{self.image.os_var}"',
                ]
        cmd = ' '.join(cmds)
        os.system(cmd)

    @property
    def default_interface(self):
        return self.interface_set.get(default=True)

    @property
    def default_ip(self):
        return self.default_interface.ip

    def create_meta_data(self):
        os.makedirs(self.meta_dir)
        with open(self.meta_data, 'w') as f:
            f.write('instance-id: iid-local01')
            f.write("network-interfaces: |")
            f.write(f"  auto {self.image.interface_name}")
            f.write(f"  iface {self.image.interface_name} inet static")
            f.write(f"  address {self.default_ip.address}")
            f.write(f"  network {self.default_ip.network}")
            f.write(f"  netmask {self.default_ip.mask}")
            f.write(f"  gateway {self.default_ip.gateway}")
            f.write(f"  broadcast {self.default_ip.broadcast}")
            f.write(f"  dns-nameservers {self.dns1}, {self.dns2}")
            f.write(f"hostname: {self.hostname}")

    def create_user_data(self):
        os.makedirs(self.meta_dir)
        with open(self.user_data, 'w') as f:
            f.write('#cloud-config')
            f.write(f'password: {self.password}')
            f.write(f"chpasswd: {{ expire: {self.password_expire} }}")
            f.write("ssh_pwauth: True")
            if self.ssh_key:
                f.write('ssh_authorized_keys:')
                f.write(f'  - {self.ssh_key}')

    def disk_img_file(self):
        return os.path.join(self.vm_dir, f'{self.name}.img')

    def create_disk(self):
        cmd = f'/usr/bin/qemu-img create -f qcow2 -b {self.image.image_path} {self.disk_img_file} {self.disk_size}'
        os.system(cmd)

    @property
    def seed_iso(self):
        return os.path.join(self.vm_dir, 'seed.iso')

    def create_seed(self):
        cmd = f'/usr/bin/genisoimage -output {self.seed_iso} -volid cidata -joliet -rock {self.meta_data} {self.user_data}'
        os.system(cmd)


class Images(models.Model):
    os_type = models.CharField(max_length=15)
    os_version = models.CharField(max_length=20)
    os_var = models.CharField(max_length=30)
    image_path = models.FilePathField()
    username = models.CharField(max_length=30)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    image_type = models.CharField(max_length=20, default='cloud_image')  # iso, cloud_image, raw_image
    interface_name = models.CharField(max_length=30)


class IP(models.Model):
    address = models.IPAddressField(unique=True)
    mask = models.IPAddressField(default='255.255.255.0')
    gateway = models.IPAddressField()
    network = models.IPAddressField()
    broadcast = models.IPAddressField()
    pool = models.ForeignKey('IPPool', on_delete=models.CASCADE)
    interface = models.OneToOneField('Interface', on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)


class IPPool(models.Model):
    mask = models.IPAddressField(default='255.255.255.0')
    network = models.IPAddressField()
    ip_start = models.PositiveSmallIntegerField(default=1)
    ip_end = models.PositiveSmallIntegerField(default=254)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)


class Interface(models.Model):
    mac = models.CharField(max_length=17, unique=True, null=True)
    vhost = models.ForeignKey('Vhost', on_delete=models.CASCADE, null=True)
    host = models.ForeignKey('Vhost', on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    default = models.BooleanField()