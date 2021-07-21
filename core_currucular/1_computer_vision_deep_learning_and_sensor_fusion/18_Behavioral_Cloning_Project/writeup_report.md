# Behavioral Cloning Project

[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

[//]: # (Image References)

[image1]: ./data/processed/model.png "Model Visualization"
[image2]: ./data/processed/training_history.png "Training history"
[image3]: ./data/processed/0_flipped.png "Flipped"
[image4]: ./data/processed/1_translated.png "Translated"
[image5]: ./data/processed/9_brighten.png "Brightend"
[image6]: ./data/processed/10_translated.png "Flipped & translated"
[image7]: ./data/processed/2_brighten.png "Flipped & translated & brightend"


### Files Submitted & Code Quality

#### 1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network 
* writeup_report.md or writeup_report.pdf summarizing the results

#### 2. Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing 
```sh
python drive.py models/model.h5
```

#### 3. Submission code is usable and readable

The model.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

### Model Architecture and Training Strategy

#### 1. An appropriate model architecture has been employed

My model consists of a convolution neural network with (3x3) and (5x5) filter sizes and depths between 24 and 64

```python
	model = Sequential()

    # crop the background
    model.add(Cropping2D(cropping=((65,20), (0,0)), input_shape=INPUT_SHAPE))
    
    # normalize the data
    model.add(Lambda(lambda x: (x / 255.0) - 0.5))
    # model.add(Lambda(lambda x: x/127.5-1.0, input_shape=INPUT_SHAPE))

    # feature layers
    model.add(Conv2D(24, (5, 5), activation='elu', strides=(2, 2)))
    model.add(Conv2D(36, (5, 5), activation='elu', strides=(2, 2)))
    model.add(Conv2D(48, (5, 5), activation='elu', strides=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='elu'))
    model.add(Conv2D(64, (3, 3), activation='elu'))
    model.add(Dropout(0.5))

    # classification layers
    model.add(Flatten())
    model.add(Dense(500, activation='elu'))
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))

    # just 1 output unit (steering angle)
    model.add(Dense(1))
```

The model includes RELU layers to introduce nonlinearity, and the data is normalized in the model using a Keras lambda layer. 

#### 2. Attempts to reduce overfitting in the model

The model contains dropout layers in order to reduce overfitting. But also i've added early stopping for if the validation loss doesn't decrease anymore.

```python
# prevent overfitting
EarlyStopping(
    monitor="val_loss",
    min_delta=0,
    patience=int(nb_epoch / 3),
)
```

The model was trained and validated on different data sets to ensure that the model was not overfitting. The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track.

#### 3. Model parameter tuning

The model used an adam optimizer, so the learning rate was not tuned manually. I've added an callback function that monitors the validation loss and adjusts the learning rate (by a factor 0.1) when the loss doesnt decrease much.

```python
# adjust the learning rate dynamically
ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.1,
    patience=int(nb_epoch / 4),
), 
```

#### 4. Appropriate training data

Training data was chosen to keep the vehicle driving on the road. I used a combination of center lane driving, recovering from the left and right sides of the road, but also driving in the opposite direction.

For details about how I created the training data, see the next section. 

### Model Architecture and Training Strategy

#### 1. Solution Design Approach

The overall strategy for deriving a model architecture was to start simpel and increment by small steps.

My first step was to use a simpel convolution neural network model with only 3 layers. 

In order to gauge how well the model was working, I split my image and steering angle data into a training and validation set. I found that my first model had a low mean squared error on the training set but a high mean squared error on the validation set. This implied that the model was overfitting. 

To combat the overfitting, I modified the model so that it drops layers to become more robust, and added some other overfitting preventing techniques. I've also added a few more layers to generalize better.

The final step was to run the simulator to see how well the car was driving around track one. At the end of the process, the vehicle is able to drive autonomously around the track without leaving the road.

#### 2. Final Model Architecture

The final model architecture consisted of a convolution neural network with five feature layers, and a dropout layer 

![final][image1]
*final model*

#### 3. Creation of the Training Set & Training Process

To capture good driving behavior, I recorded three laps on track one using center lane driving. I've had difficulties controlling the car. i wanted to use the mouse, be the feedback wasn't as smooth as i hoped. I've also drove the track backwards to get different steering angles and also different lighting.

During training i randomly select an image (left, center, right) and apply augmentation (horizontal flipping, translation, brightness) on the image (and steering angle), in order to make the model more robust.

![flipped][image3]
*Left = original image / right = flipped image*

![translated][image4]
*Left = original image / right = translated image*

![brightend][image5]
*Left = original image / right = Brightend image*

The augmentation section could also apply multiple augmentations per image.

![flipped-translated][image6]
*Left = original image / right = flipped & translated image*

![flipped-translated-brightend][image7]
*Left = original image / right = flipped & translated & brightend image*

I've made a generator that loops over all the data in random order (basically shuffling) processes it, and hand it over to the model.

I've set the number of epochs to 10, and i've devided the trainingset to the number of epochs, so in theory all images could be addressed once.

![training-history][image2]
*training history*

#### 4. Final video

So for the final video (run1 ;) ) i've first trained the model in GPU mode. It took approximate 1 hour and the early stopping kicked in at epoch 7.
```bash
python model.py
```

Then i've started the drive API, and started the simulator manually in the virtual environment.
```bash
python drive.py models/model.h5 data/run1
```

After one full lap, i've hit escape, and stopped the drive API. I needed to switch back to CPU mode start the (video) convert script, in order to create a video from the individual frames.
```bash
python video.py data/run1
```

Thats all folks