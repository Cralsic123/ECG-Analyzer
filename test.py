from flask import Flask, request, jsonify
import numpy as np
import cv2
import tensorflow as tf
import os
import base64

app = Flask(__name__)

interpreter = tf.lite.Interpreter(model_path="/Users/shuvamdas/ECG1/EEE/ECG_classifier.tflite")
interpreter.allocate_tensors()

decode = {0:'Patient has a normal heart beat. Stress is not occuring frequently. Patient follows a low carb diet. Patient can considering exercising for 30 minutes daily', 1:'Patient has a normal but seems a little impatient. Stressfull situation now and then. A little high blood pressure. Patient may need to reconsider his or her diet.', 3:'ECG seems absolutely normal. Patient seems fine. Keep exercising and eat healthy', 2: 'The ECG seems a bit distressed with the peaks and troughs a bit high. Chances of Miocardial infarction are there but minimal. Should prefer to check up on a doctor', 4:'The ECG of the patient is normal. However the patient has got some raised curves near the T and R region. Considering nothing serious but fat construction for the patient is to be worried.'}
def preprocess_image(image):
    img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    img = cv2.resize(img, (1200, 200))
    img = np.expand_dims(img, axis=-1)
    img = img / 255.0
    return img

@app.route('/')
def main():
    return 'Homepage'

@app.route('/predict', methods=['POST'])
def predict():
    import os
    import base64
    if 'image' not in request.form:
        return jsonify({'message': 'No image data in the request'}), 400

    image_data = request.form['image']
    image = cv2.imdecode(np.fromstring(base64.b64decode(image_data), dtype=np.uint8), cv2.IMREAD_COLOR)

    img = preprocess_image(image)

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    #interpreter.set_tensor(input_details[0]['index'], img.reshape((1, 64, 64, 1)).astype(np.float32))
    #interpreter.invoke()

    prediction = interpreter.get_tensor(output_details[0]['index'])
    decoded_prediction = decode[np.argmax(prediction)]

    return jsonify({'class': decoded_prediction})

if __name__ == '__main__':
    app.run(debug=True, port=8888)
