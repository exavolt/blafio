
# Note that this is for pymongo's BSON codec. Not the independent BSON codec.

import bson


def _bson_get(self, id):
    val = self.get(id)
    if not val:
        return val
    bd = bson.BSON(val)
    return bd.decode()

def _bson_set(self, id, val):
    self.set(id, bson.BSON.encode(val))


def monkey_patch(cls):
    cls.bson_get = _bson_get
    cls.bson_set = _bson_set

