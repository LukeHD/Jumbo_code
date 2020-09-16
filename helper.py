sensors = [
    "bme",
    "mpu",
    "neo"
]


def getClassByName(name):
    return globals()[name]


def getClassAttrsByClassName(name):
    classVar = getClassByName(name)
    return [attr for attr in dir(classVar) if attr[:1] != "_" and not callable(getattr(classVar, attr))]