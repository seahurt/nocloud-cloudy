from system import settings

def img_path(name):
    return settings.IMG_PATH.format(name=name)

def createImg(name, ostype, disk):
    if ostype == 'ubuntu':
        baseimg = settings.Ubuntu
    elif ostype == 'centos':
        baseimg = settings.CentOS
    else:
        return False
    new_img_path = img_path(name)
    return settings.IMG_CMD.format(baseimg_path=baseimg,
                                   new_img_path=new_img_path,
                                   disk_size=disk)
