# %%
from pydantic import BaseModel
from datetime import datetime

# Define a class using Pydantic


class Employee_pydantic(BaseModel):
    name: str
    email: str
    joining_date: datetime
    passed_probation: bool
    monthly_salary: float
    performance_rating: float

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


# %% correct attribute type
Employee_pydantic(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2022, 1, 1),
    passed_probation=True,
    monthly_salary=5000,
    performance_rating=3,
).calculate_severance_package()

# %% new attribute
Sally = Employee_pydantic(
    name="John Doe",
    email="john.doe@example.com",
    joining_date=datetime(2022, 1, 1),
    passed_probation=True,
    monthly_salary=5000,
    performance_rating=3,
)
Sally.remarks = "She is the boss's daughter."  # new attribute
Sally.calculate_severance_package()

# %% positional arguments
Employee_pydantic(
    "John Doe",
    "john.doe@example.com",
    datetime(2022, 1, 1),
    True,
    5000,
    3,
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


# %% keyword arguments not in order
Employee_pydantic(
    email="john.doe@example.com",
    joining_date=datetime(2022, 1, 1),
    passed_probation=True,
    monthly_salary=5000,
    performance_rating=3,
    name="John Doe",  # not in order
).calculate_severance_package()
# %%
