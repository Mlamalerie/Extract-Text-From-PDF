import os
import re
import glob
import logging
from PIL import Image
import pytesseract
import concurrent.futures
import time
import shutil
from difflib import SequenceMatcher
from itertools import repeat
from pdf2image import convert_from_path
from param import *

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
IR_PATH = r"G:\Mon Drive"
POPPLER_PATH = r"G:\Drive partagés\# Zone de Code #\LOCAL\HichimaPFE\poppler-0.68.0\bin"

class ReadPDF():

   def __init__(self,pdf_file,nb_pages = 1):
      self.pdf_file = pdf_file
      self.pages = convert_from_path(pdf_file, 500, poppler_path=POPPLER_PATH)
      self.image_counter = 0
      self.nb_pages = nb_pages

   def run(self):
      self.dirname = create_dir(create_dir("retrieve"),"%s" % (os.path.basename(self.pdf_file)))

      for page in self.pages:
         fname = os.path.join(self.dirname,f"page_{self.image_counter}.jpg")
         page.save(fname, 'JPEG')
         self.image_counter += 1

         if self.image_counter < self.nb_pages:
             self.image_counter += 1
         else:
            break

      return self.dirname

   def clean(self):
      shutil.rmtree(self.dirname)

class OCR:
   def __init__(self,dir):
      self.images = glob.glob(os.path.join(dir,"*.jpg")) 

   def extract_text(self):
      for image in self.images:
         img = Image.open(image)
         data = pytesseract.image_to_string(img,lang = 'eng',config='--psm 6')
      return data # string

def get_data_text_from_pdf_scanner(file):

   reader = ReadPDF(file)
   dir_where = reader.run() 

   ocr_generator = OCR(dir_where)
   data_txt = ocr_generator.extract_text() 

   reader.clean() 
   return data_txt.lower() 
