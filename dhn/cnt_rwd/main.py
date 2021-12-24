from flask import Flask, render_template, request, redirect, url_for
import json, time
from rwd import RwdGsheet
app=Flask(__name__)

rowCnt = 0;
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

# 讓使用者名稱可以直接帶入輸入網頁。
@app.route('/cnt/?<string:userName>', methods=['GET'])
def cntRe(userName):
    try:
        userName = userName
        return render_template('rwd_cnt.html', **locals())
    except:
        return 'Error，請照指示使用。'

# 接收cnt網頁來的JS資料，轉送到google sheet。
@app.route('/addData',methods=['GET'])
def addData():
    global rowCnt
    try:
        htmlJson = request.values['returnData']
        htmlJson = json.loads(htmlJson)
        userName = htmlJson[-1]
        RwdGsheet.updateDataToGsheet(dataRearrange(htmlJson), 'rwd_demo', rowCnt)
        # print(dataRearrange(htmlJson))
        rowCnt += 1
        return redirect(url_for('cntRe', userName=userName))
    except:
        return 'Error，請照指示使用。'

# 整理網頁JS傳來的資料成想要的格式。
def dataRearrange(data) -> list:
    result = [None for i in range(8)]
    result[0] = data[0]
    result[1] = data[1]
    result[2], result[3] = dataInputRearrange(data[2])
    result[4], result[5] = data[3]['inputFree']
    result[7] = time.strftime("%Y/%m/%d_%H:%M:%S")
    result[6] = data[-1]

    return result

# 整理自動乘倍數的資料，轉成想要的格式
def dataInputRearrange(data) -> (str ,str):
    inputSum = data['sum']
    formula = ''
    # 要字串轉成int值，排序後才都會由小到大，不然會出現1、28、7這種順序排列。
    dataKeys = sorted([int(i) for i in data.keys() if i != 'sum'])
    # 轉出幾乘幾(x * x)的計算式出來。
    for k in dataKeys:
        formula += "{} * {} + ".format(k, data[str(k)])
    return (formula[:-3], inputSum)

if __name__ == "__main__":
    # 取得現在sheet的列數，這樣才不會把之前寫過的覆寫掉。
    rowCnt = len(RwdGsheet.getRowCnt('rwd_demo')['values']) + 1
    app.run(host="0.0.0.0", port=80)
    # RwdGsheet.createGsheet('rwd')
    # print(len(RwdGsheet.getRowCnt('rwd_demo')['values']))
