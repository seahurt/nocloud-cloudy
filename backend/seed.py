#! python
import os
from system import settings


def createMeta(file, ip, dns, hostname, iface_name):
    dirf = os.path.dirname(file)
    # os.system('mkdir -p %s' % dirf)
    # with open(file, 'w') as mf:
    #     mf.write('instance-id: iid-local01\n')
    #     mf.write('network-interfaces: |\n')
    #     mf.write('  auto %s\n' % iface_name)
    #     mf.write('  iface %s inet static\n' % iface_name)
    #     mf.write('  address %s\n' % ip)
    #     mf.write('  network %s.0\n' % settings.NETWORK_ID)
    #     mf.write('  broadcast %s.255\n' % settings.NETWORK_ID)
    #     mf.write('  netmask 255.255.255.0\n')
    #     mf.write('  gateway %s.1\n' % settings.NETWORK_ID)
    #     mf.write('  dns-nameservers %s, 223.5.5.5\n' % dns)
    #     if hostname:
    #         mf.write('hostname: %s\n' % hostname)
    cmd = []
    cmd.append('mkdir -p %s' % dirf)
    cmd.append('echo "instance-id: iid-local01" >%s' % file)
    cmd.append('echo "network-interfaces: |" >>%s' % file)
    cmd.append('echo "  auto %s" >>%s' % (iface_name, file))
    cmd.append('echo "  iface %s inet static" >>%s' % (iface_name, file))
    cmd.append('echo "  address %s" >>%s' % (ip, file))
    cmd.append('echo "  network %s.0" >>%s' % (settings.NETWORK_ID,file))
    cmd.append('echo "  netmask 255.255.255.0" >>%s' % file)
    cmd.append('echo "  gateway %s.1" >>%s' % (settings.NETWORK_ID, file))
    cmd.append('echo "  broadcast %s.255" >>%s' % (settings.NETWORK_ID, file))
    cmd.append('echo "  dns-nameservers %s, 223.5.5.5" >>%s' % (dns, file))
    if hostname:
        cmd.append('echo "hostname: %s" >>%s' % (hostname, file))
    return ' && '.join(cmd)


def createUserData(file, passwd, expire, sshkey):
    cmd = []
    dirf = os.path.dirname(file)
    # os.system('mkdir -p %s' % dirf)
    cmd.append('mkdir -p %s' % dirf)
    # with open(file, 'w') as uf:
    cmd.append('echo "#cloud-config" >%s' % file)
        # uf.write('#cloud-config\n')
        # uf.write('password: %s\n' % passwd)
    cmd.append('echo "password: %s" >> %s' % (passwd, file))
    if not expire:
        cmd.append('echo "chpasswd: { expire: False }" >>%s' % file)
        # uf.write('chpasswd: { expire: False }\n')
        # uf.write('ssh_pwauth: True\n')
    cmd.append('echo "ssh_pwauth: True" >>%s' % file)
    if sshkey:
        #cmd.append('echo "users:" >>%s' % file)
        #cmd.append('echo "  - default" >>%s' % file)
        cmd.append('echo "ssh_authorized_keys:" >>%s' % file)
        cmd.append('echo "  - %s" >>%s' % (sshkey, file))
        #     uf.write('sh_authorized_keys:\n')
        #     uf.write('  - %s\n' % sshkey)
    return ' && '.join(cmd)


def createSeed(name, ip, dns='114.114.114.114', ostype='ubuntu', passwd='passw0rd', expire=True, hostname=None, sshkey=None):
    iface_name = 'ens3' if ostype == 'ubuntu' else 'eth0'
    meta_data_file = settings.META_DATA.format(name=name)
    user_data_file = settings.USER_DATA.format(name=name)
    cmd_1 = createMeta(meta_data_file, ip, dns, hostname, iface_name)
    cmd_2 = createUserData(user_data_file, passwd, expire, sshkey)
    cmd_this = settings.SEED_CMD.format(seed_path=seed_path(name),
                                        meta_data_path=meta_data_file,
                                        user_data_path=user_data_file)
    return ' && '.join([cmd_1, cmd_2, cmd_this])


def seed_path(name):
    return settings.SEED_PATH.format(name=name)
