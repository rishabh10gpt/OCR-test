import PIL
import argparse
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR,draw_ocr

parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--image', type=str, required=True, help="Image name for which html file is to be generated.")
parser.add_argument('--lang', type=str, default="en", help="Name of the language of the image file.")
parser.add_argument('--outhtml',type=str, default="output.html", help="Name of the html file to be generated. The file name should end with html")
def create_ocr_html(ocr,img_path,out_html="output.html",lang="en"):
    result = ocr.ocr(img_path, cls=True)
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    html = ""
    para = txts[0]
    left = boxes[0][0][0]
    top = boxes[0][0][1]
    width = (boxes[0][1][0] - boxes[0][0][0])
    for i in range(1, len(boxes)):
        if boxes[i][0][1] - boxes[i-1][0][1] < 55 and boxes[i][1][0] - boxes[i-1][1][0] < 60:
            para = para + " " + txts[i] + " "
            width = max(width, boxes[i][1][0] - boxes[i][0][0]) 
        else:
            lineht = boxes[i-1][3][1] - boxes[i-1][0][1] 
            if lineht > 50:
                width = width * 1.2
            elem = "<p contenteditable style='position: absolute; top: {}px; left: {}px; width: {}px; font-size: {}px;'>{}</p>".format(top, left, width, lineht, para)
            html += elem
            para = txts[i]
            left = boxes[i][0][0]
            top = boxes[i][0][1]
            width = (boxes[i][1][0] - boxes[i][0][0]) 
    if len(para) > 0:
        lineht = boxes[i-1][3][1] - boxes[i-1][0][1] 
        elem = "<p contenteditable style='position: absolute; top: {}px; left: {}px; width: {}px; font-size: {}px;'>{}</p>".format(top, left, width, lineht, para)
        html += elem
    with open(out_html, "w") as e:
        e.write(html)
    print("Html file {} generated.".format(out_html))
    return html

if __name__=="__main__":
    args = parser.parse_args()
    img_path = args.image
    lang = args.lang
    outhtml = args.outhtml
    supported_languages = ["en","ch","hi"]
    if lang not in supported_languages:
        print("Language not Supported, Please enter languages in : ",supported_languages)
        exit(0)
    if outhtml.split(".")[-1]!="html":
        print("Enter the outhtml ending with html only!")
        exit(0)
    ocr = PaddleOCR(use_angle_cls=True, lang=lang)
    create_ocr_html(ocr,img_path,out_html=outhtml,lang=lang)