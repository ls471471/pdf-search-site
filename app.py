from flask import Flask, render_template, request, send_from_directory, abort
import os
import re

app = Flask(__name__)

PDF_FOLDER = os.path.join('static', 'pdfs')
app.config['PDF_FOLDER'] = PDF_FOLDER

def clean_filename(name):
    # 移除標點符號與全形符號
    return re.sub(r'[^\w\u4e00-\u9fff]', '', name)

@app.route('/', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST']) 

def index():
    filename = None
    not_found = False

    if request.method == 'POST':
        name_input = request.form['name'].strip()
        name_input_clean = clean_filename(name_input)

        matched = None

        for file in os.listdir(PDF_FOLDER):
            file_clean = clean_filename(file)
            if name_input_clean in file_clean:
                matched = file
                break

        if matched:
            filename = matched
        else:
            not_found = True

    return render_template('index.html', filename=filename, not_found=not_found)

@app.route('/pdf/<path:filename>')
def get_pdf(filename):
    try:
        return send_from_directory(PDF_FOLDER, filename)
    except:
        abort(404)

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
