# README 
#### This project was made for CS 235: Data Mining Techniques, Fall 2021 at the University of California, Riverside



## Project Description
This project attempts to train a convoluted neural network to differentiate between 2D artworks and 3D artworks. My original conclusion is that the human eye, for the most part, can differentiate between 2D artworks and 3D renders. A somewhat obvious example below:

![It might be considered cheating if you're familiar with these two works, but the point should still be obvious](/assets/comparison.png)
This project is as an attempt to classify images downloaded from artstation.com with the labels of 2D or 3D. The original intent of this project was to explore whether a machine could be trained to tell the difference between images that are made using 2D mediums (eg drawn in 2D art applications or analog means) and images made using 3D methods (eg 3D rendering software like Blender, 3DMAX, etc.) o na consistent basis. I also was interested in whether or not I could feed it hyperrealistic 2D images (eg very realistic paintings or sketches) and see if it classifies them as 3D. And vice versa.

My original hypothesis was that the 3D renders would have much more realistic color gradients, like more realistic shading and lighting. Therefore, there would be much more color diversity and less matte or flat coloring, which might be more usual in 2D artwork. 

I've included a .pdf of the PowerPoint presentation I gave on the project for the class, for more details.


## File Structure 

The main project files consist of the following, in order of execution:

### artstation_data_scraper.py

A Python webscraper that uses the ***requests*** and ***json*** libraries to crawl over trending posts on artstation.com, parse their metadata to determine if they are valid to be labelled as either 2D or 3D, and download all of the images in the post. Will automaticaly set aside 25% of the downloaded posts as testing data, the rest is for training. ***This script is required to build the dataset to be used on the CNN.*** Files are saved by purpose and medium according to the following structure: 

```bash
├───test
│   ├───Digital 2D
│   └───Digital 3D
└───train
    ├───Digital 2D
    └───Digital 3D
```

This script will not download posts that have conflicting mediums (e.g. 2D ***and*** 3D) or any other kinds of invalid situations, like a **null** medium. The directory structure must remain this way for the ***keras*** library to effectively refer to the image dataset.

Arguments can be provided using the following flags: 

> -v	

	For verbose output ; miscellaneous print statements detailing the downloading progress

> -n [starting page] number_of_pages 	

	The 'starting page' option determines which page of results scraping will begin from

kmeans superpixel with average coloring.py:	iterates through all of the training and testing directory 2D and 3D images, resizes them to 800x800, and performs superpixel segmentation on them according to the SEEDS superpixel algorithm, as implemented in the opencv2 library. Superpixels are then colored with the average color of that superpixel. This is an image processing script meant to be used on a dataset of raw images (as seen in '/train' and '/test'). The results of the processing are saved into the 'resized photos' directory. 

basic and vgg16 CNN.py:		my attempt at implementing a VGG-like CNN using tensorflow modeling arguments. I also use Tensorflow's VGG16 CNN as a separate definition, for testing on deeper layer counts.

The 'resized photos' directory contains the altered dataset, and /train and /test contain the original datasets as they were scraped from artstation.com. 