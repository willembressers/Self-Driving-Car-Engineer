# **Finding Lane Lines on the Road** 

## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file. But feel free to use some other method and submit a pdf if you prefer.

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./test_images_output/solidYellowCurve2.jpg "solidYellowCurve2"

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

I've written the pipeline in a separate function so i could apply it on images and video's. This helped me to debug on images and then apply it on video's.

Initially my pipeline consisted on 5 steps: 
* grayscale (convert image to grayscale)
* blurring (blur the image, for better edge detection)
* canny (detect edges)
* roi (crop edges to the region of interest)
* hough (transform edges to lines)

After this worked i've improved the script by adding:
* split lines (split the lines into left and right bins)
* average lines (average mulitple lines into a single line )

![alt text][image1]

### 2. Identify potential shortcomings with your current pipeline

I've applied my script on the challenge code and saw that sometimes that averaging line resulted in an error. I noticed that splitting the lines into their (left, right) bins resulted in potentially empy bins. 

### 3. Suggest possible improvements to your pipeline

a possible sollution could be to "remember" the averaged lines from the previous frame (in a video), so when a bin is empty, it's likely that the lines from the previous frame would fit reasonbly well.
