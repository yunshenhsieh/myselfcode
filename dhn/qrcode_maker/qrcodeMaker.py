import qrcode, os
import xlwings
from qrcode import constants
import xlwings as xw

def qrcodeMaker(drugCode: str, barcodeNumber: str, qrSize: str, errorCorrection: constants):
    qr = qrcode.QRCode(
        error_correction=errorCorrection,
        border=2,
    )
    qr.add_data(barcodeNumber)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((int(qrSize), int(qrSize)))
    img.save(".\\history\\{}_{}.png".format(drugCode, barcodeNumber))
    print("{} QRcode已存入{}\\history\\{}_{}.png".format(drugCode, os.getcwd(), drugCode, barcodeNumber))
    qrcodePath = os.getcwd() + ".\\history\\{}_{}.png".format(drugCode, barcodeNumber)
    return qrcodePath

def checkBarcodeAndExecute(codeNum: str, envSettleDict: dict, errorCorrectionDict: dict, wx: xlwings.sheets, rng: xlwings.sheets):
    if wx[envSettleDict["barcode_cell"]].value != None:
        barcodeNumber = int(wx[envSettleDict["barcode_cell"]].value)
        qrcodePath = qrcodeMaker(codeNum, barcodeNumber, envSettleDict["size"],
                                 errorCorrectionDict[int(envSettleDict["error_correction"])])

        wx.pictures.add(qrcodePath, top=rng.top, left=rng.left)
        wx.range(envSettleDict["print_range"]).api.PrintOut(Copies=1, ActivePrinter=envSettleDict["printer_name"], Collate=True)
    else:
        wx[envSettleDict["barcode_cell"]].value == ""
        print("無此 料位號 或 材編的條碼。")
    pass

if __name__ == "__main__":
    print("Version 1.2.0")
    print("製作：謝昀燊(Vincent Xie)")
    if os.path.isdir(".\\history"):
        pass
    else:
        os.makedirs("history")

    if os.path.isfile(".\\env"):
        pass
    else:
        input("Miss environment setting file「env」")
    with open(".\\env", "r", encoding="utf-8")as f:
        envList = [env.split("=") for env in f.readlines()]
    envSettleDict = {env[0].strip() : env[1].strip() for env in envList}
    drugCodeCell = envSettleDict["drug_code_cell"]
    materialCodeCell = envSettleDict["material_code_cell"]

    errorCorrectionDict = {0 : constants.ERROR_CORRECT_L,
                       1 : constants.ERROR_CORRECT_M,
                       2 : constants.ERROR_CORRECT_Q,
                       3 : constants.ERROR_CORRECT_H}

    wb = xw.Book(envSettleDict["excel_path"])
    wx = wb.sheets[envSettleDict["sheet_name"]]
    rng = wb.sheets[envSettleDict["sheet_name"]].range(envSettleDict["qrcode_cell"])

    while True:
        codeNum = input("請輸入 料位號 或 材編：").strip().upper()
        if len(codeNum) == 3:
            wx[drugCodeCell].value = ""
            wx[materialCodeCell].value = ""
            wx[drugCodeCell].value = codeNum
            checkBarcodeAndExecute(codeNum, envSettleDict, errorCorrectionDict, wx, rng)

        else:
            wx[drugCodeCell].value = ""
            wx[materialCodeCell].value = ""
            wx[materialCodeCell].value = codeNum
            checkBarcodeAndExecute(codeNum, envSettleDict, errorCorrectionDict, wx, rng)
