# README 
#### This project was made for CS 235: Data Mining Techniques, Fall 2021 at the University of California, Riverside



## Project Description
This project attempts to train a convoluted neural network to differentiate between 2D artworks and 3D artworks. My original conclusion is that the human eye, for the most part, can differentiate between 2D artworks and 3D renders. A somewhat obvious example below:

![It might be considered cheating if you're familiar with these two works, but the point should still be obvious](/assets/comparison.png)

My original hypothesis was that the 3D renders would have much more realistic color gradients, ie more realistic shading and lighting. Therefore there would be much more color variance in 3D renders compared to 2D images. This led me to integrate the **opencv** Python library to alter all of the images in the dataset using coloring by average color per superpixel. Further details can be found in the included .pdf of the PowerPoint presentation I gave for the class, as well as in the file descriptions below. 


## File Structure 

The main project files consist of the following, in order of execution:

### 1_artstation_data_scraper.py

A Python webscraper that uses the ***requests*** and ***json*** libraries to crawl over trending posts on artstation.com, parse their metadata to determine if they are valid to be labelled as either 2D or 3D, and download all of the images in the post. Will automaticaly set aside 25% of the downloaded posts as testing data, the rest is for training. ***This script is required to build the dataset to be used on the CNN.*** Files are saved by purpose and medium according to the following structure: 

```bash
├───test
│   ├───Digital 2D
│   └───Digital 3D
└───train
    ├───Digital 2D
    └───Digital 3D
```

This script will not download posts that have conflicting mediums (e.g. 2D ***and*** 3D) or any other kinds of invalid situations, like a **null** medium. The directory structure must remain this way, otherwise unexpected and incorrect behavior may be observed with the subsequent scripts.

Arguments can be provided using the following flags: 

-***v*** 


For verbose output ; miscellaneous print statements detailing the downloading progress

-***n*** [starting page] number_of_pages 	


The 'starting page' option determines which page of results scraping will begin from
	

### 2_kmeans_superpixel_with_average_coloring.py	
Iterates through all of the training and testing images stored in the 'test' and 'train' directories, resizes them to 800x800, and performs superpixel segmentation on them according to the SLIC (Simple Linear Iterative Clustering) superpixel algorithm, as implemented in the **opencv2** library. Superpixels are then colored with the average color of that superpixel. This is an image processing script meant to be used on a dataset of raw images (as seen in '/train' and '/test'). Execution of this script must occur in the same directory as where you're storing the '/train' and '/test' directories. Altered images are then saved to '/resized photos'. As implied by the title, the SLIC method relies on k-means clustering for superpixel segmentation. You may supply a custom number of clusters using the following argument: 

> -n number_of_clusters

basic and vgg16 CNN.py:		my attempt at implementing a VGG-like CNN using tensorflow modeling arguments. I also use Tensorflow's VGG16 CNN as a separate definition, for testing on deeper layer counts.

The 'resized photos' directory contains the altered dataset, and /train and /test contain the original datasets as they were scraped from artstation.com. 


## Planned Updates
- Implement other image alteration methods supplied in the **opencv** library for comparison against the SLIC method, specifically the Felzenszwalb and Quickshift methods which don't rely on k-means clustering methodology