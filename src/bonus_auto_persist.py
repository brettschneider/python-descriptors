import json


def _load_records(filename: str) -> dict:
    """Given a filename returns a dictionary of records"""
    try:
        with open(filename, "r") as infile:
            return json.load(infile)
    except FileNotFoundError:
        return {}


def _save_records(filename: str, records: dict) -> None:
    """Saves the records to the given filename as JSON"""
    with open(filename, "w") as outfile:
        json.dump(records, outfile, indent=4)


class IdentityDescriptor:
    """Simple value passthrough descriptor"""
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)


class JsonFilename(IdentityDescriptor):
    """Use this to hold the JSON file's filename"""


def _json_filename(instance) -> str | None:
    for attr_name, attr_value in instance.__class__.__dict__.items():
        if isinstance(attr_value, JsonFilename):
            return getattr(instance, attr_name)
    return None


class RecordId(IdentityDescriptor):
    """Use this to hold a record's unique identifier"""


def _record_id(instance) -> str | None:
    for attr_name, attr_value in instance.__class__.__dict__.items():
        if isinstance(attr_value, RecordId):
            return str(getattr(instance, attr_name))
    return None


class Field:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if _json_filename(instance) and _record_id(instance):
            all_records = _load_records(_json_filename(instance))
            record = all_records.get(_record_id(instance), {})
            return record.get(self.name, None)
        return None

    def __set__(self, instance, value):
        if _json_filename(instance) and _record_id(instance):
            all_records = _load_records(_json_filename(instance))
            record = all_records.get(_record_id(instance), {})
            record[self.name] = value
            all_records[_record_id(instance)] = record
            _save_records(_json_filename(instance), all_records)


class Person:
    filename = JsonFilename()
    person_id = RecordId()
    name: str = Field()
    email: str = Field()
    age: int = Field()

    def __init__(self, filename, person_id=None):
        self.filename = filename
        self.person_id = person_id


if __name__ == '__main__':
    marketing_target_1 = Person("../datafiles/people.json", "person-1")
    marketing_target_1.name = "James Schue"
    marketing_target_1.email = "jschue@aol.com"
    marketing_target_1.age = 42

    marketing_target_2 = Person("../datafiles/people.json", "person-2")
    marketing_target_2.name = "Patricia Kaike"
    marketing_target_2.email = "fastbaker91@gmail.com"
    marketing_target_2.age = 36

    lookup_person = Person("../datafiles/people.json", "person-1")
    print(lookup_person.name)  # Outputs: James Schue
