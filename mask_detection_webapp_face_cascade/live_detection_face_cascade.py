import cv2
import numpy as np
import tensorflow as tf
# from mtcnn import MTCNN
from PIL import Image
import cProfile
import pstats
import time

tf.compat.v1.enable_eager_execution()

def live_detect_face_cascade(model, frame, process_frame=False):
    
    """
    maybe next step 
    # # Initialize MTCNN detector
    # detector = MTCNN()

    # faces = detector.detect_faces(frame)
    # faces = [face['box'] for face in faces]

    """

    # Get input and output details
    input_details = model.get_input_details()
    output_details = model.get_output_details()

    print("Processing frame...", frame.shape)
    gray = cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    

    if len(faces) == 0:
        print("No face detected")
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        return frame_bytes  # Return the frame bytes if no faces are detected

    processed_frame = frame.copy()  # Create a copy of the original frame for processing
    for (x, y, w, h) in faces:
        cv2.rectangle(processed_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        face = frame[y:y + h, x:x + w]

        # Resize frame to match model input size (if necessary)
        try:
            t_resize_start = time.process_time()
            resized = cv2.resize(face, (input_details[0]['shape'][1], input_details[0]['shape'][2]))
            resized = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            image_array = np.array(resized, dtype=np.float32)
            image_array = np.expand_dims(image_array, axis=0)
            t_resize_end = time.process_time()
            print("Resizing time:", t_resize_end - t_resize_start)
        except Exception as e:
            print("Error processing frames:", e)

        # Perform mask detection on the face
        try:
           model.set_tensor(input_details[0]['index'], image_array)
           model.invoke()
           t_prediction_start = time.process_time()
           predictions = model.get_tensor(output_details[0]['index'])
           t_prediction_end = time.process_time()
           print("Prediction time:", t_prediction_end - t_prediction_start)

        except Exception as e:
            print("Error predicting mask:", e)
            print(image_array.shape)
            continue

        mask_prob = predictions[0][0]

        # Display a label indicating mask or no mask on the face
        t_put_text_start = time.process_time()
        label = 'No Mask' if mask_prob > 0.5 else 'Mask'
        cv2.putText(processed_frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        t_put_text_end = time.process_time()
        print("putText time:", t_put_text_end - t_put_text_start)

    # Encode processed frame to bytes
    _, buffer = cv2.imencode('.jpg', processed_frame)
    frame_bytes = buffer.tobytes()
    return frame_bytes  # Return the processed frame bytes


## profiling code to test performance

# if __name__ == '__main__':
#     def profile_main():
#         model_loc = "my_model/my_model_quant.tflite"
#         model = tf.lite.Interpreter(model_loc)
#         model.allocate_tensors()
#         frame = cv2.imread("test.jpg")
#         live_detect_face_cascade(model, frame)

#     cProfile.run('profile_main()','profile_stats')
    
#     stats = pstats.Stats('profile_stats')
#     stats.sort_stats(pstats.SortKey.TIME)  # Sort by time spent
#     stats.print_stats()  # Print profiling statistics
