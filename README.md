# emma_spiders

Code to identify spiders from images. Requires OpenCV. Work in progress.

The code works by first blurring the image

![blur](./blur.jpg?raw=true "blur")

It then thresholds the image adaptively

![threshold](./threshold.jpg?raw=true "thresh")

to find the contours (in blue)

![contours](./out.jpg?raw=true "output")
