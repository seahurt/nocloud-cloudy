from system import settings
from img import img_path
from seed import seed_path
import img
import seed


def createVM(name, mem, cpu):
    img_path = img.img_path(name)
    seed_path = seed.seed_path(name)
    return settings.VM_CMD.format(name=name,
                                  mem=mem,
                                  cpu=cpu,
                                  img_path=img_path,
                                  seed_path=seed_path)
