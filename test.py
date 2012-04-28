import os
import math
import numpy
from array import array
from PIL import Image, ImageEnhance


def detect(start_x, start_y, fs_x, fs_y):
    brightness=0
    count=0
    for x in list(range(0, fs_x)):
            for y in list(range(0, fs_y)):
                br=pixels[start_x+x,start_y+y]
                count+=1
                brightness += get_brightness(br[0], br[1], br[1])
                if (x is 0) or (x is (fs_x-1)) or (y is 0) or (y is (fs_y-1)): 
                   # print start_x    
                    pixels[start_x+x,start_y+y]=(255,0,0)
    #Durschnittswert des "Sensors"
    return brightness/count


def get_brightness(r,g,b):
    #Berechnung der LUMA nach http://de.wikipedia.org/wiki/Luminanz
    return 0.2126*r + 0.7152*g + 0.0722*b

#Sensorgroesse
fs_x=1
fs_y=1
#Sensorabstand
fd_x=20
fd_y=20
#Sensor Gesamtgroesse
fc_x = fs_x+fd_x
fc_y = fs_y+fd_y

os.system("streamer -q -c /dev/video0 -o test.jpeg")
img = Image.open("test.jpeg")
pixels=img.load()
print img.size

#Berechne Anzahl der Messfelder:
fields_x=math.floor((img.size[0]-fs_x)/fc_x)+1
fields_y=math.floor((img.size[1]-fs_y)/fc_y)+1

#Berechne den Abstand vom Rand bis zum ersten Messfeld:
#start_x0= int(math.ceil((img.size[0]-(math.floor(fc_x*math.floor((img.size[0]-fs_x)/fc_x)+fs_x)))/2))
start_x0=int(math.ceil(img.size[0]-(fields_x*fc_x-fd_x))/2)
#start_y0= int(math.ceil((img.size[1]-(math.floor(fc_y*math.floor((img.size[1]-fs_y)/fc_y)+fs_y)))/2))
start_y0=int(math.ceil(img.size[1]-(fields_y*fc_y-fd_y))/2)
test=list()
for i in list(range(0,int(fields_x))):
    start_x = start_x0+i*fc_x
    for j in list(range(0,int(fields_y))):
        start_y = start_y0+j*fc_y
        #print (start_x, start_y)
        test.append(detect(start_x, start_y, fs_x, fs_y))
#        for x in list(range(start_x, start_x+fs_x)):
#            #print x
 #           for y in list(range(start_y, start_y+fs_y)):
 #               #print y
#                if (x is start_x) or (x is (start_x+fs_x-1))or(y is start_y) or (y is (start_y+fs_y-1)): 
                    #print start_x
#                    pixels[x,y]=(255,0,0)
#for start_x in list(range(start_x0, img.size[0], fc_x)):
#    #print start_x
#    for start_y in list(range(start_y0, img.size[1], fc_y)):
#        for x in list(range(start_x, start_x+fs_x)):
#            #print x
#            for y in list(range(start_y, start_y+fs_y)):
#                #print y
#                if (x is start_x) or (x is (start_x+fs_x-1))or(y is start_y) or (y is (start_y+fs_y-1)): 
#                    #print start_x
#                    pixels[x,y]=(255,0,0)
#                if (x is 291):
#                    print 'x'
test.sort()
brightness=numpy.mean(test)
print brightness
c=30
display_brightness = int(round((brightness)/15))
print display_brightness
display_b_file="/sys/class/backlight/acpi_video0/brightness"
os.system("sudo echo %d > %s" % (display_brightness, display_b_file))
os.system("rm test.jpeg")
img.show()
#img=ImageEnhance.Contrast(img)
#img.enhance(17).show()
