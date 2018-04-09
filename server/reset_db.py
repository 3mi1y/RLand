from storage.riak import RiakDb


def clear_bucket(bucket):
    keys = bucket.get_keys()
    for k in keys:
        obj = bucket.get(k)
        obj.delete()


db = RiakDb()
clear_bucket(db.user_bucket)
clear_bucket(db.poly_bucket)
clear_bucket(db.task_bucket)
clear_bucket(db.harvest_bucket)
clear_bucket(db.note_bucket)
clear_bucket(db.poly_type_bucket)

ptypes = {"root": {"name": "root", "is_container": False, "harvest": None, "children": []}}
with open("poly_types.csv") as types_db:
    for line in types_db:
        data = [f.strip() for f in line.split(",")]
        parent = data[0]
        if not parent or parent == "parent":
            continue

        name = data[1]
        is_container = data[2] == "1"
        harvest = data[3] or None

        ptype = {"name": name, "is_container": is_container, "harvest": harvest, "children": []}

        if parent in ptypes:
            ptypes[parent]["children"] += [name]
        else:
            print("Unseen parent:", parent)
        ptypes[name] = ptype

for ptype in ptypes.values():
    db.create_poly_type(ptype["name"], ptype["is_container"], ptype["harvest"], ptype["children"])
