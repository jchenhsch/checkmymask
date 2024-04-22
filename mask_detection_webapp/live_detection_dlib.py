import cv2
import tensorflow as tf
import dlib
from imutils import face_utils
import numpy as np
import asyncio

# live streaming face mask detection using dlib
# slow but accurate in face detection

def live_detect_dlib(model, frame, process_frame=False):
   

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_detect = dlib.get_frontal_face_detector()
    rects = face_detect(gray, 2)

    if len(rects) == 0:
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        print("message sent, no face detected")
        yield frame_bytes
    
    for rect in rects:
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
        face = frame[y:y + h, x:x + w]

        try:
            resized = cv2.resize(face, (400, 400))
            resized = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            image_array = np.array(resized)
            image_array = np.expand_dims(image_array, axis=0)

            # Use the model directly on the image tensor
            predictions = model(image_array)
            mask_prob = predictions[0][0]

            label = 'No Mask' if mask_prob > 0.5 else 'Mask'
            cv2.putText(frame, label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            print('message_sent')
            yield frame_bytes
        except Exception as e:
            print("Error processing frame:", e)
            continue


