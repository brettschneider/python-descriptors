import re


class PhoneNumber:
    """A descriptor ensures the (xxx) yyy-zzzz format."""

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return getattr(instance, f"_{self.name}")

    def __set__(self, instance, value):
        pattern = r"^\(\d{3}\) \d{3}-\d{4}$"
        if bool(re.match(pattern, value)):
            setattr(instance, f"_{self.name}", value)
        else:
            raise AttributeError("Invalid phone number format")


class Person:
    name: str
    phone: str = PhoneNumber()


class Company:
    industry: str
    phone: str = PhoneNumber()


if __name__ == "__main__":
    p = Person()
    p.name = "Patricia Kaike"
    p.phone = "(800) 555-1212"  # Works just fine.
    c = Company()
    c.phone = "unknown"  # Raises an attribute error
