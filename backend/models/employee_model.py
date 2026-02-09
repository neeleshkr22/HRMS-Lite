from pydantic import BaseModel, EmailStr
from typing import Optional

# Request model for creating employee
class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    department: str

# Response model for employee
class EmployeeResponse(BaseModel):
    id: str
    employee_id: str
    full_name: str
    email: str
    department: str
