import cv2 as cv

from resnet_152 import resnet152_model

import keras.backend as K
import numpy as np
import argparse
import sys

def load_model(modelFile):
	model_weights_path = modelFile
	img_width, img_height = 224, 224
	num_channels = 3
	num_classes = 196
	model = resnet152_model(img_height, img_width, num_channels, num_classes)
	model.load_weights(model_weights_path, by_name=True)
	return model

def load_image(imageFile):
	bgr_image = cv.resize(src = cv.imread(imageFile), dsize = (224, 224))
	rgb_image = cv.cvtColor(bgr_image, cv.COLOR_BGR2RGB)

	image = np.expand_dims(rgb_image, 0)
	return image

def predict_class(imageFile, modelFile):
	model = load_model(modelFile)
	image = load_image(imageFile)

	preds = model.predict(image)
	return np.argmax(preds) + 1

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--image", help="image to be processed")
	parser.add_argument("--model", help="graph/model to be executed")

	args = parser.parse_args()

	if args.image:
		imageFile = args.image
	else:
		print("Specify the image to be classified")
		sys.exit()

	if args.model:
		modelFile = args.model
	else:
		print("Specify model")
		sys.exit()

	model = load_model(modelFile)
	image = load_image(imageFile)

	preds = model.predict(image)
	print(np.argmax(preds))
	print(np.max(preds))

