# README 
#### This project was made for CS 235: Data Mining Techniques, Fall 2021 at the University of California, Riverside



## Project Description
This project attempts to train a convoluted neural network to differentiate between 2D artworks and 3D artworks. My original conclusion was that the human eye, for the most part, can differentiate between 2D artworks and 3D renders. Like paintings and cartoons versus 3D animations. A brief example below:

![It might be considered cheating if you're familiar with these two works, but the point should still be obvious](/assets/comparison.png)

My original hypothesis was that the 3D renders would have much more realistic color gradients, ie more realistic shading and lighting. Therefore there would be much more color variance in 3D renders compared to 2D images. This led me to integrate the **opencv** Python library to alter all of the images in the dataset using coloring by average color per superpixel. Further details can be found in the included .pdf of the PowerPoint presentation I gave for the class, as well as in the file descriptions below. 

The images for the original research were scraped from artstation.com, a mostly professional website for posting artworks of various different mediums. This is achieved with the webscraper written in **1_artstation_data_scraper.py**. You can use that script for creating a dataset sourced from there. More below.

## File Structure 

The main project files consist of the following, in order of execution:

### 1_artstation_data_scraper.py

A Python webscraper that uses the ***requests*** and ***json*** libraries to crawl over trending posts on artstation.com, parse their metadata to determine if they are valid to be labelled as either 2D or 3D, and download all of the images in the post. Will automaticaly set aside 25% of the downloaded posts as testing data, the rest is for training. ***This script is required to build the dataset to be used on the CNN.*** Files are saved according to the following structure: 

```bash
├───test
│   ├───Digital 2D
│   └───Digital 3D
└───train
    ├───Digital 2D
    └───Digital 3D
```

This script will not download posts that have conflicting mediums (e.g. posts with 2D ***and*** 3D) or any other kinds of invalid situations, like a **null** medium. The directory structure must remain this way, otherwise unexpected and incorrect behavior may be observed with the subsequent scripts. I intend to add an additional argument that allows you to supply a custom filepath to store the '/test' and '/train' directories.

Arguments can be provided using the following flags: 

-***v*** 

	For verbose output ; miscellaneous print statements detailing the downloading progress

-***n*** [starting page] number_of_pages 	

	The 'starting page' option determines which page of results scraping will begin from. 
	Default values are **starting_page** = 1, **number_of_pages** = 25
	

### 2_kmeans_superpixel_with_average_coloring.py	
Iterates through all of the training and testing images stored in the 'test' and 'train' directories, resizes them to 800x800, and performs superpixel segmentation on them according to the SLIC (Simple Linear Iterative Clustering) superpixel algorithm, as implemented in the **opencv2** library. Superpixels are then colored with the average color of that superpixel. This method uses k-means clustering for forming superpixel segmentation. Meanin the number of clusters can be altered for different results. The default number of desired segments is 2500. You can supply your own desired number of clusters to the script as an argument like so:

> ***n*** number_of_clusters

This is an image processing script meant to be used on a dataset of raw images (as seen in '/train' and '/test'). If you wish to run this script on your own dataset, it must follow the same directoy structure as shown under the explanation for **1_artstation_data_scraper.py**. I plan to introduce the ability to point to your own custom training and testing dataset filepaths. Altered images are saved to '/resized photos' in the same directory as this script. 



### 3_basic_and_vgg16_CNN.py		
A simple implementation of a VGG-like CNN using **tensorflow** modeling arguments. I also use **Tensorflow**'s VGG16 CNN as a separate definition, for testing on deeper layer counts. I intend to introduce more varied modeling architectures in the future for further testing. I also intend to allow the user to supply arguments to the script so they can tweak model hyperparameters for varied experimentation. 


## Planned Updates
- Custom filepath argument for where the webscraper saves
- Custom filepath argument for the source training and test datasets supplied to **2_kmeans_superpixel_with_average_coloring.py**
- Implement other image alteration methods supplied in the **opencv** library for comparison against the SLIC method, specifically the Felzenszwalb and Quickshift methods which don't rely on k-means clustering methodology
- Implement additional filters using new medium and post metadata added to artstation.com, allowing for more accurate categorizing of 2D and 3D artworks. Filter "mediums" list in metadata per post, checking for clashing mediums