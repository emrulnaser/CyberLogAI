from flask import Flask, request
from policy import check_gdpr_compliance

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
    text = request.form["text"]
    results = check_gdpr_compliance(text)
    output = "<h2>🔍 GDPR Compliance Report</h2><ul>"
    for article, status in results.items():
        output += f"<li><strong>{article}:</strong> {status}</li>"
    output += "</ul><a href='/'>⬅️ Back</a>"
    return output

if __name__ == "__main__":
    app.run(debug=True)
