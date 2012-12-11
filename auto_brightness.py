import os, time
#import numpy
from optparse import OptionParser
from cv2 import *



def get_brightness(img, MAX = 2948310. ):
	#Berechnung der LUMA nach http://de.wikipedia.org/wiki/Luminanz
	try:
		r, g, b = (img[:,:,i].mean() for i in range(3))
		return (0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))**0.5 * MAX/ float(options.m) 
	except:
		return 0


usage = "usage: %prog [options] arg1 arg2"
parser = OptionParser(usage=usage)
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=True, help="print brightness [default]")
parser.add_option("-f", "--file", action="store", dest="file",
				  default="/sys/class/backlight/intel_backlight/brightness", help="path to brightness file [default]")
parser.add_option("-s", "--sleep", action="store", dest="sleep",
				  default=10., help="sleep [default]")

parser.add_option("-m", action="store", dest="m",
				  default=210., help="m [default]")


if __name__ == '__main__':
	
	
	(options, args) = parser.parse_args()
	cam = VideoCapture(0)   # 0 -> index of camera
	t = True
	while t:
		# initialize the camera
		
		s, img = cam.read()
		
		display_brightness = get_brightness(img)
		if options.verbose:
			print(display_brightness)
		try:
			os.system("sudo echo %d > %s" % (display_brightness, options.file))
		except: pass
		time.sleep(float(options.sleep))
