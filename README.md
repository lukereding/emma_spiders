# emma_spiders

Code to identify spiders from images. Work in progress.

The code works by first blurring the image with `cv2.GaussianBlur(photo, (0,0), 15)`

[blur](./blur.jpg)

It then thresholds the image adaptively

[threshold](./threshold.jpg)

to find the contours (in blue)

[contours](./out.jpg)
