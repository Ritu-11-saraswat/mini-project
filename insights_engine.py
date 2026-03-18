mport os

def generate_insights(student_data: dict, risk_probability: float):
    """
    A simulated GenAI service.
    If you have a real API key (OpenAI/Gemini), you would construct a prompt here
    passing the `student_data` and using the LLM to return these explanations.
    """
    
    # Analyze data for explanations
    reasons = []
    if student_data.get("attendance_rate", 1.0) < 0.8:
        reasons.append("The student has a noticeably low attendance rate, missing critical instructional time.")
    if student_data.get("lms_login_frequency", 50) < 30:
        reasons.append("Interaction with the online learning platform is severely limited.")
    if student_data.get("assignments_completed", 100) < 70:
        reasons.append("There is a pattern of missing or incomplete assignments.")
        
    explanation = " ".join(reasons) if reasons else "The student's core metrics indicate normal academic progression without significant flags."
    
    # Generate recommendations
    recommendation = ""
    if risk_probability > 0.7:
        recommendation += "High Priority Interventions:\n"
        recommendation += "- Schedule an immediate 1-on-1 meeting with the student.\n"
        recommendation += "- Connect the student with the peer tutoring center.\n"
        recommendation += "- Alert the academic advising team for comprehensive support."
    elif risk_probability > 0.4:
        recommendation += "Moderate Interventions:\n"
        recommendation += "- Send an automated check-in email to assess well-being.\n"
        recommendation += "- Monitor LMS course activity closely for the next week."
    else:
        recommendation += "No immediate intervention required. Continue standard monitoring."

    # Process unstructured data note
    notes = student_data.get("teacher_notes", "No recent notes provided.")
    
    return {
        "explanation": explanation,
        "recommendation": recommendation,
        "teacher_notes_summary": f"Synthesized from records: '{notes}'"
    }
