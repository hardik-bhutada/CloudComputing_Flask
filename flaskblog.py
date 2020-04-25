import os
from flask import *
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/hardik/PycharmProjects/CloudComputing/'
ALLOWED_EXTENSIONS = {'txt', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

file = ''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload')
def upload():
    return render_template("upload.html")


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = request.form['Word']
            print(result)
            check = comparisonMatch(filename, result)
            return render_template("success.html", name=file.filename, count=check)

        return render_template("upload.html")


def comparisonMatch(file, word):
    count =0
    fopen = open(file, mode='r+')

    fread = fopen.readlines()

    for line in fread:

        if word in line:
            count = count+1

    return count


if __name__ == '__main__':
    app.run(debug=True)
