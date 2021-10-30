import bcrypt

password_to_salt = "hello"

print(password_to_salt)

salted = bcrypt.hashpw( bytes(password_to_salt,  'utf-8' ) , bcrypt.gensalt(10))

print(  bcrypt.checkpw(  bytes(password_to_salt,  'utf-8' )  , salted ))

print(salted)
