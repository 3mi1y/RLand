from datetime import datetime
import riak
import storage.security as security


# Provides access to a Riak database with RLand data types, such as
# User, Polygon, Harvest, Task, etc.
class RiakDb:

    # Initializes a RiakDb that will connect to the specified port on
    # localhost
    def __init__(self, port=8087):
        self.client = riak.RiakClient(pb_port=port)
        self.user_bucket = self.client.bucket('user')
        self.poly_bucket = self.client.bucket('polygon')
        self.task_bucket = self.client.bucket('task')
        self.harvest_bucket = self.client.bucket('harvest')
        self.note_bucket = self.client.bucket('note')
        self.poly_type_bucket = self.client.bucket('polygon_type')

    # Create a user with the given email, name, password, and address.
    def create_user(self, email, name, password, address):
        if self.user_bucket.get(email).data is None:
            new_user = self.user_bucket.new(email, data={
                    'email': email,
                    'name': name,
                    'password': security.hash_password(password),
                    'address': address,
                    'polygon_ids': [],
            })
            new_user.store()

            user = new_user.data
            return {
                'email': user['email'],
                'name': user['name'],
                'password': user['password'],
                'address': user['address'],
                'polygon_ids': user['polygon_ids'],
            }

        else:
            return False

    # Checks if a given email/password is valid for logging in. Returns
    # True if the user can login, False if either the email or password
    # is incorrect.
    def login(self, email, password):
        user = self.get_user(email)
        if user is None:
            return False

        if security.check_password(password, user['password']):
            return True
        else:
            return False

    # Gets a user by email address. No access checks are made.
    def get_user(self, email):
        user = self.user_bucket.get(email).data
        if user is None:
            return None
        return {
            'email': user['email'],
            'name': user['name'],
            'password': user['password'],
            'address': user['address'],
            'polygon_ids': user['polygon_ids'],
        }

    # Updates a user by email. If the user does not exist, nothing is
    # done. All user fields must exist on the input 'updateUser'
    def update_user(self, updateUser):
        user = self.user_bucket.get(updateUser['email'])
        if user.data:
            user.data['name'] = updateUser['name']
            if user.data['password'] != updateUser['password']:
                user.data['password'] = security.hash_password(updateUser['password'])
            user.data['address'] = updateUser['address']
            user.data['polygon_ids'] = updateUser['polygon_ids']
            user.store()

    # Deletes a user by email.
    def delete_user(self, email):
        user = self.user_bucket.get(email)
        if user.data:
            user.delete()

    # Creates a polygon with the specified location, name, owning
    # user, start date, and type. An ID is automatically assigned.
    # The created polygon is returned as in get_polygon()
    def create_polygon(self, location, name, uEmail, start_date, end_date, ptype):
        # TODO: this is really a hack
        keys = self.poly_bucket.get_keys()
        mx = max([int(k) for k in keys] + [0])
        poly_id = str(mx+1)

        # TODO: make sure start_date and end_date are actually dates
        poly = self.poly_bucket.new(poly_id, data={
            'id': poly_id,
            'location': location,
            'name': name,
            'user': uEmail,
            'start_date': start_date and str(start_date),
            'end_date': end_date and str(end_date),
            'type': ptype,
            'children': [],
        })
        poly.store()
        return {
            'id': poly_id,
            'location': location,
            'name': name,
            'user': uEmail,
            'start_date': start_date,
            'end_date': end_date,
            'type': ptype,
            'children': [],
        }

    # Retrieves a polygon by id and owner. If the owner does not match,
    # None is returned. Otherwise, returns the polygon as a dictionary.
    def get_polygon(self, poly_id, uEmail):
        poly = self.poly_bucket.get(poly_id).data
        if poly is None:
            return None
        if (poly['user'] == uEmail):
            return {
                'id': poly['id'],
                'location': poly['location'],
                'name': poly['name'],
                'user': poly['user'],
                'start_date': poly['start_date'] and datetime.strptime(poly['start_date'], "%Y-%m-%d").date(),
                'end_date': poly['end_date'] and datetime.strptime(poly['end_date'], "%Y-%m-%d").date(),
                'type': poly['type'],
                'children': poly['children'],
            }
        else:
            return None

    # Updates a polygon by its id. All polygon fields must be specified on
    # 'updatePoly'
    def update_polygon(self, updatePoly):
        poly = self.poly_bucket.get(updatePoly['id'])
        if poly.data:
            poly.data['name'] = updatePoly['name']
            poly.data['location'] = updatePoly['location']
            poly.data['start_date'] = updatePoly['start_date'] and str(updatePoly['start_date'])
            poly.data['end_date'] = updatePoly['end_date'] and str(updatePoly['end_date'])
            poly.data['type'] = updatePoly['type']
            poly.data['children'] = updatePoly['children']
            if poly.data['user'] != updatePoly['user']:
                # TODO: decide on exception handling policy
                raise Exception("Can't change the user a polygon belongs to!")
            poly.store()

    # Deletes the polygon with the given ID.
    def delete_polygon(self, poly_id):
        poly = self.poly_bucket.get(poly_id)
        if poly.data:
            poly.delete()
            return ("Deleted")

    def create_note(self, poly_id, date, title, content):
        keys = self.note_bucket.get_keys()
        mx = max([int(k) for k in keys] + [0])
        note_id = str(mx+1)
        note = self.note_bucket.new(note_id, data={
            "id": note_id,
            "poly_id": str(poly_id),
            "date": date,
            "title": title,
            "content": content
        })
        note.store()
        return {
            "id": note_id,
            "poly_id": str(poly_id),
            "date": date,
            "title": title,
            "content": content
        }

    def get_note(self, note_id):
        note = self.note_bucket.get(note_id).data
        if note is None:
            return None

        return {
            'id': note['id'],
            'poly_id': note['poly_id'],
            'date': note['date'],
            'title': note['title'],
            'content': note['content']
        }

    def get_notes(self, poly_ids):
        note_ids = self.note_bucket.get_keys()
        notes = []
        for nid in note_ids:
            data = self.note_bucket.get(nid).data
            if data and data['poly_id'] in poly_ids:
                notes += [{
                    'id': data['id'],
                    'poly_id': data['poly_id'],
                    'date': data['date'],
                    'title': data['title'],
                    'content': data['content']
                }]
        return notes

    def update_note(self, updateNote):
        note = self.note_bucket.get(updateNote['id'])
        if note.data:
            note.data['date'] = updateNote['date']
            note.data['title'] = updateNote['title']
            note.data['content'] = updateNote['content']
            if note.data['poly_id'] != updateNote['poly_id']:
                raise Exception("Can't update a note for a different polygon")
            note.store()

    def delete_note(self, note_id):
        note = self.note_bucket.get(note_id)
        if note.data:
            note.delete()
            return("Deleted")

    def create_harvest(self, poly_id, date, amount, units):
        keys = self.harvest_bucket.get_keys()
        mx = max([int(k) for k in keys] + [0])
        harvest_id = str(mx+1)
        harvest = self.harvest_bucket.new(harvest_id, data={
            'id': harvest_id,
            'poly_id': str(poly_id),
            'date': date,
            'amount': amount,
            'units': units
        })
        harvest.store()
        return{
            'id': harvest_id,
            'poly_id': str(poly_id),
            'date': date,
            'amount': amount,
            'units': units
        }

    def get_harvest(self, harvest_id):
        harvest = self.harvest_bucket.get(harvest_id).data
        if harvest is None:
            return None

        return {
            'id': harvest['id'],
            'poly_id': harvest['poly_id'],
            'date': harvest['date'],
            'amount': harvest['amount'],
            'units': harvest['units']
        }

    def get_harvests(self, poly_ids):
        harvest_ids = self.harvest_bucket.get_keys()
        harvests = []
        for hid in harvest_ids:
            data = self.harvest_bucket.get(hid).data
            if data and data['poly_id'] in poly_ids:
                harvests += [{
                    'id': data['id'],
                    'poly_id': data['poly_id'],
                    'date': data['date'],
                    'amount': data['amount'],
                    'units': data['units']
                }]
        return harvests

    def update_harvest(self, updateHarvest):
        harvest = self.harvest_bucket.get(updateHarvest['id'])
        if harvest.data:
            harvest.data['date'] = updateHarvest['date']
            harvest.data['amount'] = updateHarvest['amount']
            harvest.data['units'] = updateHarvest['units']
            if harvest.data['poly_id'] != updateHarvest['poly_id']:
                raise Exception("Can't update a harvest for a different polygon")
            harvest.store()

    def delete_harvest(self, harvest_id):
        harvest = self.harvest_bucket.get(harvest_id)
        if harvest.data:
            harvest.delete()
            return("Deleted")

    def create_task(self, poly_id, name, date,priority,completed):
        keys = self.task_bucket.get_keys()
        mx = max([int(k) for k in keys] + [0])
        task_id = str(mx+1)
        task = self.task_bucket.new(task_id, data={
            'id': task_id,
            'poly_id': str(poly_id),
            'name': name,
            'date': date,
            'priority' : priority,
            'completed' : completed
        })
        task.store()
        return {
            'id': task_id,
            'poly_id': str(poly_id),
            'name': name,
            'date': date,
            'priority':priority,
            'completed':completed
        }

    def get_task(self, task_id):
        task = self.task_bucket.get(task_id).data
        if(task is None):
            return None

        return {
            'id': task_id,
            'poly_id': task['poly_id'],
            'name': task['name'],
            'date': task['date'],
            'priority':task['priority'],
            'completed':task['completed']
        }

    def get_tasks(self, poly_ids):
        task_ids = self.task_bucket.get_keys()
        tasks = []
        for tid in task_ids:
            data = self.task_bucket.get(tid).data
            if data and data['poly_id'] in poly_ids:
                tasks += [{
                    'id': data['id'],
                    'poly_id': data['poly_id'],
                    'name': data['name'],
                    'date': data['date'],
                    'priority':data['priority'],
                    'completed':data['completed']
                }]
        return tasks

    def update_task(self, updateTask):
        task = self.task_bucket.get(updateTask['id'])
        if task.data:
            task.data['name'] = updateTask['name']
            task.data['date'] = updateTask['date']
            task.data['priority'] = updateTask['priority']
            task.data['completed'] = updateTask['completed']
            if task.data['poly_id'] != updateTask['poly_id']:
                raise Exception("Can't update a aharvest for a different polygon")
            task.store()

    def delete_task(self, task_id):
        task = self.task_bucket.get(task_id)
        if task.data:
            task.delete()
            return("Deleted")

    def create_poly_type(self, name, is_container, harvest, children):
        ptype = self.poly_type_bucket.new(name, data={
            'name': name,
            'is_container': is_container,
            'harvest': harvest,
            'children': children,
        })
        ptype.store()
        return {'name': name, 'is_container': is_container, 'harvest': harvest, 'children': children}

    def get_poly_type(self, name):
        ptype = self.poly_type_bucket.get(name).data
        if ptype is None:
            return None
        else:
            return {'name': ptype['name'], 'is_container': ptype['is_container'], 'harvest': ptype['harvest'], 'children': ptype['children']}

    def get_poly_types(self):
        keys = self.poly_type_bucket.get_keys()
        objs = self.poly_type_bucket.multiget(keys)
        pts = []
        for o in objs:
            ptype = o.data
            pts += [{'name': ptype['name'], 'is_container': ptype['is_container'], 'harvest': ptype['harvest'], 'children': ptype['children']}]
        return pts

    def update_poly_type(self, update_ptype):
        ptype = self.poly_type_bucket.get(update_ptype['name'])
        if ptype.data:
            ptype.data['is_container'] = update_ptype['is_container']
            ptype.data['harvest'] = update_ptype['harvest']
            ptype.data['children'] = update_ptype['children']
            ptype.store()

    def delete_poly_type(self, name):
        ptype = self.poly_type_bucket.get(name)
        if ptype.data:
            ptype.delete()

    def get_poly_type_tree(self):
        types_list = self.get_poly_types()
        types = dict([(t["name"], t) for t in types_list])

        def map_fields(ptype_name):
            ptype = types[ptype_name]
            if ptype:
                return { "name": ptype["name"], "leaves": [map_fields(c) for c in ptype["children"]] }
            else:
                print("Warning: polygon type not found:", ptype_name)
                return None

        root = map_fields("root")
        return root["leaves"]
