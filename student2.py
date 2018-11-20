class Student:

    def __init__(self, data):
        self.id = data[0]
        self.name = data[1]
        self.email = data[2]
        self.nmec = data[3]
        self.ano = data[4]
        self.token = data[5]
        self.userName = data[6]

    def __str__(self):
        return self.userName + " " +  self.name + " " + self.email+ " " + self.token+ " " + str(self.nmec)+ " " + str(self.ano)