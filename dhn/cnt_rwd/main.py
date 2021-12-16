from flask import Flask, send_file, render_template, request, redirect
import json
app=Flask(__name__)

@app.route('/')
def index():
    ab =1234
    cd ='456'
    return render_template('rwd_cnt.html',**locals())

@app.route('/a/cnt',methods=['GET'])
def cnt():
    v = request.values['returnData']
    print(v)
    print(type(v))
    v = json.loads(v)
    print(v)
    print(type(v))
    free = request.values['multiSumFree']
    print(json.loads(free))
    print('cnt')
    return redirect('/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
