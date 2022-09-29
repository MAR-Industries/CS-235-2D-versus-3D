# README                    |
### This project was made for CS 235: Data Mining Techniques, Fall 2021 at the University of California, Riverside. 

## Project Description
This project is as an attempt to classify images downloaded from artstation.com with the labels of 2D or 3D. The original interest of this project was to know whether a machine could be trained to tell the difference between images that are made using 2D mediums (eg drawn in 2D art applications or analog means) and images made using 3D methods (eg 3D rendering software like Blender, 3DMAX, etc.). I also was interested in whether or not I could feed it hyperrealistic 2D images (eg very realistic paintings or sketches) and see if it classifies them as 3D. And vice versa.

My original hypothesis was that the 3D renders would have much more realistic color gradients, like more realistic shading and lighting. Therefore, there would be much more color diversity and less matte or flat coloring, which might be more usual in 2D artwork. I've included a .pdf of the PowerPoint presentation I gave on the project for the class, for more details.



artstation_data_scraper.py:	the webscraper for artwork off of artstation.com. It vets for if an artwork post has been desginated as 2D or 3D, and excludes works with other mediums or conflicting mediums (2D AND 3D) assigned to them. 25% of the downloaded results are set aside in a 'test' subdirectory, while the rest go into 'train', wherein each they are separated in 'Digital 2D' and 'Digital 3D' folders.  The directory naming scheme takes advantage of the Keras library function flow_from_directory that during model fitting will automatically separate classes by separate folders in specified 'train' and 'test' directories. 

kmeans superpixel with average coloring.py:	iterates through all of the training and testing directory 2D and 3D images, resizes them to 800x800, and performs superpixel segmentation on them according to the SEEDS superpixel algorithm, as implemented in the opencv2 library. Superpixels are then colored with the average color of that superpixel. This is an image processing script meant to be used on a dataset of raw images (as seen in '/train' and '/test'). The results of the processing are saved into the 'resized photos' directory. 

basic and vgg16 CNN.py:		my attempt at implementing a VGG-like CNN using tensorflow modeling arguments. I also use Tensorflow's VGG16 CNN as a separate definition, for testing on deeper layer counts.

The 'resized photos' directory contains the altered dataset, and /train and /test contain the original datasets as they were scraped from artstation.com. 