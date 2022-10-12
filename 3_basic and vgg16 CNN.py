import tensorflow as tf
import sys
from matplotlib import pyplot as plt
from tensorflow.keras.utils import to_categorical
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.models import Sequential
from keras.layers import Flatten
from tensorflow.keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.vgg16 import VGG16
from keras.models import Model

def base_model_create():

	model = Sequential() ## stack of layers 
	#where we create the first vgg-like block 
	model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', input_shape=(175, 175, 3)))
	model.add(MaxPooling2D((2, 2)))
	##second block, 64 filters
	model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
	model.add(MaxPooling2D((2, 2)))
	#third block, 128 filters 
	model.add(Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
	model.add(MaxPooling2D((2, 2)))
	#
	model.add(Flatten())
	model.add(Dense(128, activation='relu', kernel_initializer='he_uniform'))
	model.add(Dense(1, activation='sigmoid'))
	
	##stochastic gradient descent with 0.001 learning rate and momentum 0.9 to be experimental from the get-go, edit these for testing 
	optimization = SGD(lr=0.001, momentum=0.9)
	model.compile(optimizer=optimization, loss='binary_crossentropy', metrics=['accuracy'])
	return model

# define cnn model
def vgg16_model_create():

	# using the tensorflow implementation, not using a "poor man's VGG" like mine above
	model = VGG16(include_top=False, input_shape=(175, 175, 3))
	# mark loaded layers as not trainable
	for layer in model.layers:
		layer.trainable = False
	# create new classifying layers
	flat1 = Flatten()(model.layers[-1].output)
	class1 = Dense(128, activation='relu', kernel_initializer='he_uniform')(flat1)
	output = Dense(1, activation='sigmoid')(class1)
	# define new model
	model = Model(inputs=model.inputs, outputs=output)
	# same SGD parameters for consistency before experimenting
	optimization = SGD(lr=0.001, momentum=0.9)
	model.compile(optimizer=optimization, loss='binary_crossentropy', metrics=['accuracy'])
	return model	


# create the model (alter base and vgg-16 architectures for testing)
model_to_train = vgg16_model_create()
# create data generator
datagen = ImageDataGenerator(rescale=1.0/255.0)
# preparing parsers for training on the data and testing; alternate desired directory for superpixel segmented images and the source image datasets
training = datagen.flow_from_directory('resized photos/train/', class_mode='binary', batch_size=64, target_size=(175, 175))
testing = datagen.flow_from_directory('resized photos/test/', class_mode='binary', batch_size=64, target_size=(175, 175))
# fit model_to_train
print("pre-train")
hist_track = model_to_train.fit(training, steps_per_epoch=len(training), validation_data=testing, validation_steps=len(testing), epochs=20, verbose=0)
print("post-train, pre-test")	
# evaluate model_to_train
_, accuracy = model_to_train.evaluate(testing, steps=len(testing), verbose=0)
print("post test")

# plot loss
plt.subplot(211)
plt.title('Loss')
plt.plot(hist_track.history['loss'], color='blue', label='train')
plt.plot(hist_track.history['val_loss'], color='orange', label='test')

# plot accuracy
plt.subplot(212)
plt.title('Classification Accuracy')
plt.plot(hist_track.history['accuracy'], color='blue', label='train')
plt.plot(hist_track.history['val_accuracy'], color='orange', label='test')
##filename = input('Name the file: ')
##plt.savefig(filename + '.png')
plt.show()
plt.close()
