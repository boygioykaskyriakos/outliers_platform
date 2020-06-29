
class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def get_info(self):
        return self.first_name + ' ' + self.last_name

    def get_name(self):
        return self.first_name, self.last_name


class Adult(Person):
    def __init__(self, first_name, last_name, phone_number):
        Person.__init__(self, first_name, last_name)
        self.phone_number = phone_number

    def get_phone(self):
        return str(self.phone_number)


class Child(Person):
    def __init__(self, first_name, last_name, parent_1, parent_2):
        Person.__init__(self, first_name, last_name)
        self.parent_1 = parent_1
        self.parent_2 = parent_2

    def get_info(self):
        return super(Child, self).get_info() + " " + self.parent_1.get_info() + " " + self.parent_2.get_info()

    def get_parents(self):
        return self.parent_1, self.parent_2


if __name__ == "__main__":
    p = Person("Mary", "Ann")
    a = Adult("John", "Doe", "1234567")
    c = Child("Richard", "Doe", p, a)

    assert a.get_info() == "John Doe"
    assert c.get_name() == ("Richard", "Doe")
    assert c.get_info() == "Richard Doe Mary Ann John Doe"
    assert c.get_parents() == (p, a)






