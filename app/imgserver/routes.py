import os
from flask import flash, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from app import app
UPLOAD_FOLDER = '../DB/details'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
REMOVE_FOLDER = '../DB/removed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REMOVE_FOLDER'] = REMOVE_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/images/<dirname>/<filename>')
def images_endpoint(dirname, filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'],
                                  dirname, filename))
@app.route('/recovery/<dirname>/<filename>')
def images_rec(dirname, filename):
    return send_file(os.path.join(app.config['REMOVE_FOLDER'], dirname, filename))

@app.route('/recover/<dirname>/<filename>')
def recover(dirname,filename):
    os.replace(os.path.join(app.config['REMOVE_FOLDER'],dirname, filename),os.path.join(app.config['UPLOAD_FOLDER'], dirname, filename))
    return redirect(os.path.join('../../Removed', dirname))
@app.route('/remove/images/<dirname>/<filename>')
def move(dirname,filename):
    if not os.path.exists(os.path.join(app.config['REMOVE_FOLDER'], dirname)):
        os.makedirs(os.path.join(app.config['REMOVE_FOLDER'], dirname))
    os.replace(os.path.join(app.config['UPLOAD_FOLDER'],dirname, filename),os.path.join(app.config['REMOVE_FOLDER'], dirname, filename))
    return redirect(os.path.join('../../details', dirname))

@app.route('/removed/<foldername>', methods=['GET'])
def recovery_images(foldername):
    if not os.path.exists(os.path.join(app.config['REMOVE_FOLDER'], foldername)):
        os.makedirs(os.path.join(app.config['REMOVE_FOLDER'], foldername))
    context = {"foldername": foldername,
                "images_list": os.listdir(os.path.join(app.config['REMOVE_FOLDER'], foldername))}
    return render_template("recovery_images.html", **context)
@app.route('/details/<foldername>', methods=['GET', 'POST'])
def images_gallery(foldername):
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], foldername)):
        os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], foldername), mode=0o777)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], foldername, filename))
    context = {"foldername": foldername,
                "images_list": os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], foldername))}
    return render_template("images_gallery.html", **context)