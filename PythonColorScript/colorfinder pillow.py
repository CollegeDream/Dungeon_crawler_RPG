from PIL import Image
import numpy as np

# py -m pip install --upgrade Pillow  
# py -m pip install --upgrade numpy

# Load image, ensure not palettised, and make into Numpy array
pim = Image.open('./Map Images/Room0.png').convert('RGB')
im  = np.array(pim)

# Define the blue colour we want to find - PIL uses RGB ordering
#color = (60,200,169) # room8's light color
#color = (120,177,209) # room7's light color
#color = (91,197,201) # room6's light color
#color = (143,143,143) # room5's light color
#color = (169,120,81) # room4's light color
#color = (209,202,120) # room3's light color
#color = (243,179,68) # room2's light color
#color = (148,209,120) # room1's light color
color = (154,110,184) # room0's light color
color1 = (7,255,252) # material node (1)
color2 = (7,255,30) # Loot (2)
color3 = (255,22,22) # Enemy (3)
color4 = (230,152,88) # Doors (4)
color5 = (0,0,0) #black

#Print Image into ASCII
ASCIIlist = ["'"] * 31
for i in range(im.shape[0]):
    for j in range(im.shape[1]):
        pixel = pim.getpixel((j,i))
        if(pixel==color):
            ASCIIlist[i] += 'E'
        elif(pixel==color1):
            ASCIIlist[i] += '*'
        elif(pixel==color2):
            ASCIIlist[i] += '$'
        elif(pixel==color3):
            ASCIIlist[i] += '!'
        elif(pixel==color4):
            ASCIIlist[i] += '@'
        elif(pixel==color5):
            ASCIIlist[i] += '8'
        else:
            ASCIIlist[i] += 'W'
    ASCIIlist[i] += "',"

for i in range(len(ASCIIlist)):
    print(ASCIIlist[i])

'''
Y, X = np.where(np.all(im==color,axis=2))
fileoutput = open("output.txt","w")

for p in range(0, len(X)):
    fileoutput.write('(8, ' + str(X[p]) + ', ' + str(Y[p]) + ', 0, FALSE),' + '\n')

fileoutput.write('#room8 material nodes\n')
Y, X = np.where(np.all(im==color1,axis=2))
for p in range(0, len(X)):
    fileoutput.write('(0, ' + str(X[p]) + ', ' + str(Y[p]) + ', 1, FALSE),' + '\n')
fileoutput.write('#room8 loot tiles\n')
Y, X = np.where(np.all(im==color2,axis=2))
for p in range(0, len(X)):
    fileoutput.write('(0, ' + str(X[p]) + ', ' + str(Y[p]) + ', 2, FALSE),' + '\n')
fileoutput.write('#room8 enemies\n')
Y, X = np.where(np.all(im==color3,axis=2))
for p in range(0, len(X)):
    fileoutput.write('(0, ' + str(X[p]) + ', ' + str(Y[p]) + ', 3, FALSE),' + '\n')
fileoutput.write('#room8 doors\n')
Y, X = np.where(np.all(im==color4,axis=2))
for p in range(0, len(X)):
    fileoutput.write('(0, ' + str(X[p]) + ', ' + str(Y[p]) + ', 4, FALSE),' + '\n')

fileoutput.close()
'''