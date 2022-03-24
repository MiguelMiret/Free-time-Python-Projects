# A code to plot statically in 3D a dynamical system's evolution (currently lorenz attractor).

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d


plt.style.use('dark_background')

def variables():
    dt = 0.001
    T = 20
    t0 = 0
    N = int((T-t0)/dt)
    t = np.linspace(0,T,N+1)

    return(dt,t)
    
def plot(t,x,y,z):

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(x,y,z)

    return fig

def statefunction(x, y, z, s, r, b):
    x_dot = s*(y - x)
    y_dot = r*x - y - x*z
    z_dot = x*y - b*z
    return (x_dot, y_dot, z_dot)


def DS(dt,t): #Lorentz

    #parameters
    s = 10
    r = 28
    b = 2.667

    # variables
    x = np.zeros(np.size(t))
    y = np.zeros(np.size(t))
    z = np.zeros(np.size(t))

    #initial conditions
    x[0] = 0.1
    y[0] = 0.1
    z[0] = 0.1

    #computation

    for i in range(0,np.size(t)-1):
        (x_dot,y_dot,z_dot) = statefunction(x[i],y[i],z[i],s,r,b)
        x[i+1] = x[i] + dt*x_dot
        y[i+1] = y[i] + dt*y_dot
        z[i+1] = z[i] + dt*z_dot

    return(x,y,z)


def main():

    (dt,t) = variables()

    (x,y,z) = DS(dt,t)

    fig = plot(t,x,y,z)
    plt.show()







if __name__ == '__main__':
	main()
