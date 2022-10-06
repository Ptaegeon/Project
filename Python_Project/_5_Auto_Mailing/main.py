import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase


def send_email(smtp_info, msg):
    with smtplib.SMTP(smtp_info["smtp_sever"], smtp_info["smtp_port"]) as server:

        server.starttls()
        server.login(smtp_info["smtp_user_id"], smtp_info["smtp_user_pw"])

        response = server.sendmail(msg['from'], msg['to'], msg.as_string())

        if not response:
            print('성공')
        else:
            print(response)

def make_multimsg(msg_dict):
    multi = MIMEMultipart(_subtype='mixed')

    for key, value in msg_dict.items():
        # 각 타입에 적절한 MIMExxx() 함수를 호출하여 msg 객체를 생성한다.
        if key == 'text':
            with open(value['filename'], encoding='utf-8') as fp:
                msg = MIMEText(fp.read(), _subtype=value['subtype'])
        elif key == 'image':
            with open(value['filename'], 'rb') as fp:
                msg = MIMEImage(fp.read(), _subtype=value['subtype'])
        elif key == 'audio':
            with open(value['filename'], 'rb') as fp:
                msg = MIMEAudio(fp.read(), _subtype=value['subtype'])
        else:
            with open(value['filename'], 'rb') as fp:
                msg = MIMEBase(value['maintype'], _subtype=value['subtype'])
                msg.set_payload(fp.read())
                encoders.encode_base64(msg)
        # 파일 이름을 첨부파일 제목으로 추가
        msg.add_header('Content-Disposition', 'attachment',
                       filename=os.path.basename(value['filename']))
        # 첨부파일 추가
        multi.attach(msg)

    return multi


smtp_info = dict({"smtp_sever": "smtp.naver.com",
                  "smtp_user_id": "bibersay26@naver.com",
                  "smtp_user_pw": "1qa@WS3ed",
                  "smtp_port": "587"})

title = "test email"
content = "test content"
sender = smtp_info['smtp_user_id']
receiver = "bibersay@nate.com"

msg_dict = {
    'text' : {'maintype' : 'text', 'subtype' :'plain', 'filename' : 'res/email_sending/test.txt'}, # 텍스트 첨부파일
    'image' : {'maintype' : 'image', 'subtype' :'jpg', 'filename' : 'res/email_sending/test.jpg' } # 이미지 첨부파일
    # 'audio' : {'maintype' : 'audio', 'subtype' :'mp3', 'filename' : 'res/email_sending/test.mp3' }, # 오디오 첨부파일
    # 'video' : {'maintype' : 'video', 'subtype' :'mp4', 'filename' : 'res/email_sending/test.mp4' }, # 비디오 첨부파일
    # 'application' : {'maintype' : 'application', 'subtype' : 'octect-stream', 'filename' : 'res/email_sending/test.pdf'} # 그 외 첨부파일
}


msg = MIMEText(_text=content, _charset='utf-8')

# simple text만 보낼때
# msg['Subject'] = title
# msg['From'] = sender
# msg['to'] = receiver

multi = make_multimsg((msg_dict))
multi['Subject'] = title
multi['From'] = sender
multi['To'] = receiver
multi.attach(msg)

send_email(smtp_info, multi)

