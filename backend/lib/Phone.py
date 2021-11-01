class Phone:
    number = ""

    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return f"<Phone Number: {self.number}>"


