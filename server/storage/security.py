from codecs import encode, decode

import bcrypt


# Returns a string containing a salt and hashed password, suitable for
# storing in a database.
def hash_password(password):
    hashed = bcrypt.hashpw(encode(password, "utf-8"), bcrypt.gensalt())
    return decode(hashed, "utf-8")


# Verifies that the provided 'password' matches the password originally
# used to generate 'hashed'. Returns True if the password matches.
def check_password(password, hashed):
    return bcrypt.checkpw(encode(password, "utf-8"), encode(hashed, "utf-8"))
