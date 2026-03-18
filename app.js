const API_URL = 'http://127.0.0.1:8000';

document.getElementById('refresh-btn').addEventListener('click', fetchStudents);

document.getElementById('close-modal-btn').addEventListener('click', () => {
    document.getElementById('insight-modal').classList.remove('active');
});

async function fetchStudents() {
    const tbody = document.getElementById('students-body');
    const refreshBtn = document.getElementById('refresh-btn');
    
    // Loading State
    refreshBtn.innerText = "Loading...";
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding: 40px; color: var(--text-muted);">Fetching predictive data models...</td></tr>';
    
    try {
        const response = await fetch(`${API_URL}/api/students`);
        const data = await response.json();
        
        tbody.innerHTML = '';
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding: 40px;">No student data available. Please run data_generator.py in the backend first.</td></tr>';
            refreshBtn.innerText = "Fetch Latest Data";
            return;
        }

        data.forEach((student, index) => {
            const tr = document.createElement('tr');
            
            // Add slight animation stagger based on index
            tr.style.animation = `fadeIn 0.5s ease forwards ${index * 0.05}s`;
            tr.style.opacity = '0'; // Initial state for animation
            
            let riskClass = 'risk-low';
            let riskLabel = 'Low';
            let pillClass = 'pill-success';

            if (student.risk_probability > 0.6) { 
                riskClass = 'risk-high'; 
                riskLabel = 'High';
                pillClass = 'pill-danger';
            } else if (student.risk_probability > 0.3) { 
                riskClass = 'risk-medium'; 
                riskLabel = 'Medium';
                pillClass = 'pill-warning';
            }
            
            const riskPercentage = (student.risk_probability * 100).toFixed(1) + '%';
            
            // Format Data into TR
            tr.innerHTML = `
                <td><strong>${student.student_id}</strong></td>
                <td>${student.current_grade}%</td>
                <td>${(student.attendance_rate * 100).toFixed(1)}%</td>
                <td class="${riskClass}">
                    <span class="pill ${pillClass}" style="margin-right: 8px;">${riskLabel}</span>
                    <strong style="margin-right:8px;">${riskPercentage}</strong>
                </td>
                <td>
                    <button class="btn" style="padding: 8px 16px; font-size: 13px;" onclick='analyzeStudent(${JSON.stringify(student)})'>Deep Dive Insight</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding: 40px; color: var(--danger);">Failed to connect to Analytics API Backend. Verify FastAPI is running.</td></tr>';
    } finally {
        refreshBtn.innerText = "Fetch Latest Data";
    }
}

async function analyzeStudent(student) {
    // Setup initial UI states
    document.getElementById('modal-title').innerText = `Insights for ${student.student_id}`;
    
    const explanationNode = document.getElementById('modal-explanation');
    const recommendationNode = document.getElementById('modal-recommendation');
    const notesNode = document.getElementById('modal-notes');
    
    explanationNode.innerHTML = '<span style="color:var(--text-muted)">Generating AI Insights Pipeline...</span>';
    recommendationNode.innerHTML = '...';
    notesNode.innerHTML = '...';
    
    // Set pill
    const riskPill = document.getElementById('modal-risk-pill');
    if (student.risk_probability > 0.6) {
        riskPill.className = 'pill pill-danger risk-high';
        riskPill.innerText = 'High Risk';
    } else if (student.risk_probability > 0.3) {
        riskPill.className = 'pill pill-warning risk-medium';
        riskPill.innerText = 'Moderate Risk';
    } else {
        riskPill.className = 'pill pill-success risk-low';
        riskPill.innerText = 'Low Risk';
    }
    
    // Open Modal
    document.getElementById('insight-modal').classList.add('active');
    
    try {
        const response = await fetch(`${API_URL}/api/insights`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(student)
        });
        
        const insights = await response.json();
        
        // Populate Responses
        explanationNode.innerText = insights.explanation;
        recommendationNode.innerText = insights.recommendation;
        notesNode.innerText = insights.teacher_notes_summary;

    } catch (error) {
        explanationNode.innerHTML = '<span style="color:var(--danger)">Connection to Insights Engine Failed.</span>';
    }
}

// Global Animation helper
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);

// Run on load
fetchStudents();
