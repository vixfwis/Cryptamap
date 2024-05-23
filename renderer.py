import ctypes
import pathlib

r = ctypes.CDLL(pathlib.Path().absolute() / "renderer.so")
settings = {}
def init(map, **kwargs):
    global settings
    settings.update({
        "length": ctypes.c_size_t(map.size.width()*map.size.height() * 4),
        "map": bytes(map.map),
        "background": map.model.background
    })
    settings.update(kwargs)
    r.test()

class initMapStruct(ctypes.Structure):
    _fields_ = [
        ('r', ctypes.c_uint8),
        ('g', ctypes.c_uint8),
        ('b', ctypes.c_uint8),
        ('a', ctypes.c_uint8),
        ('length', ctypes.c_size_t),
        #('map', ctypes.POINTER(ctypes.c_uint8 * settings["length"].value * 4))
    ]
    def __init__(self, background): 
        pass
        #print(settings["length"].value)
        self.r = ctypes.c_uint8(50)
        self.g = ctypes.c_uint8(100)
        self.b = ctypes.c_uint8(150)
        self.a = ctypes.c_uint8(0)
        self.length = settings["length"]
        #self.map = (ctypes.c_uint8 )(*settings["map"])

def c_initMap():
    r.initMap.argtypes = [ctypes.POINTER(initMapStruct)]
    r.initMap.restype = ctypes.POINTER(ctypes.c_uint8)*settings["length"].value
    meta = initMapStruct(settings['background'])
    l = r.initMap(meta)
    print(f"test: {l}")

if __name__ == '__main__':
    settings.update({
        "length": ctypes.c_size_t(10*10*4),
        "map": bytearray([i % 256 for i in range(1000000)]),
        "background": None
    })
    c_initMap()

