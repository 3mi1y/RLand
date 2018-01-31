import riak
from .security import hash_password
import storage.security as security
class RiakDb:
    def __init__(self):
        self.client = riak.RiakClient(pb_port=8087)
        self.user_bucket = self.client.bucket('user')

    def create_user(self, email, name, password):
        #print("creating new user")
        if self.user_bucket.get(email).data is None:
            new_user = self.user_bucket.new(email, data ={
                    'email': email,
                    'name': name,
                    'password': hash_password(password),
            })
            new_user.store()
        else:
            #TODO: do something if user already exists.
            return "User is already in db"

    def login(self,email,password):
        #print("logging in")
        user = self.get_user(email)
        if security.check_password(password,user['password']):
            return True
        else:
            return False


    def get_user(self, email):
        user = self.user_bucket.get(email).data
        if user is None:
            return None
        return { 'email': user['email'], 'name': user['name'], 'password': user['password'] }

    def delete_user(self, email):
        user = self.user_bucket.get(email)
        if user.data:
            user.delete()
