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

        if security.check_password(password,user['password']): #we could just return this line but I have this in case we need to do something else.
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

    def update_user(self, updateUser):
        user = self.user_bucket.get(updateUser['email'])
        if user.data:
            user.data['name'] = updateUser['name']
            user.data['password'] = updateUser['password']
            user.data['polygon_ids'] = updateUser['polygon_ids']
            user.store()

    def delete_user(self, email):
        user = self.user_bucket.get(email)
        if user.data:
            user.delete()


    def create_polygon(self, poly_id, location, name,uEmail):
        if self.poly_bucket.get(poly_id).data is None:
            poly = self.poly_bucket.new(poly_id, data = {
                'id': poly_id,
                'location': location,
                'name': name,
                'user' : uEmail
            })
            poly.store()
            return ({'id': poly_id, 'location': location, 'name': name, 'user': uEmail})
        else:
            # TODO: polygon already exists
            print("Oh no this already exists!")
            pass

    def get_polygon(self, poly_id,uEmail):
        poly = self.poly_bucket.get(poly_id).data
        if poly is None:
            return None
        if (poly['user'] == uEmail):
            return { 'id': poly['id'], 'location': poly['location'], 'name': poly['name'], 'user': poly['user'] }
        else:
            return ("You don't have access to that polygon.")

    def delete_polygon(self, poly_id):
        poly = self.poly_bucket.get(poly_id)
        if poly.data:
            poly.delete()
            return ("Deleted")
