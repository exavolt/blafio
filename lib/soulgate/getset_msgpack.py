
#TODO: Serialize-deserialize some value types (esp. datetime)

import msgpack


def _msgpack_get(self, id):
    val = self.get(id)
    if not val:
        return val
    return msgpack.unpackb(val)

def _msgpack_set(self, id, val):
    self.set(id, msgpack.packb(val))


def monkey_patch(cls):
    cls.msgpack_get = _msgpack_get
    cls.msgpack_set = _msgpack_set

