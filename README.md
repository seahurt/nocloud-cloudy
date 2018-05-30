# nocloud-cloudy

# First step: prepare your server
```
# Ubuntu
1. sudo apt install qemu-kvm libvirt-bin bridge-utils virt-manager virtinst virt-viewer
2. vim /etc/network/interfaces # 配置网卡为桥接网络，桥接网卡名设为为br0, 然后重启网络
3. 找一个目标文件夹比如：/kvm/,创建子目录cloud-images, metadata, vms
4. 下载ubuntu和centos的云镜相，放入cloud-img中，分别改名为ubuntu.base.img, centos.base.img。下载链接为
centos 7: http://mirrors.ustc.edu.cn/centos-cloud/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2
ubuntu 16.04: http://mirrors.ustc.edu.cn/ubuntu-cloud-images/xenial/current/xenial-server-cloudimg-amd64-disk1.img
5. Done
```
```
# Centos
1. sudo yum install qemu-kvm libvirt virt-install bridge-utils virt-manager
2. vim /etc/sysconfig/network-scripts/ifcfg-br0
3. vim /etc/sysconfig/network-scripts/ifcfg-eth0(也可能叫其它名字)
4. 找一个目标文件夹比如：/kvm/,创建子目录cloud-images, metadata, vms
5. 下载ubuntu和centos的云镜相，放入cloud-img中，分别改名为ubuntu.base.img, centos.base.img。下载链接为
centos 7: http://mirrors.ustc.edu.cn/centos-cloud/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2
ubuntu 16.04: http://mirrors.ustc.edu.cn/ubuntu-cloud-images/xenial/current/xenial-server-cloudimg-amd64-disk1.img
6. Done
```

# Config
```
更改system/settings.py里面的信息，主要更改的有BASE_URL和NETWORK_ID
```

# Setup Web Server
```
git clone <this repo>
cd nocloud-cloudy
pip install -r requirements.txt
sudo python run.py  # 需要用root权限，或者将当前用户添加到libvirtd组中
```

# Useage
```
Visit http://<your-ip>:8888
``` 

# Debug
```
ubuntu的cloud镜相默认名为
```