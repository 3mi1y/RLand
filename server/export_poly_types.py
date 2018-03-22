import json
from storage.riak import RiakDb


db = RiakDb()

def map_fields(ptype):
    return { "name": ptype["name"], "leaves": [map_fields(get_ptype(c)) for c in ptype["children"]] }

def get_ptype(name):
    return db.get_poly_type(name)

root = map_fields(get_ptype("root"))
print(json.dumps(root["leaves"]))
