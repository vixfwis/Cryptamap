import ctypes
import pathlib

r = ctypes.CDLL(pathlib.Path().absolute() / "renderer.dll")
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
        #print(settings["length"].value)
        self.r = ctypes.c_uint8(background.red())
        self.g = ctypes.c_uint8(background.green())
        self.b = ctypes.c_uint8(background.blue())
        self.a = ctypes.c_uint8(background.alpha())
        self.length = settings["length"]
        #self.map = (ctypes.c_uint8 )(*settings["map"])

def c_initMap():
    r.initMap.restype = ctypes.POINTER(ctypes.c_uint8)*settings["length"].value
    meta = initMapStruct(settings['background'])
    l = r.initMap(meta)
    print(f"test: {(l.contents)}")