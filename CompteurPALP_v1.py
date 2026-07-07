import os
import time
import json
import cv2
import numpy as np
import paho.mqtt.client as mqtt
from imutils.video import VideoStream
from imutils.video import FPS

# -----------------------------
# Configuration
# -----------------------------
THINGSBOARD_HOST = 'thingsboard.icam.technology'
ACCESS_TOKEN = os.getenv('TB_ACCESS_TOKEN', 'p7z7kCQT6WSJpXu9giO5')
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
TOPIC = 'v1/devices/me/telemetry'

# Model files for OpenCV DNN (MobileNet SSD)
PROTOTXT_PATH = 'models/MobileNetSSD_deploy.prototxt'
MODEL_PATH = 'models/MobileNetSSD_deploy.caffemodel'
CONF_THRESHOLD = 0.4

# Average service time per person (seconds)
AVG_SERVICE_TIME = 120  # adjust to your truck's average

# -----------------------------
# MQTT Setup
# -----------------------------
def setup_mqtt():
    client = mqtt.Client()
    client.username_pw_set(ACCESS_TOKEN)
    client.connect(THINGSBOARD_HOST, MQTT_PORT, MQTT_KEEPALIVE)
    client.loop_start()
    return client

# -----------------------------
# Load DNN Detector
# -----------------------------
def load_detector():
    net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)
    return net

# -----------------------------
# Main Loop
# -----------------------------
def main():
    # Initialize MQTT
    mqtt_client = setup_mqtt()

    # Load detector
    net = load_detector()

    # Initialize video stream
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fps = FPS().start()

    try:
        while True:
            frame = vs.read()
            if frame is None:
                break

            # Resize for faster processing
            frame_resized = cv2.resize(frame, (600, 600))
            (h, w) = frame_resized.shape[:2]

            # Prepare blob and detect
            blob = cv2.dnn.blobFromImage(cv2.resize(frame_resized, (300, 300)), 0.007843,
                                         (300, 300), 127.5)
            net.setInput(blob)
            detections = net.forward()

            # Count persons
            person_count = 0
            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > CONF_THRESHOLD:
                    idx = int(detections[0, 0, i, 1])
                    # Class 15 is 'person' in MobileNet SSD
                    if idx == 15:
                        person_count += 1
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype('int')
                        cv2.rectangle(frame_resized, (startX, startY), (endX, endY),
                                      (0, 255, 0), 2)

            # Estimate wait time
            est_wait = person_count * AVG_SERVICE_TIME
            minutes = int(est_wait // 60)
            seconds = int(est_wait % 60)
            wait_text = f'Est. wait: {minutes}m {seconds}s'

            # Overlay info
            info = [
                ('Queue Length', person_count),
                (wait_text, '')
            ]
            for (i, (label, val)) in enumerate(info):
                text = f"{label}: {val}" if val != '' else label
                cv2.putText(frame_resized, text, (10, h - ((i * 20) + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # Show frame
            cv2.imshow('Queue Monitor', frame_resized)
            key = cv2.waitKey(1) & 0xFF

            # Publish telemetry
            payload = {
                'queue_length': person_count,
                'estimated_wait_sec': est_wait
            }
            mqtt_client.publish(TOPIC, json.dumps(payload), 1)

            fps.update()

            if key == ord('q'):
                break

    except KeyboardInterrupt:
        pass

    # Cleanup
    fps.stop()
    cv2.destroyAllWindows()
    vs.stop()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()

if __name__ == '__main__':
    main()

