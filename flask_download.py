from flask import Flask,send_file
app=Flask(__name__)

@app.route('/download')
def downloadFile (): #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "D:/demo.txt"
    return send_file(path, as_attachment=True)

app.run(debug=True)
