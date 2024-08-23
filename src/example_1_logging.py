class LogAccess:
    """A descriptor the logs reading/writing from attributes"""
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        print(f"I'm reading from a attribute {self.name}")
        return instance._value

    def __set__(self, instance, value):
        print(f"I'm writing to attribute {self.name}")
        instance._value = value


class Person:
    name: str = LogAccess()
    email: str = LogAccess()


if __name__ == '__main__':
    p1 = Person()
    p1.name = "James Nasium"            # Outputs: "I'm writing to attribute name"
    p1.email = "jim.nasium@aol.com"     # Outputs: "I'm writing to attribute email"
    name = p1.name                      # Outputs: "I'm reading from attribute name"
    print(name)