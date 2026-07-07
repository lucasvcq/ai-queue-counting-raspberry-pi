# -*- coding: utf-8 -*-

import time
import json
import cv2
import numpy as np
import paho.mqtt.client as mqtt
from tensorflow.keras.models import load_model

THINGSBOARD_HOST = 'thingsboard.icam.technology'
ACCESS_TOKEN     = 'Ljx1Xw1HdrH2errD1Pod'  # Remplace par ton token
INTERVAL         = 2

MODEL_PATH  = 'keras_model.h5'
LABELS_PATH = 'labels.txt'

model = load_model(MODEL_PATH, compile=False)
with open(LABELS_PATH, 'r') as f:
    class_names = [l.strip() for l in f.readlines()]

# Cr�e un client MQTT avec callback_api_version enum (v5)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()

camera = cv2.VideoCapture(0)
if not camera.isOpened():
    raise RuntimeError("Impossible d'ouvrir la cam�ra")

print("D�marrage boucle capture/inf�rence... (Ctrl+C pour arr�ter)")

next_capture = time.time()
try:
    while True:
        now = time.time()
        if now < next_capture:
            time.sleep(next_capture - now)
        next_capture += INTERVAL

        # Capture image
        ret, frame = camera.read()
        if not ret:
            print("�chec capture, nouvelle tentative...")
            continue

        # Affichage webcam
        cv2.imshow("Webcam Image", frame)
        cv2.waitKey(1)  # N�cessaire pour rafra�chir l'affichage dans certaines configs

        # Pr�traitement pour le mod�le
        img = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
        img = img.astype(np.float32)
        img = (img / 127.5) - 1.0
        img = np.expand_dims(img, axis=0)

        # Pr�diction
        prediction = model.predict(img)
        idx = int(np.argmax(prediction[0]))
        confidence = float(prediction[0][idx])

        print(f"Pr�diction : {idx} ({confidence*100:.1f}%)")

        # Envoi MQTT
        payload = {
            'prediction': idx,
            'confidence': confidence
        }
        client.publish('v1/devices/me/telemetry', json.dumps(payload), qos=1)

except KeyboardInterrupt:
    print("\nInterruption utilisateur, nettoyage...")
finally:
    camera.release()
    cv2.destroyAllWindows()
    client.loop_stop()
    client.disconnect()
    print("Termin�.")