from fastapi import APIRouter
from config.database import employees_collection, attendance_collection
from datetime import date

router = APIRouter()

@router.get("")
@router.get("/")
def get_dashboard():
    total_employees = employees_collection.count_documents({})
    
    today = str(date.today())
    total_present_today = attendance_collection.count_documents({
        "date": today,
        "status": "Present"
    })
    total_absent_today = attendance_collection.count_documents({
        "date": today,
        "status": "Absent"
    })
    
    return {
        "total_employees": total_employees,
        "present_today": total_present_today,
        "absent_today": total_absent_today
    }
