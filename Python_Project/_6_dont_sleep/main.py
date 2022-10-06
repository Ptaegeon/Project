import cv2
import tensorflow
from PIL import Image, ImageOps
import numpy as np
# import beepy
import kakao_utils


# def beepsound():
#     beepy.beep(sound=6)


def send_music_link():
    KAKAO_TOKEN_FILENAME = 'res/kakao_message/kakao_token.json'
    KAKAO_APP_KEY = ""
    tokens = kakao_utils.update_tokens(KAKAO_APP_KEY, KAKAO_TOKEN_FILENAME)

    template = {
        "object_type": "text",
        "text": "30 졸았음",
        "link": {
            "web_url": "https://www.youtube.com/watch?v=7Q2N7919o5o",
            "mobile_web_url": "https://www.youtube.com/watch?v=7Q2N7919o5o"
        },
        "button_title": "잠깨는 노래"
    }

    res = kakao_utils.send_message(KAKAO_TOKEN_FILENAME, template)
    if res.json().get('result_code') == 0:
        print('성공')
    else:
        print('실패', res.json())


def preprocessing(frame):
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))

    return frame_reshaped


model_filename = 'keras_model.h5'
model = tensorflow.keras.models.load_model(model_filename)


capture = cv2.VideoCapture(0)

capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

sleep_cnt = 1

while True:

    ret, frame = capture.read()
    if ret == True:
        print("read success")

    frame_fliped = cv2.flip(frame, 1)

    cv2.imshow("Video frame", frame_fliped)

    if cv2.waitKey(200) > 0:
        break

    preprocessed = preprocessing(frame_fliped)

    prediction = model.predict(preprocessed)

    if prediction[0, 0] < prediction[0, 1]:
        print('졸림')
        sleep_cnt += 1

        if sleep_cnt % 30 == 0:
            sleep_cnt = 1
            print('졸았음')
            # beepsound()
            # send_music_link()
            break
    else:
        print('깨어있음')
        sleep_cnt = 1

capture.release()
cv2.destroyAllWindows()
