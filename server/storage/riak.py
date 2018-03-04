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
        else:
            # TODO: do something if user already exists.
            return "User is already in db"

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
        u = {
            'email': user['email'],
            'name': user['name'],
            'password': user['password'],
            'address': user['address']
        }

        try:
            u['polygon_ids'] = user['polygon_ids']
        except KeyError:
            u['polygon_ids'] = []

        return u

    # Updates a user by email. If the user does not exist, nothing is
    # done. All user fields must exist on the input 'updateUser'
    def update_user(self, updateUser):
        user = self.user_bucket.get(updateUser['email'])
        if user.data:
            user.data['name'] = updateUser['name']
            user.data['password'] = updateUser['password']
            user.data['address'] = updateUser['address']
            user.data['polygon_ids'] = updateUser['polygon_ids']
            user.store()

    # Deletes a user by email.
    def delete_user(self, email):
        user = self.user_bucket.get(email)
        if user.data:
            user.delete()

    # Creates a polygon with the specified location, name, and owning
    # user. An ID is automatically assigned. The created polygon is
    # returned as in get_polygon()
    def create_polygon(self, location, name, uEmail):
        # TODO: this is really a hack
        keys = self.poly_bucket.get_keys()
        mx = max([int(k) for k in keys] + [0])
        poly_id = str(mx+1)

        poly = self.poly_bucket.new(poly_id, data={
            'id': poly_id,
            'location': location,
            'name': name,
            'user': uEmail
        })
        poly.store()
        return {
            'id': poly_id,
            'location': location,
            'name': name,
            'user': uEmail
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
                'user': poly['user']
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
