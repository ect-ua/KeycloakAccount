import datetime

class Student:

    def __init__(self, data):
        self.id = data[0] or 0
        self.name = data[1] or ''
        self.email = data[2] or ''
        self.nmec = data[3] or 0
        self.ano = data[4] or datetime.datetime.now().year
        self.token = data[5] or ''
        self.username = data[6] or ''

    def __str__(self):
        return self.username + " " +  self.name + " " + self.email+ " " + self.token+ " " + str(self.nmec)+ " " + str(self.ano)