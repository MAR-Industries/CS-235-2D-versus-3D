##hopefully this works for k-means clustering for colors, in order to automate cluster counts
import cv2
import numpy as np
import os
from sklearn.cluster import KMeans
from skimage.segmentation import slic
##from skimage.segementation import felzenszwalb
from skimage.segmentation import mark_boundaries ##used for the segmentation mask
import matplotlib.pyplot as plt
from PIL import Image

my_dpi = 96
currentDirectory = ''

if not os.path.exists('resized photos/'):
	os.makedirs('resized photos/train/Digital 2D')
	os.mkdir('resized photos/train/Digital 3D')
	os.makedirs('resized photos/test/Digital 2D')
	os.mkdir('resized photos/test/Digital 3D')

for i in range(4):
	if i == 0:
		currentDirectory = 'train/Digital 2D'
	elif i == 1:
		currentDirectory = 'train/Digital 3D'
	elif i == 2:
		currentDirectory = 'test/Digital 2D'
	elif i == 3: 
		currentDirectory = 'test/Digital 3D'
	
	print("Starting on ", currentDirectory, "...")
	for filename in os.listdir(currentDirectory):

		if os.path.isfile('resized photos/' + currentDirectory  + '/' + filename):
			continue
		##print(currentDirectory + "/" + filename)
		loaded_image = cv2.imread(currentDirectory + "/" + filename)
		cv2.resize(loaded_image, (800,800), interpolation = cv2.INTER_AREA)
		im = Image.fromarray(loaded_image, 'RGB')
		im = im.resize((800,800))
		loaded_image = np.array(im)
		#tempImage = Image.fromarray(loaded_image, 'RGB')
		#print("loaded image type:", type(loaded_image))
		#tempImage = tempImage.resize((800,800)) ## resizing all of the images before segmenting, to save on computation
		#print("loaded image type:", type(loaded_image))
		#loaded_image = np.array(tempImage)
		h, w, c = loaded_image.shape
		
		##loaded_image = loaded_image.reshape((loaded_image.shape[0] * loaded_image.shape[1], 3))##superpixel throws a fit with incorrect channel counts, ie .png files
		
		#average coloring in superpixels actually begins here 
		img = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2HSV) ##convert to appropriate color space 
		label=slic(img,compactness=10, n_segments=2500)
		
		#main work to create color average for superpixels 
		img_reshaped=img.reshape((img.shape[0]*img.shape[1],img.shape[2]))
		slic_1Dim=np.reshape(label,-1) #inversion on SLIC 
		
		uniqueness=np.unique(slic_1Dim)
		
		uu=np.zeros(img_reshaped.shape)
		
		for i in uniqueness:
			loc=np.where(slic_1Dim==i)[0]
			matmean=np.mean(img_reshaped[loc,:],axis=0)
			uu[loc,:]=matmean
			
		final_array=np.reshape(uu,[img.shape[0],img.shape[1],img.shape[2]]).astype('uint8')
		##cv2.imshow('img',final_array)
		im = Image.fromarray(final_array)
		##im.show()
		im.save('resized photos/' + currentDirectory + '/' + filename)
		