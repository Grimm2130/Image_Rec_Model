import tensorflow as tf
import numpy as np
import time
from threading import Thread

# global variable: Model encapsulator
model = None
    
def predictOnPicture(model : tf.keras.Model, img : np.array):
    '''Function to set the model to predict on a given picture
    
    Args:
        model - A loaded instance of the Efficient_net model
        img - a numpy array interpretation of a jpg image
    
    Return:
        a return a prediction index
        '''
    names = {0: "Corn", 1: "Soy"}
    print("Predicting on image")
    st = time.time()
    pred = model.predict(tf.expand_dims(img, axis=0))
    pred = int(pred[0,0]>0.5)
    en = time.time()
    print(f"Total elapsed time: {en-st}")
    return pred, names[pred]
    

# # This function uses the trheading class to instantiate a thread to load in the model class
# class Threaded_Model_Handler(Thread):
#     def __init__(self, group= None, target= None, name= None, args = (), kwargs={}):
#         '''Model clas Handler with threading'''
#         # instantiate the threading class
#         Thread.__init__(self, group, target, name, args, kwargs)
#         self._return = None
    
#     def run(self):
#         '''Function set's the return value of the thread depending on if the target has a
#             return value or not'''
#         if self._target is not None:
#             self._return = self._target(*self._args,
#                                                 **self._kwargs)
        
#     def join(self):
#         Thread.join(self)
#         return self._return
    
def setup_evaluation_data():
    '''
    Function to set up data for evaluating the model
    '''
    testPath = "/home/pi/Documents/SeniorDesign/SeniorDes_Images/Test"
    
    testData = tf.keras.preprocessing.image_dataset_from_directory(
        directory = testPath,
        label_mode = "binary",
        batch_size = 32,
        image_size = (224,224),
        shuffle = True
    )
    return testData

    
def in_mem_Load_model():
    '''
    Function to set up the model
    '''
    print("Model's being instantiated")
    
    # Instantiate the preprocessing layer
    preprocessingLayer = tf.keras.Sequential([
    tf.keras.layers.experimental.preprocessing.RandomHeight(0.2),
    tf.keras.layers.experimental.preprocessing.RandomFlip("horizontal"),
    tf.keras.layers.experimental.preprocessing.RandomWidth(0.2),
    tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),
    # tf.keras.layers.experimental.preprocessing.RandomTranslation(0.1, 0.1)    
    ], name = "data_augmentation")
    
    # Load the EfficientNetV2B0 model package
    base_model = tf.keras.applications.efficientnet_v2.EfficientNetV2B0(
    include_top=False
    )
    base_model.trainable = False
    
    # define the input layer
    input_layer = tf.keras.layers.Input(shape = (224,224,3))
    
    # packaging
    x = preprocessingLayer(input_layer)
    x = base_model(x)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    output_layer = tf.keras.layers.Dense(units=1, activation = "sigmoid")(x)
    
    # Model instantiation
    model = tf.keras.Model(input_layer, output_layer)
    
    # load the model
    print("model is being loaded")
    filePath = "/home/pi/Documents/SeniorDesign/Models/Model_Checkpoint_Accuracy"
    
    model.load_weights(filePath)
    
    # compile the model
    model.compile(
        loss = "binary_crossentropy",
        optimizer = tf.keras.optimizers.Adam(),
        metrics = ["accuracy"]
    )
    
    # Evaluate the model
    # eval = model.evaluate(setup_evaluation_data())
    # print(eval)
    
    # return the model
    return model



