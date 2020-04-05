from werkzeug.security import generate_password_hash

passwd = input("Password: ")
h = generate_password_hash(passwd, salt_length=10)
print(h)
