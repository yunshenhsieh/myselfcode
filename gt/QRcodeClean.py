import datetime, os
print("處方箋QR code整理程式")
print("Version：1.0.1")
print("製作人：謝昀燊")
qrCodeData = input("請掃描處方箋QR code：")
qrCodeData = qrCodeData.replace(";", "\n")
fileName = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
with open("{}.txt".format(fileName), "w", encoding="big5")as w:
    w.write(qrCodeData)
os.startfile(".\\{}.txt".format(fileName))
print("====檔案名稱：{}====".format(fileName))
input("======程式執行完畢，按enter結束程式======")
