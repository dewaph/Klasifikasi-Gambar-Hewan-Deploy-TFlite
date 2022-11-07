# -*- coding: utf-8 -*-
"""klasifikasi_gambar_hewan.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j4ABXon7PqkJe1kKMcK7DcNGEL3dJBfu

Nama : Dewa Putra Haryono

Dataset kaggle : animal10
"""

import tensorflow as tf

"""Download dataset dengan kaggle API"""

#install kaggle
!pip install -q kaggle

# upload file kaggle.json
from google.colab import files
files.upload()

# buat direktori dan copy kaggle.json
! mkdir ~/.kaggle

! cp kaggle.json ~/.kaggle/

# ubah permission file kaggle.json
! chmod 600 ~/.kaggle/kaggle.json

! kaggle datasets list

#download dataset dari kaggle
!kaggle datasets download -d viratkothari/animal10

#buat direktori
!mkdir animals

#unzip file dataset
!unzip -qq animal10.zip -d animals

import os
os.listdir('/content/animals/Animals-10')

#pilih hewan yang tidak diperlukan
import shutil

hapus_animals = ['cat', 'cow', 'elephant', 'horse', 'butterfly', 'sheep', 'squirrel']

animals = os.path.join('/content/animals/Animals-10')
for x in hapus_animals:
  path = os.path.join(animals, x)
  shutil.rmtree(path)

#cek kemabali direktori animals
import os
os.listdir('/content/animals/Animals-10')

print('total gambar ayam :', len(os.listdir('/content/animals/Animals-10/chicken')))
print('total gambar anjing :', len(os.listdir('/content/animals/Animals-10/dog')))
print('total gambar laba-laba :', len(os.listdir('/content/animals/Animals-10/spider')))

# Commented out IPython magic to ensure Python compatibility.
#lihat contoh gambar
import keras
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline
img = keras.utils.load_img('/content/animals/Animals-10/chicken/chicken (1).jpeg')
imgplot = plt.imshow(img)

from tensorflow.keras.preprocessing.image import ImageDataGenerator
 
train_dir = os.path.join('/content/animals/Animals-10')
train_datagen = ImageDataGenerator(rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    shear_range=0.2,
    fill_mode = 'nearest',
    validation_split=0.2) # set validation split

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical',
    subset='training') # set sebagai training data
validation_generator = train_datagen.flow_from_directory(
    train_dir, 
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical',
    subset='validation') # set sebagai validation data

model = tf.keras.models.Sequential([
    # Note the input shape is the desired size of the image 150x150 with 3 bytes color
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.5),  
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'), 
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.5),  
    # Flatten the results to feed into a DNN
    tf.keras.layers.Flatten(), 
    # 512 neuron hidden layer
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')  
])

model.compile(optimizer=tf.optimizers.Adam(),
              loss='categorical_crossentropy',
              metrics = ['accuracy'])

model.summary()

#buat callback
class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.92 and logs.get('val_accuracy')>0.92):
      print("\nAkurasi sudah > 92%")
      self.model.stop_training = True
callbacks = myCallback()

history = model.fit(train_generator,
                    steps_per_epoch = 55,
                    epochs = 50,
                    validation_data = validation_generator,
                    verbose = 2,
                    callbacks = [callbacks])

"""Prediksi gambar"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from google.colab import files
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline
 
uploaded = files.upload()
 
for fn in uploaded.keys():
 
  # predicting images
  path = fn
  img = image.load_img(path, target_size=(150,150))
 
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  images = np.vstack([x])
 
  classes = model.predict(images, batch_size=10) 
  print(fn)
  if classes[0][0]==1:
    print('Ayam')
  elif classes[0][1]==1:
    print('Anjing')
  elif classes[0][2]==1:
    print('Laba-laba')

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from google.colab import files
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline
 
uploaded = files.upload()
 
for fn in uploaded.keys():
 
  # predicting images
  path = fn
  img = image.load_img(path, target_size=(150,150))
 
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  images = np.vstack([x])
 
  classes = model.predict(images, batch_size=10) 
  print(fn)
  if classes[0][0]==1:
    print('Ayam')
  elif classes[0][1]==1:
    print('Anjing')
  elif classes[0][2]==1:
    print('Laba-laba')

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from google.colab import files
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline
 
uploaded = files.upload()
 
for fn in uploaded.keys():
 
  # predicting images
  path = fn
  img = image.load_img(path, target_size=(150,150))
 
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  images = np.vstack([x])
 
  classes = model.predict(images, batch_size=10) 
  print(fn)
  if classes[0][0]==1:
    print('Ayam')
  elif classes[0][1]==1:
    print('Anjing')
  elif classes[0][2]==1:
    print('Laba-laba')

"""membuat plot"""

import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Akurasi Model')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Loss Model')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

"""simpan model kedalam TF-Lite"""

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with tf.io.gfile.GFile('model.tflite', 'wb') as f:
  f.write(tflite_model)