import pandas as pd
import numpy as np
import random
import os

def generate_structured_data(num_students=500):
    """
    Generates synthetic structured data for students.
    Includes slightly biased relationships for demonstration of bias mitigation later.
    """
    np.random.seed(42)
    random.seed(42)
    
    data = []
    for i in range(num_students):
        student_id = f"STU{i:04d}"
        
        # Base demographics (simplified)
        socioeconomic_status = np.random.choice(["High", "Medium", "Low"], p=[0.2, 0.5, 0.3])
        
        # Introduce a slight bias in base resources that affects other metrics
        # (This represents real-world systemic issues we want our AI to be fair about)
        resource_modifier = {"High": 1.1, "Medium": 1.0, "Low": 0.9}[socioeconomic_status]
        
        # Behavioral and Academic Metrics
        attendance_rate = float(np.clip(np.random.normal(0.85 * resource_modifier, 0.1), 0.4, 1.0))
        assignments_completed = int(np.clip(np.random.normal(80 * resource_modifier, 15), 10, 100))
        lms_login_frequency = int(np.clip(np.random.normal(50 * resource_modifier, 20), 5, 120))
        
        # Current Grade is correlated with behaviors
        base_grade = (attendance_rate * 40) + (assignments_completed * 0.4) + (lms_login_frequency * 0.1)
        noise = np.random.normal(0, 5)
        current_grade = float(np.clip(base_grade + noise, 0, 100))
        
        # Calculate a continuous "Risk Probability"
        # High risk if grade is low, attendance is low, and LMS activity is low
        risk_score = (100 - current_grade) * 0.5 + (1.0 - attendance_rate) * 30 + (100 - lms_login_frequency) * 0.2
        risk_probability = float(np.clip(risk_score / 100, 0.0, 1.0))
        
        # Generate some synthetic unstructured "teacher notes"
        notes_pool_good = [
            "Actively participates in class.",
            "Always prepared for lectures.",
            "Shows great enthusiasm.",
            "Helps peers with assignments."
        ]
        notes_pool_bad = [
            "Seems distracted during lessons.",
            "Missed several recent deadlines.",
            "Struggling with core concepts.",
            "Needs frequent reminders to stay on task."
        ]
        
        if risk_probability > 0.6:
            teacher_notes = " ".join(random.sample(notes_pool_bad, k=random.randint(1, 2)))
        elif risk_probability < 0.3:
            teacher_notes = " ".join(random.sample(notes_pool_good, k=random.randint(1, 2)))
        else:
            teacher_notes = random.choice(notes_pool_good + notes_pool_bad)
            
        data.append({
            "student_id": student_id,
            "socioeconomic_status": socioeconomic_status,
            "attendance_rate": round(attendance_rate, 2),
            "assignments_completed": assignments_completed,
            "lms_login_frequency": lms_login_frequency,
            "current_grade": round(current_grade, 2),
            "teacher_notes": teacher_notes,
            "risk_probability": round(risk_probability, 3)
        })
        
    df = pd.DataFrame(data)
    
    # Save the dataset
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    file_path = os.path.join(os.path.dirname(__file__), "synthetic_student_data.csv")
    df.to_csv(file_path, index=False)
    print(f"Generated {num_students} student records at {file_path}")
    
    return df

if __name__ == "__main__":
    generate_structured_data()
