import io
import os
from pandas import DataFrame
from google.cloud import translate
from vision_script import get_tags
from gsheet import addObjects_Message

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='CloudComputing3-Maps.json'

def translate_text(text,tag,det_lang,tr_msg,target='fr'):
	translate_client = translate.Client()
	result = translate_client.translate(text, target_language=target)
	
	print('Text',result['input'])
	print('Translation',result['translatedText'])
	print('Detected source language: ', result['detectedSourceLanguage'])
	tag.append(result['input'])
	det_lang.append(result['detectedSourceLanguage'])
	tr_msg.append(result['translatedText'])

	
def write_to_excel(tag,det_lang,tr_msg):
	l1=[1,2,3,4]
	df = DataFrame({'Message': tag, 'Translated message': tr_msg, 'Detected language':det_lang})
	df.to_excel('Catalog.xlsx',sheet_name='Foaie1',index=False)



example_text= '''Hello'''

labels_english=get_tags()
tag=list()
det_lang=list()
tr_msg=list()

for label in labels_english:
	translate_text(label.description,tag,det_lang,tr_msg)
	write_to_excel(tag,det_lang,tr_msg)
addObjects_Message(tag,tr_msg)