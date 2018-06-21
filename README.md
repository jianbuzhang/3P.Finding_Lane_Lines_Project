# **Finding lane line Project** 
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

<img src="examples/laneLines_thirdPass.jpg" width="480" alt="Combined Image" />

## Brief Introduction
---
When we are driving, we depend on our eyes to determine where we are going, and we can judge the relative position and angle of the car according to the line on the road. So the first thing we do to develop unmanned vehicles is to use image processing algorithms to automatically detect lane lines.

In this project we will use python and OpenCV to detect the line in the image.The OpenCV full name is "Open-source Computer Vision",meaning the open source vision library,which contains a number of software packages with many image processing tools.

## The steps of the project

* First,we can conduct anexperiment on a single image.
* Input an image-->Grayscale-->GaussianBlur-->Canny to detect the boundary.
* Draw a region of interest.
* Conbine step 2 and step 3.Detect the lane line in a region of interest.
* Input a driving video and detect the lane line in every frame.Finally output the video.

---

## The processing details

### 1.Import related libraries and input a image

The library `cv2`,which is a great-function library,can read and write a image,select areas, transfer colors and so on. 

The library `numpy` system is an open source numerical conputing extension of Python. After input the related libraries, we start to read a image and show it.

The library `moviepy` is a library for video editing:cutting, connecting, header insertion, video synthesis(non-linear-editing), video processing and creating custom effects.

### 2.Related functions to deal with the image

* `cv2.inRange()`: To select color
* `cv2.fillPoly()`: To select goal area(ROI)
* `cv2.line()`: To draw a line in an image
* `cv2.addWeightd()`: To add two images with determined weight
* `cv2.cvtColor()`: To transfer images to other color space
* `cv2.imwrite()`: To write an image to a file
* `canny()`: To detect the boundaries in an image

### 3.Processing the image

Define a function named `processing_img` and set `raw_image` as a input parameter. 
First of all,Grayscale conversion on the original image with `grayscale()`. Then run `gaussian_blur()` and set kernel_size as 3. Use `canny()` function to detect the boundaries.
Finally, draw a quadrangle area in which contains the lane line. Use `weighted_img()` to find out the lane line in the quadrangle area.

---

## Summarize

* One shortcoming is that the detecting effect may be influenced by the environment such as the light, the road line and the rainy weather.
* Besides, if the lane line is curving, it may be a little difficult to detect it out.
* In the comming study, I would improve the method to detect the lane line.
