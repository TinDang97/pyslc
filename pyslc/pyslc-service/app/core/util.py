import re


# create function to split string by space, special characters, and camel case


def split_string(string):
    return re.findall(r"\b\w+\b", string)
