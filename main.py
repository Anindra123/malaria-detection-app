import os
import pickle
import PIL
import numpy as np;

from PIL import Image
from skimage import color,transform;

ENSEMBLE_PATH = 'weights/ensemble_malaria_model'
PCA_PATH = 'weights/pca_malaria_weights'

pca_transform = pickle.load(open(PCA_PATH,'rb'));
ensemble_model = pickle.load(open(ENSEMBLE_PATH,'rb'));

# resize the obtained image
def resize_image(image_file,shape):
    target_shape = shape;
    img = Image.open(image_file);
    actual_shape = img.size;
    aspect_ration = float(target_shape) / max(actual_shape)
    new_shape = tuple([int(aspect_ration * shape) for shape in actual_shape])
    new_img = Image.new('RGB',(target_shape,target_shape));
    new_img.paste(img,( ( target_shape - new_shape[0] )//2, ( target_shape - new_shape[1] )//2 ))

    return new_img;

# to differentiate the dark pixel of parsitized cell
def brighten_background_pixel(image_file):
    # getting the max pixel value which is the brightest
    max_pixel =np.max(image_file)

    # setting the pixel values of those pixel in image with value of
    # 0.0 or black background pixel are set this pixel value
    image_file[image_file == 0.0] = max_pixel

    return image_file;


# preprocess the image to remove noise before extracting feature
def preprocessing(image_file):
    resized_image = resize_image(image_file,shape=224)
    resized_image = np.array(resized_image)
    # convert the image to grayscale to bright the background pixel
    gray_image = color.rgb2gray(resized_image)
    brighten_image = brighten_background_pixel(gray_image)
    return brighten_image;


# extract image features
def feature_extraction( image_file):
    cleaned_image =preprocessing(image_file)
    img = transform.resize(cleaned_image.reshape(224,224),(100,100))
    image_feature = img.reshape(-1)

    return image_feature;

def predict( image_file ):
    img = feature_extraction(image_file)
    img = np.array([img]);
    # scale the feature down to only needed features
    transformed_img = pca_transform.transform(img)
    # predict from the obtained features
    prediction = ensemble_model.predict(transformed_img)

    return 'Parasitized' if prediction == 1.0 else 'Uninfected'