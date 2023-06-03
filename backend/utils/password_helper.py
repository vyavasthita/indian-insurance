import random
import string


class PasswordGenerator:
    def __init__(self, length) -> None:
        self._length = length
        self._lower = string.ascii_lowercase
        self._upper = string.ascii_uppercase
        self._num = string.digits
        self._symbols = string.punctuation

    def generate_password(self) -> str:
        all = self._lower + self._upper + self._num + self._symbols

        return "".join(random.sample(all, self._length))



