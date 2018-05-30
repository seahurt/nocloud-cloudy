from system import settings
from .img import img_path
from .seed import seed_path


def createVM(name, mem, cpu, ostype):
    from backend.img import img_path
    from backend.seed import seed_path
    img_path = img_path(name)
    seed_path = seed_path(name)
    ostarget = settings.IMG_MAP.get(ostype)
    if not ostarget:
        raise ValueError('OStype %s not supported!' % ostype)
    return settings.VM_CMD.format(name=name,
                                  mem=mem,
                                  cpu=cpu,
                                  img_path=img_path,
                                  seed_path=seed_path,
                                  osvar=ostarget.get('version'))
