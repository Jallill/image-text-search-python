from PIL import Image
import pytesseract
from glob import glob
from multiprocessing import Process
from timeout import timeout
import os
import re
import shelve
import signal

def signal_handler(signum, frame):
    raise Exception("Timed out!")

imagesText = []

types = ('*.png', '*.jpg', '*.JPG', '*.PNG', '*.jpeg', '*.JPEG')

regexFilter = re.compile('^ *?$')
db = shelve.open('data/imagesText')

def readImage(image):
    if image in list(db.keys()): return
    
    im = Image.open(image)
    

    texts = pytesseract.image_to_string(im).split('\n')
    resultText = filter(lambda text: not regexFilter.match(text), texts)
    resultText = list(map(lambda text: text.lower(), resultText))
    db[image] = list(resultText)
    print(image ,":", db[image])


for type in types:
     for i, image in enumerate(glob(f'Images/{type}')):
        try:
            print(i)
            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(10)
            readImage(image)
        except Exception as e:
            print("Timeout:", e)

# procs = []

# for type in types:
#     for i, image in enumerate(glob(f'Images/{type}')):
#         proc = Process(target=readImage, args=(image,))
#         procs.append(proc)
#         proc.start()

# for proc in procs:
#     proc.join(10)

# for proc in procs:
#     proc.terminate()


print(len(imagesText))
os.system("killall -9 tesseract")
db.close()