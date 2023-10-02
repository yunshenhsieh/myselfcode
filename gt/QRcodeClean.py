import datetime, os
import time

def main():
    qrCodeData = input("請掃描處方箋QR code：")
    if qrCodeData == "exit":
        return qrCodeData
    else:
        qrCodeData = qrCodeData.replace(";", "\n")
        fileName = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(os.getcwd() + "\\{}.txt".format(fileName), "w", encoding="utf-8-sig")as w:
            w.write(qrCodeData)

        os.startfile(os.getcwd() + "\\{}.txt".format(fileName))
        print("====檔案名稱：「{}」已生成。====".format(fileName))
        time.sleep(1)
        print("====若要關閉程式請輸入「exit」或直接關閉。\n")
        pass

if __name__ == "__main__":
    print("處方箋QR code整理程式")
    print("Version：1.1.0")
    print("製作人：謝昀燊")
    exeCode = None
    while True:
        exeCode = main()
        if exeCode == "exit":
            break
