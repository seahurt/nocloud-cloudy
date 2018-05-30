from system import settings


def img_path(name):
    return settings.IMG_PATH.format(name=name)


def createImg(name, ostype, disk):
    ostarget = settings.IMG_MAP.get(ostype)
    if not ostarget:
        raise ValueError('OStype %s not supported!' % ostype)
    new_img_path = img_path(name)
    return settings.IMG_CMD.format(baseimg_path=ostarget.get('path'),
                                   new_img_path=new_img_path,
                                   disk_size=disk)
