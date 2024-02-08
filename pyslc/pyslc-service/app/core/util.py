import re
from hashlib import sha256
from typing import List


# create function to split string by space, special characters, and camel case


def split_string(string) -> List[str]:
    return re.findall(r"\b\w+\b", string)


def hash_string(string: str):
    string = "".join(split_string(string))
    return sha256(string.encode()).hexdigest()
