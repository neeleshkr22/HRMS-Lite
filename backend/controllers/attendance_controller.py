from fastapi import APIRouter, HTTPException
from typing import List
from models.attendance_model import AttendanceCreate, AttendanceResponse
from config.database import employees_collection, attendance_collection

router = APIRouter()

# helper function
def attendance_helper(attendance) -> dict:
    return {
        "id": str(attendance["_id"]),
        "employee_id": attendance["employee_id"],
        "date": attendance["date"],
        "status": attendance["status"]
    }

# Get all attendance records
@router.get("/", response_model=List[AttendanceResponse])
def get_all_attendance():
    attendance_list = []
    for att in attendance_collection.find().sort("date", -1):
        attendance_list.append(attendance_helper(att))
    return attendance_list

# Get attendance for specific employee
@router.get("/{employee_id}", response_model=List[AttendanceResponse])
def get_employee_attendance(employee_id: str):
    # check if employee exists
    employee = employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    attendance_list = []
    for att in attendance_collection.find({"employee_id": employee_id}).sort("date", -1):
        attendance_list.append(attendance_helper(att))
    return attendance_list

# Mark attendance
@router.post("/", response_model=AttendanceResponse)
def mark_attendance(attendance: AttendanceCreate):
    # check if employee exists
    employee = employees_collection.find_one({"employee_id": attendance.employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # validate status
    if attendance.status not in ["Present", "Absent"]:
        raise HTTPException(status_code=400, detail="Status must be Present or Absent")
    
    # check if attendance already marked for this date
    existing = attendance_collection.find_one({
        "employee_id": attendance.employee_id,
        "date": attendance.date
    })
    
    if existing:
        # update existing attendance
        attendance_collection.update_one(
            {"_id": existing["_id"]},
            {"$set": {"status": attendance.status}}
        )
        updated = attendance_collection.find_one({"_id": existing["_id"]})
        return attendance_helper(updated)
    
    # create new attendance record
    attendance_dict = attendance.dict()
    result = attendance_collection.insert_one(attendance_dict)
    new_attendance = attendance_collection.find_one({"_id": result.inserted_id})
    return attendance_helper(new_attendance)
