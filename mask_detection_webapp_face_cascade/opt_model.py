import tensorflow as tf

# Load the Keras model
model = tf.keras.models.load_model('my_model/my_model.keras')

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_quant_model = converter.convert()

#save the quantized model
with open('my_model/my_model_quant.tflite', 'wb') as f:
  f.write(tflite_quant_model)
