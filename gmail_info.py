from email.mime.text import MIMEText
import smtplib

def send_mail_for_me():
    '利用 Gmail 的服務寄發通知信'
    send_gmail_user = 'xieworker@gmail.com'
    send_gmail_password = 'g7054913'
    rece_gmail_user = 'xieworker@gmail.com'

    msg = MIMEText('imdb預算及海報爬蟲已停止')

    msg['Subject'] = ('爬蟲異常終止')
    msg['From'] = send_gmail_user
    msg['To'] = rece_gmail_user

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(send_gmail_user, send_gmail_password)
    server.send_message(msg)
    server.quit()