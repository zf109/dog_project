import numpy as np
import cv2
from keras.preprocessing import image
from tqdm import tqdm
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.applications.resnet50 import ResNet50

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers import Dropout, Flatten, Dense
from keras.callbacks import ModelCheckpoint  
from extract_bottleneck_features import extract_Resnet50
from dog_names import dog_names
import numpy as np
import tensorflow as tf

ResNet50_breed = Sequential()
ResNet50_breed.add(GlobalAveragePooling2D(input_shape=(1, 1, 2048)))
ResNet50_breed.add(Dense(133, activation='softmax'))
ResNet50_breed.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])


# define ResNet50 model
ResNet50_model = ResNet50(weights='imagenet')
ResNet50_model_graph = tf.get_default_graph()

face_cascade = cv2.CascadeClassifier('dog_app/haarcascades/haarcascade_frontalface_alt.xml')


# Load the model from saved data
ResNet50_breed.load_weights('dog_app/saved_models/weights.best.ResNet50.hdf5')
ResNet50_breed_graph = tf.get_default_graph() #lock down the default graph



def image_convert(img):
    # convert PIL.Image.Image type to 3D tensor with shape (224, 224, 3)
    x = image.img_to_array(img)
    # convert 3D tensor to 4D tensor with shape (1, 224, 224, 3) and return 4D tensor
    return np.expand_dims(x, axis=0)    

def path_to_tensor(img_path):
    # loads RGB image as PIL.Image.Image type
    img = image.load_img(img_path, target_size=(224, 224))
    # convert PIL.Image.Image type to 3D tensor with shape (224, 224, 3)
    x = image.img_to_array(img)
    # convert 3D tensor to 4D tensor with shape (1, 224, 224, 3) and return 4D tensor
    return np.expand_dims(x, axis=0)


def paths_to_tensor(img_paths):
    list_of_tensors = [path_to_tensor(img_path) for img_path in tqdm(img_paths)]
    return np.vstack(list_of_tensors)


def ResNet50_predict_labels_from_path(img_path):
    # returns prediction vector for image located at img_path    
    img = preprocess_input(path_to_tensor(img_path))
    with ResNet50_model_graph.as_default():
        pred = ResNet50_model.predict(img)
    return np.argmax(pred)


def face_detector_from_path(img_path):
    """returns "True" if face is detected in image stored at img_path"""
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    return len(faces) > 0


def dog_detector_from_path(img_path):
    """returns "True" if a dog is detected in the image stored at img_path """
    prediction = ResNet50_predict_labels_from_path(img_path)
    return ((prediction <= 268) & (prediction >= 151))


def ResNet50_predict_labels(img):
    # returns prediction vector for image located at img_path
    img_converted = preprocess_input(image_convert(img))
    with ResNet50_model_graph.as_default():
        pred = ResNet50_model.predict(img_converted)
    return np.argmax(pred)


def face_detector(img):
    """returns "True" if face is detected in image stored at img_path"""
    # img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    return len(faces) > 0


def dog_detector(img):
    """returns "True" if a dog is detected in the image stored at img_path """
    image_convert(img)
    prediction = ResNet50_predict_labels(img)
    return ((prediction <= 268) & (prediction >= 151))


def ResNet50_predict_breed_from_path(img_path):
    # extract bottleneck features
    with ResNet50_model_graph.as_default():
        bottleneck_feature = extract_Resnet50(path_to_tensor(img_path))
    # obtain predicted vector
    with ResNet50_breed_graph.as_default():
        predicted_vector = ResNet50_breed.predict(bottleneck_feature)
    # return dog breed that is predicted by the model
    return dog_names[np.argmax(predicted_vector)]


def ResNet50_predict_breed(img):
    # extract bottleneck features
    bottleneck_feature = extract_Resnet50(image_convert(img))
    # obtain predicted vector
    predicted_vector = ResNet50_breed.predict(bottleneck_feature)
    # return dog breed that is predicted by the model
    return dog_names[np.argmax(predicted_vector)]

