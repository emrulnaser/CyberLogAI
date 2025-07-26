from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

# Import logic from helper modules
from report.short_report import run_short_scan
from report.full_report import run_full_scan
from policy.checker import GDPRComplianceChecker

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB limit

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_uploaded_file(filepath):
    ext = filepath.rsplit('.', 1)[1].lower()
    content = ""
    try:
        if ext == 'txt' or ext == 'csv':
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        elif ext == 'pdf':
            import PyPDF2
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    content += page.extract_text() + "\n"
    except Exception as e:
        content = ""
    return content

@app.route('/')
def main_page():
    return render_template('Main_page.html')

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    error = None
    results = {"summary_text": "", "total_score": 0, "key_issues": [], "full_report": {}}
    scanned_text = None

    if request.method == 'POST':
        input_text = request.form.get('text', '').strip()
        file = request.files.get('file', None)
        file_content = ""

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            file_content = read_uploaded_file(save_path)
            os.remove(save_path)

        combined_text = input_text + "\n" + file_content if input_text or file_content else None

        if not combined_text or combined_text.strip() == "":
            error = "Please provide some text or upload a valid file."
        else:
            checker = GDPRComplianceChecker()
            scan_results = checker.check_compliance(combined_text)
            results = run_short_scan(scan_results)
            scanned_text = combined_text

    return render_template(
        'short_report.html',
        results=results.get('full_report', {}),
        error=error,
        scanned_text=scanned_text,
        summary_text=results.get('summary_text', ''),
        total_score=results.get('total_score', 0),
        key_issues=results.get('key_issues', [])
    )

@app.route('/full_report', methods=['GET', 'POST'])
def full_report():
    error = None
    results = None
    scanned_text = None
    overall_report = {}

    if request.method == 'POST':
        input_text = request.form.get('text_input', '').strip()
        file = request.files.get('file_input', None)
        file_content = ""

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            file_content = read_uploaded_file(save_path)
            os.remove(save_path)

        combined_text = (input_text + "\n" + file_content).strip() if (input_text or file_content) else None

        if not combined_text:
            error = "Please provide some text or upload a valid file."
        else:
            overall_report = run_full_scan(combined_text)
            results = overall_report.get("results", {})
            scanned_text = combined_text

    return render_template(
        'full_report.html',
        results=results,
        error=error,
        scanned_text=scanned_text,
        key_issues=overall_report.get('key_issues', ''),
        score=overall_report.get('score', 0),
        risk_level=overall_report.get('risk_level', 'Unknown'),
        summary=overall_report.get('summary', ''),
        total_compliance_score=overall_report.get('total_compliance_score', 'N/A'),
        compliant_articles=overall_report.get('compliant_articles', []), # Pass compliant articles
        partial_articles=overall_report.get('partial_articles', []),   # Pass partial articles
        non_compliant_articles=overall_report.get('non_compliant_articles', []) # Pass non-compliant articles
    )

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=10000, debug=True)
