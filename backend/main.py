from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HRMS Lite API", version="1.0.0")

# CORS setup - allowing all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers with error handling
try:
    from controllers import employee_controller, attendance_controller, dashboard_controller
    app.include_router(employee_controller.router, prefix="/api/employees", tags=["Employees"])
    app.include_router(attendance_controller.router, prefix="/api/attendance", tags=["Attendance"])
    app.include_router(dashboard_controller.router, prefix="/api/dashboard", tags=["Dashboard"])
    print("All routers loaded successfully!")
except Exception as e:
    print(f"Error loading routers: {e}")

@app.get("/")
def root():
    return {"message": "HRMS Lite API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
