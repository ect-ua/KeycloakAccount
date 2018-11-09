import inspect

class Student:

    def __init__(self, data):
        self.userName = data[0]
        self.name = data[1]
        self.email = data[2]
        self.token = data[3]
        self.nmec = data[4]
        self.ano = data[5]

    def __str__(self):
        return self.userName + " " +  self.name + " " + self.email+ " " + self.token+ " " + str(self.nmec)+ " " + str(self.ano)