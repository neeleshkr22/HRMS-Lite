from fastapi import APIRouter, HTTPException
from typing import List
from models.employee_model import EmployeeCreate, EmployeeResponse
from config.database import employees_collection, attendance_collection

router = APIRouter()

# helper function to convert mongodb document to response
def employee_helper(employee) -> dict:
    return {
        "id": str(employee["_id"]),
        "employee_id": employee["employee_id"],
        "full_name": employee["full_name"],
        "email": employee["email"],
        "department": employee["department"]
    }

# Get all employees
@router.get("/", response_model=List[EmployeeResponse])
def get_all_employees():
    employees = []
    for emp in employees_collection.find():
        employees.append(employee_helper(emp))
    return employees

# Get single employee
@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: str):
    employee = employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_helper(employee)

# Create new employee
@router.post("/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate):
    # check if employee id already exists
    existing = employees_collection.find_one({"employee_id": employee.employee_id})
    if existing:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    
    # check if email already exists
    existing_email = employees_collection.find_one({"email": employee.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # validate fields
    if not employee.employee_id.strip():
        raise HTTPException(status_code=400, detail="Employee ID is required")
    if not employee.full_name.strip():
        raise HTTPException(status_code=400, detail="Full name is required")
    if not employee.department.strip():
        raise HTTPException(status_code=400, detail="Department is required")
    
    employee_dict = employee.dict()
    result = employees_collection.insert_one(employee_dict)
    new_employee = employees_collection.find_one({"_id": result.inserted_id})
    return employee_helper(new_employee)

# Delete employee
@router.delete("/{employee_id}")
def delete_employee(employee_id: str):
    result = employees_collection.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # also delete attendance records for this employee
    attendance_collection.delete_many({"employee_id": employee_id})
    
    return {"message": "Employee deleted successfully"}
