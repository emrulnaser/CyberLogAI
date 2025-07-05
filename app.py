from flask import Flask, request, render_template
from utils.scanner import scan_text
import os

app = Flask(__name__)

# Create uploads folder if it doesn't exist
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None

    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file and uploaded_file.filename.endswith('.txt'):
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            results = scan_text(content)

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
