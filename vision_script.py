import io
import os
import json
from google.cloud import vision
from google.cloud.vision import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='CloudComputing3-Vision.json'

def get_image():
	#read json
	with open('youtube_details.json') as json_data:
		d = json.load(json_data)
	#print(d)
	return d

def get_tags():

	dictionary=get_image()
##		for snip in item['snippet']:
#			for th in snip['thumbnails']:
#				for quality in th['high']:
#					print(quality['url'])
	#print(dictionary['items']['snippet'])
	client = vision.ImageAnnotatorClient()

	file_name = os.path.join(os.path.dirname(__file__),'bp.jpg')

	with io.open(file_name,'rb') as image_file:
		content = image_file.read()
		
	image = types.Image(content=content)

	response = client.label_detection(image=image)

	labels = response.label_annotations
		
	return labels