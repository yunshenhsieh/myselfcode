from flask import Flask, render_template, request, redirect, url_for
import json
app=Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html',**locals())

@app.route('/cnt',methods=['GET'])
def cnt():
    try:
        userName = request.values['userName']
        return render_template('rwd_cnt.html', **locals())
    except:
        return 'Error，請照指示使用。'

@app.route('/cnt/?<string:userName>', methods=['GET'])
def cntRe(userName):
    try:
        userName = userName
        return render_template('rwd_cnt.html', **locals())
    except:
        return 'Error，請照指示使用。'

@app.route('/addData',methods=['GET'])
def addData():
    try:
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
    except:
        return 'Error，請照指示使用。'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
