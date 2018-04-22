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


user2 = db.create_user("test2@example.com", "Test 2", "test2", "2418 S 7th St West Missoula, MT")

poly21 = db.create_polygon("{\"shape\":\"rectangle\",\"neBounds\":{\"lat\":46.8650112119313,\"lng\":-114.03847303235585},\"swBounds\":{\"lat\":46.864189627987635,\"lng\":-114.03875466430242}}", "Peas", user2["email"], "2018-04-01", "2018-07-01", ["Plant", "Garden Patch/Area (NOT raised beds)", "Vegetable & Fruit Garden", "Peas", "Field Peas"])
poly22 = db.create_polygon("{\"shape\":\"polygon\",\"path\":[{\"lat\":46.865022489339296,\"lng\":-114.03836775320389},{\"lat\":46.86419540384883,\"lng\":-114.03841871517517},{\"lat\":46.864193569942216,\"lng\":-114.03825510042526},{\"lat\":46.8650261570958,\"lng\":-114.03820413845398}]}", "Squash", user2["email"], "2018-04-01", "2018-07-01", ["Plant", "Garden Patch/Area (NOT raised beds)", "Vegetable & Fruit Garden", "Squash", "Acorn"])
poly23 = db.create_polygon("{\"shape\":\"polygon\",\"path\":[{\"lat\":46.865014158935594,\"lng\":-114.03903280001782},{\"lat\":46.864117384811145,\"lng\":-114.03902743559979},{\"lat\":46.86417423596727,\"lng\":-114.03895233374737},{\"lat\":46.86417973768884,\"lng\":-114.03878871899747},{\"lat\":46.865014158935594,\"lng\":-114.0387940834155}]}", "Carrots", user2["email"], "2018-04-01", "2018-07-01", ["Plant", "Garden Patch/Area (NOT raised beds)", "Vegetable & Fruit Garden", "Carrot", "Nantes"])

user2["polygon_ids"] += map(lambda p: p["id"], [poly21, poly22, poly23])
db.update_user(user2)

user3 = db.create_user("test3@example.com", "Test 3", "test3", "2418 S 7th St West Missoula, MT")
poly31 = db.create_polygon("{\"shape\":\"polygon\",\"path\":[{\"lat\":46.86411040218481,\"lng\":-114.03831696690088},{\"lat\":46.86391600742891,\"lng\":-114.03816676319605},{\"lat\":46.8639050039311,\"lng\":-114.03757667721277},{\"lat\":46.863993031850356,\"lng\":-114.03757667721277},{\"lat\":46.86411773782218,\"lng\":-114.03771615208154}]}", "Apple Orchard", user3["email"], "2018-04-01", "", ["Plant", "Orchard", "Mono Fruit Orchard", "...", ""])
poly32 = db.create_polygon("{\"shape\":\"polygon\",\"path\":[{\"lat\":46.86501845459211,\"lng\":-114.03722536428944},{\"lat\":46.86434908478443,\"lng\":-114.0372897373058},{\"lat\":46.8644719560321,\"lng\":-114.03695982559697},{\"lat\":46.865023956227176,\"lng\":-114.03691422804371}]}", "Cabbage", user3["email"], "2018-04-01", "", ["Plant", "Row Crops", "Vegetable & Fruit Garden", "Cabbage", "Red Cabbage"])
poly33 = db.create_polygon("{\"shape\":\"polygon\",\"path\":[{\"lat\":46.86425188792662,\"lng\":-114.03769206865803},{\"lat\":46.86501845459211,\"lng\":-114.03764110668675},{\"lat\":46.8650147868351,\"lng\":-114.03735679253117},{\"lat\":46.864314240648085,\"lng\":-114.0374158011295}]}", "Potatoes", user3["email"], "2018-04-01", "", ["Plant", "Row Crops", "Vegetable & Fruit Garden", "Potato", "Russet"])
poly34 = db.create_polygon("{\"shape\":\"polygon\",\"path\":[{\"lat\":46.86502762398358,\"lng\":-114.03799515827671},{\"lat\":46.86422437935,\"lng\":-114.038046120248},{\"lat\":46.86423171497182,\"lng\":-114.03784495457188},{\"lat\":46.865023956227176,\"lng\":-114.03776448830143}]}", "Eggplant", user3["email"], "2018-04-01", "", ["Plant", "Garden Patch/Area (NOT raised beds)", "Vegetable & Fruit Garden", "Eggplant", "Ichiban"])
poly35 = db.create_polygon("{\"shape\":\"rectangle\",\"neBounds\":{\"lat\":46.86416923252616,\"lng\":-114.03767150324069},\"swBounds\":{\"lat\":46.86413805609026,\"lng\":-114.03778415601931}}", "Chicken Coop", user3["email"], "2018-04-01", "", ["Animal", "Poultry/Egg layers", "Chickens", "Egg Laying Chicken Hens", "Bantam"])
task31 = db.create_task(poly33["id"], "Harvest Potatoes", "2018-05-01", None, False, "")
task32 = db.create_task(poly34["id"], "Harvest Eggplant", "2018-05-01", None, False, "")
task33 = db.create_task(poly35["id"], "Buy Chicken Feed", "2018-05-01", None, False, "")

user3["polygon_ids"] += map(lambda p: p["id"], [poly31, poly32, poly33, poly34, poly35])
db.update_user(user3)
