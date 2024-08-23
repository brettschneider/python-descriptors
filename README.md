# Understanding Python Descriptors: A Deep Dive into Reusable Getter/Setters #

Python is a language that thrives on flexibility and dynamic behavior, and one of its more
advanced features is the descriptor protocol. While not as commonly discussed as other Pythonic
concepts, descriptors are a powerful tool for creating reusable getter and setter
functionalities. In this blog post, we'll explore what Python descriptors are, how they work
under the hood, and some practical use cases where they can shine.

## What Are Python Descriptors? ##

At their core, Python descriptors are objects that manage the access and modification of
attributes. They are a form of reusable getter and setter logic, abstracted into a class
that can be reused across multiple attributes or even multiple classes. In simpler terms,
descriptors allow you to define how an attribute is retrieved, set, or deleted in a class.

Descriptors are typically implemented using Python’s `__get__`, `__set__`, and `__delete__` methods. When an attribute
is accessed on an object, Python checks if the attribute has these special methods defined, and if so, it delegates the
operation to the descriptor.

Here’s a basic example of a descriptor:

```python
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
```

And here's an example of how it would be used:

```python
class Person:
    name: str = LogAccess()
    email: str = LogAccess()


if __name__ == '__main__':
    p1 = Person()
    p1.name = "James Nasium"  # Outputs: "I'm writing to attribute name"
    p1.email = "jim.nasium@aol.com"  # Outputs: "I'm writing to attribute email"
    name = p1.name  # Outputs: "I'm reading from attribute name"
    print(name)
```

Now you may be saying to yourself, "this looks an awful lot like a `@property`," and you'd be
right. Just like `@property` accessors, you can validate/verify/mutate values either going
in or coming out. But unlike `@property`, descriptor code is abstracted away into a separate
class that can be reused. Descriptors can be reused any number of times either within the
same class (like `name` and `email` are above) or across multiple classes.

## How Do Descriptors Work? ##

Understanding what happens when you access an attribute on an object that uses a descriptor is key to appreciating their
power. When you dereference an attribute in Python, the language performs several checks:

Instance Dictionary: Python first checks if the attribute is stored directly in the instance's dictionary (`__dict__`).
If it is, that value is returned.
Class Attributes: If the attribute is not found in the instance dictionary, Python then checks if the attribute is
defined in the class or its parent classes. If the attribute is a descriptor (i.e., it implements `__get__`, `__set__`,
or `__delete__`), Python invokes the corresponding method on the descriptor.
Default Behavior: If neither of the above applies, Python returns None or raises an AttributeError.
Here’s how Python handles a descriptor during attribute access:

`__get__`: This method is invoked when you retrieve the attribute (e.g., obj.attribute). The descriptor can return a
computed value, a stored value, or any other data.
`__set__`: This method is called when you assign a value to the attribute (e.g., obj.attribute = 42). It allows the
descriptor to control how the value is stored or modified.
`__delete__`: This method is triggered when the attribute is deleted (e.g., del obj.attribute). The descriptor can then
handle cleanup or other logic.
This mechanism allows descriptors to insert custom behavior seamlessly into attribute access.

## Practical Uses of Descriptors ##

Descriptors can be used for all kinds of handy functionality including:

* Access notification/logging (see the above example)
* Access control
* Input validation or output formatting
* Lazy evaluation or external retrieval of values

The rest of this blog post is dedicated to some simple examples.

### Input validation ###

Descriptors can be used to validate inputs or format outputs. Here's an example the enforces
a strict phone number format for string attributes. Note it is reused across two different
classes:

```python
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
    c.phone = "unknown"  # Raises an AttributeError
```

Note the `.phone` attribute on both classes is still of type "string". Code that consumes the
classes is unaware that a descriptor is working with the class. It's pretty much transparent.

### Lazy evaluation/external retrieval ###

This example does indeed implement an external data fetch, but it also implements some access
control, making the `.hostname` attribute effectively read-only.

```python
import subprocess


class Hostname:
    def __get__(self, instance, owner):
        return subprocess.run("hostname")

    def __set__(self, instance, value):
        raise AttributeError("Hostname is a read-only attribute")


class SystemInfo:
    hostname: str = Hostname()
    managed_by: str = "James Schue"


if __name__ == '__main__':
    si = SystemInfo()
    print(f"Hostname: {si.hostname}")  # Outputs:  Hostname: Steves-MacBook.local
    si.hostname = "Jims-MacBook.local"  # Raises an AttributeError
```

## Official Python Documentation ##

The official Python descriptor guide can be found https://docs.python.org/3/howto/descriptor.html
The guide includes additional examples.

## Bonus Material ##

All the source-code for this blog can be found at
https://github.com/brettschneider/python-descriptors. I've also written a more involved example
called `auto_persist`, which creates a simple JSON database from your object instantiations and
automatically updates the records in the JSON file when you read/write the attributes of live
Python objects.
