from flask import Flask, request, render_template, redirect, url_for
from policy import GDPRComplianceChecker
import PyPDF2
import csv
import io
import os
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Initialize the compliance checker instance once
checker = GDPRComplianceChecker()

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    text_input = request.form.get("text", "").strip()
    file = request.files.get("file")
    file_text = ""

    if file and file.filename:
        try:
            filename = file.filename.lower()
            raw_bytes = file.read()

            if filename.endswith(".txt"):
                file_text = raw_bytes.decode("utf-8", errors="ignore")

            elif filename.endswith(".pdf"):
                reader = PyPDF2.PdfReader(io.BytesIO(raw_bytes))
                file_text = " ".join(page.extract_text() or "" for page in reader.pages)

            elif filename.endswith(".csv"):
                stream = io.StringIO(raw_bytes.decode("utf-8", errors="ignore"))
                file_text = "\n".join(",".join(row) for row in csv.reader(stream))

            else:
                return render_template("index.html", error="Unsupported file type")

        except Exception as e:
            app.logger.error(f"File processing error: {str(e)}")
            return render_template("index.html", error=f"Error processing file: {str(e)}")

    combined_text = f"{text_input}\n{file_text}".strip()

    if not combined_text:
        return render_template("index.html", error="No text provided for scanning")

    try:
        results = checker.check_compliance(combined_text)
        return render_template(
            "index.html",
            results=results,
            scanned_text=combined_text[:500] + "..." if len(combined_text) > 500 else combined_text
        )
    except Exception as e:
        app.logger.error(f"Scanning error: {str(e)}")
        return render_template("index.html", error=f"Scanning failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
