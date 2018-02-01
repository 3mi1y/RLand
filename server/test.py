from storage.riak import RiakDb
import storage.security as security


db = RiakDb()

U_EMAIL = "test@example.com"
U_NAME = "Test User"
U_PASS = "test password"
# delete/recreate a new user
db.delete_user(U_EMAIL)
db.create_user(U_EMAIL, U_NAME, U_PASS)

# get the new user and test the password hashing
user = db.get_user(U_EMAIL)
pwhash = user['password']
print("Hash for user is ", pwhash)
if security.check_password(U_PASS, pwhash):
    print("GOOD: correct password checks out")
else:
    print("BAD : correct password but failed")
if security.check_password(U_PASS+"bad", pwhash):
    print("BAD: incorrect password was accepted")
else:
    print("GOOD: incorrect password was rejected")

# make a new polygon
db.delete_polygon("polygon1")
db.create_polygon("polygon1", "Nevada", "Area 51")

poly = db.get_polygon("polygon1")
print(poly['name'], "is in", poly['location'])
