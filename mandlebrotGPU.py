import numpy as np
import matplotlib.pyplot as plt
import imageio
import sys
from numba import vectorize

nx, ny = (1000,1000)
frames = 1000
stepPercent = 0.0
fps = 60

iterations = 50
threshold = 2
 
#file_path = "/Users/alexiev/Documents/dev/github/PythonFractals/mandlebrot/"
file_path = "C:/Users/16479/dev/alex_github/PythonFractals/mandlebrotGPU/"
images = []

@vectorize(['float32(float32, float32, float32, float32, float32)'], target='cuda')
def computeMandlebrot(num, xMin, xMax, yMin, yMax):
    cr = xMin + (num%nx)*((xMax-xMin)/(nx-1))
    ci = yMin + (int(num/ny))*((yMax-yMin)/(ny-1))   
    zr = zi = znr = zni = 0
    n = 0
    while (znr < threshold and n < iterations):
        znr = zr*zr - zi*zi + cr
        zni = 2*zr*zi + ci
        zr = znr
        zi = zni
        n+=1
    return n

def showLoadingBar(percent, total):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write("|"+ "#"*int(percent*total) + " "*(total-int(percent*total)) + "|")

def addFrame(frame):
    img = plt.figure(figsize = (8, 8))
    plt.imshow(frame)
    plt.savefig(file_path + "image.png")
    images.append(imageio.imread(file_path + "image.png"))
    plt.clf()

def main():
    nums = np.arange(nx*ny, dtype=np.float32)
    xOffset = 0.02075047 
    xMin, xMax, yMin, yMax = (-2.5+xOffset, 1+xOffset, -1.5, 2)
    for s in range(frames):
        step = stepPercent * (xMax - xMin)
        xMin+=step
        xMax-=step
        yMin+=step
        yMax-=step
        addFrame(computeMandlebrot(nums, xMin, xMax, yMin, yMax).reshape((nx, ny)))   
        showLoadingBar(s/frames, 50)
    plt.close()
    imageio.mimsave(file_path + "image.gif", images, fps=fps)

if __name__ == "__main__":
    main()

