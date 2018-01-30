import riak

class RiakDb:
    def __init__(self):
        self.client = riak.RiakClient(pb_port=8087)
        self.user_bucket = self.client.bucket('user')

    def create_user(self, email, name, password):
        new_user = self.user_bucket.new(email, data ={
                'email': email,
                'name': name,
                'password': password,
        })
        new_user.store()

    def get_user(self, email):
        user = self.user_bucket.get(email).data
        return { 'email': user['email'], 'name': user['name'], 'password': user['password'] }
