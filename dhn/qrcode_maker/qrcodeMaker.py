import qrcode, os
from qrcode import constants

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
    pass

def drugFileLocation(drugFilePath: str) -> list[str]:
    with open(drugFilePath, "r", encoding="big5-hkscs")as f:
        drugFile = f.readlines()

    return drugFile

def drugCodeClean(drugFile: list[str], drugCodeIndex: int, barcodeNumberIndex: int) -> dict:
    maxLength = barcodeNumberIndex + 1
    if drugCodeIndex + 1 > barcodeNumberIndex:
        maxLength = drugCodeIndex + 1

    drugFile = [singalData.split(";") for singalData in drugFile]
    drugCodeAndBarcodeNumberDict = {}

    for singalDataList in drugFile:
        if len(singalDataList) < maxLength:
            continue
        elif singalDataList[drugCodeIndex] != "":
            drugCodeAndBarcodeNumberDict[singalDataList[drugCodeIndex]] = singalDataList[barcodeNumberIndex]

    return drugCodeAndBarcodeNumberDict

def checkDrugCodeAndBarcodeNumberIndex(drugFile: list[str]) -> int:
    drugFileColumn = drugFile[0].split(";")
    drugCodeIndex, barcodeNumberIndex = drugFileColumn.index("料位號"), drugFileColumn.index("條碼")

    return drugCodeIndex, barcodeNumberIndex

if __name__ == "__main__":
    print("Version 1.0.0")
    print("製作：謝昀燊(Vincent Xie)")
    if os.path.isdir(".\\history"):
        pass
    else:
        os.makedirs("history")

    locationPath = os.getcwd()
    if os.path.isfile(".\\Adgn.txt"):
        pass
    else:
        input("請將drug檔放至 {} 資料夾內，並將檔名改成「Adgn.txt」。".format(locationPath))

    if os.path.isfile(".\\env"):
        pass
    else:
        input("Miss environment setting file「env」")
    with open(".\\env", "r", encoding="utf-8")as f:
        envList = [env.split("|") for env in f.readlines()]
    envSettleDict = {env[0].strip() : env[1].strip() for env in envList}

    errorCorrectionDict = {0 : constants.ERROR_CORRECT_L,
                       1 : constants.ERROR_CORRECT_M,
                       2 : constants.ERROR_CORRECT_Q,
                       3 : constants.ERROR_CORRECT_H}

    drugFilePath = locationPath + "\\Adgn.txt"
    drugFile = drugFileLocation(drugFilePath)
    drugCodeIndex, barcodeNumberIndex = checkDrugCodeAndBarcodeNumberIndex(drugFile)
    drugCodeAndBarcodeNumberDict = drugCodeClean(drugFile, drugCodeIndex, barcodeNumberIndex)

    drugCodeAndBarcodeNumberDictKeyTuple = tuple(drugCodeAndBarcodeNumberDict.keys())
    while True:
        drugCode = input("請輸入 料位號：").strip().upper()
        if drugCode not in drugCodeAndBarcodeNumberDictKeyTuple:
            print("無此 料位藥，請重新輸入。")
        else:
            barcodeNumber = drugCodeAndBarcodeNumberDict[drugCode]
            qrcodeMaker(drugCode, barcodeNumber, envSettleDict["size"], errorCorrectionDict[int(envSettleDict["error_correction"])])
