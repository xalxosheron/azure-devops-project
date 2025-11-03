from flask import Flask, render_template, request, jsonify
import os
import socket
from datetime import datetime
import docx2txt
import PyPDF2

app = Flask(__name__)

# ---------- HOME ROUTE ----------
@app.route('/')
def home():
    return render_template('index.html',
                           hostname=socket.gethostname(),
                           timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           environment=os.getenv('ENVIRONMENT', 'development'),
                           version=os.getenv('VERSION', '1.0.0'))

# ---------- HEALTH CHECK ----------
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'hostname': socket.gethostname()
    }), 200

# ---------- APP INFO ----------
@app.route('/api/info')
def info():
    return jsonify({
        'application': 'AI ATS Analyzer',
        'version': os.getenv('VERSION', '1.0.0'),
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'hostname': socket.gethostname()
    })

# ---------- RESUME ANALYSIS ROUTE ----------
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files or 'job_description' not in request.form:
        return jsonify({'error': 'Please upload resume and enter job description'}), 400

    resume_file = request.files['resume']
    job_description = request.form['job_description']

    # Extract text from uploaded resume
    resume_text = extract_text(resume_file)

    # --- Mock AI Matching Logic (replace with actual AI model later) ---
    match_score, feedback = mock_ai_analysis(resume_text, job_description)

    return jsonify({
        'match_score': match_score,
        'feedback': feedback,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


# ---------- HELPER FUNCTIONS ----------
def extract_text(file):
    """Extract text from PDF or DOCX files."""
    text = ""
    if file.filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    elif file.filename.endswith('.docx'):
        text = docx2txt.process(file)
    else:
        text = file.read().decode('utf-8', errors='ignore')
    return text


def mock_ai_analysis(resume_text, job_description):
    """Simple keyword-based matching to simulate AI scoring."""
    resume_words = set(resume_text.lower().split())
    jd_words = set(job_description.lower().split())
    overlap = len(resume_words.intersection(jd_words))
    score = min(100, int((overlap / len(jd_words)) * 100)) if jd_words else 0

    feedback = "Good match! Your resume aligns well." if score > 70 else \
               "Moderate match. Add more skills from the job description." if score > 40 else \
               "Low match. Try tailoring your resume more closely."

    return score, feedback


# ---------- MAIN ----------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)