import phonenumbers
from phonenumbers import NumberParseException

def validate_phone_number(phone_number: str, region: str = None) -> bool:
    try:
        parsed_number = phonenumbers.parse(phone_number, region)
        return phonenumbers.is_valid_number(parsed_number)
    except NumberParseException:
        return False
