import numpy as np
import matplotlib.pyplot as plt
import imageio
import sys

nx, ny = (1000,1000)

iterations = 50
threshold = 2

#file_path = "/Users/alexiev/Documents/dev/github/PythonFractals/mandlebrot/"
file_path = "C:/Users/16479/dev/alex_github/PythonFractals/mandlebrot/"

frames = 400
xOffset = 0.02075047 
#xMin, xMax, yMin, yMax = (-1.5+xOffset, xOffset, -0.5, 1)
xMin, xMax, yMin, yMax = (-2.5+xOffset, 1+xOffset, -1.5, 2)
stepPercent = 0.02

fps = 20

def complexAdd(a, b):
    return [a[0] + b[0], a[1] + b[1]]

def complexMult(a, b):
    return [a[0]*b[0] - a[1]*b[1], a[0]*b[1] + b[0]*a[1]]
    # (a+bi)(c + di)
    # ac + adi + cbi - bd`

def isInSet(z, c, n):
    #zNext = (z**2)+c
    #print(complexAdd)
    zNext = complexAdd(complexMult(z, z), c)
    if n > iterations: return 0
    if zNext[0] > threshold: return 0
    if zNext[0] < threshold and n == iterations: return 1
    return isInSet(zNext, c, n+1)

def getMandlebrotSet(xMin, xMax, yMin, yMax):
    x = np.linspace(xMin, xMax, nx)
    y = np.linspace(yMin, yMax, ny)
    set = np.zeros([nx, ny])

    for r in range(nx):
        for c in range(ny):
            set[r][c] = isInSet([0, 0], [x[c], y[r]], 0)

    return set

def showLoadingBar(percent, total):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write("|"+ "#"*int(percent*total) + " "*(total-int(percent*total)) + "|")
    
images = []

def addFrame(frame):
    img = plt.figure(figsize = (8, 8))
    plt.imshow(frame)
    plt.savefig(file_path + "image.png")
    images.append(imageio.imread(file_path + "image.png"))
    plt.clf()

sets = []

for s in range(frames):
    step = stepPercent * (xMax - xMin)
    xMin+=step
    xMax-=step
    yMin+=step
    yMax-=step
    sets.append(getMandlebrotSet(xMin, xMax, yMin, yMax))
    addFrame(sets[s])
    showLoadingBar(s/frames, 50)

plt.close()
imageio.mimsave(file_path + "image.gif", images, fps=fps)


    

    