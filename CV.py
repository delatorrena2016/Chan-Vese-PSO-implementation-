import numpy as np
from skimage import data, io, filters, color
import matplotlib.pyplot as plt
import scipy.io as sio
from mpl_toolkits import mplot3d
PI = 3.14159265358979323846264338327950288
EPS = 0.000001
class Parameters:
    h       = 0.25#PIXEL SPACING
    lambda1 = 1#INSIDE WEIGTHER; UNIFORM FOREGROUND VARYING BACKGROUND
    lambda2 = 1#OUTSIDE WEIGTHER; FG OBJECTS WITH VARYING GRAY LEVELS
    nu      = 0.5#CONTOUR AREA PENALIZER
    mu      = 1#CONTOUR LENGTH PENALIZER
    dt      = 0.1#TIME STEP
    p       = 1#LENGTH WEIGHT EXPONENT

p = Parameters()

##DIGITAL IMAGE AND CONTOUR LOADING 
img = io.imread('CPM3.jpg')
u0 = color.rgb2gray(img)#ERASING COLOR CHANNELS
#CONSTRUCT THE INITIAL LEVEL SET FUNCTION
rows, columns = np.shape(u0)#SIZE STORAGE MATRIX
phi = np.matrix([ [2 if (pow(pow(i-400,2)+pow(j-400,2),1/2)<=100) else -2 for j in range(columns)]for i in range(rows)])#COMPREHENSIVE LIST MATRIX

#INTENSITY SEGMENTED REGIONS
u0I = np.multiply(u0,(phi>=0))#MASK NOTATION
u0O = np.multiply(u0,(phi<0))

#FIND INDEX OF CONDITIONED VALUES
flatMI = np.array((phi>=0).flatten('F'))#BOOLEAN (LINEAR DATA), BY INSIDE CIRCLE CONDITION
LinearInI = np.where(flatMI==True)[1]#LINEAR INDEX OF TRUE BOOLEAN VALUE DATA 
flatMO = np.array((phi<0).flatten('F'))
LinearInO = np.where(flatMO==True)[1]#SECOND OF TUPLE (THIS ONE) TRUE BOOLEAN 

#INITIAL MEAN INTENSITIES
c1 = np.divide(u0I.sum(), max(LinearInI.shape))#MAXIMUM LENGTH OF ALL DIMENSIONS
c2 = np.divide(u0O.sum(), max(LinearInO.shape))


#PDE FINITE DIFFERENCES

phi = np.array(phi)#FOR MEAN VALUES YOU NEEDED MATRIX 'CAUSE OF WHERE, HERE YOU NEED TO OPERATE IT AS NARRAY

C1 = np.array([[1/(pow(EPS + pow(phi[i+1][j]-phi[i][j],2) + (pow(phi[i][j+1]-phi[i][j-1],2))/4,1/2)) for j in range(columns)] for i in range(rows)])
C2 = np.array([[1/(pow(EPS + pow(phi[i][j]-phi[i-1][j],2) + (pow(phi[i-1][j+1]-phi[i-1][j-1],2))/4,1/2)) for j in range(columns)] for i in range(rows)])
C3 = np.array([[1/(pow(EPS + (pow(phi[i+1][j]-phi[i-1][j],2))/4 + pow(phi[i][j+1]-phi[i][j],2),1/2)) for j in range(columns)] for i in range(rows)])
C4 = np.array([[1/(pow(EPS + (pow(phi[i+1][j-1]-phi[i-1][j-1],2))/4 + pow(phi[i][j]-phi[i][j-1],2),1/2)) for j in range(columns)] for i in range(rows)])

a=np.multiply(phi,phi)
deltaPhi = np.array([ [p.h/(PI*(p.h**2 + a[i][j])) for j in range(columns)] for i in range(rows)])
L = 1#??
Factor = p.dt*deltaPhi*p.mu*p.p*pow(L,p.p-1)
F = p.h/(p.h+Factor*(C1+C2+C3+C4))
Factor = Factor/(p.h+Factor*(C1+C2+C3+C4))
F1 = Factor*C1
F2 = Factor*C2
F3 = Factor*C3
F4 = Factor*C4
Pij = np.array([ [ p.dt*deltaPhi[i][j]*(p.nu + p.lambda1*pow(u0[i][j] - c1,2) + p.lambda2*pow(u0[i][j] - c2,2)) for j in range(columns)] for i in range(rows)])

'''
#plt.imshow(u0,cmap='gray')#DRAWS
#plt.show()#PRINTS ONTO GUI
y = np.linspace(0,902,903)
x = np.linspace(0,721,722)
xv, yv = np.meshgrid(x,y)
xv.transpose()
yv.transpose()
fig = plt.figure()
ax = plt.axes(projection='3d')
#ax.contour3D(xv, yv, phi, 2, cmap='binary')
ax.plot_wireframe(xv, yv, u0O, color='black')
'''
'''
#matf = sio.loadmat('c1.mat')#CONTOUR
#phi = matf['phi'].copy()#PHI DOESN'T OWN DATA IT IS A POINTER, SO WE COPY IT
#phi.resize(903,722)#SO WE CAN MULTIPLY ELEMENT WISE
r = np.matrix([[1,2,3,4], [1,2,3,4], [-3, -2, -2, -2]])#MANUAL COLUMN AND ROW IS NOT A MATRIX
#out = np.
#phiO=-pow(pow(x-c,2)+pow(y-h,2),1/2)

inside = [ [phi[i][j] for j in range(columns) if (phi[i][j]<0)]for i in range(rows)]#COMPREHENSIVE LIST MATRIX
outside = [ [phi[i][j] for j in range(columns) if (phi[i][j]>=0)]for i in range(rows)]
rows, columns = np.shape(u0)#SIZE STORAGE MATRIX
'''