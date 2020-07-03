import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'D:/uploadtest/'
ALLOWED_EXTENSIONS = set(['xls','xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        dirkey=True
        storage_dir = app.config['UPLOAD_FOLDER'] + file.filename.replace('.','')
        num=0
        tmp_dir=''
        while dirkey:
            if not os.path.exists(storage_dir):
                os.mkdir(storage_dir)
                break
            else:
                num+=1
                tmp_dir=file.filename.replace('.','') + str(num)
                storage_dir = app.config['UPLOAD_FOLDER'] + tmp_dir

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            storage_dir=os.path.join(storage_dir, filename)
            file.save(storage_dir)
            # 下面是導去下載csv頁面
            if tmp_dir == '':tmp_dir = file.filename.replace('.','')
            return redirect(url_for('download_csv',
                                    filename=filename,tmp_dir=tmp_dir))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

from flask import send_from_directory

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

@app.route("/download_csv/<tmp_dir>/<filename>")
def download_csv(tmp_dir,filename):
    dirpath = 'D:\\uploadtest\\'+ tmp_dir  # 這個資料夾是要讓別人下載檔案的資料夾
    # print(dirpath)
    csv_list=[]
    csv_file= os.listdir(dirpath)
    for csv_file in csv_file:
        if csv_file.endswith('.csv'):
            csv_list.append(csv_file)
    # 透過flask內建的send_from_directory
    return send_from_directory(dirpath, filename, as_attachment=True)  # as_attachment=True 一定要寫，不然會變開啟，不是下載
    return '''
        <!doctype html>
        <title>Download CSV File</title>
        <h1>Download CSV File</h1>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
        '''
if __name__ == '__main__':
    app.run(debug=True)