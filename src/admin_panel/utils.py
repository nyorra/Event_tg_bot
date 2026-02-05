import random
import string


def generate_random_code() -> str:
    part1 = "".join(random.choices(string.ascii_uppercase, k=4))
    part2 = "".join(random.choices(string.ascii_uppercase, k=4))
    return f"{part1}-{part2}"
