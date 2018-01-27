import riak

class RiakDb:
    def __init__(self):
        self.client = riak.RiakClient(pb_port=8087)
