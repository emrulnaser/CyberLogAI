
from flask import Flask, request
from policy import check_gdpr_compliance
import PyPDF2
import csv
import io
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return '''
        <h1>🛡️ GDPR Scanner</h1>
        <form method="post" action="/scan">
            <textarea name="text" rows="10" cols="60" placeholder="Paste your policy text here..."></textarea><br>
            <input type="submit" value="Scan GDPR Compliance">
        </form>
    '''

@app.route("/scan", methods=["POST"])
def scan():
    text_input = request.form.get("text", "")
    file = request.files.get("file")

    file_text = ""

    if file:
        filename = file.filename.lower()
        if filename.endswith(".txt"):
            file_text = file.read().decode("utf-8", errors="ignore")
        elif filename.endswith(".pdf"):
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                file_text += page.extract_text()
        elif filename.endswith(".csv"):
            stream = io.StringIO(file.stream.read().decode("utf-8", errors="ignore"))
            reader = csv.reader(stream)
            for row in reader:
                file_text += " ".join(row) + "\n"
        else:
            return "Unsupported file type. Please upload a .txt, .pdf, or .csv file."

    combined_text = text_input + "\n" + file_text
    results = check_gdpr_compliance(combined_text)

    output = "<h2>🔍 GDPR Compliance Report</h2><ul>"
    for article, status in results.items():
        output += f"<li><strong>{article}:</strong> {status}</li>"
    output += "</ul><a href='/'>⬅️ Back</a>"
    return output

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
