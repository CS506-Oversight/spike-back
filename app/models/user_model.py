class User:
    def __init__(self, username, password, phone, address, email, type="staff"):
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone
        self.address = address
        self.type = type
