from storage.riak import RiakDb

def clear_bucket(bucket):
    keys = bucket.get_keys()
    for k in keys:
        obj = bucket.get(k)
        obj.delete()

db = RiakDb()
clear_bucket(db.user_bucket)
clear_bucket(db.poly_bucket)
clear_bucket(db.poly_type_bucket)
