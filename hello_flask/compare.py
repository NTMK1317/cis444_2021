import bcrypt

password_to_salt = "hello"

salted = bcrypt.hashpw( bytes(password_to_salt,  'utf-8' ) , bcrypt.gensalt(10))
print(salted)
print( salted.decode('utf-8'))
salted = str(salted.decode('utf-8'))
print( salted.encode('utf-8'))
salted = salted.encode('utf-8')

print(  bcrypt.checkpw(  bytes(password_to_salt,  'utf-8' )  , b'$2b$10$Uevd9HO7hfJNzVLWC5UfFuZ2mcyhS2N4uYaLTFEnZFKliaQZTpXiK' ))

print(  bcrypt.checkpw(  bytes(password_to_salt,  'utf-8' )  , salted ))

print( salted == b'$2b$10$Uevd9HO7hfJNzVLWC5UfFuZ2mcyhS2N4uYaLTFEnZFKliaQZTpXiK' )
