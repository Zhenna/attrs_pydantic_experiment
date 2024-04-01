# %%
import re


def custom_email_validator(email: str):
    """
    This is a custom email validator that checks if an email address is valid.
    """
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

    if re.fullmatch(regex, email):
        return True
    else:
        return False


# %%

email_A = "example@example.com"
email_B = "example@example"
email_C = "@example.com"

# %%
custom_email_validator(email=email_A)

# %%
custom_email_validator(email=email_B)

# %%
custom_email_validator(email=email_C)
# %%
