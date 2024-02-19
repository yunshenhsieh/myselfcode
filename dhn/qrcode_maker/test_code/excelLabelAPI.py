import qrcode, os
from qrcode import constants
import openpyxl
from openpyxl.drawing.image import Image

def qrcodeMaker(drugCode: str, barcodeNumber: str, qrSize: str, errorCorrection: constants) -> str:
    qr = qrcode.QRCode(
        error_correction=errorCorrection,
        border=2,
    )
    qr.add_data(barcodeNumber)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((int(qrSize), int(qrSize)))
    img.save(".\\history\\{}_{}.png".format(drugCode, barcodeNumber))
    qrcodePath = ".\\history\\{}_{}.png".format(drugCode, barcodeNumber)

    return qrcodePath

def insertPictureToExcel(layoutExcelPath: str, layoutExcelSheetName: str, qrcodePath: str, insertQRcodeCell: str):
    wb = openpyxl.load_workbook(layoutExcelPath)
    ws = wb[layoutExcelSheetName]
    print(ws.title)
    print(ws["H6"].value)

    qrcodePicture = Image(qrcodePath)
    ws.add_image(qrcodePicture, insertQRcodeCell)

    wb.save("test.xlsx")
    pass

def drugFileLocation(drugFilePath: str, appearanceFilePath: str) -> list[str]:
    with open(drugFilePath, "r", encoding="big5-hkscs")as f:
        drugFile = f.readlines()
    with open(appearanceFilePath, "r", encoding="big5-hkscs")as f:
        appearanceFile = f.readlines()

    return drugFile, appearanceFile

def checkIndex(drugFile: list[str], appearanceFile: list[str]) -> int:
    drugFileColumn = drugFile[0].split(";")
    MaterialNumIndex = drugFileColumn.index("藥品編號")
    drugCodeIndex = drugFileColumn.index("料位號")
    drugNameIndex = drugFileColumn.index("標籤藥品名")
    drugSpecificationIndex = drugFileColumn.index("標籤規格")
    barcodeNumberIndex = drugFileColumn.index("條碼")

    maxLengthNum = max([MaterialNumIndex, drugCodeIndex, drugNameIndex, drugSpecificationIndex, barcodeNumberIndex]) + 1
    tmpList = []
    drugFileMaterialRowNumDict = {}
    for n, singalData in enumerate(drugFile):
        singalData = singalData.split(";")
        if len(singalData) < maxLengthNum :
            drugFileMaterialRowNumDict[singalData[MaterialNumIndex]] = n
        else:
            drugFileMaterialRowNumDict[singalData[MaterialNumIndex]] = n
            tmpList.append(singalData)

    drugFileFeatureIndexList = [drugCodeIndex, drugNameIndex, drugSpecificationIndex, barcodeNumberIndex]
    drugCodeToMaterialNumDict = {singalDataList[drugCodeIndex] : singalDataList[MaterialNumIndex] for singalDataList in tmpList}



    appearanceFileColumn = appearanceFile[0].split(",")
    drugColorIndex = appearanceFileColumn.index("顏色")
    drugShapeIndex = appearanceFileColumn.index("形狀")
    drugDosageFormIndex = appearanceFileColumn.index("劑型")
    drugOtherDescriptionIndex = appearanceFileColumn.index("中文加強描述")

    appearanceMaterialRowNumDict = {dataList.split(",")[0] : n for n, dataList in enumerate(appearanceFile) }
    appearanceFeatureIndexList = [drugColorIndex, drugShapeIndex, drugDosageFormIndex, drugOtherDescriptionIndex]


    return drugFileMaterialRowNumDict, drugFileFeatureIndexList, drugCodeToMaterialNumDict, appearanceMaterialRowNumDict, appearanceFeatureIndexList

if __name__ == "__main__":

    drugFile, appearanceFile = drugFileLocation("../Adgn.txt", "../MYE_data.csv")
    featureList = checkIndex(drugFile, appearanceFile)

    drugFileMaterialRowNumDict = featureList[0]
    drugFileFeatureIndexList = featureList[1]
    drugCodeToMaterialNumDict = featureList[2]

    appearanceMaterialRowNumDict = featureList[3]
    appearanceFeatureIndexList = featureList[4]
