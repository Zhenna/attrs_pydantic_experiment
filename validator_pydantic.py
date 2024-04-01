# %%
from pydantic import BaseModel, Field, field_validator, constr
from datetime import datetime
from custom_validator import custom_email_validator

# Define a class using Pydantic


class Employee_pydantic(BaseModel):
    name: str
    email: constr(pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
    joining_date: datetime
    passed_probation: bool
    monthly_salary: float = Field(ge=0)
    performance_rating: float = Field(ge=1, le=5)

    @field_validator("joining_date")
    def validate_joining_date(cls, value):
        if value > datetime.today():
            raise ValueError("Joining date cannot be in the future.")
        return value

    # @field_validator("email")
    # def validate_email(cls, value):
    #     if not custom_email_validator(value):
    #         raise ValueError(
    #             "Email is not valid. Please provide a valid email address."
    #         )
    #     return value

    def calculate_months_of_service(self) -> int:
        import math

        """calculate the number of months since joining the company."""
        months_service = math.floor((datetime.today() - self.joining_date).days / 30)
        return months_service

    def calculate_severance_package(self) -> float:
        """calculate the severance package based on months of service and performance rating.
        Note: This is a simplified calculation for demonstration purposes.
        """
        months_service = self.calculate_months_of_service()

        if self.passed_probation:
            if months_service < 12:
                severance_package = self.monthly_salary * months_service / 12
            else:
                severance_package = (
                    self.monthly_salary * months_service / 12
                    + self.monthly_salary * self.performance_rating
                )
        else:
            severance_package = 0
        return severance_package


# %% correct values and types
Employee_pydantic(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2022, 1, 1),
    passed_probation=True,
    monthly_salary=5000,
    performance_rating=3,
).calculate_severance_package()

# %% wrong email
Employee_pydantic(
    name="John Doe",
    email="john.doe",  # email is not valid
    joining_date=datetime(2022, 1, 1),
    passed_probation=True,
    monthly_salary=5000,
    performance_rating=3,
).calculate_severance_package()

# %% wrong date
Employee_pydantic(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2025, 1, 1),  # date is in future
    passed_probation=True,
    monthly_salary=5000,
    performance_rating=3,
).calculate_severance_package()

# %% wrong performance rating
Employee_pydantic(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2022, 1, 1),
    passed_probation=True,
    monthly_salary=5000,
    performance_rating=0,  # cannot be 0
).calculate_severance_package()

# %% negative salary
Employee_pydantic(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2022, 1, 1),
    passed_probation=True,
    monthly_salary=-5000,  # cannot be negative
    performance_rating=3,
).calculate_severance_package()

# %% incorrect attribute type
Employee_pydantic(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2022, 1, 1),
    passed_probation="Not Yet",  # type violation
    monthly_salary=5000,
    performance_rating=3,
).calculate_severance_package()

# %%
# from pydantic import BaseModel, constr

# class CheckEmail(BaseModel):
#   email: constr(pattern=r'[a-zA-Z0-9._]@([\w-]+\.)+[\w-]{2,4}')

# my_data = {
#   "email" : "notavalidemail@example"
# }

# CheckEmail.model_validate(my_data)
# %%
