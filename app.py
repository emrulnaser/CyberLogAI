from flask import Flask, request, render_template
from utils.scanner import scan_text
import os
from policy import check_gdpr_compliance

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
# You can add app.config for upload folder if you want:
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Put your route here
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            # Extract text from uploaded file
            text = scan_text(uploaded_file)

            # Run GDPR compliance check
            gdpr_report = check_gdpr_compliance(text)

            # Pass results to your HTML template
            return render_template("result.html", report=gdpr_report)
    return render_template("upload.html")


# Other routes below...

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render will set this
    app.run(host='0.0.0.0', port=port)         # Host must be 0.0.0.0
from flask import Flask, request, render_template_string
from policy import check_gdpr_compliance

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return '''
        <h1>🛡️ GDPR Scanner</h1>
        <form action="/scan" method="post">
            <textarea name="text" rows="10" cols="60" placeholder="Paste your policy text here..."></textarea><br>
            <input type="submit" value="Scan GDPR Compliance">
        </form>
    '''

@app.route("/scan", methods=["POST"])
def scan():
    text = request.form["text"]
    results = check_gdpr_compliance(text)
    output = "<h2>🔍 GDPR Compliance Report</h2><ul>"
    for article, status in results.items():
        output += f"<li><strong>{article}:</strong> {status}</li>"
    output += "</ul><a href='/'>⬅️ Back</a>"
    return output

if __name__ == "__main__":
    app.run(debug=True)

