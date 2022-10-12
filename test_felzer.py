import os
import matplotlib.pyplot as plt
from skimage.measure import regionprops
from skimage.segmentation import slic
from skimage.segmentation import felzenszwalb
from skimage.data import coffee

img = coffee()
segments = felzenszwalb(img, scale=3.0, sigma=0.95, min_size=5)

for i in range(3):
    regions = regionprops(segments, intensity_image=img[:,:,i])
    for r in regions:
        paint_region_with_avg_intensity(r.coords, int(r.mean_intensity), i)

plt.imshow(img)
plt.show()