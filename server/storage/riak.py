import riak
import storage.security as security

class RiakDb:
    def __init__(self):
        self.client = riak.RiakClient(pb_port=8087)
        self.user_bucket = self.client.bucket('user')
        self.poly_bucket = self.client.bucket('polygon')

    def create_user(self, email, name, password):
        #print("creating new user")
        if self.user_bucket.get(email).data is None:
            new_user = self.user_bucket.new(email, data ={
                    'email': email,
                    'name': name,
                    'password': security.hash_password(password),
                    'polygon_ids': [],
            })
            new_user.store()
        else:
            #TODO: do something if user already exists.
            return "User is already in db"

    def login(self,email,password):
        #print("logging in")
        user = self.get_user(email)
        if user is None:
            return False

        if security.check_password(password,user['password']):
            return True
        else:
            return False


    def get_user(self, email):
        user = self.user_bucket.get(email).data
        if user is None:
            return None
        u = { 'email': user['email'], 'name': user['name'], 'password': user['password'] }

        try:
            u['polygon_ids'] = user['polygon_ids']
        except:
            u['polygon_ids'] = []

        return u

    def delete_user(self, email):
        user = self.user_bucket.get(email)
        if user.data:
            user.delete()

    def create_polygon(self, poly_id, location, name):
        if self.poly_bucket.get(poly_id).data is None:
            poly = self.poly_bucket.new(poly_id, data = {
                'id': poly_id,
                'location': location,
                'name': name,
            })
            poly.store()
        else:
            # TODO: polygon already exists
            pass

    def get_polygon(self, poly_id):
        poly = self.poly_bucket.get(poly_id).data
        if poly is None:
            return None
        return { 'id': poly['id'], 'location': poly['location'], 'name': poly['name'] }

    def delete_polygon(self, poly_id):
        poly = self.poly_bucket.get(poly_id)
        if poly.data:
            poly.delete()
