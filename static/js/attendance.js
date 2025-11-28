// DOM Elements
const loadTodayBtn = document.getElementById('loadToday');
const loadAllBtn = document.getElementById('loadAll');
const attendanceResults = document.getElementById('attendanceResults');
const loadingIndicator = document.getElementById('loadingIndicator');

// Load Today's Attendance
loadTodayBtn.addEventListener('click', async () => {
    loadingIndicator.style.display = 'block';
    attendanceResults.innerHTML = '';
    
    try {
        const response = await fetch('/attendance/today');
        const data = await response.json();
        
        loadingIndicator.style.display = 'none';
        
        if (data.success) {
            displayTodayAttendance(data.data);
        } else {
            showMessage('Error loading attendance: ' + data.message, 'error');
        }
    } catch (error) {
        loadingIndicator.style.display = 'none';
        showMessage('Error: ' + error.message, 'error');
    }
});

// Load All Attendance Records
loadAllBtn.addEventListener('click', async () => {
    loadingIndicator.style.display = 'block';
    attendanceResults.innerHTML = '';
    
    try {
        const response = await fetch('/attendance/all');
        const data = await response.json();
        
        loadingIndicator.style.display = 'none';
        
        if (data.success) {
            displayAllAttendance(data.data);
        } else {
            showMessage('Error loading attendance: ' + data.message, 'error');
        }
    } catch (error) {
        loadingIndicator.style.display = 'none';
        showMessage('Error: ' + error.message, 'error');
    }
});

// Display Today's Attendance
function displayTodayAttendance(attendance) {
    const { date, records } = attendance;
    
    let html = `
        <div class="date-section">
            <h3>📅 ${formatDate(date)}</h3>
    `;
    
    if (Object.keys(records).length === 0) {
        html += `<p class="placeholder">No attendance records for today</p>`;
    } else {
        html += '<div class="attendance-grid">';
        
        for (const [studentId, record] of Object.entries(records)) {
            html += `
                <div class="attendance-card">
                    <h4>${studentId}</h4>
                    <span class="status present">${record.status}</span>
                    <div class="timestamp">⏰ ${record.timestamp}</div>
                </div>
            `;
        }
        
        html += '</div>';
        html += `
            <div style="margin-top: 20px; padding: 15px; background: white; border-radius: 8px;">
                <strong>Total Present:</strong> ${Object.keys(records).length}
            </div>
        `;
    }
    
    html += '</div>';
    attendanceResults.innerHTML = html;
}

// Display All Attendance Records
function displayAllAttendance(attendanceList) {
    if (attendanceList.length === 0) {
        attendanceResults.innerHTML = `<p class="placeholder">No attendance records found</p>`;
        return;
    }
    
    let html = '';
    
    attendanceList.forEach(attendance => {
        const { date, records } = attendance;
        
        html += `
            <div class="date-section">
                <h3>📅 ${formatDate(date)}</h3>
        `;
        
        if (Object.keys(records).length === 0) {
            html += `<p class="placeholder">No records for this date</p>`;
        } else {
            html += '<div class="attendance-grid">';
            
            for (const [studentId, record] of Object.entries(records)) {
                html += `
                    <div class="attendance-card">
                        <h4>${studentId}</h4>
                        <span class="status present">${record.status}</span>
                        <div class="timestamp">⏰ ${record.timestamp}</div>
                    </div>
                `;
            }
            
            html += '</div>';
            html += `
                <div style="margin-top: 15px; padding: 12px; background: white; border-radius: 8px;">
                    <strong>Total Present:</strong> ${Object.keys(records).length}
                </div>
            `;
        }
        
        html += '</div>';
    });
    
    attendanceResults.innerHTML = html;
}

// Format Date
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

// Show Message
function showMessage(message, type) {
    const messageBox = document.getElementById('messageBox');
    messageBox.textContent = message;
    messageBox.className = `message-box ${type} show`;
    
    setTimeout(() => {
        messageBox.classList.remove('show');
    }, 4000);
}
