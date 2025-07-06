
from flask import Flask, request, render_template
from policy import check_gdpr_compliance
import PyPDF2
import csv
import io
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    text_input = request.form.get("text", "")
    file = request.files.get("file")

    file_text = ""

    if file and file.filename:
        filename = file.filename.lower()
        if filename.endswith(".txt"):
            file_text = file.read().decode("utf-8", errors="ignore")
        elif filename.endswith(".pdf"):
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                file_text += page.extract_text() or ""
        elif filename.endswith(".csv"):
            stream = io.StringIO(file.stream.read().decode("utf-8", errors="ignore"))
            reader = csv.reader(stream)
            for row in reader:
                file_text += " ".join(row) + "\n"
        else:
            return "Unsupported file type. Please upload a .txt, .pdf, or .csv file."

    combined_text = text_input + "\n" + file_text
    results = check_gdpr_compliance(combined_text)

    return render_template("index.html", results=results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
