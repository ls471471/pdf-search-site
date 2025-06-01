from flask import Flask, render_template, request, send_from_directory
import os
import json

app = Flask(__name__)
PDF_FOLDER = 'static/pdfs'

try:
    with open('name_map.json', 'r', encoding='utf-8') as f:
        name_map = {entry['name']: entry['file'] for entry in json.load(f)}
except FileNotFoundError:
    name_map = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    name = request.form['name'].strip()
    filename = name_map.get(name, f"{name}.pdf")
    file_path = os.path.join(PDF_FOLDER, filename)

    if os.path.exists(file_path):
        return render_template('viewer.html', name=name, filename=filename)
    else:
        return f"找不到 {name} 的個案費用表", 404

@app.route('/pdf/<filename>')
def serve_pdf(filename):
    return send_from_directory(PDF_FOLDER, filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
