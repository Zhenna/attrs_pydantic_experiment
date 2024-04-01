# %%
from attrs import define, field, validators
from datetime import datetime

# Define a class with attributes using attrs


@define
class Employee_attrs:
    name: str = field(validator=validators.instance_of(str))
    email: str = field(
        validator=validators.matches_re(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        )
    )
    joining_date: datetime = field(validator=validators.instance_of(datetime))
    passed_probation: bool = field(validator=validators.instance_of(bool))
    monthly_salary: float = field(validator=validators.ge(0))
    performance_rating: float = field(validator=[validators.ge(1), validators.le(5)])

    @joining_date.validator
    def validate_joining_date(self, attribute, value):
        if value > datetime.today():
            raise ValueError("Joining date cannot be in the future.")

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
Employee_attrs(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2022, 1, 1),
    passed_probation=True,
    monthly_salary=5000,
    performance_rating=3,
).calculate_severance_package()

# %% wrong email
Employee_attrs(
    name="John Doe",
    email="john.doe",  # email is not valid
    joining_date=datetime(2022, 1, 1),
    passed_probation=True,
    monthly_salary=5000,
    performance_rating=3,
).calculate_severance_package()

# %% wrong date
Employee_attrs(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2025, 1, 1),  # date is in future
    passed_probation=True,
    monthly_salary=5000,
    performance_rating=3,
).calculate_severance_package()


# %% wrong performance rating
Employee_attrs(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2022, 1, 1),
    passed_probation=True,
    monthly_salary=5000,
    performance_rating=0,  # cannot be 0
).calculate_severance_package()

# %% negative salary
Employee_attrs(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2022, 1, 1),
    passed_probation=True,
    monthly_salary=-5000,  # cannot be negative
    performance_rating=3,
).calculate_severance_package()

# %% incorrect attribute type
Employee_attrs(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2022, 1, 1),
    passed_probation="Not Yet",  # type violation
    monthly_salary=5000,
    performance_rating=3,
).calculate_severance_package()
