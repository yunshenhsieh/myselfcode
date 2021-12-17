from flask import Flask, render_template, request, redirect, url_for
import json
app=Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html',**locals())

@app.route('/cnt',methods=['GET'])
def cnt():
    userName = request.values['userName']
    return render_template('rwd_cnt.html', **locals())

@app.route('/cnt/?<string:userName>', methods=['GET'])
def cntRe(userName):
    userName = userName
    return render_template('rwd_cnt.html', **locals())

@app.route('/addData',methods=['GET'])
def addData():
    v = request.values['returnData']
    print(v)
    print(type(v))
    v = json.loads(v)
    print(v)
    print(type(v))
    print('cnt')
    print(type(v[0]))
    userName = v[0]
    return redirect(url_for('cntRe', userName=userName))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
