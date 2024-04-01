# %%
import re
from dataclasses import dataclass
from datetime import datetime

# Define a class using dataclass decorator

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"


@dataclass()
class Employee_dataclass:
    name: str
    email: str
    joining_date: datetime
    passed_probation: bool
    monthly_salary: float or int
    performance_rating: int

    def __post_init__(self):
        # We'll validate the inputs here.
        if not isinstance(self.name, str):
            raise TypeError(f"'name' should be a string, was {type(self.name)}")
        if not isinstance(self.email, str):
            raise TypeError(f"'email' should be a string, was {type(self.email)}")
        if not re.fullmatch(regex, self.email):
            raise TypeError(f"'email' is not in a valid format, was {type(self.email)}")
        if not isinstance(self.joining_date, datetime):
            raise TypeError(
                f"'joining_date' should be a datetime, was {type(self.joining_date)}"
            )
        if (self.joining_date - datetime.today()).days >= 0:
            raise ValueError(
                f"'joining_date' should not be in the future, was {self.joining_date}"
            )
        if not isinstance(self.passed_probation, bool):
            raise TypeError(
                f"'passed_probation' should be a bool, was {type(self.passed_probation)}"
            )
        if not isinstance(self.monthly_salary, float) and not isinstance(
            self.monthly_salary, int
        ):
            raise TypeError(
                f"'monthly_salary' should be a float, was {type(self.monthly_salary)}"
            )
        if self.monthly_salary <= 0:
            raise ValueError(
                f"'monthly_salary' should be positive, was {self.monthly_salary}"
            )
        if not isinstance(self.performance_rating, int):
            raise TypeError(
                f"'performance_rating' should be an int, was {type(self.performance_rating)}"
            )
        if self.performance_rating < 1 or self.performance_rating > 5:
            raise ValueError(
                f"'performance_rating' should be between 1 and 5, was {self.performance_rating}"
            )

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
Employee_dataclass(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2022, 1, 1),
    passed_probation=True,
    monthly_salary=5000,
    performance_rating=3,
).calculate_severance_package()

# %% wrong email
Employee_dataclass(
    name="John Doe",
    email="john.doe",  # email is not valid
    joining_date=datetime(2022, 1, 1),
    passed_probation=True,
    monthly_salary=5000,
    performance_rating=3,
).calculate_severance_package()

# %% wrong date
Employee_dataclass(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2025, 1, 1),  # date is in future
    passed_probation=True,
    monthly_salary=5000,
    performance_rating=3,
).calculate_severance_package()

# %% wrong performance rating
Employee_dataclass(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2022, 1, 1),
    passed_probation=True,
    monthly_salary=5000,
    performance_rating=0,  # cannot be 0
).calculate_severance_package()

# %% negative salary
Employee_dataclass(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2022, 1, 1),
    passed_probation=True,
    monthly_salary=-5000,  # cannot be negative
    performance_rating=3,
).calculate_severance_package()

# %% incorrect attribute type
Employee_dataclass(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2022, 1, 1),
    passed_probation="Not Yet",  # type violation
    monthly_salary=5000,
    performance_rating=3,
).calculate_severance_package()

# %%
