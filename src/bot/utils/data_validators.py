import re


def validate_name(name: str) -> bool:
    pattern = r"^[a-zA-Zа-яА-ЯёЁ\s]+$"
    return bool(re.match(pattern, name))


def validate_and_format_russian_phone(phone: str) -> tuple[bool, str]:
    digits = re.sub(r"\D", "", phone)

    if len(digits) == 11 and digits[0] in ("7", "8"):
        digits = digits[1:]

    elif len(digits) == 10:
        pass
    else:
        return False, phone

    if len(digits) != 10:
        return False, phone

    formatted_phone = f"+7({digits[0:3]}){digits[3:6]}-{digits[6:8]}-{digits[8:10]}"
    return True, formatted_phone
