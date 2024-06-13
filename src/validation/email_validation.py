import re
 

def validate_email_format(email: str) -> bool:
    email_regex = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
    return bool(email_regex.match(email))

def is_allowed_domain(email: str, allowed_domains: list[str]) -> bool:
    domain = email.split('@')[-1]
    return domain in allowed_domains

TEMP_EMAIL_DOMAINS = {
    "tempmail.com",
    "10minutemail.com",
    "mailinator.com",
      
}

def is_temporary_email(email: str, temp_domains: set[str]) -> bool:
    domain = email.split('@')[-1]
    return domain in temp_domains

 