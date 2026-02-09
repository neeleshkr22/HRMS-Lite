from pydantic import BaseModel

# Request model for marking attendance
class AttendanceCreate(BaseModel):
    employee_id: str
    date: str  # format: YYYY-MM-DD
    status: str  # Present or Absent

# Response model for attendance
class AttendanceResponse(BaseModel):
    id: str
    employee_id: str
    date: str
    status: str
