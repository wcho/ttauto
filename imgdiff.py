import Image
import ImageChops
import math, operator

def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"
    h = ImageChops.difference(im1, im2).histogram()
    # calculate rms
    return math.sqrt(reduce(operator.add,
	map(lambda h, i: h*(i**2), h, range(1024))
	) / (float(im1.size[0]) * im1.size[1]))


def rms(im1, im2):
    h1 = im1.histogram()
    h2 = im2.histogram()
    return math.sqrt(reduce(operator.add,
	    map(lambda a,b: (a-b)**2, h1, h2))/len(h1))

vip = Image.open("vip.png")
vip0 = Image.open("vip0.png")
elev = Image.open("elev.png")
empty = Image.open("empty.png")
finish = Image.open("finish.png")
