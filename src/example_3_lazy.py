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
    si.hostname = "Jims-MacBook.local" # Raises an AttributeError
