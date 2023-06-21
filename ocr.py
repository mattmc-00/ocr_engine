# OCR Engine template from https://builtin.com/data-science/python-ocr by Fahmi Nurfikri

from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import numpy as np
import os
import cv2

inputDataPath = r"C:\Users\matth\Documents\Python Scripts\ocr\data"
pngDataPath = r"C:\Users\matth\Documents\Python Scripts\ocr\data\pngs"
outputTextPath = r"C:\Users\matth\Documents\Python Scripts\ocr\out\txts"
popplerPath = r"C:\Program Files\poppler-0.68.0\bin"

# For file path "data/ufo.pdf", set inputFileName to "ufo"
inputFileName = "ufo"

inputFilePath = os.path.join(inputDataPath, '%s.pdf' % inputFileName)
print(inputFilePath)

class PdfPage:
    def __init__(self, pageNum, pngPath):
        self.pageNum = pageNum
        self.pngPath = pngPath

pages = []
images = convert_from_path(inputFilePath, 200, poppler_path = popplerPath)
for pageNum in range(len(images)):
    pageName = os.path.join(pngDataPath, '%s_%d.png' % (inputFileName, pageNum))
    
    imgArray = np.array(images[pageNum])
    # Use normalization, thresholding, and image blur
    normImgArray = np.zeros((imgArray.shape[0], imgArray.shape[1]))
    imgArray = cv2.normalize(imgArray, normImgArray, 0, 255, cv2.NORM_MINMAX)
    imgArray = cv2.threshold(imgArray, 100, 255, cv2.THRESH_BINARY)[1]
    imgArray = cv2.GaussianBlur(imgArray, (1, 1), 0)
    img = Image.fromarray(imgArray)
    img.save(pageName)
    
    page = PdfPage(pageNum, pageName)
    pages.append(page)

for page in pages:
    print(page.pageNum, page.pngPath)
    pageArray = np.array(Image.open(page.pngPath))
    text = pytesseract.image_to_string(pageArray)
    outFilePath = os.path.join(outputTextPath, '%s_%d.txt' % (inputFileName, page.pageNum))
    outFile = open(outFilePath, "w")
    outFile.write(text)
    outFile.close()
