import os, sys
from flask import Flask, flash, request, redirect, url_for,jsonify,send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime as date_time
from urllib.parse import urlparse
import time
from shutil import copyfile

BASE_URL = 'http://localhost:5000'

now = date_time.now()
UPLOAD_DIR = now.strftime("%Y%m%d")
MILLISECONDS = int(round(time.time() * 1000))

__IMAGE_FOLDER = '_image'
IMAGE_FOLDER = 'image'
__IMAGE_UPLOAD_FOLDER = __IMAGE_FOLDER+'/'+UPLOAD_DIR
IMAGE_UPLOAD_FOLDER = IMAGE_FOLDER+'/'+UPLOAD_DIR
IMAGE_ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
IMAGE_MAX_SIZE = 16 * 1024 * 1024;
#VIDEO CONFIG
__VIDEO_FOLDER = '_video'
VIDEO_FOLDER = 'video'
__VIDEO_UPLOAD_FOLDER = __VIDEO_FOLDER+'/'+UPLOAD_DIR
VIDEO_UPLOAD_FOLDER = VIDEO_FOLDER+'/'+UPLOAD_DIR
VIDEO_ALLOWED_EXTENSIONS = set(['mp4'])
VIDEO_MAX_SIZE = 16 * 1024 * 1024;

app = Flask(__name__)
app.config['IMAGE_UPLOAD_FOLDER'] = IMAGE_UPLOAD_FOLDER
app.config['VIDEO_UPLOAD_FOLDER'] = VIDEO_UPLOAD_FOLDER


@app.route('/azura/<source>/<pathdir>/<filename>')
def show_source(source, pathdir, filename):
    #folder = folder.replace("-", "/")
    #app.config['IMAGE_UPLOAD_FOLDER'] = IMAGE_UPLOAD_FOLDER
    # return jsonify({'filename':source+'/'+pathdir}),200
     return send_from_directory(source+'/'+pathdir,filename)


@app.route('/file/handling', methods=['GET', 'POST'])
def file_handling():
    url = request.args.get('url')
    data = urlparse(url)
    path = data.path
    opath = path.replace('/azura/','') 
    newpath = path.replace('/azura/_','')
    pathdir =newpath.replace(opath.split('/')[-1],'') 
    pathdir = pathdir.strip('/')
    folder_exit(pathdir)
    copyfile(opath, newpath)
    out = {
            'status': True,
            'code': 200,
            'message': 'success'
        }
    return jsonify(out),200 


def image_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in IMAGE_ALLOWED_EXTENSIONS

def video_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in VIDEO_ALLOWED_EXTENSIONS


def folder_exit(folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder, 777)
            return True;
    except OSError as exception:
        return;


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            out = {
                'status': False,
                'code': -1,
                'message': 'No file part '
                }
            return jsonify(out),200
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            out = {
                'status': False,
                'code': -2,
                'message': 'No selected file '
                }
            return jsonify(out),200
        if file and image_allowed_file(file.filename):
            filename = str(MILLISECONDS) + '_'+ file.filename
            filename = secure_filename(filename)
            folder_exit(__IMAGE_UPLOAD_FOLDER)
            file.save(os.path.join(__IMAGE_UPLOAD_FOLDER , filename)) 
            out = {
                'status': True,
                'code': 200,
                'url' :BASE_URL + url_for('show_source',source=__IMAGE_FOLDER, pathdir=UPLOAD_DIR, filename=filename),
                'message': ' success'
                }
            return jsonify(out), 200
            #return redirect(url_for('uploaded_image',filename=filename))


    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/video', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            out = {
                'status': False,
                'code': -1,
                'message': 'No video part '
                }
            return jsonify(out),200
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            out = {
                'status': False,
                'code': -2,
                'message': 'No selected video '
                }
            return jsonify(out),200
        if file and video_allowed_file(file.filename):
            filename = str(MILLISECONDS) + '_'+ file.filename
            filename = secure_filename(filename)
            folder_exit(__VIDEO_UPLOAD_FOLDER)
            file.save(os.path.join(__VIDEO_UPLOAD_FOLDER , filename))
            out = {
                'status': True,
                'code': 200,
                'url' :BASE_URL + url_for('show_source',source=__VIDEO_FOLDER, pathdir=UPLOAD_DIR, filename=filename),
                'message': ' success'
                }
            return jsonify(out), 200
            #return redirect(url_for('uploaded_image',filename=filename))


    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''



'''
@app.route('/upload_file', methods=['GET', 'POST'])
def uploadFile(current_user):

        format = "%Y-%m-%dT%H:%M:%S"
        now = datetime.datetime.utcnow().strftime(format)

        try:
            file = request.files['file']
        except:
            file = None
        try:
            url = request.form['url']
        except:
            url = None

        if file and allowed_file(file.filename):
            filename = now + '_' +str(current_user) + '_' + file.filename
            filename = secure_filename(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_uploaded = True

        elif url:
            file = urllib.urlopen(url)
            filename = url.split('/')[-1]
            filename = now + '_' +str(current_user) + '_' + filename
            filename = secure_filename(filename)

            if file and allowed_file(filename):

                open(os.path.join(app.config['UPLOAD_FOLDER'], filename),
                     'wb').write(file.read())
            file_uploaded = True

        else:
            filename = None
            file_uploaded = False

        return file_uploaded, filename 
'''

###############################SERVER#######################

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(port=6000, debug=True)

