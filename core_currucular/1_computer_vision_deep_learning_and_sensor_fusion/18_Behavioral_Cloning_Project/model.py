# -*- coding: utf-8 -*-

# python core modules
import os

# python core modules
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.utils import plot_model
from keras.models import Sequential
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from sklearn.model_selection import train_test_split
from keras.layers import Lambda, Conv2D, Cropping2D, MaxPooling2D, Dropout, Dense, Flatten

#for debugging, allows for reproducible (deterministic) results 
np.random.seed(0)

# set defaults
IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS = 160, 320, 3
INPUT_SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)
DATA_DIR = os.path.join(os.getcwd(), 'data', 'raw', 'sample driving data')
PROCESSED_DIR = os.path.join(os.getcwd(), 'data', 'processed')


def load_image(image_file):
    # read the image
    image = cv2.imread(os.path.join(DATA_DIR, image_file.strip()))

    # convert it to from the opencv BGR space to the RGB space 
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def save_images(file_name, original, image):
    # convert RGB back to BGR (for saving)
    original = cv2.cvtColor(original, cv2.COLOR_RGB2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # combine the 2 images into 1
    combined = np.hstack([original, image])

    # define the file_path
    file_path = os.path.join(PROCESSED_DIR, file_name)

    # save the image
    cv2.imwrite(file_path, combined)


def choose_image(center, left, right, steering_angle):
    # define the steering correction (when using the left & right camera)
    steering_correction = 0.2
    
    # random choose (0=right, 1=left, 2=center)
    choice = np.random.choice(3)
    if choice == 0:
        return load_image(left), steering_angle + steering_correction
    elif choice == 1:
        return load_image(right), steering_angle - steering_correction
    return load_image(center), steering_angle


def random_flip(image, steering_angle):
    if np.random.rand() < 0.5:
        image = cv2.flip(image, 1)
        steering_angle = -steering_angle
    return image, steering_angle


def random_translate(image, steering_angle, range_x, range_y):
    trans_x = range_x * (np.random.rand() - 0.5)
    trans_y = range_y * (np.random.rand() - 0.5)
    steering_angle += trans_x * 0.002
    trans_m = np.float32([[1, 0, trans_x], [0, 1, trans_y]])
    height, width = image.shape[:2]
    image = cv2.warpAffine(image, trans_m, (width, height))
    return image, steering_angle


def random_brightness(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    ratio = 1.0 + 0.4 * (np.random.rand() - 0.5)
    hsv[:,:,2] =  hsv[:,:,2] * ratio
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)


def augument(center, left, right, steering_angle, range_x=100, range_y=10):
    # random_value = str(np.random.randint(0, high=1000))

    # choose an image (left, center, right)
    original, steering_angle = choose_image(center, left, right, steering_angle)

    # random flip the image
    image, steering_angle = random_flip(original, steering_angle)
    # save_images(random_value + '_flipped.png', original, image)

    # random translate the image
    image, steering_angle = random_translate(image, steering_angle, range_x, range_y)
    # save_images(random_value + '_translated.png', original, image)

    # random brighten the image
    image = random_brightness(image)
    # save_images(random_value + '_brighten.png', original, image)

    return image, steering_angle


def batch_generator(image_paths, steering_angles, batch_size, is_training):
    # initialize empty arrays
    images = np.empty([batch_size, IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS])
    steers = np.empty(batch_size)
    
    # loop indefenitly
    while True:
        i = 0
        
        # loop over all images in random order (shuffle)
        for index in np.random.permutation(image_paths.shape[0]):
            
            # collect the data
            center, left, right = image_paths[index]
            steering_angle = steering_angles[index]
            
            # augment the data, while training
            if is_training and np.random.rand() < 0.6:
                image, steering_angle = augument(center, left, right, steering_angle)
                
            # load the image for inferencing
            else:
                image = load_image(center) 

            # add the image and steering angle to the batch
            images[i] = image
            steers[i] = steering_angle
            
            i += 1
            if i == batch_size:
                break
        
        yield images, steers


def plot_history(history):
    plt.figure(figsize=(8, 8))

    # plot the loss
    plt.subplot(2, 1, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.legend(loc='upper right')
    plt.ylabel('Loss')

    # plot the learning rate
    plt.subplot(2, 1, 2)
    plt.plot(history.history['lr'], label='Learning rate')
    plt.ylabel('Learning rate')
    plt.xlabel('Epoch')

    # save the history
    plt.savefig(os.path.join(PROCESSED_DIR, 'training_history.png'))


def load_data():
    # load the csv into a dataframe
    df = pd.read_csv(os.path.join(DATA_DIR, 'driving_log.csv'))

    # define the features and the target
    X = df[['center', 'left', 'right']].values
    y = df['steering'].values

    # split the data
    return train_test_split(X, y, test_size=0.2, random_state=0)


def build_model():
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

    # plot the model
    plot_model(model, to_file=os.path.join(PROCESSED_DIR, 'model.png'), show_shapes=True)

    return model


def train_model(model, X_train, X_valid, y_train, y_valid):    
    # hyperparameters
    nb_epoch = 10
    batch_size = 64
    learning_rate = 1.0e-4
    samples_per_epoch = int(len(X_train) / nb_epoch)


    # compile the model
    model.compile(
        loss='mean_squared_error', 
        optimizer=Adam(lr=learning_rate)
    )

    # train the model
    history = model.fit_generator(
        batch_generator(X_train, y_train, batch_size, True),
        samples_per_epoch=samples_per_epoch,
        nb_epoch=nb_epoch,
        max_q_size=1,
        validation_data=batch_generator(X_valid, y_valid, batch_size, False),
        nb_val_samples=len(X_valid),
        callbacks=[
            # make checkpoints
            ModelCheckpoint(
                'models/model-{epoch:03d}.h5',
                monitor='val_loss',
                verbose=0,
                save_best_only=True,
                mode='auto'
            ),

            # adjust the learning rate dynamically
            ReduceLROnPlateau(
                monitor="val_loss",
                factor=0.1,
                patience=int(nb_epoch / 4),
            ), 

            # prevent overfitting
            EarlyStopping(
                monitor="val_loss",
                min_delta=0,
                patience=int(nb_epoch / 3),
            )
        ],
        verbose=1
    )

    # save the model
    model.save('models/model.h5')

    # plot the history
    plot_history(history)


def main():
    # load data
    data = load_data()
    
    # build model
    model = build_model()
    
    # train model on data, it saves as model.h5 
    train_model(model, *data)


if __name__ == '__main__':
    main()