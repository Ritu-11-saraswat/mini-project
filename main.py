import os
import sys

# Ensure this path is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import uvicorn
from app.services.insights_engine import generate_insights

app = FastAPI(title="Nexus Student Risk Prediction API")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StudentData(BaseModel):
    student_id: str
    socioeconomic_status: str
    attendance_rate: float
    assignments_completed: int
    lms_login_frequency: int
    current_grade: float
    teacher_notes: str
    risk_probability: float

@app.get("/")
def read_root():
    return {"message": "Nexus Analytics API is running"}

@app.get("/api/students")
def get_students():
    # Attempt to read the generated data, else return nothing
    csv_path = os.path.join(os.path.dirname(__file__), "ml", "synthetic_student_data.csv")
    if os.path.exists(csv_path):
        try:
            # We return the top 50 rows for display in the dashboard
            df = pd.read_csv(csv_path).head(50)
            return df.to_dict(orient="records")
        except Exception as e:
            return {"error": str(e)}
    return []

@app.post("/api/insights")
def get_insights(student: StudentData):
    student_dict = student.dict()
    # Call our Insights Engine Service
    insights = generate_insights(student_dict, student.risk_probability)
    return insights

if __name__ == "__main__":
    print("Starting API Server... Once running, open frontend/index.html in your browser.")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
