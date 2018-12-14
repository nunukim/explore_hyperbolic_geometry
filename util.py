import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib.animation as animation


def _dot(u,v, axis=-1):
    return np.sum(u*v, axis=axis, keepdims=True)

def _delta(u,v, axis=-1):
    return 2 * _dot(u-v, u-v, axis=axis) / ((1-_dot(u,u, axis))*(1-_dot(v,v, axis)))

def dist(u,v, axis=-1):
    u = np.asarray(u)
    v = np.asarray(v)
    return np.arccosh(1+_delta(u,v, axis=axis))
    
def translate(x,dx, axis=-1):
    v = np.asarray(dx)
    x = np.asarray(x)
    return ((1+2*_dot(v,x,axis)+_dot(x,x,axis))*v + (1-_dot(v,v,axis))*x) / (1+2*_dot(v,x,axis)+_dot(v,v,axis)*_dot(x,x,axis))

def rotate(x,theta):
    return np.dot(x, [[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])

    # v = np.asarray(v)
    # x = np.asarray(x)
    # return ((1+2*_dot(v,x,axis)+_dot(x,x,axis))*v + (1-_dot(v,v,axis))*x) / (1+2*_dot(v,x,axis)+_dot(v,v,axis)*_dot(x,x,axis))

def draw_circle():
    t = np.linspace(0,np.pi*2, 1025)
    plt.plot(np.cos(t), np.sin(t), color="gray", lw=.5)
    plt.xlim(-1.05, 1.05)
    plt.ylim(-1.05, 1.05)
    
