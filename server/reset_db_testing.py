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


user2 = db.create_user("test2@example.com", "Test 2", "test2", "32 Campus Drive Missoula, MT 59812")

poly21 = db.create_polygon("{\"shape\":\"rectangle\",\"neBounds\":{\"lat\":46.86147031573249,\"lng\":-113.98442540241206},\"swBounds\":{\"lat\":46.86125757135067,\"lng\":-113.98462656808817}}", "Peas", user2["email"], "2018-04-01", "2018-07-01", ["Plant", "Garden Patch/Area (NOT raised beds)", "Vegetable & Fruit Garden", "Peas", "Field Peas"])
poly22 = db.create_polygon("{\"shape\":\"rectangle\",\"neBounds\":{\"lat\":46.861473983731685,\"lng\":-113.9848840601536},\"swBounds\":{\"lat\":46.86125757135067,\"lng\":-113.9850812025162}}", "Squash", user2["email"], "2018-04-01", "2018-07-01", ["Plant", "Garden Patch/Area (NOT raised beds)", "Vegetable & Fruit Garden", "Squash", "Acorn"])
poly23 = db.create_polygon("{\"shape\":\"rectangle\",\"neBounds\":{\"lat\":46.86137494766558,\"lng\":-113.98463863802874},\"swBounds\":{\"lat\":46.86125848835412,\"lng\":-113.98486662579501}}", "Carrots", user2["email"], "2018-04-01", "2018-07-01", ["Plant", "Garden Patch/Area (NOT raised beds)", "Vegetable & Fruit Garden", "Carrot", "Nantes"])

user2["polygon_ids"] += map(lambda p: p["id"], [poly21, poly22, poly23])
db.update_user(user2)

user3 = db.create_user("test3@example.com", "Test 3", "test3", "Playfair Park Missoula, MT")
poly31 = db.create_polygon("{\"shape\":\"circle\",\"center\":{\"lat\":46.84223831101116,\"lng\":-114.01404124218902},\"radius\":28.43531355110825}", "Apple Orchard", user3["email"], "2018-04-01", "", ["Plant", "Orchard", "Mono Fruit Orchard", "...", ""])
poly32 = db.create_polygon("{\"shape\":\"rectangle\",\"neBounds\":{\"lat\":46.8427848834439,\"lng\":-114.01386317869151},\"swBounds\":{\"lat\":46.84255738786859,\"lng\":-114.01441571374858}}", "Cabbage", user3["email"], "2018-04-01", "", ["Plant", "Row Crops", "Vegetable & Fruit Garden", "Cabbage", "Red Cabbage"])
poly33 = db.create_polygon("{\"shape\":\"rectangle\",\"neBounds\":{\"lat\":46.84248767128978,\"lng\":-114.01448008676493},\"swBounds\":{\"lat\":46.8420730392414,\"lng\":-114.01481804510081}}", "Potatoes", user3["email"], "2018-04-01", "", ["Plant", "Row Crops", "Vegetable & Fruit Garden", "Potato", "Russet"])
poly34 = db.create_polygon("{\"shape\":\"rectangle\",\"neBounds\":{\"lat\":46.84261624892433,\"lng\":-114.01444893795929},\"swBounds\":{\"lat\":46.842524516665485,\"lng\":-114.0147225232788}}", "Eggplant", user3["email"], "2018-04-01", "", ["Plant", "Garden Patch/Area (NOT raised beds)", "Vegetable & Fruit Garden", "Eggplant", "Ichiban"])
task31 = db.create_task(poly33["id"], "Harvest Potatoes", "2018-05-01", None, False, "")

user3["polygon_ids"] += map(lambda p: p["id"], [poly31, poly32, poly33, poly34])
db.update_user(user3)
