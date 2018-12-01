import numpy as np
import cv2

import argparse
from enum import Enum
import io
import base64

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

def detect_text(path):
	"""Detects text in the file."""
	client = vision.ImageAnnotatorClient()

	with io.open(path, 'rb') as image_file:
		content = image_file.read()
	#_, buffer = cv2.imencode('.jpg', path)
	#content = base64.b64encode(buffer)
	
	image = vision.types.Image(content=content)

	response = client.text_detection(image=image)
	texts = response.text_annotations

	if texts:
		texts = texts[0].description
	
	#test=cv2.imread(path)
	#cv2.imshow('img',test)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	#print(texts)
	
	return texts

def recognition_book(book_spine, img):
	book_list = list()
	prev = np.zeros(img.shape, dtype=np.uint8)
	for book, area in book_spine:
		width_start = min([area[0][0], area[1][0], area[2][0], area[3][0]])
		width_end = max([area[0][0], area[1][0], area[2][0], area[3][0]])
		height_start = min([area[0][1], area[1][1], area[2][1], area[3][1]])
		height_end = max([area[0][1], area[1][1], area[2][1], area[3][1]])
		#book = book[height_start:height_end, width_start:width_end]
		#book = np.rot90(book)
		book += prev
		cv2.imwrite("temp.jpg", book)
		text = detect_text("temp.jpg")
		if not text or text is None:
			prev = book
		else:
			book_list.append(text)
			prev = np.zeros(img.shape, dtype=np.uint8)
	return book_list